from __future__ import annotations

import unittest
from collections import defaultdict
from statistics import mean

from src.instruments import compile_instrument_phrase
from src.midi.generator import derive_foreground_activity
from src.validation import analyze_strumming_flow


def phrase(instrument="acoustic_guitar", phrase_type="continuous_strumming", pattern="verse_a"):
    return {
        "instrument": instrument, "role": "verse rhythm guitar", "phrase_type": phrase_type,
        "energy": .6, "strumming_pattern": pattern,
        "harmony": [{"at": "1:1", "duration": 4, "chord": "G"}, {"at": "2:1", "duration": 4, "chord": "D"}],
        "performance_intent": {"seed": 17},
    }


def sixteenth_phrase(*, foreground=None, sustain=True):
    value = {
        "instrument": "acoustic_guitar", "role": "rhythm guitar", "phrase_type": "continuous_strumming",
        "energy": .65, "subdivision": "sixteenth", "strumming_pattern": "sixteenth_flow",
        "four_bar_variation": True, "per_string_sustain": sustain,
        "harmony": [{"at": f"{bar}:1", "duration": 4, "chord": chord}
                    for bar, chord in enumerate(["G", "D", "Em", "C"], 1)],
        "performance_intent": {"seed": 1716},
    }
    if foreground is not None:
        value["foreground_aware"] = True
        value["foreground_activity"] = foreground
    return value


