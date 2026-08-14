from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPO = 124
SECTIONS = [
    ("intro", 4, 3),
    ("long_verse", 12, 5),
    ("lift", 8, 7),
    ("first_chorus", 12, 8),
    ("instrumental_run", 8, 7),
    ("final_chorus", 16, 9),
    ("outro", 4, 4),
]
PROGRESSIONS = {
    "intro": ["Bm", "G", "D", "A"],
    "long_verse": ["Bm", "G", "D", "A"] * 3,
    "lift": ["Em", "G", "D", "A", "Em", "G", "A", "A"],
    "first_chorus": ["G", "D", "A", "Bm", "G", "D", "Em", "A", "G", "D", "A", "A"],
    "instrumental_run": ["Bm", "A", "G", "D", "Em", "G", "A", "A"],
    "final_chorus": ["G", "D", "A", "Bm", "G", "D", "Em", "A"] * 2,
    "outro": ["G", "A", "Bm", "Bm"],
}
ROOTS = {"Bm": "B1", "G": "G1", "D": "D2", "A": "A1", "Em": "E2"}
FIFTHS = {"Bm": "F#2", "G": "D2", "D": "A2", "A": "E2", "Em": "B2"}
OCTAVES = {"Bm": "B2", "G": "G2", "D": "D3", "A": "A2", "Em": "E3"}
PAD = {
    "Bm": ["B3", "D4", "F#4"], "G": ["G3", "B3", "D4"], "D": ["A3", "D4", "F#4"],
    "A": ["A3", "C#4", "E4"], "Em": ["G3", "B3", "E4"],
}


def write_json(name: str, value) -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def event(pitch: str, bar: int, beat: float, duration: float, velocity: int, **extra):
    return {"at": f"{bar}:{beat:g}", "duration": duration, "pitch": pitch, "velocity": velocity, **extra}


def harmony(section: str):
    return [{"at": f"{bar}:1", "duration": 4, "chord": chord}
            for bar, chord in enumerate(PROGRESSIONS[section], 1)]


def guitar_phrase(instrument: str, section: str, bars: int, revision: str):
    acoustic = instrument == "acoustic_guitar"
    if acoustic:
        if section in {"first_chorus", "final_chorus"}:
            patterns = ["chorus_open"]
        elif section == "lift":
            patterns = ["steady_eighths", "chorus_open"]
        else:
            patterns = ["steady_eighths"]
    elif revision == "v1":
        patterns = ["steady_eighths"]
    elif section in {"long_verse", "first_chorus", "final_chorus"}:
        patterns = ["classic_pop"]
    elif section == "instrumental_run":
        patterns = ["bass_continuous"]
    else:
        patterns = ["steady_eighths"]
    energy = {name: score / 10 for name, _, score in SECTIONS}[section]
    return {
        "instrument": instrument,
        "role": f"{section} long uninterrupted {'acoustic' if acoustic else 'electric'} strumming",
        "section_function": section,
        "phrase_type": "continuous_strumming",
        "energy": energy,
        "harmony": harmony(section),
        "strumming_patterns": patterns,
        "palm_mute": not acoustic and section in {"long_verse", "lift"},
        "gate": .86 if acoustic else (.62 if section in {"long_verse", "lift"} else .74),
        "strum_spread": .05 if acoustic else .04,
        "performance_intent": {
            "picking": "alternate",
            "attack": "continuous broad motion" if acoustic else "controlled power-strum drive",
            "release": "connected across barlines",
            "seed": 6400 + sum(ord(char) for char in instrument + section) + (1 if revision == "v2" else 0),
        },
    }


