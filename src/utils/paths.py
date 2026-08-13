from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def project_dir(song_name: str) -> Path:
    path = project_root() / "projects" / song_name
    if not path.is_dir():
        raise FileNotFoundError(f"song project not found: {path}")
    return path


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_song_config(song_path: Path, filename: str) -> dict[str, Any]:
    """Prefer a song-local config, then fall back to the shared project config."""
    local = song_path / filename
    return load_json(local if local.is_file() else project_root() / "config" / filename)
