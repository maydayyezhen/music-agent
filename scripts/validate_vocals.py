from __future__ import annotations

import argparse
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

from _bootstrap import ROOT
from src.utils import load_song_config, project_dir
from src.vocals import load_vocals


VOCAL_PYTHON = ROOT / ".venv-vocals" / "Scripts" / "python.exe"


def wav_stats(path: Path) -> tuple[int, int, float, float, float]:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        frames = handle.getnframes()
        audio = np.frombuffer(handle.readframes(frames), dtype="<i2").astype(np.float64) / 32768.0
    peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
    rms = float(np.sqrt(np.mean(audio ** 2))) if len(audio) else 0.0
    return rate, channels, frames / rate, peak, rms


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an already-rendered optional vocal project.")
    parser.add_argument("song")
    args = parser.parse_args()
    try:
        song_dir = project_dir(args.song)
        load_vocals(song_dir)
        render = load_song_config(song_dir, "render.json")
        expected_rate = int(render["sample_rate"])
        paths = {
            "vocal stem": song_dir / "stems" / "vocal.wav",
            "instrumental mix": song_dir / "output" / "mix.wav",
            "vocal mix": song_dir / "output" / "vocal_mix.wav",
        }
        stats = {}
        for label, path in paths.items():
            if not path.is_file():
                raise FileNotFoundError(path)
            stats[label] = wav_stats(path)
            rate, channels, duration, peak, rms = stats[label]
            if rate != expected_rate or duration <= 0 or peak <= 1e-4 or rms <= 1e-5:
                raise ValueError(f"invalid {label}: rate={rate}, duration={duration}, peak={peak}, rms={rms}")
            if peak >= 1.0:
                raise ValueError(f"{label} clips at {peak:.4f}")
            print(f"[OK] {label}: {duration:.2f}s, {rate} Hz, {channels}ch, peak {peak:.4f}, RMS {rms:.4f}")
        if abs(stats["instrumental mix"][2] - stats["vocal mix"][2]) > 0.01:
            raise ValueError("instrumental and vocal mix durations differ")
        if paths["instrumental mix"].read_bytes() == paths["vocal mix"].read_bytes():
            raise ValueError("vocal mix is byte-identical to the instrumental")
        probe = subprocess.run(
            [
                str(VOCAL_PYTHON),
                "-c",
                "import librosa,sys,numpy as np; y,sr=librosa.load(sys.argv[1],sr=None,mono=True); "
                "f0,_,_=librosa.pyin(y,fmin=librosa.note_to_hz('C3'),fmax=librosa.note_to_hz('C6'),sr=sr); "
                "v=f0[np.isfinite(f0)]; print(float(np.median(v)),len(v)); assert len(v)>10",
                str(paths["vocal stem"]),
            ],
            capture_output=True,
            text=True,
        )
        if probe.returncode != 0:
            raise RuntimeError("pitch detection failed: " + probe.stderr.strip())
        print(f"[OK] sung pitch detected: median Hz / voiced frames = {probe.stdout.strip()}")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print("Vocal render validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
