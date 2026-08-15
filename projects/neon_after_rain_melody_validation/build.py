from __future__ import annotations

import json
import sys
from pathlib import Path

import mido

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.midi.pitches import note_number
from src.validation import analyze_melody_structure

TPB = 480
PLAN = json.loads((PROJECT / "melody_plan.json").read_text(encoding="utf-8"))
TARGETS = {int(item["bar"]): item for item in PLAN["structural_targets"]}

# bar, beat, duration, pitch, phrase, operation, structural_role, embellishment, phrase_function, velocity
MELODY = [
    (1, 0.5, 0.5, "B4", "A", "original", "structural", None, "pickup", 82),
    (1, 1.25, 0.5, "D5", "A", "original", "surface", "passing", "motion", 78),
    (1, 2.0, 1.0, "E5", "A", "original", "structural", None, "arrival", 86),
    (1, 3.25, 0.5, "D5", "A", "original", "surface", "neighbor", "release", 78),
    (2, 0.0, 0.75, "B4", "A", "original", "structural", None, "anchor", 82),
    (2, 1.0, 0.25, "C5", "A", "original", "surface", "upper_neighbor", "ornament", 76),
    (2, 1.25, 0.75, "B4", "A", "original", "structural", None, "return", 82),
    (2, 2.25, 0.75, "G4", "A", "original", "structural", None, "arrival", 80),
    (2, 3.25, 0.5, "B4", "A", "original", "surface", "connector", "lift", 78),
    (3, 0.5, 0.5, "D5", "A", "sequence_fragment", "structural", None, "pickup", 82),
    (3, 1.25, 0.5, "E5", "A", "sequence_fragment", "surface", "passing", "motion", 80),
    (3, 2.0, 1.0, "G5", "A", "sequence_fragment", "structural", None, "arrival", 88),
    (3, 3.25, 0.5, "F#5", "A", "sequence_fragment", "surface", "neighbor", "release", 80),
    (4, 0.0, 0.75, "E5", "A", "changed_ending", "structural", None, "anchor", 82),
    (4, 1.0, 0.5, "D5", "A", "changed_ending", "surface", "passing", "motion", 78),
    (4, 1.75, 0.5, "B4", "A", "changed_ending", "structural", None, "target", 82),
    (4, 2.5, 0.5, "A4", "A", "changed_ending", "surface", "passing", "motion", 76),
    (4, 3.0, 0.75, "F#4", "A", "changed_ending", "structural", None, "open_ending", 80),

    (5, 0.5, 0.5, "B4", "A_prime", "rhythm_variation", "structural", None, "pickup", 82),
    (5, 1.0, 0.25, "C5", "A_prime", "rhythm_variation", "surface", "upper_neighbor", "ornament", 76),
    (5, 1.5, 0.5, "D5", "A_prime", "rhythm_variation", "surface", "passing", "motion", 78),
    (5, 2.25, 1.0, "E5", "A_prime", "rhythm_variation", "structural", None, "arrival", 86),
    (5, 3.5, 0.35, "D5", "A_prime", "rhythm_variation", "surface", "neighbor", "release", 76),
    (6, 0.0, 0.75, "B4", "A_prime", "one_axis_variation", "structural", None, "anchor", 82),
    (6, 1.0, 0.5, "C5", "A_prime", "one_axis_variation", "structural", None, "target", 82),
    (6, 1.75, 0.25, "B4", "A_prime", "one_axis_variation", "surface", "lower_neighbor", "ornament", 74),
    (6, 2.25, 0.75, "G4", "A_prime", "one_axis_variation", "surface", "connector", "motion", 76),
    (6, 3.25, 0.5, "E5", "A_prime", "one_axis_variation", "structural", None, "arrival", 84),
    (7, 0.5, 0.5, "C5", "A_prime", "sequence_up", "structural", None, "pickup", 82),
    (7, 1.25, 0.5, "E5", "A_prime", "sequence_up", "surface", "passing", "motion", 80),
    (7, 2.0, 1.0, "G5", "A_prime", "sequence_up", "structural", None, "arrival", 88),
    (7, 3.25, 0.5, "E5", "A_prime", "sequence_up", "surface", "release", "release", 78),
    (8, 0.0, 0.5, "F#5", "A_prime", "changed_ending", "structural", None, "tension", 84),
    (8, 0.75, 0.5, "D#5", "A_prime", "changed_ending", "structural", None, "leading_target", 86),
    (8, 1.5, 1.0, "B4", "A_prime", "changed_ending", "structural", None, "arrival", 82),

    (9, 0.5, 0.5, "E5", "B", "sequence_up", "structural", None, "pickup", 82),
    (9, 1.25, 0.5, "G5", "B", "sequence_up", "surface", "passing", "motion", 82),
    (9, 2.0, 1.0, "B5", "B", "sequence_up", "structural", None, "arrival", 90),
    (9, 3.25, 0.5, "A5", "B", "sequence_up", "surface", "neighbor", "release", 82),
    (10, 0.0, 0.5, "D5", "B", "fragment_and_revoice", "structural", None, "anchor", 82),
    (10, 0.75, 0.5, "G5", "B", "fragment_and_revoice", "surface", "connector", "motion", 82),
    (10, 1.5, 1.0, "B5", "B", "fragment_and_revoice", "structural", None, "arrival", 90),
    (10, 2.75, 0.5, "A5", "B", "fragment_and_revoice", "surface", "passing", "motion", 80),
    (10, 3.25, 0.5, "F#5", "B", "fragment_and_revoice", "structural", None, "answer", 84),
    (11, 0.5, 0.5, "F#5", "B", "register_lift", "structural", None, "pickup", 84),
    (11, 1.25, 0.5, "A5", "B", "register_lift", "surface", "passing", "motion", 84),
    (11, 2.0, 1.0, "D6", "B", "register_lift", "structural", None, "climax", 96),
    (11, 3.25, 0.5, "C6", "B", "register_lift", "surface", "neighbor", "release", 84),
    (12, 0.0, 0.5, "B5", "B", "release", "structural", None, "release", 88),
    (12, 0.75, 0.5, "G5", "B", "release", "surface", "passing", "motion", 82),
    (12, 1.5, 1.5, "E5", "B", "release", "structural", None, "arrival", 86),
    (12, 3.25, 0.25, "F#5", "B", "release", "surface", "upper_neighbor", "ornament", 74),
    (12, 3.5, 0.25, "G5", "B", "release", "surface", "upper_neighbor", "ornament", 76),

    (13, 0.5, 0.5, "B4", "A_return", "return_with_ornament", "structural", None, "pickup", 80),
    (13, 1.0, 0.25, "C5", "A_return", "return_with_ornament", "surface", "upper_neighbor", "ornament", 74),
    (13, 1.25, 0.25, "B4", "A_return", "return_with_ornament", "structural", None, "return", 78),
    (13, 2.0, 1.0, "E5", "A_return", "return_with_ornament", "structural", None, "arrival", 86),
    (13, 3.25, 0.5, "D5", "A_return", "return_with_ornament", "surface", "passing", "motion", 78),
    (14, 0.0, 0.5, "G4", "A_return", "contour_preserved_rhythm_changed", "structural", None, "anchor", 78),
    (14, 0.75, 0.5, "B4", "A_return", "contour_preserved_rhythm_changed", "surface", "passing", "motion", 78),
    (14, 1.5, 0.5, "C5", "A_return", "contour_preserved_rhythm_changed", "structural", None, "target", 82),
    (14, 2.25, 0.25, "B4", "A_return", "contour_preserved_rhythm_changed", "surface", "lower_neighbor", "ornament", 74),
    (14, 2.5, 0.25, "C5", "A_return", "contour_preserved_rhythm_changed", "structural", None, "return", 78),
    (14, 3.0, 0.75, "E5", "A_return", "contour_preserved_rhythm_changed", "structural", None, "arrival", 84),
    (15, 0.5, 0.5, "B4", "A_return", "sequence_up", "structural", None, "pickup", 80),
    (15, 1.25, 0.5, "D5", "A_return", "sequence_up", "surface", "passing", "motion", 80),
    (15, 2.0, 1.0, "G5", "A_return", "sequence_up", "structural", None, "arrival", 90),
    (15, 3.25, 0.25, "F#5", "A_return", "sequence_up", "surface", "passing", "motion", 76),
    (15, 3.5, 0.25, "E5", "A_return", "sequence_up", "structural", None, "answer", 80),
    (16, 0.0, 0.25, "C5", "A_return", "changed_ending", "surface", "anticipation_like", "pickup", 74),
    (16, 0.5, 0.5, "B4", "A_return", "changed_ending", "structural", None, "anchor", 80),
    (16, 1.25, 0.5, "D#5", "A_return", "changed_ending", "surface", "passing", "tension", 82),
    (16, 2.0, 0.75, "F#5", "A_return", "changed_ending", "structural", None, "arrival", 88),
    (16, 3.0, 0.75, "D#5", "A_return", "changed_ending", "structural", None, "open_ending", 84),

    (17, 0.5, 0.75, "B4", "Coda", "augmentation", "structural", None, "pickup", 78),
    (17, 1.5, 0.75, "D5", "Coda", "augmentation", "surface", "passing", "motion", 78),
    (17, 2.5, 1.25, "E5", "Coda", "augmentation", "structural", None, "arrival", 86),
    (18, 0.0, 1.0, "B4", "Coda", "augmentation", "structural", None, "anchor", 78),
    (18, 1.25, 0.5, "C5", "Coda", "augmentation", "surface", "neighbor", "motion", 76),
    (18, 2.0, 1.0, "E5", "Coda", "augmentation", "structural", None, "arrival", 84),
    (18, 3.25, 0.5, "G5", "Coda", "augmentation", "structural", None, "lift", 86),
    (19, 0.0, 0.75, "E5", "Coda", "resolution", "structural", None, "anchor", 82),
    (19, 1.0, 0.75, "C5", "Coda", "resolution", "structural", None, "target", 80),
    (19, 2.0, 0.5, "B4", "Coda", "resolution", "surface", "passing", "motion", 74),
    (19, 2.75, 1.0, "A4", "Coda", "resolution", "structural", None, "arrival", 78),
    (20, 0.0, 0.5, "F#4", "Coda", "final_resolution", "surface", "upper_neighbor", "approach", 74),
    (20, 0.75, 0.5, "G4", "Coda", "final_resolution", "surface", "neighbor", "approach", 76),
    (20, 1.5, 2.25, "E4", "Coda", "final_resolution", "structural", None, "final", 84),
]


