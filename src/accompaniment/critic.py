from __future__ import annotations

import math
from collections import Counter
from typing import Any

import numpy as np

from src.accompaniment.generator import materialize_clip
from src.accompaniment.schema import TEXTURE_FAMILIES, normalize_continuity, resolve_texture
from src.accompaniment.voicing import plan_smooth_voicings
from src.midi.pitches import note_number


def _position(value: str, beats_per_bar: int) -> float:
    bar, beat = value.split(":", 1)
    return (int(bar) - 1) * beats_per_bar + float(beat) - 1.0


def _entropy(values: list[float]) -> float:
    if not values:
        return 0.0
    counts = Counter(round(value, 3) for value in values)
    return float(-sum((count / len(values)) * math.log2(count / len(values)) for count in counts.values()))


def _expanded_events(clip: dict[str, Any], track: dict[str, Any], bars: int, beats_per_bar: int) -> list[dict[str, Any]]:
    materialized = materialize_clip(clip, track, beats_per_bar)
    loop_bars = int(clip["loop_bars"])
    result: list[dict[str, Any]] = []
    for loop_start in range(0, bars, loop_bars):
        shift = loop_start * beats_per_bar
        for event in materialized:
            if event.get("type", "note") in {"rest", "control_change"}:
                continue
            start = shift + _position(event["at"], beats_per_bar)
            if start >= bars * beats_per_bar:
                continue
            pitches = event.get("pitches", [event.get("pitch", event.get("note", 0))])
            result.append({
                "start": start,
                "duration": float(event["duration"]),
                "pitches": pitches,
                "multiplicity": len(pitches),
                "type": event.get("type", "note"),
                "generated_texture": event.get("_generated_texture"),
            })
    return sorted(result, key=lambda item: item["start"])


def _onset_gaps(events: list[dict[str, Any]]) -> list[float]:
    groups: dict[float, float] = {}
    for event in events:
        start = round(float(event["start"]), 4)
        groups[start] = max(groups.get(start, start), start + float(event["duration"]))
    ordered = sorted(groups.items())
    return [ordered[index + 1][0] - end for index, (_, end) in enumerate(ordered[:-1])]


