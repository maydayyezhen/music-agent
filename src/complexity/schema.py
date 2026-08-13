from __future__ import annotations

from copy import deepcopy
from typing import Any


COMPLEXITY_LEVELS = ("minimal", "simple", "standard", "rich", "dense")
DIMENSIONS = (
    "rhythm", "harmony", "arrangement", "melodic_ornamentation", "density", "variation"
)

COMPLEXITY_PRESETS: dict[str, dict[str, Any]] = {
    "minimal": {"level": "minimal", "rhythm": 1, "harmony": 2, "arrangement": 1, "melodic_ornamentation": 1, "density": 1, "variation": 1},
    "simple": {"level": "simple", "rhythm": 2, "harmony": 2, "arrangement": 2, "melodic_ornamentation": 2, "density": 2, "variation": 2},
    "standard": {"level": "standard", "rhythm": 3, "harmony": 3, "arrangement": 3, "melodic_ornamentation": 2, "density": 3, "variation": 3},
    "rich": {"level": "rich", "rhythm": 4, "harmony": 4, "arrangement": 4, "melodic_ornamentation": 3, "density": 3, "variation": 4},
    "dense": {"level": "dense", "rhythm": 5, "harmony": 4, "arrangement": 5, "melodic_ornamentation": 4, "density": 5, "variation": 5},
}

NAMED_PRESETS = {
    "quiet_galgame": {"level": "simple", "rhythm": 2, "harmony": 3, "arrangement": 2, "melodic_ornamentation": 2, "density": 1, "variation": 2},
    "pop": deepcopy(COMPLEXITY_PRESETS["standard"]),
    "brit_rock": {"level": "rich", "rhythm": 4, "harmony": 2, "arrangement": 4, "melodic_ornamentation": 2, "density": 4, "variation": 4},
    "minimal_ambient": {"level": "minimal", "rhythm": 1, "harmony": 3, "arrangement": 1, "melodic_ornamentation": 1, "density": 1, "variation": 1},
    "battle_dense": deepcopy(COMPLEXITY_PRESETS["dense"]),
}

BUDGETS = {"minimal": 5, "simple": 8, "standard": 11, "rich": 15, "dense": 19}
REST_RATIO_GUIDES = {
    "minimal": (0.35, 0.65), "simple": (0.25, 0.50), "standard": (0.15, 0.40),
    "rich": (0.10, 0.30), "dense": (0.05, 0.20),
}


def normalize_complexity(value: str | dict[str, Any] | None) -> dict[str, Any]:
    """Return a complete profile without mutating the composition.

    Missing complexity is intentionally equivalent to standard. Old files do
    not need migration and their musical events are never rewritten.
    """
    if value is None:
        value = "standard"
    if isinstance(value, str):
        key = value.lower().strip().replace(" ", "_")
        source = COMPLEXITY_PRESETS.get(key) or NAMED_PRESETS.get(key)
        if source is None:
            raise ValueError(f"unknown complexity level/preset: {value!r}")
        result = deepcopy(source)
    elif isinstance(value, dict):
        level = str(value.get("level", "standard")).lower()
        if level not in COMPLEXITY_LEVELS:
            raise ValueError(f"complexity.level must be one of {COMPLEXITY_LEVELS}")
        result = deepcopy(COMPLEXITY_PRESETS[level])
        for key in DIMENSIONS:
            if key in value:
                number = value[key]
                if not isinstance(number, int) or not 1 <= number <= 5:
                    raise ValueError(f"complexity.{key} must be an integer from 1 to 5")
                result[key] = number
    else:
        raise ValueError("complexity must be a level string or an object")
    result["budget"] = BUDGETS[result["level"]]
    result["melody_rest_ratio_guide"] = list(REST_RATIO_GUIDES[result["level"]])
    return result


