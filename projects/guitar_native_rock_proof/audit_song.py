from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import wave
from collections import Counter
from pathlib import Path

import mido
import numpy as np


ROOT = Path(__file__).resolve().parent
TPB = 480
BEATS_PER_BAR = 4
SECTIONS = [
    ("intro", 1, 8), ("theme_a", 9, 24), ("theme_b", 25, 40),
    ("bridge", 41, 48), ("main_solo", 49, 80),
    ("final_theme", 81, 96), ("outro", 97, 104),
]


def read_notes(path: Path) -> tuple[list[dict], list[dict]]:
    midi = mido.MidiFile(path)
    notes: list[dict] = []
    bends: list[dict] = []
    for track_index, track in enumerate(midi.tracks):
        tick = 0
        active: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for message in track:
            tick += message.time
            if message.type == "note_on" and message.velocity > 0:
                active.setdefault((message.channel, message.note), []).append((tick, message.velocity))
            elif message.type in {"note_off", "note_on"}:
                key = (message.channel, message.note)
                if key in active and active[key]:
                    start, velocity = active[key].pop(0)
                    notes.append({"track": track_index, "channel": message.channel, "pitch": message.note,
                                  "start": start / midi.ticks_per_beat, "end": tick / midi.ticks_per_beat,
                                  "velocity": velocity})
            elif message.type == "pitchwheel":
                bends.append({"track": track_index, "channel": message.channel,
                              "beat": tick / midi.ticks_per_beat, "pitch": message.pitch})
    return sorted(notes, key=lambda x: (x["start"], x["pitch"])), bends


