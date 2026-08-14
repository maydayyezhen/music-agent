from __future__ import annotations

from typing import Any

from src.accompaniment.voicing import plan_smooth_voicings

from .common import harmony, merge_same_pitch_legato, note


def compile_phrase(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    phrase_type = phrase["phrase_type"]
    if phrase_type not in {"voice_led_chords", "organ_voice_led_chords", "piano_voice_led_chords"}:
        raise ValueError(f"unsupported keyboard phrase_type: {phrase_type!r}")
    spans = harmony(phrase, beats_per_bar)
    raw_spans = []
    from .common import chord_pitches
    register = phrase.get("register_midi", [55, 79])
    voices = int(phrase.get("voices", 3))
    for span in spans:
        raw_spans.append({"at": span["at"], "duration": span["duration"],
                          "pitches": chord_pitches(span["chord"], 48, 84, 3)})
    voicings = plan_smooth_voicings(raw_spans, tuple(register), voices, 0.9, 0.9)
    organ = phrase_type.startswith("organ") or phrase.get("instrument") == "organ"
    velocity = int(round(50 + float(phrase.get("energy", 0.5)) * 38))
    result: list[dict[str, Any]] = []
    previous: set[int] = set()
    for index, (span, voicing) in enumerate(zip(spans, voicings)):
        for voice_index, pitch in enumerate(voicing):
            retained = pitch in previous
            result.append(note(pitch, span["start"], span["duration"] if organ else span["duration"] - 0.08,
                               velocity - voice_index * 2, beats_per_bar,
                               ["legato" if organ else "tenuto"], _voice=voice_index, _common_tone=retained))
        if not organ and phrase.get("pedal", True):
            result.append({"type": "control_change", "control": 64, "value": 127,
                           "at": f"{int(span['start'] // beats_per_bar) + 1}:1", "_intent": "pedal_down"})
            end = span["start"] + span["duration"] - 0.08
            from .common import at
            result.append({"type": "control_change", "control": 64, "value": 0,
                           "at": at(end, beats_per_bar), "_intent": "pedal_retake"})
        previous = set(voicing)
    return merge_same_pitch_legato(result, beats_per_bar) if organ else result