def _explicit_voicings(events: list[dict[str, Any]]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for event in events:
        if event["type"] != "chord" or len(event["pitches"]) < 2:
            continue
        voicing = tuple(sorted(note_number(pitch) for pitch in event["pitches"]))
        if not result or voicing != result[-1]:
            result.append(voicing)
    return result


def _voicing_metrics(voicings: list[tuple[int, ...]]) -> tuple[float, float]:
    distances: list[float] = []
    retentions: list[float] = []
    for first, second in zip(voicings, voicings[1:]):
        count = min(len(first), len(second))
        distances.append(sum(abs(first[index] - second[index]) for index in range(count)) / max(1, count))
        first_pc, second_pc = {value % 12 for value in first}, {value % 12 for value in second}
        shared = first_pc & second_pc
        retained_pitch_classes = {value % 12 for value in set(first) & set(second)}
        retentions.append(1.0 if not shared else len(retained_pitch_classes & shared) / len(shared))
    return (float(np.mean(distances)) if distances else 0.0, float(np.mean(retentions)) if retentions else 0.0)


def _infer_family(texture: str | None, events: list[dict[str, Any]], is_percussion: bool) -> str:
    if is_percussion:
        return "point"
    if texture:
        return TEXTURE_FAMILIES[texture]
    if not events:
        return "silent"
    durations = [float(event["duration"]) for event in events for _ in range(event["multiplicity"])]
    sustain_ratio = sum(duration >= 1.75 for duration in durations) / len(durations)
    average_duration = float(np.mean(durations))
    gaps = _onset_gaps(events)
    legato_ratio = sum(abs(gap) <= 0.12 or gap < 0 for gap in gaps) / len(gaps) if gaps else 0.0
    if sustain_ratio >= 0.45:
        return "plane"
    if legato_ratio >= 0.45 or (all(event["type"] == "note" for event in events) and average_duration >= 0.90):
        return "line"
    return "point"


def analyze_continuity(composition: dict[str, Any]) -> dict[str, Any]:
    beats_per_bar = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    track_metrics: dict[str, dict[str, dict[str, Any]]] = {}
    section_metrics: dict[str, dict[str, Any]] = {}
    warnings: list[dict[str, str]] = []

    for section in composition["sections"]:
        section_name, bars = str(section["name"]), int(section["bars"])
        distribution = {"point": 0, "line": 0, "plane": 0, "silent": 0}
        accompaniment_families: list[str] = []
        textures: Counter[str] = Counter()
        for track_name, track in composition["tracks"].items():
            clip = track.get("sections", {}).get(section_name)
            if not clip:
                distribution["silent"] += 1
                continue
            events = _expanded_events(clip, track, bars, beats_per_bar)
            role_text = f"{track_name} {track.get('role', '')}".lower()
            percussion = any(word in role_text for word in ("drum", "percussion", "鼓", "打击"))
            melody = any(word in role_text for word in ("lead melody", "main melody", "主旋律", "hook"))
            texture = resolve_texture(track, clip)
            semantic_phrase = clip.get("instrument_phrase", {})
            semantic_type = str(semantic_phrase.get("phrase_type", ""))
            continuity = normalize_continuity(texture, track.get("continuity"), clip.get("continuity")) if texture else None
            generated_events = [event for event in events if event.get("generated_texture")]
            analyzed_events = generated_events if generated_events else events
            family = _infer_family(texture, analyzed_events, percussion)
            distribution[family] += 1
            if texture:
                textures[texture] += 1
            if not percussion and not melody and family != "silent":
                accompaniment_families.append(family)

            durations = [float(event["duration"]) for event in analyzed_events for _ in range(event["multiplicity"])]
            gaps = _onset_gaps(analyzed_events)
            average_duration = float(np.mean(durations)) if durations else 0.0
            short_ratio = sum(duration < 0.75 for duration in durations) / len(durations) if durations else 0.0
            sustain_ratio = sum(duration >= 1.75 for duration in durations) / len(durations) if durations else 0.0
            legato_ratio = sum(abs(gap) <= 0.12 or gap < 0 for gap in gaps) / len(gaps) if gaps else 0.0
            overlap_ratio = sum(gap < -0.01 for gap in gaps) / len(gaps) if gaps else 0.0
            positive_gaps = [gap for gap in gaps if gap > 0.01]

            if clip.get("harmony_spans") and texture:
                pattern = dict(track.get("texture_pattern", {}))
                pattern.update(clip.get("texture_pattern", {}))
                register = tuple(pattern.get("register", [55, 76]))
                voices = int(pattern.get("voices", 3))
                normalized = continuity or normalize_continuity(texture)
                voicings = plan_smooth_voicings(clip["harmony_spans"], register, voices, normalized["common_tone_retention"], normalized["voice_leading_strength"])
            else:
                voicings = _explicit_voicings(analyzed_events)
            voice_distance, common_retention = _voicing_metrics(voicings)

            metric = {
                "texture": texture or "implicit",
                "family": family,
                "average_note_duration": average_duration,
                "short_note_ratio": short_ratio,
                "sustain_ratio": sustain_ratio,
                "legato_ratio": legato_ratio,
                "average_gap_between_notes": float(np.mean(positive_gaps)) if positive_gaps else 0.0,
                "overlap_ratio": overlap_ratio,
                "duration_entropy": _entropy(durations),
                "voice_leading_distance": voice_distance,
                "common_tone_retention": common_retention,
                "event_count": len(analyzed_events),
                "total_track_event_count": len(events),
                "continuity_target": continuity,
            }
            track_metrics.setdefault(track_name, {})[section_name] = metric

            intentional_detached = semantic_type in {"palm_muted_eighths", "open_power_chords"}
            if not percussion and not melody and not intentional_detached and len(analyzed_events) >= bars * 2 and short_ratio >= 0.70 and metric["duration_entropy"] < 0.75 and metric["average_gap_between_notes"] >= 0.12:
                warnings.append({"code": "pointillistic_disconnected", "section": section_name, "track": track_name, "message": "accompaniment is overly pointillistic / disconnected"})
            if texture in {"sustain", "pedal"} and sustain_ratio < 0.60:
                warnings.append({"code": "texture_target_mismatch", "section": section_name, "track": track_name, "message": f"{texture} texture lacks sustained durations"})
            if texture in {"arpeggio", "counterline", "broken_chord"} and len(gaps) >= 4 and legato_ratio < 0.35:
                warnings.append({"code": "line_is_disconnected", "section": section_name, "track": track_name, "message": f"{texture} should read as a connected line"})
            if voice_distance > 7.0 and len(voicings) >= 3:
                warnings.append({"code": "poor_voice_leading", "section": section_name, "track": track_name, "message": "adjacent chord voicings move too far on average"})
            if texture == "stab" and bars >= 8 and len(analyzed_events) >= bars * 3:
                warnings.append({"code": "excessive_stab", "section": section_name, "track": track_name, "message": "stab texture dominates a long section"})

        non_silent_accompaniment = [family for family in accompaniment_families if family != "silent"]
        if len(non_silent_accompaniment) >= 3 and set(non_silent_accompaniment) == {"point"}:
            warnings.append({"code": "arrangement_lacks_continuity", "section": section_name, "track": "*", "message": "arrangement lacks sustained harmonic layers and continuous lines"})
        if textures.get("stab", 0) >= 3:
            warnings.append({"code": "too_many_stabs", "section": section_name, "track": "*", "message": "multiple accompaniment tracks use stab simultaneously"})
        section_metrics[section_name] = {
            "texture_distribution": dict(textures),
            "point_line_plane_balance": distribution,
            "accompaniment_families": non_silent_accompaniment,
        }

    return {
        "track_metrics": track_metrics,
        "section_metrics": section_metrics,
        "warnings": warnings,
        "warning_count": len(warnings),
    }
