from __future__ import annotations

from copy import deepcopy
from typing import Any


TEXTURE_TYPES = (
    "sustain", "pulse", "broken_chord", "arpeggio", "ostinato",
    "counterline", "stab", "pedal",
)

TEXTURE_FAMILIES = {
    "sustain": "plane",
    "pulse": "point",
    "broken_chord": "line",
    "arpeggio": "line",
    "ostinato": "line",
    "counterline": "line",
    "stab": "point",
    "pedal": "plane",
}

CONTINUITY_DEFAULTS: dict[str, dict[str, float]] = {
    "sustain": {"sustain_ratio": 0.90, "legato_ratio": 0.80, "overlap": 0.08, "common_tone_retention": 0.90, "voice_leading_strength": 0.90},
    "pulse": {"sustain_ratio": 0.20, "legato_ratio": 0.10, "overlap": 0.00, "common_tone_retention": 0.65, "voice_leading_strength": 0.75},
    "broken_chord": {"sustain_ratio": 0.35, "legato_ratio": 0.65, "overlap": 0.04, "common_tone_retention": 0.65, "voice_leading_strength": 0.80},
    "arpeggio": {"sustain_ratio": 0.45, "legato_ratio": 0.80, "overlap": 0.05, "common_tone_retention": 0.65, "voice_leading_strength": 0.85},
    "ostinato": {"sustain_ratio": 0.30, "legato_ratio": 0.45, "overlap": 0.02, "common_tone_retention": 0.55, "voice_leading_strength": 0.70},
    "counterline": {"sustain_ratio": 0.60, "legato_ratio": 0.75, "overlap": 0.05, "common_tone_retention": 0.60, "voice_leading_strength": 0.85},
    "stab": {"sustain_ratio": 0.10, "legato_ratio": 0.00, "overlap": 0.00, "common_tone_retention": 0.40, "voice_leading_strength": 0.60},
    "pedal": {"sustain_ratio": 1.00, "legato_ratio": 1.00, "overlap": 0.08, "common_tone_retention": 1.00, "voice_leading_strength": 1.00},
}


def resolve_texture(track: dict[str, Any], clip: dict[str, Any]) -> str | None:
    texture = clip.get("texture", track.get("texture"))
    if texture is None:
        return None
    texture = str(texture).lower().strip()
    if texture not in TEXTURE_TYPES:
        raise ValueError(f"texture must be one of {TEXTURE_TYPES}: {texture!r}")
    return texture


def normalize_continuity(texture: str | None, *values: dict[str, Any] | None) -> dict[str, float]:
    result = deepcopy(CONTINUITY_DEFAULTS.get(texture or "pulse", CONTINUITY_DEFAULTS["pulse"]))
    for value in values:
        if value is None:
            continue
        if not isinstance(value, dict):
            raise ValueError("continuity must be an object")
        for key in result:
            if key in value:
                number = value[key]
                if not isinstance(number, (int, float)) or not 0 <= float(number) <= 1:
                    raise ValueError(f"continuity.{key} must be between 0 and 1")
                result[key] = float(number)
    return result
