from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import mido

from src.composition import load_composition, validate_composition
from src.instruments import compile_instrument_phrase, export_long_form_plans
from src.midi import generate_song_midis
from src.validation import analyze_long_form_phrases

ROOT = Path(__file__).resolve().parents[1]
DEMOS = ROOT / "projects" / "long_form_phrase_demos"


class LongFormPhraseTests(unittest.TestCase):
    def test_eight_bar_singing_lead_meets_acceptance(self) -> None:
        composition = load_composition(DEMOS / "01_singing_lead_8bar" / "composition.json")
        report = analyze_long_form_phrases(composition)
        metrics = report["sections"][0]["assessment"]
        self.assertEqual(report["warning_count"], 0)
        self.assertEqual(metrics["strong_cadences"], 1)
        self.assertGreaterEqual(metrics["cross_bar_notes"], 2)
        self.assertGreaterEqual(min(metrics["peak_bars"]), 3)
        phrase = composition["tracks"]["lead_guitar"]["sections"]["solo"]["instrument_phrase"]
        events = compile_instrument_phrase(phrase, 4)
        # Experimental realization now defaults to the safe skeleton: planning is
        # preserved, but guitar effects require an explicit realization opt-in.
        articulations = {art for event in events for art in event.get("articulations", [])}
        self.assertNotIn("slide", articulations)
        self.assertNotIn("legato", articulations)
        self.assertTrue(all(event.get("bend_semitones") is None and event.get("vibrato") is None for event in events))

    def test_sixteen_bar_solo_exports_all_three_planning_layers(self) -> None:
        composition = load_composition(DEMOS / "02_developing_solo_16bar" / "composition.json")
        plan = export_long_form_plans(composition, 4)["plans"][0]
        self.assertEqual(plan["section_arc"]["peak_bar"], 12)
        self.assertGreaterEqual(len({op for rel in plan["phrase_relationships"] for op in rel["motif_operations"]}), 3)
        self.assertEqual(len(plan["melodic_state_trace"]), 8)
        self.assertTrue(all(item["continuation_required"] for item in plan["melodic_state_trace"]
                            if item["point"] == "end" and item["phrase_id"] != "C"))

    def test_ab_midis_differ_and_long_form_metrics_improve(self) -> None:
        folder = DEMOS / "03_legacy_vs_long_form_ab"
        comparison = json.loads((folder / "ab-comparison-report.json").read_text(encoding="utf-8"))
        self.assertNotEqual((folder / "legacy_short_phrase.mid").read_bytes(), (folder / "long_form_phrase.mid").read_bytes())
        self.assertGreater(comparison["legacy"]["independent_endings"], comparison["long_form"]["independent_endings"])
        self.assertLess(comparison["legacy"]["cross_bar_connections"], comparison["long_form"]["cross_bar_connections"])
        self.assertEqual(comparison["long_form"]["peak_bar"], [12])

    def test_schema_rejects_incomplete_long_form_but_legacy_stays_valid(self) -> None:
        composition = load_composition(DEMOS / "01_singing_lead_8bar" / "composition.json")
        invalid = deepcopy(composition)
        del invalid["tracks"]["lead_guitar"]["sections"]["solo"]["instrument_phrase"]["section_arc"]
        with self.assertRaisesRegex(ValueError, "long_form phrase is missing"):
            validate_composition(invalid)
        validate_composition(load_composition(DEMOS / "03_legacy_vs_long_form_ab" / "legacy_composition.json"))

    def test_long_form_export_has_no_same_pitch_overlap_or_stuck_notes(self) -> None:
        folder = DEMOS / "02_developing_solo_16bar"
        composition = load_composition(folder / "composition.json")
        instruments = json.loads((folder / "instruments.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            path = generate_song_midis(composition, instruments, Path(temporary))["lead_guitar"]
            active: set[tuple[int, int]] = set()
            for track in mido.MidiFile(path).tracks:
                for message in track:
                    if message.type == "note_on" and message.velocity > 0:
                        key = (message.channel, message.note); self.assertNotIn(key, active); active.add(key)
                    elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                        active.discard((message.channel, message.note))
            self.assertFalse(active)


if __name__ == "__main__": unittest.main()
