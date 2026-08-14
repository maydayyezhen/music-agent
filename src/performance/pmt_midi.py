from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import mido

from .midi_import import effective_tempo_map
from .pmt import PMTError, PMTNote


def _tempo_segments(tempo_map: list[tuple[int, int]], ticks_per_beat: int) -> list[tuple[int, float, int]]:
    segments: list[tuple[int, float, int]] = []
    elapsed_ms = 0.0
    for index, (tick, tempo) in enumerate(tempo_map):
        if index:
            prev_tick, _, prev_tempo = segments[-1]
            elapsed_ms += (tick - prev_tick) * prev_tempo / ticks_per_beat / 1000.0
        segments.append((tick, elapsed_ms, tempo))
    return segments


def milliseconds_to_ticks(milliseconds: int | float, *, tempo_map: list[tuple[int, int]], ticks_per_beat: int) -> int:
    if ticks_per_beat <= 0:
        raise PMTError("ticks_per_beat must be positive")
    target = max(0.0, float(milliseconds))
    segments = _tempo_segments(tempo_map, ticks_per_beat)
    for index, (start_tick, start_ms, tempo) in enumerate(segments):
        next_ms = segments[index + 1][1] if index + 1 < len(segments) else None
        if next_ms is None or target < next_ms:
            return round(start_tick + (target - start_ms) * 1000.0 * ticks_per_beat / tempo)
    start_tick, start_ms, tempo = segments[-1]
    return round(start_tick + (target - start_ms) * 1000.0 * ticks_per_beat / tempo)


def _meta_message(event: Mapping[str, Any]) -> mido.Message | mido.MetaMessage:
    event_type = str(event["type"])
    if event_type == "set_tempo":
        return mido.MetaMessage("set_tempo", tempo=int(event["tempo"]))
    if event_type == "time_signature":
        return mido.MetaMessage(
            "time_signature",
            numerator=int(event["numerator"]),
            denominator=int(event["denominator"]),
            clocks_per_click=int(event.get("clocks_per_click", 24)),
            notated_32nd_notes_per_beat=int(event.get("notated_32nd_notes_per_beat", 8)),
        )
    if event_type == "key_signature":
        return mido.MetaMessage("key_signature", key=str(event["key"]))
    if event_type == "sysex":
        return mido.Message("sysex", data=tuple(int(value) for value in event["data"]))
    raise PMTError(f"unsupported conductor event: {event_type}")


def _channel_message(event: Mapping[str, Any], channel: int) -> mido.Message:
    event_type = str(event["type"])
    if event_type == "control_change":
        return mido.Message("control_change", channel=channel, control=int(event["control"]), value=int(event["value"]))
    if event_type == "program_change":
        return mido.Message("program_change", channel=channel, program=int(event["program"]))
    if event_type == "pitchwheel":
        return mido.Message("pitchwheel", channel=channel, pitch=int(event["pitch"]))
    if event_type == "aftertouch":
        return mido.Message("aftertouch", channel=channel, value=int(event["value"]))
    if event_type == "polytouch":
        return mido.Message("polytouch", channel=channel, note=int(event["note"]), value=int(event["value"]))
    raise PMTError(f"unsupported channel event: {event_type}")


