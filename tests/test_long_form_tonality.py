from __future__ import annotations

import unittest
from pathlib import Path

from src.composition import load_composition
from src.instruments import compile_instrument_phrase, export_long_form_plans
from src.instruments.common import position
from src.melody.tonality import resolve_tonality
from src.midi.pitches import note_number


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "projects" / "connected_lead_reference_demo"


class LongFormTonalityTests(unittest.TestCase):
    def test_legacy_key_root_remains_natural_minor(self) -> None:
        pitch_classes, descriptor = resolve_tonality({"key_root": "E"})
        self.assertEqual(descriptor["source"], "legacy_key_root")
        self.assertEqual(descriptor["mode"], "natural_minor")
        self.assertEqual(pitch_classes, {1, 2, 4, 6, 7, 9, 11})

    def test_explicit_major_and_borrowed_interval_are_preserved(self) -> None:
        major, descriptor = resolve_tonality({"tonality": {"tonic": "D", "mode": "major"}})
        borrowed, borrowed_descriptor = resolve_tonality({"tonality": {"tonic": "D", "mode": "major", "additional_intervals": [10]}})
        self.assertIn(1, major)
        self.assertNotIn(0, major)
        self.assertIn(0, borrowed)
        self.assertEqual(descriptor["mode"], "major")
        self.assertEqual(borrowed_descriptor["additional_intervals"], [10])

    def test_unknown_mode_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported long-form tonality mode"):
            resolve_tonality({"tonality": {"tonic": "D", "mode": "banana"}})

    def test_demo_uses_palette_and_preserves_expression_metadata(self) -> None:
        composition = load_composition(DEMO / "composition.json")
        phrase = composition["tracks"]["lead_guitar"]["sections"]["solo"]["instrument_phrase"]
        events = compile_instrument_phrase(phrase, 4)
        plan = export_long_form_plans(composition, 4)["plans"][0]
        allowed = set(plan["tonality"]["pitch_classes"])
        self.assertEqual(plan["tonality"]["tonic"], "D")
        self.assertEqual(plan["tonality"]["mode"], "major")
        self.assertTrue(all(note_number(event["pitch"]) % 12 in allowed for event in events))
        self.assertTrue(any(event.get("slide_from_semitones") is not None for event in events))
        self.assertTrue(any(event.get("vibrato") for event in events))
        starts = [position(event["at"], 4) for event in events]
        ends = [start + float(event["duration"]) for start, event in zip(starts, events)]
        connected = sum(next_start - end <= 0.05 for end, next_start in zip(ends, starts[1:]))
        self.assertGreaterEqual(connected / max(1, len(events) - 1), 0.60)
        pitches = [note_number(event["pitch"]) for event in events]
        repeats = sum(left == right for left, right in zip(pitches, pitches[1:]))
        self.assertGreaterEqual(repeats, 6)
        self.assertEqual(pitches[-1] % 12, plan["tonality"]["tonic_pitch_class"])


if __name__ == "__main__":
    unittest.main()
