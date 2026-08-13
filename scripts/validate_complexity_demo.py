from __future__ import annotations

import json
import math
import wave
from pathlib import Path

import mido
import numpy as np

from _bootstrap import ROOT
from src.complexity import COMPLEXITY_LEVELS
from src.complexity.critic import analyze_complexity
from src.composition import load_composition


DEMO = ROOT / "projects" / "complexity_demo"


def wav_stats(path: Path) -> dict[str, float | int]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        rate = handle.getframerate()
        frames = handle.getnframes()
        samples = np.frombuffer(handle.readframes(frames), dtype="<i2").astype(np.int32)
    peak = int(np.max(np.abs(samples))) if len(samples) else 0
    rms = float(np.sqrt(np.mean(samples.astype(np.float64) ** 2))) if len(samples) else 0.0
    return {
        "duration_seconds": frames / rate,
        "channels": channels,
        "sample_rate": rate,
        "peak_dbfs": 20 * math.log10(max(peak / 32768.0, 1e-12)),
        "rms_dbfs": 20 * math.log10(max(rms / 32768.0, 1e-12)),
    }


def midi_health(path: Path) -> dict[str, int]:
    midi = mido.MidiFile(path)
    active: dict[tuple[int, int], int] = {}
    overlaps = tiny = note_count = 0
    for track in midi.tracks:
        tick = 0
        for message in track:
            tick += message.time
            if message.type == "note_on" and message.velocity > 0:
                key = (message.channel, message.note)
                if key in active:
                    overlaps += 1
                active[key] = tick
                note_count += 1
            elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                key = (message.channel, message.note)
                start = active.pop(key, None)
                if start is not None and tick - start < 30:
                    tiny += 1
    return {"notes": note_count, "overlaps": overlaps, "tiny": tiny, "stuck": len(active)}


def main() -> int:
    rows: list[dict] = []
    for level in COMPLEXITY_LEVELS:
        folder = DEMO / level
        composition = load_composition(folder / "composition.json")
        report = analyze_complexity(composition)
        (folder / "complexity-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        mix = wav_stats(folder / "output" / "mix.wav")
        midi = midi_health(folder / "output" / "full_song.mid")
        stem_stats = [wav_stats(path) for path in sorted((folder / "stems").glob("*.wav"))]
        if not stem_stats or any(float(item["rms_dbfs"]) <= -120 for item in stem_stats):
            raise RuntimeError(f"{level}: missing or silent stem")
        if not (59.5 <= float(mix["duration_seconds"]) <= 59.7 and mix["channels"] == 2 and mix["sample_rate"] == 44100):
            raise RuntimeError(f"{level}: unexpected WAV format/duration {mix}")
        if midi["overlaps"] or midi["tiny"] or midi["stuck"]:
            raise RuntimeError(f"{level}: unhealthy MIDI {midi}")
        row = {
            "level": level,
            "tracks": len(composition["tracks"]),
            "theme_b_density": report["section_metrics"]["theme_b"]["section_density"],
            "theme_b_onset_overlap": report["section_metrics"]["theme_b"]["onset_overlap_ratio"],
            "duration_seconds": mix["duration_seconds"],
            "peak_dbfs": mix["peak_dbfs"],
            "rms_dbfs": mix["rms_dbfs"],
            "midi_notes": midi["notes"],
            "midi_overlaps": midi["overlaps"],
            "midi_stuck": midi["stuck"],
            "critic_warnings": report["warning_count"],
        }
        rows.append(row)
    densities = [float(row["theme_b_density"]) for row in rows]
    notes = [int(row["midi_notes"]) for row in rows]
    if densities != sorted(densities) or notes != sorted(notes):
        raise RuntimeError("complexity progression is not monotonic")
    (DEMO / "comparison.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Signal Garden: five-level validation",
        "",
        "Same D-Dorian piano theme, 100 BPM, 24 bars, and 59.6-second form in every version.",
        "",
        "| Level | Tracks | Theme-B events/bar | Onset overlap | MIDI notes | Peak | RMS | Critic warnings |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['level']} | {row['tracks']} | {row['theme_b_density']:.2f} | {row['theme_b_onset_overlap']:.2f} | "
            f"{row['midi_notes']} | {row['peak_dbfs']:.2f} dBFS | {row['rms_dbfs']:.2f} dBFS | {row['critic_warnings']} |"
        )
    lines += ["", "All rendered stems are non-silent; all full-song MIDIs have zero same-pitch overlaps, tiny notes, and stuck notes.", ""]
    (DEMO / "comparison.md").write_text("\n".join(lines), encoding="utf-8")
    print("[OK] Five rendered levels validated")
    for row in rows:
        print(f"{row['level']:8} tracks={row['tracks']} density={row['theme_b_density']:.2f} notes={row['midi_notes']} peak={row['peak_dbfs']:.2f}dBFS warnings={row['critic_warnings']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
