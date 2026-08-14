from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mido

from src.accompaniment.generator import materialize_clip
from src.midi.pitches import drum_number, note_number

TICKS_PER_BEAT = 480


@dataclass(frozen=True)
class NoteEvent:
    start: float
    duration: float
    pitch: int
    velocity: int
    articulations: tuple[str, ...] = ()
    profile_triggers: tuple[tuple[str, int, int, int], ...] = ()
    pitch_curve: tuple[tuple[float, int], ...] = ()


@dataclass(frozen=True)
class ControlEvent:
    start: float
    control: int
    value: int


PerformanceEvent = NoteEvent | ControlEvent


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
        events = _expand_track(composition, track_name, track_data)
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
    name: str, instrument: dict[str, Any], channel: int, notes: list[PerformanceEvent]
) -> mido.MidiTrack:
    messages: list[tuple[int, int, mido.Message]] = []
    sounding = [note for note in notes if isinstance(note, NoteEvent)]
    for note in notes:
        if isinstance(note, ControlEvent):
            tick = round(note.start * TICKS_PER_BEAT)
            messages.append((tick, 0, mido.Message("control_change", control=note.control, value=note.value, channel=channel)))
            continue
        start_tick = round(note.start * TICKS_PER_BEAT)
        end_tick = round((note.start + note.duration) * TICKS_PER_BEAT)
        for trigger_type, data1, data2, lead_ticks in note.profile_triggers:
            trigger_tick = max(0, start_tick - lead_ticks)
            if trigger_type == "keyswitch":
                messages.append((trigger_tick, 0, mido.Message("note_on", note=data1, velocity=data2, channel=channel)))
                messages.append((start_tick, 0, mido.Message("note_off", note=data1, velocity=0, channel=channel)))
        messages.append((start_tick, 1, mido.Message("note_on", note=note.pitch, velocity=note.velocity, channel=channel)))
        messages.append((end_tick, 0, mido.Message("note_off", note=note.pitch, velocity=0, channel=channel)))
        channel_safe = not any(
            other is not note and other.start < note.start + note.duration and
            other.start + other.duration > note.start
            for other in sounding
        )
        if channel_safe:
            for relative_beat, pitch_value in note.pitch_curve:
                messages.append((round((note.start + relative_beat) * TICKS_PER_BEAT), 2,
                                 mido.Message("pitchwheel", pitch=max(-8192, min(8191, pitch_value)), channel=channel)))
    # Identical keyswitch/control events from a strummed chord are a single physical action.
    unique: dict[tuple[int, str, int, int], tuple[int, int, mido.Message]] = {}
    passthrough: list[tuple[int, int, mido.Message]] = []
    for item in messages:
        tick, order, message = item
        if message.type in {"control_change", "pitchwheel"} or (message.type in {"note_on", "note_off"} and getattr(message, "note", 127) < 36):
            key = (tick, message.type, getattr(message, "note", getattr(message, "control", 0)),
                   getattr(message, "velocity", getattr(message, "value", getattr(message, "pitch", 0))))
            unique[key] = item
        else:
            passthrough.append(item)
    messages = passthrough + list(unique.values())
    messages.sort(key=lambda item: (item[0], item[1], getattr(item[2], "note", getattr(item[2], "control", 0))))

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


def _foreground_track(track_name: str, track_data: dict[str, Any]) -> bool:
    text = f"{track_name} {track_data.get('role', '')}".lower()
    return any(token in text for token in ("vocal", "lead melody", "main melody", "foreground", "hook", "主旋律"))