def melody_events() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for bar, beat, duration, pitch, phrase, operation, role, embellishment, function, velocity in MELODY:
        target = TARGETS[bar]
        event: dict[str, object] = {
            "start_beat": (bar - 1) * 4 + beat,
            "duration_beats": duration,
            "pitch": pitch,
            "phrase_id": phrase,
            "motif_id": "A",
            "motif_operation": operation,
            "structural_role": role,
            "phrase_function": function,
            "velocity": velocity,
        }
        if role == "surface":
            event["embellishment_type"] = embellishment
            event["parent_target"] = target["id"]
        elif pitch == target["pitch"]:
            event["target_id"] = target["id"]
        result.append(event)
    return result


def _append_timed(track: mido.MidiTrack, messages: list[tuple[int, int, mido.Message]]) -> None:
    previous = 0
    for tick, order, message in sorted(messages, key=lambda item: (item[0], item[1])):
        del order
        message.time = tick - previous
        track.append(message)
        previous = tick


def write_midi(path: Path, events: list[dict[str, object]]) -> None:
    midi = mido.MidiFile(type=1, ticks_per_beat=TPB)

    conductor = mido.MidiTrack()
    conductor.append(mido.MetaMessage("track_name", name="Conductor", time=0))
    conductor.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(PLAN["metadata"]["tempo_bpm"]), time=0))
    conductor.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    conductor.append(mido.MetaMessage("key_signature", key="Em", time=0))
    midi.tracks.append(conductor)

    melody_track = mido.MidiTrack()
    melody_track.append(mido.MetaMessage("track_name", name="Marimba Lead", time=0))
    melody_track.append(mido.Message("program_change", program=12, channel=0, time=0))
    melody_messages: list[tuple[int, int, mido.Message]] = []
    for event in events:
        start = round(float(event["start_beat"]) * TPB)
        end = round((float(event["start_beat"]) + float(event["duration_beats"])) * TPB)
        pitch = note_number(str(event["pitch"]))
        velocity = int(event["velocity"])
        melody_messages.append((start, 1, mido.Message("note_on", note=pitch, velocity=velocity, channel=0)))
        melody_messages.append((end, 0, mido.Message("note_off", note=pitch, velocity=0, channel=0)))
    _append_timed(melody_track, melody_messages)
    midi.tracks.append(melody_track)

    harmony_track = mido.MidiTrack()
    harmony_track.append(mido.MetaMessage("track_name", name="Electric Piano Bed", time=0))
    harmony_track.append(mido.Message("program_change", program=4, channel=1, time=0))
    harmony_messages: list[tuple[int, int, mido.Message]] = []
    for item in PLAN["harmony"]:
        start = round((int(item["bar"]) - 1) * 4 * TPB)
        end = round(((int(item["bar"]) - 1) * 4 + 3.75) * TPB)
        base_velocity = 50 + (4 if 9 <= int(item["bar"]) <= 12 else 0)
        for index, pitch_name in enumerate(item["voicing"]):
            pitch = note_number(str(pitch_name))
            velocity = max(36, base_velocity - index * 2)
            harmony_messages.append((start, 1, mido.Message("note_on", note=pitch, velocity=velocity, channel=1)))
            harmony_messages.append((end, 0, mido.Message("note_off", note=pitch, velocity=0, channel=1)))
    _append_timed(harmony_track, harmony_messages)
    midi.tracks.append(harmony_track)

    midi.save(path)


def main() -> int:
    output = PROJECT / "output"
    reports = PROJECT / "reports"
    output.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)

    events = melody_events()
    midi_path = output / "neon_after_rain.mid"
    write_midi(midi_path, events)

    (output / "melody_events.json").write_text(
        json.dumps(events, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report = analyze_melody_structure(PLAN, events)
    (reports / "validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(midi_path)
    print(reports / "validation.json")
    print(json.dumps(report["metrics"], ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
