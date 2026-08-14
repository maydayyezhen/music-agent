from __future__ import annotations

import argparse
import json
import math
import wave
from collections import defaultdict
from pathlib import Path

import mido
import numpy as np


HERE = Path(__file__).resolve().parent


def wav_metrics(path: Path, include_sections: bool = False) -> dict:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        rate = handle.getframerate()
        frames = handle.getnframes()
        width = handle.getsampwidth()
        data = handle.readframes(frames)
    if width != 2:
        raise ValueError(f"expected PCM16: {path}")
    audio = np.frombuffer(data, dtype="<i2").astype(np.float64) / 32768.0
    audio = audio.reshape(-1, channels)
    mono = audio.mean(axis=1)
    absolute = np.abs(audio)
    peak = float(absolute.max()) if audio.size else 0.0
    rms = float(np.sqrt(np.mean(audio * audio))) if audio.size else 0.0
    threshold = 10 ** (-60 / 20)
    active = np.flatnonzero(np.abs(mono) > threshold)
    onset = float(active[0] / rate) if active.size else None
    last = float(active[-1] / rate) if active.size else None
    clipped = int(np.sum(absolute >= 32767 / 32768))
    result = {
        "duration_seconds": frames / rate,
        "channels": channels,
        "sample_rate": rate,
        "peak_linear": peak,
        "peak_dbfs": 20 * math.log10(max(peak, 1e-12)),
        "rms_dbfs": 20 * math.log10(max(rms, 1e-12)),
        "clipped_samples": clipped,
        "non_silent": bool(active.size),
        "first_active_second": onset,
        "last_active_second": last,
    }
    if include_sections:
        cursor = 0
        section_metrics = {}
        for name, bars in [("Narthex", 4), ("Invocation", 8), ("Procession", 8), ("Sanctus", 8), ("Great Amen", 10), ("Benediction", 8)]:
            seconds = bars * 4 * 60 / 84
            start = round(cursor * rate)
            end = min(len(audio), round((cursor + seconds) * rate))
            window = audio[start:end]
            peak_here = float(np.max(np.abs(window))) if window.size else 0.0
            rms_here = float(np.sqrt(np.mean(window * window))) if window.size else 0.0
            section_metrics[name] = {
                "start_second": cursor,
                "end_second": cursor + seconds,
                "peak_dbfs": 20 * math.log10(max(peak_here, 1e-12)),
                "rms_dbfs": 20 * math.log10(max(rms_here, 1e-12)),
            }
            cursor += seconds
        result["sections"] = section_metrics
    return result


def midi_metrics(path: Path) -> dict:
    midi = mido.MidiFile(path)
    current = [0] * len(midi.tracks)
    active: dict[tuple[int, int, int], list[tuple[int, int]]] = defaultdict(list)
    overlaps = 0
    stuck = 0
    tiny = 0
    notes = 0
    min_ticks = None
    max_ticks = 0
    for ti, track in enumerate(midi.tracks):
        lane: dict[tuple[int, int], tuple[int, int]] = {}
        tick = 0
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                key = (msg.channel, msg.note)
                if key in lane:
                    overlaps += 1
                lane[key] = (tick, msg.velocity)
                notes += 1
            elif msg.type in {"note_off", "note_on"} and (msg.type == "note_off" or msg.velocity == 0):
                key = (msg.channel, msg.note)
                if key in lane:
                    start, _ = lane.pop(key)
                    duration = tick - start
                    min_ticks = duration if min_ticks is None else min(min_ticks, duration)
                    max_ticks = max(max_ticks, duration)
                    if duration < 24:  # 1/20 beat at 480 PPQ
                        tiny += 1
        stuck += len(lane)
    return {"note_count": notes, "same_pitch_overlaps": overlaps, "stuck_notes": stuck, "tiny_notes_under_24_ticks": tiny, "minimum_note_ticks": min_ticks, "maximum_note_ticks": max_ticks, "ticks_per_beat": midi.ticks_per_beat}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label", choices=["v1", "final"])
    args = parser.parse_args()
    output = HERE / "output" / f"{args.label}.wav"
    report = {
        "label": args.label,
        "mix": wav_metrics(output, include_sections=True),
        "stems": {path.stem: wav_metrics(path) for path in sorted((HERE / "stems").glob("*.wav"))},
        "midi": {path.stem: midi_metrics(path) for path in sorted((HERE / "tracks").glob("*.mid"))},
    }
    (HERE / f"analysis_{args.label}.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
