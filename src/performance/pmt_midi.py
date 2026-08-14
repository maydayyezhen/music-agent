from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import mido

from .pmt import PMTError, PMTNote


def milliseconds_to_ticks(
    milliseconds: int | float,
    *,
    tempo_us_per_beat: int,
    ticks_per_beat: int,
) -> int:
    if tempo_us_per_beat <= 0:
        raise PMTError("tempo_us_per_beat must be positive")
    if ticks_per_beat <= 0:
        raise PMTError("ticks_per_beat must be positive")
    return round(float(milliseconds) * 1000.0 * ticks_per_beat / tempo_us_per_beat)


def _conductor_track(
    *,
    title: str,
    tempo_us_per_beat: int,
    numerator: int,
    denominator: int,
) -> mido.MidiTrack:
    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name=title, time=0))
    track.append(mido.MetaMessage("set_tempo", tempo=tempo_us_per_beat, time=0))
    track.append(
        mido.MetaMessage(
            "time_signature",
            numerator=numerator,
            denominator=denominator,
            time=0,
        )
    )
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def _musical_track(
    notes: Sequence[PMTNote],
    *,
    name: str,
    channel: int,
    bank: int,
    tempo_us_per_beat: int,
    ticks_per_beat: int,
) -> mido.MidiTrack:
    if not 0 <= channel <= 15:
        raise PMTError(f"MIDI channel must be zero-based 0..15, got {channel}")
    if not 0 <= bank <= 16383:
        raise PMTError(f"MIDI bank must be 0..16383, got {bank}")

    messages: list[tuple[int, int, mido.Message]] = []
    active_program: int | None = None
    ordered = sorted(notes, key=lambda note: (note.onset_ms, note.pitch))

    for note in ordered:
        if note.program == 128:
            if channel != 9:
                raise PMTError("PMT drum program 128 requires MIDI channel 10")
        elif not 0 <= note.program <= 127:
            raise PMTError(f"invalid melodic program: {note.program}")

        start_tick = milliseconds_to_ticks(
            note.onset_ms,
            tempo_us_per_beat=tempo_us_per_beat,
            ticks_per_beat=ticks_per_beat,
        )
        duration_tick = max(
            1,
            milliseconds_to_ticks(
                note.duration_ms,
                tempo_us_per_beat=tempo_us_per_beat,
                ticks_per_beat=ticks_per_beat,
            ),
        )
        end_tick = start_tick + duration_tick

        program = 0 if note.program == 128 else note.program
        if program != active_program:
            messages.append(
                (
                    start_tick,
                    1,
                    mido.Message(
                        "program_change",
                        program=program,
                        channel=channel,
                    ),
                )
            )
            active_program = program

        messages.append(
            (
                start_tick,
                2,
                mido.Message(
                    "note_on",
                    note=note.pitch,
                    velocity=note.velocity,
                    channel=channel,
                ),
            )
        )
        messages.append(
            (
                end_tick,
                0,
                mido.Message(
                    "note_off",
                    note=note.pitch,
                    velocity=0,
                    channel=channel,
                ),
            )
        )

    messages.sort(
        key=lambda item: (
            item[0],
            item[1],
            getattr(item[2], "note", -1),
        )
    )

    track = mido.MidiTrack()
    track.append(mido.MetaMessage("track_name", name=name, time=0))
    track.append(
        mido.Message(
            "control_change",
            control=0,
            value=(bank >> 7) & 0x7F,
            channel=channel,
            time=0,
        )
    )
    track.append(
        mido.Message(
            "control_change",
            control=32,
            value=bank & 0x7F,
            channel=channel,
            time=0,
        )
    )

    previous_tick = 0
    for absolute_tick, _, message in messages:
        message.time = absolute_tick - previous_tick
        track.append(message)
        previous_tick = absolute_tick
    track.append(mido.MetaMessage("end_of_track", time=0))
    return track


def generate_pmt_midis(
    notes: Sequence[PMTNote],
    project_path: Path,
    metadata: Mapping[str, Any],
) -> dict[str, Path]:
    """Generate standalone track MIDIs and one full MIDI from decoded PMT notes."""

    tempo_us_per_beat = int(metadata["tempo_microseconds_per_beat"])
    ticks_per_beat = int(metadata.get("ticks_per_beat", 480))
    signature = metadata.get("time_signature", [4, 4])
    numerator, denominator = int(signature[0]), int(signature[1])
    title = str(metadata.get("title", "PMT Performance"))
    track_configs = metadata.get("tracks", {})

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
    full_midi.tracks.append(
        _conductor_track(
            title=title,
            tempo_us_per_beat=tempo_us_per_beat,
            numerator=numerator,
            denominator=denominator,
        )
    )

    generated: dict[str, Path] = {}
    for track_index in sorted(grouped):
        config = track_configs[str(track_index)]
        name = str(config["name"])
        midi_track = _musical_track(
            grouped[track_index],
            name=name,
            channel=int(config["channel"]),
            bank=int(config.get("bank", 0)),
            tempo_us_per_beat=tempo_us_per_beat,
            ticks_per_beat=ticks_per_beat,
        )

        standalone = mido.MidiFile(type=1, ticks_per_beat=ticks_per_beat)
        standalone.tracks.append(
            _conductor_track(
                title=title,
                tempo_us_per_beat=tempo_us_per_beat,
                numerator=numerator,
                denominator=denominator,
            )
        )
        standalone.tracks.append(mido.MidiTrack(midi_track))
        path = tracks_dir / f"{name}.mid"
        standalone.save(path)
        generated[name] = path
        full_midi.tracks.append(midi_track)

    full_path = output_dir / "full_song.mid"
    full_midi.save(full_path)
    generated["full_song"] = full_path
    return generated
