from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median
from typing import Any, Sequence
import json
import math

import mido


ACOUSTIC_GUITAR_PROGRAMS = {24, 25}
GUITAR_PROGRAMS = set(range(24, 32))


@dataclass(frozen=True)
class NoteEvent:
    track: int
    channel: int
    program: int
    pitch: int
    velocity: int
    onset_tick: int
    end_tick: int


@dataclass(frozen=True)
class StrokeEvent:
    onset_tick: int
    pitches: tuple[int, ...]
    velocities: tuple[int, ...]
    end_ticks: tuple[int, ...]
    direction: str
    direction_confidence: float
    stroke_type: str
    spread_beats: float
    bar: int
    slot: int
    grid_deviation_beats: float


def _round_half_up(value: float) -> int:
    return int(math.floor(value + 0.5))


def _median(values: Sequence[float], default: float = 0.0) -> float:
    return float(median(values)) if values else default


def _pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    dx = [value - mean_x for value in xs]
    dy = [value - mean_y for value in ys]
    denominator = math.sqrt(
        sum(value * value for value in dx)
        * sum(value * value for value in dy)
    )
    if denominator <= 1e-12:
        return 0.0
    return sum(a * b for a, b in zip(dx, dy)) / denominator


def _first_time_signature(midi: mido.MidiFile) -> tuple[int, int]:
    for track in midi.tracks:
        for message in track:
            if message.type == "time_signature":
                return int(message.numerator), int(message.denominator)
    return 4, 4


def _track_channel_notes(
    midi: mido.MidiFile,
) -> dict[tuple[int, int], list[NoteEvent]]:
    result: dict[tuple[int, int], list[NoteEvent]] = defaultdict(list)
    for track_index, track in enumerate(midi.tracks):
        absolute_tick = 0
        programs: dict[int, int] = defaultdict(int)
        pending: dict[
            tuple[int, int], deque[tuple[int, int, int]]
        ] = defaultdict(deque)
        for message in track:
            absolute_tick += int(message.time)
            if not hasattr(message, "channel"):
                continue
            channel = int(message.channel)
            if message.type == "program_change":
                programs[channel] = int(message.program)
                continue
            if message.type == "note_on" and int(message.velocity) > 0:
                pending[(channel, int(message.note))].append(
                    (
                        absolute_tick,
                        int(message.velocity),
                        int(programs[channel]),
                    )
                )
                continue
            if message.type == "note_off" or (
                message.type == "note_on" and int(message.velocity) == 0
            ):
                queue = pending[(channel, int(message.note))]
                if not queue:
                    continue
                onset_tick, velocity, program = queue.popleft()
                result[(track_index, channel)].append(
                    NoteEvent(
                        track=track_index,
                        channel=channel,
                        program=128 if channel == 9 else program,
                        pitch=int(message.note),
                        velocity=velocity,
                        onset_tick=onset_tick,
                        end_tick=max(onset_tick + 1, absolute_tick),
                    )
                )
    for events in result.values():
        events.sort(key=lambda event: (event.onset_tick, event.pitch))
    return dict(result)


