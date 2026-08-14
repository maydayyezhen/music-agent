from __future__ import annotations

import random
import re
import itertools
from typing import Any

from src.accompaniment.voicing import midi_to_note
from src.midi.pitches import note_number

CHORD_RE = re.compile(r"^([A-Ga-g])([#b]?)(?:(m)|(?:(?:5)|(?:maj)|(?:major)|(?:minor)))?$")
PCS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def position(value: str, beats_per_bar: int) -> float:
    bar, beat = str(value).split(":", 1)
    return (int(bar) - 1) * beats_per_bar + float(beat) - 1.0


def at(value: float, beats_per_bar: int) -> str:
    bar = int(value // beats_per_bar) + 1
    beat = value % beats_per_bar + 1
    return f"{bar}:{f'{beat:.3f}'.rstrip('0').rstrip('.')}"


def seeded(phrase: dict[str, Any]) -> random.Random:
    intent = phrase.get("performance_intent", {})
    return random.Random(int(intent.get("seed", phrase.get("seed", 0))))


def root_pc(chord: str) -> int:
    match = re.match(r"^([A-Ga-g])([#b]?)", chord)
    if not match:
        raise ValueError(f"invalid chord symbol: {chord!r}")
    letter, accidental = match.groups()
    return (PCS[letter.upper()] + {"": 0, "#": 1, "b": -1}[accidental]) % 12


def chord_quality(chord: str) -> str:
    text = chord.lower()
    if text.endswith("5"):
        return "power"
    if "m" in text and "maj" not in text:
        return "minor"
    return "major"


def chord_pitches(chord: str, low: int, high: int, voices: int = 3) -> list[int]:
    pc = root_pc(chord)
    quality = chord_quality(chord)
    intervals = [0, 7, 12] if quality == "power" else ([0, 3, 7] if quality == "minor" else [0, 4, 7])
    root = next((value for value in range(low, high + 1) if value % 12 == pc), low)
    pitches = [root + interval for interval in intervals]
    while len(pitches) < voices:
        pitches.append(pitches[len(pitches) % len(intervals)] + 12)
    return [pitch for pitch in pitches[:voices] if pitch <= high]


def power_chord_pitches(chord: str, low: int, high: int) -> list[int]:
    pc = root_pc(chord)
    root = next(value for value in range(low, high + 1) if value % 12 == pc)
    pitches = [root, root + 7, root + 12]
    return [pitch for pitch in pitches if pitch <= high]


def harmony(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    spans = phrase.get("harmony", phrase.get("harmony_spans", []))
    if not isinstance(spans, list) or not spans:
        raise ValueError("instrument_phrase requires non-empty harmony")
    result = []
    for span in spans:
        if "chord" not in span:
            raise ValueError("instrument_phrase harmony entries require chord")
        result.append({**span, "start": position(span["at"], beats_per_bar), "duration": float(span["duration"])})
    return result


def note(pitch: int, start: float, duration: float, velocity: int, beats_per_bar: int,
         articulations: list[str] | None = None, **metadata: Any) -> dict[str, Any]:
    event = {
        "type": "note", "pitch": midi_to_note(pitch), "at": at(start, beats_per_bar),
        "duration": round(max(0.05, duration), 3), "velocity": max(1, min(127, int(velocity))),
    }
    if articulations:
        event["articulations"] = list(dict.fromkeys(articulations))
    event.update({key: value for key, value in metadata.items() if value is not None})
    return event


def drum(name: str, start: float, velocity: int, beats_per_bar: int, limb: str,
         duration: float = 0.12, **metadata: Any) -> dict[str, Any]:
    return {"type": "drum", "note": name, "at": at(start, beats_per_bar),
            "duration": duration, "velocity": max(1, min(127, int(velocity))),
            "_limb": limb, **metadata}


def assign_guitar_note(pitch: int, tuning: list[int], max_fret: int = 24,
                       preferred_fret: int | None = None, used_strings: set[int] | None = None) -> tuple[int, int]:
    candidates = []
    for string, open_pitch in enumerate(tuning):
        fret = pitch - open_pitch
        if 0 <= fret <= max_fret and (used_strings is None or string not in used_strings):
            cost = fret if preferred_fret is None else abs(fret - preferred_fret) * 2 + fret * 0.05
            candidates.append((cost, string, fret))
    if not candidates:
        raise ValueError(f"pitch {midi_to_note(pitch)} is not playable on configured guitar")
    _, string, fret = min(candidates)
    return string, fret


def assign_guitar_chord(pitches: list[int], tuning: list[int], max_fret: int = 24,
                        preferred_fret: int | None = None) -> list[tuple[int, int, int]]:
    """Find a global one-note-per-string assignment instead of greedy local choices."""
    candidates: list[list[tuple[int, int]]] = []
    for pitch in pitches:
        options = [(string, pitch - open_pitch) for string, open_pitch in enumerate(tuning)
                   if 0 <= pitch - open_pitch <= max_fret]
        if not options:
            raise ValueError(f"pitch {midi_to_note(pitch)} is not playable on configured guitar")
        candidates.append(options)
    best: tuple[float, tuple[tuple[int, int], ...]] | None = None
    for assignment in itertools.product(*candidates):
        strings = [item[0] for item in assignment]
        if len(set(strings)) != len(strings):
            continue
        frets = [item[1] for item in assignment]
        span = max(frets) - min(frets)
        centre = sum(frets) / len(frets)
        position_cost = centre if preferred_fret is None else abs(centre - preferred_fret)
        cost = span * 3 + position_cost + sum(frets) * 0.02
        if best is None or cost < best[0]:
            best = (cost, assignment)
    if best is None:
        rendered = ", ".join(midi_to_note(pitch) for pitch in pitches)
        raise ValueError(f"guitar chord has no one-note-per-string assignment: {rendered}")
    return [(pitch, string, fret) for pitch, (string, fret) in zip(pitches, best[1])]


def midi_pitch(value: str | int) -> int:
    return note_number(value)


def merge_same_pitch_legato(events: list[dict[str, Any]], beats_per_bar: int) -> list[dict[str, Any]]:
    """Merge sustained common tones even when voice-leading swaps their voice index."""
    controls = [event for event in events if event.get("type") == "control_change"]
    lanes: dict[int, list[dict[str, Any]]] = {}
    for event in events:
        if event.get("type", "note") != "note":
            continue
        pitch = note_number(event["pitch"])
        start = position(event["at"], beats_per_bar)
        end = start + float(event["duration"])
        lane = lanes.setdefault(pitch, [])
        if lane and start <= lane[-1]["_end"] + 1e-6:
            lane[-1]["_end"] = max(lane[-1]["_end"], end)
            lane[-1]["articulations"] = list(dict.fromkeys(
                lane[-1].get("articulations", []) + event.get("articulations", [])
            ))
            lane[-1]["_common_tone"] = True
        else:
            lane.append({**event, "_start_value": start, "_end": end})
    merged = []
    for lane in lanes.values():
        for event in lane:
            start = event.pop("_start_value")
            end = event.pop("_end")
            event["duration"] = round(end - start, 3)
            merged.append(event)
    return sorted(merged + controls, key=lambda event: position(event["at"], beats_per_bar))
