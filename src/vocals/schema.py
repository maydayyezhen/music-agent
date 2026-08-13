from __future__ import annotations

from pathlib import Path
from typing import Any

from src.utils import load_json


def vocals_enabled(song_dir: Path) -> bool:
    path = song_dir / "vocals.json"
    return path.is_file() and bool(load_json(path).get("enabled", True))


def load_vocals(song_dir: Path) -> dict[str, Any]:
    path = song_dir / "vocals.json"
    if not path.is_file():
        raise FileNotFoundError(f"optional vocal score not found: {path}")
    data = load_json(path)
    if not data.get("enabled", True):
        raise ValueError("vocals.json exists but enabled is false")
    language = data.get("language", "zh")
    engines = {
        "zh": "espnet_opencpop_visinger",
        "en": "soulx_singer",
        "ja": "espnet_kiritan_visinger",
    }
    if language not in engines:
        raise ValueError(f"unsupported vocal language: {language}; choose zh, en, or ja")
    engine = data.get("engine", engines[language])
    if engine != engines[language]:
        raise ValueError(f"unsupported vocal engine: {engine}")
    phrases = data.get("phrases")
    if not isinstance(phrases, list) or not phrases:
        raise ValueError("vocals.json must contain at least one phrase")
    previous_end = -1.0
    for phrase_index, phrase in enumerate(phrases, 1):
        if not isinstance(phrase, dict):
            raise ValueError(f"phrase {phrase_index} must be an object")
        start = float(phrase.get("start_beat", 0))
        notes = phrase.get("notes")
        if start < 0 or not isinstance(notes, list) or not notes:
            raise ValueError(f"phrase {phrase_index} needs start_beat >= 0 and non-empty notes")
        cursor = start
        for note_index, note in enumerate(notes, 1):
            if not isinstance(note, dict):
                raise ValueError(f"phrase {phrase_index} note {note_index} must be an object")
            lyric = str(note.get("lyric", "")).strip()
            pitch = note.get("pitch")
            beats = float(note.get("duration", 0))
            if language in ("zh", "ja") and len(lyric) != 1:
                raise ValueError(
                    f"phrase {phrase_index} note {note_index}: lyric must be one character/kana"
                )
            if language == "en" and (not lyric or " " in lyric):
                raise ValueError(
                    f"phrase {phrase_index} note {note_index}: English lyric must be one word or syllable token"
                )
            if not isinstance(pitch, (str, int)) or beats <= 0:
                raise ValueError(
                    f"phrase {phrase_index} note {note_index}: pitch and positive duration are required"
                )
            cursor += beats
        if start < previous_end:
            raise ValueError(f"phrase {phrase_index} overlaps the previous phrase")
        previous_end = cursor
    return data
