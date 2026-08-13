from __future__ import annotations

import wave
from pathlib import Path

import numpy as np


def place_phrase_wavs(
    rendered: list[tuple[float, Path]], output_path: Path, sample_rate: int, total_seconds: float | None = None
) -> dict[str, float]:
    chunks: list[tuple[int, np.ndarray]] = []
    frames = 0
    for offset_seconds, path in rendered:
        with wave.open(str(path), "rb") as handle:
            if handle.getsampwidth() != 2 or handle.getframerate() != sample_rate:
                raise ValueError(f"unexpected vocal WAV format: {path}")
            channels = handle.getnchannels()
            data = np.frombuffer(handle.readframes(handle.getnframes()), dtype="<i2").astype(np.float64)
        audio = data.reshape(-1, channels).mean(axis=1) / 32768.0
        offset = round(offset_seconds * sample_rate)
        chunks.append((offset, audio))
        frames = max(frames, offset + len(audio))
    if total_seconds is not None:
        frames = max(frames, round(total_seconds * sample_rate))
    result = np.zeros(frames, dtype=np.float64)
    for offset, audio in chunks:
        result[offset:offset + len(audio)] += audio
    peak = float(np.max(np.abs(result))) if len(result) else 0.0
    if peak > 0.98:
        result *= 0.98 / peak
    pcm = (np.clip(result, -1.0, 1.0) * 32767.0).astype("<i2")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())
    return {
        "duration_seconds": len(result) / sample_rate,
        "peak": float(np.max(np.abs(result))) if len(result) else 0.0,
        "rms": float(np.sqrt(np.mean(result ** 2))) if len(result) else 0.0,
    }
