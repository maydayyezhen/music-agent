from __future__ import annotations

import wave
from pathlib import Path


def trim_wav(path: Path, duration_seconds: float) -> None:
    """Trim a PCM WAV in place while preserving its channel/format metadata."""
    temporary = path.with_suffix(".trimmed.wav")
    with wave.open(str(path), "rb") as source:
        parameters = source.getparams()
        frame_limit = min(source.getnframes(), round(duration_seconds * source.getframerate()))
        frames = source.readframes(frame_limit)
    with wave.open(str(temporary), "wb") as destination:
        destination.setparams(parameters)
        destination.writeframes(frames)
    temporary.replace(path)
