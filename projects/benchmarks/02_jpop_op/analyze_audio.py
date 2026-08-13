from __future__ import annotations

import json
import math
import wave
from pathlib import Path

import mido
import numpy as np


ROOT = Path(__file__).resolve().parent
SECTIONS = [("intro", 4), ("verse", 8), ("pre_chorus", 8), ("chorus", 16), ("outro", 12)]


def db(value: float) -> float:
    return 20 * math.log10(max(value, 1e-12))


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        data = np.frombuffer(handle.readframes(handle.getnframes()), dtype="<i2").astype(np.float64) / 32768
    return data.reshape(-1, channels), rate


def wav_stats(path: Path, tempo: float) -> dict:
    data, rate = read_wav(path)
    mono = np.mean(data, axis=1)
    bars_cursor = 0
    per_section = {}
    seconds_per_bar = 4 * 60 / tempo
    for name, bars in SECTIONS:
        start = round(bars_cursor * seconds_per_bar * rate)
        end = round((bars_cursor + bars) * seconds_per_bar * rate)
        excerpt = mono[start:end]
        per_section[name] = {
            "rms_dbfs": round(db(float(np.sqrt(np.mean(excerpt * excerpt)))), 2),
            "peak_dbfs": round(db(float(np.max(np.abs(excerpt)))), 2),
        }
        bars_cursor += bars
    return {
        "duration_seconds": round(len(data) / rate, 3),
        "rms_dbfs": round(db(float(np.sqrt(np.mean(mono * mono)))), 2),
        "peak_dbfs": round(db(float(np.max(np.abs(data)))), 2),
        "sections": per_section,
    }


def midi_stats(path: Path) -> dict:
    midi = mido.MidiFile(path)
    note_count = 0
    velocities = []
    ranges = []
    on: dict[tuple[int, int], int] = {}
    overlaps = 0
    tiny = 0
    absolute = 0
    for track in midi.tracks:
        absolute = 0
        on.clear()
        for msg in track:
            absolute += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                key = (msg.channel, msg.note)
                if key in on:
                    overlaps += 1
                on[key] = absolute
                note_count += 1
                velocities.append(msg.velocity)
                ranges.append(msg.note)
            elif msg.type in ("note_off", "note_on"):
                key = (msg.channel, msg.note)
                if key in on:
                    if absolute - on[key] < 5:
                        tiny += 1
                    on.pop(key)
    return {
        "note_count": note_count,
        "pitch_min": min(ranges) if ranges else None,
        "pitch_max": max(ranges) if ranges else None,
        "velocity_min": min(velocities) if velocities else None,
        "velocity_max": max(velocities) if velocities else None,
        "same_pitch_overlaps": overlaps,
        "tiny_notes_lt_5_ticks": tiny,
    }


def main() -> None:
    composition = json.loads((ROOT / "composition.json").read_text(encoding="utf-8"))
    tempo = float(composition["metadata"]["tempo"])
    report = {"mix": wav_stats(ROOT / "output" / "mix.wav", tempo), "stems": {}, "midi": {}}
    for stem in sorted((ROOT / "stems").glob("*.wav")):
        report["stems"][stem.stem] = wav_stats(stem, tempo)
    for midi in sorted((ROOT / "tracks").glob("*.mid")):
        report["midi"][midi.stem] = midi_stats(midi)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
