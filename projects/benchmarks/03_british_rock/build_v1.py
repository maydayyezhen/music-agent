from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def note(pitch: str, at: str, duration: float, velocity: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": at, "duration": duration, "velocity": velocity}


def chord(pitches: list[str], at: str, duration: float, velocity: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": at, "duration": duration, "velocity": velocity}


def drum(name: str, at: str, velocity: int, duration: float = 0.12) -> dict:
    return {"type": "drum", "note": name, "at": at, "duration": duration, "velocity": velocity}


def clip(loop_bars: int, events: list[dict]) -> dict:
    return {"loop_bars": loop_bars, "events": events}


def riff_bar(bar: int, root: str, fifth: str, octave: str, accent: int = 104) -> list[dict]:
    # Short-short-rest-short-long-short: the song's recognizable rhythmic fingerprint.
    return [
        chord([root, fifth], f"{bar}:1", 0.38, accent),
        note(octave, f"{bar}:1.5", 0.28, accent - 12),
        chord([root, fifth], f"{bar}:2.25", 0.34, accent - 5),
        chord([root, fifth], f"{bar}:3", 0.70, accent + 3),
        note(octave, f"{bar}:4", 0.36, accent - 8),
    ]


def hats(bar: int, open_last: bool = False, base: int = 76) -> list[dict]:
    out: list[dict] = []
    for i in range(8):
        beat = 1 + i * 0.5
        name = "open_hat" if open_last and i == 7 else "closed_hat"
        vel = base + (9 if i % 2 == 0 else -7) + (3 if i == 0 else 0)
        out.append(drum(name, f"{bar}:{beat:g}", vel))
    return out


def rock_drums(loop_bars: int, chorus: bool = False, fill_last: bool = False) -> list[dict]:
    out: list[dict] = []
    for bar in range(1, loop_bars + 1):
        out += hats(bar, open_last=chorus and bar % 2 == 0, base=82 if chorus else 73)
        out += [drum("snare", f"{bar}:2", 111 if chorus else 104), drum("snare", f"{bar}:4", 114 if chorus else 107)]
        kicks = [1, 1.75, 3, 3.5] if chorus else [1, 2.75, 3.5]
        if bar % 2 == 0:
            kicks = kicks + ([2.5] if chorus else [4.25])
        out += [drum("kick", f"{bar}:{beat:g}", 112 if beat in (1, 3) else 98) for beat in kicks]
        if chorus and bar == 1:
            out.append(drum("crash", f"{bar}:1", 118, 0.3))
    if fill_last:
        bar = loop_bars
        out += [
            drum("low_tom", f"{bar}:3", 94),
            drum("mid_tom", f"{bar}:3.5", 101),
            drum("high_tom", f"{bar}:4", 108),
            drum("snare", f"{bar}:4.5", 116),
        ]
    return out


sections = [
    {"name": "cold_open", "bars": 4},
    {"name": "verse", "bars": 12},
    {"name": "chorus", "bars": 12},
    {"name": "breakdown", "bars": 8},
    {"name": "final_chorus", "bars": 8},
    {"name": "outro", "bars": 2},
]

guitar_l = {
    "cold_open": clip(2, riff_bar(1, "E3", "B3", "E4", 109) + riff_bar(2, "G3", "D4", "G4", 105)),
    "verse": clip(4,
        riff_bar(1, "E3", "B3", "E4", 101)
        + riff_bar(2, "G3", "D4", "G4", 98)
        + riff_bar(3, "A3", "E4", "A4", 104)
        + riff_bar(4, "G3", "D4", "G4", 99)
    ),
    "chorus": clip(4,
        riff_bar(1, "D3", "A3", "D4", 110)
        + riff_bar(2, "A3", "E4", "A4", 112)
        + riff_bar(3, "E3", "B3", "E4", 115)
        + riff_bar(4, "G3", "D4", "G4", 111)
    ),
    "breakdown": clip(4, [
        chord(["C3", "G3"], "1:1", 1.6, 91), chord(["C3", "G3"], "1:3.25", 0.5, 84),
        chord(["G3", "D4"], "2:1", 1.4, 90), chord(["G3", "D4"], "2:3", 0.6, 88),
        chord(["D3", "A3"], "3:1", 1.5, 94), chord(["D3", "A3"], "3:3.5", 0.4, 88),
        chord(["A3", "E4"], "4:1", 0.35, 97), chord(["A3", "E4"], "4:2", 0.35, 94),
        chord(["B3", "F#4"], "4:3", 0.35, 101), chord(["D4", "A4"], "4:4", 0.45, 106),
    ]),
    "final_chorus": clip(4,
        riff_bar(1, "D3", "A3", "D4", 114)
        + riff_bar(2, "A3", "E4", "A4", 116)
        + riff_bar(3, "E3", "B3", "E4", 120)
        + riff_bar(4, "G3", "D4", "G4", 115)
    ),
    "outro": clip(2, riff_bar(1, "E3", "B3", "E4", 116) + [chord(["E3", "B3", "E4"], "2:1", 3.6, 120)]),
}

# V1 deliberately keeps the right guitar busy so the rendered balance can be judged and revised.
guitar_r = {
    "cold_open": clip(2, [
        chord(["E4", "B4"], "1:1", 1.7, 92), chord(["E4", "B4"], "1:3", 1.7, 96),
        chord(["G4", "D5"], "2:1", 1.7, 90), chord(["G4", "D5"], "2:3", 1.7, 95),
    ]),
    "verse": clip(4, [
        chord(["E4", "B4"], "1:1", 0.8, 94), chord(["E4", "B4"], "1:2", 0.8, 91), chord(["E4", "B4"], "1:3", 0.8, 96), chord(["E4", "B4"], "1:4", 0.8, 92),
        chord(["G4", "D5"], "2:1", 0.8, 94), chord(["G4", "D5"], "2:2", 0.8, 90), chord(["G4", "D5"], "2:3", 0.8, 96), chord(["G4", "D5"], "2:4", 0.8, 91),
        chord(["A4", "E5"], "3:1", 0.8, 97), chord(["A4", "E5"], "3:2", 0.8, 92), chord(["A4", "E5"], "3:3", 0.8, 99), chord(["A4", "E5"], "3:4", 0.8, 94),
        chord(["G4", "D5"], "4:1", 0.8, 95), chord(["G4", "D5"], "4:2", 0.8, 91), chord(["G4", "D5"], "4:3", 0.8, 98), chord(["G4", "D5"], "4:4", 0.8, 93),
    ]),
    "chorus": clip(4, [
        chord(["D4", "A4", "D5"], "1:1", 1.75, 105), chord(["D4", "A4", "D5"], "1:3", 1.75, 109),
        chord(["A3", "E4", "A4"], "2:1", 1.75, 107), chord(["A3", "E4", "A4"], "2:3", 1.75, 111),
        chord(["E4", "B4", "E5"], "3:1", 1.75, 112), chord(["E4", "B4", "E5"], "3:3", 1.75, 115),
        chord(["G4", "D5", "G5"], "4:1", 1.75, 108), chord(["G4", "D5", "G5"], "4:3", 1.75, 112),
    ]),
    "breakdown": clip(4, [
        note("E4", "1:2.5", 0.35, 82), note("G4", "1:4", 0.35, 86),
        note("B4", "2:2.5", 0.35, 84), note("A4", "2:4", 0.35, 88),
        note("F#4", "3:2.5", 0.35, 86), note("A4", "3:4", 0.35, 90),
        note("E4", "4:2.5", 0.35, 89), note("D5", "4:4", 0.4, 96),
    ]),
    "final_chorus": clip(4, [
        chord(["D4", "A4", "D5"], "1:1", 1.75, 110), chord(["D4", "A4", "D5"], "1:3", 1.75, 113),
        chord(["A3", "E4", "A4"], "2:1", 1.75, 112), chord(["A3", "E4", "A4"], "2:3", 1.75, 115),
        chord(["E4", "B4", "E5"], "3:1", 1.75, 116), chord(["E4", "B4", "E5"], "3:3", 1.75, 120),
        chord(["G4", "D5", "G5"], "4:1", 1.75, 113), chord(["G4", "D5", "G5"], "4:3", 1.75, 117),
    ]),
    "outro": clip(2, [note("B4", "1:1.5", 0.35, 102), note("G4", "1:2.5", 0.35, 98), chord(["E4", "B4", "E5"], "2:1", 3.5, 116)]),
}

bass = {
    "cold_open": clip(2, [
        note("E2", "1:1", 0.7, 103), note("B2", "1:2", 0.4, 91), note("D3", "1:2.75", 0.35, 88), note("E3", "1:3.5", 0.45, 98),
        note("G2", "2:1", 0.7, 101), note("D3", "2:2", 0.4, 90), note("F#2", "2:3", 0.35, 87), note("G2", "2:3.5", 0.6, 96),
    ]),
    "verse": clip(4, [
        note("E2", "1:1", 0.7, 101), note("B2", "1:2", 0.35, 91), note("D3", "1:2.75", 0.35, 88), note("E3", "1:3.5", 0.4, 96), note("F#2", "1:4.5", 0.25, 84),
        note("G2", "2:1", 0.7, 100), note("D3", "2:2", 0.35, 90), note("B2", "2:2.75", 0.35, 86), note("G2", "2:3.5", 0.45, 95), note("G#2", "2:4.5", 0.25, 86),
        note("A2", "3:1", 0.7, 104), note("E3", "3:2", 0.35, 94), note("G3", "3:2.75", 0.35, 90), note("A2", "3:3.5", 0.45, 98), note("F#2", "3:4.5", 0.25, 84),
        note("G2", "4:1", 0.7, 101), note("D3", "4:2", 0.35, 91), note("B2", "4:2.75", 0.35, 87), note("G2", "4:3.5", 0.45, 96), note("D#2", "4:4.5", 0.25, 90),
    ]),
    "chorus": clip(4, [
        note("D2", "1:1", 0.45, 108), note("A2", "1:1.75", 0.35, 96), note("D3", "1:2.5", 0.35, 101), note("C3", "1:3.25", 0.35, 92), note("B2", "1:4", 0.45, 96),
        note("A2", "2:1", 0.45, 108), note("E3", "2:1.75", 0.35, 98), note("A2", "2:2.5", 0.35, 102), note("B2", "2:3.25", 0.35, 94), note("D#2", "2:4.5", 0.25, 91),
        note("E2", "3:1", 0.45, 112), note("B2", "3:1.75", 0.35, 101), note("E3", "3:2.5", 0.35, 106), note("D3", "3:3.25", 0.35, 96), note("F#2", "3:4.5", 0.25, 92),
        note("G2", "4:1", 0.45, 109), note("D3", "4:1.75", 0.35, 98), note("G2", "4:2.5", 0.35, 103), note("A2", "4:3.25", 0.35, 96), note("C#3", "4:4.5", 0.25, 92),
    ]),
    "breakdown": clip(4, [
        note("C2", "1:1", 1.4, 92), note("G2", "1:3", 0.45, 86), note("B2", "1:4.5", 0.25, 82),
        note("G2", "2:1", 1.2, 90), note("D3", "2:3", 0.4, 84), note("C#3", "2:4.5", 0.25, 84),
        note("D2", "3:1", 1.2, 94), note("A2", "3:3", 0.4, 87), note("G#2", "3:4.5", 0.25, 86),
        note("A2", "4:1", 0.6, 96), note("B2", "4:2", 0.4, 91), note("D3", "4:3", 0.4, 94), note("D#3", "4:4.5", 0.25, 92),
    ]),
    "final_chorus": clip(4, []),
    "outro": clip(2, [note("E2", "1:1", 0.55, 111), note("B2", "1:2", 0.35, 99), note("D3", "1:3", 0.35, 97), note("E2", "1:4", 0.45, 105), note("E2", "2:1", 3.6, 114)]),
}
# Final chorus reuses the chorus bass pattern in V1.
bass["final_chorus"] = bass["chorus"]

drums = {
    "cold_open": clip(2, rock_drums(2, chorus=False, fill_last=True)),
    "verse": clip(4, rock_drums(4, chorus=False, fill_last=True)),
    "chorus": clip(4, rock_drums(4, chorus=True, fill_last=True)),
    "breakdown": clip(4, [
        drum("kick", "1:1", 101), drum("closed_hat", "1:1", 72), drum("snare", "1:3", 98), drum("closed_hat", "1:3", 69),
        drum("kick", "2:1", 99), drum("closed_hat", "2:1", 70), drum("snare", "2:3", 98), drum("closed_hat", "2:3", 68),
        drum("kick", "3:1", 102), drum("closed_hat", "3:1", 72), drum("snare", "3:3", 101), drum("closed_hat", "3:3", 70),
        drum("kick", "4:1", 105), drum("closed_hat", "4:1", 74), drum("snare", "4:3", 104), drum("low_tom", "4:3.5", 91), drum("mid_tom", "4:4", 99), drum("high_tom", "4:4.5", 108),
    ]),
    "final_chorus": clip(4, rock_drums(4, chorus=True, fill_last=True)),
    "outro": clip(2, rock_drums(2, chorus=True, fill_last=False) + [drum("crash", "2:1", 124, 0.5), drum("kick", "2:1", 120)]),
}

organ = {
    "breakdown": clip(4, [
        chord(["E4", "G4", "C5"], "1:1", 3.7, 61),
        chord(["D4", "G4", "B4"], "2:1", 3.7, 59),
        chord(["F#4", "A4", "D5"], "3:1", 3.7, 62),
        chord(["E4", "A4", "C5"], "4:1", 3.7, 64),
    ]),
    "final_chorus": clip(4, [
        chord(["F#4", "A4", "D5"], "1:1", 3.7, 54),
        chord(["E4", "A4", "C#5"], "2:1", 3.7, 53),
        chord(["G4", "B4", "E5"], "3:1", 3.7, 57),
        chord(["G4", "B4", "D5"], "4:1", 3.7, 55),
    ]),
}

composition = {
    "metadata": {
        "title": "Borrowed Trouble",
        "tempo": 156,
        "time_signature": "4/4",
        "key": "E minor / modal rock",
        "composer_note": "Fast British/alternative rock: twin overdriven guitars, mobile bass, live-feeling drums, no strings. V1."
    },
    "sections": sections,
    "tracks": {
        "guitar_l": {"sections": guitar_l},
        "guitar_r": {"sections": guitar_r},
        "bass": {"sections": bass},
        "drums": {"sections": drums},
        "organ": {"sections": organ},
    },
}

instruments = {
    "guitar_l": {"engine": "fluidsynth", "bank": 0, "program": 29, "channel": 1, "gm_name": "Overdriven Guitar"},
    "guitar_r": {"engine": "fluidsynth", "bank": 0, "program": 29, "channel": 2, "gm_name": "Overdriven Guitar"},
    "bass": {"engine": "fluidsynth", "bank": 0, "program": 33, "channel": 3, "gm_name": "Electric Bass (finger)"},
    "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 0, "gm_name": "Standard Drum Kit"},
    "organ": {"engine": "fluidsynth", "bank": 0, "program": 16, "channel": 4, "gm_name": "Drawbar Organ"},
}

render = {
    "sample_rate": 44100,
    "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
    "fluidsynth_gain": 0.7,
    "tail_seconds": 2.0,
    "master_peak_db": -1.0,
    "mix": {
        "guitar_l": {"volume_db": -5.2, "pan": -0.68, "mute": False},
        "guitar_r": {"volume_db": -5.2, "pan": 0.68, "mute": False},
        "bass": {"volume_db": -2.8, "pan": 0.0, "mute": False},
        "drums": {"volume_db": -2.5, "pan": 0.0, "mute": False},
        "organ": {"volume_db": -11.0, "pan": 0.12, "mute": False},
    },
}

(ROOT / "tracks").mkdir(parents=True, exist_ok=True)
(ROOT / "stems").mkdir(parents=True, exist_ok=True)
(ROOT / "output").mkdir(parents=True, exist_ok=True)
(ROOT / "composition_v1.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "composition.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "instruments.json").write_text(json.dumps(instruments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "render.json").write_text(json.dumps(render, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

