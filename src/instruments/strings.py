from __future__ import annotations

from typing import Any

from src.accompaniment.voicing import plan_smooth_voicings

from .common import chord_pitches, harmony, merge_same_pitch_legato, note


def compile_phrase(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    if phrase["phrase_type"] not in {"long_tones_inner_movement", "sustained_inner_movement"}:
        raise ValueError(f"unsupported strings phrase_type: {phrase['phrase_type']!r}")
    spans = harmony(phrase, beats_per_bar)
    register = phrase.get("register_midi", [55, 83])
    voices = int(phrase.get("voices", 3))
    raw = [{"at": span["at"], "duration": span["duration"],
            "pitches": chord_pitches(span["chord"], 48, 88, 3)} for span in spans]
    voicings = plan_smooth_voicings(raw, tuple(register), voices, 0.95, 0.95)
    velocity = int(round(42 + float(phrase.get("energy", 0.5)) * 34))
    lanes: dict[int, list[dict[str, Any]]] = {voice: [] for voice in range(voices)}
    for span_index, (span, voicing) in enumerate(zip(spans, voicings)):
        for voice, pitch in enumerate(voicing):
            lane = lanes[voice]
            retained = bool(lane and lane[-1]["pitch"] == pitch and abs(lane[-1]["end"] - span["start"]) < 0.1)
            if retained:
                lane[-1]["end"] = span["start"] + span["duration"]
                lane[-1]["crescendo"] = lane[-1]["crescendo"] or span_index >= len(spans) // 2
                continue
            arts = ["legato", "sustain"] + (["crescendo"] if span_index >= len(spans) // 2 else [])
            lane.append({"pitch": pitch, "start": span["start"], "end": span["start"] + span["duration"],
                         "velocity": velocity + span_index * 2 - voice, "arts": arts,
                         "crescendo": span_index >= len(spans) // 2})
    result: list[dict[str, Any]] = []
    for voice, lane in lanes.items():
        for item in lane:
            arts = item["arts"] + (["crescendo"] if item["crescendo"] and "crescendo" not in item["arts"] else [])
            result.append(note(item["pitch"], item["start"], item["end"] - item["start"],
                               item["velocity"], beats_per_bar, arts,
                               _voice=voice, _common_tone=(item["end"] - item["start"] > spans[0]["duration"]), _divisi=True))
    return merge_same_pitch_legato(result, beats_per_bar)
