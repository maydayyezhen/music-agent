from __future__ import annotations

from copy import deepcopy
from typing import Any

from src.accompaniment.schema import normalize_continuity, resolve_texture
from src.accompaniment.voicing import midi_to_note, plan_smooth_voicings
from src.midi.pitches import note_number


def _position(value: str, beats_per_bar: int) -> float:
    bar, beat = value.split(":", 1)
    return (int(bar) - 1) * beats_per_bar + float(beat) - 1.0


def _at(value: float, beats_per_bar: int) -> str:
    bar = int(value // beats_per_bar) + 1
    beat = value % beats_per_bar + 1
    beat_text = f"{beat:.3f}".rstrip("0").rstrip(".")
    return f"{bar}:{beat_text}"


def _note(pitch: int, start: float, duration: float, velocity: int, beats_per_bar: int) -> dict[str, Any]:
    return {"type": "note", "pitch": midi_to_note(pitch), "at": _at(start, beats_per_bar), "duration": round(max(0.05, duration), 3), "velocity": max(1, min(127, int(velocity)))}


def _chord(pitches: tuple[int, ...], start: float, duration: float, velocity: int, beats_per_bar: int) -> dict[str, Any]:
    return {"type": "chord", "pitches": [midi_to_note(pitch) for pitch in pitches], "at": _at(start, beats_per_bar), "duration": round(max(0.05, duration), 3), "velocity": max(1, min(127, int(velocity)))}


def _settings(pattern: dict[str, Any]) -> tuple[tuple[int, int], int, int]:
    register = pattern.get("register", [55, 76])
    if not isinstance(register, list) or len(register) != 2:
        raise ValueError("texture_pattern.register must be [low_midi, high_midi]")
    return (int(register[0]), int(register[1])), int(pattern.get("voices", 3)), int(pattern.get("velocity", 60))


def _span_data(harmony_spans: list[dict[str, Any]], beats_per_bar: int) -> list[tuple[float, float]]:
    return [(_position(span["at"], beats_per_bar), float(span["duration"])) for span in harmony_spans]


def _sustain(
    spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], continuity: dict[str, float],
    pattern: dict[str, Any], velocity: int, beats_per_bar: int,
) -> list[dict[str, Any]]:
    timing = _span_data(spans, beats_per_bar)
    strum_spread = float(pattern.get("strum_spread", 0.0))
    voices: list[list[dict[str, Any]]] = [[] for _ in range(len(voicings[0]))]
    for span_index, ((start, duration), voicing) in enumerate(zip(timing, voicings)):
        for voice_index, pitch in enumerate(voicing):
            lane = voices[voice_index]
            end = start + duration
            if lane and lane[-1]["pitch"] == pitch and abs(lane[-1]["end"] - start) <= 0.12:
                lane[-1]["end"] = end
            else:
                attack = start + voice_index * strum_spread
                lane.append({"pitch": pitch, "start": attack, "end": end + continuity["overlap"], "velocity": velocity - voice_index * 2 + span_index % 2})
    return [
        _note(item["pitch"], item["start"], item["end"] - item["start"], item["velocity"], beats_per_bar)
        for lane in voices for item in lane
    ]


def _pulse(
    spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], pattern: dict[str, Any],
    velocity: int, beats_per_bar: int,
) -> list[dict[str, Any]]:
    offsets = [float(value) for value in pattern.get("offsets", [0.0, 1.5, 3.0])]
    durations = [float(value) for value in pattern.get("durations", [0.65, 0.4, 0.75])]
    accents = [float(value) for value in pattern.get("accents", [1.0, 0.82, 0.92])]
    result: list[dict[str, Any]] = []
    for index, (span, voicing) in enumerate(zip(spans, voicings)):
        start, span_duration = _position(span["at"], beats_per_bar), float(span["duration"])
        for pulse_index, offset in enumerate(offsets):
            # Phrase-level breath: the last weak pulse disappears every fourth span.
            if index % 4 == 3 and pulse_index == len(offsets) - 1:
                continue
            if offset < span_duration:
                result.append(_chord(voicing, start + offset, min(durations[pulse_index % len(durations)], span_duration - offset), round(velocity * accents[pulse_index % len(accents)]), beats_per_bar))
    return result


