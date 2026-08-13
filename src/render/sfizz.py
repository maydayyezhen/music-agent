from __future__ import annotations

import os
import shutil
from pathlib import Path


def find_sfizz() -> Path | None:
    configured = os.environ.get("MUSIC_AGENT_SFIZZ")
    for candidate in (configured, shutil.which("sfizz_render"), shutil.which("sfizz-render")):
        if candidate and Path(candidate).is_file():
            return Path(candidate).resolve()
    return None


def render_midi_with_sfizz(*args: object, **kwargs: object) -> None:
    executable = find_sfizz()
    if executable is None:
        raise FileNotFoundError(
            "sfizz-render is not installed. FluidSynth tracks still work; install sfizz before using an SFZ mapping."
        )
    raise NotImplementedError(
        "The sfizz backend discovery and routing contract is ready, but CLI flags must be finalized against the installed sfizz version."
    )
