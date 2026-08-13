from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mido

from src.midi.pitches import drum_number, note_number

TICKS_PER_BEAT = 480


@dataclass(frozen=True)
class NoteEvent:
    start: float
    duration: float
    pitch: int
    velocity: int


def generate_song_midis(
    composition: dict[str, Any],
    instruments: dict[str, Any],
    project_path: Path,
    track_names: set[str] | None = None,
) -> dict[str, Path]:
    tracks_dir = project_path / "tracks"
    output_dir = project_path / "output"
    tracks_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated: dict[str, Path] = {}
    full_midi = mido.MidiFile(type=1, ticks_per_beat=TICKS_PER_BEAT)
    full_midi.tracks.append(_conductor_track(composition))

    for index, (track_name, track_data) in enumerate(composition["tracks"].items()):
        if track_names is not None and track_name not in track_names:
            continue
        if track_name not in instruments:
            raise KeyError(f"instrument mapping is missing track '{track_name}'")
        instrument = instruments[track_name]
        channel = _channel_for(track_name, instrument, index)
        events = _expand_track(composition, track_data)
        midi_track = _musical_track(track_name, instrument, channel, events)

        standalone = mido.MidiFile(type=1, ticks_per_beat=TICKS_PER_BEAT)
        standalone.tracks.append(_conductor_track(composition))
        standalone.tracks.append(mido.MidiTrack(midi_track))
        path = tracks_dir / f"{track_name}.mid"
        standalone.save(path)
        generated[track_name] = path
        full_midi.tracks.append(midi_track)

    if track_names is None:
        full_path = output_dir / "full_song.mid"
        full_midi.save(full_path)
        generated["full_song"] = full_path
    return generated


def _channel_for(track_name: str, instrument: dict[str, Any], index: int) -> int:
    configured = instrument.get("channel")
    if configured is not None:
        channel = int(configured) - 1
    else:
        available = [value for value in range(16) if value != 9]
        channel = available[index % len(available)]
    if not 0 <= channel <= 15:
        raise ValueError(f"invalid MIDI channel for {track_name}: {channel + 1}")
    return channel


def _conductor_track(composition: dict[str, Any]) -> mido.MidiTrack:
    metadata = composition["metadata"]
    numerator, denominator = (int(part) for part in metadata["time_signature"].split("/"))
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name=_midi_text(metadata["title"]), time=0))
    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(metadata["tempo"]), time=0))
    track.append(
        mido.MetaMessage("time_signature", numerator=numerator, denominator=denominator, time=0)
    )
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def _musical_track(
    name: str, instrument: dict[str, Any], channel: int, notes: list[NoteEvent]
) -> mido.MidiTrack:
    messages: list[tuple[int, int, mido.Message]] = []
    for note in notes:
        start_tick = round(note.start * TICKS_PER_BEAT)
        end_tick = round((note.start + note.duration) * TICKS_PER_BEAT)
        messages.append((start_tick, 1, mido.Message("note_on", note=note.pitch, velocity=note.velocity, channel=channel)))
        messages.append((end_tick, 0, mido.Message("note_off", note=note.pitch, velocity=0, channel=channel)))
    messages.sort(key=lambda item: (item[0], item[1], item[2].note))

    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name=_midi_text(name), time=0))
    # FluidSynth uses the combined 14-bit bank number. Percussion banks (120
    # and 128 in GeneralUser GS) also need these messages on MIDI channel 10;
    # omitting them made every configured drum kit fall back to Standard 1.
    bank = int(instrument.get("bank", 128 if channel == 9 else 0))
    track.append(mido.Message("control_change", control=0, value=(bank >> 7) & 0x7F, channel=channel, time=0))
    track.append(mido.Message("control_change", control=32, value=bank & 0x7F, channel=channel, time=0))
    track.append(mido.Message("program_change", program=int(instrument.get("program", 0)), channel=channel, time=0))
    previous_tick = 0
    for absolute_tick, _, message in messages:
        message.time = absolute_tick - previous_tick
        track.append(message)
        previous_tick = absolute_tick
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def _expand_track(composition: dict[str, Any], track_data: dict[str, Any]) -> list[NoteEvent]:
    numerator = int(composition["metadata"]["time_signature"].split("/")[0])
    section_offset_bars = 0
    notes: list[NoteEvent] = []
    for section in composition["sections"]:
        name, section_bars = section["name"], section["bars"]
        clip = track_data.get("sections", {}).get(name)
        if clip:
            loop_bars = int(clip["loop_bars"])
            for loop_start in range(0, section_bars, loop_bars):
                for event in clip.get("events", []):
                    if event.get("type", "note") == "rest":
                        continue
                    local_bar, beat = _parse_position(event["at"])
                    effective_bar = loop_start + local_bar - 1
                    if effective_bar >= section_bars:
                        continue
                    start = (section_offset_bars + effective_bar) * numerator + (beat - 1)
                    duration = float(event["duration"])
                    velocity = int(event["velocity"])
                    pitches = _event_pitches(event)
                    for pitch in pitches:
                        notes.append(NoteEvent(start, duration, pitch, velocity))
        section_offset_bars += section_bars
    return notes


def _parse_position(value: str) -> tuple[int, float]:
    bar, beat = value.split(":", 1)
    return int(bar), float(beat)


def _event_pitches(event: dict[str, Any]) -> list[int]:
    event_type = event.get("type", "note")
    if event_type == "drum":
        return [drum_number(event["note"])]
    if event_type == "chord":
        return [note_number(pitch) for pitch in event["pitches"]]
    return [note_number(event["pitch"])]


def _midi_text(value: object) -> str:
    """Keep JSON metadata Unicode while making standard MIDI text portable."""
    return str(value).encode("latin-1", errors="replace").decode("latin-1")
