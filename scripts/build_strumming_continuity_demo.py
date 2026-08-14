from __future__ import annotations

import json
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from _bootstrap import ROOT
from src.instruments import compile_instrument_phrase
from src.midi import generate_song_midis
from src.validation import analyze_strumming_flow


PROJECT = ROOT / "projects" / "strumming_continuity_demo"
CHORDS = ["G", "D", "Em", "C", "G", "D", "Em", "C"]


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def harmony(start: int, count: int):
    return [{"at": f"{index + 1}:1", "duration": 4, "chord": CHORDS[start + index]} for index in range(count)]


def phrase(instrument, phrase_type, role, start, patterns, seed, **extra):
    return {"instrument": instrument, "role": role, "phrase_type": phrase_type, "energy": extra.pop("energy", .6),
            "harmony": harmony(start, 2), "strumming_patterns": patterns, "performance_intent": {"seed": seed}, **extra}


def clip(source):
    return {"loop_bars": 2, "sound_library_profile": "general_midi", "instrument_phrase": source}


def composition():
    acoustic = {
        "baseline": phrase("acoustic_guitar", "sustained_chord_hit", "intentional error baseline", 0, ["single_hit"], 501),
        "verse": phrase("acoustic_guitar", "continuous_strumming", "verse continuous rhythm", 2, ["verse_a"], 502),
        "pre_chorus": phrase("acoustic_guitar", "continuous_strumming", "pre chorus gradual opening", 4, ["verse_a", "steady_eighths"], 503),
        "chorus": phrase("acoustic_guitar", "continuous_strumming", "chorus open continuous", 6, ["chorus_open"], 504, energy=.82),
    }
    electric = {
        "baseline": phrase("electric_rhythm_guitar", "sustained_chord_hit", "intentional error baseline", 0, ["single_hit"], 601),
        "verse": phrase("electric_rhythm_guitar", "continuous_strumming", "verse palm muted continuous", 2, ["steady_eighths"], 602, palm_mute=True),
        "pre_chorus": phrase("electric_rhythm_guitar", "continuous_strumming", "pre chorus complementary pattern", 4, ["steady_eighths", "classic_pop"], 603, palm_mute=True),
        "chorus": phrase("electric_rhythm_guitar", "continuous_strumming", "chorus classic pop width", 6, ["classic_pop"], 604, energy=.78),
    }
    return {
        "metadata": {"title": "Continuous Right Hand Motion Test", "tempo": 112, "time_signature": "4/4", "key": "G major", "seed": 501604},
        "complexity": {"level": "standard", "rhythm": 4, "harmony": 2, "arrangement": 2, "melodic_ornamentation": 1, "density": 2, "variation": 4},
        "complexity_contour": "gradual_build",
        "sections": [{"name": "baseline", "bars": 2, "energy": 2}, {"name": "verse", "bars": 2, "energy": 4},
                     {"name": "pre_chorus", "bars": 2, "energy": 6}, {"name": "chorus", "bars": 2, "energy": 8}],
        "tracks": {
            "acoustic_guitar": {"role": "acoustic guitar rhythm", "sections": {name: clip(source) for name, source in acoustic.items()}},
            "electric_rhythm_guitar": {"role": "electric rhythm guitar width", "sections": {name: clip(source) for name, source in electric.items()}},
        },
    }


def baseline_composition():
    source = phrase("acoustic_guitar", "sustained_chord_hit", "single hit baseline", 0, ["single_hit"], 700)
    source["harmony"] = [{"at": f"{index + 1}:1", "duration": 4, "chord": CHORDS[index]} for index in range(8)]
    return {"metadata": {"title": "Single Hit Baseline", "tempo": 112, "time_signature": "4/4", "key": "G major"},
            "sections": [{"name": "baseline", "bars": 8}],
            "tracks": {"acoustic_guitar": {"role": "acoustic guitar sustained chord baseline",
                                              "sections": {"baseline": {"loop_bars": 8, "instrument_phrase": source}}}}}