def _conductor_track(*, title: str, metadata: Mapping[str, Any], sidecar: Mapping[str, Any] | None) -> mido.MidiTrack:
    messages: list[tuple[int, int, mido.Message | mido.MetaMessage]] = []
    if sidecar and sidecar.get("conductor_events"):
        for event in sidecar["conductor_events"]:
            messages.append((int(event["tick"]), int(event.get("order", 0)), _meta_message(event)))
    else:
        messages.append((0, 0, mido.MetaMessage("set_tempo", tempo=int(metadata["tempo_microseconds_per_beat"]))))
        signature = metadata.get("time_signature", [4, 4])
        messages.append((0, 1, mido.MetaMessage("time_signature", numerator=int(signature[0]), denominator=int(signature[1]))))
    messages.sort(key=lambda item: (item[0], item[1]))
    track = mido.MidiTrack([mido.MetaMessage("track_name", name=title, time=0)])
    previous_tick = 0
    for tick, _, message in messages:
        message.time = tick - previous_tick
        track.append(message)
        previous_tick = tick
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def _musical_track(notes: Sequence[PMTNote], *, name: str, channel: int, bank: int, ticks_per_beat: int,
                   tempo_map: list[tuple[int, int]], sidecar_track: Mapping[str, Any] | None) -> mido.MidiTrack:
    if not 0 <= channel <= 15:
        raise PMTError(f"MIDI channel must be zero-based 0..15, got {channel}")
    messages: list[tuple[int, int, int, mido.Message]] = []
    has_sidecar_program = False
    if sidecar_track:
        for event in sidecar_track.get("events", []):
            msg = _channel_message(event, channel)
            has_sidecar_program = has_sidecar_program or msg.type == "program_change"
            messages.append((int(event["tick"]), 1, int(event.get("order", 0)), msg))

    active_program: int | None = None
    for sequence, note in enumerate(sorted(notes, key=lambda n: (n.onset_ms, n.pitch))):
        start_tick = milliseconds_to_ticks(note.onset_ms, tempo_map=tempo_map, ticks_per_beat=ticks_per_beat)
        end_tick = milliseconds_to_ticks(note.onset_ms + note.duration_ms, tempo_map=tempo_map, ticks_per_beat=ticks_per_beat)
        end_tick = max(start_tick + 1, end_tick)
        program = 0 if note.program == 128 else note.program
        if not has_sidecar_program and program != active_program:
            messages.append((start_tick, 1, -1000 + sequence, mido.Message("program_change", program=program, channel=channel)))
            active_program = program
        messages.append((start_tick, 2, sequence, mido.Message("note_on", note=note.pitch, velocity=note.velocity, channel=channel)))
        messages.append((end_tick, 0, sequence, mido.Message("note_off", note=note.pitch, velocity=0, channel=channel)))

    messages.sort(key=lambda item: (item[0], item[1], item[2], getattr(item[3], "note", -1)))
    track = mido.MidiTrack([mido.MetaMessage("track_name", name=name, time=0)])
    if not sidecar_track:
        track.append(mido.Message("control_change", control=0, value=(bank >> 7) & 0x7F, channel=channel, time=0))
        track.append(mido.Message("control_change", control=32, value=bank & 0x7F, channel=channel, time=0))
    previous_tick = 0
    for tick, _, _, message in messages:
        message.time = tick - previous_tick
        track.append(message)
        previous_tick = tick
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def generate_pmt_midis(notes: Sequence[PMTNote], project_path: Path, metadata: Mapping[str, Any],
                        sidecar: Mapping[str, Any] | None = None) -> dict[str, Path]:
    ticks_per_beat = int(metadata.get("ticks_per_beat", 480))
    title = str(metadata.get("title", "PMT Performance"))
    track_configs = metadata.get("tracks", {})
    conductor_events = sidecar.get("conductor_events", []) if sidecar else []
    tempo_map = effective_tempo_map(conductor_events)
    if not conductor_events:
        tempo_map = [(0, int(metadata["tempo_microseconds_per_beat"]))]

    grouped: dict[int, list[PMTNote]] = defaultdict(list)
    for note in notes:
        grouped[note.track].append(note)
    unknown = sorted(set(grouped) - {int(key) for key in track_configs})
    if unknown:
        raise PMTError(f"missing PMT track metadata for tracks: {unknown}")

    tracks_dir = project_path / "tracks"
    output_dir = project_path / "output"
    tracks_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    full_midi = mido.MidiFile(type=1, ticks_per_beat=ticks_per_beat)
    full_midi.tracks.append(_conductor_track(title=title, metadata=metadata, sidecar=sidecar))
    generated: dict[str, Path] = {}
    for track_index in sorted(grouped):
        config = track_configs[str(track_index)]
        name = str(config["name"])
        sidecar_track = sidecar.get("tracks", {}).get(str(track_index)) if sidecar else None
        midi_track = _musical_track(
            grouped[track_index],
            name=name,
            channel=int(config["channel"]),
            bank=int(config.get("bank", 0)),
            ticks_per_beat=ticks_per_beat,
            tempo_map=tempo_map,
            sidecar_track=sidecar_track,
        )
        standalone = mido.MidiFile(type=1, ticks_per_beat=ticks_per_beat)
        standalone.tracks.append(_conductor_track(title=title, metadata=metadata, sidecar=sidecar))
        standalone.tracks.append(mido.MidiTrack(midi_track))
        path = tracks_dir / f"{name}.mid"
        standalone.save(path)
        generated[name] = path
        full_midi.tracks.append(midi_track)
    full_path = output_dir / "full_song.mid"
    full_midi.save(full_path)
    generated["full_song"] = full_path
    return generated
