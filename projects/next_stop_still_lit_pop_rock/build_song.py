from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SONG = "next_stop_still_lit_pop_rock"
TITLE = "下一站还亮着 (Next Stop Still Lit)"
TEMPO = 116
TIME_SIGNATURE = "4/4"
KEY = "D major / B minor color"

SECTIONS = [
    ("intro", 4, "standard"),
    ("verse_1", 12, "rich"),
    ("pre_1", 8, "rich"),
    ("chorus_1", 12, "rich"),
    ("verse_2", 12, "rich"),
    ("pre_2", 8, "rich"),
    ("chorus_2", 12, "dense"),
    ("bridge", 8, "rich"),
    ("final_chorus", 8, "dense"),
    ("outro", 4, "standard"),
]

PROGRESSIONS = {
    "intro": ["D", "A/C#", "Bm", "G"],
    "verse_1": ["D", "A/C#", "Bm", "G", "D/F#", "G", "Em", "A", "Bm", "G", "D", "A"],
    "pre_1": ["Em", "G", "D/F#", "A", "Em", "G", "Asus4", "A"],
    "chorus_1": ["G", "A", "F#m", "Bm", "G", "A", "D", "D/F#", "G", "A", "Bm", "A"],
    "verse_2": ["Bm", "G", "D", "A", "Bm", "G", "D/F#", "A", "Em", "G", "D", "A"],
    "pre_2": ["Em", "G", "D/F#", "A", "Em", "G", "Asus4", "A"],
    "chorus_2": ["G", "A", "F#m", "Bm", "G", "A", "D", "D/F#", "Em", "G", "A", "A"],
    "bridge": ["Bm", "A", "G", "D/F#", "Em", "G", "Asus4", "A"],
    "final_chorus": ["G", "A", "D", "Bm", "G", "A", "D", "A"],
    "outro": ["D", "A/C#", "G", "D"],
}

H = {
    "D": {
        "ac": ["D3", "A3", "D4", "F#4"],
        "high": ["A3", "D4", "F#4"],
        "power": ["D3", "A3"],
        "organ": ["D3", "A3", "D4", "F#4"],
        "bass": "D2", "fifth": "A2", "color": "F#2",
    },
    "D/F#": {
        "ac": ["D3", "A3", "D4", "F#4"],
        "high": ["A3", "D4", "F#4"],
        "power": ["D3", "A3"],
        "organ": ["F#3", "A3", "D4", "F#4"],
        "bass": "F#2", "fifth": "A2", "color": "D2",
    },
    "A": {
        "ac": ["A2", "E3", "A3", "C#4"],
        "high": ["E3", "A3", "C#4"],
        "power": ["A2", "E3"],
        "organ": ["A2", "E3", "A3", "C#4"],
        "bass": "A1", "fifth": "E2", "color": "C#2",
    },
    "A/C#": {
        "ac": ["A2", "E3", "A3", "C#4"],
        "high": ["E3", "A3", "C#4"],
        "power": ["A2", "E3"],
        "organ": ["C#3", "E3", "A3", "C#4"],
        "bass": "C#2", "fifth": "E2", "color": "A1",
    },
    "Asus4": {
        "ac": ["A2", "E3", "A3", "D4"],
        "high": ["E3", "A3", "D4"],
        "power": ["A2", "E3"],
        "organ": ["A2", "E3", "A3", "D4"],
        "bass": "A1", "fifth": "E2", "color": "D2",
    },
    "Bm": {
        "ac": ["B2", "F#3", "B3", "D4"],
        "high": ["F#3", "B3", "D4"],
        "power": ["B2", "F#3"],
        "organ": ["B2", "F#3", "B3", "D4"],
        "bass": "B1", "fifth": "F#2", "color": "D2",
    },
    "G": {
        "ac": ["G2", "D3", "G3", "B3"],
        "high": ["D3", "G3", "B3"],
        "power": ["G2", "D3"],
        "organ": ["G2", "D3", "G3", "B3"],
        "bass": "G1", "fifth": "D2", "color": "B1",
    },
    "Em": {
        "ac": ["E2", "B2", "E3", "G3"],
        "high": ["B2", "E3", "G3"],
        "power": ["E2", "B2"],
        "organ": ["E3", "G3", "B3", "E4"],
        "bass": "E2", "fifth": "B2", "color": "G2",
    },
    "F#m": {
        "ac": ["F#2", "C#3", "F#3", "A3"],
        "high": ["C#3", "F#3", "A3"],
        "power": ["F#2", "C#3"],
        "organ": ["F#2", "C#3", "F#3", "A3"],
        "bass": "F#1", "fifth": "C#2", "color": "A1",
    },
}

APPROACH = {
    "D": "C#2", "D/F#": "E2", "A": "G#1", "A/C#": "B1",
    "Asus4": "G#1", "Bm": "A1", "G": "F#1", "Em": "D#2", "F#m": "E1",
}


def pos(bar: int, beat: float) -> str:
    text = f"{beat:.2f}".rstrip("0").rstrip(".")
    return f"{bar}:{text}"


