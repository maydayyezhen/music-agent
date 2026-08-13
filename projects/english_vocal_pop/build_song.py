from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SECTIONS = [
    ("intro", 4), ("verse_1", 8), ("pre_1", 4), ("chorus_1", 8),
    ("verse_2", 8), ("pre_2", 4), ("chorus_2", 8), ("bridge", 8),
    ("final_chorus", 12), ("outro", 4),
]


def note(pitch: str, at: str, duration: float, velocity: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": at, "duration": duration, "velocity": velocity}


def chord(pitches: list[str], at: str, duration: float, velocity: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": at, "duration": duration, "velocity": velocity}


def drum(name: str, at: str, velocity: int, duration: float = 0.14) -> dict:
    return {"type": "drum", "note": name, "at": at, "duration": duration, "velocity": velocity}


def clip(bars: int, events: list[dict]) -> dict:
    return {"loop_bars": bars, "events": events}


VERSE = [
    ("E2", ["G3", "B3", "D4", "F#4"]),
    ("C2", ["G3", "C4", "D4", "E4"]),
    ("G2", ["G3", "B3", "D4", "A4"]),
    ("F#2", ["A3", "D4", "F#4", "A4"]),
]
PRE = [
    ("A2", ["G3", "A3", "C4", "E4"]),
    ("B2", ["A3", "B3", "D4", "F#4"]),
    ("C3", ["G3", "C4", "D4", "E4"]),
    ("D3", ["A3", "D4", "E4", "G4"]),
]
CHORUS = [
    ("G2", ["G3", "B3", "D4", "A4"]),
    ("F#2", ["A3", "D4", "F#4", "A4"]),
    ("E2", ["G3", "B3", "D4", "F#4"]),
    ("C2", ["G3", "C4", "D4", "E4"]),
    ("B1", ["G3", "B3", "D4", "G4"]),
    ("C2", ["G3", "C4", "E4", "G4"]),
    ("D2", ["A3", "D4", "E4", "G4"]),
    ("D2", ["A3", "C4", "D4", "F#4"]),
]
BRIDGE = [
    ("E2", ["G3", "B3", "E4"]), ("D2", ["A3", "D4", "F#4"]),
    ("C2", ["G3", "C4", "E4"]), ("B1", ["G3", "B3", "D4"]),
    ("A1", ["G3", "A3", "C4", "E4"]), ("B1", ["G3", "B3", "D4", "G4"]),
    ("C2", ["G3", "C4", "D4", "E4"]), ("D2", ["A3", "D4", "F#4"]),
]
TAG = [
    ("C2", ["G3", "C4", "E4", "G4"]), ("D2", ["A3", "D4", "F#4", "A4"]),
    ("E2", ["G3", "B3", "D4", "F#4"]), ("D2", ["G3", "B3", "D4", "G4"]),
]


def piano_section(prog: list[tuple[str, list[str]]], bars: int, mode: str) -> list[dict]:
    events: list[dict] = []
    for bar in range(1, bars + 1):
        low, upper = prog[(bar - 1) % len(prog)]
        if mode == "verse":
            events += [note(low, f"{bar}:1", 1.2, 62 + bar % 3), chord(upper, f"{bar}:1.04", .82, 66),
                       chord(upper[1:], f"{bar}:3.03", .65, 62)]
            if bar % 2 == 0:
                events.append(note(upper[-1], f"{bar}:4.5", .32, 69))
        elif mode == "pre":
            arp = [low, upper[0], upper[1], upper[2], upper[-1], upper[2], upper[1], upper[-1]]
            for step, pitch in enumerate(arp):
                events.append(note(pitch, f"{bar}:{1 + step * .5:g}", .40, 66 + bar * 2 + step % 2 * 3))
        elif mode == "chorus":
            events += [note(low, f"{bar}:1", 1.55, 74), chord(upper, f"{bar}:1.03", 1.35, 76),
                       chord(upper[1:], f"{bar}:3.03", .74, 71), chord(upper, f"{bar}:4.03", .55, 73)]
        elif mode == "bridge":
            events += [note(low, f"{bar}:1", 2.8 if bar <= 4 else 1.7, 58 + bar * 2),
                       chord(upper, f"{bar}:1.05", 2.65 if bar <= 4 else 1.55, 61 + bar * 2)]
            if bar > 4:
                events.append(chord(upper[1:], f"{bar}:3.02", .78, 68 + bar))
    return events


def intro_piano() -> list[dict]:
    events: list[dict] = []
    pitches = ["G3", "D4", "A4", "B4", "D4", "G4", "B4", "D5"]
    for bar in range(1, 5):
        shape = pitches if bar in (1, 4) else (["E3", "B3", "D4", "G4", "C4", "E4", "G4", "A4"] if bar == 2 else ["C3", "G3", "D4", "E4", "G3", "C4", "D4", "G4"])
        for step, pitch in enumerate(shape):
            events.append(note(pitch, f"{bar}:{1 + step * .5:g}", .39, 58 + (8 if step in (0, 4) else step % 2 * 3)))
    events += [note("D4", "3:3", .4, 76), note("E4", "3:3.5", .4, 79), note("G4", "3:4", .4, 83),
               note("B4", "3:4.5", .42, 87), note("D5", "4:1", 1.45, 90)]
    return events


def outro_piano() -> list[dict]:
    return [
        chord(["G2", "D3", "B3", "D4", "A4"], "1:1", 2.7, 67),
        note("D5", "1:3", .45, 79), note("B4", "1:3.5", .45, 76), note("G4", "1:4", 1.1, 74),
        chord(["E3", "B3", "D4", "G4"], "2:1", 2.7, 61),
        chord(["C3", "G3", "D4", "E4"], "3:1", 2.7, 59),
        chord(["G2", "D3", "A3", "B3", "G4"], "4:1", 3.7, 64),
    ]


def bass_section(roots: list[str], bars: int, mode: str) -> list[dict]:
    patterns = {
        "E2": ["E2", "B2", "D3", "B2", "G2", "B2", "D3", "D#3"],
        "C2": ["C2", "G2", "B2", "G2", "E2", "G2", "A2", "B2"],
        "G2": ["G2", "D3", "B2", "D3", "G2", "A2", "B2", "F#2"],
        "F#2": ["F#2", "A2", "D3", "A2", "F#2", "E2", "F2", "F#2"],
        "A2": ["A2", "E3", "G3", "E3", "C3", "B2", "A#2", "B2"],
        "B2": ["B2", "F#3", "A3", "F#3", "D3", "C#3", "C3", "B2"],
        "C3": ["C3", "G3", "E3", "G3", "C3", "B2", "C3", "C#3"],
        "D3": ["D3", "A3", "C4", "A3", "F#3", "E3", "D3", "D2"],
        "B1": ["B1", "F#2", "D3", "F#2", "G2", "F#2", "E2", "D2"],
        "A1": ["A1", "E2", "G2", "E2", "C2", "B1", "A#1", "B1"],
        "D2": ["D2", "A2", "C3", "A2", "F#2", "E2", "F2", "F#2"],
    }
    events: list[dict] = []
    for bar in range(1, bars + 1):
        pattern = patterns[roots[(bar - 1) % len(roots)]]
        if mode == "bridge" and bar <= 4:
            pattern = pattern[::2]
            spacing = 1.0
            duration = .78
        else:
            spacing = .5
            duration = .42
        for step, pitch in enumerate(pattern):
            events.append(note(pitch, f"{bar}:{1 + step * spacing:g}", duration,
                               73 + (8 if step in (0, 4) else 0) + (5 if mode == "chorus" else 0)))
    return events


def guitar_section(roots: list[str], bars: int, mode: str) -> list[dict]:
    fifths = {"E2": ["E3", "B3"], "C2": ["C3", "G3"], "G2": ["G2", "D3"], "F#2": ["F#2", "C#3"],
              "A2": ["A2", "E3"], "B2": ["B2", "F#3"], "C3": ["C3", "G3"], "D3": ["D3", "A3"],
              "B1": ["B2", "F#3"], "A1": ["A2", "E3"], "D2": ["D3", "A3"]}
    events: list[dict] = []
    for bar in range(1, bars + 1):
        shape = fifths[roots[(bar - 1) % len(roots)]]
        if mode == "verse":
            for beat in (1.5, 2.5, 3.5, 4.5):
                events.append(chord(shape, f"{bar}:{beat:g}", .25, 68 + (6 if beat in (1.5, 3.5) else 0)))
        elif mode == "pre":
            events += [chord(shape, f"{bar}:1.05", 2.5, 72 + bar * 3), chord(shape, f"{bar}:4", .65, 78 + bar * 3)]
        elif mode == "chorus":
            for step in range(8):
                events.append(chord(shape, f"{bar}:{1 + step * .5:g}", .32, 74 + (9 if step in (0, 4) else step % 2 * 3)))
        elif mode == "bridge" and bar > 4:
            events += [chord(shape, f"{bar}:1", 1.3, 70 + bar * 2), chord(shape, f"{bar}:3", 1.3, 73 + bar * 2)]
    return events


def string_section(prog: list[tuple[str, list[str]]], bars: int, mode: str) -> list[dict]:
    events: list[dict] = []
    top_pre = ["A4", "B4", "C5", "D5"]
    top_chorus = ["B4", "A4", "G4", "E4", "D5", "E5", "D5", "A4"]
    for bar in range(1, bars + 1):
        _, upper = prog[(bar - 1) % len(prog)]
        support = upper[1:]
        if mode == "pre":
            target = top_pre[(bar - 1) % 4]
            support = [p for p in support if p != target]
            events += [chord(support, f"{bar}:1.08", 3.68, 53 + bar * 5), note(target, f"{bar}:3", 1.65, 66 + bar * 4)]
        elif mode == "chorus":
            target = top_chorus[(bar - 1) % 8]
            support = [p for p in support if p != target]
            events += [chord(support, f"{bar}:1.08", 3.68, 65 + (5 if bar in (1, 5, 9) else 0)),
                       note(target, f"{bar}:3.05", .72, 72 + bar % 4 * 3)]
        elif mode == "bridge":
            events.append(note(["B3", "A3", "G3", "D4", "E4", "G4", "A4", "B4"][bar - 1], f"{bar}:1.08", 3.6, 50 + bar * 4))
    return events


def pad_section(prog: list[tuple[str, list[str]]], bars: int, velocity: int) -> list[dict]:
    return [chord(prog[(bar - 1) % len(prog)][1], f"{bar}:1.1", 3.65, velocity + bar % 3) for bar in range(1, bars + 1)]


def drum_section(bars: int, mode: str, fills: set[int]) -> list[dict]:
    events: list[dict] = []
    for bar in range(1, bars + 1):
        if mode in ("chorus", "final") and bar in (1, 9):
            events.append(drum("crash", f"{bar}:1", 108 if bar == 1 else 102, .25))
        if mode == "bridge" and bar <= 4:
            kicks = (1, 3)
            hats = (1, 2, 3, 4)
            snare_beats = (3,)
        elif mode == "intro":
            kicks = () if bar < 3 else (1, 3)
            hats = () if bar < 3 else (1, 2, 3, 4)
            snare_beats = () if bar < 3 else (2, 4)
        elif mode == "verse":
            kicks = (1, 2.5, 3.5, 4.5)
            hats = tuple(1 + x * .5 for x in range(8))
            snare_beats = (2, 4)
        elif mode == "pre":
            kicks = (1, 2.5, 3, 4.5)
            hats = tuple(1 + x * .5 for x in range(8))
            snare_beats = (2, 4)
        else:
            kicks = (1, 1.5, 2.5, 3, 3.5, 4.5)
            hats = tuple(1 + x * .5 for x in range(8))
            snare_beats = (2, 4)
        for beat in kicks:
            events.append(drum("kick", f"{bar}:{beat:g}", 96 + (7 if beat in (1, 3) else 0)))
        for beat in snare_beats:
            events.append(drum("snare", f"{bar}:{beat:g}", 98 if mode != "intro" else 88))
        for i, beat in enumerate(hats):
            hat = "open_hat" if mode in ("pre", "chorus", "final") and beat == 4.5 and bar not in fills else "closed_hat"
            events.append(drum(hat, f"{bar}:{beat:g}", 66 + (10 if i % 2 == 0 else 0) + (6 if mode in ("chorus", "final") else 0), .10))
        if bar in fills:
            events += [drum("snare", f"{bar}:3.5", 82), drum("high_tom", f"{bar}:3.75", 88),
                       drum("mid_tom", f"{bar}:4.25", 94), drum("low_tom", f"{bar}:4.5", 101),
                       drum("snare", f"{bar}:4.75", 106)]
    return events


def build_composition() -> dict:
    chorus12 = CHORUS + TAG
    return {
        "metadata": {"title": "Different Windows", "tempo": 108, "time_signature": "4/4", "key": "G major", "style": "English vocal pop", "version": "v1"},
        "sections": [{"name": name, "bars": bars} for name, bars in SECTIONS],
        "tracks": {
            "piano": {"sections": {
                "intro": clip(4, intro_piano()), "verse_1": clip(8, piano_section(VERSE, 8, "verse")),
                "pre_1": clip(4, piano_section(PRE, 4, "pre")), "chorus_1": clip(8, piano_section(CHORUS, 8, "chorus")),
                "verse_2": clip(8, piano_section(VERSE, 8, "verse")), "pre_2": clip(4, piano_section(PRE, 4, "pre")),
                "chorus_2": clip(8, piano_section(CHORUS, 8, "chorus")), "bridge": clip(8, piano_section(BRIDGE, 8, "bridge")),
                "final_chorus": clip(12, piano_section(chorus12, 12, "chorus")), "outro": clip(4, outro_piano()),
            }},
            "bass": {"sections": {
                "intro": clip(4, [note("G2", "3:1", 1.7, 67), note("D3", "3:3", 1.7, 64), note("E2", "4:1", 1.7, 69), note("F#2", "4:3", 1.6, 72)]),
                "verse_1": clip(8, bass_section([x[0] for x in VERSE], 8, "verse")), "pre_1": clip(4, bass_section([x[0] for x in PRE], 4, "pre")),
                "chorus_1": clip(8, bass_section([x[0] for x in CHORUS], 8, "chorus")), "verse_2": clip(8, bass_section([x[0] for x in VERSE], 8, "verse")),
                "pre_2": clip(4, bass_section([x[0] for x in PRE], 4, "pre")), "chorus_2": clip(8, bass_section([x[0] for x in CHORUS], 8, "chorus")),
                "bridge": clip(8, bass_section([x[0] for x in BRIDGE], 8, "bridge")), "final_chorus": clip(12, bass_section([x[0] for x in chorus12], 12, "chorus")),
                "outro": clip(4, [note("E2", "1:1", 1.7, 68), note("C2", "2:1", 1.7, 64), note("G2", "3:1", 1.8, 66), note("G2", "4:1", 3.6, 61)]),
            }},
            "guitar": {"sections": {
                "intro": clip(4, [chord(["G3", "D4"], "3:3", .5, 66), chord(["B3", "F#4"], "4:3", .7, 72)]),
                "verse_1": clip(8, guitar_section([x[0] for x in VERSE], 8, "verse")), "pre_1": clip(4, guitar_section([x[0] for x in PRE], 4, "pre")),
                "chorus_1": clip(8, guitar_section([x[0] for x in CHORUS], 8, "chorus")), "verse_2": clip(8, guitar_section([x[0] for x in VERSE], 8, "verse")),
                "pre_2": clip(4, guitar_section([x[0] for x in PRE], 4, "pre")), "chorus_2": clip(8, guitar_section([x[0] for x in CHORUS], 8, "chorus")),
                "bridge": clip(8, guitar_section([x[0] for x in BRIDGE], 8, "bridge")), "final_chorus": clip(12, guitar_section([x[0] for x in chorus12], 12, "chorus")),
                "outro": clip(4, [chord(["G3", "D4"], "1:1", 2.8, 67)]),
            }},
            "strings": {"sections": {
                "pre_1": clip(4, string_section(PRE, 4, "pre")), "chorus_1": clip(8, string_section(CHORUS, 8, "chorus")),
                "pre_2": clip(4, string_section(PRE, 4, "pre")), "chorus_2": clip(8, string_section(CHORUS, 8, "chorus")),
                "bridge": clip(8, string_section(BRIDGE, 8, "bridge")), "final_chorus": clip(12, string_section(chorus12, 12, "chorus")),
                "outro": clip(4, [chord(["B3", "D4", "G4"], "1:1.1", 3.6, 57), note("G4", "2:1.1", 3.5, 53), note("E4", "3:1.1", 3.5, 50), note("D4", "4:1.1", 3.5, 47)]),
            }},
            "pad": {"sections": {
                "intro": clip(4, pad_section([CHORUS[0], VERSE[0], VERSE[1], CHORUS[0]], 4, 40)),
                "verse_1": clip(8, pad_section(VERSE, 8, 35)), "pre_1": clip(4, pad_section(PRE, 4, 43)),
                "chorus_1": clip(8, pad_section(CHORUS, 8, 48)), "verse_2": clip(8, pad_section(VERSE, 8, 37)),
                "pre_2": clip(4, pad_section(PRE, 4, 45)), "chorus_2": clip(8, pad_section(CHORUS, 8, 50)),
                "bridge": clip(8, pad_section(BRIDGE, 8, 42)), "final_chorus": clip(12, pad_section(chorus12, 12, 53)),
                "outro": clip(4, pad_section([VERSE[0], VERSE[1], CHORUS[0], CHORUS[0]], 4, 38)),
            }},
            "drums": {"sections": {
                "intro": clip(4, drum_section(4, "intro", {4})), "verse_1": clip(8, drum_section(8, "verse", {8})),
                "pre_1": clip(4, drum_section(4, "pre", {4})), "chorus_1": clip(8, drum_section(8, "chorus", {8})),
                "verse_2": clip(8, drum_section(8, "verse", {8})), "pre_2": clip(4, drum_section(4, "pre", {4})),
                "chorus_2": clip(8, drum_section(8, "chorus", {8})), "bridge": clip(8, drum_section(8, "bridge", {8})),
                "final_chorus": clip(12, drum_section(12, "final", {8, 12})),
                "outro": clip(4, [drum("crash", "1:1", 88, .3), drum("kick", "1:1", 82), drum("snare", "1:3", 76)]),
            }},
        },
    }


def phrase(pid: str, section: str, text: str, tokens: list[str], pitches: list[str], durations: list[float], start: float) -> dict:
    assert len(tokens) == len(pitches) == len(durations), (pid, len(tokens), len(pitches), len(durations))
    notes = []
    cursor = start
    for index, (token, pitch, duration) in enumerate(zip(tokens, pitches, durations)):
        notes.append({
            "lyric_token": token, "pitch": pitch, "duration": duration,
            "start_beat": round(cursor, 3), "phrase_start": index == 0, "phrase_end": index == len(tokens) - 1,
        })
        cursor += duration
    return {
        "phrase_id": pid, "section": section, "text": text, "start_beat": start,
        "end_beat": round(cursor, 3), "boundary_before": "phrase_start", "boundary_after": "phrase_end",
        "breath_after_beats": round(max(0.0, 8 - (cursor - start)), 3), "notes": notes,
    }


def default_durations(n: int, last: float = 1.5) -> list[float]:
    durations = [.5] * n
    if n >= 2:
        durations[-2] = 1.0
    durations[-1] = last
    return durations


def fit(pattern: list[str], n: int) -> list[str]:
    return [pattern[i % len(pattern)] for i in range(n)]


def build_vocal_score() -> dict:
    phrases: list[dict] = []
    verse_pitch_a = ["B3", "D4", "E4", "G4", "F#4", "E4", "D4", "B3", "D4"]
    verse_pitch_b = ["B3", "D4", "E4", "G4", "A4", "G4", "E4", "D4", "B3"]
    pre_pitch = ["E4", "F#4", "G4", "A4", "B4", "A4", "B4", "D5"]
    title_pitch = ["D4", "E4", "G4", "G4", "A4", "B4", "D5"]
    chorus_b = ["B4", "A4", "G4", "G4", "A4", "B4", "A4", "G4"]
    chorus_c = ["B4", "B4", "A4", "G4", "A4", "B4", "D5"]
    chorus_d = ["B4", "A4", "G4", "E4", "G4", "A4", "G4"]
    bridge_low = ["B3", "D4", "E4", "G4", "E4", "D4", "B3", "D4"]
    entries = [
        ("v1_1", "verse_1", "Coffee ring on a moving box", ["Cof-", "-fee", "ring", "on", "a", "mov-", "-ing", "box"], verse_pitch_a, 16.5),
        ("v1_2", "verse_1", "Seven-thirty on the station clock", ["Sev-", "-en", "thir-", "-ty", "on", "the", "sta-", "-tion", "clock"], verse_pitch_b, 24.5),
        ("v1_3", "verse_1", "I kept your note in my jacket seam", ["I", "kept", "your", "note", "in", "my", "jack-", "-et", "seam"], verse_pitch_a, 32.5),
        ("v1_4", "verse_1", "A little far isn't out of reach", ["A", "lit-", "-tle", "far", "is-", "-n't", "out", "of", "reach"], verse_pitch_b, 40.5),
        ("p1_1", "pre_1", "Every red light tells me wait", ["Ev-", "-ery", "red", "light", "tells", "me", "wait"], pre_pitch, 48.5),
        ("p1_2", "pre_1", "Every green light says to go", ["Ev-", "-ery", "green", "light", "says", "to", "go"], ["F#4", "G4", "A4", "B4", "D5", "C5", "D5"], 56.5),
        ("c1_1", "chorus_1", "Different windows, same sky", ["Dif-", "-fer-", "-ent", "win-", "-dows", "same", "sky"], title_pitch, 64.5),
        ("c1_2", "chorus_1", "You turn your lamp on, so do I", ["You", "turn", "your", "lamp", "on", "so", "do", "I"], chorus_b, 72.5),
        ("c1_3", "chorus_1", "If the miles keep pulling through", ["If", "the", "miles", "keep", "pull-", "-ing", "through"], chorus_c, 80.5),
        ("c1_4", "chorus_1", "They can't move the moon from you", ["They", "can't", "move", "the", "moon", "from", "you"], chorus_d, 88.5),
        ("v2_1", "verse_2", "New street names in a stranger's rain", ["New", "street", "names", "in", "a", "stran-", "-ger's", "rain"], verse_pitch_b, 96.5),
        ("v2_2", "verse_2", "I learn the corners, miss my train", ["I", "learn", "the", "cor-", "-ners", "miss", "my", "train"], verse_pitch_a, 104.5),
        ("v2_3", "verse_2", "Your voice arrives in a midnight tone", ["Your", "voice", "ar-", "-rives", "in", "a", "mid-", "-night", "tone"], verse_pitch_b, 112.5),
        ("v2_4", "verse_2", "Makes this borrowed room feel close to home", ["Makes", "this", "bor-", "-rowed", "room", "feel", "close", "to", "home"], verse_pitch_a, 120.5),
        ("p2_1", "pre_2", "Every wrong turn draws a line", ["Ev-", "-ery", "wrong", "turn", "draws", "a", "line"], pre_pitch, 128.5),
        ("p2_2", "pre_2", "Back to where your map meets mine", ["Back", "to", "where", "your", "map", "meets", "mine"], ["F#4", "G4", "A4", "B4", "D5", "C5", "D5"], 136.5),
        ("c2_1", "chorus_2", "Different windows, same sky", ["Dif-", "-fer-", "-ent", "win-", "-dows", "same", "sky"], title_pitch, 144.5),
        ("c2_2", "chorus_2", "You turn your lamp on, so do I", ["You", "turn", "your", "lamp", "on", "so", "do", "I"], chorus_b, 152.5),
        ("c2_3", "chorus_2", "If the miles keep pulling through", ["If", "the", "miles", "keep", "pull-", "-ing", "through"], chorus_c, 160.5),
        ("c2_4", "chorus_2", "They can't move the moon from you", ["They", "can't", "move", "the", "moon", "from", "you"], chorus_d, 168.5),
        ("b_1", "bridge", "Someday the boxes turn to shelves", ["Some-", "-day", "the", "box-", "-es", "turn", "to", "shelves"], bridge_low, 176.5),
        ("b_2", "bridge", "We stop explaining where we are", ["We", "stop", "ex-", "-plain-", "-ing", "where", "we", "are"], ["B3", "D4", "E4", "F#4", "G4", "A4", "G4", "F#4"], 184.5),
        ("b_3", "bridge", "No more counting time in calls", ["No", "more", "count-", "-ing", "time", "in", "calls"], ["D4", "E4", "G4", "A4", "B4", "A4", "G4"], 192.5),
        ("b_4", "bridge", "No more waving through the dark", ["No", "more", "wav-", "-ing", "through", "the", "dark"], ["E4", "G4", "A4", "B4", "C5", "D5", "D5"], 200.5),
        ("fc_1", "final_chorus", "Different windows, same sky", ["Dif-", "-fer-", "-ent", "win-", "-dows", "same", "sky"], title_pitch, 208.5),
        ("fc_2", "final_chorus", "You turn your lamp on, so do I", ["You", "turn", "your", "lamp", "on", "so", "do", "I"], chorus_b, 216.5),
        ("fc_3", "final_chorus", "When the morning opens blue", ["When", "the", "morn-", "-ing", "o-", "-pens", "blue"], ["B4", "C5", "D5", "E5", "D5", "C5", "E5"], 224.5),
        ("fc_4", "final_chorus", "I will share the room with you", ["I", "will", "share", "the", "room", "with", "you"], ["D5", "B4", "A4", "G4", "A4", "B4", "G4"], 232.5),
        ("fc_5", "final_chorus", "Different windows, one light", ["Dif-", "-fer-", "-ent", "win-", "-dows", "one", "light"], ["D4", "E4", "G4", "A4", "B4", "D5", "E5"], 240.5),
        ("fc_6", "final_chorus", "Leave it burning through the night", ["Leave", "it", "burn-", "-ing", "through", "the", "night"], ["D5", "B4", "A4", "G4", "A4", "B4", "G4"], 248.5),
        ("out_1", "outro", "Different windows, same sky", ["Dif-", "-fer-", "-ent", "win-", "-dows", "same", "sky"], ["D4", "E4", "G4", "G4", "A4", "B4", "G4"], 260.0),
    ]
    for pid, section, text, tokens, pitch_pattern, start in entries:
        durations = default_durations(len(tokens), 1.75 if "sky" in text.lower() or text.endswith("I") or text.endswith("blue") or text.endswith("you") or text.endswith("night") else 1.5)
        if pid.endswith("_1") and section.startswith("chorus") or pid in {"fc_1", "out_1"}:
            durations = [.5, .5, .5, 1.0, 1.0, 1.0, 1.75]
        phrases.append(phrase(pid, section, text, tokens, fit(pitch_pattern, len(tokens)), durations, start))
    return {
        "metadata": {
            "title": "Different Windows", "language": "en", "tempo": 108, "time_signature": "4/4", "key": "G major",
            "score_type": "language_neutral_vocal_topline", "time_unit": "quarter_note_beats",
            "start_beat_origin": "zero_based_absolute", "render_status": "score_only_no_vocal_audio",
            "intended_range": {"lowest": "B3", "highest": "E5"},
            "tokenization": "One sung syllable per note; leading/trailing hyphens join syllables into a word.",
        },
        "phrase_count": len(phrases), "phrases": phrases,
    }


def main() -> None:
    composition = build_composition()
    encoded = json.dumps(composition, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "composition_v1.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition.json").write_text(encoded, encoding="utf-8")
    score = build_vocal_score()
    (ROOT / "vocal-score.json").write_text(json.dumps(score, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
