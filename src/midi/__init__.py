from typing import Any


def generate_song_midis(*args: Any, **kwargs: Any):
    """Lazy import prevents composition helpers and MIDI pitches from cycling."""
    from .generator import generate_song_midis as implementation

    return implementation(*args, **kwargs)


__all__ = ["generate_song_midis"]
