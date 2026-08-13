from __future__ import annotations

import json
import math
import wave
from pathlib import Path

import mido
import numpy as np

ROOT = Path(__file__).resolve().parent


def db(value: float) -> float:
    return 20 * math.log10(max(value, 1e-12))


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        data = np.frombuffer(handle.readframes(handle.getnframes()), dtype="<i2").astype(np.float64) / 32768
    return data.reshape(-1, channels), rate


def wav_stats(path: Path, composition: dict) -> dict:
    data, rate = read_wav(path)
    mono = data.mean(axis=1)
    tempo = float(composition["metadata"]["tempo"])
    seconds_per_bar = 240 / tempo
    bar_cursor = 0
    sections = {}
    for section in composition["sections"]:
        start = round(bar_cursor * seconds_per_bar * rate)
        end = round((bar_cursor + section["bars"]) * seconds_per_bar * rate)
        excerpt = mono[start:end]
        sections[section["name"]] = {
            "rms_dbfs": round(db(float(np.sqrt(np.mean(excerpt * excerpt)))), 2),
            "peak_dbfs": round(db(float(np.max(np.abs(excerpt)))), 2),
        }
        bar_cursor += section["bars"]
    return {
        "duration_seconds": round(len(data) / rate, 3),
        "rms_dbfs": round(db(float(np.sqrt(np.mean(mono * mono)))), 2),
        "peak_dbfs": round(db(float(np.max(np.abs(data)))), 2),
        "sections": sections,
    }


def midi_stats(path: Path) -> dict:
    midi = mido.MidiFile(path)
    active = {}
    count = overlaps = tiny = 0
    pitches, velocities = [], []
    for track in midi.tracks:
        tick = 0
        active.clear()
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                key = (msg.channel, msg.note)
                overlaps += int(key in active)
                active[key] = tick
                count += 1
                pitches.append(msg.note)
                velocities.append(msg.velocity)
            elif msg.type in ("note_off", "note_on"):
                key = (msg.channel, msg.note)
                if key in active:
                    tiny += int(tick - active[key] < 5)
                    active.pop(key)
    return {
        "note_count": count, "pitch_min": min(pitches), "pitch_max": max(pitches),
        "velocity_min": min(velocities), "velocity_max": max(velocities),
        "same_pitch_overlaps": overlaps, "tiny_notes_lt_5_ticks": tiny,
    }


def score_stats(score: dict) -> dict:
    notes = [note for phrase in score["phrases"] for note in phrase["notes"]]
    phrase_violations = []
    for phrase in score["phrases"]:
        starts = [note["start_beat"] for note in phrase["notes"]]
        ends = [note["start_beat"] + note["duration"] for note in phrase["notes"]]
        if any(b < a for a, b in zip(starts, starts[1:])):
            phrase_violations.append(f"{phrase['phrase_id']}: nonmonotonic")
        if phrase["notes"][0]["phrase_start"] is not True or phrase["notes"][-1]["phrase_end"] is not True:
            phrase_violations.append(f"{phrase['phrase_id']}: boundary")
        if round(max(ends), 3) != phrase["end_beat"]:
            phrase_violations.append(f"{phrase['phrase_id']}: end")
    return {
        "phrase_count": len(score["phrases"]), "note_count": len(notes),
        "first_start_beat": min(n["start_beat"] for n in notes),
        "last_end_beat": max(n["start_beat"] + n["duration"] for n in notes),
        "min_duration": min(n["duration"] for n in notes), "max_duration": max(n["duration"] for n in notes),
        "validation_violations": phrase_violations,
    }


def main() -> None:
    composition = json.loads((ROOT / "composition.json").read_text(encoding="utf-8"))
    score = json.loads((ROOT / "vocal-score.json").read_text(encoding="utf-8"))
    report = {"mix": wav_stats(ROOT / "output" / "mix.wav", composition), "stems": {}, "midi": {}, "vocal_score": score_stats(score)}
    for path in sorted((ROOT / "stems").glob("*.wav")):
        report["stems"][path.stem] = wav_stats(path, composition)
    for path in sorted((ROOT / "tracks").glob("*.mid")):
        report["midi"][path.stem] = midi_stats(path)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
