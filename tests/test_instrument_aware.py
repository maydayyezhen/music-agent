from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import mido

from src.accompaniment.generator import materialize_clip
from src.composition import load_composition, validate_composition
from src.midi import generate_song_midis
from src.instruments import compile_instrument_phrase
from src.performance import apply_profile, load_profile
from src.validation import analyze_instrument_aware

ROOT = Path(__file__).resolve().parents[1]
DEMOS = ROOT / "projects" / "instrument_aware_demos"


class InstrumentAwareTests(unittest.TestCase):
    def test_lead_preserves_authored_fretboard_path_and_slide_curve(self) -> None:
        phrase = {
            "instrument": "electric_lead_guitar", "role": "lead", "phrase_type": "melodic_lead",
            "energy": 0.8, "motif": [{
                "pitch": "G4", "at": "1:1", "duration": 1.0, "articulations": ["slide"],
                "planned_string": 3, "planned_fret": 12, "slide_from_semitones": -2.0,
            }], "performance_intent": {"seed": 9},
        }
        events = compile_instrument_phrase(phrase, 4)
        self.assertEqual(events[0]["_string"], 3)
        self.assertEqual(events[0]["_fret"], 12)
        self.assertEqual(events[0]["slide_from_semitones"], -2.0)

    def test_lead_rejects_impossible_authored_fretboard_path(self) -> None:
        phrase = {
            "instrument": "electric_lead_guitar", "role": "lead", "phrase_type": "melodic_lead",
            "energy": 0.8, "motif": [{"pitch": "G4", "at": "1:1", "duration": 1,
                                         "planned_string": 5, "planned_fret": 1}],
            "performance_intent": {"seed": 10},
        }
        with self.assertRaisesRegex(ValueError, "planned string/fret"):
            compile_instrument_phrase(phrase, 4)
    def test_legacy_midi_path_remains_byte_stable(self) -> None:
        composition = load_composition(ROOT / "projects" / "demo_song" / "composition.json")
        instruments = json.loads((ROOT / "config" / "instruments.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = generate_song_midis(composition, instruments, Path(first))
            two = generate_song_midis(deepcopy(composition), instruments, Path(second))
            self.assertEqual(one["full_song"].read_bytes(), two["full_song"].read_bytes())

    def test_semantic_phrase_requires_seed_and_cannot_mix_final_events(self) -> None:
        composition = load_composition(DEMOS / "01_rhythm_guitar_palm_muted_verse" / "composition.json")
        invalid = deepcopy(composition)
        phrase = invalid["tracks"]["rhythm_guitar"]["sections"]["verse"]["instrument_phrase"]
        del phrase["performance_intent"]["seed"]
        with self.assertRaisesRegex(ValueError, "deterministic seed"):
            validate_composition(invalid)
        invalid = deepcopy(composition)
        invalid["tracks"]["rhythm_guitar"]["sections"]["verse"]["events"] = [
            {"type": "note", "pitch": "E3", "at": "1:1", "duration": 1, "velocity": 80}
        ]
        with self.assertRaisesRegex(ValueError, "cannot mix"):
            validate_composition(invalid)

    def test_rhythm_guitar_has_physical_strum_and_fret_assignments(self) -> None:
        composition = load_composition(DEMOS / "01_rhythm_guitar_palm_muted_verse" / "composition.json")
        track = composition["tracks"]["rhythm_guitar"]
        clip = track["sections"]["verse"]
        events = materialize_clip(clip, track, 4)
        groups: dict[str, list[dict[str, object]]] = {}
        for event in events:
            groups.setdefault(str(event["_attack_group"]), []).append(event)
            self.assertIn("_string", event); self.assertIn("_fret", event)
            self.assertIn("palm_mute", event["articulations"])
        first = next(iter(groups.values()))
        self.assertEqual(len({event["at"] for event in first}), len(first))
        self.assertEqual(len({event["_string"] for event in first}), len(first))

    def test_lead_profile_emits_real_pitchwheel_messages(self) -> None:
        folder = DEMOS / "03_lead_guitar_expression"
        composition = load_composition(folder / "composition.json")
        instruments = json.loads((folder / "instruments.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            paths = generate_song_midis(composition, instruments, Path(temporary))
            messages = [message for track in mido.MidiFile(paths["lead_guitar"]).tracks for message in track]
        self.assertTrue(any(message.type == "pitchwheel" and message.pitch != 0 for message in messages))

    def test_ample_profile_maps_semantics_without_changing_composer(self) -> None:
        event = {"type": "note", "pitch": "E3", "at": "1:1", "duration": 1.0,
                 "velocity": 80, "articulations": ["palm_mute"]}
        ample, report = apply_profile([event], load_profile("ample_guitar_v4"))
        gm, gm_report = apply_profile([event], load_profile("general_midi"))
        self.assertEqual(ample[0]["profile_triggers"][0]["note"], 26)
        self.assertLess(gm[0]["duration"], event["duration"])
        self.assertEqual(report["articulation_coverage"]["palm_mute"]["mapped"], 1)
        self.assertEqual(gm_report["articulation_coverage"]["palm_mute"]["fallback"], 1)

    def test_all_seven_minimum_demos_validate_and_render_non_silent(self) -> None:
        folders = sorted(path for path in DEMOS.iterdir() if path.is_dir())
        self.assertEqual(len(folders), 7)
        for folder in folders:
            composition = load_composition(folder / "composition.json")
            report = analyze_instrument_aware(composition)
            self.assertEqual(report["error_count"], 0, folder.name)
            self.assertEqual(report["warning_count"], 0, folder.name)
            self.assertTrue((folder / "semantic_phrases.json").is_file())
            self.assertTrue((folder / "validation-report.json").is_file())
            self.assertGreater((folder / "output" / "final.wav").stat().st_size, 100_000)
            self.assertGreater((folder / "output" / "full_song.mid").stat().st_size, 100)

    def test_note_spacing_analysis_reports_no_semantic_same_pitch_overlaps(self) -> None:
        composition = load_composition(ROOT / "projects" / "instrument_aware_full_song" / "composition.json")
        report = analyze_instrument_aware(composition)
        overlaps = sum(
            section["note_spacing"]["same_pitch_overlap_count"]
            for track in report["track_metrics"].values()
            for section in track["sections"].values()
        )
        self.assertEqual(overlaps, 0)

    def test_full_song_semantic_midis_have_no_same_pitch_overlap_or_stuck_notes(self) -> None:
        folder = ROOT / "projects" / "instrument_aware_full_song"
        composition = load_composition(folder / "composition.json")
        instruments = json.loads((folder / "instruments.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            paths = generate_song_midis(composition, instruments, Path(temporary))
            for name in composition["tracks"]:
                active: set[tuple[int, int]] = set()
                for track in mido.MidiFile(paths[name]).tracks:
                    for message in track:
                        if message.type == "note_on" and message.velocity > 0:
                            key = (message.channel, message.note)
                            self.assertNotIn(key, active, f"{name}: {key}")
                            active.add(key)
                        elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                            active.discard((message.channel, message.note))
                self.assertFalse(active, name)


if __name__ == "__main__":
    unittest.main()
