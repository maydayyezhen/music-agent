from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SECTIONS = [
    ("Narthex", 4),
    ("Invocation", 8),
    ("Procession", 8),
    ("Sanctus", 8),
    ("Great Amen", 10),
    ("Benediction", 8),
]

PROGRESSIONS = {
    "Narthex": ["Dm", "Bb", "Gm", "A"],
    "Invocation": ["Dm", "C", "Bb", "A", "Dm", "F", "Gm", "A"],
    "Procession": ["Dm", "Bb", "F", "C", "Gm", "DmA", "Bb", "A"],
    "Sanctus": ["Bb", "C", "Dm", "A", "Bb", "F", "Gm", "A"],
    "Great Amen": ["Dm", "C", "Bb", "F", "Gm", "DmA", "Bb", "C", "A", "Dm"],
    "Benediction": ["Bb", "F", "C", "Dm", "Gm", "DmA", "A", "Dm"],
}

CHORDS = {
    "Dm": ["D3", "A3", "D4", "F4"],
    "C": ["C3", "G3", "C4", "E4"],
    "Bb": ["Bb2", "F3", "Bb3", "D4"],
    "A": ["A2", "E3", "A3", "C#4"],
    "F": ["F2", "C3", "A3", "F4"],
    "Gm": ["G2", "D3", "G3", "Bb3"],
    "DmA": ["A2", "D3", "A3", "F4"],
}

ROOTS = {"Dm": "D2", "C": "C2", "Bb": "Bb1", "A": "A1", "F": "F1", "Gm": "G1", "DmA": "A1"}
FIFTHS = {"Dm": "A2", "C": "G2", "Bb": "F2", "A": "E2", "F": "C2", "Gm": "D2", "DmA": "D2"}
APPROACH = {"Dm": "C#2", "C": "B1", "Bb": "A1", "A": "G#1", "F": "E1", "Gm": "F#1", "DmA": "G#1"}


def write_json(name: str, data: object) -> None:
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def note(bar: int, beat: float, pitch: str, duration: float, velocity: int) -> dict:
    return {"type": "note", "at": f"{bar}:{beat:g}", "pitch": pitch, "duration": duration, "velocity": velocity}


def chord(bar: int, pitches: list[str], duration: float, velocity: int, beat: float = 1) -> dict:
    return {"type": "chord", "at": f"{bar}:{beat:g}", "pitches": pitches, "duration": duration, "velocity": velocity}


def drumless_point(bar: int, pitch: str, velocity: int) -> dict:
    return note(bar, 1, pitch, 1.2, velocity)


def clip(bars: int, events: list[dict], texture: str | None = None, motif: str | None = None, variation: str = "A") -> dict:
    result = {"loop_bars": bars, "events": events}
    if texture:
        result["texture"] = texture
    if motif:
        result["rhythm_motif"] = motif
        result["rhythm_variation"] = variation
    return result


def organ_events(section: str, v2: bool) -> list[dict]:
    events = []
    for bar, symbol in enumerate(PROGRESSIONS[section], 1):
        pitches = CHORDS[symbol]
        # v2 opens the final Amen by moving the top voice upward while retaining inner tones.
        if v2 and section == "Great Amen" and bar in {8, 9, 10}:
            pitches = {
                8: ["C3", "G3", "E4", "G4"],
                9: ["A2", "E3", "C#4", "A4"],
                10: ["D3", "A3", "F4", "D5"],
            }[bar]
        velocity = 50 if section in {"Narthex", "Benediction"} else (61 if section == "Great Amen" else 55)
        events.append(chord(bar, pitches, 3.92, velocity))
    return events


def bass_events(section: str, v2: bool) -> list[dict]:
    events = []
    progression = PROGRESSIONS[section]
    for bar, symbol in enumerate(progression, 1):
        base = 56 if section == "Benediction" else (67 if section == "Great Amen" else 61)
        events.append(note(bar, 1, ROOTS[symbol], 2.4 if bar % 2 else 1.9, base + (bar % 3)))
        events.append(note(bar, 3 if bar % 2 == 0 else 3.5, FIFTHS[symbol], 0.85 if bar % 2 == 0 else 0.45, base - 5))
        if bar < len(progression) and (bar % 2 == 0 or section == "Great Amen"):
            next_symbol = progression[bar]
            events.append(note(bar, 4, APPROACH[next_symbol], 0.78, base - 8))
    if v2 and section == "Benediction":
        # Let the last cadence breathe instead of walking through it.
        events = [event for event in events if not (event["at"].startswith("7:4") or event["at"].startswith("8:3"))]
    return events