def organ_events(section: str, bars: int, revision: str):
    result = []
    if section == "intro":
        for bar, pitches in [(3, ["F#4", "A4", "D5"]), (4, ["E4", "F#4", "A4"])]:
            for index, pitch in enumerate(pitches):
                result.append(event(pitch, bar, 1 + index, .72, 60 + index * 4, _motif="rising-light"))
        return result
    verse_cell = ["F#4", "B4", "A4", "F#4", "E4", "D4"]
    chorus_cell = ["B4", "A4", "F#4", "D5", "C#5", "B4"]
    run_cell = ["F#4", "A4", "B4", "D5", "C#5", "B4", "A4", "F#4"]
    for bar in range(1, bars + 1):
        cycle = (bar - 1) % 4
        if section == "long_verse":
            if cycle == 3:
                result.append(event("F#4" if bar < 9 else "A4", bar, 1, 2.75, 65, _motif="verse-release"))
            else:
                for index, pitch in enumerate(verse_cell[cycle * 2:cycle * 2 + 2]):
                    result.append(event(pitch, bar, 1.5 + index * 1.25, .82, 64 + index * 4, _motif="verse-answer"))
        elif section == "lift":
            pitches = ["E4", "F#4", "A4", "B4"] if bar <= 4 else ["F#4", "A4", "B4", "C#5"]
            for index, pitch in enumerate(pitches):
                result.append(event(pitch, bar, 1 + index * .75, .58, 66 + bar + index, _motif="lift-sequence"))
        elif section in {"first_chorus", "final_chorus"}:
            high = revision == "v2" and section == "final_chorus" and bar > 12
            pitches = chorus_cell[cycle:cycle + 3]
            if len(pitches) < 3:
                pitches += chorus_cell[:3 - len(pitches)]
            for index, pitch in enumerate(pitches):
                if high:
                    octave = int(pitch[-1]) + 1
                    pitch = pitch[:-1] + str(octave)
                result.append(event(pitch, bar, 1 + index * 1.25, .88 if index < 2 else 1.1,
                                    72 + index * 4 + (5 if high else 0), _motif="open-road-hook"))
        elif section == "instrumental_run":
            for index, pitch in enumerate(run_cell):
                if (bar + index) % 3:
                    result.append(event(pitch, bar, 1 + index * .375, .3, 68 + index % 4 * 3,
                                        _motif="running-counterline"))
        elif section == "outro":
            pitch = ["B4", "A4", "F#4", "B4"][bar - 1]
            result.append(event(pitch, bar, 1, 3.25 if bar == bars else 2.5, 62 - bar * 2, _motif="outro-return"))
    return result


def bass_events(section: str, bars: int):
    result = []
    chorus = "chorus" in section
    for bar, chord in enumerate(PROGRESSIONS[section], 1):
        pattern = [(1, ROOTS[chord], 1.2), (2.5, FIFTHS[chord], .72), (3.5, OCTAVES[chord], .4)]
        if chorus or section == "instrumental_run":
            pattern = [(1, ROOTS[chord], .72), (2, FIFTHS[chord], .66), (3, OCTAVES[chord], .66), (4, FIFTHS[chord], .42)]
        for index, (beat, pitch, duration) in enumerate(pattern):
            result.append(event(pitch, bar, beat, duration, 68 + index * 4 + (6 if chorus else 0), _bass_function="connected_drive"))
    return result


def drum(pitch: int, bar: int, beat: float, duration: float, velocity: int, **extra):
    return {"at": f"{bar}:{beat:g}", "duration": duration, "pitch": pitch, "velocity": velocity, **extra}


def drum_events(section: str, bars: int, revision: str):
    result = []
    chorus = "chorus" in section
    for bar in range(1, bars + 1):
        for step in range(8):
            cymbal = 42 if not chorus else 51
            if revision == "v2" and step == 7 and bar % 4 == 0:
                cymbal = 46
            phrase_shape = (bar % 4) * 2 if revision == "v2" else 0
            result.append(drum(cymbal, bar, 1 + step * .5, .1,
                               54 + (11 if step % 2 == 0 else 0) + (7 if chorus else 0) + phrase_shape,
                               _limb="right_hand"))
        for beat in [2, 4]:
            result.append(drum(38, bar, beat, .1, 84 + (8 if chorus else 0), _limb="left_hand"))
        kicks = [1, 3] if section == "intro" else ([1, 1.5, 3, 3.5] if chorus else [1, 2.5, 3.5])
        if revision == "v2" and section != "intro":
            phase = bar % 4
            non_chorus_kicks = {
                0: [1, 2.5, 3.5], 1: [1, 2, 3.5],
                2: [1, 1.5, 3], 3: [1, 2.5, 3, 3.5],
            }
            chorus_kicks = {
                0: [1, 1.5, 3, 3.5], 1: [1, 2.5, 3, 3.5],
                2: [1, 1.5, 2.5, 3.5], 3: [1, 2, 3, 3.5],
            }
            kicks = (chorus_kicks if chorus else non_chorus_kicks)[phase]
        for beat in kicks:
            result.append(drum(36, bar, beat, .1, 84 + (6 if chorus else 0), _limb="right_foot"))
        if bar == bars:
            for index, pitch in enumerate([45, 47, 50]):
                result.append(drum(pitch, bar, 3 + index * .33, .12, 76 + index * 5, _limb="fill"))
        if chorus and bar % 4 == 1:
            result.append(drum(49, bar, 1, .18, 96, _limb="right_hand", _boundary_crash=True))
    return result


