from __future__ import annotations

from collections import defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping

import mido

from .pmt import PMTNote, decode_tokens, encode_notes, serialize_tokens

SUPPORTED_CHANNEL_EVENTS = {
    "control_change",
    "program_change",
    "pitchwheel",
    "aftertouch",
    "polytouch",
}


def _safe_name(value: str, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip()).strip("_.")
    return text or fallback


def _merged_meta_events(midi: mido.MidiFile) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    tick = 0
    for order, message in enumerate(mido.merge_tracks(midi.tracks)):
        tick += message.time
        if message.type == "set_tempo":
            result.append({"type": "set_tempo", "tick": tick, "order": order, "tempo": int(message.tempo)})
        elif message.type == "time_signature":
            result.append({
                "type": "time_signature", "tick": tick, "order": order,
                "numerator": int(message.numerator), "denominator": int(message.denominator),
                "clocks_per_click": int(message.clocks_per_click),
                "notated_32nd_notes_per_beat": int(message.notated_32nd_notes_per_beat),
            })
        elif message.type == "key_signature":
            result.append({"type": "key_signature", "tick": tick, "order": order, "key": str(message.key)})
        elif message.type == "sysex":
            result.append({"type": "sysex", "tick": tick, "order": order, "data": list(message.data)})
    return result


def effective_tempo_map(conductor_events: Iterable[Mapping[str, Any]]) -> list[tuple[int, int]]:
    raw = sorted(
        ((int(event["tick"]), int(event["order"]), int(event["tempo"]))
         for event in conductor_events if event.get("type") == "set_tempo"),
        key=lambda item: (item[0], item[1]),
    )
    result: list[tuple[int, int]] = []
    for tick, _, tempo in raw:
        if result and result[-1][0] == tick:
            result[-1] = (tick, tempo)
        else:
            result.append((tick, tempo))
    if not result or result[0][0] != 0:
        result.insert(0, (0, 500000))
    return result


def ticks_to_microseconds(tick: int, tempo_map: list[tuple[int, int]], ticks_per_beat: int) -> float:
    total = 0.0
    for index, (start_tick, tempo) in enumerate(tempo_map):
        if tick <= start_tick:
            break
        next_tick = tempo_map[index + 1][0] if index + 1 < len(tempo_map) else tick
        end_tick = min(tick, next_tick)
        if end_tick > start_tick:
            total += (end_tick - start_tick) * tempo / ticks_per_beat
        if tick < next_tick:
            break
    return total


def _message_to_dict(message: mido.Message, tick: int, order: int) -> dict[str, Any]:
    result: dict[str, Any] = {"type": message.type, "tick": tick, "order": order}
    if message.type == "control_change":
        result.update(control=int(message.control), value=int(message.value))
    elif message.type == "program_change":
        result.update(program=int(message.program))
    elif message.type == "pitchwheel":
        result.update(pitch=int(message.pitch))
    elif message.type == "aftertouch":
        result.update(value=int(message.value))
    elif message.type == "polytouch":
        result.update(note=int(message.note), value=int(message.value))
    else:
        raise ValueError(f"unsupported sidecar event: {message.type}")
    return result


def _extract_track_channel(
    source_track_index: int,
    track: mido.MidiTrack,
    channel: int,
    tempo_map: list[tuple[int, int]],
    ticks_per_beat: int,
) -> tuple[list[PMTNote], list[dict[str, Any]], str, set[int], int]:
    tick = 0
    programs: dict[int, int] = defaultdict(int)
    pending: dict[tuple[int, int], deque[tuple[int, int, int]]] = defaultdict(deque)
    notes: list[PMTNote] = []
    events: list[dict[str, Any]] = []
    track_name = ""
    programs_seen: set[int] = set()
    unmatched = 0

    for order, message in enumerate(track):
        tick += message.time
        if message.type == "track_name":
            track_name = str(message.name)
            continue
        if not hasattr(message, "channel") or int(message.channel) != channel:
            continue
        if message.type == "program_change":
            programs[channel] = int(message.program)
            programs_seen.add(int(message.program))
            events.append(_message_to_dict(message, tick, order))
            continue
        if message.type in SUPPORTED_CHANNEL_EVENTS:
            events.append(_message_to_dict(message, tick, order))
            continue
        if message.type == "note_on" and message.velocity > 0:
            program = 128 if channel == 9 else programs[channel]
            programs_seen.add(program)
            pending[(channel, int(message.note))].append((tick, int(message.velocity), program))
            continue
        if message.type == "note_off" or (message.type == "note_on" and message.velocity == 0):
            queue = pending[(channel, int(message.note))]
            if not queue:
                unmatched += 1
                continue
            start_tick, velocity, program = queue.popleft()
            onset_us = ticks_to_microseconds(start_tick, tempo_map, ticks_per_beat)
            end_us = ticks_to_microseconds(tick, tempo_map, ticks_per_beat)
            notes.append(PMTNote(
                track=0,
                program=program,
                pitch=int(message.note),
                onset_ms=max(0, round(onset_us / 1000.0)),
                duration_ms=max(1, round((end_us - onset_us) / 1000.0)),
                velocity=velocity,
            ))

    unmatched += sum(len(queue) for queue in pending.values())
    fallback = f"src{source_track_index:02d}_ch{channel + 1:02d}"
    return notes, events, _safe_name(track_name, fallback), programs_seen, unmatched


