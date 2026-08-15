from __future__ import annotations

import json
from pathlib import Path
import unittest

from src.context_policy import creative_context_allowed


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills_v2" / "registry.json"
MATERIAL_REGISTRY = ROOT / "materials_v2" / "registry.json"
INSTRUMENT_CONFIG = ROOT / "config" / "instruments.json"
CONTEXT_POLICY = ROOT / "config" / "creative_context.json"

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
    ROOT / "scripts" / "build_melody_skeleton_v2.py",
    ROOT / "scripts" / "build_long_form_phrase_demos.py",
    ROOT / "tests" / "test_melody_skeleton_v2.py",
    ROOT / "tests" / "fixtures" / "lead_guitar_long_form_v2",
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

    def test_instrumentation_planning_is_default_for_multi_instrument_composition(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in registry["active_skills"]}
        planner = rows["instrumentation-role-planning"]
        self.assertTrue(planner["default_for_multi_instrument_composition"])

    def test_material_retrieval_does_not_use_genre_as_instrument_selector(self) -> None:
        registry = json.loads(MATERIAL_REGISTRY.read_text(encoding="utf-8"))
        policy = registry["retrieval_policy"]
        self.assertTrue(policy["instrumentation_before_materials"])
        self.assertTrue(policy["genre_tags_are_compatibility_hints"])
        self.assertTrue(policy["genre_tags_must_not_select_instrumentation"])
        self.assertTrue(policy["do_not_infer_energy_from_genre"])
        self.assertTrue(policy["expand_if_one_instrument_family_dominates_without_user_constraint"])

    def test_pop_rock_retrieval_keeps_acoustic_candidates(self) -> None:
        registry = json.loads(MATERIAL_REGISTRY.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in registry["materials"]}
        for material_id in (
            "warm-pop-sixteenth-strum",
            "gentle-steel-strum-picking",
            "multi-take-acoustic-stack",
        ):
            self.assertIn("pop-rock", rows[material_id]["genre_tags"])

    def test_ambiguous_guitar_fallback_is_not_overdriven(self) -> None:
        config = json.loads(INSTRUMENT_CONFIG.read_text(encoding="utf-8"))
        self.assertTrue(config["guitar"]["legacy_ambiguous_alias"])
        self.assertNotEqual(config["guitar"]["program"], config["overdriven_guitar"]["program"])
        self.assertIn("acoustic_guitar", config)
        self.assertIn("electric_guitar", config)
        self.assertIn("overdriven_guitar", config)

    def test_composition_context_is_allowlist_based(self) -> None:
        policy = json.loads(CONTEXT_POLICY.read_text(encoding="utf-8"))
        self.assertFalse(policy["modes"]["composition"]["default_allow"])

        for path in (
            "SKILL.md",
            "skills_v2/melody_structure_development/SKILL.md",
            "materials_v2/registry.json",
            "profiles/general_midi/profile.json",
            "docs/agent_api/README.md",
        ):
            self.assertTrue(creative_context_allowed(path), path)

        for path in (
            "scripts/build_any_demo.py",
            "tests/test_anything.py",
            "src/melody/long_form.py",
            "source_library/private_reference.mid",
            "projects/unrelated_song/composition.json",
            "docs/random_demo_notes.md",
        ):
            self.assertFalse(creative_context_allowed(path), path)

    def test_only_active_project_enters_composition_context(self) -> None:
        self.assertTrue(
            creative_context_allowed(
                "projects/current_song/composition.json",
                active_project="current_song",
            )
        )
        self.assertFalse(
            creative_context_allowed(
                "projects/other_song/composition.json",
                active_project="current_song",
            )
        )

    def test_debug_and_source_modes_require_explicit_mode_change(self) -> None:
        self.assertFalse(creative_context_allowed("src/melody/long_form.py"))
        self.assertTrue(
            creative_context_allowed(
                "src/melody/long_form.py",
                mode="implementation_debug",
            )
        )
        self.assertFalse(creative_context_allowed("source_library/reference.mid"))
        self.assertTrue(
            creative_context_allowed(
                "source_library/reference.mid",
                mode="source_study",
            )
        )
        self.assertFalse(
            creative_context_allowed(
                "scripts/build_any_demo.py",
                mode="implementation_debug",
            )
        )
        self.assertTrue(
            creative_context_allowed(
                "scripts/build_any_demo.py",
                mode="test_maintenance",
            )
        )

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
