from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import json
import math
import wave

import mido
import numpy as np

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TPB = 480
SR = 44_100


def select_notes(voicing: list[int], action: str) -> list[int]:
    if action == "full_strum":
        return list(voicing)
    if action == "low_partial":
        return list(voicing[:3])
    if action == "middle_partial":
        start = max(0, (len(voicing) - 3) // 2)
        return list(voicing[start : start + 3])
    if action in {"high_partial", "light_upstroke"}:
        return list(voicing[-3:])
    if action == "ghost_strum":
        return list(voicing[-2:])
    if action == "single_string_restrike":
        return [voicing[-2]]
    if action == "air_strum":
        return []
    raise ValueError(f"unsupported action: {action}")


def duration_beats(action: str) -> float:
    return {
        "full_strum": 0.92,
        "low_partial": 0.78,
        "middle_partial": 0.74,
        "high_partial": 0.58,
        "light_upstroke": 0.48,
        "ghost_strum": 0.20,
        "single_string_restrike": 0.52,
        "air_strum": 0.0,
    }[action]


def build_segments(grid: dict) -> list[dict]:
    segments: list[dict] = []
    for bar in grid["bars"]:
        bar_start = (int(bar["bar"]) - 1) * 4.0
        voicing = [int(value) for value in bar["voicing_midi"]]
        pattern = grid["patterns"][str(bar["pattern"])]
        if len(pattern) != 8:
            raise ValueError(f"pattern {bar['pattern']} must contain eight slots")
        for slot_index, (action_value, velocity_value) in enumerate(pattern):
            action = str(action_value)
            selected = select_notes(voicing, action)
            if not selected:
                continue
            direction = str(grid["hand_clock"][slot_index])
            ordered = selected if direction == "down" else list(reversed(selected))
            total_spread_beats = 0.050 if direction == "down" else 0.034
            spread_step = total_spread_beats / max(1, len(ordered) - 1)
            for string_index, pitch in enumerate(ordered):
                start = bar_start + slot_index * 0.5 + string_index * spread_step
                velocity = int(velocity_value)
                velocity -= string_index if direction == "down" else max(
                    0, len(ordered) - string_index - 1
                )
                segments.append(
                    {
                        "pitch": int(pitch),
                        "start": start,
                        "end": start + duration_beats(action),
                        "velocity": max(1, min(127, velocity)),
                    }
                )

    by_pitch: dict[int, list[dict]] = defaultdict(list)
    for segment in segments:
        by_pitch[int(segment["pitch"])].append(segment)
    for items in by_pitch.values():
        items.sort(key=lambda item: float(item["start"]))
        for previous, current in zip(items, items[1:]):
            if float(previous["end"]) >= float(current["start"]):
                previous["end"] = max(
                    float(previous["start"]) + 0.03,
                    float(current["start"]) - 1 / TPB,
                )
    return segments


def write_midi(grid: dict, segments: list[dict]) -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tempo = float(grid["tempo_bpm"])
    midi = mido.MidiFile(type=1, ticks_per_beat=TPB)

    conductor = mido.MidiTrack()
    conductor.append(mido.MetaMessage("track_name", name=grid["title"], time=0))
    conductor.append(
        mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo), time=0)
    )
    conductor.append(
        mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0)
    )
    midi.tracks.append(conductor)

    track = mido.MidiTrack()
    track.append(
        mido.MetaMessage("track_name", name="Acoustic Guitar Strumming", time=0)
    )
    track.append(mido.Message("program_change", channel=0, program=25, time=0))
    track.append(
        mido.Message("control_change", channel=0, control=10, value=50, time=0)
    )

    events: list[tuple[int, int, mido.Message]] = []
    for segment in segments:
        start_tick = round(float(segment["start"]) * TPB)
        end_tick = max(start_tick + 1, round(float(segment["end"]) * TPB))
        events.append(
            (
                start_tick,
                1,
                mido.Message(
                    "note_on",
                    channel=0,
                    note=int(segment["pitch"]),
                    velocity=int(segment["velocity"]),
                    time=0,
                ),
            )
        )
        events.append(
            (
                end_tick,
                0,
                mido.Message(
                    "note_off",
                    channel=0,
                    note=int(segment["pitch"]),
                    velocity=0,
                    time=0,
                ),
            )
        )

    events.sort(key=lambda item: (item[0], item[1], getattr(item[2], "note", -1)))
    previous_tick = 0
    for tick, _, message in events:
        message.time = tick - previous_tick
        track.append(message)
        previous_tick = tick
    midi.tracks.append(track)

    path = OUTPUT / "acoustic_strumming_fragment.mid"
    midi.save(path)
    return path


