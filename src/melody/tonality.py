from __future__ import annotations

from typing import Any

from src.instruments.common import root_pc


MODE_INTERVALS: dict[str, tuple[int, ...]] = {
    "major": (0, 2, 4, 5, 7, 9, 11),
    "natural_minor": (0, 2, 3, 5, 7, 8, 10),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "major_pentatonic": (0, 2, 4, 7, 9),
    "minor_pentatonic": (0, 3, 5, 7, 10),
    "minor_blues": (0, 3, 5, 6, 7, 10),
}

MODE_ALIASES = {
    "ionian": "major",
    "minor": "natural_minor",
    "aeolian": "natural_minor",
}


def _interval_list(value: Any, field: str) -> list[int]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"tonality.{field} must be a non-empty integer list")
    if any(not isinstance(interval, int) for interval in value):
        raise ValueError(f"tonality.{field} must contain only integers")
    return [interval % 12 for interval in value]


def resolve_tonality(phrase: dict[str, Any]) -> tuple[set[int], dict[str, Any]]:
    """Resolve the pitch-class palette for long-form melody generation.

    Existing compositions that only provide ``key_root`` retain the old natural-minor
    behavior. New compositions may provide an explicit ``tonality`` object:

    {
      "tonic": "D",
      "mode": "major",
      "additional_intervals": [10]
    }

    ``scale_intervals`` overrides the named mode. Additional/excluded intervals are
    relative to the tonic and make borrowed colors explicit instead of silently forcing
    every song through one fixed scale.
    """
    raw = phrase.get("tonality")
    legacy = raw is None
    if raw is None:
        raw = {
            "tonic": phrase.get("key_root", "E"),
            "mode": phrase.get("mode", "natural_minor"),
        }
    if not isinstance(raw, dict):
        raise ValueError("long-form tonality must be an object")

    tonic = str(raw.get("tonic", phrase.get("key_root", "E")))
    mode = MODE_ALIASES.get(str(raw.get("mode", "natural_minor")).lower(),
                            str(raw.get("mode", "natural_minor")).lower())

    if "scale_intervals" in raw:
        intervals = _interval_list(raw["scale_intervals"], "scale_intervals")
        mode_name = "custom"
    else:
        if mode not in MODE_INTERVALS:
            supported = ", ".join(sorted(MODE_INTERVALS))
            raise ValueError(f"unsupported long-form tonality mode {mode!r}; supported: {supported}")
        intervals = list(MODE_INTERVALS[mode])
        mode_name = mode

    additional = raw.get("additional_intervals", [])
    excluded = raw.get("excluded_intervals", [])
    if additional:
        additional = _interval_list(additional, "additional_intervals")
    if excluded:
        excluded = _interval_list(excluded, "excluded_intervals")

    resolved_intervals = sorted((set(intervals) | set(additional)) - set(excluded))
    if len(resolved_intervals) < 2:
        raise ValueError("long-form tonality must resolve to at least two pitch classes")

    tonic_pc = root_pc(tonic)
    pitch_classes = {(tonic_pc + interval) % 12 for interval in resolved_intervals}
    descriptor = {
        "source": "legacy_key_root" if legacy else "explicit",
        "tonic": tonic,
        "tonic_pitch_class": tonic_pc,
        "mode": mode_name,
        "scale_intervals": resolved_intervals,
        "pitch_classes": sorted(pitch_classes),
        "additional_intervals": sorted(set(additional)),
        "excluded_intervals": sorted(set(excluded)),
    }
    return pitch_classes, descriptor
