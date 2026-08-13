from __future__ import annotations

import json
from pathlib import Path

from _bootstrap import ROOT
from src.complexity.schema import BUDGETS, COMPLEXITY_LEVELS, COMPLEXITY_PRESETS


DEMO = ROOT / "projects" / "complexity_demo"
SECTIONS = (("intro", 4), ("theme_a", 8), ("theme_b", 8), ("outro", 4))
CHORDS = {
    1: ["D4", "F4", "A4", "C5"],
    2: ["C4", "E4", "G4", "B4"],
    3: ["G3", "B3", "D4", "A4"],
    4: ["A3", "C4", "E4", "G4"],
}
ROOTS = {1: "D2", 2: "C2", 3: "G1", 4: "A1"}


def event(pitch: str, at: str, duration: float, velocity: int) -> dict:
    return {"type": "note", "pitch": pitch, "at": at, "duration": duration, "velocity": velocity}


def chord(pitches: list[str], at: str, duration: float, velocity: int) -> dict:
    return {"type": "chord", "pitches": pitches, "at": at, "duration": duration, "velocity": velocity}


def drum(note: str, at: str, velocity: int, duration: float = 0.18) -> dict:
    return {"type": "drum", "note": note, "at": at, "duration": duration, "velocity": velocity}


def lead_clip(level: int, section: str) -> dict:
    base = [
        event("D5", "1:1", 1.0, 88), event("A4", "1:2.5", 0.5, 78),
        event("C5", "1:3", 0.85, 84), event("E5", "1:4", 0.75, 90),
        event("F5", "2:1", 1.0, 91), event("E5", "2:2.25", 0.5, 82),
        event("C5", "2:3", 0.75, 80), event("D5", "2:4", 1.0, 94),
    ]
    if section == "intro":
        base = [event("D5", "2:1", 1.5, 72), event("A4", "3:3", 0.75, 68), event("C5", "4:1", 1.5, 76)]
    elif section == "outro":
        base = [event("F5", "1:1", 1.5, 78), event("E5", "2:1", 1.0, 74), event("C5", "2:3", 1.0, 70), event("D5", "3:1", 4.0, 76)]
    elif section == "theme_b":
        base = [dict(item) for item in base]
        for item in base:
            if item.get("pitch") in {"D5", "C5", "E5", "F5"}:
                item["pitch"] = {"D5": "D6", "C5": "C6", "E5": "E6", "F5": "F6"}[item["pitch"]]

    # All levels preserve the same eight structural tones. Complexity adds
    # transformation around them rather than replacing the identity.
    additions: list[dict] = []
    if level >= 2 and section in {"theme_a", "theme_b"}:
        additions += [event("A4" if section == "theme_a" else "A5", "3:1.5", 0.5, 75), event("C5" if section == "theme_a" else "C6", "3:2.5", 0.5, 79), event("D5" if section == "theme_a" else "D6", "4:1", 1.5, 88)]
    if level >= 3 and section in {"theme_a", "theme_b"}:
        additions += [event("E5" if section == "theme_a" else "E6", "2:3.75", 0.25, 72), event("G5" if section == "theme_a" else "G6", "3:3.5", 0.5, 82), event("F5" if section == "theme_a" else "F6", "4:3", 0.5, 76)]
    if level >= 4 and section == "theme_b":
        additions += [event("C6", "1:2.25", 0.25, 74), event("D6", "1:2.75", 0.25, 78), event("G6", "2:2.75", 0.25, 80), event("E6", "3:3", 0.35, 76)]
    if level >= 5 and section == "theme_b":
        additions += [event("A5", "1:1.75", 0.25, 70), event("B5", "1:2", 0.25, 73), event("A6", "2:2.5", 0.25, 84), event("G6", "4:2", 0.5, 80), event("E6", "4:2.75", 0.25, 75)]
    return {"loop_bars": 4, "rhythm_motif": "signal_A", "rhythm_variation": "A" if level <= 2 else ("A'" if level == 3 else "B"), "events": sorted(base + additions, key=lambda x: tuple(float(v) for v in x["at"].split(":")))}


