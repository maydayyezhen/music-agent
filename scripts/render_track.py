from __future__ import annotations

import argparse
import sys

from _bootstrap import ROOT
from src.composition import load_composition
from src.midi import generate_song_midis
from src.render import render_track
from src.render.wav import trim_wav
from src.utils import load_song_config, project_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate MIDI and WAV for one song track.")
    parser.add_argument("song", help="project name under projects/")
    parser.add_argument("track", help="track name, for example piano")
    args = parser.parse_args()
    try:
        song_dir = project_dir(args.song)
        composition = load_composition(song_dir / "composition.json")
        instruments = load_song_config(song_dir, "instruments.json")
        render_config = load_song_config(song_dir, "render.json")
        if args.track not in composition["tracks"]:
            choices = ", ".join(composition["tracks"])
            raise KeyError(f"unknown track '{args.track}'. Available: {choices}")
        midi_paths = generate_song_midis(
            composition, instruments, song_dir, track_names={args.track}
        )
        stem = song_dir / "stems" / f"{args.track}.wav"
        render_track(args.track, midi_paths[args.track], instruments, render_config, stem)
        beats_per_bar = int(composition["metadata"]["time_signature"].split("/")[0])
        score_seconds = (
            sum(section["bars"] for section in composition["sections"])
            * beats_per_bar
            * 60.0
            / float(composition["metadata"]["tempo"])
        )
        trim_wav(stem, score_seconds + float(render_config.get("tail_seconds", 2.0)))
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print(f"[OK] MIDI: {midi_paths[args.track]}")
    print(f"[OK] Stem: {stem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