def lead_phrase(start_bar: int, pitches: list[str], velocity: int, variant: int = 0) -> list[dict]:
    rhythms = [
        [(1, 1, 1.45), (1, 2.5, 0.45), (1, 3, 0.92), (2, 1, 1.9), (2, 3, 0.92), (2, 4, 0.72)],
        [(1, 1, 0.92), (1, 2, 0.92), (1, 3, 1.75), (2, 1, 1.45), (2, 2.5, 0.45), (2, 3, 1.68)],
        [(1, 1, 1.9), (1, 3, 0.92), (1, 4, 0.72), (2, 1, 0.92), (2, 2, 1.9), (2, 4, 0.72)],
    ][variant % 3]
    return [note(start_bar + rel_bar - 1, beat, pitch, duration, velocity + (i % 3) * 2) for i, ((rel_bar, beat, duration), pitch) in enumerate(zip(rhythms, pitches))]


def lead_events(section: str, v2: bool) -> list[dict]:
    if section == "Narthex":
        return [note(3, 1, "D4", 2.7, 55), note(3, 4, "F4", 0.72, 58), note(4, 1, "E4", 1.45, 56), note(4, 3, "D4", 1.75, 60)]
    phrase_sets = {
        "Invocation": [
            ["D4", "F4", "G4", "A4", "G4", "F4"],
            ["E4", "F4", "A4", "G4", "F4", "E4"],
            ["D4", "F4", "G4", "A4", "C5", "A4"],
            ["Bb4", "A4", "G4", "E4", "C#4", "D4"],
        ],
        "Procession": [
            ["D4", "F4", "A4", "Bb4", "A4", "F4"],
            ["F4", "A4", "C5", "Bb4", "A4", "G4"],
            ["G4", "Bb4", "D5", "C5", "A4", "F4"],
            ["Bb4", "A4", "G4", "E4", "C#4", "D4"],
        ],
        "Sanctus": [
            ["F4", "Bb4", "C5", "D5", "C5", "Bb4"],
            ["A4", "C5", "D5", "E5", "D5", "C#5"],
            ["Bb4", "D5", "F5", "E5", "D5", "C5"],
            ["Bb4", "A4", "G4", "E4", "C#4", "D4"],
        ],
        "Great Amen": [
            ["D4", "F4", "A4", "D5", "C5", "A4"],
            ["F4", "A4", "C5", "F5", "E5", "C5"],
            ["G4", "Bb4", "D5", "F5", "E5", "D5"],
            ["Bb4", "D5", "F5", "G5", "F5", "E5"],
            ["A4", "C#5", "E5", "A5", "F5", "D5"],
        ],
        "Benediction": [
            ["F4", "Bb4", "A4", "F4", "G4", "A4"],
            ["G4", "A4", "C5", "A4", "F4", "D4"],
            ["G4", "Bb4", "A4", "F4", "E4", "D4"],
            ["E4", "F4", "E4", "C#4", "D4", "D4"],
        ],
    }
    result = []
    for i, pitches in enumerate(phrase_sets[section]):
        velocity = 66 + (4 if section == "Procession" else 0) + (10 if section == "Sanctus" else 0) + (14 if section == "Great Amen" else 0) - (7 if section == "Benediction" else 0)
        result.extend(lead_phrase(i * 2 + 1, pitches, velocity, i))
    if v2 and section == "Great Amen":
        # Strengthen the arrival: delay the summit to bar 8 and give it room.
        result = [event for event in result if not event["at"].startswith("8:")]
        result.extend([note(8, 1, "D5", 1.45, 91), note(8, 2.5, "F5", 0.45, 94), note(8, 3, "G5", 1.72, 98)])
    if v2 and section == "Benediction":
        result = [event for event in result if not event["at"].startswith("8:")]
        result.append(note(8, 1, "D4", 3.55, 58))
    return result


def ooh_events(section: str, v2: bool) -> list[dict]:
    if section == "Narthex":
        return []
    events = []
    progression = PROGRESSIONS[section]
    for bar, symbol in enumerate(progression, 1):
        # Two connected inner voices; attacks are offset from the main theme.
        source = CHORDS[symbol]
        pitches = [source[1], source[2]]
        duration = 3.72
        velocity = 48 if section == "Benediction" else (62 if section in {"Sanctus", "Great Amen"} else 53)
        events.append(chord(bar, pitches, duration, velocity, beat=1.15 if bar % 2 else 1))
    if v2 and section == "Invocation":
        # Reduce masking by withholding inner choir from the opening two bars.
        events = [event for event in events if int(event["at"].split(":")[0]) > 2]
    return events


