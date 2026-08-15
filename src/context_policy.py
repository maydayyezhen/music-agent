from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "creative_context.json"


def load_context_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_repo_path(path: str | Path) -> str:
    value = str(path).replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value.lstrip("/")


def _resolve_mode(policy: dict[str, Any], mode: str) -> dict[str, Any]:
    modes = policy.get("modes", {})
    if mode not in modes:
        raise ValueError(f"unknown creative context mode: {mode!r}")

    raw = modes[mode]
    parent_name = raw.get("extends")
    if parent_name:
        parent = _resolve_mode(policy, str(parent_name))
    else:
        parent = {
            "allowed_exact": [],
            "allowed_prefixes": [],
            "denied_prefixes": [],
            "allow_active_project": False,
            "default_allow": False,
        }

    merged = {
        "allowed_exact": list(parent.get("allowed_exact", [])),
        "allowed_prefixes": list(parent.get("allowed_prefixes", [])),
        "denied_prefixes": list(parent.get("denied_prefixes", [])),
        "allow_active_project": bool(parent.get("allow_active_project", False)),
        "default_allow": bool(parent.get("default_allow", False)),
    }
    for field in ("allowed_exact", "allowed_prefixes", "denied_prefixes"):
        merged[field].extend(raw.get(field, []))
    if "allow_active_project" in raw:
        merged["allow_active_project"] = bool(raw["allow_active_project"])
    if "default_allow" in raw:
        merged["default_allow"] = bool(raw["default_allow"])
    return merged


def creative_context_allowed(
    path: str | Path,
    *,
    active_project: str | None = None,
    mode: str = "composition",
    policy: dict[str, Any] | None = None,
) -> bool:
    policy = policy or load_context_policy()
    rules = _resolve_mode(policy, mode)
    candidate = normalize_repo_path(path)

    if candidate in rules["allowed_exact"]:
        return True
    if any(candidate.startswith(prefix) for prefix in rules["allowed_prefixes"]):
        return True

    if rules["allow_active_project"] and active_project:
        active_prefix = f"projects/{normalize_repo_path(active_project).strip('/')}/"
        if candidate == active_prefix[:-1] or candidate.startswith(active_prefix):
            return True

    if any(candidate.startswith(prefix) for prefix in rules["denied_prefixes"]):
        return False
    return bool(rules["default_allow"])


def require_creative_context_path(
    path: str | Path,
    *,
    active_project: str | None = None,
    mode: str = "composition",
    policy: dict[str, Any] | None = None,
) -> None:
    if not creative_context_allowed(
        path,
        active_project=active_project,
        mode=mode,
        policy=policy,
    ):
        raise PermissionError(
            f"{normalize_repo_path(path)!r} is outside {mode!r} creative context"
        )
