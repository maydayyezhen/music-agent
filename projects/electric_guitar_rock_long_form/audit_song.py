from __future__ import annotations

import hashlib
import json
import math
import wave
from pathlib import Path

import mido


ROOT = Path(__file__).resolve().parent
TEMPO = 108
SECTION_BARS = {"intro": 8, "verse1": 12, "pre_chorus": 8, "chorus1": 16, "verse2": 12,
                "bridge_void": 8, "bridge_build": 8, "final_chorus": 16, "outro": 8}


def midi_audit(path: Path) -> dict:
    midi = mido.MidiFile(path)
    active: dict[tuple[int, int], list[int]] = {}
    overlaps = stuck = unmatched = tiny = 0
    note_count = 0
    absolute = 0
    for msg in mido.merge_tracks(midi.tracks):
        absolute += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            key = (msg.channel, msg.note)
            if active.get(key):
                overlaps += 1
            active.setdefault(key, []).append(absolute)
            note_count += 1
        elif msg.type in {"note_off", "note_on"} and getattr(msg, "velocity", 0) == 0:
            key = (msg.channel, msg.note)
            starts = active.get(key)
            if not starts:
                unmatched += 1
            else:
                start = starts.pop(0)
                if absolute - start < 12:
                    tiny += 1
    stuck = sum(len(values) for values in active.values())
    return {"notes": note_count, "overlap": overlaps, "stuck": stuck, "unmatched": unmatched, "tiny": tiny}


def wav_audit(path: Path) -> dict:
    with wave.open(str(path), "rb") as handle:
        frames = handle.readframes(handle.getnframes())
        width = handle.getsampwidth()
        channels = handle.getnchannels()
        rate = handle.getframerate()
        count = handle.getnframes()
    if width != 2:
        raise ValueError(f"expected 16-bit PCM: {path}")
    import array
    samples = array.array("h", frames)
    if not samples:
        return {"duration_seconds": 0.0, "peak": 0, "rms": 0.0, "clipped_samples": 0}
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(sum(float(value) * value for value in samples) / len(samples))
    return {"duration_seconds": count / rate, "sample_rate": rate, "channels": channels,
            "peak": peak, "peak_dbfs": round(20 * math.log10(max(1, peak) / 32768), 3),
            "rms": round(rms, 3), "clipped_samples": sum(abs(value) >= 32767 for value in samples)}


def section_offsets() -> dict[str, tuple[int, int]]:
    cursor = 0
    result = {}
    for name, bars in SECTION_BARS.items():
        result[name] = (cursor * 4, (cursor + bars) * 4)
        cursor += bars
    return result


def note_events(path: Path) -> list[tuple[float, int]]:
    midi = mido.MidiFile(path)
    absolute = 0
    result = []
    for msg in mido.merge_tracks(midi.tracks):
        absolute += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            result.append((absolute / midi.ticks_per_beat, msg.note))
    return result


def window_metrics(events: list[tuple[float, int]], start: float, end: float) -> dict:
    chosen = [(time, pitch) for time, pitch in events if start <= time < end]
    return {"event_count": len(chosen), "unique_pitches": len({pitch for _, pitch in chosen}),
            "median_pitch": sorted(pitch for _, pitch in chosen)[len(chosen) // 2] if chosen else None}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    midi = {path.stem: midi_audit(path) for path in sorted((ROOT / "tracks").glob("*.mid"))}
    wavs = {path.stem: wav_audit(path) for path in sorted((ROOT / "stems").glob("*.wav"))}
    final = wav_audit(ROOT / "output" / "final.wav")
    offsets = section_offsets()
    bridge = {}
    for track in ("lead_guitar", "rhythm_guitar", "bass", "drums", "organ", "strings"):
        events = note_events(ROOT / "tracks" / f"{track}.mid")
        a0, a1 = offsets["bridge_void"]
        b0, b1 = offsets["bridge_build"]
        bridge[track] = {
            "bridge_void": window_metrics(events, a0, a1),
            "bridge_build_first_half": window_metrics(events, b0, b0 + (b1 - b0) / 2),
            "bridge_build_second_half": window_metrics(events, b0 + (b1 - b0) / 2, b1),
        }
    composition_match = (ROOT / "composition.json").read_bytes() == (ROOT / "composition_final.json").read_bytes()
    report = {
        "midi": midi, "stems": wavs, "final": final, "bridge_evidence": bridge,
        "composition_final_matches": composition_match,
        "v1_sha256": sha256(ROOT / "output" / "v1.wav"),
        "final_sha256": sha256(ROOT / "output" / "final.wav"),
    }
    report["v1_final_different"] = report["v1_sha256"] != report["final_sha256"]
    (ROOT / "audit-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

