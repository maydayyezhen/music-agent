from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from _bootstrap import ROOT
from src.composition import load_composition
from src.instruments import export_semantic_phrases
from src.validation import analyze_instrument_aware

BASE = ROOT / "projects" / "instrument_aware_demos"


def phrase(instrument: str, role: str, phrase_type: str, energy: float, seed: int, **extra: object) -> dict[str, object]:
    return {
        "instrument": instrument, "role": role, "phrase_type": phrase_type, "energy": energy,
        "performance_intent": {"attack": "intentional", "release": "phrase_shaped", "humanization": "action_based", "seed": seed},
        **extra,
    }


def harmony(chords: list[str], beats: int = 4) -> list[dict[str, object]]:
    return [{"at": f"{index + 1}:1", "duration": beats, "chord": chord} for index, chord in enumerate(chords)]


def clip(data: dict[str, object], bars: int, profile: str = "general_midi") -> dict[str, object]:
    return {"loop_bars": bars, "sound_library_profile": profile, "instrument_phrase": data}


def base(title: str, sections: list[dict[str, object]], tracks: dict[str, object], tempo: int = 100) -> dict[str, object]:
    return {
        "metadata": {"title": title, "tempo": tempo, "time_signature": "4/4", "key": "E minor"},
        "complexity": "standard", "complexity_contour": "custom", "sections": sections, "tracks": tracks,
    }


DEMOS: dict[str, dict[str, object]] = {
    "01_rhythm_guitar_palm_muted_verse": base(
        "Palm-Muted Verse Study", [{"name": "verse", "bars": 8}],
        {"rhythm_guitar": {"role": "electric rhythm guitar", "sound_library_profile": "general_midi", "sections": {
            "verse": clip(phrase("electric_rhythm_guitar", "rhythm", "palm_muted_eighths", 0.52, 101,
                                  harmony=harmony(["E5", "C5", "G5", "D5", "E5", "C5", "D5", "D5"]),
                                  subdivision=0.5, gate=0.42, strum_spread=0.045,
                                  rest_steps=[7, 15, 23, 31, 39, 47, 55, 63], articulations=["palm_mute"]), 8)}}}, 104),
    "02_open_power_chord_chorus": base(
        "Open Power Chorus Study", [{"name": "chorus", "bars": 8}],
        {"rhythm_guitar": {"role": "electric rhythm guitar", "sections": {
            "chorus": clip(phrase("electric_rhythm_guitar", "rhythm", "open_power_chords", 0.84, 102,
                                   harmony=harmony(["E5", "G5", "D5", "A5", "E5", "C5", "D5", "E5"]),
                                   subdivision=1.0, gate=0.82, strum_spread=0.07,
                                   rest_steps=[3, 11, 19, 27], articulations=["sustain", "accent"]), 8)}}}, 112),
    "03_lead_guitar_expression": base(
        "Lead Articulation Study", [{"name": "lead", "bars": 8}],
        {"lead_guitar": {"role": "electric lead guitar", "sections": {
            "lead": clip(phrase("electric_lead_guitar", "lead", "melodic_lead", 0.75, 103,
                                 motif=[
                                     {"at": "1:1", "pitch": "E4", "duration": 1.3, "articulations": ["sustain"]},
                                     {"at": "1:2.5", "pitch": "G4", "duration": 1.4, "articulations": ["hammer_on", "legato"]},
                                     {"at": "2:1", "pitch": "A4", "duration": 2.7, "articulations": ["bend", "vibrato"], "bend_semitones": 2},
                                     {"at": "3:1", "pitch": "B4", "duration": 0.8, "articulations": ["slide", "legato"]},
                                     {"at": "3:2", "pitch": "D5", "duration": 0.8, "articulations": ["pull_off", "legato"]},
                                     {"at": "3:3", "pitch": "B4", "duration": 1.6, "articulations": ["sustain"]},
                                     {"at": "5:1", "pitch": "G4", "duration": 0.7, "articulations": ["hammer_on"]},
                                     {"at": "5:2", "pitch": "A4", "duration": 0.7, "articulations": ["hammer_on"]},
                                     {"at": "5:3", "pitch": "B4", "duration": 2.2, "articulations": ["bend_release", "vibrato"], "bend_semitones": 2},
                                     {"at": "7:1", "pitch": "D5", "duration": 0.6, "articulations": ["slide"]},
                                     {"at": "7:2", "pitch": "B4", "duration": 0.8, "articulations": ["pull_off"]},
                                     {"at": "7:3", "pitch": "E5", "duration": 4.5, "articulations": ["sustain", "vibrato"]}
                                 ]), 8)}}}, 92),
    "04_bass_locked_with_kick": base(
        "Bass and Kick Study", [{"name": "groove", "bars": 8}],
        {
            "bass": {"role": "electric bass", "sections": {"groove": clip(phrase(
                "electric_bass", "bass", "kick_locked_line", 0.66, 104,
                harmony=harmony(["E5", "C5", "G5", "D5", "E5", "C5", "D5", "E5"]),
                kick_offsets=[0, 2], articulations=["finger"]), 8)}},
            "drums": {"role": "drum kit", "sections": {"groove": clip(phrase(
                "drum_kit", "drums", "rock_verse", 0.58, 105, bars=8, transition_fill=False), 8)}}
        }, 108),
    "05_verse_chorus_drums": base(
        "Verse Chorus Drum Study", [{"name": "verse", "bars": 8}, {"name": "chorus", "bars": 8}],
        {"drums": {"role": "drum kit", "sections": {
            "verse": clip(phrase("drum_kit", "drums", "rock_verse", 0.45, 106, bars=8, transition_fill=True), 8),
            "chorus": clip(phrase("drum_kit", "drums", "chorus_with_fill", 0.86, 107, bars=8, transition_fill=True), 8)
        }}}, 116),
    "06_keyboard_voice_leading": base(
        "Keyboard Voice-Leading Study", [{"name": "progression", "bars": 8}],
        {"piano": {"role": "piano harmony", "sections": {"progression": clip(phrase(
            "piano", "harmony", "piano_voice_led_chords", 0.48, 108,
            harmony=harmony(["C", "G", "Am", "F", "C", "G", "Dm", "G"]),
            register_midi=[55, 79], voices=4, pedal=True, articulations=["tenuto"]), 8)}}}, 88),
    "07_strings_inner_movement": base(
        "Strings Inner-Movement Study", [{"name": "arc", "bars": 8}],
        {"strings": {"role": "string ensemble", "sections": {"arc": clip(phrase(
            "strings", "plane", "long_tones_inner_movement", 0.55, 109,
            harmony=harmony(["Em", "C", "G", "D", "Em", "C", "Am", "B"]),
            register_midi=[55, 83], voices=4, articulations=["sustain", "legato"]), 8)}}}, 76),
}

