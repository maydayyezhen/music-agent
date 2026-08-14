from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import mido

from src.performance import PMTNote
from src.performance.pmt_midi import generate_pmt_midis


class PMTMidiTests(unittest.TestCase):
    def test_decoded_pmt_notes_generate_track_and_full_midis(self) -> None:
        notes = [
            PMTNote(0, 30, 60, 0, 1000, 78),
            PMTNote(0, 30, 64, 500, 250, 82),
        ]
        metadata = {
            "title": "PMT unit test",
            "tempo_microseconds_per_beat": 500000,
            "ticks_per_beat": 480,
            "time_signature": [4, 4],
            "tracks": {
                "0": {
                    "name": "lead_guitar",
                    "channel": 0,
                    "bank": 0,
                }
            },
        }

        with tempfile.TemporaryDirectory() as directory:
            generated = generate_pmt_midis(
                notes,
                Path(directory),
                metadata,
            )

            self.assertTrue(generated["lead_guitar"].is_file())
            self.assertTrue(generated["full_song"].is_file())

            midi = mido.MidiFile(generated["lead_guitar"])
            note_ons = [
                message
                for track in midi.tracks
                for message in track
                if message.type == "note_on" and message.velocity > 0
            ]
            programs = [
                message.program
                for track in midi.tracks
                for message in track
                if message.type == "program_change"
            ]
            self.assertEqual([message.note for message in note_ons], [60, 64])
            self.assertEqual(programs, [30])


if __name__ == "__main__":
    unittest.main()