def bass_clip(level: int, section: str) -> dict:
    events: list[dict] = []
    for bar in range(1, 5):
        root = ROOTS[bar]
        events.append(event(root, f"{bar}:1", 3.5 if level <= 2 else 1.75, 70 + level * 2))
        if level >= 3:
            fifth = {1: "A2", 2: "G2", 3: "D2", 4: "E2"}[bar]
            events.append(event(fifth, f"{bar}:3", 0.75, 68 + level * 2))
        if level >= 4 and section in {"theme_a", "theme_b"}:
            approach = {1: "C#2", 2: "B1", 3: "F#1", 4: "G1"}[bar]
            events.append(event(approach, f"{bar}:4.5", 0.35, 65 + level * 2))
        if level >= 5 and section == "theme_b":
            octave_echo = {1: "D3", 2: "C3", 3: "G2", 4: "A2"}[bar]
            events.append(event(octave_echo, f"{bar}:2.25", 0.35, 73))
    return {"loop_bars": 4, "rhythm_motif": "bass_anchor", "rhythm_variation": "A" if level < 4 else "B'", "events": events}


def pad_clip(level: int, section: str) -> dict:
    events: list[dict] = []
    stride = 2 if level == 1 else 1
    for bar in range(1, 5, stride):
        duration = 7.5 if stride == 2 else (3.5 if level <= 3 else 2.75)
        events.append(chord(CHORDS[bar], f"{bar}:1", duration, 48 + level * 3))
        if level >= 5 and section == "theme_b":
            events.append(chord(CHORDS[bar], f"{bar}:4", 0.65, 55))
    return {"loop_bars": 4, "rhythm_motif": "pad_breath", "rhythm_variation": "C" if level == 1 else "A", "events": events}


def drums_clip(level: int, section: str) -> dict:
    events: list[dict] = []
    for bar in range(1, 5):
        if section == "intro" and bar < 3:
            continue
        for beat in (1, 3):
            events.append(drum("kick", f"{bar}:{beat}", 74 + level * 3))
        for beat in (2, 4):
            events.append(drum("snare", f"{bar}:{beat}", 72 + level * 3))
        hats = (1, 2, 3, 4) if level == 2 else (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5)
        for beat in hats:
            if level >= 4 and beat == 3.5 and bar % 2 == 0:
                continue
            events.append(drum("closed_hat", f"{bar}:{beat}", 49 + (int(beat * 2) % 3) * 5))
        if level >= 4 and bar == 4:
            events += [drum("low_tom", "4:3.5", 76), drum("mid_tom", "4:4", 82), drum("high_tom", "4:4.5", 88)]
        if level >= 5 and section == "theme_b":
            events.append(drum("kick", f"{bar}:2.5", 72))
            events.append(drum("open_hat", f"{bar}:4.5", 62))
    return {"loop_bars": 4, "rhythm_motif": "drum_grid", "rhythm_variation": "A" if level <= 3 else "B", "events": events}


def guitar_clip(level: int, section: str) -> dict:
    events: list[dict] = []
    for bar in range(1, 5):
        tones = CHORDS[bar][1:]
        if level == 3:
            events.append(chord(tones, f"{bar}:2.5", 0.65, 61))
        else:
            for beat in (1.75, 3.75):
                events.append(chord(tones, f"{bar}:{beat}", 0.4, 58 + level * 2))
            if level >= 5 and section == "theme_b":
                events.append(chord(tones, f"{bar}:4.5", 0.25, 66))
    return {"loop_bars": 4, "rhythm_motif": "chord_answer", "rhythm_variation": "A'" if level == 3 else "B", "events": events}


def strings_clip(level: int, section: str) -> dict:
    pitches = ("A3", "G3", "B3", "C4")
    events = [event(pitches[bar - 1], f"{bar}:1", 2.5, 49 + level * 2) for bar in range(1, 5)]
    if level >= 5 and section == "theme_b":
        events += [event("E4", "2:4", 0.75, 62), event("F4", "4:3", 1.0, 65)]
    return {"loop_bars": 4, "rhythm_motif": "counter_long", "rhythm_variation": "C", "events": events}


def make_track(role: str, clips: dict[str, dict]) -> dict:
    return {"role": role, "sections": clips}


def distribute_budget(level_name: str, roles: list[str], delta: int) -> dict[str, int]:
    index = max(0, min(4, COMPLEXITY_LEVELS.index(level_name) + delta))
    target = BUDGETS[COMPLEXITY_LEVELS[index]]
    points = {role: 1 for role in roles}
    points["lead"] = min(5, max(2, index + 2))
    remaining = max(0, target - sum(points.values()))
    for role in ("drums", "chords", "counter", "bass", "texture"):
        if role in points and remaining:
            add = min(5 - points[role], remaining, 2)
            points[role] += add
            remaining -= add
    return points


