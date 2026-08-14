from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT
from src.mixer import mix_stems
from src.performance import decode_tokens
from src.performance.pmt_midi import generate_pmt_midis
from src.render import render_midi, render_track
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
        notes = decode_tokens(
            (song_dir / "performance.pmt").read_text(encoding="utf-8")
        )
        if not notes:
            raise ValueError("performance.pmt decoded to no notes")
        metadata = json.loads(
            (song_dir / "performance.meta.json").read_text(encoding="utf-8")
        )
        sidecar_path = song_dir / "performance.midi-sidecar.json"
        sidecar = (
            json.loads(sidecar_path.read_text(encoding="utf-8"))
            if sidecar_path.is_file()
            else None
        )
        instruments = load_song_config(song_dir, "instruments.json")
        config = load_song_config(song_dir, "render.json")

        print(
            f"Generating MIDI from PMT for "
            f"{metadata.get('title', args.song)}..."
        )
        midi_paths = generate_pmt_midis(notes, song_dir, metadata, sidecar)
        score_seconds = max(
            note.onset_ms + note.duration_ms for note in notes
        ) / 1000.0
        render_duration = score_seconds + float(
            config.get("tail_seconds", 2.0)
        )
        output = song_dir / "output" / "mix.wav"

        if config.get("render_full_midi_direct", False):
            stem = song_dir / "stems" / "full_song.wav"
            print(f"Rendering complete multitrack MIDI -> {stem.name}")
            render_midi(
                midi_paths["full_song"],
                {"engine": "fluidsynth"},
                config,
                stem,
            )
            trim_wav(stem, render_duration)
            stats = mix_stems(
                song_dir / "stems",
                output,
                {
                    "full_song": {
                        "volume_db": 0.0,
                        "pan": 0.0,
                        "mute": False,
                    }
                },
                int(config["sample_rate"]),
                float(config.get("master_peak_db", -1.0)),
            )
        else:
            track_names = [
                str(metadata["tracks"][key]["name"])
                for key in sorted(
                    metadata["tracks"], key=lambda value: int(value)
                )
            ]
            missing = [name for name in track_names if name not in instruments]
            if missing:
                raise KeyError(
                    f"instrument mapping is missing PMT tracks: {missing}"
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
    if sidecar is not None:
        print(f"[OK] MIDI sidecar: {sidecar_path}")
    print(f"[OK] Full MIDI: {midi_paths['full_song']}")
    print(f"[OK] Final mix: {output}")
    print(
        f"     duration {stats['duration_seconds']:.2f}s, "
        f"normalization {stats['normalization_db']:.2f} dB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