def derive_foreground_activity(
    composition: dict[str, Any], current_track_name: str, section_name: str, loop_bars: int,
) -> list[dict[str, Any]]:
    """Return sixteenth-step foreground occupancy without changing source composition."""
    beats = int(composition["metadata"]["time_signature"].split("/")[0])
    step_duration = beats / 16
    active = [set() for _ in range(loop_bars)]
    onsets = [set() for _ in range(loop_bars)]
    long_holds = [set() for _ in range(loop_bars)]
    for track_name, track_data in composition.get("tracks", {}).items():
        if track_name == current_track_name or not _foreground_track(track_name, track_data):
            continue
        clip = track_data.get("sections", {}).get(section_name)
        if not clip:
            continue
        try:
            events = materialize_clip(deepcopy(clip), track_data, beats)
        except (KeyError, ValueError):
            events = [deepcopy(event) for event in clip.get("events", [])]
        for event in events:
            if event.get("type", "note") in {"rest", "control_change"}:
                continue
            local_bar, beat = _parse_position(event["at"])
            if not 1 <= local_bar <= loop_bars:
                continue
            start = (local_bar - 1) * beats + beat - 1
            duration = max(0.0, float(event.get("duration", 0)))
            end = min(loop_bars * beats, start + duration)
            onset_step = min(15, max(0, int(round((beat - 1) / step_duration))))
            onsets[local_bar - 1].add(onset_step)
            cursor = start
            while cursor < end - 1e-8:
                bar = int(cursor // beats)
                if bar >= loop_bars:
                    break
                step = min(15, int((cursor - bar * beats) / step_duration + 1e-8))
                active[bar].add(step)
                if cursor >= start + 1.0:
                    long_holds[bar].add(step)
                cursor += step_duration
    result = []
    for bar in range(loop_bars):
        if not active[bar] and not onsets[bar]:
            continue
        breath_steps = {step for step in range(16) if step not in active[bar]}
        release_steps = sorted(breath_steps | long_holds[bar])
        result.append({"bar": bar + 1, "active_steps": sorted(active[bar]),
                       "onset_steps": sorted(onsets[bar]), "release_steps": release_steps,
                       "long_hold_steps": sorted(long_holds[bar])})
    return result


def _expand_track(composition: dict[str, Any], track_name: str, track_data: dict[str, Any]) -> list[PerformanceEvent]:
    numerator = int(composition["metadata"]["time_signature"].split("/")[0])
    section_offset_bars = 0
    notes: list[PerformanceEvent] = []
    for section in composition["sections"]:
        name, section_bars = section["name"], section["bars"]
        clip = track_data.get("sections", {}).get(name)
        if clip:
            loop_bars = int(clip["loop_bars"])
            working_clip = clip
            phrase = clip.get("instrument_phrase")
            if phrase and phrase.get("foreground_aware") and not phrase.get("foreground_activity"):
                working_clip = deepcopy(clip)
                working_clip["instrument_phrase"]["foreground_activity"] = derive_foreground_activity(
                    composition, track_name, name, loop_bars
                )
            events = materialize_clip(working_clip, track_data, numerator)
            for loop_start in range(0, section_bars, loop_bars):
                for event in events:
                    if event.get("type", "note") == "rest":
                        continue
                    local_bar, beat = _parse_position(event["at"])
                    effective_bar = loop_start + local_bar - 1
                    if effective_bar >= section_bars:
                        continue
                    start = (section_offset_bars + effective_bar) * numerator + (beat - 1)
                    if event.get("type") == "control_change":
                        notes.append(ControlEvent(start, int(event["control"]), int(event["value"])))
                        continue
                    duration = float(event["duration"])
                    velocity = int(event["velocity"])
                    pitches = _event_pitches(event)
                    triggers = []
                    for trigger in event.get("profile_triggers", []):
                        if trigger.get("type") == "keyswitch":
                            triggers.append(("keyswitch", int(trigger["note"]), int(trigger.get("velocity", 64)), int(trigger.get("lead_ticks", 24))))
                    pitch_curve: list[tuple[float, int]] = []
                    bend = event.get("bend_semitones")
                    bend_range = float(event.get("_pitch_bend_range", 2.0))
                    slide_from = event.get("slide_from_semitones")
                    if slide_from is not None and bend_range > 0:
                        start_value = round(max(-1.0, min(1.0, float(slide_from) / bend_range)) * 8191)
                        pitch_curve.extend([
                            (0.0, start_value),
                            (duration * 0.12, round(start_value * 0.86)),
                            (duration * 0.24, round(start_value * 0.62)),
                            (duration * 0.38, round(start_value * 0.34)),
                            (duration * 0.52, round(start_value * 0.12)),
                            (duration * 0.62, 0),
                        ])
                    if bend is not None and bend_range > 0:
                        value = round(max(-1.0, min(1.0, float(bend) / bend_range)) * 8191)
                        pitch_curve.extend([
                            (duration * 0.18, round(value * 0.2)),
                            (duration * 0.30, round(value * 0.5)),
                            (duration * 0.45, round(value * 0.8)),
                            (duration * 0.58, value),
                            (duration * 0.80, value),
                            (duration * 0.92, round(value * 0.4)),
                            (duration * 0.98, 0),
                        ])
                    vibrato = event.get("vibrato")
                    if isinstance(vibrato, dict):
                        delay = float(vibrato.get("delay", 0.35))
                        depth = max(0.0, min(1.0, float(vibrato.get("depth", 0.3))))
                        cursor = delay
                        sign = 1
                        while cursor < duration - 0.05:
                            pitch_curve.append((cursor, round(sign * depth * 2048)))
                            sign *= -1
                            cursor += 0.125
                        pitch_curve.append((max(delay, duration - 0.03), 0))
                    for pitch in pitches:
                        notes.append(NoteEvent(start, duration, pitch, velocity,
                                               tuple(event.get("articulations", [])), tuple(triggers), tuple(pitch_curve)))
        section_offset_bars += section_bars
    if any(clip.get("instrument_phrase") for clip in track_data.get("sections", {}).values()):
        notes = _trim_semantic_same_pitch_overlaps(notes)
    return notes


def _trim_semantic_same_pitch_overlaps(events: list[PerformanceEvent]) -> list[PerformanceEvent]:
    """New semantic tracks may request legato, but one MIDI key must not retrigger while active.

    This deliberately does not run for legacy event clips, preserving their MIDI bytes.
    """
    notes = [event for event in events if isinstance(event, NoteEvent)]
    next_start: dict[tuple[int, float], float] = {}
    by_pitch: dict[int, list[NoteEvent]] = {}
    for event in notes:
        by_pitch.setdefault(event.pitch, []).append(event)
    for pitch_events in by_pitch.values():
        ordered = sorted(pitch_events, key=lambda event: event.start)
        for current, following in zip(ordered, ordered[1:]):
            if current.start + current.duration > following.start:
                next_start[(id(current), current.start)] = following.start
    result: list[PerformanceEvent] = []
    for event in events:
        if isinstance(event, NoteEvent):
            end = next_start.get((id(event), event.start))
            if end is not None:
                event = NoteEvent(event.start, max(0.05, end - event.start), event.pitch, event.velocity,
                                  event.articulations, event.profile_triggers, event.pitch_curve)
        result.append(event)
    return result


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
