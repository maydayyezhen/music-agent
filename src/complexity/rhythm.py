from __future__ import annotations

from copy import deepcopy
from typing import Any


def vary_rhythm_motif(pattern: list[dict[str, Any]], variation: str) -> list[dict[str, Any]]:
    """Create a small, deterministic rhythm variation without choosing pitches.

    This intentionally operates before pitch assignment. It gives composers an
    inspectable A/A'/B vocabulary while leaving style-specific pitch and
    articulation decisions to the composition layer.
    """
    if variation not in {"A", "A'", "B", "B'", "C"}:
        raise ValueError("variation must be A, A', B, B', or C")
    result = deepcopy(pattern)
    if variation == "A" or not result:
        return result
    if variation == "A'":
        result[-1]["duration"] = round(float(result[-1]["duration"]) * 1.5, 3)
    elif variation == "B":
        for index, item in enumerate(result):
            if index % 2:
                item["offset"] = round(float(item["offset"]) + 0.25, 3)
    elif variation == "B'":
        result = [item for index, item in enumerate(result) if index % 3 != 1]
        for item in result:
            item["duration"] = round(max(0.25, float(item["duration"]) * 0.75), 3)
    else:  # C: augmentation, useful for breakdowns and outros.
        for item in result:
            item["offset"] = round(float(item["offset"]) * 2.0, 3)
            item["duration"] = round(float(item["duration"]) * 2.0, 3)
    return result
