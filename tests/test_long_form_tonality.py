from __future__ import annotations

import unittest

from src.melody.tonality import resolve_tonality


class LongFormTonalityTests(unittest.TestCase):
    def test_missing_tonality_is_rejected_instead_of_inventing_e_minor(self) -> None:
        with self.assertRaisesRegex(ValueError, "explicit tonality"):
            resolve_tonality({})

    def test_legacy_key_root_does_not_infer_minor_mode(self) -> None:
        with self.assertRaisesRegex(ValueError, "explicit mode"):
            resolve_tonality({"key_root": "C"})

    def test_explicit_tonality_requires_tonic(self) -> None:
        with self.assertRaisesRegex(ValueError, "tonality.tonic"):
            resolve_tonality({"tonality": {"mode": "major"}})

    def test_explicit_tonality_requires_mode_or_scale(self) -> None:
        with self.assertRaisesRegex(ValueError, "tonality.mode"):
            resolve_tonality({"tonality": {"tonic": "C"}})

    def test_custom_chromatic_palette_is_preserved(self) -> None:
        pitch_classes, descriptor = resolve_tonality({
            "tonality": {"tonic": "C", "scale_intervals": list(range(12))}
        })
        self.assertEqual(pitch_classes, set(range(12)))
        self.assertEqual(descriptor["source"], "explicit")
        self.assertEqual(descriptor["mode"], "custom")

    def test_explicit_legacy_key_root_still_has_compatibility_route(self) -> None:
        pitch_classes, descriptor = resolve_tonality({"key_root": "C", "mode": "major"})
        self.assertEqual(descriptor["source"], "legacy_key_root")
        self.assertEqual(descriptor["tonic"], "C")
        self.assertEqual(descriptor["mode"], "major")
        self.assertEqual(pitch_classes, {0, 2, 4, 5, 7, 9, 11})

    def test_unknown_mode_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported long-form tonality mode"):
            resolve_tonality({"tonality": {"tonic": "D", "mode": "banana"}})


if __name__ == "__main__":
    unittest.main()
