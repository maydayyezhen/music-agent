from __future__ import annotations

import hashlib
import json
import wave
from pathlib import Path

import mido
import numpy as np


ROOT = Path(__file__).resolve().parent


def audio_stats(path: Path) -> dict:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        frames = handle.getnframes()
        width = handle.getsampwidth()
        raw = handle.readframes(frames)
    data = np.frombuffer(raw, dtype="<i2").astype(np.float64) if width == 2 else np.array([], dtype=np.float64)
    peak = float(np.max(np.abs(data))) if data.size else 0.0
    rms = float(np.sqrt(np.mean(data * data))) if data.size else 0.0
    return {
        "duration_seconds": frames / rate,
        "sample_rate": rate,
        "channels": channels,
        "peak_linear": peak / 32768.0,
        "peak_dbfs": 20 * np.log10(max(1e-12, peak / 32768.0)),
        "rms_dbfs": 20 * np.log10(max(1e-12, rms / 32768.0)),
        "clipped_samples": int(np.sum(np.abs(data) >= 32767)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def midi_stats(path: Path, lead: bool = False) -> dict:
    midi = mido.MidiFile(path)
    active: dict[tuple[int, int], tuple[int, int]] = {}
    active_pitches: dict[int, set[int]] = {}
    same_pitch_overlap = unmatched = stuck = tiny = different_pitch_overlap = pitchbend = 0
    note_onsets = []
    for track in midi.tracks:
        tick = 0
        for message in track:
            tick += message.time
            if message.type == "pitchwheel":
                pitchbend += 1
            if message.type == "note_on" and message.velocity > 0:
                key = (message.channel, message.note)
                if key in active:
                    same_pitch_overlap += 1
                sounding = active_pitches.setdefault(message.channel, set())
                if lead and sounding and message.note not in sounding:
                    different_pitch_overlap += 1
                active[key] = (tick, message.velocity)
                sounding.add(message.note)
                note_onsets.append(tick / midi.ticks_per_beat)
            elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                key = (message.channel, message.note)
                started = active.pop(key, None)
                if started is None:
                    unmatched += 1
                else:
                    if tick - started[0] < 24:
                        tiny += 1
                    active_pitches.setdefault(message.channel, set()).discard(message.note)
    stuck = len(active)
    return {
        "same_pitch_overlap": same_pitch_overlap,
        "different_pitch_overlap": different_pitch_overlap if lead else None,
        "stuck": stuck,
        "unmatched_note_off": unmatched,
        "tiny_notes": tiny,
        "pitchbend_messages": pitchbend,
        "note_on_count": len(note_onsets),
        "bridge_note_on_count": sum(224 <= onset < 288 for onset in note_onsets) if lead else None,
    }


def section_audio(path: Path, composition: dict) -> dict:
    with wave.open(str(path), "rb") as handle:
        rate = handle.getframerate()
        channels = handle.getnchannels()
        raw = handle.readframes(handle.getnframes())
    data = np.frombuffer(raw, dtype="<i2").reshape(-1, channels).astype(np.float64)
    seconds_per_bar = 4 * 60 / float(composition["metadata"]["tempo"])
    cursor = 0
    result = {}
    for section in composition["sections"]:
        start = round(cursor * seconds_per_bar * rate)
        cursor += int(section["bars"])
        end = min(len(data), round(cursor * seconds_per_bar * rate))
        segment = data[start:end]
        rms = float(np.sqrt(np.mean(segment * segment))) if segment.size else 0.0
        result[section["name"]] = {
            "bars": section["bars"],
            "rms_dbfs": 20 * np.log10(max(1e-12, rms / 32768.0)),
        }
    return result


def main() -> None:
    composition = json.loads((ROOT / "composition.json").read_text(encoding="utf-8"))
    report = {
        "mix": audio_stats(ROOT / "output" / "mix.wav"),
        "section_audio": section_audio(ROOT / "output" / "mix.wav", composition),
        "stems": {path.stem: audio_stats(path) for path in sorted((ROOT / "stems").glob("*.wav"))},
        "midi": {path.stem: midi_stats(path, path.stem == "lead_guitar") for path in sorted((ROOT / "tracks").glob("*.mid"))},
    }
    report["midi"]["full_song"] = midi_stats(ROOT / "output" / "full_song.mid")
    (ROOT / "render-analysis.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
