from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT  # noqa: F401
from src.mixer import mix_stems
from src.performance import decode_tokens
from src.performance.pmt_midi import generate_pmt_midis
from src.render import render_track
from src.render.wav import trim_wav
from src.utils import load_song_config, project_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a performance.pmt project through the existing audio backends."
    )
    parser.add_argument("song", help="project name under projects/")
    args = parser.parse_args()

    try:
        song_dir = project_dir(args.song)
        tokens = (song_dir / "performance.pmt").read_text(
            encoding="utf-8"
        )
        notes = decode_tokens(tokens)
        if not notes:
            raise ValueError("performance.pmt decoded to no notes")

        metadata = json.loads(
            (song_dir / "performance.meta.json").read_text(
                encoding="utf-8"
            )
        )
        instruments = load_song_config(song_dir, "instruments.json")
        config = load_song_config(song_dir, "render.json")

        print(
            f"Generating MIDI from PMT for "
            f"{metadata.get('title', args.song)}..."
        )
        midi_paths = generate_pmt_midis(
            notes,
            song_dir,
            metadata,
        )

        track_names = [
            str(metadata["tracks"][key]["name"])
            for key in sorted(
                metadata["tracks"],
                key=lambda value: int(value),
            )
        ]
        missing = [
            name for name in track_names if name not in instruments
        ]
        if missing:
            raise KeyError(
                f"instrument mapping is missing PMT tracks: {missing}"
            )

        score_seconds = max(
            note.onset_ms + note.duration_ms
            for note in notes
        ) / 1000.0
        render_duration = score_seconds + float(
            config.get("tail_seconds", 2.0)
        )

        for track_name in track_names:
            stem = song_dir / "stems" / f"{track_name}.wav"
            print(f"Rendering {track_name} -> {stem.name}")
            render_track(
                track_name,
                midi_paths[track_name],
                instruments,
                config,
                stem,
            )
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

    print(f"[OK] PMT notes: {len(notes)}")
    print(f"[OK] Full MIDI: {midi_paths['full_song']}")
    print(f"[OK] Final mix: {output}")
    print(
        f"     duration {stats['duration_seconds']:.2f}s, "
        f"normalization {stats['normalization_db']:.2f} dB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