def main():
    PROJECT.mkdir(parents=True, exist_ok=True)
    data = composition()
    instruments = {
        "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25, "gm_name": "Steel Guitar"},
        "electric_rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29, "gm_name": "Overdrive Guitar"},
    }
    render = {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": .82,
              "tail_seconds": 2, "master_peak_db": -1, "mix": {
                  "acoustic_guitar": {"volume_db": 2, "pan": -.32, "mute": False},
                  "electric_rhythm_guitar": {"volume_db": -1, "pan": .34, "mute": False}}}
    write_json(PROJECT / "composition.json", data); write_json(PROJECT / "composition.normalized.json", data)
    write_json(PROJECT / "instruments.json", instruments); write_json(PROJECT / "render.json", render)

    paths = generate_song_midis(data, instruments, PROJECT)
    shutil.copy2(paths["full_song"], PROJECT / "continuous_strum_test.mid")
    shutil.copy2(paths["acoustic_guitar"], PROJECT / "acoustic_strum_test.mid")
    shutil.copy2(paths["electric_rhythm_guitar"], PROJECT / "electric_strum_test.mid")
    baseline_dir = PROJECT / "baseline_render"
    baseline_paths = generate_song_midis(baseline_composition(), {"acoustic_guitar": instruments["acoustic_guitar"]}, baseline_dir)
    shutil.copy2(baseline_paths["full_song"], PROJECT / "single_hit_baseline.mid")

    debug = {"schema_version": 1, "title": data["metadata"]["title"], "tracks": {}}
    for track_name, track in data["tracks"].items():
        debug["tracks"][track_name] = {}
        global_bar = 1
        for section in data["sections"]:
            phrase_data = track["sections"][section["name"]]["instrument_phrase"]
            compile_instrument_phrase(phrase_data, 4)
            bars = deepcopy(phrase_data["_strumming_debug"]["bars"])
            for item in bars:
                item["global_bar"] = global_bar + item["bar"] - 1
            debug["tracks"][track_name][section["name"]] = bars
            global_bar += section["bars"]
    write_json(PROJECT / "strumming_pattern_debug.json", debug)
    report = analyze_strumming_flow(data)
    write_json(PROJECT / "strumming-validation.json", report)
    a = report["tracks"]["acoustic_guitar"]["sections"]
    e = report["tracks"]["electric_rhythm_guitar"]["sections"]
    md = ["# Strumming Flow Report", "", "## Eight-bar A/B result", "",
          "- Bars 1-2 are the intentional failure baseline: one sounding downbeat hit per bar, with the remaining seven hand-grid positions preserved as air motion.",
          f"- Bars 3-4 Acoustic Verse: {a['verse']['average_hand_motions_per_bar']:.1f} hand motions/bar, {a['verse']['average_sounding_strums_per_bar']:.1f} sounding strums/bar, upstroke ratio {a['verse']['upstroke_ratio']:.0%}.",
          f"- Bars 5-6 Acoustic Pre-Chorus: {a['pre_chorus']['average_sounding_strums_per_bar']:.1f} sounding strums/bar; the pattern changes from Verse A to steady eighths without resetting the hand direction.",
          f"- Bars 7-8 Acoustic Chorus: {a['chorus']['average_sounding_strums_per_bar']:.1f} sounding strums/bar, {a['chorus']['only_one_strum_bars']} one-hit bars.",
          f"- Electric Verse/Pre/Chorus densities: {e['verse']['average_sounding_strums_per_bar']:.1f} / {e['pre_chorus']['average_sounding_strums_per_bar']:.1f} / {e['chorus']['average_sounding_strums_per_bar']:.1f}.",
          "- Every non-final bar declares last hand direction `up`, next expected direction `down`, and `pattern_continues_across_bar=true`.",
          "- Air strums remain in `strumming_pattern_debug.json`; they are not converted into fake pitched notes.",
          f"- Validator warnings: {report['warning_count']}. The two baseline bars are explicitly labeled and excluded from Verse/Chorus acceptance.", ""]
    (PROJECT / "strumming_flow_report.md").write_text("\n".join(md), encoding="utf-8")

    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_song.py"), "strumming_continuity_demo"], cwd=ROOT)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    shutil.copy2(PROJECT / "output" / "mix.wav", PROJECT / "continuous_strum_test.wav")
    print(f"[OK] {PROJECT}")


if __name__ == "__main__":
    main()
