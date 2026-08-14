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
        self.assertEqual(pitch_classes, {0, 2, 4, 6, 7, 9, 11})

    def test_explicit_major_and_borrowed_interval_are_preserved(self) -> None:
        major, descriptor = resolve_tonality({"tonality": {"tonic": "D", "mode": "major"}})
        borrowed, borrowed_descriptor = resolve_tonality({
            "tonality": {"tonic": "D", "mode": "major", "additional_intervals": [10]}
        })
        self.assertIn(1, major)
        self.assertNotIn(0, major)
        self.assertIn(0, borrowed)
        self.assertEqual(descriptor["mode"], "major")
        self.assertEqual(borrowed_descriptor["additional_intervals"], [10])

    def test_unknown_mode_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported long-form tonality mode"):
            resolve_tonality({"tonality": {"tonic": "D", "mode": "banana"}})

    def test_demo_uses_palette_and_guitar_performance_shaping(self) -> None:
        composition = load_composition(DEMO / "composition.json")
        phrase = composition["tracks"]["lead_guitar"]["sections"]["solo"]["instrument_phrase"]
        events = compile_instrument_phrase(phrase, 4)
        plan = export_long_form_plans(composition, 4)["plans"][0]
        allowed = set(plan["tonality"]["pitch_classes"])

        self.assertEqual(plan["tonality"]["tonic"], "D")
        self.assertEqual(plan["tonality"]["mode"], "major")
        self.assertEqual(plan["performance_shaping"]["note_length_model"], "guitar_gate_cycles")
        self.assertTrue(all(note_number(event["pitch"]) % 12 in allowed for event in events))
        self.assertTrue(any(event.get("slide_from_semitones") is not None for event in events))
        self.assertTrue(any(event.get("_legato_pitch_fallback") for event in events))
        self.assertTrue(any(event.get("vibrato") for event in events))

        durations = [round(float(event["duration"]), 3) for event in events]
        velocities = [int(event["velocity"]) for event in events]
        self.assertGreaterEqual(len(set(durations)), 8)
        self.assertGreaterEqual(max(durations), 1.4)
        self.assertLessEqual(min(durations), 0.25)
        self.assertGreaterEqual(len(set(velocities)), 6)
        self.assertGreaterEqual(max(velocities) - min(velocities), 12)

        starts = [position(event["at"], 4) for event in events]
        ends = [start + float(event["duration"]) for start, event in zip(starts, events)]
        near_connected = sum(next_start - end <= 0.08 for end, next_start in zip(ends, starts[1:]))
        self.assertGreaterEqual(near_connected / max(1, len(events) - 1), 0.35)

        pitches = [note_number(event["pitch"]) for event in events]
        repeats = sum(left == right for left, right in zip(pitches, pitches[1:]))
        self.assertGreaterEqual(repeats, 6)
        self.assertEqual(pitches[-1] % 12, plan["tonality"]["tonic_pitch_class"])
        self.assertGreaterEqual(events[-1]["duration"], 1.4)


if __name__ == "__main__":
    unittest.main()