def import_midi(midi_path: Path) -> dict[str, Any]:
    midi = mido.MidiFile(midi_path)
    conductor_events = _merged_meta_events(midi)
    tempo_map = effective_tempo_map(conductor_events)
    ticks_per_beat = int(midi.ticks_per_beat)

    units: list[tuple[int, int]] = []
    for source_track_index, track in enumerate(midi.tracks):
        channels = sorted({
            int(message.channel)
            for message in track
            if hasattr(message, "channel") and message.type in {"note_on", "note_off"}
        })
        for channel in channels:
            if any(
                hasattr(message, "channel")
                and int(message.channel) == channel
                and message.type == "note_on"
                and message.velocity > 0
                for message in track
            ):
                units.append((source_track_index, channel))

    if len(units) > 16:
        raise ValueError(f"PMT supports at most 16 active tracks, source requires {len(units)}")

    all_notes: list[PMTNote] = []
    tracks_meta: dict[str, Any] = {}
    sidecar_tracks: dict[str, Any] = {}
    unsupported_messages: dict[str, int] = defaultdict(int)
    used_names: set[str] = set()
    total_unmatched = 0

    for pmt_track, (source_track_index, channel) in enumerate(units):
        notes, events, base_name, programs_seen, unmatched = _extract_track_channel(
            source_track_index,
            midi.tracks[source_track_index],
            channel,
            tempo_map,
            ticks_per_beat,
        )
        total_unmatched += unmatched
        name = base_name
        suffix = 2
        while name in used_names:
            name = f"{base_name}_{suffix}"
            suffix += 1
        used_names.add(name)

        mapped_notes = [
            PMTNote(
                track=pmt_track,
                program=note.program,
                pitch=note.pitch,
                onset_ms=note.onset_ms,
                duration_ms=note.duration_ms,
                velocity=note.velocity,
            )
            for note in notes
        ]
        all_notes.extend(mapped_notes)
        source_program = min(programs_seen) if programs_seen else (128 if channel == 9 else 0)
        tracks_meta[str(pmt_track)] = {
            "name": name,
            "source_track_index": source_track_index,
            "channel": channel,
            "bank": 0,
            "source_programs": sorted(programs_seen),
            "source_program": source_program,
            "note_count": len(mapped_notes),
        }
        sidecar_tracks[str(pmt_track)] = {
            "name": name,
            "source_track_index": source_track_index,
            "channel": channel,
            "events": events,
        }

    for track in midi.tracks:
        for message in track:
            if message.type == "sequencer_specific":
                unsupported_messages[message.type] += 1

    tokens = encode_notes(all_notes)
    time_signature = [4, 4]
    for event in conductor_events:
        if event["type"] == "time_signature" and int(event["tick"]) == 0:
            time_signature = [int(event["numerator"]), int(event["denominator"])]

    metadata = {
        "title": midi_path.stem,
        "source_filename": midi_path.name,
        "ticks_per_beat": ticks_per_beat,
        "tempo_microseconds_per_beat": int(tempo_map[0][1]),
        "time_signature": time_signature,
        "tracks": tracks_meta,
    }
    sidecar = {
        "schema": "music-agent-midi-sidecar",
        "schema_version": 1,
        "ticks_per_beat": ticks_per_beat,
        "conductor_events": conductor_events,
        "tracks": sidecar_tracks,
    }
    decoded_notes = decode_tokens(tokens)
    source_normalized = sorted(
        (n.track, n.program, n.pitch, n.onset_ms, n.duration_ms, n.velocity)
        for n in all_notes
    )
    pmt_normalized = sorted(
        (n.track, n.program, n.pitch, n.onset_ms, n.duration_ms, n.velocity)
        for n in decoded_notes
    )
    fingerprint = {
        "source_filename": midi_path.name,
        "source_sha256": sha256(midi_path.read_bytes()).hexdigest(),
        "midi_type": int(midi.type),
        "ticks_per_beat": ticks_per_beat,
        "active_tracks": len(units),
        "note_count": len(all_notes),
        "source_note_tuple_sha256": sha256(json.dumps(source_normalized, separators=(",", ":")).encode()).hexdigest(),
        "pmt_note_tuple_sha256": sha256(json.dumps(pmt_normalized, separators=(",", ":")).encode()).hexdigest(),
        "channel_event_count": sum(len(item["events"]) for item in sidecar_tracks.values()),
        "conductor_event_count": len(conductor_events),
        "unmatched_note_events": total_unmatched,
        "unsupported_messages": dict(sorted(unsupported_messages.items())),
    }
    return {
        "notes": all_notes,
        "tokens": tokens,
        "metadata": metadata,
        "sidecar": sidecar,
        "fingerprint": fingerprint,
    }


def write_project(midi_path: Path, project_path: Path) -> dict[str, Any]:
    result = import_midi(midi_path)
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / "performance.pmt").write_text(serialize_tokens(result["tokens"]), encoding="utf-8")
    for filename, key in (
        ("performance.meta.json", "metadata"),
        ("performance.midi-sidecar.json", "sidecar"),
        ("source-fingerprint.json", "fingerprint"),
    ):
        (project_path / filename).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    instruments = {
        item["name"]: {"engine": "fluidsynth", "source_program": item["source_program"], "channel": item["channel"] + 1}
        for item in result["metadata"]["tracks"].values()
    }
    mix = {
        item["name"]: {"volume_db": 0.0, "pan": 0.0, "mute": False}
        for item in result["metadata"]["tracks"].values()
    }
    (project_path / "instruments.json").write_text(json.dumps(instruments, indent=2) + "\n", encoding="utf-8")
    render = {
        "sample_rate": 44100,
        "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
        "fluidsynth_gain": 0.65,
        "tail_seconds": 2.0,
        "master_peak_db": -1.0,
        "mix": mix,
        "render_full_midi_direct": True,
    }
    (project_path / "render.json").write_text(json.dumps(render, indent=2) + "\n", encoding="utf-8")
    return result
