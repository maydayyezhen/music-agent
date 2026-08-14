from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import mido

from src.skills_v2.acoustic_strumming import (
    analyze_midi,
    generate_demo_midi,
)


class AcousticStrummingV2Tests(unittest.TestCase):
    MASK = [1, 0, 1, 1, 0, 1, 0, 1]

    def build_source(
        self,
        path: Path,
        *,
        transpose: int = 0,
        tempo: int = 500000,
        program: int = 25,
        velocity_offset: int = 0,
    ) -> None:
        midi = mido.MidiFile(type=1, ticks_per_beat=480)
        conductor = mido.MidiTrack()
        conductor.append(
            mido.MetaMessage(
                "set_tempo",
                tempo=tempo,
                time=0,
            )
        )
        conductor.append(
            mido.MetaMessage(
                "time_signature",
                numerator=4,
                denominator=4,
                time=0,
            )
        )
        midi.tracks.append(conductor)

        track = mido.MidiTrack()
        track.append(
            mido.Message(
                "program_change",
                channel=0,
                program=program,
                time=0,
            )
        )
        absolute = []
        chord = [45, 52, 57, 60, 64]
        for bar in range(4):
            for slot, active in enumerate(self.MASK):
                if not active:
                    continue
                direction = "down" if slot % 2 == 0 else "up"
                pitches = chord if slot == 0 else chord[-3:]
                if direction == "up":
                    pitches = list(reversed(pitches))
                start_tick = round(
                    (bar * 4 + slot * 0.5) * 480
                )
                for index, pitch in enumerate(pitches):
                    onset = start_tick + index * 8
                    velocity = min(
                        127,
                        70
                        + (8 if slot == 0 else 0)
                        + velocity_offset,
                    )
                    absolute.append(
                        (
                            onset,
                            1,
                            mido.Message(
                                "note_on",
                                channel=0,
                                note=pitch + transpose,
                                velocity=velocity,
                            ),
                        )
                    )
                    absolute.append(
                        (
                            onset + 300,
                            0,
                            mido.Message(
                                "note_off",
                                channel=0,
                                note=pitch + transpose,
                                velocity=0,
                            ),
                        )
                    )

        absolute.sort(key=lambda item: (item[0], item[1]))
        previous_tick = 0
        for tick, _, message in absolute:
            message.time = tick - previous_tick
            track.append(message)
            previous_tick = tick
        midi.tracks.append(track)
        midi.save(path)

    def test_invariance_fingerprint_survives_common_transformations(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline.mid"
            transformed = root / "transformed.mid"
            self.build_source(baseline)
            self.build_source(
                transformed,
                transpose=5,
                tempo=750000,
                program=27,
                velocity_offset=15,
            )

            first = analyze_midi(baseline)
            second = analyze_midi(transformed)

            self.assertEqual(
                first["model"]["invariance_fingerprint"],
                second["model"]["invariance_fingerprint"],
            )
            self.assertEqual(
                first["model"]["attack_mask"],
                self.MASK,
            )
            self.assertEqual(
                first["model"]["motion"]["slot_zero_direction"],
                "down",
            )

    def test_generated_demo_is_valid_and_uses_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mid"
            output = root / "demo.mid"
            self.build_source(source)
            result = analyze_midi(source)
            generate_demo_midi(result["model"], output)

            generated = mido.MidiFile(output)
            messages = [
                message
                for track in generated.tracks
                for message in track
            ]
            note_ons = [
                message
                for message in messages
                if message.type == "note_on"
                and message.velocity > 0
            ]
            self.assertTrue(output.is_file())
            self.assertGreater(len(note_ons), 20)
            self.assertTrue(
                any(
                    message.type == "program_change"
                    and message.program == 25
                    for message in messages
                )
            )


if __name__ == "__main__":
    unittest.main()