def pad_events(section: str, bars: int):
    if section not in {"lift", "first_chorus", "final_chorus"}:
        return []
    result = []
    start = 5 if section == "lift" else 1
    for bar, chord in enumerate(PROGRESSIONS[section], 1):
        if bar < start:
            continue
        for index, pitch in enumerate(PAD[chord]):
            result.append(event(pitch, bar, 1, 3.82, 39 + index * 3 + (4 if "chorus" in section else 0), _role="harmonic_plane"))
    return result


def explicit_clip(events, bars):
    return {"loop_bars": bars, "events": events}


def semantic_clip(phrase, bars):
    return {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": phrase}


def build(revision: str):
    tracks = {
        "acoustic_guitar": {"role": "acoustic guitar uninterrupted right-hand engine", "sections": {}},
        "electric_rhythm_guitar": {"role": "electric rhythm guitar continuous power-strum counter-grid", "sections": {}},
        "drawbar_organ": {"role": "main melody lead instrument with deliberate rests", "sections": {}},
        "electric_bass": {"role": "connected bass line", "sections": {}},
        "drums": {"role": "pop rock propulsion and boundaries", "sections": {}},
        "orchestra_pad": {"role": "late harmonic plane", "sections": {}},
    }
    for section, bars, _ in SECTIONS:
        tracks["acoustic_guitar"]["sections"][section] = semantic_clip(guitar_phrase("acoustic_guitar", section, bars, revision), bars)
        if section != "intro":
            tracks["electric_rhythm_guitar"]["sections"][section] = semantic_clip(
                guitar_phrase("electric_rhythm_guitar", section, bars, revision), bars
            )
        tracks["drawbar_organ"]["sections"][section] = explicit_clip(organ_events(section, bars, revision), bars)
        tracks["electric_bass"]["sections"][section] = explicit_clip(bass_events(section, bars), bars)
        tracks["drums"]["sections"][section] = explicit_clip(drum_events(section, bars, revision), bars)
        pad = pad_events(section, bars)
        if pad:
            tracks["orchestra_pad"]["sections"][section] = explicit_clip(pad, bars)
    return {
        "metadata": {"title": "Hands Across the Highway", "tempo": TEMPO, "time_signature": "4/4",
                     "key": "D major / B minor", "seed": 64124, "stage": revision,
                     "vocal_rendering": "disabled; instrumental strumming stress test"},
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 3, "arrangement": 4,
                       "melodic_ornamentation": 2, "density": 4, "variation": 4},
        "complexity_contour": "gradual_build",
        "sections": [{"name": name, "bars": bars, "energy": energy,
                      "complexity_budget": ({"lead": 2, "acoustic": 4, "electric": 2, "rhythm": 2, "texture": 1}
                                            if energy <= 5 else
                                            {"lead": 3, "acoustic": 4, "electric": 3, "rhythm": 4, "texture": 1})}
                     for name, bars, energy in SECTIONS],
        "tracks": tracks,
    }


def write_config(revision: str):
    write_json("instruments.json", {
        "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25, "gm_name": "Steel Guitar"},
        "electric_rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29, "gm_name": "Overdrive Guitar"},
        "drawbar_organ": {"engine": "fluidsynth", "bank": 0, "program": 16, "gm_name": "Drawbar Organ"},
        "electric_bass": {"engine": "fluidsynth", "bank": 0, "program": 34, "gm_name": "Electric Bass (pick)"},
        "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16, "gm_name": "Power Drum Kit"},
        "orchestra_pad": {"engine": "fluidsynth", "bank": 8, "program": 48, "gm_name": "Orchestra Pad"},
    })
    write_json("render.json", {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
                                "fluidsynth_gain": .82, "tail_seconds": 2, "master_peak_db": -1,
                                "mix": {
                                    "acoustic_guitar": {"volume_db": 1.5, "pan": -.34, "mute": False},
                                    "electric_rhythm_guitar": {"volume_db": -2.4 if revision == "v2" else -1.8, "pan": .32, "mute": False},
                                    "drawbar_organ": {"volume_db": 1.0 if revision == "v2" else -1.5, "pan": .04, "mute": False},
                                    "electric_bass": {"volume_db": 2.5, "pan": 0, "mute": False},
                                    "drums": {"volume_db": 2.8, "pan": 0, "mute": False},
                                    "orchestra_pad": {"volume_db": -8, "pan": .12, "mute": False},
                                }})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", choices=["v1", "v2"], default="v1")
    args = parser.parse_args()
    composition = build(args.revision)
    write_json(f"composition_{args.revision}.json", composition)
    write_json("composition.json", composition)
    write_json("composition.normalized.json", composition)
    if args.revision == "v2":
        write_json("composition_final.json", composition)
    write_config(args.revision)
    print(f"Built {args.revision}: {sum(bars for _, bars, _ in SECTIONS)} bars at {TEMPO} BPM")


if __name__ == "__main__":
    main()