def _broken(
    spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], pattern: dict[str, Any],
    continuity: dict[str, float], velocity: int, beats_per_bar: int,
) -> list[dict[str, Any]]:
    indices = [int(value) for value in pattern.get("indices", [0, 1, 2, 1, 0])]
    step = float(pattern.get("step", 0.75))
    cursor = int(pattern.get("start_cursor", 0))
    result: list[dict[str, Any]] = []
    for span_index, (span, voicing) in enumerate(zip(spans, voicings)):
        start, span_duration = _position(span["at"], beats_per_bar), float(span["duration"])
        local = 0.0
        while local < span_duration - 0.05:
            pitch = voicing[indices[cursor % len(indices)] % len(voicing)]
            duration = min(step * (0.96 + continuity["legato_ratio"] * 0.08), span_duration - local + continuity["overlap"])
            result.append(_note(pitch, start + local, duration, velocity + (4 if cursor % len(indices) == 0 else 0) - span_index % 2, beats_per_bar))
            cursor += 1
            local += step
    return result


def _arpeggio(
    spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], pattern: dict[str, Any],
    continuity: dict[str, float], velocity: int, beats_per_bar: int,
) -> list[dict[str, Any]]:
    step = float(pattern.get("step", 0.5))
    direction = 1
    cursor = 0
    previous_pitch: int | None = None
    result: list[dict[str, Any]] = []
    for span_index, (span, voicing) in enumerate(zip(spans, voicings)):
        start, span_duration = _position(span["at"], beats_per_bar), float(span["duration"])
        if previous_pitch is not None:
            # Preserve contour direction, but remap the running cursor to the
            # nearest legal tone instead of resetting to root or making a leap.
            cursor = min(range(len(voicing)), key=lambda index: abs(voicing[index] - previous_pitch))
        local = 0.0
        while local < span_duration - 0.05:
            cursor = max(0, min(len(voicing) - 1, cursor))
            pitch = voicing[cursor]
            result.append(_note(pitch, start + local, min(step + continuity["overlap"], span_duration - local + continuity["overlap"]), velocity + (cursor == len(voicing) - 1) * 3, beats_per_bar))
            previous_pitch = pitch
            if len(voicing) > 1:
                cursor += direction
                if cursor >= len(voicing):
                    cursor = len(voicing) - 2
                    direction = -1
                elif cursor < 0:
                    cursor = 1
                    direction = 1
            local += step
        # Cursor and direction deliberately persist across chord boundaries.
        if span_index % 4 == 3:
            direction *= -1
    return result


def _ostinato(
    spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], pattern: dict[str, Any],
    continuity: dict[str, float], velocity: int, beats_per_bar: int,
) -> list[dict[str, Any]]:
    indices = [int(value) for value in pattern.get("indices", [0, 1, 0, 2])]
    offsets = [float(value) for value in pattern.get("offsets", [0, 1, 2, 3.25])]
    durations = [float(value) for value in pattern.get("durations", [0.7, 0.45, 0.7, 0.5])]
    accents = [int(value) for value in pattern.get("accents", [5, 0, 3, -2])]
    result: list[dict[str, Any]] = []
    for span_index, (span, voicing) in enumerate(zip(spans, voicings)):
        start, span_duration = _position(span["at"], beats_per_bar), float(span["duration"])
        for index, offset in enumerate(offsets):
            if span_index % 4 == 3 and index == 2:  # small recognizable phrase variation
                continue
            if offset < span_duration:
                pitch_index = indices[index % len(indices)]
                if span_index % 8 == 7 and index == len(offsets) - 1:
                    pitch_index += 1
                result.append(_note(voicing[pitch_index % len(voicing)], start + offset, min(durations[index % len(durations)] + continuity["overlap"], span_duration - offset), velocity + accents[index % len(accents)], beats_per_bar))
    return result


