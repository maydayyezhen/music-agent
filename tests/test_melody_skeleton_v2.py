from __future__ import annotations

import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path

import mido

from src.composition import load_composition, validate_composition
from src.instruments import compile_instrument_phrase
from src.validation import validate_melody_skeleton

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "lead_guitar_long_form_v2"


class MelodySkeletonV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_melody_skeleton_v2.py")], cwd=ROOT)
        if result.returncode: raise RuntimeError("melody skeleton builder failed")

    def test_skeleton_is_strictly_monophonic_and_effect_free(self) -> None:
        payload = json.loads((FIXTURE / "melody_skeleton_v2.json").read_text(encoding="utf-8"))
        report = validate_melody_skeleton(payload["plan"], payload["notes"], FIXTURE / "melody_skeleton_v2.mid")
        self.assertTrue(report["passed"], report["failures"])
        metrics = report["metrics"]
        self.assertTrue(metrics["monophonic"]); self.assertEqual(metrics["pitch_bends"], 0)
        self.assertEqual(metrics["overlapping_different_pitches"], 0); self.assertEqual(metrics["articulation_keyswitches"], 0)
        self.assertEqual(metrics["random_cc"], 0); self.assertEqual(metrics["peak_bar"], 7)
        self.assertEqual(metrics["final_resolution_bar"], 8); self.assertGreaterEqual(metrics["primary_motif_occurrences"], 3)
        self.assertGreaterEqual(metrics["motif_developments"], 2); self.assertEqual(metrics["unrelated_phrase_fragments"], 0)

    def test_default_mode_is_legacy_stable(self) -> None:
        legacy = load_composition(ROOT / "projects" / "instrument_aware_demos" / "03_lead_guitar_expression" / "composition.json")
        phrase = legacy["tracks"]["lead_guitar"]["sections"]["lead"]["instrument_phrase"]
        self.assertNotIn("phrase_generation_mode", phrase)
        events_without_field = compile_instrument_phrase(deepcopy(phrase), 4)
        explicit = deepcopy(phrase); explicit["phrase_generation_mode"] = "legacy_stable"
        self.assertEqual(events_without_field, compile_instrument_phrase(explicit, 4))

    def test_experimental_mode_must_be_explicit(self) -> None:
        composition = load_composition(ROOT / "projects" / "long_form_phrase_demos" / "01_singing_lead_8bar" / "composition.json")
        phrase = composition["tracks"]["lead_guitar"]["sections"]["solo"]["instrument_phrase"]
        self.assertEqual(phrase["phrase_generation_mode"], "long_form_experimental")
        stable = deepcopy(phrase); stable["phrase_generation_mode"] = "legacy_stable"; stable["motif"] = [
            {"pitch": "E4", "at": "1:1", "duration": 1, "articulations": ["sustain"]}
        ]
        self.assertEqual(len(compile_instrument_phrase(stable, 4)), 1)
        experimental = deepcopy(phrase); experimental["phrase_generation_mode"] = "long_form_experimental"
        validate_composition({**composition, "tracks": {"lead_guitar": {**composition["tracks"]["lead_guitar"], "sections": {"solo": {**composition["tracks"]["lead_guitar"]["sections"]["solo"], "instrument_phrase": experimental}}}}})

    def test_pitch_bend_is_dropped_when_channel_has_overlap(self) -> None:
        from src.midi.generator import NoteEvent, _musical_track
        track = _musical_track("lead", {"bank": 0, "program": 30}, 0, [
            NoteEvent(0, 2, 64, 80, pitch_curve=((.5, 4096), (1.5, 0))),
            NoteEvent(1, 2, 67, 80),
        ])
        self.assertFalse(any(message.type == "pitchwheel" for message in track))


if __name__ == "__main__": unittest.main()
