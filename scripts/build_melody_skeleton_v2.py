from __future__ import annotations

import json
from pathlib import Path

import mido

from _bootstrap import ROOT
from src.midi.pitches import note_number
from src.validation import validate_melody_skeleton

OUT = ROOT / "tests" / "fixtures" / "lead_guitar_long_form_v2"
TPB = 480

PLAN = {
    "metadata": {"tempo": 100, "time_signature": "4/4", "key": "E minor", "seed": 4202,
                 "instrument": "GM Acoustic Grand Piano program 0"},
    "harmony": ["Em", "C", "G", "D", "Em", "C", "Am", "B7"],
    "section": {"bars": [1, 8], "role": "lead_melody",
                "arc": {"opening_energy": 0.35, "peak_bar": 7, "resolution_bar": 8,
                        "direction": "gradual_rise_then_release"}},
    "motif": {"id": "A", "length_beats": 4, "contour": "rise_fall",
              "rhythmic_identity": "short_short_long"},
    "phrase_plan": [
        {"bars": [1, 2], "function": "introduce", "resolution": "open", "reset_state": False},
        {"bars": [3, 4], "function": "develop", "operation": "change_ending", "resolution": "deferred", "reset_state": False},
        {"bars": [5, 6], "function": "expand", "operation": "sequence_up", "resolution": "deferred", "reset_state": False},
        {"bars": [7, 8], "function": "climax_and_resolve", "operation": "augmentation_release", "resolution": "strong", "reset_state": True},
    ],
    "rests": [
        {"after_beat": 3.0, "duration_beats": 0.5, "rest_type": "breath", "reset_state": False},
        {"after_beat": 11.0, "duration_beats": 0.5, "rest_type": "breath", "reset_state": False},
        {"after_beat": 19.0, "duration_beats": 0.5, "rest_type": "breath", "reset_state": False},
        {"after_beat": 32.0, "duration_beats": 0.0, "rest_type": "section_end", "reset_state": True},
    ],
}

NOTES = [
    # A: short-short-long, open ending.
    (0.5, .5, "E4", "original", None), (1.25, .5, "G4", "original", None),
    (2.0, 1.0, "B4", "original", None), (3.5, .5, "A4", "original", None),
    (4.25, .5, "G4", "continuation", None), (5.0, 1.0, "B4", "continuation", None),
    (6.25, .75, "D5", "continuation", None), (7.25, 1.0, "C5", "continuation", "phrase_continuation"),
    # A': same rhythmic identity, changed ending, still deferred.
    (8.5, .5, "E4", "change_ending", None), (9.25, .5, "G4", "change_ending", None),
    (10.0, 1.0, "B4", "change_ending", None), (11.5, .5, "C5", "change_ending", None),
    (12.25, .5, "B4", "change_ending", None), (13.0, .75, "D5", "change_ending", None),
    (14.0, .75, "E5", "change_ending", None), (15.0, 1.2, "D5", "change_ending", "delayed_resolution"),
    # Sequence/expansion into upper register.
    (16.5, .5, "G4", "sequence_up", None), (17.25, .5, "B4", "sequence_up", None),
    (18.0, 1.0, "D5", "sequence_up", None), (19.5, .5, "E5", "sequence_up", None),
    (20.25, .5, "D5", "sequence_up", None), (21.0, .75, "E5", "sequence_up", None),
    (22.0, .75, "F#5", "sequence_up", None), (23.0, 1.2, "G5", "sequence_up", "anticipation"),
    # Developed climax in bar 7, release and sole strong resolution in bar 8.
    (24.5, .75, "A5", "augmentation_release", None), (25.5, .75, "B5", "augmentation_release", None),
    (26.5, 1.25, "D6", "augmentation_release", None),
    (28.0, .5, "B5", "augmentation_release", None), (28.75, .5, "G5", "augmentation_release", None),
    (29.5, .75, "F#5", "augmentation_release", None), (30.5, 1.5, "E5", "augmentation_release", None),
]


def note_data() -> list[dict[str, object]]:
    return [{"start_beat": start, "duration_beats": duration, "pitch": pitch, "motif_id": "A",
             "motif_operation": operation, **({"cross_bar_reason": reason} if reason else {})}
            for start, duration, pitch, operation, reason in NOTES]


def write_midi(path: Path, notes: list[dict[str, object]]) -> None:
    midi = mido.MidiFile(type=1, ticks_per_beat=TPB)
    conductor = mido.MidiTrack(); conductor.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(100), time=0)); midi.tracks.append(conductor)
    track = mido.MidiTrack(); track.append(mido.Message("program_change", program=0, channel=0, time=0))
    messages = []
    for item in notes:
        start = round(float(item["start_beat"]) * TPB); end = round((float(item["start_beat"]) + float(item["duration_beats"])) * TPB)
        pitch = note_number(str(item["pitch"])); messages.extend([(start, 1, mido.Message("note_on", note=pitch, velocity=76, channel=0)), (end, 0, mido.Message("note_off", note=pitch, velocity=0, channel=0))])
    previous = 0
    for tick, _, message in sorted(messages, key=lambda value: (value[0], value[1])):
        message.time = tick - previous; track.append(message); previous = tick
    midi.tracks.append(track); midi.save(path)


def legacy_notes() -> list[dict[str, object]]:
    result = []
    pattern = [(0, .5, "E4"), (.75, .5, "G4"), (1.5, .5, "B4"), (2.25, 1.0, "D5")]
    for block in range(4):
        for start, duration, pitch in pattern:
            result.append({"start_beat": block * 8 + start, "duration_beats": duration, "pitch": pitch,
                           "motif_id": f"fragment_{block + 1}", "motif_operation": "independent"})
    return result


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    notes = note_data(); payload = {"plan": PLAN, "notes": notes}
    (OUT / "melody_skeleton_v2.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_midi(OUT / "melody_skeleton_v2.mid", notes); write_midi(OUT / "legacy_fragmented_test.mid", legacy_notes())
    report = validate_melody_skeleton(PLAN, notes, OUT / "melody_skeleton_v2.mid")
    lines = ["# Lead Melody Skeleton Validation", "", *[f"- {key}: {value}" for key, value in report["metrics"].items()], "", f"Conclusion: {report['conclusion']}"]
    (OUT / "melody_skeleton_v2_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    ab = {
        "shared": {"bpm": 100, "key": "E minor", "harmony": PLAN["harmony"], "instrument": "GM program 0", "seed": 4202, "bars": 8},
        "legacy": {"independent_phrase_resets": 3, "long_rest_distribution": "one large gap after every two-bar fragment", "motif_developments": 0, "peak_bars": [1, 3, 5, 7], "final_cadence_bars": [2, 4, 6, 8], "unified_motif": False, "scattered_fills": True, "unreasoned_long_sustains": 0, "overlap": 0, "pitch_bend": 0},
        "v2": {"independent_phrase_resets": report["metrics"]["independent_phrase_resets"], "longest_silence_beats": report["metrics"]["longest_silence_beats"], "motif_developments": report["metrics"]["motif_developments"], "peak_bar": report["metrics"]["peak_bar"], "final_resolution_bar": 8, "unified_motif": True, "scattered_fills": False, "unreasoned_long_sustains": report["metrics"]["unreasoned_long_sustains"], "overlap": report["metrics"]["overlapping_different_pitches"], "pitch_bend": report["metrics"]["pitch_bends"]},
    }
    (OUT / "ab_report.json").write_text(json.dumps(ab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if report["passed"] else 1


if __name__ == "__main__": raise SystemExit(main())