def note(bar: int, beat: float, pitch: str, dur: float, vel: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": pos(bar, beat), "duration": dur, "velocity": max(1, min(127, vel))}


def chord(bar: int, beat: float, pitches: list[str], dur: float, vel: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": pos(bar, beat), "duration": dur, "velocity": max(1, min(127, vel))}


def drum(bar: int, beat: float, name: str, vel: int, dur: float = 0.10) -> dict:
    return {"type": "drum", "note": name, "at": pos(bar, beat), "duration": dur, "velocity": max(1, min(127, vel))}


def clip(events: list[dict], bars: int) -> dict:
    return {"loop_bars": bars, "events": events}


VOCAL_LINES = {
    "intro": [
        (3, 2.0, "F#4", .75, 72), (3, 3.0, "A4", .75, 76), (3, 4.0, "B4", .90, 79),
        (4, 1.5, "A4", .85, 77), (4, 2.75, "F#4", .70, 73), (4, 3.75, "E4", 1.05, 71),
    ],
    "verse_1": [
        (1, 1.5, "F#4", .75, 76), (1, 2.5, "A4", .75, 79), (1, 3.5, "B4", 1.20, 82),
        (2, 1.25, "A4", 1.35, 80), (2, 3.0, "E4", .70, 73), (2, 4.0, "F#4", .80, 76),
        (3, 2.0, "D4", 1.05, 72), (3, 3.5, "F#4", 1.20, 76),
        (4, 1.5, "G4", .70, 78), (4, 2.5, "F#4", .70, 76), (4, 3.5, "E4", 1.35, 73),
        (5, 1.0, "F#4", .80, 77), (5, 2.0, "A4", .80, 80), (5, 3.25, "B4", 1.40, 83),
        (6, 1.5, "D5", .80, 85), (6, 2.5, "B4", .70, 82), (6, 3.5, "A4", 1.35, 79),
        (7, 2.0, "G4", 1.00, 76), (7, 3.5, "E4", 1.20, 72),
        (8, 1.5, "F#4", .70, 76), (8, 2.5, "E4", .70, 72), (8, 3.5, "C#4", 1.30, 70),
        (9, 1.0, "B4", .75, 81), (9, 2.0, "D5", .75, 84), (9, 3.25, "F#5", 1.15, 86),
        (10, 1.5, "B4", 1.00, 81), (10, 3.0, "A4", .75, 78), (10, 4.0, "G4", .80, 75),
        (11, 1.0, "F#4", .70, 76), (11, 2.25, "A4", .85, 80), (11, 3.5, "F#4", 1.20, 76),
        (12, 1.5, "E4", .70, 73), (12, 2.5, "C#4", .70, 70), (12, 3.5, "D4", 1.40, 72),
    ],
    "pre_1": [
        (1, 1.0, "G4", .75, 78), (1, 2.0, "A4", .65, 80), (1, 3.0, "B4", 1.15, 82),
        (2, 1.0, "B4", .75, 82), (2, 2.0, "D5", .75, 85), (2, 3.25, "B4", 1.20, 82),
        (3, 1.0, "A4", .75, 80), (3, 2.0, "B4", .75, 82), (3, 3.0, "D5", 1.25, 86),
        (4, 1.0, "C#5", .75, 85), (4, 2.0, "E5", .75, 88), (4, 3.25, "C#5", 1.20, 84),
        (5, 1.0, "B4", .70, 83), (5, 2.0, "D5", .70, 86), (5, 3.0, "E5", 1.20, 89),
        (6, 1.0, "D5", .70, 86), (6, 2.0, "E5", .70, 89), (6, 3.0, "F#5", 1.20, 92),
        (7, 1.0, "E5", .70, 89), (7, 2.0, "F#5", .70, 92), (7, 3.0, "G5", 1.15, 94),
        (8, 1.0, "E5", .70, 90), (8, 2.0, "F#5", .70, 93), (8, 3.0, "A5", 1.70, 97),
    ],
    "chorus_1": [
        (1, 1.0, "B4", .70, 88), (1, 2.0, "D5", .70, 91), (1, 3.0, "D5", .50, 91), (1, 4.0, "E5", .80, 93),
        (2, 1.0, "E5", .70, 93), (2, 2.0, "F#5", .70, 96), (2, 3.0, "E5", 1.35, 92),
        (3, 1.5, "C#5", .70, 89), (3, 2.5, "A4", .70, 84), (3, 3.5, "C#5", 1.20, 88),
        (4, 1.0, "D5", .80, 91), (4, 2.0, "F#5", .80, 96), (4, 3.25, "E5", 1.25, 92),
        (5, 1.0, "B4", .70, 88), (5, 2.0, "D5", .70, 91), (5, 3.0, "E5", .70, 94), (5, 4.0, "D5", .80, 90),
        (6, 1.0, "C#5", .70, 90), (6, 2.0, "E5", .70, 94), (6, 3.0, "F#5", .70, 97), (6, 4.0, "A5", .85, 100),
        (7, 1.5, "F#5", 1.20, 96), (7, 3.0, "E5", .70, 92), (7, 4.0, "D5", 1.15, 90),
        (8, 1.5, "A4", .70, 84), (8, 2.5, "B4", .70, 87), (8, 3.5, "D5", 1.25, 91),
        (9, 1.0, "D5", .70, 91), (9, 2.0, "E5", .70, 94), (9, 3.0, "F#5", 1.35, 97),
        (10, 1.0, "E5", .70, 94), (10, 2.0, "C#5", .70, 89), (10, 3.0, "B4", 1.55, 86),
        (11, 1.0, "D5", .70, 91), (11, 2.0, "F#5", .70, 96), (11, 3.0, "A5", 1.45, 100),
        (12, 1.5, "E5", .70, 93), (12, 2.5, "F#5", .70, 96), (12, 3.5, "E5", 1.15, 92),
    ],
    "verse_2": [
        (1, 1.25, "D5", .65, 82), (1, 2.0, "B4", .65, 79), (1, 3.0, "F#4", 1.05, 75),
        (2, 1.5, "G4", .70, 76), (2, 2.5, "B4", .70, 80), (2, 3.5, "D5", 1.10, 84),
        (3, 1.0, "A4", .70, 79), (3, 2.0, "F#4", .70, 75), (3, 3.25, "E4", 1.20, 72),
        (4, 1.5, "C#5", .70, 83), (4, 2.5, "B4", .70, 80), (4, 3.5, "A4", 1.25, 78),
        (5, 1.0, "B4", .70, 81), (5, 2.0, "D5", .70, 84), (5, 3.25, "F#5", 1.20, 88),
        (6, 1.25, "D5", .70, 84), (6, 2.25, "B4", .70, 81), (6, 3.25, "A4", 1.25, 78),
        (7, 1.0, "A4", .70, 80), (7, 2.0, "B4", .70, 82), (7, 3.0, "D5", .70, 85), (7, 4.0, "F#5", .80, 89),
        (8, 1.5, "E5", .70, 86), (8, 2.5, "C#5", .70, 82), (8, 3.5, "A4", 1.20, 78),
        (9, 1.0, "G4", .70, 77), (9, 2.0, "B4", .70, 81), (9, 3.0, "E5", 1.25, 87),
        (10, 1.5, "D5", .70, 84), (10, 2.5, "B4", .70, 81), (10, 3.5, "G4", 1.20, 76),
        (11, 1.0, "F#4", .70, 76), (11, 2.0, "A4", .70, 80), (11, 3.0, "D5", 1.30, 85),
        (12, 1.25, "C#5", .70, 83), (12, 2.25, "B4", .70, 80), (12, 3.25, "A4", 1.35, 78),
    ],
    "pre_2": [
        (1, 1.0, "B4", .70, 82), (1, 2.0, "G4", .70, 78), (1, 3.0, "B4", 1.10, 83),
        (2, 1.0, "D5", .70, 86), (2, 2.0, "B4", .70, 82), (2, 3.0, "D5", 1.15, 86),
        (3, 1.0, "A4", .70, 80), (3, 2.0, "D5", .70, 86), (3, 3.0, "F#5", 1.15, 92),
        (4, 1.0, "E5", .70, 89), (4, 2.0, "C#5", .70, 85), (4, 3.0, "E5", 1.15, 90),
        (5, 1.0, "B4", .70, 84), (5, 2.0, "D5", .70, 87), (5, 3.0, "E5", 1.15, 91),
        (6, 1.0, "D5", .70, 88), (6, 2.0, "F#5", .70, 93), (6, 3.0, "G5", 1.15, 95),
        (7, 1.0, "E5", .70, 91), (7, 2.0, "G5", .70, 96), (7, 3.0, "A5", 1.10, 99),
        (8, 1.0, "F#5", .70, 95), (8, 2.0, "E5", .70, 91), (8, 3.0, "A5", 1.70, 100),
    ],
    "chorus_2": [
        (1, 1.0, "B4", .65, 90), (1, 1.75, "D5", .65, 93), (1, 2.75, "E5", .65, 95), (1, 3.75, "F#5", .95, 98),
        (2, 1.0, "E5", .70, 95), (2, 2.0, "F#5", .70, 98), (2, 3.0, "A5", 1.35, 102),
        (3, 1.0, "F#5", .70, 97), (3, 2.0, "C#5", .70, 90), (3, 3.0, "A4", 1.35, 85),
        (4, 1.0, "D5", .70, 93), (4, 2.0, "F#5", .70, 98), (4, 3.0, "B5", 1.35, 103),
        (5, 1.0, "A5", .70, 101), (5, 2.0, "F#5", .70, 98), (5, 3.0, "E5", 1.35, 94),
        (6, 1.0, "C#5", .70, 91), (6, 2.0, "E5", .70, 95), (6, 3.0, "F#5", 1.35, 98),
        (7, 1.0, "A5", .80, 102), (7, 2.25, "F#5", .80, 98), (7, 3.5, "D5", 1.15, 93),
        (8, 1.0, "A4", .70, 85), (8, 2.0, "B4", .70, 88), (8, 3.0, "D5", .70, 92), (8, 4.0, "F#5", .80, 98),
        (9, 1.0, "G5", .70, 98), (9, 2.0, "E5", .70, 94), (9, 3.0, "B4", 1.35, 87),
        (10, 1.0, "D5", .70, 92), (10, 2.0, "B4", .70, 88), (10, 3.0, "G4", 1.35, 82),
        (11, 1.0, "E5", .70, 95), (11, 2.0, "F#5", .70, 98), (11, 3.0, "A5", 1.35, 102),
        (12, 1.0, "E5", .70, 94), (12, 2.0, "C#5", .70, 90), (12, 3.0, "A4", 1.60, 85),
    ],
    "bridge": [
        (5, 1.0, "B4", 1.55, 84), (5, 3.0, "E5", 1.55, 90),
        (6, 1.0, "D5", 1.55, 88), (6, 3.0, "B4", 1.55, 84),
        (7, 1.0, "D5", .80, 88), (7, 2.0, "E5", .80, 91), (7, 3.0, "G5", 1.55, 96),
        (8, 1.0, "F#5", .80, 94), (8, 2.0, "E5", .80, 91), (8, 3.0, "A5", 1.55, 99),
    ],
    "final_chorus": [
        (1, 1.0, "D5", .70, 94), (1, 2.0, "E5", .70, 96), (1, 3.0, "F#5", 1.25, 100),
        (2, 1.0, "E5", .70, 96), (2, 2.0, "F#5", .70, 100), (2, 3.0, "A5", 1.30, 104),
        (3, 1.0, "A5", .80, 104), (3, 2.25, "F#5", .80, 100), (3, 3.5, "D5", 1.15, 94),
        (4, 1.0, "D5", .70, 94), (4, 2.0, "F#5", .70, 100), (4, 3.0, "B5", 1.35, 105),
        (5, 1.0, "A5", .70, 103), (5, 2.0, "F#5", .70, 100), (5, 3.0, "E5", 1.35, 96),
        (6, 1.0, "C#5", .70, 92), (6, 2.0, "E5", .70, 96), (6, 3.0, "A5", 1.45, 104),
        (7, 1.0, "F#5", .80, 101), (7, 2.25, "E5", .80, 97), (7, 3.5, "D5", 1.30, 94),
        (8, 1.0, "C#5", .70, 92), (8, 2.0, "B4", .70, 88), (8, 3.0, "A4", 1.60, 85),
    ],
    "outro": [
        (1, 1.5, "F#4", .75, 75), (1, 2.5, "A4", .75, 78), (1, 3.5, "B4", 1.15, 80),
        (2, 1.5, "A4", .80, 78), (2, 3.0, "E4", 1.15, 72),
        (3, 1.5, "G4", .80, 75), (3, 2.75, "F#4", .70, 73), (3, 3.75, "E4", 1.05, 71),
        (4, 1.0, "F#4", .75, 74), (4, 2.0, "E4", .75, 72), (4, 3.0, "D4", 1.85, 70),
    ],
}


def vocal_section(name: str) -> list[dict]:
    return [note(bar, beat, pitch, dur, vel) for bar, beat, pitch, dur, vel in VOCAL_LINES.get(name, [])]


ACOUSTIC_PATTERNS = {
    "light": [(1.0, "full", 0), (1.75, "high", -7), (2.0, "full", -2), (2.75, "high", -8), (3.0, "full", 1), (3.75, "high", -7), (4.0, "full", -1)],
    "flow": [(1.0, "full", 1), (1.5, "high", -5), (1.75, "high", -8), (2.0, "full", -1), (2.75, "high", -7), (3.0, "full", 1), (3.5, "high", -5), (3.75, "high", -8), (4.0, "full", -1), (4.5, "high", -6)],
    "build": [(1.0, "full", 1), (1.5, "high", -5), (1.75, "high", -7), (2.0, "full", 0), (2.5, "high", -5), (2.75, "high", -7), (3.0, "full", 2), (3.5, "high", -4), (3.75, "high", -7), (4.0, "full", 1), (4.5, "high", -4), (4.75, "high", -7)],
    "chorus": [(1.0, "full", 1), (1.5, "high", -5), (2.0, "full", -1), (2.5, "high", -6), (3.0, "full", 1), (3.5, "high", -5), (4.0, "full", -1), (4.5, "high", -6)],
}


def acoustic_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    progression = PROGRESSIONS[name]
    for bar, symbol in enumerate(progression, 1):
        if name == "bridge" and bar <= 4:
            continue
        if name == "intro":
            pattern = ACOUSTIC_PATTERNS["light"] if bar <= 2 else ACOUSTIC_PATTERNS["flow"]
            base = 64 if bar <= 2 else 69
        elif name.startswith("verse"):
            pattern, base = ACOUSTIC_PATTERNS["flow"], 67 if name == "verse_1" else 69
        elif name.startswith("pre"):
            pattern, base = ACOUSTIC_PATTERNS["build"], 70 + min(4, bar // 2)
        elif name in {"chorus_1", "chorus_2", "final_chorus"}:
            pattern, base = ACOUSTIC_PATTERNS["chorus"], 68 if name == "chorus_1" else 70
        elif name == "bridge":
            pattern, base = ACOUSTIC_PATTERNS["build"], 67 + (bar - 4)
        else:
            pattern, base = ACOUSTIC_PATTERNS["light"], 62
        for idx, (beat, width, delta) in enumerate(pattern):
            pitches = H[symbol]["ac"] if width == "full" else H[symbol]["high"]
            if width == "high" and bar % 4 == 0 and idx in {2, 7}:
                continue
            out.append(chord(bar, beat, pitches, .43 if width == "full" else .21, base + delta))
    return out


def muted_guitar_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    if name == "intro":
        active_bars, beats, base = range(3, 5), [1.0, 1.5, 2.0, 2.5, 3.5, 4.0], 61
    elif name == "verse_1":
        active_bars, beats, base = range(5, bars + 1), [1.0, 1.5, 2.0, 2.5, 3.5, 4.0], 62
    elif name == "verse_2":
        active_bars, beats, base = range(1, bars + 1), [1.0, 1.5, 2.0, 2.5, 3.5, 4.0, 4.5], 63
    elif name.startswith("pre"):
        active_bars, beats, base = range(1, bars + 1), [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5], 64
    elif name == "bridge":
        active_bars, beats, base = range(5, bars + 1), [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5], 62
    else:
        return out
    for bar in active_bars:
        symbol = PROGRESSIONS[name][bar - 1]
        local_beats = list(beats)
        if bar % 4 == 0 and name.startswith("verse"):
            local_beats = [beat for beat in local_beats if beat not in {3.5, 4.5}]
        for index, beat in enumerate(local_beats):
            ramp = min(9, index * 2)
            phrase_boost = min(8, max(0, bar - 1)) if name.startswith("pre") or name == "bridge" else 0
            out.append(chord(bar, beat, H[symbol]["power"], .22, base + ramp + phrase_boost))
    return out


def rhythm_guitar_section(name: str, bars: int) -> list[dict]:
    if name not in {"chorus_1", "chorus_2", "final_chorus", "bridge"}:
        return []
    out: list[dict] = []
    for bar, symbol in enumerate(PROGRESSIONS[name], 1):
        if name == "bridge" and bar > 4:
            continue
        if name == "bridge":
            hits = [(1.0, 1.90, 70), (3.0, 1.90, 67)]
        else:
            base = 73 if name == "chorus_1" else 76 if name == "chorus_2" else 80
            hits = [(1.0, .96, base + 2), (2.0, .96, base), (3.0, .96, base + 2), (4.0, .96, base)]
        for beat, dur, vel in hits:
            out.append(chord(bar, beat, H[symbol]["power"], dur, vel))
    return out


LEAD_GUITAR_LINES = {
    "chorus_1": [(4, 4.55, "B4", 1.00, 83), (8, 4.50, "A4", 1.10, 81), (12, 4.45, "C#5", 1.00, 85)],
    "chorus_2": [(4, 4.45, "D5", 1.10, 87), (8, 4.50, "F#5", 1.10, 90), (12, 4.45, "E5", 1.05, 88)],
    "bridge": [
        (1, 1.0, "F#4", 1.45, 84), (1, 2.75, "A4", .85, 87), (1, 3.75, "B4", 1.10, 90),
        (2, 1.0, "C#5", .90, 91), (2, 2.25, "B4", .80, 88), (2, 3.25, "A4", 1.40, 86),
        (3, 1.0, "B4", .90, 89), (3, 2.25, "D5", .95, 92), (3, 3.50, "E5", 1.30, 94),
        (4, 1.0, "F#5", 1.85, 96), (4, 3.25, "E5", 1.40, 93),
        (6, 3.0, "D5", 1.55, 88), (8, 3.0, "E5", 1.55, 90),
    ],
    "final_chorus": [(4, 4.45, "F#5", 1.10, 91), (8, 4.35, "A5", 1.20, 94)],
}


def lead_guitar_section(name: str) -> list[dict]:
    return [note(bar, beat, pitch, dur, vel) for bar, beat, pitch, dur, vel in LEAD_GUITAR_LINES.get(name, [])]


def bass_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    progression = PROGRESSIONS[name]
    section_names = [item[0] for item in SECTIONS]
    for bar, symbol in enumerate(progression, 1):
        current = H[symbol]
        if bar < len(progression):
            next_symbol = progression[bar]
        elif name != "outro":
            next_name = SECTIONS[section_names.index(name) + 1][0]
            next_symbol = PROGRESSIONS[next_name][0]
        else:
            next_symbol = "D"
        approach = APPROACH[next_symbol]
        if name == "intro":
            out += [note(bar, 1.0, current["bass"], 1.55, 72), note(bar, 3.0, current["fifth"], 1.35, 68)]
        elif name.startswith("verse") or name.startswith("pre"):
            out += [
                note(bar, 1.0, current["bass"], .72, 76 if name.startswith("verse") else 79),
                note(bar, 2.0, current["fifth"] if bar % 2 else current["bass"], 1.45, 73 if name.startswith("verse") else 77),
                note(bar, 4.0, approach, .70, 72 if name.startswith("verse") else 77),
            ]
            if name.startswith("pre") and bar in {4, 8}:
                out.append(note(bar, 3.5, current["color"], .38, 76 + bar))
        elif name in {"chorus_1", "chorus_2", "final_chorus"}:
            base = 81 if name == "chorus_1" else 84 if name == "chorus_2" else 87
            third_pitch = current["color"] if bar % 2 == 0 else current["bass"]
            out += [note(bar, 1.0, current["bass"], .72, base + 2), note(bar, 2.0, current["fifth"], .68, base), note(bar, 3.0, third_pitch, .68, base - 1), note(bar, 4.0, approach, .72, base)]
            if (name != "chorus_1" and bar in {6, bars}) or (name == "chorus_1" and bar == bars):
                out.append(note(bar, 4.5, current["color"], .35, base + 2))
        elif name == "bridge":
            if bar <= 4:
                out += [note(bar, 1.0, current["bass"], 1.55, 75), note(bar, 3.0, current["color"], 1.25, 72)]
            else:
                out += [note(bar, 1.0, current["bass"], .72, 78 + bar - 4), note(bar, 2.0, current["fifth"], .72, 76 + bar - 4), note(bar, 3.0, current["color"], .72, 75 + bar - 4), note(bar, 4.0, approach, .72, 77 + bar - 4)]
        else:
            out += [note(bar, 1.0, current["bass"], 1.55, 70), note(bar, 3.0, current["fifth"], 1.30, 66)]
    return out


def organ_section(name: str, bars: int) -> list[dict]:
    if name not in {"pre_1", "pre_2", "chorus_1", "chorus_2", "bridge", "final_chorus"}:
        return []
    out: list[dict] = []
    for bar, symbol in enumerate(PROGRESSIONS[name], 1):
        if name.startswith("pre"):
            vel, dur = 43 + min(10, bar), 3.72
        elif name == "bridge":
            vel, dur = (48 if bar <= 4 else 52 + (bar - 4)), 3.76
        else:
            vel, dur = (47 if name == "chorus_1" else 50 if name == "chorus_2" else 54), 3.78
        out.append(chord(bar, 1.0, H[symbol]["organ"], dur, vel))
    return out


def add_hat_eighths(out: list[dict], bar: int, name: str, base: int) -> None:
    for index, beat in enumerate((1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5)):
        out.append(drum(bar, beat, name, base + (4 if index % 2 == 0 else -3), .08))


def add_fill(out: list[dict], bar: int, base: int) -> None:
    for beat, drum_name, delta in ((3.50, "high_tom", 0), (3.75, "mid_tom", 3), (4.00, "low_tom", 5), (4.25, "snare", 7), (4.50, "mid_tom", 5), (4.75, "snare", 9)):
        out.append(drum(bar, beat, drum_name, base + delta, .10))


def drums_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    if name == "intro":
        for bar in range(1, bars + 1):
            if bar <= 2:
                for beat in (1.0, 2.0, 3.0, 4.0): out.append(drum(bar, beat, "closed_hat", 45 if beat in {1.0, 3.0} else 39, .08))
                for beat in (1.0, 3.0): out.append(drum(bar, beat, "kick", 75, .10))
                for beat in (2.0, 4.0): out.append(drum(bar, beat, "side_stick", 61, .10))
            else:
                add_hat_eighths(out, bar, "closed_hat", 49)
                for beat in (1.0, 3.0, 3.5): out.append(drum(bar, beat, "kick", 82, .10))
                for beat in (2.0, 4.0): out.append(drum(bar, beat, "snare", 75, .10))
                if bar == 4: out.append(drum(bar, 4.5, "open_hat", 66, .16))
        return out
    if name.startswith("verse"):
        for bar in range(1, bars + 1):
            add_hat_eighths(out, bar, "closed_hat", 52 if name == "verse_1" else 55)
            kicks = (1.0, 2.75, 3.5) if bar % 2 else (1.0, 1.75, 3.0, 4.5)
            for beat in kicks: out.append(drum(bar, beat, "kick", 86 if name == "verse_1" else 89, .10))
            for beat in (2.0, 4.0): out.append(drum(bar, beat, "snare", 82 if name == "verse_1" else 85, .10))
            if bar in {2, 6, 10}: out.append(drum(bar, 3.75, "side_stick", 48, .08))
            if name == "verse_2" and bar in {4, 8}: out.append(drum(bar, 4.5, "open_hat", 67, .16))
            if bar in {4, 8, 12}: add_fill(out, bar, 66 if name == "verse_1" else 69)
        return out
    if name.startswith("pre"):
        for bar in range(1, bars + 1):
            add_hat_eighths(out, bar, "closed_hat", 54 + bar)
            for beat in (1.0, 1.75, 3.0, 3.5): out.append(drum(bar, beat, "kick", 88 + min(8, bar), .10))
            for beat in (2.0, 4.0): out.append(drum(bar, beat, "snare", 86 + min(8, bar), .10))
            if bar in {4, 8}: out.append(drum(bar, 4.5, "open_hat", 72 + bar, .16))
            if bar == 8: add_fill(out, bar, 78)
        return out
    if name in {"chorus_1", "chorus_2", "final_chorus"}:
        for bar in range(1, bars + 1):
            add_hat_eighths(out, bar, "closed_hat", 61 if name == "chorus_1" else 64)
            kicks = [1.0, 1.5, 3.0, 3.5] + ([4.5] if bar % 2 else [])
            for beat in kicks: out.append(drum(bar, beat, "kick", 99 if name == "chorus_1" else 103, .10))
            for beat in (2.0, 4.0): out.append(drum(bar, beat, "snare", 98 if name == "chorus_1" else 102, .10))
            if name != "chorus_1":
                for beat in (2.0, 4.0): out.append(drum(bar, beat, "tambourine", 67 if name == "chorus_2" else 72, .08))
            if bar in {1, 5, 9}: out.append(drum(bar, 1.0, "crash", 102 if name == "chorus_1" else 108, .14))
            if bar in {4, 8, 12} and bar <= bars: add_fill(out, bar, 80 if name == "chorus_1" else 84)
        return out
    if name == "bridge":
        for bar in range(1, bars + 1):
            if bar <= 4:
                for beat in (1.0, 2.0, 3.0, 4.0): out.append(drum(bar, beat, "ride", 54 if beat != 1.0 else 59, .10))
                for beat in (1.0, 3.5): out.append(drum(bar, beat, "kick", 82, .10))
                out.append(drum(bar, 3.0, "snare", 88, .10))
            else:
                add_hat_eighths(out, bar, "closed_hat", 58 + (bar - 4) * 2)
                for beat in (1.0, 1.75, 3.0, 3.5): out.append(drum(bar, beat, "kick", 88 + (bar - 4) * 2, .10))
                for beat in (2.0, 4.0): out.append(drum(bar, beat, "snare", 89 + (bar - 4) * 2, .10))
                if bar == 8:
                    add_fill(out, bar, 84)
                    out.append(drum(bar, 4.75, "open_hat", 91, .16))
        return out
    for bar in range(1, bars + 1):
        for beat in (1.0, 2.0, 3.0, 4.0): out.append(drum(bar, beat, "ride", 50 - bar, .10))
        out.append(drum(bar, 1.0, "kick", 78 - bar * 2, .10))
        if bar < 4: out.append(drum(bar, 3.0, "snare", 71 - bar, .10))
        if bar == 4: out.append(drum(bar, 1.0, "crash", 88, .16))
    return out


def make_composition() -> dict:
    sections: list[dict] = []
    for name, bars, complexity in SECTIONS:
        if complexity == "dense": budget = {"lead": 5, "rhythm_section": 5, "guitars": 5, "harmony": 4}
        elif complexity == "rich": budget = {"lead": 4, "rhythm_section": 4, "guitars": 4, "harmony": 3}
        else: budget = {"lead": 2, "rhythm_section": 2, "guitars": 3, "harmony": 2}
        sections.append({"name": name, "bars": bars, "complexity": complexity, "complexity_budget": budget})

    tracks = {
        "vocal_lead": {"role": "foreground vocal surrogate / harmonica lead melody", "sections": {}},
        "acoustic_guitar": {"role": "steel-string sixteenth-grid rhythmic bed / vocal support", "sections": {}},
        "muted_guitar": {"role": "palm-muted pulse / verse and pre-chorus propulsion", "sections": {}},
        "rhythm_guitar": {"role": "continuous overdriven rhythm bed / chorus mass", "sections": {}},
        "lead_guitar": {"role": "sustained electric answer / bridge foreground handoff", "sections": {}},
        "bass": {"role": "section-linked contour-aware bass foundation", "sections": {}},
        "organ": {"role": "sustained harmonic color / pre-chorus and chorus support", "sections": {}},
        "drums": {"role": "pop-rock drum kit / groove and section dynamics", "sections": {}},
    }
    for name, bars, _ in SECTIONS:
        events = vocal_section(name)
        if events: tracks["vocal_lead"]["sections"][name] = clip(events, bars)
        events = acoustic_section(name, bars)
        if events: tracks["acoustic_guitar"]["sections"][name] = clip(events, bars)
        events = muted_guitar_section(name, bars)
        if events: tracks["muted_guitar"]["sections"][name] = clip(events, bars)
        events = rhythm_guitar_section(name, bars)
        if events: tracks["rhythm_guitar"]["sections"][name] = clip(events, bars)
        events = lead_guitar_section(name)
        if events: tracks["lead_guitar"]["sections"][name] = clip(events, bars)
        tracks["bass"]["sections"][name] = clip(bass_section(name, bars), bars)
        events = organ_section(name, bars)
        if events: tracks["organ"]["sections"][name] = clip(events, bars)
        tracks["drums"]["sections"][name] = clip(drums_section(name, bars), bars)
    return {
        "metadata": {
            "title": TITLE, "tempo": TEMPO, "time_signature": TIME_SIGNATURE, "key": KEY,
            "description": "Original three-minute pop-rock song. Harmonica serves as the vocal surrogate; steel-string acoustic guitar supplies flowing sixteenth-grid motion, muted and overdriven electric guitars split section roles, bass carries section-linked contour, organ supplies restrained harmonic color, and drums shape the energy arc.",
        },
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 3, "arrangement": 5, "melodic_ornamentation": 4, "density": 4, "variation": 4},
        "complexity_contour": "wave",
        "sections": sections,
        "tracks": tracks,
    }


INSTRUMENTS = {
    "vocal_lead": {"engine": "fluidsynth", "bank": 0, "program": 22, "gm_name": "Harmonica", "profile": "general_midi"},
    "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25, "gm_name": "Acoustic Guitar (steel)", "profile": "general_midi"},
    "muted_guitar": {"engine": "fluidsynth", "bank": 0, "program": 28, "gm_name": "Electric Guitar (muted)", "profile": "general_midi"},
    "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29, "gm_name": "Overdriven Guitar", "profile": "general_midi"},
    "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30, "gm_name": "Distortion Guitar", "profile": "general_midi"},
    "bass": {"engine": "fluidsynth", "bank": 0, "program": 33, "gm_name": "Electric Bass (finger)", "profile": "general_midi"},
    "organ": {"engine": "fluidsynth", "bank": 0, "program": 16, "gm_name": "Drawbar Organ", "profile": "general_midi"},
    "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 0, "gm_name": "Standard Drum Kit", "profile": "general_midi"},
}

RENDER = {
    "sample_rate": 44100,
    "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
    "fluidsynth_gain": 0.70,
    "tail_seconds": 2.0,
    "master_peak_db": -1.0,
    "mix": {
        "vocal_lead": {"volume_db": -2.3, "pan": 0.0, "mute": False},
        "acoustic_guitar": {"volume_db": -7.4, "pan": -0.34, "mute": False},
        "muted_guitar": {"volume_db": -8.4, "pan": 0.32, "mute": False},
        "rhythm_guitar": {"volume_db": -7.2, "pan": 0.44, "mute": False},
        "lead_guitar": {"volume_db": -5.4, "pan": 0.14, "mute": False},
        "bass": {"volume_db": -3.2, "pan": 0.0, "mute": False},
        "organ": {"volume_db": -10.2, "pan": -0.12, "mute": False},
        "drums": {"volume_db": -3.4, "pan": 0.0, "mute": False},
    },
}

MANIFEST = {
    "schema": "music-agent-project-facade",
    "schema_version": 1,
    "project": {"title": TITLE, "description": "Original structured pop-rock composition created under the V2 workflow."},
    "artifacts": {
        "composition": {"standard": "music-agent composition extension", "path": "composition.json", "authority": "authoritative"},
        "instrument_config": {"standard": "music-agent instrument extension", "path": "instruments.json", "authority": "authoritative"},
        "render_config": {"standard": "music-agent render extension", "path": "render.json", "authority": "authoritative"},
        "execution_midi": {"standard": "MIDI 1.0 Standard MIDI File", "path": "output/full_song.mid", "authority": "derived"},
        "final_audio": {"standard": "WAVE PCM audio", "path": "output/mix.wav", "authority": "derived"},
    },
}


def write_project(project_dir: Path) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    payloads = {"composition.json": make_composition(), "instruments.json": INSTRUMENTS, "render.json": RENDER, "manifest.json": MANIFEST}
    for filename, payload in payloads.items():
        (project_dir / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    bars = sum(bars for _, bars, _ in SECTIONS)
    duration = bars * 4 * 60 / TEMPO
    print(f"[OK] Built {SONG}: {bars} bars at {TEMPO} BPM ({duration:.1f}s score time)")
    print("[OK] Authoritative artifacts: composition.json, instruments.json, render.json")
    print("[OK] Project facade: manifest.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the structured V2 pop-rock project and optionally render it.")
    parser.add_argument("--render", action="store_true", help="after building, route rendering through scripts/render_project.py")
    args = parser.parse_args()
    project_dir = Path(__file__).resolve().parent
    root = project_dir.parents[1]
    write_project(project_dir)
    if args.render:
        return subprocess.run([sys.executable, str(root / "scripts" / "render_project.py"), SONG], cwd=root).returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