class StrummingContinuityTests(unittest.TestCase):
    def test_grid_keeps_air_motion_and_expands_sounding_actions(self):
        source = phrase()
        events = compile_instrument_phrase(source, 4)
        bars = source["_strumming_debug"]["bars"]
        self.assertEqual([bar["hand_motion_count"] for bar in bars], [8, 8])
        self.assertEqual([bar["sounding_strum_count"] for bar in bars], [6, 6])
        self.assertIn("air_strum", bars[0]["actions"])
        groups = {event["_attack_group"] for event in events}
        self.assertEqual(len(groups), 12)
        self.assertTrue(all("_hand_step" in event and "_strum_action" in event for event in events))

    def test_generic_continuous_strumming_does_not_default_to_breathing_gaps(self):
        source = phrase()
        source.pop("strumming_pattern")
        compile_instrument_phrase(source, 4)
        bars = source["_strumming_debug"]["bars"]
        self.assertTrue(all(bar["pattern_id"] == "steady_eighths" for bar in bars))
        self.assertTrue(all(bar["sounding_strum_count"] == 8 for bar in bars))
        self.assertTrue(all("air_strum" not in bar["actions"] for bar in bars))

    def test_explicit_breathing_mode_can_request_gaps_without_a_pattern_id(self):
        source = phrase()
        source.pop("strumming_pattern")
        source["strumming_continuity"] = "breathing"
        compile_instrument_phrase(source, 4)
        bars = source["_strumming_debug"]["bars"]
        self.assertTrue(all(bar["pattern_id"] == "verse_a" for bar in bars))
        self.assertTrue(all("air_strum" in bar["actions"] for bar in bars))

    def test_hand_direction_continues_across_bar_and_chord(self):
        source = phrase(pattern="steady_eighths")
        events = compile_instrument_phrase(source, 4)
        bars = source["_strumming_debug"]["bars"]
        self.assertEqual(bars[0]["last_hand_direction"], "up")
        self.assertEqual(bars[0]["next_expected_direction"], bars[1]["hand_motion"][0])
        self.assertTrue(bars[0]["pattern_continues_across_bar"])
        starts = {(event["at"], event["_hand_direction"]) for event in events}
        self.assertTrue(any(at.startswith("1:4.5") and direction == "up" for at, direction in starts))
        self.assertTrue(any(at == "2:1" and direction == "down" for at, direction in starts))

    def test_sustained_hit_is_explicitly_distinct(self):
        source = phrase(phrase_type="sustained_chord_hit", pattern="single_hit")
        events = compile_instrument_phrase(source, 4)
        groups = {event["_attack_group"] for event in events}
        self.assertEqual(len(groups), 2)
        self.assertGreater(max(event["duration"] for event in events), 3.5)
        self.assertEqual(source["_strumming_debug"]["bars"][0]["sounding_strum_count"], 1)

    def test_muted_strum_does_not_stack_gate_articulations(self):
        source = phrase(pattern="steady_eighths")
        events = compile_instrument_phrase(source, 4)
        muted = [event for event in events if event.get("_strum_action") == "muted_strum"]
        self.assertTrue(muted)
        self.assertTrue(all(event.get("articulations", []).count("palm_mute") == 1 for event in muted))
        self.assertTrue(all("staccato" not in event.get("articulations", []) for event in muted))

    def test_acoustic_and_electric_patterns_are_independent(self):
        acoustic = phrase(pattern="chorus_open")
        electric = phrase(instrument="electric_rhythm_guitar", pattern="classic_pop")
        acoustic_events = compile_instrument_phrase(acoustic, 4)
        electric_events = compile_instrument_phrase(electric, 4)
        self.assertNotEqual(acoustic["_strumming_debug"]["bars"][0]["actions"], electric["_strumming_debug"]["bars"][0]["actions"])
        self.assertNotEqual(len({event["_attack_group"] for event in acoustic_events}), len({event["_attack_group"] for event in electric_events}))

    def test_sixteenth_grid_has_sixteen_alternating_hand_positions(self):
        source = sixteenth_phrase()
        compile_instrument_phrase(source, 4)
        for bar in source["_strumming_debug"]["bars"]:
            self.assertEqual(bar["subdivision"], "sixteenth")
            self.assertEqual(bar["hand_motion_count"], 16)
            self.assertEqual(bar["hand_motion"], ["down" if step % 2 == 0 else "up" for step in range(16)])
            self.assertIn("air_strum", bar["actions"])

    def test_generic_sixteenth_continuous_strumming_starts_dense_not_gapped(self):
        source = sixteenth_phrase()
        source.pop("strumming_pattern")
        compile_instrument_phrase(source, 4)
        bars = source["_strumming_debug"]["bars"]
        self.assertTrue(all(bar["pattern_id"] == "sixteenth_continuous" for bar in bars))
        self.assertEqual(bars[0]["sounding_strum_count"], 16)
        self.assertNotIn("air_strum", bars[0]["actions"])

    def test_four_bar_variants_are_related_not_random_replacements(self):
        source = sixteenth_phrase()
        compile_instrument_phrase(source, 4)
        debug = source["_four_bar_variation_debug"]
        self.assertEqual(len({item["variant_id"] for item in debug["bars"]}), 4)
        base = debug["base_actions"]
        for item in debug["bars"]:
            distance = sum(left != right for left, right in zip(base, item["actions"]))
            self.assertLessEqual(distance, 4)

    def test_per_string_state_retains_unselected_strings_without_pitch_overlap(self):
        source = sixteenth_phrase()
        events = compile_instrument_phrase(source, 4)
        steps = source["_per_string_state_debug"]["steps"]
        self.assertTrue(any(item["previous_attack_still_sounding"] for item in steps if item["action"] != "air_strum"))
        self.assertEqual(sum(item["cross_bar_sustain"] for item in steps), 3)
        by_pitch = defaultdict(list)
        for event in events:
            bar, beat = event["at"].split(":")
            start = (int(bar) - 1) * 4 + float(beat) - 1
            by_pitch[event["pitch"]].append((start, start + float(event["duration"])))
        overlaps = 0
        for lane in by_pitch.values():
            lane.sort()
            overlaps += sum(left[1] > right[0] for left, right in zip(lane, lane[1:]))
        self.assertEqual(overlaps, 0)

    def test_foreground_thins_voicing_and_velocity_without_stopping_hand(self):
        active = [{"bar": bar, "active_steps": list(range(16)), "release_steps": list(range(10, 16))}
                  for bar in range(1, 5)]
        normal, foreground = sixteenth_phrase(), sixteenth_phrase(foreground=active)
        normal_events = compile_instrument_phrase(normal, 4)
        foreground_events = compile_instrument_phrase(foreground, 4)
        normal_grid, foreground_grid = normal["_strumming_debug"]["bars"], foreground["_strumming_debug"]["bars"]
        self.assertTrue(all(item["hand_motion_count"] == 16 for item in foreground_grid))
        self.assertLessEqual(mean(item["sounding_strum_count"] for item in normal_grid) -
                             mean(item["sounding_strum_count"] for item in foreground_grid), 1.0)
        self.assertLess(mean(event["velocity"] for event in foreground_events), mean(event["velocity"] for event in normal_events))
        normal_full = sum(event["_strum_action"] == "full_strum" for event in normal_events) / len(normal_events)
        foreground_full = sum(event["_strum_action"] == "full_strum" for event in foreground_events) / len(foreground_events)
        self.assertLess(foreground_full, normal_full)

    def test_foreground_activity_is_derived_from_main_melody_events(self):
        composition = {
            "metadata": {"title": "test", "tempo": 110, "time_signature": "4/4", "key": "G"},
            "sections": [{"name": "test", "bars": 4}],
            "tracks": {
                "acoustic_guitar": {"role": "rhythm guitar", "sections": {}},
                "vocal_melody": {"role": "main melody", "sections": {"test": {"loop_bars": 4, "events": [
                    {"at": "1:1", "duration": 2, "pitch": "G4", "velocity": 80},
                    {"at": "3:1", "duration": 4, "pitch": "A4", "velocity": 82},
                ]}}},
            },
        }
        activity = derive_foreground_activity(composition, "acoustic_guitar", "test", 4)
        self.assertEqual([item["bar"] for item in activity], [1, 3])
        self.assertTrue(activity[0]["active_steps"])
        self.assertTrue(activity[1]["long_hold_steps"])

    def test_validator_reports_continuous_verse_metrics(self):
        source = phrase()
        composition = {
            "metadata": {"title": "test", "tempo": 110, "time_signature": "4/4", "key": "G"},
            "sections": [{"name": "verse_1", "bars": 2}],
            "tracks": {"acoustic_guitar": {"sections": {"verse_1": {"loop_bars": 2, "instrument_phrase": source}}}},
        }
        report = analyze_strumming_flow(composition)
        metrics = report["tracks"]["acoustic_guitar"]["sections"]["verse_1"]
        self.assertEqual(metrics["average_hand_motions_per_bar"], 8)
        self.assertEqual(metrics["average_sounding_strums_per_bar"], 6)
        self.assertEqual(metrics["only_one_strum_bars"], [])
        self.assertEqual(metrics["bar_pattern_reset_count"], 0)
        self.assertEqual(report["warning_count"], 0)

    def test_unknown_pattern_is_rejected(self):
        source = phrase(pattern="not_a_pattern")
        with self.assertRaisesRegex(ValueError, "unknown strumming pattern"):
            compile_instrument_phrase(source, 4)


if __name__ == "__main__":
    unittest.main()