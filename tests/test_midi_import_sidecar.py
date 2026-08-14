from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import mido

from src.performance.midi_import import import_midi, write_project
from src.performance.pmt import decode_tokens
from src.performance.pmt_midi import generate_pmt_midis


class MidiImportSidecarTests(unittest.TestCase):
    def build_source(self, path: Path) -> None:
        midi = mido.MidiFile(type=1, ticks_per_beat=480)
        conductor = mido.MidiTrack()
        conductor.append(
            mido.MetaMessage(
                "time_signature", numerator=4, denominator=4, time=0
            )
        )
        conductor.append(mido.MetaMessage("set_tempo", tempo=500000, time=0))
        conductor.append(
            mido.Message(
                "sysex", data=(0x7E, 0x7F, 0x09, 0x01), time=0
            )
        )
        midi.tracks.append(conductor)

        track = mido.MidiTrack()
        track.append(
            mido.Message(
                "program_change", channel=0, program=25, time=0
            )
        )
        track.append(
            mido.Message(
                "control_change", channel=0, control=64, value=127, time=0
            )
        )
        track.append(
            mido.Message(
                "note_on", channel=0, note=60, velocity=79, time=0
            )
        )
        track.append(
            mido.Message(
                "note_off", channel=0, note=60, velocity=0, time=480
            )
        )
        track.append(
            mido.Message(
                "control_change", channel=0, control=64, value=0, time=240
            )
        )
        midi.tracks.append(track)
        midi.save(path)

    def test_import_preserves_notes_cc_program_and_sysex(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mid"
            self.build_source(source)
            result = import_midi(source)
            decoded = decode_tokens(result["tokens"])

            self.assertEqual(len(decoded), 1)
            self.assertEqual(decoded[0].program, 25)
            events = result["sidecar"]["tracks"]["0"]["events"]
            self.assertEqual(
                [event["type"] for event in events],
                ["program_change", "control_change", "control_change"],
            )
            self.assertTrue(
                any(
                    event["type"] == "sysex"
                    for event in result["sidecar"]["conductor_events"]
                )
            )

    def test_generated_midi_replays_sidecar_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mid"
            project = root / "project"
            self.build_source(source)
            write_project(source, project)

            notes = decode_tokens(
                (project / "performance.pmt").read_text(encoding="utf-8")
            )
            metadata = json.loads(
                (project / "performance.meta.json").read_text(
                    encoding="utf-8"
                )
            )
            sidecar = json.loads(
                (project / "performance.midi-sidecar.json").read_text(
                    encoding="utf-8"
                )
            )
            generated = generate_pmt_midis(
                notes, project, metadata, sidecar
            )
            midi = mido.MidiFile(generated["full_song"])
            messages = [
                message for track in midi.tracks for message in track
            ]

            self.assertTrue(
                any(message.type == "sysex" for message in messages)
            )
            self.assertEqual(
                sum(
                    message.type == "control_change"
                    and message.control == 64
                    for message in messages
                ),
                2,
            )
            self.assertEqual(
                sum(
                    message.type == "program_change"
                    and message.program == 25
                    for message in messages
                ),
                1,
            )


if __name__ == "__main__":
    unittest.main()