def list_candidates_from_grouped(
    grouped: dict[tuple[int, int], list[NoteEvent]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (track, channel), notes in grouped.items():
        programs = sorted({note.program for note in notes})
        clustered_onsets = Counter(round(note.onset_tick / 24) for note in notes)
        chord_note_ratio = (
            sum(count for count in clustered_onsets.values() if count >= 3)
            / len(notes)
            if notes
            else 0.0
        )
        if any(program in ACOUSTIC_GUITAR_PROGRAMS for program in programs):
            guitar_bonus = 3.0
        elif any(program in GUITAR_PROGRAMS for program in programs):
            guitar_bonus = 1.5
        else:
            guitar_bonus = 0.0
        score = guitar_bonus + math.log10(len(notes) + 1) + chord_note_ratio
        rows.append(
            {
                "track": track,
                "channel": channel,
                "programs": programs,
                "note_count": len(notes),
                "chord_note_ratio": round(chord_note_ratio, 4),
                "selection_score": round(score, 4),
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            -row["selection_score"],
            row["track"],
            row["channel"],
        ),
    )


def list_candidates(midi_path: Path) -> list[dict[str, Any]]:
    midi = mido.MidiFile(midi_path)
    return list_candidates_from_grouped(_track_channel_notes(midi))


def _select_notes(
    midi: mido.MidiFile,
    track_index: int | None,
    channel: int | None,
) -> tuple[list[NoteEvent], dict[str, Any]]:
    grouped = _track_channel_notes(midi)
    if track_index is not None:
        matches = [
            (key, notes)
            for key, notes in grouped.items()
            if key[0] == track_index and (channel is None or key[1] == channel)
        ]
        if not matches:
            raise ValueError(
                f"no note data found for track={track_index}, channel={channel}"
            )
        if len(matches) > 1:
            raise ValueError(
                f"track {track_index} contains multiple active channels; "
                "pass --channel"
            )
        (selected_track, selected_channel), notes = matches[0]
    else:
        candidates = list_candidates_from_grouped(grouped)
        if not candidates:
            raise ValueError("MIDI contains no paired note events")
        selected_track = int(candidates[0]["track"])
        selected_channel = int(candidates[0]["channel"])
        notes = grouped[(selected_track, selected_channel)]
    return notes, {
        "track": selected_track,
        "channel": selected_channel,
        "programs": sorted({note.program for note in notes}),
        "note_count": len(notes),
    }


def _stroke_direction(
    notes: Sequence[NoteEvent], ticks_per_beat: int
) -> tuple[str, float]:
    if len(notes) < 3:
        return "unknown", 0.0
    onset_values = [note.onset_tick / ticks_per_beat for note in notes]
    pitch_values = [float(note.pitch) for note in notes]
    spread = max(onset_values) - min(onset_values)
    if spread < 0.008:
        return "unknown", 0.0
    correlation = _pearson(onset_values, pitch_values)
    if abs(correlation) < 0.30:
        return "unknown", round(abs(correlation), 4)
    spread_evidence = min(1.0, spread / 0.08)
    confidence = min(
        1.0,
        abs(correlation) * (0.55 + 0.45 * spread_evidence),
    )
    return ("down" if correlation > 0 else "up"), round(confidence, 4)


def _stroke_type(
    notes: Sequence[NoteEvent], global_pitch_median: float
) -> str:
    pitches = [note.pitch for note in notes]
    count = len(pitches)
    span = max(pitches) - min(pitches) if count > 1 else 0
    center = sum(pitches) / count
    if count >= 5 and span >= 12:
        return "full"
    if count == 1:
        return "single_string"
    if count == 2:
        return "double_stop"
    if count in {3, 4}:
        if center >= global_pitch_median + 2:
            return "high_partial"
        if center <= global_pitch_median - 2:
            return "low_partial"
        return "middle_partial"
    return "compact_chord"


def cluster_strokes(
    notes: Sequence[NoteEvent],
    *,
    ticks_per_beat: int,
    beats_per_bar: float,
    slots_per_beat: int = 2,
    cluster_window_beats: float = 0.12,
) -> list[StrokeEvent]:
    if not notes:
        return []
    sorted_notes = sorted(
        notes,
        key=lambda note: (note.onset_tick, note.pitch),
    )
    window_ticks = max(1, round(cluster_window_beats * ticks_per_beat))
    clusters: list[list[NoteEvent]] = []
    current: list[NoteEvent] = []
    cluster_start = 0
    for note in sorted_notes:
        if not current:
            current = [note]
            cluster_start = note.onset_tick
        elif note.onset_tick - cluster_start <= window_ticks:
            current.append(note)
        else:
            clusters.append(current)
            current = [note]
            cluster_start = note.onset_tick
    if current:
        clusters.append(current)

    global_pitch_median = _median(
        [note.pitch for note in sorted_notes]
    )
    slots_per_bar = max(1, round(beats_per_bar * slots_per_beat))
    strokes: list[StrokeEvent] = []
    for cluster in clusters:
        onset_tick = min(note.onset_tick for note in cluster)
        direction, confidence = _stroke_direction(cluster, ticks_per_beat)
        onset_beat = onset_tick / ticks_per_beat
        global_slot = _round_half_up(onset_beat * slots_per_beat)
        slot_beat = global_slot / slots_per_beat
        bar = global_slot // slots_per_bar
        slot = global_slot % slots_per_bar
        spread_beats = (
            max(note.onset_tick for note in cluster)
            - min(note.onset_tick for note in cluster)
        ) / ticks_per_beat
        ordered = sorted(
            cluster,
            key=lambda note: (note.onset_tick, note.pitch),
        )
        strokes.append(
            StrokeEvent(
                onset_tick=onset_tick,
                pitches=tuple(note.pitch for note in ordered),
                velocities=tuple(note.velocity for note in ordered),
                end_ticks=tuple(note.end_tick for note in ordered),
                direction=direction,
                direction_confidence=confidence,
                stroke_type=_stroke_type(cluster, global_pitch_median),
                spread_beats=round(spread_beats, 6),
                bar=bar,
                slot=slot,
                grid_deviation_beats=round(
                    onset_beat - slot_beat,
                    6,
                ),
            )
        )
    return strokes


def _dominant(counter: Counter[str], default: str) -> str:
    if not counter:
        return default
    return sorted(
        counter.items(),
        key=lambda item: (-item[1], item[0]),
    )[0][0]


def _accent_class(values: Sequence[float], value: float) -> str:
    if not values:
        return "neutral"
    ordered = sorted(values)
    low = ordered[max(0, math.floor((len(ordered) - 1) * 0.33))]
    high = ordered[
        min(len(ordered) - 1, math.ceil((len(ordered) - 1) * 0.67))
    ]
    if value <= low and value < high:
        return "light"
    if value >= high and value > low:
        return "accent"
    return "neutral"


def summarize_strokes(
    strokes: Sequence[StrokeEvent],
    *,
    ticks_per_beat: int,
    beats_per_bar: float,
    slots_per_beat: int = 2,
) -> dict[str, Any]:
    slots_per_bar = max(1, round(beats_per_bar * slots_per_beat))
    if not strokes:
        raise ValueError("no stroke candidates were extracted")
    bar_count = max(stroke.bar for stroke in strokes) + 1

    known_directions = [
        stroke
        for stroke in strokes
        if stroke.direction in {"down", "up"}
    ]
    phase_scores: dict[str, float] = {}
    for phase in ("down", "up"):
        score = 0.0
        for stroke in known_directions:
            expected = (
                phase
                if stroke.slot % 2 == 0
                else ("up" if phase == "down" else "down")
            )
            if stroke.direction == expected:
                score += max(0.1, stroke.direction_confidence)
        phase_scores[phase] = score
    phase = max(
        phase_scores,
        key=lambda key: (phase_scores[key], key == "down"),
    )
    direction_evidence = sum(phase_scores.values())
    alternate_confidence = (
        phase_scores[phase] / direction_evidence
        if direction_evidence > 0
        else 0.0
    )

    per_bar_velocity: dict[int, list[float]] = defaultdict(list)
    stroke_velocity: dict[int, float] = {}
    for index, stroke in enumerate(strokes):
        value = sum(stroke.velocities) / len(stroke.velocities)
        stroke_velocity[index] = value
        per_bar_velocity[stroke.bar].append(value)

    slot_rows: list[dict[str, Any]] = []
    attack_mask: list[int] = []
    fingerprint_types: list[str] = []
    fingerprint_accents: list[str] = []
    for slot in range(slots_per_bar):
        rows = [
            (index, stroke)
            for index, stroke in enumerate(strokes)
            if stroke.slot == slot
        ]
        observed_bars = len({stroke.bar for _, stroke in rows})
        probability = observed_bars / bar_count
        attack_mask.append(1 if probability >= 0.5 else 0)
        types = Counter(stroke.stroke_type for _, stroke in rows)
        dominant_type = _dominant(types, "air_candidate")
        fingerprint_types.append(
            dominant_type if probability >= 0.5 else "air_candidate"
        )

        relative_values: list[float] = []
        accent_classes: list[str] = []
        spread_ratios: list[float] = []
        directions = Counter[str]()
        confidence_values: list[float] = []
        for index, stroke in rows:
            bar_values = per_bar_velocity[stroke.bar]
            bar_median = _median(bar_values, 1.0)
            relative_values.append(
                stroke_velocity[index] / max(1.0, bar_median)
            )
            accent_classes.append(
                _accent_class(bar_values, stroke_velocity[index])
            )
            spread_ratios.append(
                stroke.spread_beats / (1 / slots_per_beat)
            )
            if stroke.direction in {"down", "up"}:
                directions[stroke.direction] += 1
                confidence_values.append(stroke.direction_confidence)

        accent = _dominant(Counter(accent_classes), "neutral")
        fingerprint_accents.append(
            accent if probability >= 0.5 else "air"
        )
        expected_direction = (
            phase
            if slot % 2 == 0
            else ("up" if phase == "down" else "down")
        )
        slot_rows.append(
            {
                "slot": slot,
                "expected_direction": expected_direction,
                "attack_probability": round(probability, 4),
                "dominant_stroke_type": dominant_type,
                "stroke_type_distribution": {
                    key: round(value / len(rows), 4)
                    for key, value in sorted(types.items())
                }
                if rows
                else {},
                "relative_velocity_median": round(
                    _median(relative_values, 1.0),
                    4,
                ),
                "accent_class": accent,
                "spread_ratio_median": round(
                    _median(spread_ratios),
                    4,
                ),
                "observed_direction": _dominant(
                    directions,
                    "unknown",
                ),
                "direction_confidence_median": round(
                    _median(confidence_values),
                    4,
                ),
            }
        )

    ordered_strokes = sorted(
        strokes,
        key=lambda stroke: stroke.onset_tick,
    )
    ring_flags: list[float] = []
    for current, following in zip(
        ordered_strokes,
        ordered_strokes[1:],
    ):
        ring_flags.extend(
            1.0 if end_tick > following.onset_tick else 0.0
            for end_tick in current.end_ticks
        )

    grid_alignment = sum(
        abs(stroke.grid_deviation_beats) <= 0.125
        for stroke in strokes
    ) / len(strokes)

    return {
        "schema": "music-agent-acoustic-strumming-model",
        "schema_version": 1,
        "technique": "continuous_eighth_alternating_strumming",
        "subdivision": "eighth",
        "slots_per_bar": slots_per_bar,
        "motion": {
            "type": "alternate",
            "slot_zero_direction": phase,
            "continuous_motion": True,
            "cross_bar_continuity": True,
            "alternate_direction_confidence": round(
                alternate_confidence,
                4,
            ),
        },
        "slot_profiles": slot_rows,
        "attack_mask": attack_mask,
        "sustain_observations": {
            "ring_through_next_attack_ratio": round(
                sum(ring_flags) / len(ring_flags),
                4,
            )
            if ring_flags
            else 0.0,
            "interpretation": (
                "observed note overlap only; not proof of literal string motion"
            ),
        },
        "evidence": {
            "bar_count": bar_count,
            "stroke_count": len(strokes),
            "known_direction_strokes": len(known_directions),
            "grid_alignment_ratio": round(grid_alignment, 4),
        },
        "invariance_fingerprint": {
            "subdivision": "eighth",
            "slot_zero_direction": phase,
            "attack_mask": attack_mask,
            "dominant_stroke_types": fingerprint_types,
            "accent_classes": fingerprint_accents,
        },
        "limitations": [
            (
                "Air strokes are inferred from missing grid attacks and are "
                "not directly present in MIDI."
            ),
            (
                "Down/up direction requires a measurable low-to-high or "
                "high-to-low onset spread."
            ),
            (
                "String identity, pick angle and fretting hand technique are "
                "not recoverable from ordinary MIDI alone."
            ),
        ],
    }


def analyze_midi(
    midi_path: Path,
    *,
    track_index: int | None = None,
    channel: int | None = None,
    cluster_window_beats: float = 0.12,
) -> dict[str, Any]:
    midi = mido.MidiFile(midi_path)
    numerator, denominator = _first_time_signature(midi)
    beats_per_bar = numerator * 4 / denominator
    notes, selection = _select_notes(midi, track_index, channel)
    strokes = cluster_strokes(
        notes,
        ticks_per_beat=int(midi.ticks_per_beat),
        beats_per_bar=beats_per_bar,
        cluster_window_beats=cluster_window_beats,
    )
    model = summarize_strokes(
        strokes,
        ticks_per_beat=int(midi.ticks_per_beat),
        beats_per_bar=beats_per_bar,
    )
    return {
        "source": {
            "filename": midi_path.name,
            "midi_type": int(midi.type),
            "ticks_per_beat": int(midi.ticks_per_beat),
            "time_signature": [numerator, denominator],
        },
        "selection": selection,
        "model": model,
        "strokes": [asdict(stroke) for stroke in strokes],
    }


def write_analysis(result: dict[str, Any], study_dir: Path) -> None:
    study_dir.mkdir(parents=True, exist_ok=True)
    (study_dir / "analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (study_dir / "model.json").write_text(
        json.dumps(
            result["model"],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    model = result["model"]
    lines = [
        "# Acoustic strumming study",
        "",
        "## Direct MIDI observations",
        "",
        (
            "- Selected track/channel: "
            f"{result['selection']['track']} / "
            f"{result['selection']['channel']}"
        ),
        f"- Paired notes: {result['selection']['note_count']}",
        f"- Stroke candidates: {model['evidence']['stroke_count']}",
        (
            "- Grid alignment ratio: "
            f"{model['evidence']['grid_alignment_ratio']}"
        ),
        (
            "- Direction evidence strokes: "
            f"{model['evidence']['known_direction_strokes']}"
        ),
        "",
        "## Generalized model",
        "",
        f"- Technique: `{model['technique']}`",
        (
            "- Slot-zero direction: "
            f"`{model['motion']['slot_zero_direction']}`"
        ),
        f"- Attack mask: `{model['attack_mask']}`",
        (
            "- Alternate-direction confidence: "
            f"{model['motion']['alternate_direction_confidence']}"
        ),
        "",
        "## Inference boundary",
        "",
        "- Missing grid positions are only air-stroke candidates.",
        (
            "- MIDI onset order supports a direction estimate but does not "
            "prove the physical gesture."
        ),
        (
            "- Absolute pitch, key, tempo, program and source song form are "
            "excluded from the model fingerprint."
        ),
        "",
    ]
    (study_dir / "observations.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def _select_voicing(
    pitches: Sequence[int], stroke_type: str
) -> list[int]:
    ordered = sorted(set(int(pitch) for pitch in pitches))
    if stroke_type == "full":
        return ordered
    if stroke_type == "low_partial":
        return ordered[: max(2, min(4, len(ordered)))]
    if stroke_type == "high_partial":
        return ordered[-max(2, min(4, len(ordered))) :]
    if stroke_type == "middle_partial":
        if len(ordered) <= 3:
            return ordered
        start = max(0, (len(ordered) - 3) // 2)
        return ordered[start : start + 3]
    if stroke_type == "double_stop":
        return ordered[-2:]
    if stroke_type == "single_string":
        return ordered[-1:]
    return ordered[: min(4, len(ordered))]


def generate_demo_midi(
    model: dict[str, Any],
    output_path: Path,
    *,
    progression: Sequence[Sequence[int]] | None = None,
    tempo_bpm: float = 104.0,
    program: int = 25,
    ticks_per_beat: int = 480,
) -> Path:
    progression = progression or (
        (45, 52, 57, 60, 64),
        (41, 48, 53, 57, 60),
        (48, 55, 60, 64, 67),
        (43, 50, 55, 59, 62),
    )
    slots_per_bar = int(model["slots_per_bar"])
    slot_duration_beats = 4.0 / slots_per_bar
    events: list[tuple[int, int, mido.Message]] = []
    active_by_pitch: dict[int, tuple[int, int]] = {}
    sequence = 0

    for bar_index, chord in enumerate(progression):
        for profile in model["slot_profiles"]:
            if float(profile["attack_probability"]) < 0.5:
                continue
            slot = int(profile["slot"])
            direction = str(profile["expected_direction"])
            stroke_type = str(profile["dominant_stroke_type"])
            selected = _select_voicing(chord, stroke_type)
            if direction == "up":
                selected = list(reversed(selected))
            start_beat = (
                bar_index * 4 + slot * slot_duration_beats
            )
            start_tick = round(start_beat * ticks_per_beat)
            spread_ratio = max(
                0.02,
                float(profile.get("spread_ratio_median", 0.08)),
            )
            spread_ticks = max(
                1,
                round(
                    spread_ratio
                    * slot_duration_beats
                    * ticks_per_beat
                ),
            )
            step_ticks = max(
                1,
                spread_ticks // max(1, len(selected) - 1),
            )
            accent = str(profile.get("accent_class", "neutral"))
            velocity = {
                "light": 58,
                "neutral": 70,
                "accent": 84,
            }.get(accent, 70)

            for order, pitch in enumerate(selected):
                note_on_tick = start_tick + order * step_ticks
                if pitch in active_by_pitch:
                    old_end_tick, old_sequence = active_by_pitch.pop(pitch)
                    if old_end_tick >= note_on_tick:
                        events.append(
                            (
                                max(0, note_on_tick - 1),
                                old_sequence,
                                mido.Message(
                                    "note_off",
                                    channel=0,
                                    note=pitch,
                                    velocity=0,
                                ),
                            )
                        )
                sequence += 1
                events.append(
                    (
                        note_on_tick,
                        sequence,
                        mido.Message(
                            "note_on",
                            channel=0,
                            note=pitch,
                            velocity=max(
                                1,
                                min(127, velocity - order),
                            ),
                        ),
                    )
                )
                desired_end = note_on_tick + round(
                    1.25 * ticks_per_beat
                )
                active_by_pitch[pitch] = (
                    desired_end,
                    sequence,
                )

        chord_end_tick = round(
            (bar_index + 1) * 4 * ticks_per_beat
        )
        if bar_index + 1 < len(progression):
            next_chord = set(progression[bar_index + 1])
        else:
            next_chord = set()
        for pitch, (end_tick, _) in list(
            active_by_pitch.items()
        ):
            if pitch not in next_chord:
                sequence += 1
                events.append(
                    (
                        min(end_tick, chord_end_tick),
                        sequence,
                        mido.Message(
                            "note_off",
                            channel=0,
                            note=pitch,
                            velocity=0,
                        ),
                    )
                )
                active_by_pitch.pop(pitch, None)

    final_tick = round(
        len(progression) * 4 * ticks_per_beat
    )
    for pitch, (end_tick, _) in active_by_pitch.items():
        sequence += 1
        events.append(
            (
                min(end_tick, final_tick),
                sequence,
                mido.Message(
                    "note_off",
                    channel=0,
                    note=pitch,
                    velocity=0,
                ),
            )
        )

    midi = mido.MidiFile(type=1, ticks_per_beat=ticks_per_beat)
    conductor = mido.MidiTrack()
    conductor.append(
        mido.MetaMessage(
            "set_tempo",
            tempo=mido.bpm2tempo(tempo_bpm),
            time=0,
        )
    )
    conductor.append(
        mido.MetaMessage(
            "time_signature",
            numerator=4,
            denominator=4,
            time=0,
        )
    )
    midi.tracks.append(conductor)

    track = mido.MidiTrack()
    track.append(
        mido.MetaMessage(
            "track_name",
            name="Synthetic acoustic strumming demo",
            time=0,
        )
    )
    track.append(
        mido.Message(
            "program_change",
            channel=0,
            program=program,
            time=0,
        )
    )
    events.sort(
        key=lambda item: (
            item[0],
            0 if item[2].type == "note_off" else 1,
            item[1],
        )
    )
    previous_tick = 0
    for absolute_tick, _, message in events:
        message.time = max(0, absolute_tick - previous_tick)
        track.append(message)
        previous_tick = absolute_tick
    midi.tracks.append(track)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    midi.save(output_path)
    return output_path
