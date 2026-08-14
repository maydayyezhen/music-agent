from __future__ import annotations

from typing import Any

from .common import assign_guitar_note, harmony, note, root_pc, seeded

STANDARD_BASS = [28, 33, 38, 43]  # E1 A1 D2 G2


def compile_phrase(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    if phrase["phrase_type"] not in {"kick_locked_line", "supportive_bass", "connecting_bass"}:
        raise ValueError(f"unsupported electric bass phrase_type: {phrase['phrase_type']!r}")
    tuning = [int(value) for value in phrase.get("tuning", STANDARD_BASS)]
    register = phrase.get("register_midi", [28, 52])
    kick_offsets = [float(value) for value in phrase.get("kick_offsets", [0.0, 2.0])]
    rng = seeded(phrase)
    velocity = int(round(56 + float(phrase.get("energy", 0.5)) * 42))
    result: list[dict[str, Any]] = []
    previous_fret = 3
    spans = harmony(phrase, beats_per_bar)
    for index, span in enumerate(spans):
        pc = root_pc(span["chord"])
        roots = [value for value in range(int(register[0]), int(register[1]) + 1) if value % 12 == pc]
        root = min(roots, key=lambda value: abs(value - (tuning[0] + previous_fret)))
        fifth = root + 7 if root + 7 <= int(register[1]) else root - 5
        next_pc = root_pc(spans[(index + 1) % len(spans)]["chord"])
        approach_candidates = [value for value in range(int(register[0]), int(register[1]) + 1)
                               if (value + 1) % 12 == next_pc or (value - 1) % 12 == next_pc]
        approach = min(approach_candidates, key=lambda value: abs(value - root))
        pattern = [(0.0, root, "root", 1.55), (2.0, fifth, "fifth", 0.75),
                   (3.25, approach, "approach", 0.55)]
        if index % 2:
            pattern = [(0.0, root, "root", 0.8), (1.0, root + 12 if root + 12 <= register[1] else fifth, "octave", 0.65),
                       (2.0, fifth, "fifth", 0.7), (3.25, approach, "approach", 0.55)]
        for local, pitch, function, duration in pattern:
            if local >= span["duration"]:
                continue
            string, fret = assign_guitar_note(pitch, tuning, 24, previous_fret)
            previous_fret = fret
            locked = any(abs(local - offset) < 0.02 for offset in kick_offsets)
            arts = list(phrase.get("articulations", ["finger"])) + (["accent"] if locked else [])
            result.append(note(pitch, span["start"] + local, min(duration, span["duration"] - local),
                               velocity + (7 if locked else -2) + rng.choice([-1, 0, 0, 1]), beats_per_bar,
                               arts, _string=string, _fret=fret, _bass_function=function, _kick_locked=locked))
    return result
