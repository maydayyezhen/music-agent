from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SONG = "crash_into_daylight_pop_rock"
TEMPO = 148

SECTIONS = [
    ("intro", 8, "standard"),
    ("verse_1", 16, "rich"),
    ("pre_1", 8, "rich"),
    ("chorus_1", 16, "rich"),
    ("turn", 4, "rich"),
    ("verse_2", 12, "rich"),
    ("pre_2", 8, "rich"),
    ("chorus_2", 16, "dense"),
    ("bridge", 8, "rich"),
    ("final_chorus", 12, "dense"),
    ("outro", 4, "standard"),
]

PROGRESSIONS = {
    "intro": ["E", "B", "C#m", "A", "E", "F#m", "A", "B"],
    "verse_1": ["E", "B/D#", "C#m", "A", "E", "A", "B", "B", "C#m", "B", "A", "E/G#", "F#m", "A", "B", "B"],
    "pre_1": ["F#m", "A", "E", "B", "F#m", "A", "B", "B"],
    "chorus_1": ["E", "B", "C#m", "A", "E", "B", "A", "B", "C#m", "B", "A", "E/G#", "F#m", "A", "B", "B"],
    "turn": ["C#m", "A", "E", "B"],
    "verse_2": ["E", "B/D#", "C#m", "A", "E", "A", "B", "B", "C#m", "A", "F#m", "B"],
    "pre_2": ["F#m", "A", "E", "B", "F#m", "A", "B", "B"],
    "chorus_2": ["E", "B", "C#m", "A", "E", "B", "A", "B", "C#m", "B", "A", "E/G#", "F#m", "A", "B", "B"],
    "bridge": ["C#m", "A", "E", "B", "C#m", "A", "F#m", "B"],
    "final_chorus": ["E", "B", "C#m", "A", "E", "B", "A", "B", "C#m", "B", "A", "E"],
    "outro": ["E", "C#m", "A", "E"],
}

H = {
    "E": {"g": ["E3", "B3"], "p": ["G#3", "B3", "E4"], "pad": ["E3", "B3", "E4", "G#4"], "bass": "E2", "fifth": "B2"},
    "B": {"g": ["B2", "F#3"], "p": ["F#3", "B3", "D#4"], "pad": ["B2", "F#3", "B3", "D#4"], "bass": "B1", "fifth": "F#2"},
    "B/D#": {"g": ["B2", "F#3"], "p": ["F#3", "B3", "D#4"], "pad": ["D#3", "F#3", "B3", "D#4"], "bass": "D#2", "fifth": "F#2"},
    "C#m": {"g": ["C#3", "G#3"], "p": ["G#3", "C#4", "E4"], "pad": ["C#3", "G#3", "C#4", "E4"], "bass": "C#2", "fifth": "G#2"},
    "A": {"g": ["A2", "E3"], "p": ["E3", "A3", "C#4"], "pad": ["A2", "E3", "A3", "C#4"], "bass": "A1", "fifth": "E2"},
    "E/G#": {"g": ["E3", "B3"], "p": ["G#3", "B3", "E4"], "pad": ["G#2", "E3", "B3", "E4"], "bass": "G#2", "fifth": "B2"},
    "F#m": {"g": ["F#2", "C#3"], "p": ["F#3", "A3", "C#4"], "pad": ["F#2", "C#3", "F#3", "A3"], "bass": "F#1", "fifth": "C#2"},
}


def pos(bar: int, beat: float) -> str:
    text = f"{beat:.2f}".rstrip("0").rstrip(".")
    return f"{bar}:{text}"


