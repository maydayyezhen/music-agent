from __future__ import annotations

import unittest

from src.performance.gesture_ir import (
    GestureAction,
    GestureIRError,
    PerformanceGesture,
    build_sidecar,
)
from src.performance.pmt import PMTError, PMTNote, decode_tokens, encode_notes


class PMTCoreTests(unittest.TestCase):
    def test_multitrack_round_trip_keeps_performance_attributes_local(self) -> None:
        notes = [
            PMTNote(1, 48, 55, 0, 1000, 54),
            PMTNote(0, 0, 60, 0, 500, 78),
            PMTNote(0, 0, 64, 500, 250, 83),
        ]

        tokens = encode_notes(notes)
        decoded = decode_tokens(tokens)

        self.assertEqual(
            [(note.onset_ms, note.track, note.pitch) for note in decoded],
            [(0, 0, 60), (0, 1, 55), (500, 0, 64)],
        )
        self.assertEqual([note.duration_ms for note in decoded], [500, 1000, 250])
        self.assertEqual([note.velocity for note in decoded], [78, 54, 82])
        first_shift = tokens.index("TSHIFT_49")
        self.assertGreater(first_shift, tokens.index("PITCH_55"))

    def test_long_gap_is_tiled_without_bar_tokens(self) -> None:
        tokens = encode_notes(
            [
                PMTNote(0, 0, 60, 0, 500, 78),
                PMTNote(0, 0, 62, 2370, 500, 78),
            ]
        )

        self.assertIn(
            ["TSHIFT_99", "TSHIFT_99", "TSHIFT_36"],
            [tokens[index:index + 3] for index in range(len(tokens) - 2)],
        )
        self.assertNotIn("<BAR>", tokens)
        self.assertEqual(decode_tokens(tokens)[1].onset_ms, 2370)

    def test_same_onset_emits_no_time_shift(self) -> None:
        tokens = encode_notes(
            [
                PMTNote(0, 0, 60, 0, 800, 72),
                PMTNote(0, 0, 64, 0, 800, 72),
                PMTNote(0, 0, 67, 0, 800, 72),
            ]
        )
        self.assertFalse(any(token.startswith("TSHIFT_") for token in tokens))

    def test_agent_extension_tiles_long_note_duration(self) -> None:
        tokens = encode_notes([PMTNote(0, 0, 60, 0, 4300, 72)])
        decoded = decode_tokens(tokens)

        self.assertEqual(decoded[0].duration_ms, 4300)
        self.assertEqual(tokens.count("DURP_199"), 2)

    def test_paper_compatible_mode_can_still_clamp_to_two_seconds(self) -> None:
        decoded = decode_tokens(
            encode_notes(
                [PMTNote(0, 0, 60, 0, 4300, 72)],
                tile_long_durations=False,
            )
        )
        self.assertEqual(decoded[0].duration_ms, 2000)

    def test_bar_token_is_rejected_in_performance_mode(self) -> None:
        with self.assertRaises(PMTError):
            decode_tokens("<BOS> TRACK_0 PROG_0 <BAR> <EOS>")


class GestureIRTests(unittest.TestCase):
    def test_non_retriggered_guitar_chain_is_valid_sidecar(self) -> None:
        gesture = PerformanceGesture(
            gesture_id="lead-g1",
            track=0,
            program=30,
            instrument="electric_guitar",
            string_index=2,
            actions=(
                GestureAction(
                    action_id="a1",
                    kind="pick",
                    time_ms=1200,
                    note_id="n1",
                    pitch=64,
                    velocity=91,
                ),
                GestureAction(
                    action_id="a2",
                    kind="hammer_on",
                    time_ms=1450,
                    note_id="n2",
                    from_pitch=64,
                    to_pitch=67,
                    transition_ms=35,
                    retrigger=False,
                ),
                GestureAction(
                    action_id="a3",
                    kind="slide",
                    time_ms=1710,
                    note_id="n3",
                    from_pitch=67,
                    to_pitch=69,
                    transition_ms=140,
                    retrigger=False,
                ),
                GestureAction(
                    action_id="a4",
                    kind="vibrato",
                    time_ms=2060,
                    note_id="n3",
                    pitch=69,
                    parameters={
                        "delay_ms": 420,
                        "rate_hz": 5.1,
                        "depth_cents": 24,
                    },
                ),
                GestureAction(
                    action_id="a5",
                    kind="release",
                    time_ms=2680,
                    note_id="n3",
                    pitch=69,
                ),
            ),
        )

        sidecar = build_sidecar([gesture], source="unit-test")

        self.assertEqual(sidecar["schema_version"], 1)
        self.assertFalse(
            sidecar["gestures"][0]["actions"][1]["retrigger"]
        )

    def test_transition_must_explicitly_disable_retrigger(self) -> None:
        invalid = GestureAction(
            action_id="a1",
            kind="hammer_on",
            time_ms=100,
            from_pitch=64,
            to_pitch=67,
            transition_ms=30,
            retrigger=True,
        )
        with self.assertRaises(GestureIRError):
            invalid.validate()


if __name__ == "__main__":
    unittest.main()