INSTRUMENTS = {
    "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29},
    "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30},
    "bass": {"engine": "fluidsynth", "bank": 0, "program": 33},
    "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16},
    "piano": {"engine": "fluidsynth", "bank": 0, "program": 0},
    "strings": {"engine": "fluidsynth", "bank": 0, "program": 48},
}


def render_config(track_names: list[str]) -> dict[str, object]:
    pans = {"rhythm_guitar": -0.25, "lead_guitar": 0.05, "bass": 0, "drums": 0, "piano": 0, "strings": 0}
    volumes = {"rhythm_guitar": -3, "lead_guitar": -2, "bass": -2, "drums": -5, "piano": -3, "strings": -2}
    return {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.7,
            "tail_seconds": 2.0, "master_peak_db": -1.0,
            "mix": {name: {"volume_db": volumes.get(name, -3), "pan": pans.get(name, 0), "mute": False} for name in track_names}}


def main() -> int:
    BASE.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for name, composition in DEMOS.items():
        folder = BASE / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "composition.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "instruments.json").write_text(json.dumps({key: INSTRUMENTS[key] for key in composition["tracks"]}, indent=2) + "\n", encoding="utf-8")
        (folder / "render.json").write_text(json.dumps(render_config(list(composition["tracks"])), indent=2) + "\n", encoding="utf-8")
        loaded = load_composition(folder / "composition.json")
        (folder / "semantic_phrases.json").write_text(json.dumps(export_semantic_phrases(loaded), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report = analyze_instrument_aware(loaded)
        (folder / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "README.md").write_text(
            f"# {composition['metadata']['title']}\n\n"
            f"Instrument-aware minimum demo `{name}`. Source intent is in `composition.json`; the extracted semantic layer is `semantic_phrases.json`; `validation-report.json` contains musical/playability diagnostics. General MIDI is an explicit articulation fallback for the real FluidSynth render.\n",
            encoding="utf-8",
        )
        relative = folder.relative_to(ROOT / "projects").as_posix()
        completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_song.py"), relative], cwd=ROOT)
        if completed.returncode or report["error_count"]:
            failures.append(f"{name}: render={completed.returncode}, validation_errors={report['error_count']}")
        else:
            shutil.copy2(folder / "output" / "mix.wav", folder / "output" / "final.wav")
        print(f"{name}: errors={report['error_count']} warnings={report['warning_count']} render={completed.returncode}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
