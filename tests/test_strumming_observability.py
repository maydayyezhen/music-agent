from __future__ import annotations

import unittest

from src.skills_v2.strumming_observability import (
    annotate_direction_observability,
    apply_alternate_generation_assumption,
    can_generate_directional_demo,
)


class StrummingObservabilityTests(unittest.TestCase):
    def quantized_analysis(self) -> dict:
        slot_profiles = [
            {
                "slot": slot,
                "expected_direction": "down" if slot % 2 == 0 else "up",
                "attack_probability": 1.0,
                "dominant_stroke_type": "middle_partial",
                "accent_class": "neutral",
            }
            for slot in range(8)
        ]
        return {
            "model": {
                "technique": "continuous_eighth_alternating_strumming",
                "motion": {
                    "type": "alternate",
                    "slot_zero_direction": "down",
                    "continuous_motion": True,
                    "cross_bar_continuity": True,
                    "alternate_direction_confidence": 0.0,
                },
                "slot_profiles": slot_profiles,
                "invariance_fingerprint": {
                    "slot_zero_direction": "down",
                    "attack_mask": [1] * 8,
                },
                "evidence": {"stroke_count": 8},
                "limitations": [],
            },
            "strokes": [
                {
                    "pitches": [48, 52, 55],
                    "spread_beats": 0.0,
                }
                for _ in range(8)
            ],
        }

    def test_quantized_chords_do_not_learn_direction(self) -> None:
        result = annotate_direction_observability(self.quantized_analysis())
        direction = result["observability"]["direction"]
        model = result["model"]

        self.assertEqual(
            direction["status"],
            "unobservable_quantized_onsets",
        )
        self.assertEqual(direction["measurable_direction_strokes"], 0)
        self.assertEqual(direction["zero_spread_ratio"], 1.0)
        self.assertEqual(model["motion"]["type"], "unknown")
        self.assertEqual(model["motion"]["slot_zero_direction"], "unknown")
        self.assertTrue(
            all(
                profile["expected_direction"] == "unknown"
                for profile in model["slot_profiles"]
            )
        )
        self.assertFalse(can_generate_directional_demo(model))

    def test_explicit_assumption_does_not_mutate_model(self) -> None:
        result = annotate_direction_observability(self.quantized_analysis())
        model = result["model"]
        assumed = apply_alternate_generation_assumption(model)

        self.assertEqual(model["motion"]["slot_zero_direction"], "unknown")
        self.assertEqual(assumed["motion"]["slot_zero_direction"], "down")
        self.assertEqual(
            assumed["motion"]["generation_assumption"],
            "alternate_down_up_not_learned",
        )
        self.assertEqual(
            [profile["expected_direction"] for profile in assumed["slot_profiles"]],
            ["down", "up", "down", "up", "down", "up", "down", "up"],
        )


if __name__ == "__main__":
    unittest.main()
