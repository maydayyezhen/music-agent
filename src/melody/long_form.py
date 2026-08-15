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
    if not low <= target <= high:
        raise ValueError(f"authored long-form pitch {target} is outside register {low}..{high}")
    if target % 12 in scale_pcs:
        return target
    for distance in range(1, 13):
        for value in (target - distance, target + distance):
            if low <= value <= high and value % 12 in scale_pcs:
                return value
    raise ValueError("could not quantize authored long-form pitch inside configured register")


def _resolve_pitch(target: int, scale_pcs: set[int], low: int, high: int, quantization: str) -> int:
    if not low <= target <= high:
        raise ValueError(f"authored long-form pitch {target} is outside register {low}..{high}")
    if quantization == "none":
        return target
    if quantization == "scale":
        return _nearest_scale_pitch(target, scale_pcs, low, high)
    raise ValueError("pitch_quantization must be 'none' or 'scale'")


def _chord_at(phrase: dict[str, Any], beat: float, beats_per_bar: int) -> str:
    spans = phrase["harmony"]
    selected = spans[0]["chord"]
    for span in spans:
        if position(span["at"], beats_per_bar) <= beat + 1e-6:
            selected = span["chord"]
        else:
            break
    return str(selected)


def _apply_explicit_transform(
    base: list[dict[str, Any]],
    relationship: dict[str, Any],
) -> list[dict[str, Any]]:
    """Apply only transformations explicitly authored in the project.

    Relationship labels and motif_operations are descriptive metadata. They never
    change pitch, rhythm, register, phrase endings, or cadence targets by themselves.
    """
    result = deepcopy(base)
    transform = relationship.get("transform", {})
    if transform is None:
        transform = {}
    if not isinstance(transform, dict):
        raise ValueError("long-form relationship transform must be an object")

    slice_spec = transform.get("slice")
    if slice_spec is not None:
        if (
            not isinstance(slice_spec, list)
            or len(slice_spec) != 2
            or any(not isinstance(value, int) for value in slice_spec)
        ):
            raise ValueError("long-form transform.slice must be [start_index, end_index]")
        start_index, end_index = slice_spec
        result = result[start_index:end_index]
        if not result:
            raise ValueError("long-form transform.slice removed the entire motif")

    time_scale = float(transform.get("time_scale", 1.0))
    if time_scale <= 0:
        raise ValueError("long-form transform.time_scale must be positive")
    offset_shift = float(transform.get("offset_shift_beats", 0.0))
    degree_shift = int(transform.get("degree_shift", 0))

    for item in result:
        item["offset"] = float(item["offset"]) * time_scale + offset_shift
        item["duration"] = float(item["duration"]) * time_scale
        if "degree" in item:
            item["degree"] = int(item["degree"]) + degree_shift

    if result and "ending_degree_delta" in transform:
        if "degree" not in result[-1]:
            raise ValueError("ending_degree_delta requires a degree-based final motif note")
        result[-1]["degree"] = int(result[-1]["degree"]) + int(transform["ending_degree_delta"])

    if result and "ending_duration_delta" in transform:
        result[-1]["duration"] = float(result[-1]["duration"]) + float(transform["ending_duration_delta"])
        if result[-1]["duration"] <= 0:
            raise ValueError("ending_duration_delta produced a non-positive duration")

    overrides = relationship.get("note_overrides", [])
    if overrides is None:
        overrides = []
    if not isinstance(overrides, list):
        raise ValueError("long-form note_overrides must be a list")
    for override in overrides:
        if not isinstance(override, dict) or not isinstance(override.get("index"), int):
            raise ValueError("long-form note_overrides entries need integer index")
        index = int(override["index"])
        if not 0 <= index < len(result):
            raise ValueError("long-form note_overrides index is outside transformed motif")
        allowed = {
            "offset", "duration", "degree", "pitch", "action", "gesture", "velocity",
            "velocity_delta", "cross_bar_reason", "rest_type_after", "bend_semitones",
            "slide_from_semitones", "vibrato",
        }
        for key, value in override.items():
            if key != "index":
                if key not in allowed:
                    raise ValueError(f"unsupported long-form note override field: {key}")
                result[index][key] = value

    return result


def _velocity_delta(
    action: str,
    gesture: str,
    note_index: int,
    start: float,
    beats_per_bar: int,
    item: dict[str, Any],
) -> int:
    """Optional performance shaping. This never runs unless explicitly enabled."""
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


