from __future__ import annotations

import math
from typing import Any

from .common import assign_guitar_chord, chord_quality, harmony, note, power_chord_pitches, root_pc, seeded


HAND_MOTION = ["down", "up", "down", "up", "down", "up", "down", "up"]
SIXTEENTH_HAND_MOTION = ["down" if index % 2 == 0 else "up" for index in range(16)]

ALLOWED_STRUM_ACTIONS = {
    "full_strum", "partial_strum", "single_string_restrike", "muted_strum",
    "ghost_strum", "air_strum",
    # Backward-compatible eighth-note vocabulary.
    "accent_strum", "light_upstroke", "bass_note",
}

PATTERNS: dict[str, list[str]] = {
    "single_hit": ["accent_strum", "air_strum", "air_strum", "air_strum", "air_strum", "air_strum", "air_strum", "air_strum"],
    # Explicit breathing family. Do not use this merely because a part is a verse.
    "verse_a": ["partial_strum", "air_strum", "partial_strum", "light_upstroke", "air_strum", "light_upstroke", "accent_strum", "light_upstroke"],
    "steady_eighths": ["partial_strum", "light_upstroke", "muted_strum", "light_upstroke", "partial_strum", "light_upstroke", "accent_strum", "light_upstroke"],
    "classic_pop": ["partial_strum", "air_strum", "accent_strum", "light_upstroke", "air_strum", "light_upstroke", "partial_strum", "light_upstroke"],
    "chorus_open": ["accent_strum", "light_upstroke", "partial_strum", "light_upstroke", "full_strum", "light_upstroke", "accent_strum", "light_upstroke"],
    "bass_continuous": ["bass_note", "air_strum", "partial_strum", "light_upstroke", "bass_note", "light_upstroke", "accent_strum", "light_upstroke"],
}

# These are original neutral skeletons, not transcriptions of any reference song.
SIXTEENTH_PATTERNS: dict[str, list[str]] = {
    # Selective-sounding family with deliberate air strokes.
    "sixteenth_flow": [
        "full_strum", "air_strum", "partial_strum", "single_string_restrike",
        "partial_strum", "air_strum", "partial_strum", "ghost_strum",
        "full_strum", "single_string_restrike", "partial_strum", "air_strum",
        "muted_strum", "partial_strum", "air_strum", "partial_strum",
    ],
    # Dense connected family. Every hand position may create an audible contact, but
    # weak positions use narrow/ghost/restrike actions rather than sixteen block chords.
    "sixteenth_continuous": [
        "full_strum", "single_string_restrike", "partial_strum", "single_string_restrike",
        "partial_strum", "ghost_strum", "partial_strum", "single_string_restrike",
        "full_strum", "single_string_restrike", "partial_strum", "single_string_restrike",
        "muted_strum", "partial_strum", "single_string_restrike", "partial_strum",
    ],
}

SOUNDING_ACTIONS = set(PATTERNS["chorus_open"] + PATTERNS["steady_eighths"] + PATTERNS["bass_continuous"]) - {"air_strum"}


def _requests_breathing_gaps(phrase: dict[str, Any]) -> bool:
    mode = str(
        phrase.get(
            "strumming_continuity",
            phrase.get("density_mode", phrase.get("spacing_mode", "")),
        )
    ).lower()
    return any(token in mode for token in ("breathing", "spaced", "sparse", "gapped", "air"))