def _counterline(
    spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], pattern: dict[str, Any],
    continuity: dict[str, float], velocity: int, beats_per_bar: int,
) -> list[dict[str, Any]]:
    offsets = [float(value) for value in pattern.get("offsets", [0.5, 2.0, 3.25])]
    durations = [float(value) for value in pattern.get("durations", [1.4, 0.9, 0.6])]
    phrase_shape = [0.25, 0.55, 0.85, 1.0, 0.75, 0.5, 0.3, 0.15]
    previous: int | None = None
    result: list[dict[str, Any]] = []
    for span_index, (span, voicing) in enumerate(zip(spans, voicings)):
        start, span_duration = _position(span["at"], beats_per_bar), float(span["duration"])
        if span_index % 8 == 7:  # release/breath
            offsets_here = offsets[:1]
        else:
            offsets_here = offsets
        target_index = round(phrase_shape[span_index % len(phrase_shape)] * (len(voicing) - 1))
        for note_index, offset in enumerate(offsets_here):
            if offset >= span_duration:
                continue
            candidates = list(voicing)
            contour_index = max(0, min(len(candidates) - 1, target_index + note_index - 1))
            target = candidates[contour_index]
            if previous is not None:
                target = min(candidates, key=lambda pitch: abs(pitch - previous) + abs(pitch - target) * 0.35)
            duration = min(durations[note_index % len(durations)] + continuity["overlap"], span_duration - offset)
            result.append(_note(target, start + offset, duration, velocity + (note_index == 0) * 3, beats_per_bar))
            previous = target
    return result


def _stab(spans: list[dict[str, Any]], voicings: list[tuple[int, ...]], pattern: dict[str, Any], velocity: int, beats_per_bar: int) -> list[dict[str, Any]]:
    offsets = [float(value) for value in pattern.get("offsets", [0.0, 2.75])]
    result: list[dict[str, Any]] = []
    for span_index, (span, voicing) in enumerate(zip(spans, voicings)):
        if span_index % 4 == 2:
            continue
        start, duration = _position(span["at"], beats_per_bar), float(span["duration"])
        for offset in offsets:
            if offset < duration:
                result.append(_chord(voicing, start + offset, min(0.28 if offset else 0.4, duration - offset), velocity + (5 if offset == 0 else -2), beats_per_bar))
    return result


def _pedal(spans: list[dict[str, Any]], pattern: dict[str, Any], continuity: dict[str, float], velocity: int, beats_per_bar: int) -> list[dict[str, Any]]:
    timing = _span_data(spans, beats_per_bar)
    start = min(value[0] for value in timing)
    end = max(value[0] + value[1] for value in timing)
    configured = pattern.get("pitch")
    if configured is not None:
        pitch = note_number(configured)
    else:
        shared = set(note_number(pitch) % 12 for pitch in spans[0]["pitches"])
        for span in spans[1:]:
            shared &= {note_number(pitch) % 12 for pitch in span["pitches"]}
        pitch_class = min(shared) if shared else note_number(spans[0]["pitches"][0]) % 12
        register = pattern.get("register", [43, 60])
        pitch = min((midi for midi in range(int(register[0]), int(register[1]) + 1) if midi % 12 == pitch_class), key=lambda midi: abs(midi - sum(register) / 2))
    return [_note(pitch, start, end - start + continuity["overlap"], velocity, beats_per_bar)]


def generate_texture_events(
    texture: str,
    harmony_spans: list[dict[str, Any]],
    continuity: dict[str, Any] | None = None,
    pattern: dict[str, Any] | None = None,
    beats_per_bar: int = 4,
) -> list[dict[str, Any]]:
    if not harmony_spans:
        return []
    pattern = pattern or {}
    normalized = normalize_continuity(texture, continuity)
    register, voices, velocity = _settings(pattern)
    voicings = plan_smooth_voicings(harmony_spans, register, voices, normalized["common_tone_retention"], normalized["voice_leading_strength"])
    if texture == "sustain":
        result = _sustain(harmony_spans, voicings, normalized, pattern, velocity, beats_per_bar)
    elif texture == "pulse":
        result = _pulse(harmony_spans, voicings, pattern, velocity, beats_per_bar)
    elif texture == "broken_chord":
        result = _broken(harmony_spans, voicings, pattern, normalized, velocity, beats_per_bar)
    elif texture == "arpeggio":
        result = _arpeggio(harmony_spans, voicings, pattern, normalized, velocity, beats_per_bar)
    elif texture == "ostinato":
        result = _ostinato(harmony_spans, voicings, pattern, normalized, velocity, beats_per_bar)
    elif texture == "counterline":
        result = _counterline(harmony_spans, voicings, pattern, normalized, velocity, beats_per_bar)
    elif texture == "stab":
        result = _stab(harmony_spans, voicings, pattern, velocity, beats_per_bar)
    elif texture == "pedal":
        result = _pedal(harmony_spans, pattern, normalized, velocity, beats_per_bar)
    else:
        raise ValueError(f"unsupported texture: {texture!r}")
    return _trim_same_pitch_overlaps(result, beats_per_bar)


