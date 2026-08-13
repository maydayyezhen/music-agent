from __future__ import annotations

import re

NOTE_RE = re.compile(r"^([A-Ga-g])([#b]?)(-?\d+)$")
SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
DRUM_NOTES = {
    "kick": 36,
    "snare": 38,
    "side_stick": 37,
    "closed_hat": 42,
    "pedal_hat": 44,
    "open_hat": 46,
    "crash": 49,
    "ride": 51,
    "low_tom": 45,
    "mid_tom": 47,
    "high_tom": 50,
    "tambourine": 54,
}


def note_number(value: str | int) -> int:
    if isinstance(value, int):
        number = value
    else:
        match = NOTE_RE.match(value)
        if not match:
            raise ValueError(f"invalid pitch: {value!r}")
        letter, accidental, octave_text = match.groups()
        accidental_offset = {"": 0, "#": 1, "b": -1}[accidental]
        number = (int(octave_text) + 1) * 12 + SEMITONES[letter.upper()] + accidental_offset
    if not 0 <= number <= 127:
        raise ValueError(f"MIDI note outside 0..127: {value!r}")
    return number


def drum_number(value: str | int) -> int:
    if isinstance(value, str) and value in DRUM_NOTES:
        return DRUM_NOTES[value]
    return note_number(value)