def build(level_name: str) -> dict:
    level = COMPLEXITY_LEVELS.index(level_name) + 1
    profile = COMPLEXITY_PRESETS[level_name]
    tracks = {
        "piano": make_track("lead melody", {name: lead_clip(level, name) for name, _ in SECTIONS}),
        "bass": make_track("bass anchor", {name: bass_clip(level, name) for name, _ in SECTIONS if not (level == 2 and name == "outro")}),
        "pad": make_track("harmonic atmosphere", {name: pad_clip(level, name) for name, _ in SECTIONS}),
    }
    if level >= 2:
        tracks["drums"] = make_track("drum groove", {name: drums_clip(level, name) for name, _ in SECTIONS if not (level == 2 and name in {"intro", "outro"})})
    if level >= 3:
        tracks["guitar"] = make_track("offbeat chord response", {name: guitar_clip(level, name) for name, _ in SECTIONS if name in {"theme_a", "theme_b"}})
    if level >= 4:
        tracks["strings"] = make_track("long counterline", {name: strings_clip(level, name) for name, _ in SECTIONS if name in {"theme_b", "outro"}})

    roles = ["lead", "bass", "texture"] + (["drums"] if level >= 2 else []) + (["chords"] if level >= 3 else []) + (["counter"] if level >= 4 else [])
    contour_deltas = (-1, 0, 1, 0)

    return {
        "metadata": {"title": f"Signal Garden - {level_name.title()}", "tempo": 100, "time_signature": "4/4", "key": "D Dorian"},
        "complexity": profile,
        "complexity_contour": "wave",
        "rhythm_motifs": {
            "signal_A": [{"offset": 0, "duration": 1}, {"offset": 1.5, "duration": 0.5}, {"offset": 2, "duration": 0.85}, {"offset": 3, "duration": 0.75}],
            "bass_anchor": [{"offset": 0, "duration": 1.75}, {"offset": 2, "duration": 0.75}],
            "pad_breath": [{"offset": 0, "duration": 3.5}],
            "drum_grid": [{"offset": 0, "duration": 0.18}, {"offset": 1, "duration": 0.18}, {"offset": 2, "duration": 0.18}, {"offset": 3, "duration": 0.18}],
            "chord_answer": [{"offset": 1.5, "duration": 0.65}, {"offset": 3.5, "duration": 0.4}],
            "counter_long": [{"offset": 0, "duration": 2.5}]
        },
        "sections": [
            {"name": name, "bars": bars, "complexity_budget": distribute_budget(level_name, roles, contour_deltas[index])}
            for index, (name, bars) in enumerate(SECTIONS)
        ],
        "tracks": tracks,
    }


def local_render(track_names: list[str]) -> dict:
    pans = {"piano": -0.08, "bass": 0.0, "pad": 0.24, "drums": 0.0, "guitar": -0.35, "strings": 0.38}
    volumes = {"piano": -2.5, "bass": -4.0, "pad": -9.0, "drums": -5.0, "guitar": -7.0, "strings": -8.0}
    return {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.7, "tail_seconds": 2.0, "master_peak_db": -1.0, "mix": {name: {"volume_db": volumes[name], "pan": pans[name], "mute": False} for name in track_names}}


def main() -> int:
    DEMO.mkdir(parents=True, exist_ok=True)
    for level in COMPLEXITY_LEVELS:
        composition = build(level)
        folder = DEMO / level
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "composition.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "render.json").write_text(json.dumps(local_render(list(composition["tracks"])), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "musical-brief.md").write_text(
            f"# Signal Garden - {level}\n\nSame D-Dorian theme, 100 BPM, 24 bars. Complexity target: `{level}`. "
            "Piano always carries the structural eight-tone theme; added events transform rather than replace it.\n",
            encoding="utf-8",
        )
    (DEMO / "README.md").write_text(
        "# Signal Garden complexity demo\n\nFive real renders of the same D-Dorian piano theme. "
        "Pitch identity, form, tempo, key, and main instrument remain fixed; rhythm, role count, ornamentation, interaction, and sectional density change.\n",
        encoding="utf-8",
    )
    print(f"[OK] Built five variants in {DEMO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
