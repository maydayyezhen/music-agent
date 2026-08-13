from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from _bootstrap import ROOT
from src.composition import load_composition
from src.mixer import mix_stems
from src.utils import load_song_config, project_dir
from src.vocals import load_vocals
from src.vocals.mix import place_phrase_wavs
from src.vocals.score import build_phrase_score
from src.vocals.japanese import build_japanese_phrase_score


VOCAL_PYTHON = ROOT / ".venv-vocals" / "Scripts" / "python.exe"
MODEL = "assets/vocals/espnet-opencpop-visinger"
JAPANESE_MODEL = "assets/vocals/espnet-kiritan-visinger"


def render_english_vocals(
    song_dir: Path,
    vocals: dict,
    tempo: float,
    sample_rate: int,
    song_seconds: float,
) -> tuple[Path, dict[str, float]]:
    stem = song_dir / "stems" / "vocal.wav"
    work_dir = song_dir / "vocals" / "soulx"
    work_dir.mkdir(parents=True, exist_ok=True)
    job = {
        "phrases": vocals["phrases"],
        "tempo": tempo,
        "device": vocals.get("device", "cuda"),
        "sample_rate": sample_rate,
        "song_seconds": song_seconds,
        "metadata": str(work_dir / "target.json"),
        "save_dir": str(work_dir / "render"),
        "output": str(stem),
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
        json.dump(job, handle, ensure_ascii=False)
        job_path = Path(handle.name)
    try:
        print(f"Rendering {len(vocals['phrases'])} English vocal phrases with SoulX-Singer...")
        subprocess.run(
            [str(VOCAL_PYTHON), str(ROOT / "scripts" / "_soulx_worker.py"), str(job_path)],
            cwd=ROOT,
            check=True,
        )
    finally:
        job_path.unlink(missing_ok=True)
    import wave
    import numpy as np
    with wave.open(str(stem), "rb") as handle:
        audio = np.frombuffer(handle.readframes(handle.getnframes()), dtype="<i2").astype(np.float64) / 32768.0
        duration = handle.getnframes() / handle.getframerate()
    return stem, {
        "duration_seconds": duration,
        "peak": float(np.max(np.abs(audio))),
        "rms": float(np.sqrt(np.mean(audio ** 2))),
    }


def render_vocals(song_dir: Path) -> tuple[Path, dict[str, float]]:
    vocals = load_vocals(song_dir)
    composition = load_composition(song_dir / "composition.json")
    tempo = float(composition["metadata"]["tempo"])
    render = load_song_config(song_dir, "render.json")
    sample_rate = int(render["sample_rate"])
    if not VOCAL_PYTHON.is_file():
        raise FileNotFoundError("vocal environment missing; run scripts/setup_vocals.ps1")
    phrase_wavs: list[tuple[float, Path]] = []
    beats_per_bar = int(composition["metadata"]["time_signature"].split("/")[0])
    song_seconds = (
        sum(section["bars"] for section in composition["sections"])
        * beats_per_bar
        * 60.0
        / tempo
        + float(render.get("tail_seconds", 2.0))
    )
    if vocals.get("language") == "en":
        return render_english_vocals(song_dir, vocals, tempo, sample_rate, song_seconds)
    intermediate = song_dir / "vocals" / "phrases"
    intermediate.mkdir(parents=True, exist_ok=True)
    for index, phrase in enumerate(vocals["phrases"], 1):
        language = vocals.get("language", "zh")
        score = build_japanese_phrase_score(phrase, tempo) if language == "ja" else build_phrase_score(phrase, tempo)
        output = intermediate / f"phrase_{index:03d}.wav"
        job = {
            "model": JAPANESE_MODEL if language == "ja" else MODEL,
            "config": (
                "exp/svs_train_visinger_24_raw_phn_pyopenjtalk_jp/config.yaml"
                if language == "ja" else "exp/svs_visinger_normal/config.yaml"
            ),
            "checkpoint": (
                "exp/svs_train_visinger_24_raw_phn_pyopenjtalk_jp/200epoch.pth"
                if language == "ja" else "exp/svs_visinger_normal/500epoch.pth"
            ),
            "sample_rate": sample_rate,
            "device": vocals.get("device", "cuda"),
            "seed": vocals.get("seed", 777),
            "noise_scale": vocals.get("noise_scale", 0.667),
            "noise_scale_dur": vocals.get("noise_scale_dur", 0.8),
            "tempo": tempo,
            "phone_times": score.phone_times,
            "phones": score.phones,
            "notes": score.notes,
            "output": str(output),
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(job, handle, ensure_ascii=False)
            job_path = Path(handle.name)
        try:
            print(f"Rendering vocal phrase {index}/{len(vocals['phrases'])}: " + "".join(n["lyric"] for n in phrase["notes"]))
            subprocess.run(
                [str(VOCAL_PYTHON), str(ROOT / "scripts" / "_vocal_worker.py"), str(job_path)],
                cwd=ROOT / (JAPANESE_MODEL if language == "ja" else MODEL),
                check=True,
            )
        finally:
            job_path.unlink(missing_ok=True)
        phrase_wavs.append((score.offset_seconds, output))
    stem = song_dir / "stems" / "vocal.wav"
    return stem, place_phrase_wavs(phrase_wavs, stem, sample_rate, song_seconds)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render optional Chinese, English, or Japanese lead vocals.")
    parser.add_argument("song", help="project name under projects/")
    parser.add_argument("--stem-only", action="store_true", help="render vocal.wav but do not create vocal_mix.wav")
    args = parser.parse_args()
    try:
        song_dir = project_dir(args.song)
        stem, vocal_stats = render_vocals(song_dir)
        print(f"[OK] Vocal stem: {stem}")
        print(f"     duration {vocal_stats['duration_seconds']:.2f}s, peak {vocal_stats['peak']:.4f}, RMS {vocal_stats['rms']:.4f}")
        if not args.stem_only:
            config = load_song_config(song_dir, "render.json")
            mix = dict(config["mix"])
            mix["vocal"] = load_vocals(song_dir).get("mix", {"volume_db": -2.0, "pan": 0.0, "mute": False})
            output = song_dir / "output" / "vocal_mix.wav"
            stats = mix_stems(song_dir / "stems", output, mix, int(config["sample_rate"]), float(config.get("master_peak_db", -1.0)))
            print(f"[OK] Vocal mix: {output}")
            print(f"     duration {stats['duration_seconds']:.2f}s, normalization {stats['normalization_db']:.2f} dB")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