def _trim_same_pitch_overlaps(events: list[dict[str, Any]], beats_per_bar: int) -> list[dict[str, Any]]:
    """Legato may overlap different pitches, but never duplicate one MIDI key."""
    previous_by_pitch: dict[str, dict[str, Any]] = {}
    for event in sorted(events, key=lambda item: _position(item["at"], beats_per_bar)):
        if event.get("type", "note") != "note":
            continue
        pitch = str(event["pitch"])
        start = _position(event["at"], beats_per_bar)
        previous = previous_by_pitch.get(pitch)
        if previous is not None:
            previous_start = _position(previous["at"], beats_per_bar)
            if previous_start + float(previous["duration"]) > start:
                previous["duration"] = round(max(0.05, start - previous_start), 3)
        previous_by_pitch[pitch] = event
    return events


def generate_bass_line(
    harmony_spans: list[dict[str, Any]],
    continuity: dict[str, Any] | None = None,
    pattern: dict[str, Any] | None = None,
    beats_per_bar: int = 4,
) -> list[dict[str, Any]]:
    """Bass-specific line: held root, fifth, approach, anticipation, and release."""
    pattern = deepcopy(pattern or {})
    pattern.setdefault("register", [31, 48])
    pattern.setdefault("voices", 3)
    pattern.setdefault("velocity", 68)
    voicings = plan_smooth_voicings(harmony_spans, tuple(pattern["register"]), 3, 0.5, 0.75)
    result: list[dict[str, Any]] = []
    overlap = normalize_continuity("counterline", continuity)["overlap"]
    for index, (span, voicing) in enumerate(zip(harmony_spans, voicings)):
        start, duration = _position(span["at"], beats_per_bar), float(span["duration"])
        root_pc = note_number(span["pitches"][0]) % 12
        root = min((pitch for pitch in range(pattern["register"][0], pattern["register"][1] + 1) if pitch % 12 == root_pc), key=lambda pitch: abs(pitch - voicing[0]))
        if index % 4 == 0:
            result.append(_note(root, start, min(2.75, duration), pattern["velocity"] + 4, beats_per_bar))
            result.append(_note(voicing[-1], start + 2.75, min(1.25 + overlap, duration - 2.75 + overlap), pattern["velocity"] - 3, beats_per_bar))
        elif index % 4 == 1:
            result.append(_note(root, start, min(2.0, duration), pattern["velocity"] + 1, beats_per_bar))
            result.append(_note(voicing[1], start + 2.0, min(1.5 + overlap, duration - 2.0), pattern["velocity"] - 2, beats_per_bar))
            if index + 1 < len(harmony_spans):
                next_root_pc = note_number(harmony_spans[index + 1]["pitches"][0]) % 12
                approaches = [pitch for pitch in range(pattern["register"][0], pattern["register"][1] + 1) if (pitch + 1) % 12 == next_root_pc or (pitch - 1) % 12 == next_root_pc]
                approach = min(approaches, key=lambda pitch: abs(pitch - voicing[1]))
                result.append(_note(approach, start + 3.5, 0.5 + overlap, pattern["velocity"] - 6, beats_per_bar))
        elif index % 4 == 2:
            result.append(_note(root, start, min(3.25, duration), pattern["velocity"] + 2, beats_per_bar))
            result.append(_note(voicing[1], start + 3.25, min(0.75 + overlap, duration - 3.25 + overlap), pattern["velocity"] - 4, beats_per_bar))
        else:
            result.append(_note(root, start, min(1.75, duration), pattern["velocity"] + 3, beats_per_bar))
            result.append(_note(voicing[-1], start + 1.75, min(1.25 + overlap, duration - 1.75), pattern["velocity"] - 2, beats_per_bar))
            result.append(_note(root + 12 if root + 12 <= pattern["register"][1] else root, start + 3.0, min(1.0 + overlap, duration - 3.0 + overlap), pattern["velocity"], beats_per_bar))
    return _trim_same_pitch_overlaps(result, beats_per_bar)


