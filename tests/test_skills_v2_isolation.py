from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills_v2" / "registry.json"
FORBIDDEN = (
    "references/",
    "skills/",
    "docs/instrument_research/",
    "projects/",
)


class SkillsV2IsolationTests(unittest.TestCase):
    def test_active_skills_are_local_and_legacy_free(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        active = registry["active_skills"]
        self.assertGreaterEqual(len(active), 1)

        seen: set[str] = set()
        for row in active:
            skill_id = row["id"]
            self.assertNotIn(skill_id, seen)
            seen.add(skill_id)

            relative = row["path"]
            self.assertTrue(relative.startswith("skills_v2/"))
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)

            text = path.read_text(encoding="utf-8")
            for forbidden in FORBIDDEN:
                self.assertNotIn(forbidden, text, f"{skill_id}: {forbidden}")


if __name__ == "__main__":
    unittest.main()
