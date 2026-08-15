from __future__ import annotations

from typing import Any

from .common import assign_guitar_chord, assign_guitar_note, harmony, note, power_chord_pitches, seeded
from .strumming import compile_continuous_strumming

STANDARD_TUNING = [40, 45, 50, 55, 59, 64]  # E2 A2 D3 G3 B3 E4
LONG_FORM_MODES = {"long_form_authored", "long_form_experimental", "long_form"}


def _settings(phrase: dict[str, Any]) -> tuple[list[int], int, int]:
    tuning = [int(value) for value in phrase.get("tuning", STANDARD_TUNING)]
    return tuning, int(phrase.get("max_fret", 24)), int(round(58 + float(phrase.get("energy", 0.5)) * 46))


def _rhythm_chords(phrase: dict[str, Any], beats_per_bar: int, open_chords: bool) -> list[dict[str, Any]]:
    tuning, max_fret, velocity = _settings(phrase)
    rng = seeded(phrase)
    direction = str(phrase.get("performance_intent", {}).get("picking", "alternate"))
    step = float(phrase.get("subdivision", 0.5 if not open_chords else 1.0))
    gate = float(phrase.get("gate", 0.38 if not open_chords else 0.86))
    spread = float(phrase.get("strum_spread", 0.045 if not open_chords else 0.075))
    rests = {int(value) for value in phrase.get("rest_steps", [])}
    articulations = list(phrase.get("articulations", []))
    if not open_chords and "palm_mute" not in articulations:
        articulations.append("palm_mute")
    result: list[dict[str, Any]] = []
    attack_index = 0
    preferred_fret = 2
    for span_index, span in enumerate(harmony(phrase, beats_per_bar)):
        pitches = power_chord_pitches(span["chord"], tuning[0], tuning[-1] + max_fret)
        assignments = assign_guitar_chord(pitches, tuning, max_fret, preferred_fret)
        preferred_fret = round(sum(item[2] for item in assignments) / len(assignments))
        local = 0.0
        while local < span["duration"] - 0.04:
            sectional_breath = open_chords and span_index % 4 == 3 and local >= span["duration"] - step
            if attack_index not in rests and not sectional_breath:
                up = direction == "alternate" and attack_index % 2 == 1
                ordered = sorted(assignments, key=lambda item: item[1], reverse=up)
                chord_group = f"strum-{span_index}-{attack_index}"
                for order, (pitch, string, fret) in enumerate(ordered):
                    accent = 7 if abs((span["start"] + local) % beats_per_bar) < 0.01 else 0
                    turnaround = 4 if open_chords and span_index % 4 == 2 and local >= span["duration"] - step * 2 else 0
                    event_velocity = velocity + accent + turnaround - order * 2 + rng.choice([-1, 0, 0, 1])
                    result.append(note(pitch, span["start"] + local + order * spread,
                                       min(step * gate * (0.82 if turnaround else 1.0), span["duration"] - local), event_velocity,
                                       beats_per_bar, articulations + (["accent"] if accent else []),
                                       _string=string, _fret=fret, _attack_group=chord_group,
                                       _strum_direction="up" if up else "down"))
            attack_index += 1
            local += step
    return result


def _lead(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    tuning, max_fret, base_velocity = _settings(phrase)
    motif = phrase.get("motif")
    if not isinstance(motif, list) or not motif:
        raise ValueError("melodic_lead instrument_phrase requires motif")
    result: list[dict[str, Any]] = []
    preferred_fret = 7
    for index, item in enumerate(motif):
        from .common import position, midi_pitch
        pitch = midi_pitch(item["pitch"])
        planned_string = item.get("planned_string")
        planned_fret = item.get("planned_fret")
        if planned_string is not None or planned_fret is not None:
            if not isinstance(planned_string, int) or not 0 <= planned_string < len(tuning):
                raise ValueError("planned_string must be a zero-based configured guitar string index")
            if not isinstance(planned_fret, int) or not 0 <= planned_fret <= max_fret:
                raise ValueError("planned_fret must be inside the configured fretboard")
            if tuning[planned_string] + planned_fret != pitch:
                raise ValueError(
                    f"planned string/fret does not produce {item['pitch']}: "
                    f"string {planned_string}, fret {planned_fret}"
                )
            string, fret = planned_string, planned_fret
        else:
            string, fret = assign_guitar_note(pitch, tuning, max_fret, preferred_fret)
        preferred_fret = fret
        arts = list(item.get("articulations", phrase.get("articulations", ["sustain"])))
        phrase_accent = 0
        if index == 0 or "bend" in arts or "bend_release" in arts:
            phrase_accent += 7
        if "hammer_on" in arts or "pull_off" in arts:
            phrase_accent -= 4
        if "slide" in arts:
            phrase_accent += 2
        event = note(pitch, position(item["at"], beats_per_bar), float(item["duration"]),
                     int(item.get("velocity", base_velocity + phrase_accent)), beats_per_bar, arts,
                     _string=string, _fret=fret, _phrase_note=index)
        if "bend" in arts or "bend_release" in arts:
            event["bend_semitones"] = float(item.get("bend_semitones", 2.0))
        if "slide" in arts and item.get("slide_from_semitones") is not None:
            event["slide_from_semitones"] = float(item["slide_from_semitones"])
        if "vibrato" in arts:
            event["vibrato"] = item.get("vibrato", {"delay": 0.35, "depth": 0.35, "rate": 5.2})
        result.append(event)
    return result


def _long_form_lead(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    from src.melody import compile_long_form_lead
    tuning, max_fret, base_velocity = _settings(phrase)
    events, plan = compile_long_form_lead(phrase, beats_per_bar, tuning, max_fret, base_velocity)
    phrase["_long_form_plan"] = plan
    return events


def compile_phrase(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    phrase_type = phrase["phrase_type"]
    if phrase_type in {"continuous_strumming", "acoustic_continuous_strumming", "sustained_chord_hit"} or phrase.get("strumming_pattern") or phrase.get("strumming_patterns"):
        return compile_continuous_strumming(phrase, beats_per_bar)
    if phrase_type == "palm_muted_eighths":
        return _rhythm_chords(phrase, beats_per_bar, False)
    if phrase_type == "open_power_chords":
        return _rhythm_chords(phrase, beats_per_bar, True)
    if phrase_type in {"melodic_lead", "lead_melody"}:
        if phrase.get("phrase_generation_mode", "legacy_stable") in LONG_FORM_MODES:
            return _long_form_lead(phrase, beats_per_bar)
        return _lead(phrase, beats_per_bar)
    raise ValueError(f"unsupported electric guitar phrase_type: {phrase_type!r}")
