from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from src.utils.paths import project_root


def find_fluidsynth() -> Path | None:
    configured = os.environ.get("MUSIC_AGENT_FLUIDSYNTH")
    candidates = [
        Path(configured) if configured else None,
        project_root() / "tools" / "fluidsynth" / "bin" / "fluidsynth.exe",
        project_root() / "tools" / "fluidsynth" / "fluidsynth.exe",
        Path(shutil.which("fluidsynth")) if shutil.which("fluidsynth") else None,
    ]
    return next((path.resolve() for path in candidates if path and path.is_file()), None)


def render_midi(
    midi_path: Path,
    soundfont_path: Path,
    output_wav: Path,
    sample_rate: int = 44100,
    gain: float = 0.7,
) -> None:
    executable = find_fluidsynth()
    if executable is None:
        raise FileNotFoundError(
            "FluidSynth not found. Run: python scripts/setup_assets.py"
        )
    if not soundfont_path.is_file():
        raise FileNotFoundError(
            f"SoundFont not found: {soundfont_path}. Run: python scripts/setup_assets.py"
        )
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(executable),
        "-ni",
        "-g",
        str(gain),
        "-F",
        str(output_wav),
        "-T",
        "wav",
        "-r",
        str(sample_rate),
        str(soundfont_path),
        str(midi_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if completed.returncode != 0 or not output_wav.is_file():
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"FluidSynth render failed ({completed.returncode}): {detail}")
