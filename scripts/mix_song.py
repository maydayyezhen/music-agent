from __future__ import annotations

import argparse
import sys

from _bootstrap import ROOT
from src.mixer import mix_stems
from src.utils import load_song_config, project_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Mix existing WAV stems without rerendering MIDI.")
    parser.add_argument("song", help="project name under projects/")
    args = parser.parse_args()
    try:
        song_dir = project_dir(args.song)
        config = load_song_config(song_dir, "render.json")
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
    print(f"[OK] Mix: {output}")
    print(
        f"     {stats['duration_seconds']:.2f}s, peak {20.0 * __import__('math').log10(max(stats['peak_after'], 1e-12)):.2f} dBFS, "
        f"normalization {stats['normalization_db']:.2f} dB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