def _pattern_ids(phrase: dict[str, Any], bars: int) -> list[str]:
    configured = phrase.get("strumming_patterns", phrase.get("strumming_pattern"))
    if isinstance(configured, list) and configured:
        pattern_ids = [str(value) for value in configured]
    elif isinstance(configured, str):
        pattern_ids = [configured]
    else:
        role = str(phrase.get("section_function", phrase.get("role", ""))).lower()
        phrase_type = str(phrase.get("phrase_type", ""))
        if phrase_type == "sustained_chord_hit":
            pattern_ids = ["single_hit"]
        elif "pre" in role or "build" in role:
            pattern_ids = ["verse_a", "steady_eighths", "chorus_open"]
        elif "chorus" in role or "open" in phrase_type:
            pattern_ids = ["chorus_open"]
        elif "bass" in phrase_type:
            pattern_ids = ["bass_continuous"]
        elif _requests_breathing_gaps(phrase):
            pattern_ids = ["verse_a"]
        else:
            # Generic continuous strumming should actually be continuous. Air strokes
            # are a texture choice, not an automatic verse/default identity.
            pattern_ids = ["steady_eighths"]
    unknown = [name for name in pattern_ids if name not in PATTERNS]
    if unknown:
        raise ValueError(f"unknown strumming pattern(s): {unknown}")
    if len(pattern_ids) == 1:
        return pattern_ids * bars
    if len(pattern_ids) >= bars:
        return pattern_ids[:bars]
    # A short sequence represents a gradual arc, not a loop that restarts every bar.
    return [pattern_ids[min(len(pattern_ids) - 1, int(index * len(pattern_ids) / bars))] for index in range(bars)]


def build_strumming_grid(phrase: dict[str, Any], beats_per_bar: int) -> dict[str, Any]:
    spans = harmony(phrase, beats_per_bar)
    end = max(span["start"] + span["duration"] for span in spans)
    bars = int(math.ceil(end / beats_per_bar))
    subdivision = str(phrase.get("subdivision", "eighth"))
    if subdivision not in {"eighth", "sixteenth"}:
        raise ValueError("strumming subdivision must be eighth or sixteenth")
    if subdivision == "sixteenth":
        return _build_sixteenth_grid(phrase, bars)
    pattern_ids = _pattern_ids(phrase, bars)
    grid = []
    for bar in range(bars):
        pattern_id = pattern_ids[bar]
        actions = PATTERNS[pattern_id]
        grid.append({
            "bar": bar + 1,
            "subdivision": "eighth",
            "hand_motion": list(HAND_MOTION),
            "actions": list(actions),
            "sounding_strum_count": sum(action != "air_strum" for action in actions),
            "hand_motion_count": 8,
            "pattern_id": pattern_id,
            "last_hand_direction": "up",
            "next_expected_direction": "down",
            "pattern_continues_across_bar": bar < bars - 1,
        })
    return {"subdivision": "eighth", "bars": grid, "total_bars": bars}


def _foreground_by_bar(phrase: dict[str, Any]) -> dict[int, dict[str, Any]]:
    configured = phrase.get("foreground_activity", [])
    if not isinstance(configured, list):
        return {}
    return {int(item["bar"]): item for item in configured if isinstance(item, dict) and "bar" in item}


def _related_variant(base: list[str], index: int) -> tuple[list[str], list[dict[str, Any]]]:
    actions = list(base)
    changes: list[dict[str, Any]] = []

    def change(step: int, action: str, reason: str) -> None:
        previous = actions[step]
        if previous != action:
            actions[step] = action
            changes.append({"step": step, "from": previous, "to": action, "reason": reason})

    if index == 1:
        change(5, "single_string_restrike", "add one connected weak-position restrike")
        change(7, "air_strum", "trade a ghost stroke for air")
        change(12, "ghost_strum", "soften the late accent")
    elif index == 2:
        change(3, "air_strum", "remove one inner attack")
        change(8, "partial_strum", "thin the midpoint full sweep")
        change(11, "partial_strum", "move activity to a related weak position")
        change(14, "single_string_restrike", "add a one-string pickup")
    elif index == 3:
        change(0, "air_strum", "carry retained strings across the downbeat")
        change(4, "muted_strum", "muted variation of the same pulse")
        change(14, "single_string_restrike", "retain the pickup fragment")
        change(15, "air_strum", "leave a cross-bar hand-motion gap")
    return actions, changes