def strings_events(section: str, v2: bool) -> list[dict]:
    if section in {"Narthex", "Invocation"}:
        return []
    contours = {
        "Procession": ["A3", "Bb3", "A3", "G3", "Bb3", "A3", "G3", "E3"],
        "Sanctus": ["D4", "E4", "F4", "E4", "D4", "C4", "Bb3", "C#4"],
        "Great Amen": ["F3", "E3", "D3", "C3", "D3", "F3", "G3", "A3", "C#4", "D4"],
        "Benediction": ["D4", "C4", "G3", "A3", "Bb3", "A3", "G3", "F3"],
    }[section]
    events = []
    for bar, pitch in enumerate(contours, 1):
        vel = 47 if section == "Benediction" else (61 if section == "Great Amen" else 54)
        start_beat = 1.5 if bar % 2 else 1
        # Even-bar notes cross into the following delayed (beat 1.5) entry,
        # creating a true cantabile line rather than isolated swells.
        duration = (3.15 if bar % 2 else 4.55) if v2 else (2.25 if bar % 2 else 2.85)
        if v2 and section == "Great Amen" and bar == len(contours):
            duration = 4.48  # release just before Benediction's delayed D4 entrance
        events.append(note(bar, start_beat, pitch, duration, vel + bar % 3))
        if bar % 3 == 0 and bar < len(contours) and contours[bar] != pitch and not (v2 and section == "Great Amen" and bar == 9):
            events.append(note(bar, 3.5, contours[bar], 1.25, vel - 4))
    if v2 and section == "Great Amen":
        events.extend([note(8, 3.5, "Bb3", 1.2, 64)])
    return events


def bells_events(section: str, v2: bool) -> list[dict]:
    points = {
        "Narthex": [(1, "D5"), (4, "A5")],
        "Invocation": [(1, "D5"), (5, "A5"), (8, "E5")],
        "Procession": [(1, "D5"), (4, "C5"), (8, "A5")],
        "Sanctus": [(1, "Bb5"), (3, "D6"), (5, "F5"), (8, "E5")],
        "Great Amen": [(1, "D5"), (3, "F5"), (5, "G5"), (7, "Bb5"), (9, "A5"), (10, "D6")],
        "Benediction": [(1, "Bb5"), (4, "D5"), (8, "D6")],
    }[section]
    if v2:
        # v1's bells were too regular; v2 keeps only structural portals and the final blessing.
        keep = {"Narthex": {1, 4}, "Invocation": {1, 8}, "Procession": {1, 8}, "Sanctus": {1, 5}, "Great Amen": {1, 7, 10}, "Benediction": {1, 8}}[section]
        points = [item for item in points if item[0] in keep]
    base = 56 if section == "Benediction" else 64
    return [drumless_point(bar, pitch, base + (bar % 4) * 2) for bar, pitch in points]