def pluck(freq: float, duration: float, velocity: int, rng: np.random.Generator) -> np.ndarray:
    count = max(1, int(duration * SR))
    t = np.arange(count, dtype=np.float64) / SR
    signal = np.zeros(count, dtype=np.float64)
    phases = rng.uniform(0, 2 * math.pi, 8)
    for harmonic in range(1, 9):
        decay = np.exp(-t * (2.0 + harmonic * 0.38))
        signal += (
            np.sin(2 * math.pi * freq * harmonic * t + phases[harmonic - 1])
            * decay
            / harmonic**1.25
        )
    signal += rng.standard_normal(count) * np.exp(-t * 60) * 0.10
    signal *= 1 - np.exp(-t * 180)
    signal *= velocity / 127
    return signal


def write_preview(grid: dict, segments: list[dict]) -> Path:
    tempo = float(grid["tempo_bpm"])
    seconds_per_beat = 60.0 / tempo
    total_seconds = len(grid["bars"]) * 4 * seconds_per_beat + 2.0
    audio = np.zeros(int(total_seconds * SR), dtype=np.float64)
    rng = np.random.default_rng(20260814)

    for segment in segments:
        start = int(float(segment["start"]) * seconds_per_beat * SR)
        duration = max(
            0.05,
            (float(segment["end"]) - float(segment["start"]))
            * seconds_per_beat,
        )
        frequency = 440.0 * 2 ** ((int(segment["pitch"]) - 69) / 12)
        tone = pluck(frequency, duration, int(segment["velocity"]), rng)
        end = min(len(audio), start + len(tone))
        audio[start:end] += tone[: end - start] * 0.12

    for delay_seconds, gain in ((0.045, 0.20), (0.092, 0.11), (0.155, 0.07)):
        delay = int(delay_seconds * SR)
        audio[delay:] += audio[:-delay] * gain

    audio = np.tanh(audio * 1.2)
    peak = float(np.max(np.abs(audio)))
    if peak > 0:
        audio *= (10 ** (-1 / 20)) / peak
    stereo = np.column_stack([audio * 0.95, audio * 0.82])
    pcm = np.clip(stereo * 32767, -32768, 32767).astype("<i2")

    path = OUTPUT / "acoustic_strumming_fragment.wav"
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(pcm.tobytes())
    return path


def validate_midi(path: Path) -> None:
    active: dict[tuple[int, int], int] = defaultdict(int)
    note_ons = 0
    note_offs = 0
    midi = mido.MidiFile(path)
    for track in midi.tracks:
        for message in track:
            if message.type == "note_on" and message.velocity > 0:
                active[(message.channel, message.note)] += 1
                note_ons += 1
            elif message.type == "note_off" or (
                message.type == "note_on" and message.velocity == 0
            ):
                active[(message.channel, message.note)] -= 1
                note_offs += 1
    unbalanced = {key: value for key, value in active.items() if value != 0}
    if unbalanced or note_ons != note_offs:
        raise RuntimeError(
            f"unbalanced MIDI: ons={note_ons}, offs={note_offs}, active={unbalanced}"
        )
    print(f"[OK] note-ons/note-offs: {note_ons}/{note_offs}")


def main() -> None:
    grid = json.loads((HERE / "action_grid.json").read_text(encoding="utf-8"))
    segments = build_segments(grid)
    midi_path = write_midi(grid, segments)
    wav_path = write_preview(grid, segments)
    validate_midi(midi_path)
    print(f"[OK] MIDI: {midi_path}")
    print(f"[OK] WAV preview: {wav_path}")


if __name__ == "__main__":
    main()