def materialize_clip(clip: dict[str, Any], track: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    """Return explicit events plus optional texture-generated accompaniment."""
    if clip.get("instrument_phrase"):
        from src.instruments import compile_instrument_phrase
        from src.performance import apply_profile, load_profile
        events = compile_instrument_phrase(clip["instrument_phrase"], beats_per_bar)
        profile_name = str(clip.get("sound_library_profile", track.get("sound_library_profile", "general_midi")))
        compiled, report = apply_profile(events, load_profile(profile_name))
        clip["_profile_report"] = report
        return compiled
    events = [deepcopy(event) for event in clip.get("events", [])]
    spans = clip.get("harmony_spans", [])
    if not spans:
        return events
    texture = resolve_texture(track, clip)
    if texture is None:
        raise ValueError("harmony_spans require a track or clip texture")
    continuity = normalize_continuity(texture, track.get("continuity"), clip.get("continuity"))
    pattern = deepcopy(track.get("texture_pattern", {}))
    pattern.update(clip.get("texture_pattern", {}))
    if pattern.get("bass_line"):
        generated = generate_bass_line(spans, continuity, pattern, beats_per_bar)
    else:
        generated = generate_texture_events(texture, spans, continuity, pattern, beats_per_bar)
    for event in generated:
        event["_generated_texture"] = texture
    return _merge_explicit_and_generated(events, generated, beats_per_bar, int(clip["loop_bars"]) * beats_per_bar)


def _flatten_tonal_events(events: list[dict[str, Any]], generated: bool) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for event in events:
        if event.get("type", "note") == "chord":
            for pitch in event["pitches"]:
                note = {key: deepcopy(value) for key, value in event.items() if key != "pitches"}
                note["type"] = "note"
                note["pitch"] = pitch
                note["_generated"] = generated
                result.append(note)
        else:
            item = deepcopy(event)
            item["_generated"] = generated
            result.append(item)
    return result


def _merge_explicit_and_generated(
    explicit: list[dict[str, Any]], generated: list[dict[str, Any]], beats_per_bar: int, loop_beats: float,
) -> list[dict[str, Any]]:
    """Merge texture material with authored notes, always preserving authored events.

    Same-pitch overlaps are trimmed or omitted only on generated accompaniment.
    Different pitches may overlap for legato and sustained textures.
    """
    merged = _flatten_tonal_events(explicit, False) + _flatten_tonal_events(generated, True)
    tonal = [event for event in merged if event.get("type", "note") == "note"]
    non_tonal = [event for event in merged if event.get("type", "note") != "note"]
    accepted: list[dict[str, Any]] = []
    for pitch in sorted({str(event["pitch"]) for event in tonal}):
        lane = sorted(
            (event for event in tonal if str(event["pitch"]) == pitch),
            key=lambda event: (_position(event["at"], beats_per_bar), bool(event.get("_generated"))),
        )
        explicit_lane = [event for event in lane if not event.get("_generated")]
        generated_lane = [event for event in lane if event.get("_generated")]
        # Generated notes never cross the local loop edge: otherwise the next
        # loop's first note would duplicate the same MIDI key.
        for event in generated_lane:
            start = _position(event["at"], beats_per_bar)
            event["duration"] = round(min(float(event["duration"]), max(0.05, loop_beats - start)), 3)
        kept_generated: list[dict[str, Any]] = []
        for event in generated_lane:
            start = _position(event["at"], beats_per_bar)
            end = start + float(event["duration"])
            conflicts = [
                authored for authored in explicit_lane
                if _position(authored["at"], beats_per_bar) < end
                and _position(authored["at"], beats_per_bar) + float(authored["duration"]) > start
            ]
            if conflicts:
                authored_start = min(_position(item["at"], beats_per_bar) for item in conflicts)
                if start < authored_start and authored_start - start >= 0.05:
                    event["duration"] = round(authored_start - start, 3)
                    kept_generated.append(event)
                continue
            kept_generated.append(event)
        kept_generated.sort(key=lambda event: _position(event["at"], beats_per_bar))
        for first, second in zip(kept_generated, kept_generated[1:]):
            first_start = _position(first["at"], beats_per_bar)
            second_start = _position(second["at"], beats_per_bar)
            if first_start + float(first["duration"]) > second_start:
                first["duration"] = round(max(0.05, second_start - first_start), 3)
        accepted.extend(explicit_lane)
        accepted.extend(kept_generated)
    for event in accepted:
        event.pop("_generated", None)
    for event in non_tonal:
        event.pop("_generated", None)
    return sorted(accepted + non_tonal, key=lambda event: _position(event["at"], beats_per_bar))