def build(v2: bool) -> dict:
    section_objs = []
    energy = {"Narthex": 2, "Invocation": 4, "Procession": 6, "Sanctus": 8, "Great Amen": 10, "Benediction": 3}
    budgets = {
        "Narthex": {"lead": 2, "harmony": 3, "point": 1},
        "Invocation": {"lead": 4, "harmony": 3, "bass": 2},
        "Procession": {"lead": 4, "harmony": 3, "counterline": 2, "bass": 1, "point": 1},
        "Sanctus": {"lead": 5, "harmony": 4, "counterline": 3, "bass": 2, "point": 1},
        "Great Amen": {"lead": 5, "harmony": 4, "counterline": 4, "bass": 2},
        "Benediction": {"lead": 3, "harmony": 2, "counterline": 1, "bass": 1, "point": 1},
    }
    for name, bars in SECTIONS:
        level = "simple" if name in {"Narthex", "Benediction"} else ("rich" if name in {"Sanctus", "Great Amen"} else "standard")
        section_objs.append({"name": name, "bars": bars, "energy": energy[name], "complexity": {"level": level, "density": 2 if name == "Narthex" else 3}, "complexity_budget": budgets[name]})
    tracks = {
        "choir_theme": {"role": "main lead melody / sacred theme", "texture": "counterline", "continuity": {"sustain_ratio": 0.62, "legato_ratio": 0.7, "overlap": 0.02, "common_tone_retention": 0.7, "voice_leading_strength": 0.85}, "sections": {}},
        "choir_inner": {"role": "inner choral harmony plane", "texture": "sustain", "continuity": {"sustain_ratio": 0.9, "legato_ratio": 0.88, "overlap": 0.04, "common_tone_retention": 0.9, "voice_leading_strength": 0.92}, "sections": {}},
        "pipe_organ": {"role": "cathedral harmonic plane", "texture": "sustain", "continuity": {"sustain_ratio": 0.95, "legato_ratio": 0.92, "overlap": 0.0, "common_tone_retention": 0.94, "voice_leading_strength": 0.95}, "sections": {}},
        "double_bass": {"role": "independent sacred bass line", "texture": "counterline", "continuity": {"sustain_ratio": 0.55, "legato_ratio": 0.54, "overlap": 0.01, "common_tone_retention": 0.4, "voice_leading_strength": 0.8}, "sections": {}},
        "slow_strings": {"role": "independent counterline and swell", "texture": "counterline", "continuity": {"sustain_ratio": 0.65, "legato_ratio": 0.72, "overlap": 0.03, "common_tone_retention": 0.72, "voice_leading_strength": 0.86}, "sections": {}},
        "bell_tower": {"role": "ceremonial point accents", "texture": "stab", "sections": {}},
    }
    for name, bars in SECTIONS:
        tracks["choir_theme"]["sections"][name] = clip(bars, lead_events(name, v2), "counterline", "plainchant_cell", "B'" if name in {"Sanctus", "Great Amen"} else "A")
        if ooh_events(name, v2): tracks["choir_inner"]["sections"][name] = clip(bars, ooh_events(name, v2), "sustain")
        tracks["pipe_organ"]["sections"][name] = clip(bars, organ_events(name, v2), "sustain")
        if name != "Narthex": tracks["double_bass"]["sections"][name] = clip(bars, bass_events(name, v2), "counterline")
        if strings_events(name, v2): tracks["slow_strings"]["sections"][name] = clip(bars, strings_events(name, v2), "counterline")
        tracks["bell_tower"]["sections"][name] = clip(bars, bells_events(name, v2), "stab")
    return {
        "metadata": {"title": "Lux in Absidis (Light in the Apse)", "tempo": 84, "time_signature": "4/4", "key": "D minor", "composer_note": "Original instrumental church-choir work; choir presets are wordless instruments."},
        "complexity": {"level": "standard", "rhythm": 2, "harmony": 4, "arrangement": 4, "melodic_ornamentation": 2, "density": 3, "variation": 4},
        "complexity_contour": "sparse_to_climax",
        "rhythm_motifs": {"plainchant_cell": [{"offset": 0, "duration": 1.5}, {"offset": 1.5, "duration": 0.5}, {"offset": 2, "duration": 1}, {"offset": 4, "duration": 2}, {"offset": 6, "duration": 1}, {"offset": 7, "duration": 0.75}], "bass_breath": [{"offset": 0, "duration": 2.4}, {"offset": 2.5, "duration": 0.45}, {"offset": 3, "duration": 0.8}]},
        "sections": section_objs,
        "tracks": tracks,
    }