def merge_complexity(base: dict[str, Any], override: str | dict[str, Any] | None) -> dict[str, Any]:
    if override is None:
        return deepcopy(base)
    if isinstance(override, str):
        return normalize_complexity(override)
    level = str(override.get("level", base["level"]))
    seed = normalize_complexity(level) if "level" in override else deepcopy(base)
    for key in DIMENSIONS:
        if key in override:
            number = override[key]
            if not isinstance(number, int) or not 1 <= number <= 5:
                raise ValueError(f"section complexity.{key} must be 1..5")
            seed[key] = number
    seed["budget"] = BUDGETS[seed["level"]]
    seed["melody_rest_ratio_guide"] = list(REST_RATIO_GUIDES[seed["level"]])
    return seed


def _contour_delta(contour: str, index: int, total: int, name: str) -> int:
    lower = name.lower()
    if contour == "flat":
        return 0
    if contour in ("gradual_build", "sparse_to_climax"):
        fraction = index / max(1, total - 1)
        return -1 if fraction < 0.25 else (1 if fraction >= 0.70 else 0)
    if contour == "wave":
        return (-1, 0, 1, 0)[index % 4]
    if contour == "verse_chorus":
        if any(word in lower for word in ("intro", "break", "outro")):
            return -1
        if any(word in lower for word in ("chorus", "final", "climax")):
            return 1
        return 0
    if contour == "custom":
        return 0
    raise ValueError(f"unknown complexity_contour: {contour!r}")


def resolve_section_complexities(composition: dict[str, Any]) -> dict[str, dict[str, Any]]:
    global_profile = normalize_complexity(composition.get("complexity"))
    contour = str(composition.get("complexity_contour", "flat"))
    sections = composition.get("sections", [])
    resolved: dict[str, dict[str, Any]] = {}
    for index, section in enumerate(sections):
        delta = _contour_delta(contour, index, len(sections), str(section["name"]))
        level_index = max(0, min(4, COMPLEXITY_LEVELS.index(global_profile["level"]) + delta))
        contoured = merge_complexity(global_profile, COMPLEXITY_LEVELS[level_index]) if delta else deepcopy(global_profile)
        # Preserve explicitly customized dimensions across automatic contours.
        if delta and isinstance(composition.get("complexity"), dict):
            for dimension in DIMENSIONS:
                if dimension in composition["complexity"]:
                    contoured[dimension] = global_profile[dimension]
        resolved[str(section["name"])] = merge_complexity(contoured, section.get("complexity"))
    return resolved


def parse_complexity_request(text: str) -> dict[str, Any]:
    """Deterministic, inspectable mapping from common brief language."""
    lower = text.lower()
    level = "standard"
    rules = (
        (("极简", "minimal", "非常空"), "minimal"),
        (("简单", "simple"), "simple"),
        (("丰富", "complex", "复杂一点", "rich"), "rich"),
        (("很疯", "炫技", "dense", "高密度"), "dense"),
    )
    for words, candidate in rules:
        if any(word in lower for word in words):
            level = candidate
    profile = normalize_complexity(level)
    if any(word in lower for word in ("节奏有意思", "节奏复杂", "syncop", "切分")):
        profile["rhythm"] = max(profile["rhythm"], 4)
    if any(word in lower for word in ("和声漂亮", "和声丰富", "harmon")):
        profile["harmony"] = max(profile["harmony"], 4)
    if any(word in lower for word in ("不要很吵", "不吵", "安静", "空", "sparse")):
        profile["density"] = min(profile["density"], 2)
    if any(word in lower for word in ("编曲复杂", "层次丰富", "多层")):
        profile["arrangement"] = max(profile["arrangement"], 4)
    if any(word in lower for word in ("少装饰", "不要花哨")):
        profile["melodic_ornamentation"] = min(profile["melodic_ornamentation"], 2)
    if any(word in lower for word in ("朴素", "plain melody", "simple melody")):
        profile["melodic_ornamentation"] = min(profile["melodic_ornamentation"], 2)
    constraints: list[str] = []
    if any(word in lower for word in ("不要所有乐器一直一起响", "不要全都一起", "not all instruments", "不要齐奏")):
        constraints += ["avoid_all_tracks_continuous", "prefer_call_and_response"]
    if constraints:
        profile["arrangement_constraints"] = constraints
    return profile
