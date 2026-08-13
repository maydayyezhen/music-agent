from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.complexity import normalize_complexity, parse_complexity_request, resolve_section_complexities, vary_rhythm_motif
from src.complexity.critic import analyze_complexity
from src.composition.loader import load_composition, validate_composition


ROOT = Path(__file__).resolve().parents[1]


class ComplexityTests(unittest.TestCase):
    def test_old_composition_remains_valid_and_unmodified(self) -> None:
        path = ROOT / "projects" / "demo_song" / "composition.json"
        before = path.read_bytes()
        composition = load_composition(path)
        self.assertEqual(normalize_complexity(composition.get("complexity"))["level"], "standard")
        self.assertEqual(before, path.read_bytes())

    def test_all_presets_are_complete(self) -> None:
        for level in ("minimal", "simple", "standard", "rich", "dense"):
            profile = normalize_complexity(level)
            self.assertEqual(profile["level"], level)
            for dimension in ("rhythm", "harmony", "arrangement", "melodic_ornamentation", "density", "variation"):
                self.assertIn(profile[dimension], range(1, 6))

    def test_natural_language_dimensions_do_not_collapse_to_density(self) -> None:
        profile = parse_complexity_request("丰富一点，节奏更有意思，但不要很吵，旋律少装饰")
        self.assertEqual(profile["level"], "rich")
        self.assertGreaterEqual(profile["rhythm"], 4)
        self.assertLessEqual(profile["density"], 2)
        self.assertLessEqual(profile["melodic_ornamentation"], 2)
        constrained = parse_complexity_request("编曲复杂，但不要所有乐器一直一起响")
        self.assertIn("avoid_all_tracks_continuous", constrained["arrangement_constraints"])

    def test_section_override_wins_over_contour(self) -> None:
        composition = {"complexity": "standard", "complexity_contour": "gradual_build", "sections": [
            {"name": "intro", "bars": 4}, {"name": "final", "bars": 8, "complexity": {"level": "simple", "harmony": 5}}
        ]}
        resolved = resolve_section_complexities(composition)
        self.assertEqual(resolved["intro"]["level"], "simple")
        self.assertEqual(resolved["final"]["level"], "simple")
        self.assertEqual(resolved["final"]["harmony"], 5)

    def test_rhythm_variations_are_pitch_independent(self) -> None:
        pattern = [{"offset": 0, "duration": 1}, {"offset": 1.5, "duration": 0.5}]
        varied = vary_rhythm_motif(pattern, "B")
        self.assertEqual(pattern[1]["offset"], 1.5)
        self.assertEqual(varied[1]["offset"], 1.75)
        self.assertNotIn("pitch", varied[0])

    def test_invalid_budget_is_rejected(self) -> None:
        composition = json.loads((ROOT / "projects" / "demo_song" / "composition.json").read_text(encoding="utf-8"))
        composition["sections"][0]["complexity_budget"] = {"lead": 6}
        with self.assertRaisesRegex(ValueError, "must be 0..5"):
            validate_composition(composition)

    def test_five_demo_levels_share_identity_and_increase_climax_density(self) -> None:
        densities = []
        for level in ("minimal", "simple", "standard", "rich", "dense"):
            composition = load_composition(ROOT / "projects" / "complexity_demo" / level / "composition.json")
            self.assertEqual(composition["metadata"]["tempo"], 100)
            self.assertEqual(composition["metadata"]["key"], "D Dorian")
            first = composition["tracks"]["piano"]["sections"]["theme_a"]["events"][0]
            self.assertEqual(first["pitch"], "D5")
            densities.append(analyze_complexity(composition)["section_metrics"]["theme_b"]["section_density"])
        self.assertEqual(densities, sorted(densities))
        self.assertGreater(densities[-1], densities[0] * 4)


if __name__ == "__main__":
    unittest.main()
