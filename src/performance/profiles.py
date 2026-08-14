from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from src.utils.paths import project_root


def load_profile(name: str) -> dict[str, Any]:
    path = project_root() / "profiles" / name / "profile.json"
    if not path.is_file():
        raise FileNotFoundError(f"sound-library profile not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def apply_profile(events: list[dict[str, Any]], profile: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    result: list[dict[str, Any]] = []
    coverage: dict[str, dict[str, int]] = {}
    for source in events:
        event = deepcopy(source)
        if event.get("type") not in {"note", "chord"}:
            result.append(event)
            continue
        for articulation in event.get("articulations", []):
            mapping = profile.get("articulations", {}).get(articulation)
            row = coverage.setdefault(articulation, {"mapped": 0, "fallback": 0, "unsupported": 0})
            if not mapping:
                row["unsupported"] += 1
                continue
            if "keyswitch" in mapping:
                event.setdefault("profile_triggers", []).append({"type": "keyswitch", **mapping["keyswitch"]})
                row["mapped"] += 1
            elif "cc" in mapping:
                event.setdefault("profile_triggers", []).append({"type": "control_change", **mapping["cc"]})
                row["mapped"] += 1
            elif "fallback" in mapping:
                fallback = mapping["fallback"]
                event["duration"] = round(float(event["duration"]) * float(fallback.get("gate_ratio", 1.0)), 3)
                event["velocity"] = max(1, min(127, int(event["velocity"]) + int(fallback.get("velocity_delta", 0))))
                row["fallback"] += 1
            else:
                row["unsupported"] += 1
        if event.get("bend_semitones") is not None and profile.get("supports", {}).get("pitch_bend"):
            event["_pitch_bend_range"] = float(profile.get("pitch_bend_range", 2))
        if event.get("slide_from_semitones") is not None and profile.get("supports", {}).get("pitch_bend"):
            event["_pitch_bend_range"] = float(profile.get("pitch_bend_range", 2))
        result.append(event)
    return result, {"profile": profile["id"], "articulation_coverage": coverage}
