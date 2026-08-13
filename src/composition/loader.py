from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.accompaniment.schema import TEXTURE_TYPES, normalize_continuity, resolve_texture
from src.complexity import normalize_complexity, resolve_section_complexities


def load_composition(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    validate_composition(data)
    return data


def validate_composition(data: dict[str, Any]) -> None:
    metadata = data.get("metadata", {})
    for field in ("title", "tempo", "time_signature", "key"):
        if field not in metadata:
            raise ValueError(f"composition metadata is missing '{field}'")
    if not isinstance(metadata["tempo"], (int, float)) or metadata["tempo"] <= 0:
        raise ValueError("metadata.tempo must be positive")
    beats_per_bar = int(str(metadata["time_signature"]).split("/")[0])

    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("composition.sections must not be empty")

    # Complexity fields are optional. Validation resolves defaults in memory
    # but deliberately does not modify old composition files.
    normalize_complexity(data.get("complexity"))
    contour = data.get("complexity_contour", "flat")
    if contour not in {"flat", "gradual_build", "verse_chorus", "wave", "sparse_to_climax", "custom"}:
        raise ValueError(f"unsupported complexity_contour: {contour!r}")
    names: set[str] = set()
    for section in sections:
        name = section.get("name")
        bars = section.get("bars")
        if not name or name in names:
            raise ValueError(f"section names must be non-empty and unique: {name!r}")
        if not isinstance(bars, int) or bars <= 0:
            raise ValueError(f"section '{name}' must have a positive integer bar count")
        names.add(name)
        if "complexity" in section:
            if not isinstance(section["complexity"], (str, dict)):
                raise ValueError(f"section '{name}' complexity must be a string or object")
        budget = section.get("complexity_budget")
        if budget is not None:
            if not isinstance(budget, dict) or not budget:
                raise ValueError(f"section '{name}' complexity_budget must be a non-empty object")
            for role, points in budget.items():
                if not isinstance(role, str) or not role:
                    raise ValueError(f"section '{name}' complexity_budget role names must be strings")
                if not isinstance(points, int) or not 0 <= points <= 5:
                    raise ValueError(f"section '{name}' complexity_budget.{role} must be 0..5")

    # Resolution depends on valid section names, so it happens after the
    # structural section checks above. Section override always wins.
    resolve_section_complexities(data)

    _validate_rhythm_motifs(data.get("rhythm_motifs", {}))

    tracks = data.get("tracks")
    if not isinstance(tracks, dict) or not tracks:
        raise ValueError("composition.tracks must be a non-empty object")
    for track_name, track in tracks.items():
        if "texture" in track and track["texture"] not in TEXTURE_TYPES:
            raise ValueError(f"track '{track_name}' texture must be one of {TEXTURE_TYPES}")
        if "continuity" in track:
            normalize_continuity(track.get("texture"), track["continuity"])
        track_sections = track.get("sections", {})
        unknown = set(track_sections) - names
        if unknown:
            raise ValueError(f"track '{track_name}' references unknown sections: {sorted(unknown)}")
        for section_name, clip in track_sections.items():
            loop_bars = clip.get("loop_bars")
            if not isinstance(loop_bars, int) or loop_bars <= 0:
                raise ValueError(f"{track_name}.{section_name}.loop_bars must be positive")
            for event in clip.get("events", []):
                _validate_event(track_name, section_name, event, loop_bars)
            texture = resolve_texture(track, clip)
            if "continuity" in clip:
                normalize_continuity(texture, track.get("continuity"), clip["continuity"])
            harmony_spans = clip.get("harmony_spans", [])
            if harmony_spans:
                if texture is None:
                    raise ValueError(f"{track_name}.{section_name}.harmony_spans require texture")
                _validate_harmony_spans(track_name, section_name, harmony_spans, loop_bars, beats_per_bar)
            elif "texture_pattern" in clip and not clip.get("events"):
                raise ValueError(f"{track_name}.{section_name}.texture_pattern requires harmony_spans or explicit events")
            motif = clip.get("rhythm_motif")
            if motif is not None:
                if motif not in data.get("rhythm_motifs", {}):
                    raise ValueError(f"{track_name}.{section_name} references unknown rhythm_motif {motif!r}")
                variation = clip.get("rhythm_variation", "A")
                if variation not in {"A", "A'", "B", "B'", "C"}:
                    raise ValueError(f"unsupported rhythm_variation in {track_name}.{section_name}: {variation!r}")


def _validate_harmony_spans(track: str, section: str, spans: Any, loop_bars: int, beats_per_bar: int) -> None:
    if not isinstance(spans, list) or not spans:
        raise ValueError(f"{track}.{section}.harmony_spans must be a non-empty list")
    previous = -1.0
    for span in spans:
        if not isinstance(span, dict):
            raise ValueError(f"{track}.{section}.harmony_spans entries must be objects")
        at = span.get("at")
        if not isinstance(at, str) or ":" not in at:
            raise ValueError(f"{track}.{section}.harmony span needs at like '1:1'")
        bar_text, beat_text = at.split(":", 1)
        bar, beat = int(bar_text), float(beat_text)
        position = (bar - 1) * beats_per_bar + beat - 1
        if not 1 <= bar <= loop_bars or beat < 1 or position < previous:
            raise ValueError(f"{track}.{section}.harmony_spans must be ordered and inside loop")
        if not isinstance(span.get("duration"), (int, float)) or span["duration"] <= 0:
            raise ValueError(f"{track}.{section}.harmony span duration must be positive")
        if position + float(span["duration"]) > loop_bars * beats_per_bar + 1e-6:
            raise ValueError(f"{track}.{section}.harmony span extends beyond loop")
        if not isinstance(span.get("pitches"), list) or len(span["pitches"]) < 2:
            raise ValueError(f"{track}.{section}.harmony span requires at least two pitches")
        for pitch in span["pitches"]:
            from src.midi.pitches import note_number
            note_number(pitch)
        previous = position


def _validate_rhythm_motifs(motifs: Any) -> None:
    if not isinstance(motifs, dict):
        raise ValueError("rhythm_motifs must be an object")
    for name, pattern in motifs.items():
        if not isinstance(pattern, list) or not pattern:
            raise ValueError(f"rhythm motif {name!r} must contain events")
        previous = -1.0
        for item in pattern:
            if not isinstance(item, dict):
                raise ValueError(f"rhythm motif {name!r} events must be objects")
            offset = item.get("offset")
            duration = item.get("duration")
            if not isinstance(offset, (int, float)) or offset < 0 or offset < previous:
                raise ValueError(f"rhythm motif {name!r} offsets must be non-negative and ordered")
            if not isinstance(duration, (int, float)) or duration <= 0:
                raise ValueError(f"rhythm motif {name!r} durations must be positive")
            previous = float(offset)


def _validate_event(track: str, section: str, event: dict[str, Any], loop_bars: int) -> None:
    event_type = event.get("type", "note")
    if event_type not in {"note", "chord", "drum", "rest"}:
        raise ValueError(f"unsupported event type in {track}.{section}: {event_type}")
    at = event.get("at")
    if not isinstance(at, str) or ":" not in at:
        raise ValueError(f"event in {track}.{section} needs an 'at' value like '1:1.5'")
    bar_text, beat_text = at.split(":", 1)
    bar, beat = int(bar_text), float(beat_text)
    if not 1 <= bar <= loop_bars or beat < 1:
        raise ValueError(f"event position is outside loop in {track}.{section}: {at}")
    if event_type != "rest":
        duration = event.get("duration")
        velocity = event.get("velocity")
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError(f"event duration must be positive in {track}.{section}")
        if not isinstance(velocity, int) or not 1 <= velocity <= 127:
            raise ValueError(f"event velocity must be 1..127 in {track}.{section}")
    if event_type == "note" and "pitch" not in event:
        raise ValueError(f"note event needs pitch in {track}.{section}")
    if event_type == "chord" and not event.get("pitches"):
        raise ValueError(f"chord event needs pitches in {track}.{section}")
    if event_type == "drum" and "note" not in event:
        raise ValueError(f"drum event needs note in {track}.{section}")
