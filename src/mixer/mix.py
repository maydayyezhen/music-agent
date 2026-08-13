from __future__ import annotations

import math
import wave
from pathlib import Path
from typing import Any

import numpy as np


def mix_stems(
    stems_dir: Path,
    output_path: Path,
    mix_config: dict[str, Any],
    sample_rate: int,
    master_peak_db: float = -1.0,
) -> dict[str, float]:
    loaded: list[tuple[str, np.ndarray, dict[str, Any]]] = []
    max_frames = 0
    for name, settings in mix_config.items():
        if settings.get("mute", False):
            continue
        path = stems_dir / f"{name}.wav"
        if not path.is_file():
            raise FileNotFoundError(f"stem not found: {path}")
        audio, rate = _read_wav(path)
        if rate != sample_rate:
            raise ValueError(f"sample rate mismatch for {path}: {rate} != {sample_rate}")
        loaded.append((name, audio, settings))
        max_frames = max(max_frames, len(audio))
    if not loaded:
        raise ValueError("no unmuted stems to mix")

    result = np.zeros((max_frames, 2), dtype=np.float64)
    for _, audio, settings in loaded:
        mono = audio.mean(axis=1) if audio.shape[1] > 1 else audio[:, 0]
        gain = 10.0 ** (float(settings.get("volume_db", 0.0)) / 20.0)
        pan = max(-1.0, min(1.0, float(settings.get("pan", 0.0))))
        angle = (pan + 1.0) * math.pi / 4.0
        result[: len(mono), 0] += mono * gain * math.cos(angle)
        result[: len(mono), 1] += mono * gain * math.sin(angle)

    peak_before = float(np.max(np.abs(result)))
    target_peak = 10.0 ** (master_peak_db / 20.0)
    normalization_db = 0.0
    if peak_before > target_peak:
        scale = target_peak / peak_before
        result *= scale
        normalization_db = 20.0 * math.log10(scale)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_wav(output_path, result, sample_rate)
    return {
        "duration_seconds": len(result) / sample_rate,
        "peak_before": peak_before,
        "normalization_db": normalization_db,
        "peak_after": float(np.max(np.abs(result))),
    }


def _read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        width = handle.getsampwidth()
        rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    if width != 2:
        raise ValueError(f"only 16-bit PCM WAV is supported: {path}")
    audio = np.frombuffer(frames, dtype="<i2").astype(np.float64) / 32768.0
    return audio.reshape(-1, channels), rate


def _write_wav(path: Path, audio: np.ndarray, sample_rate: int) -> None:
    pcm = np.clip(audio, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())
