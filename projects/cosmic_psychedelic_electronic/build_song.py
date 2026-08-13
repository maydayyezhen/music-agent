from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SECTIONS = [("launch", 8), ("orbital_garden", 12), ("prism_build", 8), ("zero_gravity", 8), ("wormhole", 12), ("apogee_bloom", 12), ("reentry", 8)]


def note(pitch: str, at: str, duration: float, velocity: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": at, "duration": duration, "velocity": velocity}


def chord(pitches: list[str], at: str, duration: float, velocity: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": at, "duration": duration, "velocity": velocity}


def drum(name: str, at: str, velocity: int, duration: float = .13) -> dict:
    return {"type": "drum", "note": name, "at": at, "duration": duration, "velocity": velocity}


def clip(bars: int, events: list[dict]) -> dict:
    return {"loop_bars": bars, "events": events}


ORBIT = [
    ("D2", ["A3", "C4", "E4", "F4"]), ("G1", ["B3", "D4", "E4", "F4"]),
    ("C2", ["G3", "B3", "D4", "E4"]), ("A1", ["G3", "A3", "C4", "E4"]),
]
TAIL = [
    ("Bb1", ["A3", "Bb3", "D4", "F4"]), ("C2", ["G3", "C4", "D4", "E4"]),
    ("D2", ["A3", "C4", "E4", "F4"]), ("G1", ["B3", "D4", "E4", "G4"]),
]
PRISM = [
    ("Bb1", ["A3", "D4", "F4", "Bb4"]), ("C2", ["G3", "C4", "E4", "G4"]),
    ("D2", ["A3", "C4", "E4", "F4"]), ("A1", ["A3", "C#4", "E4", "G4"]),
]
ZERO = [
    ("D2", ["A3", "C4", "E4", "F4"]), ("D2", ["G3", "C4", "E4", "G4"]),
    ("D2", ["G3", "B3", "D4", "E4"]), ("D2", ["A3", "Bb3", "D4", "F4"]),
]
WORM = [
    ("D2", ["A3", "C4", "D4", "F4"]), ("Eb2", ["G3", "Bb3", "D4", "Eb4"]),
    ("C2", ["G3", "Bb3", "D4", "E4"]), ("A1", ["G3", "A3", "C#4", "E4"]),
]


def lead_launch() -> list[dict]:
    return [
        note("D4", "2:3", .42, 68), note("A4", "2:3.5", .42, 72), note("C5", "2:4", 1.15, 76),
        note("D4", "4:2.5", .42, 72), note("A4", "4:3", .42, 76), note("C5", "4:3.5", .75, 80),
        note("E5", "6:2", 1.35, 84), note("F5", "7:2.5", .42, 86), note("E5", "7:3", .42, 82),
        note("C5", "7:3.5", .42, 79), note("D5", "7:4", .85, 85),
    ]


def lead_orbit() -> list[dict]:
    # Two 4-bar statements plus a displaced 4-bar developmental answer.
    phrase = [
        (1, 1, "D4", .42, 91), (1, 1.5, "A4", .42, 96), (1, 2, "C5", .9, 99), (1, 3, "E5", 1.45, 104),
        (2, 1, "F5", .42, 103), (2, 1.5, "E5", .42, 98), (2, 2, "C5", .42, 94), (2, 2.5, "D5", 1.35, 101),
        (3, 1.5, "A4", .42, 91), (3, 2, "C5", .42, 94), (3, 2.5, "D5", .9, 98), (3, 3.5, "F5", .9, 105),
        (4, 1, "E5", .42, 99), (4, 1.5, "C5", .42, 94), (4, 2, "A4", .9, 91), (4, 3, "D5", 1.45, 102),
    ]
    events = []
    for shift, trans in ((0, 0), (4, 0)):
        for b, beat, p, dur, vel in phrase:
            events.append(note(p, f"{b + shift}:{beat:g}", dur, vel + (3 if shift else 0)))
    answer = [
        (9, 1.5, "F4", .42), (9, 2, "C5", .42), (9, 2.5, "D5", .9), (9, 3.5, "G5", .9),
        (10, 1.5, "F5", .42), (10, 2, "D5", .42), (10, 2.5, "C5", .9), (10, 3.5, "D5", .9),
        (11, 1.5, "A4", .42), (11, 2, "C5", .42), (11, 2.5, "E5", .9), (11, 3.5, "F5", .9),
        (12, 1.5, "E5", .42), (12, 2, "C5", .42), (12, 2.5, "A4", .9), (12, 3.5, "D5", .9),
    ]
    events += [note(p, f"{b}:{beat:g}", dur, 96 + (5 if p in {"F5", "G5"} else 0)) for b, beat, p, dur in answer]
    return events


def lead_prism() -> list[dict]:
    events = []
    cells = [
        ["D4", "A4", "C5", "E5"], ["E4", "Bb4", "D5", "F5"],
        ["F4", "C5", "E5", "G5"], ["G4", "D5", "F5", "A5"],
    ]
    for pair in range(4):
        for local in range(2):
            bar = pair * 2 + local + 1
            cell = cells[pair]
            positions = (1, 1.5, 2, 3) if local == 0 else (1.5, 2, 2.5, 3.5)
            for i, (pitch, beat) in enumerate(zip(cell, positions)):
                events.append(note(pitch, f"{bar}:{beat:g}", .38 if i < 3 else .82, 88 + pair * 5 + i * 2))
    return events


def lead_zero() -> list[dict]:
    return [
        note("D5", "1:1", 2.7, 78), note("A4", "2:1", 1.7, 72), note("F4", "2:3", 1.7, 69),
        note("E5", "3:1", 2.7, 77), note("C5", "4:1", 1.7, 73), note("A4", "4:3", 1.7, 70),
        note("F5", "5:1", 2.7, 82), note("E5", "6:1", 1.7, 76), note("C5", "6:3", 1.7, 72),
        note("D5", "7:1", 3.35, 84),
    ]


def lead_worm() -> list[dict]:
    events = []
    cells = [["D4", "C5", "A4", "E5"], ["Eb4", "D5", "Bb4", "F5"], ["C4", "Bb4", "G4", "E5"], ["A3", "C#5", "G4", "E5"]]
    for bar in range(1, 13):
        cell = cells[(bar - 1) % 4]
        positions = (1.5, 2, 2.75, 3.5) if bar <= 4 else ((1, 1.75, 2.5, 3.25) if bar <= 8 else (1, 1.5, 2, 2.5))
        for i, (pitch, beat) in enumerate(zip(cell, positions)):
            events.append(note(pitch, f"{bar}:{beat:g}", .34 if i < 3 else (.7 if bar <= 8 else .42), 86 + bar + i * 3))
        if bar >= 9:
            events.append(note("D5" if bar % 2 else "E5", f"{bar}:3.5", .7, 104 + bar % 3))
    return events


def lead_apogee() -> list[dict]:
    base = lead_orbit()
    # Raise theme one octave where safe; G5 becomes G6, highest point is A6.
    order = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    def up(p: str) -> str:
        for name in sorted(order, key=len, reverse=True):
            if p.startswith(name):
                return name + str(int(p[len(name):]) + 1)
        raise ValueError(p)
    for event in base:
        event["pitch"] = up(event["pitch"])
        event["velocity"] = min(118, event["velocity"] + 5)
    # Expand final landing rather than ending with the displaced answer unchanged.
    base += [note("F6", "11:4", .42, 112), note("E6", "12:1", .42, 108), note("D6", "12:1.5", .75, 111), note("A6", "12:2.5", 1.65, 118)]
    return base


def lead_reentry() -> list[dict]:
    return [
        note("F5", "1:1", .7, 92), note("E5", "1:2", .7, 88), note("C5", "1:3", .7, 84), note("D5", "1:4", 1.4, 90),
        note("E5", "3:1", .7, 85), note("C5", "3:2", .7, 81), note("A4", "3:3", .7, 77), note("D5", "3:4", 1.4, 86),
        note("A4", "5:1", 1.6, 74), note("D5", "5:3", 1.6, 78), note("A4", "7:1", 1.6, 66), note("D4", "7:3", 3.6, 70),
    ]


def bass_events(prog: list[tuple[str, list[str]]], bars: int, mode: str) -> list[dict]:
    patterns = {
        "D2": ["D2", "A2", "C3", "D3", "F2", "A2", "C3", "C#3"],
        "G1": ["G1", "D2", "F2", "G2", "B2", "A2", "G#2", "A2"],
        "C2": ["C2", "G2", "B2", "C3", "E2", "G2", "A2", "G#2"],
        "A1": ["A1", "E2", "G2", "A2", "C3", "B2", "A#2", "A2"],
        "Bb1": ["Bb1", "F2", "A2", "Bb2", "D3", "C3", "B2", "Bb2"],
        "Eb2": ["Eb2", "Bb2", "D3", "Eb3", "G2", "F2", "E2", "Eb2"],
    }
    events = []
    for bar in range(1, bars + 1):
        root, _ = prog[(bar - 1) % len(prog)]
        pitches = patterns[root]
        if mode == "pedal":
            pitches = ["D2", "A2"]
            positions, durations = (1, 3), (1.7, 1.7)
        elif mode == "sparse":
            pitches = pitches[::2]
            positions, durations = (1, 2, 3, 4), (.72,) * 4
        else:
            positions, durations = tuple(1 + i * .5 for i in range(8)), (.41,) * 8
        for i, (pitch, beat, dur) in enumerate(zip(pitches, positions, durations)):
            events.append(note(pitch, f"{bar}:{beat:g}", dur, 70 + (10 if i in (0, 4) else 0) + (7 if mode == "drive" else 0)))
    return events


def bell_events(prog: list[tuple[str, list[str]]], bars: int, mode: str) -> list[dict]:
    events = []
    for bar in range(1, bars + 1):
        _, upper = prog[(bar - 1) % len(prog)]
        sequence = upper + upper[-2:0:-1]
        if mode == "sparse":
            sequence = [upper[0], upper[2], upper[-1], upper[1]]
            positions = (1, 2, 3, 4)
        else:
            positions = tuple(1 + i * .5 for i in range(len(sequence)))
        for i, (pitch, beat) in enumerate(zip(sequence, positions)):
            events.append(note(pitch, f"{bar}:{beat:g}", .32 if mode != "sparse" else .62, 54 + (6 if i in (0, 4) else i % 3 * 2) + (8 if mode == "build" else 0)))
    return events


def pad_events(prog: list[tuple[str, list[str]]], bars: int, which: str, velocity: int) -> list[dict]:
    events = []
    for bar in range(1, bars + 1):
        root, upper = prog[(bar - 1) % len(prog)]
        if which == "solar":
            pitches = upper
        else:
            pitches = upper[1:] + (["D5"] if "D4" not in upper else [])
        events.append(chord(pitches, f"{bar}:1.1", 3.62, velocity + bar % 4))
    return events


def chime_events(prog: list[tuple[str, list[str]]], bars: int, mode: str) -> list[dict]:
    events = []
    for bar in range(1, bars + 1):
        _, upper = prog[(bar - 1) % len(prog)]
        top = upper[-1]
        if mode == "motor":
            for i, beat in enumerate((1.25, 2.25, 3.25, 4.25)):
                events.append(note(top, f"{bar}:{beat:g}", .22, 58 + i * 4 + bar % 3))
        elif bar % 2 == 0:
            events += [note(top, f"{bar}:3.5", .34, 64 + bar), note(upper[-2], f"{bar}:4", .34, 59 + bar)]
    return events


def drums(bars: int, mode: str, fills: set[int]) -> list[dict]:
    events = []
    for bar in range(1, bars + 1):
        if mode == "none":
            if bar == bars:
                events += [drum("high_tom", f"{bar}:3.5", 66), drum("mid_tom", f"{bar}:4", 72), drum("low_tom", f"{bar}:4.5", 78)]
            continue
        if mode == "launch" and bar < 5:
            continue
        if mode in ("full", "drive") and bar in (1, 5, 9):
            events.append(drum("crash", f"{bar}:1", 104 if mode == "full" else 110, .25))
        if mode == "half":
            kicks, snares, hats = (1, 3.5), (3,), (1, 2, 3, 4)
        elif mode == "broken":
            kicks, snares, hats = (1, 2.75, 4.25), (2, 4), tuple(1 + i * .5 for i in range(8))
        else:
            kicks = (1, 2, 3, 4) if mode == "full" else (1, 1.5, 2.5, 3, 4.5)
            snares, hats = (2, 4), tuple(1 + i * .5 for i in range(8))
        for beat in kicks:
            events.append(drum("kick", f"{bar}:{beat:g}", 96 + (8 if beat in (1, 3) else 0) + (5 if mode == "drive" else 0)))
        for beat in snares:
            events.append(drum("snare", f"{bar}:{beat:g}", 94 + (6 if mode in ("full", "drive") else 0)))
        for i, beat in enumerate(hats):
            kind = "open_hat" if mode in ("full", "drive") and beat == 4.5 and bar not in fills else "closed_hat"
            events.append(drum(kind, f"{bar}:{beat:g}", 61 + (11 if i % 2 == 0 else 0) + (6 if mode == "drive" else 0), .10))
        if bar in fills:
            events += [drum("snare", f"{bar}:3.5", 82), drum("high_tom", f"{bar}:3.75", 88), drum("mid_tom", f"{bar}:4.25", 95), drum("low_tom", f"{bar}:4.5", 103), drum("snare", f"{bar}:4.75", 108)]
    return events


def main() -> None:
    orbit12 = ORBIT * 2 + TAIL
    apogee12 = ORBIT * 2 + TAIL
    reentry_prog = ORBIT * 2
    composition = {
        "metadata": {"title": "Parallax Bloom", "tempo": 112, "time_signature": "4/4", "key": "D Dorian", "style": "cosmic psychedelic electronic", "version": "v1"},
        "sections": [{"name": name, "bars": bars} for name, bars in SECTIONS],
        "tracks": {
            "lead": {"sections": {
                "launch": clip(8, lead_launch()), "orbital_garden": clip(12, lead_orbit()), "prism_build": clip(8, lead_prism()),
                "zero_gravity": clip(8, lead_zero()), "wormhole": clip(12, lead_worm()), "apogee_bloom": clip(12, lead_apogee()), "reentry": clip(8, lead_reentry()),
            }},
            "acid_bass": {"sections": {
                "launch": clip(8, [note("D2", "5:1", 1.7, 66), note("A2", "5:3", 1.7, 62), note("C2", "7:1", 1.7, 68), note("A1", "7:3", 1.7, 64)]),
                "orbital_garden": clip(12, bass_events(orbit12, 12, "full")), "prism_build": clip(8, bass_events(PRISM, 8, "drive")),
                "zero_gravity": clip(8, bass_events(ZERO, 8, "pedal")), "wormhole": clip(12, bass_events(WORM, 12, "drive")),
                "apogee_bloom": clip(12, bass_events(apogee12, 12, "drive")), "reentry": clip(8, bass_events(reentry_prog, 8, "sparse")),
            }},
            "bell_piano": {"sections": {
                "launch": clip(8, bell_events(ORBIT * 2, 8, "sparse")), "orbital_garden": clip(12, bell_events(orbit12, 12, "flow")),
                "prism_build": clip(8, bell_events(PRISM, 8, "build")), "zero_gravity": clip(8, bell_events(ZERO, 8, "sparse")),
                "wormhole": clip(12, bell_events(WORM, 12, "build")), "apogee_bloom": clip(12, bell_events(apogee12, 12, "flow")),
                "reentry": clip(8, bell_events(reentry_prog, 8, "sparse")),
            }},
            "solar_pad": {"sections": {name: clip(bars, pad_events((ORBIT * 3 if bars == 12 else ORBIT * 2), bars, "solar", 35 if name in ("launch", "zero_gravity", "reentry") else (48 if name == "apogee_bloom" else 42))) for name, bars in SECTIONS}},
            "chime": {"sections": {
                "launch": clip(8, chime_events(ORBIT * 2, 8, "points")), "orbital_garden": clip(12, chime_events(orbit12, 12, "points")),
                "prism_build": clip(8, chime_events(PRISM, 8, "motor")), "zero_gravity": clip(8, chime_events(ZERO, 8, "points")),
                "wormhole": clip(12, chime_events(WORM, 12, "motor")), "apogee_bloom": clip(12, chime_events(apogee12, 12, "points")),
                "reentry": clip(8, chime_events(reentry_prog, 8, "points")),
            }},
            "night_pad": {"sections": {
                "launch": clip(8, pad_events(ORBIT * 2, 8, "night", 31)), "orbital_garden": clip(12, pad_events(orbit12, 12, "night", 34)),
                "prism_build": clip(8, pad_events(PRISM, 8, "night", 38)), "zero_gravity": clip(8, pad_events(ZERO, 8, "night", 47)),
                "wormhole": clip(12, pad_events(WORM, 12, "night", 37)), "apogee_bloom": clip(12, pad_events(apogee12, 12, "night", 44)),
                "reentry": clip(8, pad_events(reentry_prog, 8, "night", 29)),
            }},
            "drums": {"sections": {
                "launch": clip(8, drums(8, "launch", {8})), "orbital_garden": clip(12, drums(12, "full", {8, 12})),
                "prism_build": clip(8, drums(8, "drive", {8})), "zero_gravity": clip(8, drums(8, "none", set())),
                "wormhole": clip(12, drums(12, "broken", {8, 12})), "apogee_bloom": clip(12, drums(12, "drive", {4, 8, 12})),
                "reentry": clip(8, drums(4, "half", {4})),
            }},
        },
    }
    encoded = json.dumps(composition, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "composition_v1.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition.json").write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
