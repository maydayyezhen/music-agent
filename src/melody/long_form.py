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
            start = phrase_start + float(item["offset"])
            if relation["relationship"] == "climax" and note_index == len(transformed) - 1:
                start = (end_bar - 1) * beats_per_bar + beats_per_bar * 0.5
            if start >= phrase_end - 0.1:
                continue
            bar = int(start // beats_per_bar) + 1
            progress = (bar - 1) / max(1, bars - 1)
            contour = round((peak_bar - 1) * progress * 5 / max(1, peak_bar - 1))
            desired = root + int(item["degree"]) + contour
            if bar < target_bar:
                desired = min(desired, target_pitch - max(2, target_bar - bar))
            if bar == target_bar and (relation["relationship"] == "climax" or note_index == len(transformed) - 1):
                desired = target_pitch
            if bar > peak_bar:
                desired -= round((bar - peak_bar) * 0.7)
            pitch = _nearest_scale_pitch(desired, scale_pcs, low, high)
            chord = _chord_at(phrase, start, beats_per_bar)
            chord_pc = root_pc(chord)
            function = "chord_tone" if pitch % 12 in {
                chord_pc, (chord_pc + 3) % 12, (chord_pc + 4) % 12, (chord_pc + 7) % 12
            } else "non_chord_tone"
            duration = min(float(item["duration"]), phrase_end - start)
            cross_bar_reason = item.get("cross_bar_reason")
            bar_end = (int(start // beats_per_bar) + 1) * beats_per_bar
            if cross_bar_reason:
                requested = bar_end - start + float(item.get("cross_bar_tail_beats", 0.2))
                duration = min(max(duration, requested), float(item["duration"]) + 0.5, phrase_end - start)
            else:
                duration = min(duration, bar_end - start)
            arts: list[str] = []
            realization = phrase.get("realization", {})
            allow_articulations = bool(realization.get("enable_articulations", False))
            allow_pitch_bend = bool(realization.get("enable_pitch_bend", False))
            action = str(item.get("action", "pick")) if allow_articulations else "pick"
            if action in {"hammer_on", "pull_off"}:
                arts.extend([action, "legato"])
            elif action == "slide":
                arts.extend(["slide", "legato"])
            elif action in {"bend", "bend_release"} and allow_pitch_bend:
                arts.append(action)
            elif action == "vibrato":
                arts.append("vibrato")
            is_final = relation["relationship"] == "resolution" and note_index == len(transformed) - 1
            if is_final:
                arts.append("resolution")
            string, fret = assign_guitar_note(pitch, tuning, max_fret, preferred_fret)
            preferred_fret = fret
            velocity = base_velocity + round(float(arc["energy_curve"][bar - 1]) * 10) + (5 if bar == peak_bar else 0)
            event = note(
                pitch, start, duration, velocity, beats_per_bar, arts,
                _string=string, _fret=fret, _phrase_id=relation["phrase_id"],
                _relationship=relation["relationship"], _motif_version=phrase_index,
                _note_function=function, _cross_bar=bool(cross_bar_reason),
                _cross_bar_reason=cross_bar_reason,
                _rest_type_after=item.get("rest_type_after"),
                _gesture=item.get("gesture"),
            )
            if "bend" in arts or "bend_release" in arts:
                event["bend_semitones"] = float(item.get("bend_semitones", 2.0))
            if "slide" in arts and item.get("slide_from_semitones") is not None:
                event["slide_from_semitones"] = float(item["slide_from_semitones"])
            if "vibrato" in arts:
                event["vibrato"] = item.get(
                    "vibrato",
                    {"delay": 0.35, "depth": 0.35, "rate": 5.2},
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
        "schema_version": 2,
        "section_arc": deepcopy(arc),
        "phrase_relationships": deepcopy(relationships),
        "melodic_state_trace": state_trace,
        "long_form_phrase_rules": deepcopy(rules),
        "tonality": tonality,
    }
    events = sorted(events, key=lambda event: position(event["at"], beats_per_bar))
    if not phrase.get("realization", {}).get("allow_profile_legato_overlap", False):
        for current, following in zip(events, events[1:]):
            current_start = position(current["at"], beats_per_bar)
            next_start = position(following["at"], beats_per_bar)
            current["duration"] = round(
                max(0.05, min(float(current["duration"]), next_start - current_start)), 3
            )
    return events, plan


def export_long_form_plan(phrase: dict[str, Any]) -> dict[str, Any] | None:
    plan = phrase.get("_long_form_plan")
    return deepcopy(plan) if isinstance(plan, dict) else None
