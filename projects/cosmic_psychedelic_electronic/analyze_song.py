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
    with wave.open(str(path), "rb") as h:
        rate, channels = h.getframerate(), h.getnchannels()
        data = np.frombuffer(h.readframes(h.getnframes()), dtype="<i2").astype(np.float64) / 32768
    return data.reshape(-1, channels), rate


def wav_stats(path: Path, comp: dict) -> dict:
    data, rate = read_wav(path)
    mono = data.mean(axis=1)
    sec_per_bar = 240 / float(comp["metadata"]["tempo"])
    cursor, sections = 0, {}
    for section in comp["sections"]:
        start = round(cursor * sec_per_bar * rate)
        end = round((cursor + section["bars"]) * sec_per_bar * rate)
        x = mono[start:end]
        sections[section["name"]] = {"rms_dbfs": round(db(float(np.sqrt(np.mean(x*x)))), 2), "peak_dbfs": round(db(float(np.max(np.abs(x)))), 2)}
        cursor += section["bars"]
    return {"duration_seconds": round(len(data)/rate, 3), "rms_dbfs": round(db(float(np.sqrt(np.mean(mono*mono)))), 2), "peak_dbfs": round(db(float(np.max(np.abs(data)))), 2), "sections": sections}


def midi_stats(path: Path) -> dict:
    midi = mido.MidiFile(path)
    count = overlaps = tiny = stuck = 0
    pitches, velocities = [], []
    for track in midi.tracks:
        tick, active = 0, {}
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity:
                key = (msg.channel, msg.note)
                overlaps += int(key in active)
                active[key] = tick
                count += 1; pitches.append(msg.note); velocities.append(msg.velocity)
            elif msg.type in ("note_off", "note_on"):
                key = (msg.channel, msg.note)
                if key in active:
                    tiny += int(tick - active[key] < 5)
                    active.pop(key)
        stuck += len(active)
    return {"note_count": count, "pitch_min": min(pitches), "pitch_max": max(pitches), "velocity_min": min(velocities), "velocity_max": max(velocities), "same_pitch_overlaps": overlaps, "tiny_notes_lt_5_ticks": tiny, "stuck_notes": stuck}


def main() -> None:
    comp = json.loads((ROOT/"composition.json").read_text(encoding="utf-8"))
    out = {"mix": wav_stats(ROOT/"output"/"mix.wav", comp), "stems": {}, "midi": {}}
    for p in sorted((ROOT/"stems").glob("*.wav")): out["stems"][p.stem] = wav_stats(p, comp)
    for p in sorted((ROOT/"tracks").glob("*.mid")): out["midi"][p.stem] = midi_stats(p)
    print(json.dumps(out, indent=2))


if __name__ == "__main__": main()
