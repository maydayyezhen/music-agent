from __future__ import annotations

import unittest

from src.composition import validate_composition
from src.instruments import compile_instrument_phrase, export_long_form_plans
from src.instruments.common import position
from src.midi.pitches import note_number
from src.validation import analyze_long_form_phrases


def neutral_phrase() -> dict:
    return {
        "instrument": "electric_lead_guitar",
        "role": "lead",
        "phrase_type": "melodic_lead",
        "phrase_generation_mode": "long_form_authored",
        "energy": 0.5,
        "performance_intent": {"seed": 1},
        "tonality": {"tonic": "C", "scale_intervals": list(range(12))},
        "register_midi": [48, 72],
        "motif_root_midi": 60,
        "pitch_quantization": "none",
        "motif_seed": [
            {"offset": 0.0, "duration": 0.5, "degree": 0},
            {"offset": 1.0, "duration": 0.5, "degree": 0},
            {"offset": 2.0, "duration": 0.5, "degree": 0},
        ],
        "harmony": [{"at": "1:1", "duration": 16, "chord": "C"}],
        "section_arc": {
            "bars": [1, 4],
            "energy_curve": [0.5, 0.5, 0.5, 0.5],
        },
        "phrase_relationships": [
            {
                "phrase_id": "P1",
                "bars": [1, 1],
                "relationship": "introduce",
                "continuation_from": None,
                "continuation_to": "P2",
                "resolution": "deferred",
                "motif_operations": [],
            },
            {
                "phrase_id": "P2",
                "bars": [2, 2],
                "relationship": "sequence",
                "continuation_from": "P1",
                "continuation_to": "P3",
                "resolution": "deferred",
                "motif_operations": ["transpose_up"],
            },
            {
                "phrase_id": "P3",
                "bars": [3, 3],
                "relationship": "climax",
                "continuation_from": "P2",
                "continuation_to": "P4",
                "resolution": "deferred",
                "motif_operations": ["change_ending"],
            },
            {
                "phrase_id": "P4",
                "bars": [4, 4],
                "relationship": "resolution",
                "continuation_from": "P3",
                "continuation_to": None,
                "resolution": "strong",
                "motif_operations": ["augmentation"],
            },
        ],
        "long_form_phrase_rules": {},
    }


def composition(phrase: dict) -> dict:
    return {
        "metadata": {
            "title": "Synthetic Long Form Test",
            "tempo": 100,
            "time_signature": "4/4",
            "key": "explicit test palette",
        },
        "sections": [{"name": "solo", "bars": 4}],
        "tracks": {
            "lead_guitar": {
                "role": "lead",
                "sections": {
                    "solo": {
                        "loop_bars": 4,
                        "instrument_phrase": phrase,
                    }
                },
            }
        },
    }


class LongFormPhraseTests(unittest.TestCase):
    def test_relationship_labels_do_not_compose_notes(self) -> None:
        phrase = neutral_phrase()
        validate_composition(composition(phrase))
        events = compile_instrument_phrase(phrase, 4)

        self.assertEqual([note_number(event["pitch"]) for event in events], [60] * 12)
        self.assertEqual(
            [round(position(event["at"], 4) % 4, 3) for event in events],
            [0.0, 1.0, 2.0] * 4,
        )
        self.assertEqual([event["duration"] for event in events], [0.5] * 12)
        self.assertFalse(any(event.get("vibrato") for event in events))
        self.assertFalse(any(event.get("bend_semitones") for event in events))
        self.assertEqual(phrase["_long_form_plan"]["execution_policy"], "authored_only")
        self.assertEqual(
            phrase["_long_form_plan"]["performance_shaping"]["note_length_model"],
            "authored",
        )

    def test_only_explicit_transform_changes_material(self) -> None:
        phrase = neutral_phrase()
        phrase["phrase_relationships"][1]["transform"] = {
            "degree_shift": 2,
            "time_scale": 0.5,
        }
        events = compile_instrument_phrase(phrase, 4)
        second = [event for event in events if 4 <= position(event["at"], 4) < 8]

        self.assertEqual([note_number(event["pitch"]) for event in second], [62, 62, 62])
        self.assertEqual(
            [round(position(event["at"], 4) - 4, 3) for event in second],
            [0.0, 0.5, 1.0],
        )
        self.assertEqual([event["duration"] for event in second], [0.25, 0.25, 0.25])

    def test_validator_counts_only_explicit_development(self) -> None:
        plain = composition(neutral_phrase())
        plain_report = analyze_long_form_phrases(plain)
        self.assertEqual(
            plain_report["sections"][0]["assessment"]["motif_developments"],
            0,
        )

        transformed_phrase = neutral_phrase()
        transformed_phrase["phrase_relationships"][1]["transform"] = {"degree_shift": 1}
        transformed = composition(transformed_phrase)
        transformed_report = analyze_long_form_phrases(transformed)
        self.assertEqual(
            transformed_report["sections"][0]["assessment"]["motif_developments"],
            1,
        )

    def test_authored_duration_may_cross_bar_without_special_permission(self) -> None:
        phrase = neutral_phrase()
        phrase["motif_seed"] = [
            {"offset": 3.5, "duration": 0.75, "degree": 0},
        ]
        phrase["phrase_relationships"] = [
            {
                "phrase_id": "P",
                "bars": [1, 4],
                "relationship": "introduce",
                "continuation_from": None,
                "continuation_to": None,
                "resolution": "deferred",
                "motif_operations": [],
            }
        ]
        validate_composition(composition(phrase))
        events = compile_instrument_phrase(phrase, 4)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["duration"], 0.75)
        self.assertTrue(events[0]["_cross_bar"])

    def test_schema_does_not_require_a_peak_or_final_tonic_plan(self) -> None:
        data = composition(neutral_phrase())
        validate_composition(data)

    def test_validator_measures_but_does_not_judge_without_rules(self) -> None:
        data = composition(neutral_phrase())
        validate_composition(data)
        report = analyze_long_form_phrases(data)
        self.assertEqual(report["error_count"], 0)
        self.assertEqual(report["warning_count"], 0)
        self.assertEqual(report["sections"][0]["assessment"]["active_style_rules"], [])

    def test_validator_only_enforces_explicit_style_rule(self) -> None:
        phrase = neutral_phrase()
        phrase["section_arc"]["peak_bar"] = 4
        phrase["long_form_phrase_rules"] = {"require_delayed_peak": True}
        data = composition(phrase)
        validate_composition(data)
        report = analyze_long_form_phrases(data)
        codes = [item["code"] for item in report["diagnostics"]]
        self.assertIn("early_peak", codes)

    def test_authored_mode_exports_plan(self) -> None:
        data = composition(neutral_phrase())
        validate_composition(data)
        plans = export_long_form_plans(data, 4)["plans"]
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0]["execution_policy"], "authored_only")


if __name__ == "__main__":
    unittest.main()
