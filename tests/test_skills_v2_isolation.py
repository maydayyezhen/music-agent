from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills_v2" / "registry.json"
FORBIDDEN_SKILL_REFERENCES = (
    "references/",
    "skills/",
    "docs/instrument_research/",
    "projects/",
)

REMOVED_LEGACY_PATHS = (
    ROOT / "skills",
    ROOT / "references",
    ROOT / "docs" / "instrument_research",
    ROOT / "docs" / "continuous_strumming.md",
    ROOT / "docs" / "guitar_native_lead_playbook.md",
    ROOT / "docs" / "long_form_phrase_analysis.md",
    ROOT / "docs" / "long_form_phrase_application.md",
    ROOT / "docs" / "long_form_phrase_change_list.md",
    ROOT / "docs" / "long_form_phrase_schema.md",
    ROOT / "docs" / "long_form_rollback_audit.md",
    ROOT / "docs" / "long_form_tonality.md",
    ROOT / "docs" / "long_form_v2_change_list.md",
    ROOT / "docs" / "pmt_gesture_ir_experiment.md",
)

REMOVED_LEGACY_PROJECTS = (
    "accompaniment_continuity_demo",
    "church_choir_demo",
    "comfortably_numb_agent_reconstruction",
    "complexity_demo",
    "demo_song",
    "electric_guitar_rock_epic",
    "electric_guitar_rock_long_form",
    "electric_guitar_rock_stable_v2",
    "english_vocal_pop",
    "guitar_native_rock_proof",
    "instrument_aware_demos",
    "instrument_aware_full_song",
    "knowledge_demo",
    "long_continuous_strum_song",
    "long_form_phrase_demos",
    "next_stop_unnamed",
    "old_demo",
    "sixteenth_strumming_demo",
    "strumming_continuity_demo",
    "vocal_demo",
    "vocal_demo_en",
    "vocal_demo_ja",
    "walk_me_to_the_streetlamp",
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
            for forbidden in FORBIDDEN_SKILL_REFERENCES:
                self.assertNotIn(forbidden, text, f"{skill_id}: {forbidden}")

    def test_removed_legacy_knowledge_paths_stay_removed(self) -> None:
        for path in REMOVED_LEGACY_PATHS:
            self.assertFalse(path.exists(), f"legacy path returned: {path.relative_to(ROOT)}")

    def test_removed_legacy_projects_stay_removed(self) -> None:
        projects = ROOT / "projects"
        for name in REMOVED_LEGACY_PROJECTS:
            path = projects / name
            self.assertFalse(path.exists(), f"legacy project returned: {name}")


if __name__ == "__main__":
    unittest.main()
