from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills_v2"
REGISTRY = SKILLS_ROOT / "registry.json"
FORBIDDEN_REFERENCES = (
    "references/",
    "skills/",
    "docs/instrument_research/",
    "projects/",
)


def main() -> int:
    errors: list[str] = []

    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as error:
        print(f"[FAIL] cannot read skills registry: {error}", file=sys.stderr)
        return 1

    active = registry.get("active_skills")
    if not isinstance(active, list):
        errors.append("registry.active_skills must be a list")
        active = []

    seen_ids: set[str] = set()
    for row in active:
        if not isinstance(row, dict):
            errors.append("active skill entry must be an object")
            continue
        skill_id = str(row.get("id", "")).strip()
        path_text = str(row.get("path", "")).strip()
        if not skill_id:
            errors.append("active skill requires id")
            continue
        if skill_id in seen_ids:
            errors.append(f"duplicate skill id: {skill_id}")
        seen_ids.add(skill_id)
        if not path_text.startswith("skills_v2/"):
            errors.append(f"skill {skill_id} escapes skills_v2: {path_text}")
            continue
        path = ROOT / path_text
        if not path.is_file():
            errors.append(f"skill {skill_id} is missing: {path_text}")
            continue
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_REFERENCES:
            if forbidden in text:
                errors.append(
                    f"skill {skill_id} references inactive legacy path {forbidden!r}"
                )

    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    print(f"[OK] active skills: {len(active)}")
    print("[OK] all active skills stay inside skills_v2")
    print("[OK] no active skill directly references inactive legacy paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