def write_planning_files() -> None:
    (HERE / "musical-brief.md").write_text("""# Musical Brief — Lux in Absidis

- Genre: instrumental church-choir / sacred cinematic miniature; no lyrics and no vocals workflow.
- Emotional target: begin in shadowed stone, gather into a solemn procession, open into a radiant but controlled Great Amen, then recede into a blessing.
- Tonality: D minor with brief Dorian/modal light; functional cadences use A major/C-sharp.
- Tempo and meter: 84 BPM, 4/4.
- Length: 46 bars; 131.43 seconds of score plus about 3 seconds of natural render tail.
- Core motif: long–short–held chant cell (1.5, 0.5, 1.0 | 2.0, 1.0, 0.75 beats), initially D–F–G | A–G–F.
- Harmony: Dm-centred, plagal colour from Bb/F/Gm, dominant A for sacred cadential gravity.
- Instrumentation: Concert Choir (main wordless theme), Voice Oohs (inner choral plane), Pipe Organ 2, Slow Strings, Double Bass, Bell Tower.
- Exclusions: no lyrics, no vocals.json, no drums, no pop groove, no rapid ostinato wall, no claim that choir presets pronounce words.
- Complexity: standard overall; rhythm 2, harmony 4, arrangement 4, ornamentation 2, density 3, variation 4; sparse-to-climax contour. Richness comes from voicing, register and role exchange rather than busy subdivisions.
""", encoding="utf-8")
    (HERE / "energy-map.md").write_text("""# Energy Map

| Section | Bars | Energy | Point / Line / Plane | Entrances, register, tension and transition |
|---|---:|---:|---|---|
| Narthex | 4 | 2 | Bell / late choir / organ | Empty low-mid organ vault; two bell portals; theme appears only in bars 3–4; A-major threshold. |
| Invocation | 8 | 4 | Sparse bell / theme+bass / organ+inner choir | Theme establishes chant cell in D4–C5; bass approaches cadences; inner choir remains restrained. |
| Procession | 8 | 6 | Bell / theme+bass+strings / organ+inner choir | Strings enter as independent contrary line; wider register and clearer forward motion. |
| Sanctus | 8 | 8 | Ceremonial bell / high theme+counterlines / organ+choir plane | Theme rises to F5; dominant tension is stronger; choral width expands. |
| Great Amen | 10 | 10 | Structural bells / summit theme+bass+strings / full organ+inner choir | Longest span; delayed A5 summit; final D-major-like radiance is avoided—resolution remains solemn D minor. |
| Benediction | 8 | 3 | Entrance/final bell / descending theme+strings+bass / soft organ+inner choir | Register and velocities fall; bass yields at final cadence; last D is held into the room. |

Silence is structural: no bass/strings/inner choir at the opening, strings wait until Procession, bells never become a pulse, and the final cadence sheds moving detail.
""", encoding="utf-8")
    (HERE / "instrument-notes.md").write_text("""# Instrument Notes

| Track | Role | Rhythmic identity | Texture / continuity | Planned silence |
|---|---|---|---|---|
| choir_theme | unmistakable main theme | long–short chant cell, two-bar question/answer, phrase-end breath | Line; connected but articulated, rising only at earned climaxes | enters late in Narthex; breath after every two-bar phrase |
| choir_inner | alto/tenor-like harmonic support | one broad attack per bar, slightly displaced on alternating bars | Plane; sustained close inner voices, smooth common-tone motion | absent throughout Narthex; v2 may withhold opening Invocation |
| pipe_organ | cathedral harmonic foundation | one long voiced span per bar | Plane; 3.92-beat chords, restrained attacks, smooth inversions | always present by design, but low in the mix |
| double_bass | independent foundation | held roots, fifth answers, semitone approaches, occasional release | Line; mixed durations and destination-led motion | absent in Narthex and simplified at closing cadence |
| slow_strings | counter-motion and swell | long notes beginning on beat 1 or 1.5, occasional approach | Line/soft plane; does not duplicate organ blocks | absent through Narthex and Invocation |
| bell_tower | architectural punctuation | isolated downbeat tolls only | Point; long-decay accents at thresholds | most bars; density reduced further in final revision |

SoundFont presets are treated as ordinary lyricless instruments. Spatial character comes from sustained writing, overlapping natural decays, register, restrained dynamics, and the SoundFont renderer's room/reverb behaviour.
""", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", choices=["v1", "v2"])
    args = parser.parse_args()
    HERE.mkdir(parents=True, exist_ok=True)
    write_planning_files()
    composition = build(args.version == "v2")
    version_name = "composition_v2.json" if args.version == "v2" else "composition_v1.json"
    write_json(version_name, composition)
    write_json("composition.json", composition)
    if args.version == "v1":
        write_json("instruments.json", {
            "choir_theme": {"engine": "fluidsynth", "bank": 0, "program": 52, "gm_name": "Concert Choir"},
            "choir_inner": {"engine": "fluidsynth", "bank": 0, "program": 53, "gm_name": "Voice Oohs"},
            "pipe_organ": {"engine": "fluidsynth", "bank": 8, "program": 19, "gm_name": "Pipe Organ 2"},
            "double_bass": {"engine": "fluidsynth", "bank": 0, "program": 43, "gm_name": "Double Bass"},
            "slow_strings": {"engine": "fluidsynth", "bank": 0, "program": 49, "gm_name": "Slow Strings"},
            "bell_tower": {"engine": "fluidsynth", "bank": 11, "program": 14, "gm_name": "Bell Tower"},
        })
        write_json("render.json", {
            "sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.58, "tail_seconds": 3.0, "master_peak_db": -1.0,
            "mix": {
                "choir_theme": {"volume_db": -2.5, "pan": -0.08, "mute": False},
                "choir_inner": {"volume_db": -8.0, "pan": 0.15, "mute": False},
                "pipe_organ": {"volume_db": -8.5, "pan": 0.0, "mute": False},
                "double_bass": {"volume_db": -7.0, "pan": 0.0, "mute": False},
                "slow_strings": {"volume_db": -8.5, "pan": -0.22, "mute": False},
                "bell_tower": {"volume_db": -11.5, "pan": 0.25, "mute": False},
            },
        })


if __name__ == "__main__":
    main()