def note(bar: int, beat: float, pitch: str, dur: float, vel: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": pos(bar, beat), "duration": dur, "velocity": vel}


def chord(bar: int, beat: float, pitches: list[str], dur: float, vel: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": pos(bar, beat), "duration": dur, "velocity": vel}


def drum(bar: int, beat: float, name: str, vel: int, dur: float = 0.1) -> dict:
    return {"type": "drum", "note": name, "at": pos(bar, beat), "duration": dur, "velocity": vel}


def clip(events: list[dict], bars: int) -> dict:
    return {"loop_bars": bars, "events": events}


def phrase(base_bar: int, pattern: list[tuple[int, float, str, float, int]], velocity_delta: int = 0) -> list[dict]:
    return [note(base_bar + b - 1, beat, pitch, dur, max(1, min(127, vel + velocity_delta))) for b, beat, pitch, dur, vel in pattern]


VERSE_A = [
    (1, 2, "G#4", .72, 78), (1, 3, "F#4", .48, 74), (1, 3.75, "E4", 1.0, 72),
    (2, 1.5, "F#4", .50, 74), (2, 2.5, "G#4", .95, 78), (2, 4, "B4", .70, 81),
    (3, 2, "C#5", .70, 83), (3, 3, "B4", .50, 80), (3, 3.75, "G#4", 1.20, 76),
    (4, 3, "F#4", .70, 72), (4, 4, "E4", .80, 70),
]
VERSE_B = [
    (1, 1.5, "G#4", .70, 77), (1, 2.5, "B4", .52, 81), (1, 3.5, "C#5", .90, 84),
    (2, 2, "B4", .65, 80), (2, 3, "A4", .52, 77), (2, 4, "G#4", .85, 75),
    (3, 1.5, "F#4", .60, 74), (3, 2.5, "G#4", .60, 77), (3, 3.5, "B4", 1.05, 82),
    (4, 2, "A4", .55, 78), (4, 3, "F#4", .55, 73), (4, 4, "E4", .90, 71),
]
PRE = [
    (1, 1.5, "F#4", .60, 80), (1, 2.5, "A4", .60, 83), (1, 3.5, "G#4", .75, 81),
    (2, 1, "G#4", .60, 81), (2, 2, "B4", .60, 85), (2, 3, "A4", .60, 83), (2, 4, "B4", .70, 86),
    (3, 1.5, "A4", .60, 84), (3, 2.5, "B4", .60, 87), (3, 3.5, "C#5", .80, 90),
    (4, 1, "B4", .55, 87), (4, 2, "C#5", .55, 91), (4, 3, "D#5", .55, 93), (4, 4, "E5", .90, 97),
]
CHORUS = [
    (1, 1, "B4", .65, 91), (1, 2, "B4", .65, 92), (1, 3, "C#5", .65, 94), (1, 4, "E5", .95, 99),
    (2, 1.5, "F#5", .70, 101), (2, 2.5, "E5", .70, 98), (2, 3.5, "D#5", 1.0, 96),
    (3, 1, "C#5", .65, 93), (3, 2, "B4", .65, 90), (3, 3, "A4", .65, 87), (3, 4, "B4", .85, 91),
    (4, 1.5, "G#4", .65, 86), (4, 2.5, "A4", .65, 88), (4, 3.5, "B4", 1.10, 93),
]
BRIDGE = [
    (1, 2, "E5", .90, 88), (1, 3.5, "C#5", 1.10, 84),
    (2, 2, "B4", .80, 82), (2, 3.5, "A4", 1.20, 80),
    (3, 1.5, "G#4", .65, 80), (3, 2.5, "B4", .65, 84), (3, 3.5, "C#5", 1.0, 87),
    (4, 2, "D#5", .65, 90), (4, 3, "E5", 1.45, 94),
]
OUTRO = [
    (1, 2, "B4", .65, 86), (1, 3, "C#5", .65, 88), (1, 4, "E5", 1.0, 93),
    (2, 2, "D#5", .65, 89), (2, 3, "B4", 1.1, 85),
    (3, 1.5, "A4", .65, 83), (3, 2.5, "B4", .65, 86), (3, 3.5, "G#4", .9, 82),
    (4, 1, "F#4", .65, 80), (4, 2, "G#4", .65, 82), (4, 3, "E4", 1.75, 78),
]


def vocal_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    if name == "intro":
        p = [(5, 3, "B4", .7, 78), (6, 1, "C#5", .7, 80), (6, 2.5, "B4", 1.15, 76),
             (7, 1, "G#4", .7, 74), (7, 2, "A4", .7, 76), (7, 3, "B4", 1.45, 82),
             (8, 2.5, "D#5", .45, 82), (8, 3.25, "B4", .45, 76), (8, 4, "A4", .7, 74)]
        return phrase(1, p)
    if name.startswith("verse"):
        blocks = bars // 4
        for i in range(blocks):
            pattern = VERSE_A if i % 2 == 0 else VERSE_B
            delta = 0 if name == "verse_1" else 2
            out.extend(phrase(i * 4 + 1, pattern, delta))
        return out
    if name.startswith("pre"):
        out.extend(phrase(1, PRE, 0 if name == "pre_1" else 2))
        out.extend(phrase(5, PRE, 3 if name == "pre_1" else 5))
        return out
    if name.startswith("chorus") or name == "final_chorus":
        blocks = bars // 4
        delta = 0 if name == "chorus_1" else 2 if name == "chorus_2" else 5
        for i in range(blocks):
            out.extend(phrase(i * 4 + 1, CHORUS, delta + (1 if i == blocks - 1 else 0)))
        return out
    if name == "turn":
        return [note(1, 1, "E5", 1.4, 88), note(3, 3, "B4", 1.5, 82)]
    if name == "bridge":
        out.extend(phrase(1, BRIDGE))
        out.extend(phrase(5, BRIDGE, 4))
        return out
    if name == "outro":
        return phrase(1, OUTRO)
    return out


def muted_guitar(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    start = 5 if name == "intro" else 1
    for bar in range(start, bars + 1):
        h = H[PROGRESSIONS[name][bar - 1]]
        if name == "bridge" and bar <= 4:
            beats = [1, 2, 4]
            gate = .35
        elif name.startswith("pre"):
            beats = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]
            gate = .22
        else:
            beats = [1, 1.5, 2, 2.5, 3, 3.5, 4]
            if bar % 4 != 0:
                beats.append(4.5)
            gate = .24
        for i, beat in enumerate(beats):
            base = 58 if name == "intro" else 62
            if name.startswith("pre"):
                base += 4
            vel = base + (6 if beat in {1, 3} else 0) + min(6, i)
            out.append(chord(bar, beat, h["g"], gate, vel))
    return out


def rhythm_guitar(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    start = 5 if name == "bridge" else 1
    for bar in range(start, bars + 1):
        h = H[PROGRESSIONS[name][bar - 1]]
        for beat in [1, 2, 3, 4]:
            vel = 86 + (4 if beat in {1, 3} else 0) + (3 if name == "final_chorus" else 0)
            out.append(chord(bar, beat, h["g"], 1.08, vel))
        if bar in {4, 8, 12, 16}:
            out.append(chord(bar, 4.75, h["g"], .28, 92))
    return out


def bass_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    open_mode = name.startswith("chorus") or name in {"final_chorus", "turn"}
    for bar in range(1, bars + 1):
        h = H[PROGRESSIONS[name][bar - 1]]
        if name == "bridge" and bar <= 4:
            for beat, dur, vel in [(1, 1.6, 82), (3, 1.55, 79)]:
                out.append(note(bar, beat, h["bass"], dur, vel))
        elif open_mode or (name == "bridge" and bar > 4):
            for beat in [1, 2, 3, 4]:
                pitch = h["fifth"] if beat == 3 and bar % 2 == 0 else h["bass"]
                vel = 88 + (3 if beat in {1, 3} else -1)
                if name == "final_chorus":
                    vel += 2
                out.append(note(bar, beat, pitch, .84, vel))
            if bar % 4 == 0:
                out.append(note(bar, 4.5, h["fifth"], .32, 78))
        elif name == "outro":
            out.append(note(bar, 1, h["bass"], 1.6, 76))
            out.append(note(bar, 3, h["fifth"], 1.3, 72))
        else:
            out.append(note(bar, 1, h["bass"], .72, 82))
            out.append(note(bar, 2, h["bass"], 1.45, 78))
            out.append(note(bar, 4, h["bass"], .72, 80))
            if bar % 4 == 0:
                out.append(note(bar, 4.5, h["fifth"], .32, 74))
    return out


def piano_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    for bar in range(1, bars + 1):
        h = H[PROGRESSIONS[name][bar - 1]]
        if name.startswith("verse"):
            out.append(chord(bar, 2.5, h["p"], .9, 51 + bar % 3))
            if bar % 2 == 0:
                out.append(chord(bar, 4, h["p"], .55, 46))
        elif name.startswith("pre"):
            out.append(chord(bar, 2, h["p"], .65, 53))
            out.append(chord(bar, 4, h["p"], .65, 56))
        elif name.startswith("chorus") or name == "final_chorus":
            if bar % 2 == 1:
                out.append(chord(bar, 1, h["p"], 3.4, 50))
            else:
                out.append(chord(bar, 3, h["p"], .8, 48))
        elif name in {"turn", "bridge", "outro"}:
            out.append(chord(bar, 1, h["p"], 3.55, 46 if name == "outro" else 49))
    return out


def pad_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    if name not in {"bridge", "final_chorus", "outro"}:
        return out
    for bar in range(1, bars + 1):
        if name == "outro" and bar < 3:
            continue
        h = H[PROGRESSIONS[name][bar - 1]]
        out.append(chord(bar, 1, h["pad"], 3.85, 42 if name != "outro" else 34))
    return out


def clean_guitar(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    active_bars = range(1, bars + 1)
    if name == "bridge":
        active_bars = range(1, 5)
    for bar in active_bars:
        h = H[PROGRESSIONS[name][bar - 1]]
        tones = h["p"]
        seq = [0, 1, 2, 1, 0, 1, 2, 1]
        for step, idx in enumerate(seq):
            out.append(note(bar, 1 + step * .5, tones[idx], .46, 48 + (4 if step in {0, 4} else 0)))
    return out


def lead_guitar(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    if name == "intro":
        return [note(2, 3, "E4", 1.7, 69), note(4, 3, "G#4", 1.7, 73), note(8, 1, "F#4", 2.2, 76)]
    if name == "turn":
        pitches = ["C#4", "E4", "F#4", "G#4", "B4", "A4", "F#4"]
        for i, p in enumerate(pitches):
            out.append(note(1 + i // 2, 1 + (i % 2) * 2, p, 1.35, 78 + i))
        return out
    if name == "bridge":
        pitches = ["C#4", "E4", "F#4", "G#4", "A4", "B4", "C#5", "B4", "G#4", "F#4"]
        for i, pitch in enumerate(pitches):
            out.append(note(1 + i // 2, 1 + (i % 2) * 2, pitch, 1.3 if i < 8 else 1.8, 74 + min(i, 6)))
        return out
    if name.startswith("verse"):
        for bar in range(4, bars + 1, 4):
            out.append(note(bar, 1, "B4", 1.25, 68))
        return out
    if name.startswith("chorus") or name == "final_chorus":
        for bar in range(4, bars + 1, 4):
            out.append(note(bar, 4, "E5" if name == "final_chorus" else "B4", 1.7, 72 if name != "final_chorus" else 78))
        return out
    return out


def drums_section(name: str, bars: int) -> list[dict]:
    out: list[dict] = []
    for bar in range(1, bars + 1):
        if name == "intro" and bar <= 4:
            for beat in [1, 2, 3, 4]:
                out.append(drum(bar, beat, "closed_hat", 55 if beat in {1, 3} else 50))
            out.append(drum(bar, 2, "side_stick", 66, .12))
            out.append(drum(bar, 4, "side_stick", 66, .12))
            out.append(drum(bar, 1, "kick", 84))
            out.append(drum(bar, 3, "kick", 84))
            continue
        half_time = name == "bridge" and bar <= 4
        chorus = name.startswith("chorus") or name == "final_chorus" or (name == "bridge" and bar > 4)
        pre = name.startswith("pre")
        outro = name == "outro"
        hat_name = "ride" if name == "final_chorus" and bar > 4 else "closed_hat"
        for step in range(8):
            beat = 1 + step * .5
            vel = (72 if chorus else 64 if pre else 60 if outro else 63) + (4 if step % 4 == 0 else -3)
            out.append(drum(bar, beat, hat_name, vel))
        if half_time:
            out.append(drum(bar, 3, "snare", 96, .12))
            for beat in [1, 2.5]:
                out.append(drum(bar, beat, "kick", 92))
        else:
            snare_velocity = 104 if chorus else 96 if pre else 82 if outro else 91
            out.append(drum(bar, 2, "snare", snare_velocity, .12))
            out.append(drum(bar, 4, "snare", snare_velocity, .12))
            kicks = [1, 1.5, 2.5, 3, 3.5, 4.5] if chorus else [1, 2.5, 3.5] if pre else [1, 2.5] if bar % 2 else [1, 3, 3.5]
            if outro:
                kicks = [1, 3]
            for beat in kicks:
                out.append(drum(bar, beat, "kick", 106 if chorus else 96 if pre else 87 if outro else 94))
        if bar == 1 and name in {"chorus_1", "chorus_2", "final_chorus", "turn"}:
            out.append(drum(bar, 1, "crash", 100 if name != "final_chorus" else 108, .12))
        if bar % 4 == 0 and not outro:
            for beat, tom in [(3.25, "high_tom"), (3.75, "mid_tom"), (4.25, "low_tom"), (4.75, "snare")]:
                out.append(drum(bar, beat, tom, 88 if chorus else 78, .12))
        if pre and bar in {4, 8}:
            out.append(drum(bar, 4.5, "open_hat", 82, .18))
    return out


def make_composition() -> dict:
    sections = []
    for name, bars, complexity in SECTIONS:
        budget = {"lead": 4, "drums": 4, "bass": 3, "guitars": 4}
        if complexity == "dense":
            budget.update({"lead": 5, "drums": 5, "bass": 4, "guitars": 5})
        sections.append({"name": name, "bars": bars, "complexity": complexity, "complexity_budget": budget})

    tracks = {
        "vocal_lead": {"role": "foreground vocal surrogate / lead melody", "sections": {}},
        "muted_guitar": {"role": "palm-muted rhythm guitar / verse drive", "sections": {}},
        "rhythm_guitar": {"role": "continuous overdriven rhythm bed / chorus foundation", "sections": {}},
        "lead_guitar": {"role": "sustained overdrive answer / melodic support", "sections": {}},
        "clean_guitar": {"role": "clean arpeggiated support / transition texture", "sections": {}},
        "bass": {"role": "section-linked pop-rock bass foundation", "sections": {}},
        "piano": {"role": "harmonic support / offbeat stabs and sustained voicings", "sections": {}},
        "pad": {"role": "background harmonic plane / bridge and final lift", "sections": {}},
        "drums": {"role": "pop-rock drum kit / groove and section dynamics", "sections": {}},
    }
    for name, bars, _ in SECTIONS:
        tracks["vocal_lead"]["sections"][name] = clip(vocal_section(name, bars), bars)
        tracks["bass"]["sections"][name] = clip(bass_section(name, bars), bars)
        tracks["drums"]["sections"][name] = clip(drums_section(name, bars), bars)
        if name in {"intro", "verse_1", "verse_2", "pre_1", "pre_2", "bridge"}:
            tracks["muted_guitar"]["sections"][name] = clip(muted_guitar(name, bars), bars)
        if name in {"chorus_1", "chorus_2", "bridge", "final_chorus"}:
            tracks["rhythm_guitar"]["sections"][name] = clip(rhythm_guitar(name, bars), bars)
        guitar_fill = lead_guitar(name, bars)
        if guitar_fill:
            tracks["lead_guitar"]["sections"][name] = clip(guitar_fill, bars)
        if name in {"intro", "turn", "bridge", "outro"}:
            tracks["clean_guitar"]["sections"][name] = clip(clean_guitar(name, bars), bars)
        if name != "intro":
            tracks["piano"]["sections"][name] = clip(piano_section(name, bars), bars)
        pad_events = pad_section(name, bars)
        if pad_events:
            tracks["pad"]["sections"][name] = clip(pad_events, bars)

    return {
        "metadata": {
            "title": "撞向天光 (Crash Into Daylight)",
            "tempo": TEMPO,
            "time_signature": "4/4",
            "key": "E major",
            "description": "Original upbeat pop-rock song with a flute vocal-surrogate, section-linked guitars, bass, piano, pad and dynamic drums.",
        },
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 4, "arrangement": 5, "melodic_ornamentation": 3, "density": 4, "variation": 4},
        "complexity_contour": "verse_chorus",
        "sections": sections,
        "tracks": tracks,
    }


INSTRUMENTS = {
    "vocal_lead": {"engine": "fluidsynth", "bank": 0, "program": 73, "gm_name": "Flute"},
    "muted_guitar": {"engine": "fluidsynth", "bank": 0, "program": 28, "gm_name": "Electric Guitar (muted)"},
    "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29, "gm_name": "Overdriven Guitar"},
    "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30, "gm_name": "Distortion Guitar"},
    "clean_guitar": {"engine": "fluidsynth", "bank": 0, "program": 27, "gm_name": "Electric Guitar (clean)"},
    "bass": {"engine": "fluidsynth", "bank": 0, "program": 33, "gm_name": "Electric Bass (finger)"},
    "piano": {"engine": "fluidsynth", "bank": 0, "program": 0, "gm_name": "Acoustic Grand Piano"},
    "pad": {"engine": "fluidsynth", "bank": 0, "program": 89, "gm_name": "Pad 2 (warm)"},
    "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 0, "gm_name": "Standard Drum Kit"},
}

RENDER = {
    "sample_rate": 44100,
    "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
    "fluidsynth_gain": 0.7,
    "tail_seconds": 2.0,
    "master_peak_db": -1.0,
    "mix": {
        "vocal_lead": {"volume_db": -2.5, "pan": 0.0, "mute": False},
        "muted_guitar": {"volume_db": -8.0, "pan": -0.42, "mute": False},
        "rhythm_guitar": {"volume_db": -7.0, "pan": 0.42, "mute": False},
        "lead_guitar": {"volume_db": -5.5, "pan": 0.18, "mute": False},
        "clean_guitar": {"volume_db": -8.5, "pan": -0.28, "mute": False},
        "bass": {"volume_db": -3.5, "pan": 0.0, "mute": False},
        "piano": {"volume_db": -8.0, "pan": -0.15, "mute": False},
        "pad": {"volume_db": -11.0, "pan": 0.12, "mute": False},
        "drums": {"volume_db": -3.5, "pan": 0.0, "mute": False},
    },
}


def write_project(project_dir: Path) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    composition = make_composition()
    (project_dir / "composition.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (project_dir / "instruments.json").write_text(json.dumps(INSTRUMENTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (project_dir / "render.json").write_text(json.dumps(RENDER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Built {SONG}: {sum(b for _, b, _ in SECTIONS)} bars at {TEMPO} BPM")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the structured pop-rock demo and optionally render it")
    parser.add_argument("--render", action="store_true", help="run scripts/render_song.py after building")
    args = parser.parse_args()
    project_dir = Path(__file__).resolve().parent
    root = project_dir.parents[1]
    write_project(project_dir)
    if args.render:
        completed = subprocess.run([sys.executable, str(root / "scripts" / "render_song.py"), SONG], cwd=root)
        return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
