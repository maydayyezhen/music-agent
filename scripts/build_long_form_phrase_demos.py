from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

from _bootstrap import ROOT
from src.composition import load_composition
from src.instruments import export_long_form_plans, export_semantic_phrases
from src.midi import generate_song_midis
from src.render import render_track
from src.render.wav import trim_wav
from src.validation import analyze_long_form_phrases
from src.accompaniment.generator import materialize_clip
from src.instruments.common import position
from src.midi.pitches import note_number

BASE = ROOT / "projects" / "long_form_phrase_demos"
INSTRUMENTS = {"lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30}}
RENDER = {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.72,
          "tail_seconds": 2.0, "master_peak_db": -1.0,
          "mix": {"lead_guitar": {"volume_db": -2, "pan": 0, "mute": False}}}


def harmony(chords: list[str]) -> list[dict[str, object]]:
    return [{"at": f"{index + 1}:1", "duration": 4, "chord": chord} for index, chord in enumerate(chords)]


def relationships(bars: int) -> list[dict[str, object]]:
    if bars == 8:
        return [
            {"phrase_id": "A1", "bars": [1, 2], "relationship": "introduce", "continuation_from": None, "continuation_to": "A2", "resolution": "deferred", "motif_operations": []},
            {"phrase_id": "A2", "bars": [3, 4], "relationship": "continuation", "continuation_from": "A1", "continuation_to": "A3", "resolution": "deferred", "motif_operations": ["rhythmic_extension", "change_ending"]},
            {"phrase_id": "A3", "bars": [5, 6], "relationship": "variation", "continuation_from": "A2", "continuation_to": "C", "resolution": "deferred", "motif_operations": ["transpose_up", "change_ending"]},
            {"phrase_id": "C", "bars": [7, 8], "relationship": "resolution", "continuation_from": "A3", "continuation_to": None, "resolution": "strong", "motif_operations": ["augmentation"]},
        ]
    return [
        {"phrase_id": "A1", "bars": [1, 4], "relationship": "introduce", "continuation_from": None, "continuation_to": "A2", "resolution": "deferred", "motif_operations": []},
        {"phrase_id": "A2", "bars": [5, 8], "relationship": "variation", "continuation_from": "A1", "continuation_to": "A3", "resolution": "weak", "motif_operations": ["transpose_up", "change_ending"]},
        {"phrase_id": "A3", "bars": [9, 12], "relationship": "climax", "continuation_from": "A2", "continuation_to": "C", "resolution": "deferred", "motif_operations": ["transpose_up", "rhythmic_extension", "compression"]},
        {"phrase_id": "C", "bars": [13, 16], "relationship": "resolution", "continuation_from": "A3", "continuation_to": None, "resolution": "strong", "motif_operations": ["augmentation", "fragmentation"]},
    ]


def long_phrase(bars: int, seed: int) -> dict[str, object]:
    chords = (["Em", "C", "G", "D"] * (bars // 4))
    energies = [round(0.36 + 0.58 * (index / max(1, int(bars * .7))) if index <= int(bars * .7)
                      else 0.92 - 0.48 * ((index - int(bars * .7)) / max(1, bars - int(bars * .7) - 1)), 3)
                for index in range(bars)]
    energies = [min(1.0, max(0.0, value)) for value in energies]
    peak_bar = 6 if bars == 8 else 12
    target = "E6" if bars == 16 else "B5"
    return {
        "instrument": "electric_lead_guitar", "role": "lead", "phrase_type": "melodic_lead",
        "phrase_generation_mode": "long_form_experimental", "energy": 0.74,
        "performance_intent": {"attack": "singing", "release": "arc_shaped", "humanization": "action_based", "seed": seed},
        "key_root": "E", "register_midi": [59, 88], "motif_root_midi": 64, "motif_id": "motif_A",
        "motif_seed": [
            {"offset": 0.5, "duration": 0.75, "degree": 0, "action": "pick"},
            {"offset": 1.25, "duration": 0.75, "degree": 3, "action": "hammer_on"},
            {"offset": 3.5, "duration": 1.0, "degree": 5, "action": "slide", "cross_bar_reason": "phrase_continuation"},
            {"offset": 4.4, "duration": 0.7, "degree": 3, "action": "pull_off"},
            {"offset": 5.2, "duration": 1.2, "degree": 7, "action": "pick", "cross_bar_reason": "delayed_resolution", "rest_type_after": "breath"},
            {"offset": 8.5, "duration": 0.8, "degree": 5, "action": "slide"},
            {"offset": 9.4, "duration": 0.75, "degree": 3, "action": "pull_off"},
            {"offset": 10.4, "duration": 1.9, "degree": 8, "action": "pick", "cross_bar_reason": "target_sustain",
             "rest_type_after": "breath"},
        ],
        "harmony": harmony(chords),
        "section_arc": {"section_id": f"lead_{bars}_bar_arc", "bars": [1, bars],
                        "opening_register": "mid", "peak_register": "high", "peak_bar": peak_bar,
                        "final_resolution_bar": bars, "energy_curve": energies,
                        "density_curve": [round(0.42 + 0.3 * value, 3) for value in energies],
                        "cadence_plan": {"strong_cadences": [bars], "weak_cadences": [bars // 2],
                                         "avoid_resolution_bars": [bars // 4, peak_bar]},
                        "breath_bars": [bars // 4, bars // 2, bars - 2],
                        "cross_bar_note_bars": [2, bars // 2, peak_bar, bars - 2],
                        "delayed_target": {"pitch": target, "bar": peak_bar}},
        "phrase_relationships": relationships(bars),
        "long_form_phrase_rules": {"planning_window_bars": bars, "minimum_connected_span_bars": 6,
                                   "maximum_strong_cadences_per_8_bars": 1,
                                   "minimum_cross_bar_notes_per_8_bars": 2,
                                   "minimum_motif_developments_per_section": 3,
                                   "maximum_independent_phrase_resets_per_8_bars": 1,
                                   "maximum_consecutive_full_rest_bars": 1,
                                   "require_delayed_peak": True, "require_delayed_resolution": True},
    }


def legacy_phrase(bars: int, seed: int) -> dict[str, object]:
    motif = []
    pitches = ["E4", "G4", "B4", "A4", "G4", "D5"]
    for block in range(0, bars, 4):
        for index, pitch in enumerate(pitches):
            motif.append({"pitch": pitch, "at": f"{block + 1}:{1 + index * .5}", "duration": 0.42 if index < 5 else 1.3,
                          "articulations": ["sustain", "vibrato"] if index == 5 else (["hammer_on", "legato"] if index == 1 else ["sustain"])})
    return {"instrument": "electric_lead_guitar", "role": "lead", "phrase_type": "melodic_lead",
            "phrase_generation_mode": "legacy_stable", "energy": 0.74,
            "performance_intent": {"attack": "section_shaped", "release": "phrase_shaped", "humanization": "action_based", "seed": seed},
            "harmony": harmony(["Em", "C", "G", "D"] * (bars // 4)), "motif": motif}


def legacy_metrics(composition_data: dict[str, object]) -> dict[str, object]:
    track = composition_data["tracks"]["lead_guitar"]
    clip = track["sections"]["solo"]
    events = materialize_clip(deepcopy(clip), track, 4)
    cross_bar = sum(1 for event in events if position(event["at"], 4) + float(event["duration"]) >
                    (int(position(event["at"], 4) // 4) + 1) * 4 + 1e-6)
    peak = max(note_number(event["pitch"]) for event in events)
    peak_bars = sorted({int(position(event["at"], 4) // 4) + 1 for event in events if note_number(event["pitch"]) == peak})
    endings = sum("vibrato" in event.get("articulations", []) for event in events)
    return {"independent_endings": endings, "cross_bar_connections": cross_bar,
            "peak_bar": peak_bars, "motif_developments": 0,
            "assessment": "four unrelated closed statements"}


def composition(title: str, bars: int, phrase: dict[str, object]) -> dict[str, object]:
    return {"metadata": {"title": title, "tempo": 104, "time_signature": "4/4", "key": "E minor"},
            "sections": [{"name": "solo", "bars": bars}],
            "tracks": {"lead_guitar": {"role": "electric lead guitar", "sections": {"solo": {
                "loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": phrase}}}}}


def write_project(name: str, data: dict[str, object], description: str) -> Path:
    folder = BASE / name; folder.mkdir(parents=True, exist_ok=True)
    (folder / "composition.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "instruments.json").write_text(json.dumps(INSTRUMENTS, indent=2) + "\n", encoding="utf-8")
    (folder / "render.json").write_text(json.dumps(RENDER, indent=2) + "\n", encoding="utf-8")
    loaded = load_composition(folder / "composition.json")
    (folder / "semantic_phrases.json").write_text(json.dumps(export_semantic_phrases(loaded), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plans = export_long_form_plans(loaded, 4)
    (folder / "section-arc.json").write_text(json.dumps({"plans": [p["section_arc"] for p in plans["plans"]]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "phrase-relationship-graph.json").write_text(json.dumps({"plans": [p["phrase_relationships"] for p in plans["plans"]]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "melodic-state-trace.json").write_text(json.dumps({"plans": [p["melodic_state_trace"] for p in plans["plans"]]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = analyze_long_form_phrases(loaded)
    (folder / "long-form-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "README.md").write_text(f"# {data['metadata']['title']}\n\n{description}\n", encoding="utf-8")
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_song.py"), f"long_form_phrase_demos/{name}"], cwd=ROOT)
    if completed.returncode: raise RuntimeError(f"render failed: {name}")
    shutil.copy2(folder / "output" / "mix.wav", folder / "output" / "final.wav")
    return folder


def ab_project() -> None:
    folder = BASE / "03_legacy_vs_long_form_ab"; folder.mkdir(parents=True, exist_ok=True)
    legacy = composition("Legacy Short Phrase AB", 16, legacy_phrase(16, 303))
    long = composition("Long Form Phrase AB", 16, long_phrase(16, 303))
    (folder / "legacy_composition.json").write_text(json.dumps(legacy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "composition.json").write_text(json.dumps(long, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "instruments.json").write_text(json.dumps(INSTRUMENTS, indent=2) + "\n", encoding="utf-8")
    (folder / "render.json").write_text(json.dumps(RENDER, indent=2) + "\n", encoding="utf-8")
    loaded_long = load_composition(folder / "composition.json"); loaded_legacy = load_composition(folder / "legacy_composition.json")
    with tempfile.TemporaryDirectory() as long_temp, tempfile.TemporaryDirectory() as legacy_temp:
        long_paths = generate_song_midis(loaded_long, INSTRUMENTS, Path(long_temp))
        legacy_paths = generate_song_midis(loaded_legacy, INSTRUMENTS, Path(legacy_temp))
        shutil.copy2(long_paths["lead_guitar"], folder / "long_form_phrase.mid")
        (folder / "tracks").mkdir(parents=True, exist_ok=True)
        shutil.copy2(long_paths["lead_guitar"], folder / "tracks" / "lead_guitar.mid")
        (folder / "output").mkdir(parents=True, exist_ok=True)
        shutil.copy2(long_paths["full_song"], folder / "output" / "full_song.mid")
        shutil.copy2(legacy_paths["lead_guitar"], folder / "legacy_short_phrase.mid")
    render_track("lead_guitar", folder / "long_form_phrase.mid", INSTRUMENTS, RENDER, folder / "long_form_phrase.wav")
    render_track("lead_guitar", folder / "legacy_short_phrase.mid", INSTRUMENTS, RENDER, folder / "legacy_short_phrase.wav")
    trim_wav(folder / "long_form_phrase.wav", 16 * 4 * 60 / 104 + 2); trim_wav(folder / "legacy_short_phrase.wav", 16 * 4 * 60 / 104 + 2)
    (folder / "semantic_phrases.json").write_text(json.dumps({
        "legacy": export_semantic_phrases(loaded_legacy), "long_form": export_semantic_phrases(loaded_long)
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plans = export_long_form_plans(loaded_long, 4)
    for filename, key in (("section-arc.json", "section_arc"), ("phrase-relationship-graph.json", "phrase_relationships"), ("melodic-state-trace.json", "melodic_state_trace")):
        (folder / filename).write_text(json.dumps({"plans": [p[key] for p in plans["plans"]]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = analyze_long_form_phrases(loaded_long)
    (folder / "long-form-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metrics = report["sections"][0]["assessment"]
    comparison = {"shared_conditions": {"chords": ["Em", "C", "G", "D"] * 4, "bpm": 104, "program": 30, "key": "E minor", "bars": 16, "seed": 303},
                  "legacy": legacy_metrics(legacy),
                  "long_form": {"independent_endings": metrics["strong_cadences"], "cross_bar_connections": metrics["cross_bar_notes"], "peak_bar": metrics["peak_bars"], "motif_developments": metrics["motif_developments"], "assessment": "one arc with dependent transformations and delayed resolution"}}
    (folder / "ab-comparison-report.json").write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "README.md").write_text("# Legacy versus Long-Form A/B\n\nSame harmony, BPM, GM distortion-guitar program, key, length and seed. The legacy MIDI restarts and closes every four bars; the long-form MIDI shares an arc, relationship graph and persistent state.\n", encoding="utf-8")


def main() -> int:
    write_project("01_singing_lead_8bar", composition("Eight-Bar Singing Lead", 8, long_phrase(8, 301)),
                  "One connected eight-bar singing lead: one strong cadence, cross-bar notes, slide and legato, delayed peak, and motif development after bar four.")
    write_project("02_developing_solo_16bar", composition("Sixteen-Bar Developing Solo", 16, long_phrase(16, 302)),
                  "A1 introduction, A2 transposed variation, A3 compressed expansion/climax, then augmented fragmented resolution. Includes arc, relationship graph, and state trace.")
    ab_project()
    return 0


if __name__ == "__main__": raise SystemExit(main())
