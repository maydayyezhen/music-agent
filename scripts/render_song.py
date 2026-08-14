from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT
from src.composition import load_composition
from src.midi import generate_song_midis
from src.mixer import mix_stems
from src.render import render_track
from src.render.wav import trim_wav
from src.utils import load_song_config, project_dir
from src.vocals import vocals_enabled
from src.instruments import export_long_form_plans, export_semantic_phrases
from src.validation import analyze_instrument_aware, analyze_long_form_phrases


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate all MIDI tracks, stems, and the final mix.")
    parser.add_argument("song", help="project name under projects/")
    parser.add_argument(
        "--with-vocals",
        action="store_true",
        help="after the instrumental mix, render vocals.json and create output/vocal_mix.wav",
    )
    args = parser.parse_args()
    try:
        song_dir = project_dir(args.song)
        composition = load_composition(song_dir / "composition.json")
        semantic = export_semantic_phrases(composition)
        if semantic["phrases"]:
            (song_dir / "semantic_phrases.json").write_text(
                json.dumps(semantic, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            instrument_report = analyze_instrument_aware(composition)
            (song_dir / "instrument-validation.json").write_text(
                json.dumps(instrument_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            if instrument_report["error_count"]:
                raise ValueError(
                    f"instrument-aware validation failed with {instrument_report['error_count']} physical/schema error(s)"
                )
            beats_per_bar = int(composition["metadata"]["time_signature"].split("/")[0])
            long_form = export_long_form_plans(composition, beats_per_bar)
            if long_form["plans"]:
                (song_dir / "long-form-plans.json").write_text(
                    json.dumps(long_form, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
                long_form_report = analyze_long_form_phrases(composition)
                (song_dir / "long-form-validation.json").write_text(
                    json.dumps(long_form_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
        instruments = load_song_config(song_dir, "instruments.json")
        config = load_song_config(song_dir, "render.json")
        print(f"Generating MIDI for {composition['metadata']['title']}...")
        midi_paths = generate_song_midis(composition, instruments, song_dir)
        beats_per_bar = int(composition["metadata"]["time_signature"].split("/")[0])
        score_seconds = (
            sum(section["bars"] for section in composition["sections"])
            * beats_per_bar
            * 60.0
            / float(composition["metadata"]["tempo"])
        )
        render_duration = score_seconds + float(config.get("tail_seconds", 2.0))
        for track_name in composition["tracks"]:
            stem = song_dir / "stems" / f"{track_name}.wav"
            print(f"Rendering {track_name} -> {stem.name}")
            render_track(track_name, midi_paths[track_name], instruments, config, stem)
            trim_wav(stem, render_duration)
        output = song_dir / "output" / "mix.wav"
        stats = mix_stems(
            song_dir / "stems",
            output,
            config["mix"],
            int(config["sample_rate"]),
            float(config.get("master_peak_db", -1.0)),
        )
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print(f"[OK] Full MIDI: {midi_paths['full_song']}")
    print(f"[OK] Final mix: {output}")
    print(f"     duration {stats['duration_seconds']:.2f}s, normalization {stats['normalization_db']:.2f} dB")
    if semantic["phrases"]:
        print(f"[OK] Semantic phrases: {song_dir / 'semantic_phrases.json'}")
        print(f"[OK] Instrument validation: {song_dir / 'instrument-validation.json'}")
        if 'long_form' in locals() and long_form["plans"]:
            print(f"[OK] Long-form plans: {song_dir / 'long-form-plans.json'}")
            print(f"[OK] Long-form validation: {song_dir / 'long-form-validation.json'}")
    if args.with_vocals:
        if not vocals_enabled(song_dir):
            print("[FAIL] --with-vocals requires an enabled vocals.json", file=sys.stderr)
            return 1
        completed = __import__("subprocess").run(
            [sys.executable, str(ROOT / "scripts" / "render_vocals.py"), args.song],
            cwd=ROOT,
        )
        return completed.returncode
    if vocals_enabled(song_dir):
        print("[INFO] vocals.json found; add --with-vocals to render the optional vocal version")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