def pitchwheel_gestures(bends: list[dict]) -> dict:
    gestures: list[list[dict]] = []
    current: list[dict] = []
    for event in bends:
        if current and event["beat"] - current[-1]["beat"] > 0.6:
            gestures.append(current)
            current = []
        current.append(event)
        if event["pitch"] == 0 and current:
            gestures.append(current)
            current = []
    if current:
        gestures.append(current)
    slides = [g for g in gestures if g and g[0]["pitch"] < 0 and g[-1]["pitch"] == 0
              and all(a["pitch"] <= b["pitch"] for a, b in zip(g, g[1:]))]
    bends_up = [g for g in gestures if g and max(x["pitch"] for x in g) > 0]
    return {"gesture_count": len(gestures), "slide_in_gesture_count": len(slides),
            "upward_bend_or_vibrato_gesture_count": len(bends_up),
            "slide_start_bars": [int(g[0]["beat"] // 4) + 1 for g in slides]}


def section_for(global_bar: int) -> str:
    for name, first, last in SECTIONS:
        if first <= global_bar <= last:
            return name
    return "outside"


def midi_audit(path: Path, motif_signatures: list[tuple[int, ...]]) -> dict:
    notes, bends = read_notes(path)
    tonal = [n for n in notes if n["channel"] != 9]
    if not tonal:
        return {"note_count": 0}
    gaps = [max(0.0, right["start"] - left["end"]) for left, right in zip(tonal, tonal[1:])]
    overlaps = [min(left["end"], right["end"]) - right["start"]
                for left, right in zip(tonal, tonal[1:]) if right["start"] < left["end"] - 1e-6]
    sounding_bars = sorted({int(n["start"] // 4) + 1 for n in tonal})
    max_blank = 0
    run = 0
    for bar in range(1, 105):
        if bar in sounding_bars:
            run = 0
        else:
            run += 1
            max_blank = max(max_blank, run)
    islands = 1 + sum(gap > 0.5 for gap in gaps) if tonal else 0
    long_rests = [{"after_bar": int(left["end"] // 4) + 1, "beats": round(gap, 3)}
                  for left, right, gap in zip(tonal, tonal[1:], gaps) if gap > 1.0]
    boundary_gaps = []
    for bar in range(4, 105, 4):
        boundary = bar * 4
        before = [n for n in tonal if n["start"] < boundary]
        after = [n for n in tonal if n["start"] >= boundary]
        if before and after:
            boundary_gaps.append({"after_bar": bar, "gap_beats": round(max(0, after[0]["start"] - before[-1]["end"]), 3)})
    active_at_bend = []
    for bend in bends:
        active = [n["pitch"] for n in tonal if n["channel"] == bend["channel"] and n["start"] <= bend["beat"] < n["end"]]
        active_at_bend.append({**bend, "active_notes": active})
    pitch_classes = [n["pitch"] % 12 for n in tonal]
    motif_hits = []
    for signature in motif_signatures:
        length = len(signature)
        for index in range(len(pitch_classes) - length + 1):
            if tuple(pitch_classes[index:index + length]) == signature:
                motif_hits.append({"index": index, "bar": int(tonal[index]["start"] // 4) + 1, "signature": signature})
    exact_licks = Counter()
    for bar in range(1, 105, 4):
        window = tuple((round(n["start"] - (bar - 1) * 4, 3), n["pitch"], round(n["end"] - n["start"], 3))
                       for n in tonal if (bar - 1) * 4 <= n["start"] < (bar + 3) * 4)
        if window:
            exact_licks[window] += 1
    highest = max(tonal, key=lambda n: (n["pitch"], n["velocity"]))
    return {
        "note_count": len(tonal), "sounding_bars": len(sounding_bars),
        "sounding_bar_ratio": round(len(sounding_bars) / 104, 4),
        "phrase_islands_gap_gt_half_beat": islands,
        "rests_over_one_beat": long_rests,
        "max_consecutive_blank_bars": max_blank,
        "four_bar_boundary_gaps": boundary_gaps,
        "different_pitch_overlap_count": len(overlaps),
        "max_overlap_beats": round(max(overlaps, default=0), 4),
        "pitchwheel_message_count": len(bends),
        "pitchwheel_gestures": pitchwheel_gestures(bends),
        "unsafe_pitchwheel_messages": [x for x in active_at_bend if len(x["active_notes"]) != 1],
        "highest_note": {**highest, "global_bar": int(highest["start"] // 4) + 1,
                         "section": section_for(int(highest["start"] // 4) + 1)},
        "motif_occurrences": motif_hits,
        "identical_four_bar_window_repetitions": max(exact_licks.values(), default=0),
    }


def solo_audit(path: Path) -> dict:
    notes, bends = read_notes(path)
    solo_start, solo_end = 48 * 4, 80 * 4
    solo = [{**n, "local_start": n["start"] - solo_start, "local_end": n["end"] - solo_start}
            for n in notes if n["channel"] != 9 and solo_start <= n["start"] < solo_end]
    gaps = [max(0.0, b["local_start"] - a["local_end"]) for a, b in zip(solo, solo[1:])]
    bar_counts = Counter(int(n["local_start"] // 4) + 1 for n in solo)
    pitch_peak = max(solo, key=lambda n: n["pitch"])
    density_curve = [bar_counts.get(bar, 0) for bar in range(1, 33)]
    return {
        "bars": 32, "note_count": len(solo), "active_bars": sum(bar_counts.get(b, 0) > 0 for b in range(1, 33)),
        "continuous_span_beats": round((solo[-1]["local_end"] - solo[0]["local_start"]), 3),
        "maximum_internal_gap_beats": round(max(gaps, default=0), 3),
        "phrase_islands_gap_gt_half_beat": 1 + sum(g > 0.5 for g in gaps),
        "rests_over_one_beat": sum(g > 1.0 for g in gaps),
        "notes_per_bar": density_curve,
        "density_by_8_bars": [sum(density_curve[i:i + 8]) for i in range(0, 32, 8)],
        "peak": {"pitch": pitch_peak["pitch"], "local_bar": int(pitch_peak["local_start"] // 4) + 1,
                 "global_bar": int(pitch_peak["start"] // 4) + 1},
        "pitchwheel_messages_in_solo": sum(solo_start <= b["beat"] < solo_end for b in bends),
    }


def audio_audit(path: Path) -> dict:
    with wave.open(str(path), "rb") as wav:
        frames = wav.readframes(wav.getnframes())
        channels = wav.getnchannels()
        rate = wav.getframerate()
    data = np.frombuffer(frames, dtype=np.int16).astype(np.float64) / 32768.0
    if channels > 1:
        data = data.reshape(-1, channels).mean(axis=1)
    peak = float(np.max(np.abs(data))) if data.size else 0.0
    rms = float(np.sqrt(np.mean(data ** 2))) if data.size else 0.0
    tempo = 116
    rows = {}
    for name, first, last in SECTIONS:
        start = round((first - 1) * 4 * 60 / tempo * rate)
        end = round(last * 4 * 60 / tempo * rate)
        part = data[start:end]
        part_rms = float(np.sqrt(np.mean(part ** 2))) if part.size else 0.0
        rows[name] = 20 * np.log10(max(part_rms, 1e-12))
    return {"duration_seconds": len(data) / rate, "peak_dbfs": 20 * np.log10(max(peak, 1e-12)),
            "rms_dbfs": 20 * np.log10(max(rms, 1e-12)), "section_rms_dbfs": rows}


def midi_safety(path: Path) -> dict:
    midi = mido.MidiFile(path)
    active: dict[tuple[int, int, int], int] = {}
    same_pitch_overlaps = 0
    unmatched_note_offs = 0
    tiny_notes = 0
    for track_index, track in enumerate(midi.tracks):
        tick = 0
        for message in track:
            tick += message.time
            if message.type == "note_on" and message.velocity > 0:
                key = (track_index, message.channel, message.note)
                if key in active:
                    same_pitch_overlaps += 1
                active[key] = tick
            elif message.type in {"note_off", "note_on"}:
                key = (track_index, message.channel, message.note)
                start = active.pop(key, None)
                if start is None:
                    unmatched_note_offs += 1
                elif tick - start < round(midi.ticks_per_beat * 0.04):
                    tiny_notes += 1
    return {"same_pitch_overlaps": same_pitch_overlaps, "unmatched_note_offs": unmatched_note_offs,
            "stuck_notes": len(active), "tiny_notes_lt_0_04_beats": tiny_notes}


def stem_audit(stems: Path) -> dict:
    result = {}
    for path in sorted(stems.glob("*.wav")):
        stats = audio_audit(path)
        result[path.stem] = {"rms_dbfs": float(stats["rms_dbfs"]), "non_silent": bool(stats["rms_dbfs"] > -80)}
    return result


def combine_rhythm_section(source: Path, destination: Path) -> None:
    midi = mido.MidiFile(source)
    result = mido.MidiFile(type=1, ticks_per_beat=midi.ticks_per_beat)
    result.tracks.append(mido.MidiTrack(midi.tracks[0]))
    for track in midi.tracks[1:]:
        name = next((msg.name for msg in track if msg.type == "track_name"), "")
        if name in {"rhythm_guitar", "bass", "drums"}:
            result.tracks.append(mido.MidiTrack(track))
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.save(destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", choices=["v1", "v2"])
    args = parser.parse_args()
    target = ROOT / args.version
    target.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "output" / "full_song.mid", target / "full_song.mid")
    shutil.copy2(ROOT / "tracks" / "lead_guitar.mid", target / "lead_guitar_only.mid")
    combine_rhythm_section(ROOT / "output" / "full_song.mid", target / "rhythm_section_only.mid")
    shutil.copy2(ROOT / "output" / "mix.wav", target / "full_song.wav")
    shutil.copy2(ROOT / "stems" / "lead_guitar.wav", target / "lead_guitar_only.wav")
    motif_signatures = [(4, 7, 9, 11, 9, 7, 4), (7, 9, 11, 2, 11, 9, 7)]
    report = {
        "version": args.version,
        "thresholds": {"phrase_island_gap_beats": 0.5, "long_rest_beats": 1.0},
        "lead": midi_audit(target / "lead_guitar_only.mid", motif_signatures),
        "main_solo": solo_audit(target / "lead_guitar_only.mid"),
        "audio": audio_audit(target / "full_song.wav"),
        "midi_safety": midi_safety(target / "full_song.mid"),
        "stems": stem_audit(ROOT / "stems"),
        "sha256": {name: hashlib.sha256((target / name).read_bytes()).hexdigest()
                   for name in ["composition.json", "full_song.mid", "lead_guitar_only.mid", "full_song.wav"]},
    }
    (target / "audit-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