def _thin_for_foreground(
    actions: list[str], info: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    result = list(actions)
    changes: list[dict[str, Any]] = []
    active_steps = {int(value) for value in info.get("active_steps", [])}
    release_steps = {int(value) for value in info.get("release_steps", [])}
    if not active_steps:
        return result, changes

    def change(step: int, action: str, reason: str) -> None:
        previous = result[step]
        if previous != action:
            result[step] = action
            changes.append({"step": step, "from": previous, "to": action, "reason": reason})

    removed = False
    for step, action in enumerate(list(result)):
        if step in release_steps:
            continue
        if step in active_steps and action == "full_strum":
            change(step, "partial_strum", "foreground-active full sweep thinned")
        elif step in active_steps and action == "partial_strum" and step % 4 != 0:
            change(step, "single_string_restrike" if step % 2 else "muted_strum",
                   "foreground-active string count reduced")
        elif step in active_steps and not removed and action in {"ghost_strum", "single_string_restrike"}:
            change(step, "air_strum", "one weak attack removed while hand keeps moving")
            removed = True
    return result, changes


def _build_sixteenth_grid(phrase: dict[str, Any], bars: int) -> dict[str, Any]:
    configured = phrase.get("strumming_pattern", phrase.get("strumming_patterns"))
    if isinstance(configured, list):
        configured = configured[0] if configured else None
    if configured is None:
        configured = "sixteenth_flow" if _requests_breathing_gaps(phrase) else "sixteenth_continuous"
    pattern_id = str(configured)
    if pattern_id not in SIXTEENTH_PATTERNS:
        raise ValueError(f"unknown sixteenth strumming pattern: {pattern_id!r}")
    base = SIXTEENTH_PATTERNS[pattern_id]
    foreground = _foreground_by_bar(phrase)
    grid = []
    variation_debug = []
    for bar in range(1, bars + 1):
        variant = (bar - 1) % 4 if phrase.get("four_bar_variation", True) else 0
        actions, changes = _related_variant(base, variant)
        foreground_changes: list[dict[str, Any]] = []
        info = foreground.get(bar, {}) if phrase.get("foreground_aware", False) else {}
        if info:
            actions, foreground_changes = _thin_for_foreground(actions, info)
        variant_name = ("A", "A'", "B", "B'")[variant]
        variant_id = f"{pattern_id}:{variant_name}"
        item = {
            "bar": bar, "subdivision": "sixteenth", "hand_motion": list(SIXTEENTH_HAND_MOTION),
            "actions": actions, "sounding_strum_count": sum(action != "air_strum" for action in actions),
            "hand_motion_count": 16, "pattern_id": pattern_id, "variant_id": variant_id,
            "last_hand_direction": "up", "next_expected_direction": "down",
            "pattern_continues_across_bar": bar < bars,
            "foreground_active": bool(info.get("active_steps")),
            "foreground_velocity_delta": -8 if info.get("active_steps") else 0,
            "foreground_release_steps": [int(value) for value in info.get("release_steps", [])],
        }
        grid.append(item)
        variation_debug.append({"bar": bar, "variant_id": variant_id, "actions": actions,
                                "related_changes": changes, "foreground_changes": foreground_changes})
    phrase["_four_bar_variation_debug"] = {
        "base_pattern_id": pattern_id, "base_actions": list(base), "cycle": "A -> A' -> B -> B'",
        "bars": variation_debug,
    }
    return {"subdivision": "sixteenth", "bars": grid, "total_bars": bars}


def _span_at(spans: list[dict[str, Any]], position: float) -> tuple[int, dict[str, Any]]:
    for index, span in enumerate(spans):
        if span["start"] - 1e-8 <= position < span["start"] + span["duration"] - 1e-8:
            return index, span
    return len(spans) - 1, spans[-1]


def compile_continuous_strumming(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    if str(phrase.get("subdivision", "eighth")) == "sixteenth":
        return _compile_sixteenth_strumming(phrase, beats_per_bar)
    tuning = [int(value) for value in phrase.get("tuning", [40, 45, 50, 55, 59, 64])]
    max_fret = int(phrase.get("max_fret", 24))
    energy = float(phrase.get("energy", 0.55))
    velocity = int(round(57 + energy * 45))
    spread = float(phrase.get("strum_spread", 0.042))
    gate = float(phrase.get("gate", 0.74))
    acoustic = str(phrase.get("instrument", "")).lower() in {"acoustic_guitar", "steel_guitar", "nylon_guitar"}
    rng = seeded(phrase)
    spans = harmony(phrase, beats_per_bar)
    grid = build_strumming_grid(phrase, beats_per_bar)
    phrase["_strumming_debug"] = grid

    assignments: list[list[tuple[int, int, int]]] = []
    preferred_fret = 2
    for span in spans:
        if acoustic:
            root_class = root_pc(span["chord"])
            root = next(value for value in range(tuning[0], min(tuning[0] + 13, tuning[-1] + max_fret + 1)) if value % 12 == root_class)
            third = 3 if chord_quality(span["chord"]) == "minor" else 4
            pitches = [root, root + 7, root + 12, root + 12 + third]
        else:
            pitches = power_chord_pitches(span["chord"], tuning[0], tuning[-1] + max_fret)
        assigned = assign_guitar_chord(pitches, tuning, max_fret, preferred_fret)
        preferred_fret = round(sum(item[2] for item in assigned) / len(assigned))
        assignments.append(assigned)

    result: list[dict[str, Any]] = []
    for bar_info in grid["bars"]:
        bar_index = int(bar_info["bar"]) - 1
        for step_index, (direction, action) in enumerate(zip(bar_info["hand_motion"], bar_info["actions"])):
            position = bar_index * beats_per_bar + step_index * 0.5
            span_index, span = _span_at(spans, position)
            if position >= span["start"] + span["duration"] - 1e-8:
                continue
            if action == "air_strum":
                continue
            chord = assignments[span_index]
            if action == "bass_note":
                chosen = chord[:1]
            elif action in {"full_strum", "accent_strum"}:
                chosen = chord
            elif action in {"muted_strum", "ghost_strum"}:
                chosen = chord[: min(2, len(chord))] if direction == "down" else chord[-min(2, len(chord)):]
            else:
                count = min(3, len(chord))
                chosen = chord[:count] if direction == "down" else chord[-count:]
            ordered = sorted(chosen, key=lambda item: item[1], reverse=direction == "up")
            action_delta = {"accent_strum": 8, "full_strum": 5, "partial_strum": 0, "light_upstroke": -7,
                            "muted_strum": -9, "ghost_strum": -15, "bass_note": 1}.get(action, 0)
            articulations = list(phrase.get("articulations", []))
            if action in {"muted_strum", "ghost_strum"}:
                if "palm_mute" not in articulations:
                    articulations.append("palm_mute")
                if action == "ghost_strum" and "dead_note" not in articulations:
                    articulations.append("dead_note")
            if direction == "up": articulations.append("strum_up")
            else: articulations.append("strum_down")
            if action == "accent_strum": articulations.append("accent")
            if phrase.get("palm_mute") and action not in {"full_strum", "accent_strum"} and "palm_mute" not in articulations:
                articulations.append("palm_mute")
            base_duration = 0.5 * gate
            if phrase.get("phrase_type") == "sustained_chord_hit" and step_index == 0:
                base_duration = min(span["start"] + span["duration"] - position, beats_per_bar)
            elif action in {"muted_strum", "ghost_strum"}:
                base_duration *= 0.42
            elif action in {"full_strum", "accent_strum"}:
                base_duration *= 1.12
            group = f"continuous-strum-{bar_index + 1}-{step_index + 1}"
            for order, (pitch, string, fret) in enumerate(ordered):
                result.append(note(
                    pitch, position + order * spread, max(0.08, base_duration - order * 0.012),
                    velocity + action_delta - order + rng.choice([-1, 0, 0, 1]), beats_per_bar, articulations,
                    _string=string, _fret=fret, _attack_group=group, _strum_direction=direction,
                    _hand_step=step_index, _hand_direction=direction, _strum_action=action,
                    _pattern_id=bar_info["pattern_id"], _pattern_continues_across_bar=bar_info["pattern_continues_across_bar"],
                ))
    return _trim_same_pitch(result, beats_per_bar)


def _sixteenth_assignments(
    phrase: dict[str, Any], spans: list[dict[str, Any]], tuning: list[int], max_fret: int,
) -> list[list[tuple[int, int, int]]]:
    acoustic = str(phrase.get("instrument", "")).lower() in {"acoustic_guitar", "steel_guitar", "nylon_guitar"}
    assignments: list[list[tuple[int, int, int]]] = []
    preferred_fret = 2
    for span in spans:
        if acoustic:
            root_class = root_pc(span["chord"])
            root = next(value for value in range(tuning[0], min(tuning[0] + 13, tuning[-1] + max_fret + 1)) if value % 12 == root_class)
            third = 3 if chord_quality(span["chord"]) == "minor" else 4
            pitches = [root, root + 7, root + 12, root + 12 + third]
        else:
            pitches = power_chord_pitches(span["chord"], tuning[0], tuning[-1] + max_fret)
        assigned = assign_guitar_chord(pitches, tuning, max_fret, preferred_fret)
        preferred_fret = round(sum(item[2] for item in assigned) / len(assigned))
        assignments.append(assigned)
    return assignments


def _chosen_strings(chord: list[tuple[int, int, int]], direction: str, action: str) -> list[tuple[int, int, int]]:
    ordered = sorted(chord, key=lambda item: item[1], reverse=direction == "up")
    if action in {"full_strum", "accent_strum"}:
        return ordered
    if action in {"single_string_restrike", "bass_note"}:
        return ordered[:1]
    if action == "ghost_strum":
        return ordered[:1]
    if action == "muted_strum":
        return ordered[: min(2, len(ordered))]
    return ordered[: min(3, len(ordered))]


def _compile_sixteenth_strumming(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    tuning = [int(value) for value in phrase.get("tuning", [40, 45, 50, 55, 59, 64])]
    max_fret = int(phrase.get("max_fret", 24))
    energy = float(phrase.get("energy", 0.55))
    base_velocity = int(round(57 + energy * 45))
    spread = float(phrase.get("strum_spread", 0.025))
    step_duration = beats_per_bar / 16
    gate = float(phrase.get("gate", 0.74))
    persistent = bool(phrase.get("per_string_sustain", True))
    rng = seeded(phrase)
    spans = harmony(phrase, beats_per_bar)
    end = max(span["start"] + span["duration"] for span in spans)
    grid = build_strumming_grid(phrase, beats_per_bar)
    phrase["_strumming_debug"] = grid
    assignments = _sixteenth_assignments(phrase, spans, tuning, max_fret)
    events: list[dict[str, Any]] = []
    active_by_string: dict[int, dict[str, Any]] = {}
    state_debug: list[dict[str, Any]] = []
    previous_attack = -1.0

    def close_string(string: int, at_position: float, reason: str) -> None:
        state = active_by_string.pop(string, None)
        if not state:
            return
        release = max(state["start"] + 0.06, at_position - 0.01)
        state["event"]["duration"] = round(release - state["start"], 3)
        state["event"]["_release_reason"] = reason

    def close_same_pitch(pitch: int, at_position: float, except_string: int) -> None:
        for string, state in list(active_by_string.items()):
            if string != except_string and state["pitch"] == pitch:
                close_string(string, at_position, "same_pitch_midi_safety")

    for bar_info in grid["bars"]:
        bar_index = int(bar_info["bar"]) - 1
        for step_index, (direction, action) in enumerate(zip(bar_info["hand_motion"], bar_info["actions"])):
            position = bar_index * beats_per_bar + step_index * step_duration
            span_index, span = _span_at(spans, position)
            chord = assignments[span_index]
            target_by_string = {string: (pitch, fret) for pitch, string, fret in chord}
            active_before = {string: {"pitch": state["pitch"], "fret": state["fret"]}
                             for string, state in active_by_string.items()}
            stopped_for_move = []
            for string, state in list(active_by_string.items()):
                target = target_by_string.get(string)
                if target != (state["pitch"], state["fret"]):
                    close_string(string, position, "chord_shape_move")
                    stopped_for_move.append(string)

            selected = [] if action == "air_strum" else _chosen_strings(chord, direction, action)
            retriggered = []
            opened = []
            retained_before_attack = [string for string in active_by_string]
            action_delta = {
                "full_strum": 8, "partial_strum": 0, "single_string_restrike": -3,
                "muted_strum": -10, "ghost_strum": -16,
            }.get(action, 0)
            metrical_delta = 4 if step_index in {0, 4, 8, 12} else 0
            velocity_delta = int(bar_info.get("foreground_velocity_delta", 0))
            for order, (pitch, string, fret) in enumerate(selected):
                if string in active_by_string:
                    close_string(string, position, "selected_string_retrigger")
                    retriggered.append(string)
                close_same_pitch(pitch, position, string)
                event_start = position + order * spread
                articulations = list(phrase.get("articulations", []))
                if direction == "up": articulations.append("strum_up")
                else: articulations.append("strum_down")
                if action in {"muted_strum", "ghost_strum"} and "palm_mute" not in articulations:
                    articulations.append("palm_mute")
                if action == "ghost_strum": articulations.append("dead_note")
                if action == "full_strum": articulations.append("accent")
                if phrase.get("palm_mute") and action != "full_strum" and "palm_mute" not in articulations:
                    articulations.append("palm_mute")
                item = note(
                    pitch, event_start, step_duration * gate,
                    base_velocity + action_delta + metrical_delta + velocity_delta - order + rng.choice([-1, 0, 0, 1]),
                    beats_per_bar, articulations,
                    _string=string, _fret=fret, _attack_group=f"sixteenth-strum-{bar_index + 1}-{step_index + 1}",
                    _strum_direction=direction, _hand_step=step_index, _hand_direction=direction,
                    _strum_action=action, _pattern_id=bar_info["pattern_id"], _variant_id=bar_info["variant_id"],
                    _pattern_continues_across_bar=bar_info["pattern_continues_across_bar"],
                )
                events.append(item)
                opened.append(string)
                if persistent and action not in {"muted_strum", "ghost_strum"}:
                    active_by_string[string] = {"pitch": pitch, "fret": fret, "start": event_start, "event": item}
                else:
                    short_gate = step_duration * (.42 if action in {"muted_strum", "ghost_strum"} else gate)
                    item["duration"] = round(max(0.06, short_gate - order * 0.008), 3)

            sustaining = bool(active_before) and position > previous_attack
            if selected:
                previous_attack = position
            state_debug.append({
                "bar": bar_index + 1, "step": step_index, "position_beats": round(position, 3),
                "direction": direction, "action": action,
                "active_before": active_before, "retained_before_attack": retained_before_attack,
                "stopped_for_chord_move": stopped_for_move, "selected_strings": [item[1] for item in selected],
                "retriggered_strings": retriggered, "opened_strings": opened,
                "active_after": {string: {"pitch": state["pitch"], "fret": state["fret"]}
                                 for string, state in active_by_string.items()},
                "previous_attack_still_sounding": sustaining,
                "cross_bar_sustain": step_index == 0 and bool(active_before),
                "foreground_active": bool(bar_info.get("foreground_active")),
            })

    for string in list(active_by_string):
        close_string(string, end, "phrase_end")
    phrase["_per_string_state_debug"] = {
        "enabled": persistent, "subdivision": "sixteenth", "tuning": tuning,
        "steps": state_debug,
    }
    return _trim_same_pitch(events, beats_per_bar)


def _trim_same_pitch(events: list[dict[str, Any]], beats_per_bar: int) -> list[dict[str, Any]]:
    from .common import position
    lanes: dict[str, list[dict[str, Any]]] = {}
    for event in sorted(events, key=lambda item: position(item["at"], beats_per_bar)):
        pitch = str(event["pitch"])
        start = position(event["at"], beats_per_bar)
        lane = lanes.setdefault(pitch, [])
        if lane:
            previous = lane[-1]
            previous_start = position(previous["at"], beats_per_bar)
            if previous_start + float(previous["duration"]) > start:
                previous["duration"] = round(max(0.05, start - previous_start - 0.01), 3)
        lane.append(event)
    return events