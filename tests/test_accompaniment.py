from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import mido

from src.accompaniment import analyze_continuity, generate_texture_events, materialize_clip, plan_smooth_voicings
from src.composition import load_composition, validate_composition
from src.midi import generate_song_midis


ROOT = Path(__file__).resolve().parents[1]
SPANS = [
    {"at": "1:1", "duration": 4.0, "pitches": ["C3", "E3", "G3"]},
    {"at": "2:1", "duration": 4.0, "pitches": ["A2", "C3", "E3"]},
    {"at": "3:1", "duration": 4.0, "pitches": ["F2", "A2", "C3"]},
    {"at": "4:1", "duration": 4.0, "pitches": ["G2", "B2", "D3"]},
]


class AccompanimentTests(unittest.TestCase):
    def test_old_composition_and_midi_are_unchanged_without_texture_fields(self) -> None:
        path = ROOT / "projects" / "demo_song" / "composition.json"
        composition = load_composition(path)
        instruments = json.loads((ROOT / "config" / "instruments.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_paths = generate_song_midis(composition, instruments, Path(first))
            second_paths = generate_song_midis(deepcopy(composition), instruments, Path(second))
            for track in composition["tracks"]:
                self.assertEqual(first_paths[track].read_bytes(), second_paths[track].read_bytes())

    def test_all_eight_textures_materialize_distinct_rules(self) -> None:
        signatures = {}
        for texture in ("sustain", "pulse", "broken_chord", "arpeggio", "ostinato", "counterline", "stab", "pedal"):
            events = generate_texture_events(texture, SPANS, pattern={"register": [55, 72], "voices": 3})
            self.assertTrue(events, texture)
            signatures[texture] = (len(events), round(sum(event["duration"] for event in events), 2), events[0]["type"])
        self.assertEqual(len(set(signatures.values())), 8)

    def test_arpeggio_contour_continues_across_chord_boundary(self) -> None:
        events = generate_texture_events("arpeggio", SPANS[:2], pattern={"register": [60, 76], "voices": 3, "step": 0.75})
        boundary = [event for event in events if event["at"].startswith("2:")][0]
        previous = [event for event in events if event["at"].startswith("1:")][-1]
        # It must not forcibly reset to the lowest note of the new chord.
        new_lowest = min(plan_smooth_voicings(SPANS[:2], (60, 76), 3)[1])
        from src.midi.pitches import note_number
        self.assertLessEqual(abs(note_number(boundary["pitch"]) - note_number(previous["pitch"])), 7)
        self.assertNotEqual(note_number(boundary["pitch"]), new_lowest)

    def test_sustain_retains_common_tones_as_single_long_notes(self) -> None:
        events = generate_texture_events("sustain", SPANS[:2], pattern={"register": [55, 72], "voices": 3})
        self.assertTrue(any(event["duration"] >= 7.9 for event in events))
        self.assertTrue(all(event["duration"] >= 3.9 for event in events))

    def test_section_texture_override_wins_and_validates_continuity(self) -> None:
        clip = {"loop_bars": 4, "texture": "arpeggio", "continuity": {"legato_ratio": 0.9}, "harmony_spans": SPANS, "events": []}
        events = materialize_clip(clip, {"texture": "sustain"}, 4)
        self.assertGreater(len(events), 12)
        invalid = json.loads((ROOT / "projects" / "demo_song" / "composition.json").read_text(encoding="utf-8"))
        invalid["tracks"]["pad"]["texture"] = "cloud"
        with self.assertRaisesRegex(ValueError, "texture"):
            validate_composition(invalid)

    def test_after_keeps_source_melody_events(self) -> None:
        source = load_composition(ROOT / "projects" / "benchmarks" / "01_galgame" / "composition.json")
        after = load_composition(ROOT / "projects" / "accompaniment_continuity_demo" / "after_continuity" / "composition.json")
        from src.midi.pitches import note_number
        for section in source["tracks"]["piano"]["sections"]:
            expected = [event for event in source["tracks"]["piano"]["sections"][section]["events"] if event.get("type", "note") == "note" and note_number(event["pitch"]) >= note_number("D4") and event["velocity"] >= 62]
            actual = after["tracks"]["piano"]["sections"][section]["events"]
            self.assertEqual(expected, actual)

    def test_before_after_continuity_improves_and_balances_point_line_plane(self) -> None:
        base = ROOT / "projects" / "accompaniment_continuity_demo"
        before = analyze_continuity(load_composition(base / "before_continuity" / "composition.json"))
        after = analyze_continuity(load_composition(base / "after_continuity" / "composition.json"))
        self.assertGreater(before["warning_count"], after["warning_count"])
        for section in ("a", "b", "return"):
            balance = after["section_metrics"][section]["point_line_plane_balance"]
            self.assertGreater(balance["point"], 0)
            self.assertGreater(balance["line"], 0)
            self.assertGreater(balance["plane"], 0)

    def test_generated_demo_midi_has_no_same_pitch_overlaps_or_stuck_notes(self) -> None:
        path = ROOT / "projects" / "accompaniment_continuity_demo" / "after_continuity" / "output" / "full_song.mid"
        midi = mido.MidiFile(path)
        for track in midi.tracks:
            active = set()
            for message in track:
                if message.type == "note_on" and message.velocity > 0:
                    key = (message.channel, message.note)
                    self.assertNotIn(key, active)
                    active.add(key)
                elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                    active.discard((message.channel, message.note))
            self.assertFalse(active)


if __name__ == "__main__":
    unittest.main()