def _shape_note_lengths(
    events: list[dict[str, Any]],
    phrase: dict[str, Any],
    beats_per_bar: int,
) -> list[dict[str, Any]]:
    """Optional guitar gate shaping, enabled only by realization.shape_note_lengths."""
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


def compile_long_form_lead(
    phrase: dict[str, Any],
    beats_per_bar: int,
    tuning: list[int],
    max_fret: int,
    base_velocity: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Realize an authored long-form melody without inventing compositional content.

    The executor may map authored material to the instrument, but it does not infer a
    rising contour, delayed peak, sequence transposition, cadence pitch, final tonic,
    vibrato ending, or other musical decision from semantic labels.
    """
    arc = phrase["section_arc"]
    relationships = phrase["phrase_relationships"]
    motif = phrase["motif_seed"]
    rules = phrase.get("long_form_phrase_rules", {})
    bars = int(arc["bars"][1]) - int(arc["bars"][0]) + 1
    scale_pcs, tonality = resolve_tonality(phrase)
    low, high = [int(value) for value in phrase["register_midi"]]
    motif_root = int(phrase.get("motif_root_midi", 0))
    quantization = str(phrase.get("pitch_quantization", "none"))
    realization = phrase.get("realization", {})
    if not isinstance(realization, dict):
        raise ValueError("long-form realization must be an object")

    energy_curve = arc.get("energy_curve")
    if energy_curve is None:
        energy_curve = [float(phrase.get("energy", 0.5))] * bars

    delayed_target = arc.get("delayed_target")
    target_pitch = note_number(delayed_target["pitch"]) if isinstance(delayed_target, dict) and "pitch" in delayed_target else None
    target_bar = int(delayed_target["bar"]) if isinstance(delayed_target, dict) and "bar" in delayed_target else None

    state: dict[str, Any] = {
        "active_motif": phrase.get("motif_id", "motif_A"),
        "motif_version": 0,
        "current_register": arc.get("opening_register", "unspecified"),
        "direction": "unknown",
        "tension": float(energy_curve[0]),
        "resolved": False,
        "continuation_required": True,
        "target_pitch": target_pitch,
        "target_bar": target_bar,
        "last_interval": 0,
        "last_note_function": "unknown",
        "phrase_breath_remaining": 0.0,
        "cadence_strength": 0.0,
    }

    events: list[dict[str, Any]] = []
    state_trace: list[dict[str, Any]] = []
    preferred_fret = 7
    previous_pitch: int | None = None

    for phrase_index, relation in enumerate(relationships):
        start_bar, end_bar = [int(value) for value in relation["bars"]]
        state_trace.append({
            "phrase_id": relation["phrase_id"],
            "point": "start",
            **deepcopy(state),
        })
        transformed = _apply_explicit_transform(motif, relation)
        phrase_start = (start_bar - 1) * beats_per_bar
        phrase_end = end_bar * beats_per_bar

        for note_index, item in enumerate(transformed):
            start = phrase_start + float(item["offset"])
            if start < phrase_start - 1e-8 or start >= phrase_end - 1e-8:
                raise ValueError(
                    f"authored long-form note starts outside phrase {relation['phrase_id']}: {start}"
                )
            bar = int(start // beats_per_bar) + 1

            if "pitch" in item:
                pitch = note_number(item["pitch"])
                if not low <= pitch <= high:
                    raise ValueError(
                        f"authored long-form pitch {item['pitch']} is outside register {low}..{high}"
                    )
            else:
                desired = motif_root + int(item["degree"])
                pitch = _resolve_pitch(desired, scale_pcs, low, high, quantization)

            chord = _chord_at(phrase, start, beats_per_bar)
            chord_pc = root_pc(chord)
            function = "chord_tone" if pitch % 12 in {
                chord_pc,
                (chord_pc + 3) % 12,
                (chord_pc + 4) % 12,
                (chord_pc + 7) % 12,
            } else "non_chord_tone"

            authored_duration = float(item["duration"])
            duration = min(authored_duration, phrase_end - start)
            if duration <= 0:
                raise ValueError("authored long-form duration must be positive")

            allow_articulations = bool(realization.get("enable_articulations", False))
            allow_pitch_bend = bool(realization.get("enable_pitch_bend", False))
            action = str(item.get("action", "pick")) if allow_articulations else "pick"
            arts: list[str] = []
            if action in {"hammer_on", "pull_off"}:
                arts.extend([action, "legato"])
            elif action == "slide":
                arts.extend(["slide", "legato"])
            elif action in {"bend", "bend_release"} and allow_pitch_bend:
                arts.append(action)
            elif action == "vibrato":
                arts.extend(["vibrato", "sustain"])

            string, fret = assign_guitar_note(pitch, tuning, max_fret, preferred_fret)
            preferred_fret = fret
            gesture = str(item.get("gesture", ""))

            if "velocity" in item:
                velocity = int(item["velocity"])
            else:
                velocity = base_velocity + round(float(energy_curve[bar - 1]) * 10)
                if bool(realization.get("velocity_shaping", False)):
                    velocity += _velocity_delta(action, gesture, note_index, start, beats_per_bar, item)
                else:
                    velocity += int(item.get("velocity_delta", 0))
            velocity = max(1, min(127, velocity))

            event = note(
                pitch,
                start,
                duration,
                velocity,
                beats_per_bar,
                arts,
                _string=string,
                _fret=fret,
                _phrase_id=relation["phrase_id"],
                _relationship=relation["relationship"],
                _motif_version=phrase_index,
                _note_function=function,
                _cross_bar=start + duration > (int(start // beats_per_bar) + 1) * beats_per_bar + 1e-8,
                _cross_bar_reason=item.get("cross_bar_reason"),
                _rest_type_after=item.get("rest_type_after"),
                _gesture=gesture,
                _action=action,
                _authored_duration=round(authored_duration, 3),
            )

            if action in {"bend", "bend_release"} and allow_pitch_bend:
                event["bend_semitones"] = float(item.get("bend_semitones", 2.0))
            if action == "slide" and item.get("slide_from_semitones") is not None:
                event["slide_from_semitones"] = float(item["slide_from_semitones"])
            if action in {"hammer_on", "pull_off"} and allow_pitch_bend and previous_pitch is not None:
                transition = previous_pitch - pitch
                if 0 < abs(transition) <= 2:
                    event["slide_from_semitones"] = float(transition)
                    event["_legato_pitch_fallback"] = True
            if action == "vibrato":
                event["vibrato"] = item.get(
                    "vibrato",
                    {"delay": 0.35, "depth": 0.30, "rate": 5.0},
                )

            events.append(event)
            if previous_pitch is not None:
                state["last_interval"] = pitch - previous_pitch
                state["direction"] = (
                    "ascending" if pitch > previous_pitch else
                    "descending" if pitch < previous_pitch else
                    "level"
                )
            state["last_note_function"] = function
            state["tension"] = float(energy_curve[bar - 1])
            state["current_register"] = (
                "high" if pitch >= 76 else "mid_high" if pitch >= 69 else "mid"
            )
            previous_pitch = pitch

        resolution = relation["resolution"]
        state["motif_version"] = phrase_index + 1
        state["resolved"] = resolution == "strong"
        state["continuation_required"] = (
            not state["resolved"] and relation.get("continuation_to") is not None
        )
        state["cadence_strength"] = (
            1.0 if resolution == "strong" else 0.45 if resolution == "weak" else 0.15
        )
        state["phrase_breath_remaining"] = (
            0.5 if end_bar in arc.get("breath_bars", []) else 0.0
        )
        state_trace.append({
            "phrase_id": relation["phrase_id"],
            "point": "end",
            **deepcopy(state),
            "rest_type": "structural_end" if state["resolved"] else "breath",
        })

    if bool(realization.get("shape_note_lengths", False)):
        events = _shape_note_lengths(events, phrase, beats_per_bar)
        note_length_model = "explicit_guitar_gate_cycles"
    else:
        events = sorted(events, key=lambda event: position(event["at"], beats_per_bar))
        note_length_model = "authored"

    plan = {
        "schema_version": 4,
        "execution_policy": "authored_only",
        "section_arc": deepcopy(arc),
        "phrase_relationships": deepcopy(relationships),
        "melodic_state_trace": state_trace,
        "long_form_phrase_rules": deepcopy(rules),
        "tonality": tonality,
        "performance_shaping": {
            "velocity_by_action": bool(realization.get("velocity_shaping", False)),
            "note_length_model": note_length_model,
            "general_midi_legato_fallback": (
                "soft_attack_plus_pitch_curve"
                if bool(realization.get("enable_pitch_bend", False))
                else "disabled"
            ),
        },
    }
    return events, plan


def export_long_form_plan(phrase: dict[str, Any]) -> dict[str, Any] | None:
    plan = phrase.get("_long_form_plan")
    return deepcopy(plan) if isinstance(plan, dict) else None
