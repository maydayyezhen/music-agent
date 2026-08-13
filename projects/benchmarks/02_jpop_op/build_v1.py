from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def note(pitch: str, at: str, duration: float, velocity: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": at, "duration": duration, "velocity": velocity}


def chord(pitches: list[str], at: str, duration: float, velocity: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": at, "duration": duration, "velocity": velocity}


def drum(name: str, at: str, duration: float, velocity: int) -> dict:
    return {"type": "drum", "note": name, "at": at, "duration": duration, "velocity": velocity}


def clip(loop_bars: int, events: list[dict]) -> dict:
    return {"loop_bars": loop_bars, "events": events}


def piano_intro() -> list[dict]:
    events: list[dict] = []
    voicings = [
        ("D3", ["A3", "D4", "E4", "F#4"]),
        ("C#3", ["A3", "C#4", "E4", "F#4"]),
        ("B2", ["A3", "B3", "D4", "F#4"]),
        ("G2", ["A3", "B3", "D4", "G4"]),
    ]
    for bar, (low, upper) in enumerate(voicings, 1):
        events.append(note(low, f"{bar}:1", 1.7, 73 + bar))
        events.append(chord(upper, f"{bar}:1.04", 1.55, 72 + bar))
        for beat, pitch in zip((2.5, 3, 3.5, 4), upper):
            events.append(note(pitch, f"{bar}:{beat}", 0.38, 68 + bar))
    events += [
        note("A4", "1:3", 0.42, 88), note("B4", "1:3.5", 0.42, 91),
        note("D5", "1:4", 0.9, 96), note("F#5", "2:2", 0.46, 92),
        note("E5", "2:2.5", 0.46, 88), note("D5", "2:3", 0.9, 91),
        note("A4", "3:3", 0.42, 86), note("B4", "3:3.5", 0.42, 89),
        note("D5", "3:4", 0.9, 95), note("E5", "4:2", 0.42, 92),
        note("D5", "4:2.5", 0.42, 89), note("B4", "4:3", 0.7, 86),
    ]
    return events


def piano_verse() -> list[dict]:
    return [
        chord(["F#3", "A3", "D4", "E4"], "1:1.03", 0.72, 68),
        chord(["A3", "D4", "F#4"], "1:3.02", 0.62, 65),
        note("A4", "1:3.5", 0.38, 78), note("B4", "1:4", 0.38, 81),
        chord(["E3", "A3", "C#4"], "2:1.02", 0.72, 67),
        chord(["A3", "C#4", "E4"], "2:3.03", 0.62, 65),
        note("E4", "2:3.5", 0.38, 76), note("F#4", "2:4", 0.38, 79),
        chord(["F#3", "A3", "B3", "D4"], "3:1.02", 0.72, 69),
        chord(["A3", "B3", "D4", "F#4"], "3:3.02", 0.62, 66),
        note("D5", "3:3.5", 0.38, 82), note("B4", "3:4", 0.7, 79),
        chord(["G3", "A3", "B3", "D4"], "4:1.03", 0.72, 70),
        chord(["A3", "B3", "D4", "G4"], "4:3.01", 0.62, 67),
        note("A4", "4:3.5", 0.38, 78), note("F#4", "4:4", 0.7, 76),
    ]


def piano_pre() -> list[dict]:
    events: list[dict] = []
    patterns = [
        ["E3", "B3", "D4", "F#4", "G4", "F#4", "B4", "D5"],
        ["F#3", "C#4", "E4", "A4", "C#5", "A4", "C#5", "E5"],
        ["G3", "D4", "F#4", "A4", "B4", "A4", "D5", "F#5"],
        ["A3", "E4", "G4", "B4", "D5", "C#5", "E5", "A5"],
    ]
    for block in range(2):
        for offset, pitches in enumerate(patterns, 1):
            bar = block * 4 + offset
            for step, pitch in enumerate(pitches):
                beat = 1 + step * 0.5
                velocity = 72 + block * 6 + step % 2 * 4 + offset
                events.append(note(pitch, f"{bar}:{beat:g}", 0.42, velocity))
    return events


def piano_chorus() -> list[dict]:
    events: list[dict] = []
    punches = {
        1: ["D3", "A3", "D4", "F#4"], 2: ["C#3", "A3", "C#4", "E4"],
        3: ["B2", "F#3", "A3", "D4"], 4: ["G2", "D3", "A3", "B3"],
        5: ["F#2", "A3", "D4", "F#4"], 6: ["G2", "D3", "B3", "D4"],
        7: ["E3", "B3", "D4", "G4"], 8: ["A2", "E3", "G3", "C#4"],
    }
    for bar, pitches in punches.items():
        events.append(chord(pitches, f"{bar}:1", 1.35, 82 if bar not in (1, 5) else 88))
        events.append(chord(pitches[1:], f"{bar}:3.02", 0.72, 76))
    hook = [
        (1, 1, "A4", .42, 96), (1, 1.5, "B4", .42, 99), (1, 2, "D5", .44, 104),
        (1, 2.5, "E5", .44, 106), (1, 3, "F#5", 1.35, 112),
        (2, 1, "E5", .44, 102), (2, 1.5, "D5", .44, 100), (2, 2, "B4", .88, 96),
        (2, 3, "A4", .42, 92), (2, 3.5, "B4", .42, 95), (2, 4, "D5", .82, 102),
        (3, 1, "F#5", .44, 108), (3, 1.5, "E5", .44, 103), (3, 2, "D5", .88, 100),
        (3, 3, "B4", .44, 96), (3, 3.5, "D5", .44, 100), (3, 4, "E5", .82, 104),
        (4, 1, "D5", .44, 101), (4, 1.5, "B4", .44, 96), (4, 2, "A4", 1.35, 94),
        (5, 1, "A4", .42, 98), (5, 1.5, "B4", .42, 101), (5, 2, "D5", .44, 106),
        (5, 2.5, "E5", .44, 108), (5, 3, "F#5", 1.35, 114),
        (6, 1, "G5", .44, 111), (6, 1.5, "F#5", .44, 107), (6, 2, "E5", .88, 103),
        (6, 3, "D5", .42, 100), (6, 3.5, "E5", .42, 103), (6, 4, "F#5", .82, 108),
        (7, 1, "E5", .44, 104), (7, 1.5, "D5", .44, 101), (7, 2, "B4", .88, 97),
        (7, 3, "A4", .42, 94), (7, 3.5, "B4", .42, 98), (7, 4, "D5", .82, 103),
        (8, 1, "C#5", .44, 103), (8, 1.5, "B4", .44, 99), (8, 2, "A4", 1.7, 96),
    ]
    events.extend(note(p, f"{b}:{beat:g}", dur, vel) for b, beat, p, dur, vel in hook)
    return events


def piano_outro() -> list[dict]:
    events = piano_chorus()
    # Only the first 8 bars reuse the chorus material; bars 9–12 are a distinct cadence.
    events += [
        chord(["B2", "F#3", "A3", "D4"], "9:1", 2.8, 72),
        note("F#4", "9:1.5", .42, 82), note("E4", "9:2", .42, 79), note("D4", "9:2.5", .85, 77),
        chord(["G2", "D3", "A3", "B3"], "10:1", 2.8, 69),
        note("B4", "10:2", .42, 82), note("A4", "10:2.5", .42, 79), note("F#4", "10:3", .85, 76),
        chord(["E3", "B3", "D4", "G4"], "11:1", 1.7, 66),
        chord(["A2", "E3", "G3", "C#4"], "11:3", 1.7, 68),
        note("E4", "11:3.5", .4, 78), note("F#4", "11:4", .4, 81),
        chord(["D2", "A2", "F#3", "A3", "D4", "E4"], "12:1", 3.65, 74),
        note("A4", "12:2", .42, 80), note("D5", "12:2.5", .42, 86), note("F#5", "12:3", 1.2, 88),
    ]
    return events


def bass_pattern(roots: list[str], bars: int, intensity: int = 0) -> list[dict]:
    # Each bar explicitly points into the next harmony using scale and chromatic approaches.
    templates = {
        "D2": ["D2", "A2", "C#3", "D3", "F#2", "A2", "B2", "C#3"],
        "C#2": ["C#2", "E2", "A2", "C#3", "E3", "C#3", "B2", "A#2"],
        "B1": ["B1", "F#2", "A2", "B2", "D3", "C#3", "B2", "A2"],
        "G1": ["G1", "D2", "F#2", "G2", "B2", "A2", "G2", "G#2"],
        "E2": ["E2", "B2", "D3", "E3", "G2", "A2", "A#2", "B2"],
        "F#2": ["F#2", "C#3", "E3", "F#3", "A2", "B2", "C3", "C#3"],
        "A1": ["A1", "E2", "G2", "A2", "C#3", "B2", "A2", "C#2"],
    }
    events: list[dict] = []
    for bar in range(1, bars + 1):
        pitches = templates[roots[(bar - 1) % len(roots)]]
        for step, pitch in enumerate(pitches):
            vel = 78 + intensity + (7 if step in (0, 4) else 0) + (2 if step % 2 else 0)
            events.append(note(pitch, f"{bar}:{1 + step * .5:g}", .43, min(112, vel)))
    return events


def guitar_muted() -> list[dict]:
    events: list[dict] = []
    shapes = [["D3", "A3"], ["A2", "E3"], ["B2", "F#3"], ["G2", "D3"]]
    for bar, pitches in enumerate(shapes, 1):
        for beat in (1.5, 2.5, 3.5, 4):
            events.append(chord(pitches, f"{bar}:{beat:g}", .24, 72 + (5 if beat in (1.5, 3.5) else 0)))
    return events


def guitar_chorus() -> list[dict]:
    roots = [["D3", "A3"], ["A2", "E3"], ["B2", "F#3"], ["G2", "D3"],
             ["F#2", "C#3"], ["G2", "D3"], ["E3", "B3"], ["A2", "E3"]]
    events: list[dict] = []
    for bar, shape in enumerate(roots, 1):
        for step in range(8):
            events.append(chord(shape, f"{bar}:{1 + step * .5:g}", .34, 78 + (8 if step in (0, 4) else step % 2 * 3)))
    # High octave answers occupy hook rests, never copy the piano line.
    events += [
        chord(["A4", "A5"], "2:2.75", .38, 88), chord(["B4", "B5"], "2:3.25", .38, 91),
        chord(["D5", "D6"], "4:3.25", .6, 94), chord(["B4", "B5"], "6:2.75", .38, 90),
        chord(["D5", "D6"], "6:3.25", .38, 93), chord(["E5", "E6"], "8:3.2", .62, 96),
    ]
    return events


def strings_pre() -> list[dict]:
    events: list[dict] = []
    chords = [
        ["B3", "D4", "G4"], ["C#4", "E4", "A4"], ["D4", "F#4", "B4"], ["E4", "G4", "D5"],
        ["D4", "G4", "B4"], ["E4", "A4", "C#5"], ["F#4", "B4", "D5"], ["G4", "C#5", "E5"],
    ]
    top = ["G4", "A4", "B4", "D5", "B4", "C#5", "D5", "E5"]
    for bar in range(1, 9):
        events.append(chord(chords[bar - 1], f"{bar}:1.05", 3.7, 55 + bar * 3))
        events.append(note(top[bar - 1], f"{bar}:3", 1.7, 66 + bar * 3))
    return events


def strings_chorus() -> list[dict]:
    sustained = [
        ["A3", "D4", "F#4"], ["A3", "C#4", "E4"], ["A3", "B3", "D4"], ["B3", "D4", "G4"],
        ["A3", "D4", "F#4"], ["B3", "D4", "G4"], ["B3", "D4", "G4"], ["A3", "C#4", "E4"],
    ]
    counter = ["F#5", "E5", "D5", "B4", "A4", "B4", "D5", "C#5"]
    events: list[dict] = []
    for bar in range(1, 9):
        events.append(chord(sustained[bar - 1], f"{bar}:1.06", 3.72, 70 + (4 if bar in (1, 5) else 0)))
        events.append(note(counter[bar - 1], f"{bar}:2.03", 1.65, 77 + bar % 3 * 3))
    return events


def pad_events(roots: list[list[str]], bars: int, velocity: int) -> list[dict]:
    return [chord(roots[(bar - 1) % len(roots)], f"{bar}:1.08", 3.72, velocity) for bar in range(1, bars + 1)]


def drum_bar(bar: int, mode: str, fill: bool = False) -> list[dict]:
    events: list[dict] = []
    if mode == "chorus":
        events.append(drum("crash", f"{bar}:1", .2, 112 if bar == 1 else 104))
        kicks = (1, 1.5, 2.5, 3, 3.5, 4.5)
        hats = [1 + step * .5 for step in range(8)]
    elif mode == "pre":
        kicks = (1, 2.5, 3, 4.5)
        hats = [1 + step * .5 for step in range(8)]
    elif mode == "intro":
        kicks = (1, 3, 4.5)
        hats = [1, 2, 3, 4]
    else:
        kicks = (1, 2.5, 3.5, 4.5)
        hats = [1 + step * .5 for step in range(8)]
    for beat in kicks:
        events.append(drum("kick", f"{bar}:{beat:g}", .16, 100 if beat in (1, 3) else 88))
    for beat in (2, 4):
        events.append(drum("snare", f"{bar}:{beat:g}", .18, 101 if mode != "intro" else 94))
    for index, beat in enumerate(hats):
        hat = "open_hat" if mode in ("pre", "chorus") and beat == 4.5 and not fill else "closed_hat"
        events.append(drum(hat, f"{bar}:{beat:g}", .11, 70 + (10 if index % 2 == 0 else 0) + (5 if mode == "chorus" else 0)))
    if fill:
        events += [
            drum("snare", f"{bar}:3.5", .12, 82), drum("high_tom", f"{bar}:3.75", .14, 88),
            drum("mid_tom", f"{bar}:4.25", .14, 94), drum("low_tom", f"{bar}:4.5", .16, 101),
            drum("snare", f"{bar}:4.75", .12, 106),
        ]
    return events


def drums_for(bars: int, mode: str, fills: set[int]) -> list[dict]:
    events: list[dict] = []
    for bar in range(1, bars + 1):
        events.extend(drum_bar(bar, mode, bar in fills))
    return events


def main() -> None:
    pad_prog = [
        ["D4", "A4", "E5", "F#5"], ["C#4", "A4", "E5", "F#5"],
        ["B3", "F#4", "A4", "D5"], ["G3", "D4", "A4", "B4"],
    ]
    pre_pad = [
        ["E4", "B4", "D5", "F#5"], ["F#4", "C#5", "E5", "A5"],
        ["G4", "D5", "F#5", "B5"], ["A4", "E5", "G5", "D6"],
    ]
    composition = {
        "metadata": {
            "title": "Hikari no Compass", "tempo": 148, "time_signature": "4/4", "key": "D major",
            "style": "2000s J-Pop / Anime OP / Galgame OP", "version": "v1"
        },
        "sections": [
            {"name": "intro", "bars": 4}, {"name": "verse", "bars": 8},
            {"name": "pre_chorus", "bars": 8}, {"name": "chorus", "bars": 16},
            {"name": "outro", "bars": 12},
        ],
        "tracks": {
            "piano": {"sections": {
                "intro": clip(4, piano_intro()), "verse": clip(4, piano_verse()),
                "pre_chorus": clip(8, piano_pre()), "chorus": clip(8, piano_chorus()),
                "outro": clip(12, piano_outro()),
            }},
            "bass": {"sections": {
                "intro": clip(4, bass_pattern(["D2", "C#2", "B1", "G1"], 4, -8)),
                "verse": clip(4, bass_pattern(["D2", "C#2", "B1", "G1"], 4, 0)),
                "pre_chorus": clip(4, bass_pattern(["E2", "F#2", "G1", "A1"], 4, 5)),
                "chorus": clip(8, bass_pattern(["D2", "C#2", "B1", "G1", "F#2", "G1", "E2", "A1"], 8, 9)),
                "outro": clip(12, bass_pattern(["D2", "C#2", "B1", "G1", "F#2", "G1", "E2", "A1", "B1", "G1", "E2", "D2"], 12, 2)),
            }},
            "guitar": {"sections": {
                "intro": clip(4, [chord(["D4", "A4"], "2:3", .46, 82), chord(["E4", "B4"], "2:3.5", .46, 85),
                                  chord(["F#4", "C#5"], "4:3", .46, 88), chord(["A4", "E5"], "4:3.5", .7, 92)]),
                "verse": clip(4, guitar_muted()),
                "pre_chorus": clip(4, [
                    chord(["E3", "B3"], "1:1.04", 2.6, 76), chord(["E3", "B3"], "1:4", .5, 82),
                    chord(["F#3", "C#4"], "2:1.03", 2.6, 80), chord(["F#3", "C#4"], "2:4", .5, 85),
                    chord(["G3", "D4"], "3:1.02", 2.6, 84), chord(["G3", "D4"], "3:4", .5, 89),
                    chord(["A3", "E4"], "4:1.01", 2.6, 88), chord(["A3", "E4"], "4:4", .72, 95),
                ]),
                "chorus": clip(8, guitar_chorus()),
                "outro": clip(12, guitar_chorus()),
            }},
            "strings": {"sections": {
                "pre_chorus": clip(8, strings_pre()), "chorus": clip(8, strings_chorus()),
                "outro": clip(12, strings_chorus() + [
                    chord(["B3", "D4", "F#4"], "9:1.06", 3.7, 62),
                    chord(["B3", "D4", "G4"], "10:1.06", 3.7, 60),
                    chord(["B3", "D4", "G4"], "11:1.06", 1.7, 57),
                    chord(["A3", "C#4", "E4"], "11:3.06", 1.7, 59),
                    chord(["A3", "D4", "F#4"], "12:1.06", 3.72, 64),
                ]),
            }},
            "pad": {"sections": {
                "intro": clip(4, pad_events(pad_prog, 4, 42)),
                "verse": clip(4, [chord(pad_prog[2], "3:1.1", 3.6, 38), chord(pad_prog[3], "4:1.1", 3.6, 40)]),
                "pre_chorus": clip(4, pad_events(pre_pad, 4, 48)),
                "chorus": clip(8, pad_events(pad_prog + [pad_prog[0], pad_prog[3], pre_pad[0], pre_pad[3]], 8, 53)),
                "outro": clip(12, pad_events(pad_prog + [pad_prog[0], pad_prog[3], pre_pad[0], pre_pad[3], pad_prog[2], pad_prog[3], pre_pad[0], pad_prog[0]], 12, 43)),
            }},
            "drums": {"sections": {
                "intro": clip(4, drums_for(4, "intro", {4})),
                "verse": clip(4, drums_for(4, "verse", {4})),
                "pre_chorus": clip(8, drums_for(8, "pre", {4, 8})),
                "chorus": clip(8, drums_for(8, "chorus", {8})),
                "outro": clip(12, drums_for(8, "chorus", {8})),
            }},
        },
    }
    encoded = json.dumps(composition, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "composition_v1.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition.json").write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
