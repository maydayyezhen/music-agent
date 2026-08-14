from __future__ import annotations

from copy import deepcopy
from typing import Any

from src.midi.pitches import note_number

from src.instruments.common import assign_guitar_note, note, position, root_pc
from src.melody.tonality import resolve_tonality

RELATIONSHIPS = {
    "introduce", "repeat", "variation", "sequence", "extension", "fragmentation",
    "augmentation", "compression", "continuation", "answer", "climax", "resolution",
}


def _nearest_scale_pitch(target: int, scale_pcs: set[int], low: int, high: int) -> int:
    target = max(low, min(high, target))
    for distance in range(13):
        for value in (target, target - distance, target + distance):
            if low <= value <= high and value % 12 in scale_pcs:
                return value
    return target


def _chord_at(phrase: dict[str, Any], beat: float, beats_per_bar: int) -> str:
    spans = phrase["harmony"]
    selected = spans[0]["chord"]
    for span in spans:
        if position(span["at"], beats_per_bar) <= beat + 1e-6:
            selected = span["chord"]
        else:
            break
    return str(selected)


def _operations(base: list[dict[str, Any]], relationship: dict[str, Any], phrase_index: int) -> list[dict[str, Any]]:
    result = deepcopy(base)
    operations = set(relationship.get("motif_operations", []))
    if "fragmentation" in operations:
        result = result[len(result) // 2:]
    if "compression" in operations:
        for item in result:
            item["offset"] *= 0.75
            item["duration"] *= 0.75
    if "augmentation" in operations:
        for item in result:
            item["offset"] *= 1.25
            item["duration"] *= 1.25
    transpose = 0
    if "transpose_up" in operations or relationship["relationship"] in {"sequence", "climax"}:
        transpose += 2 + min(phrase_index, 2)
    if "transpose_down" in operations:
        transpose -= 2
    for item in result:
        item["degree"] = int(item["degree"]) + transpose
    if "rhythmic_extension" in operations or "extension" in operations:
        result[-1]["duration"] += 0.75
    if "change_ending" in operations:
        result[-1]["degree"] += 2 if phrase_index % 2 else -1
    if relationship["relationship"] == "resolution":
        result[-1]["degree"] = 0
    return result


def _velocity_delta(action: str, gesture: str, note_index: int, start: float,
                    beats_per_bar: int, item: dict[str, Any]) -> int:
    """Make the attack pattern describe guitar technique instead of a flat piano roll."""
    if action in {"hammer_on", "pull_off"}:
        delta = -13
    elif action == "slide":
        delta = -7
    elif action == "vibrato":
        delta = -3
    elif action in {"bend", "bend_release"}:
        delta = 4
    elif "repeated" in gesture:
        delta = (4, -6, -2)[note_index % 3]
    else:
        delta = (2, -2, 0, -4)[note_index % 4]
    beat = start % beats_per_bar
    if beat < 0.03:
        delta += 3
    return delta + int(item.get("velocity_delta", 0))


def _shape_note_lengths(events: list[dict[str, Any]], phrase: dict[str, Any],
                        beats_per_bar: int) -> list[dict[str, Any]]:
    """Turn grid durations into guitar-like gates while keeping the line monophonic-safe.

    Repeated pitches need a short release so the next pick can speak. Entering hammer-ons,
    pull-offs and slides are held almost to the next onset, while target holds keep their
    authored length. The old implementation simply clipped every note at the next onset,
    making very different gestures sound like identical rectangular blocks.
    """
    realization = phrase.get("realization", {})
    repeated_cycle = tuple(float(value) for value in realization.get(
        "repeated_pick_gate_cycle", [0.58, 0.82, 0.68]
    ))
    picked_cycle = tuple(float(value) for value in realization.get(
        "picked_gate_cycle", [0.88, 0.96, 0.79, 0.92]
    ))
    if not repeated_cycle or not picked_cycle:
        raise ValueError("long-form gate cycles must not be empty")

    ordered = sorted(events, key=lambda event: position(event["at"], beats_per_bar))
    for index, (current, following) in enumerate(zip(ordered, ordered[1:])):
        current_start = position(current["at"], beats_per_bar)
        next_start = position(following["at"], beats_per_bar)
        onset_gap = max(0.05, next_start - current_start)
        authored = float(current["duration"])
        current_pitch = note_number(current["pitch"])
        next_pitch = note_number(following["pitch"])
        current_action = str(current.get("_action", "pick"))
        next_action = str(following.get("_action", "pick"))
        gesture = str(current.get("_gesture", ""))

        if current_pitch == next_pitch:
            gate = repeated_cycle[index % len(repeated_cycle)]
            shaped = min(authored, onset_gap * gate)
        elif next_action in {"hammer_on", "pull_off"}:
            shaped = min(authored, onset_gap * 0.985)
        elif next_action == "slide":
            shaped = min(authored, onset_gap * 0.94)
        elif current_action == "vibrato" or "hold" in gesture or "landing" in gesture:
            shaped = min(authored, onset_gap * 0.99)
        else:
            gate = picked_cycle[index % len(picked_cycle)]
            shaped = min(authored, onset_gap * gate)
        current["duration"] = round(max(0.05, shaped), 3)
    return ordered


def compile_long_form_lead(phrase: dict[str, Any], beats_per_bar: int,
                           tuning: list[int], max_fret: int, base_velocity: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    arc = phrase["section_arc"]
    relationships = phrase["phrase_relationships"]
    motif = phrase["motif_seed"]
    rules = phrase.get("long_form_phrase_rules", {})
    bars = int(arc["bars"][1]) - int(arc["bars"][0]) + 1
    scale_pcs, tonality = resolve_tonality(phrase)
    low, high = [int(value) for value in phrase.get("register_midi", [57, 88])]
    root = _nearest_scale_pitch(int(phrase.get("motif_root_midi", 64)), scale_pcs, low, high)
    target_pitch = note_number(arc["delayed_target"]["pitch"])
    target_bar = int(arc["delayed_target"]["bar"])
    realization = phrase.get("realization", {})
    peak_hold_beats = float(realization.get("peak_hold_beats", 1.5))
    final_resolution_beats = float(realization.get("final_resolution_beats", 1.5))
    state: dict[str, Any] = {
        "active_motif": phrase.get("motif_id", "motif_A"), "motif_version": 0,
        "current_register": arc["opening_register"], "direction": "ascending",
        "tension": float(arc["energy_curve"][0]), "resolved": False,
        "continuation_required": True, "target_pitch": target_pitch, "target_bar": target_bar,
        "last_interval": 0, "last_note_function": "chord_tone",
        "phrase_breath_remaining": 0.0, "cadence_strength": 0.0,
    }
    events: list[dict[str, Any]] = []
    state_trace: list[dict[str, Any]] = []
    preferred_fret = 7
    previous_pitch = root
    peak_bar = int(arc["peak_bar"])

    for phrase_index, relation in enumerate(relationships):
        start_bar, end_bar = [int(value) for value in relation["bars"]]
        state_trace.append({"phrase_id": relation["phrase_id"], "point": "start", **deepcopy(state)})
        transformed = _operations(motif, relation, phrase_index)
        phrase_start = (start_bar - 1) * beats_per_bar
        phrase_end = end_bar * beats_per_bar
        for note_index, item in enumerate(transformed):
            is_relation_end = note_index == len(transformed) - 1
            is_peak_target = relation["relationship"] == "climax" and is_relation_end
            is_final = relation["relationship"] == "resolution" and is_relation_end
            start = phrase_start + float(item["offset"])
            if is_peak_target:
                start = max(phrase_start, phrase_end - peak_hold_beats)
            if is_final:
                start = max(phrase_start, phrase_end - final_resolution_beats)
            if start >= phrase_end - 0.1:
                continue
            bar = int(start // beats_per_bar) + 1
            progress = (bar - 1) / max(1, bars - 1)
            contour = round((peak_bar - 1) * progress * 5 / max(1, peak_bar - 1))
            desired = root + int(item["degree"]) + contour
            if bar < target_bar:
                desired = min(desired, target_pitch - max(2, target_bar - bar))
            if bar == target_bar and is_peak_target:
                desired = target_pitch
            if bar > peak_bar:
                desired -= round((bar - peak_bar) * 0.7)
            if is_final:
                desired = root
            pitch = _nearest_scale_pitch(desired, scale_pcs, low, high)
            chord = _chord_at(phrase, start, beats_per_bar)
            chord_pc = root_pc(chord)
            function = "chord_tone" if pitch % 12 in {
                chord_pc, (chord_pc + 3) % 12, (chord_pc + 4) % 12, (chord_pc + 7) % 12
            } else "non_chord_tone"
            duration = min(float(item["duration"]), phrase_end - start)
            if is_peak_target:
                duration = min(max(duration, peak_hold_beats), phrase_end - start)
            if is_final:
                duration = min(max(duration, final_resolution_beats), phrase_end - start)
            cross_bar_reason = item.get("cross_bar_reason")
            bar_end = (int(start // beats_per_bar) + 1) * beats_per_bar
            if cross_bar_reason:
                requested = bar_end - start + float(item.get("cross_bar_tail_beats", 0.2))
                duration = min(max(duration, requested), float(item["duration"]) + 0.5, phrase_end - start)
            elif not (is_peak_target or is_final):
                duration = min(duration, bar_end - start)

            allow_articulations = bool(realization.get("enable_articulations", False))
            allow_pitch_bend = bool(realization.get("enable_pitch_bend", False))
            action = str(item.get("action", "pick")) if allow_articulations else "pick"
            if is_peak_target or is_final:
                action = "vibrato"
            arts: list[str] = []
            if action in {"hammer_on", "pull_off"}:
                arts.extend([action, "legato"])
            elif action == "slide":
                arts.extend(["slide", "legato"])
            elif action in {"bend", "bend_release"} and allow_pitch_bend:
                arts.append(action)
            elif action == "vibrato":
                arts.extend(["vibrato", "sustain"])
            if is_final:
                arts.append("resolution")

            string, fret = assign_guitar_note(pitch, tuning, max_fret, preferred_fret)
            preferred_fret = fret
            gesture = str(item.get("gesture", ""))
            velocity = (
                base_velocity
                + round(float(arc["energy_curve"][bar - 1]) * 10)
                + (5 if bar == peak_bar else 0)
                + _velocity_delta(action, gesture, note_index, start, beats_per_bar, item)
            )
            event = note(
                pitch, start, duration, velocity, beats_per_bar, arts,
                _string=string, _fret=fret, _phrase_id=relation["phrase_id"],
                _relationship=relation["relationship"], _motif_version=phrase_index,
                _note_function=function, _cross_bar=bool(cross_bar_reason),
                _cross_bar_reason=cross_bar_reason,
                _rest_type_after=item.get("rest_type_after"),
                _gesture=gesture, _action=action,
                _authored_duration=round(float(item["duration"]), 3),
            )
            if "bend" in arts or "bend_release" in arts:
                event["bend_semitones"] = float(item.get("bend_semitones", 2.0))
            if "slide" in arts and item.get("slide_from_semitones") is not None:
                event["slide_from_semitones"] = float(item["slide_from_semitones"])
            if action in {"hammer_on", "pull_off"} and allow_pitch_bend:
                transition = previous_pitch - pitch
                if 0 < abs(transition) <= 2:
                    event["slide_from_semitones"] = float(transition)
                    event["_legato_pitch_fallback"] = True
            if "vibrato" in arts:
                event["vibrato"] = item.get(
                    "vibrato",
                    {"delay": 0.28 if is_peak_target or is_final else 0.35,
                     "depth": 0.30, "rate": 5.0},
                )
            events.append(event)
            state["last_interval"] = pitch - previous_pitch
            state["direction"] = "ascending" if pitch > previous_pitch else (
                "descending" if pitch < previous_pitch else "level"
            )
            state["last_note_function"] = function
            state["tension"] = float(arc["energy_curve"][bar - 1])
            state["current_register"] = "high" if pitch >= 76 else ("mid_high" if pitch >= 69 else "mid")
            previous_pitch = pitch
        resolution = relation["resolution"]
        state["motif_version"] = phrase_index + 1
        state["resolved"] = resolution == "strong"
        state["continuation_required"] = not state["resolved"] and relation.get("continuation_to") is not None
        state["cadence_strength"] = 1.0 if resolution == "strong" else (0.45 if resolution == "weak" else 0.15)
        state["phrase_breath_remaining"] = 0.5 if end_bar in arc.get("breath_bars", []) else 0.0
        state_trace.append({
            "phrase_id": relation["phrase_id"], "point": "end", **deepcopy(state),
            "rest_type": "structural_end" if state["resolved"] else "breath",
        })

    plan = {
        "schema_version": 3,
        "section_arc": deepcopy(arc),
        "phrase_relationships": deepcopy(relationships),
        "melodic_state_trace": state_trace,
        "long_form_phrase_rules": deepcopy(rules),
        "tonality": tonality,
        "performance_shaping": {
            "velocity_by_action": True,
            "note_length_model": "guitar_gate_cycles",
            "general_midi_legato_fallback": "soft_attack_plus_pitch_curve",
        },
    }
    events = _shape_note_lengths(events, phrase, beats_per_bar)
    return events, plan


def export_long_form_plan(phrase: dict[str, Any]) -> dict[str, Any] | None:
    plan = phrase.get("_long_form_plan")
    return deepcopy(plan) if isinstance(plan, dict) else None
