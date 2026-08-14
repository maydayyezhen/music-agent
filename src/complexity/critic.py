from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from src.complexity.schema import resolve_section_complexities
from src.accompaniment.generator import materialize_clip


@dataclass
class TrackSectionMetrics:
    note_density: float
    rest_ratio: float
    duration_entropy: float
    same_grid_ratio: float
    velocity_variance: float
    pattern_repetition: float
    event_count: int


def _position(value: str, beats_per_bar: int) -> float:
    bar, beat = value.split(":", 1)
    return (int(bar) - 1) * beats_per_bar + float(beat) - 1.0


def _entropy(values: list[float]) -> float:
    if not values:
        return 0.0
    counts = Counter(round(value, 4) for value in values)
    probabilities = [count / len(values) for count in counts.values()]
    return float(-sum(p * math.log2(p) for p in probabilities))


def _union_coverage(intervals: list[tuple[float, float]], total: float) -> float:
    if not intervals or total <= 0:
        return 0.0
    merged: list[list[float]] = []
    for start, end in sorted(intervals):
        start, end = max(0.0, start), min(total, end)
        if end <= start:
            continue
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return sum(end - start for start, end in merged) / total


def _expanded_events(clip: dict[str, Any], track: dict[str, Any], section_bars: int, beats_per_bar: int) -> list[dict[str, float]]:
    loop_bars = int(clip["loop_bars"])
    loop_beats = loop_bars * beats_per_bar
    result: list[dict[str, float]] = []
    for loop_bar in range(0, section_bars, loop_bars):
        shift = loop_bar * beats_per_bar
        for event in materialize_clip(clip, track, beats_per_bar):
            if event.get("type", "note") in {"rest", "control_change"}:
                continue
            start = shift + _position(event["at"], beats_per_bar)
            if start >= section_bars * beats_per_bar:
                continue
            multiplicity = len(event.get("pitches", [])) if event.get("type") == "chord" else 1
            result.append({
                "start": start,
                "duration": float(event["duration"]),
                "velocity": float(event["velocity"]),
                "notes": float(max(1, multiplicity)),
                "loop_phase": (start - shift) % loop_beats,
            })
    return result


def analyze_complexity(composition: dict[str, Any]) -> dict[str, Any]:
    beats_per_bar = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    section_profiles = resolve_section_complexities(composition)
    track_metrics: dict[str, dict[str, dict[str, float | int]]] = {}
    section_metrics: dict[str, dict[str, float | int]] = {}
    warnings: list[dict[str, str]] = []

    for section in composition["sections"]:
        section_name, bars = str(section["name"]), int(section["bars"])
        total_beats = bars * beats_per_bar
        events_by_track: dict[str, list[dict[str, float]]] = {}
        for track_name, track in composition["tracks"].items():
            clip = track.get("sections", {}).get(section_name)
            events = _expanded_events(clip, track, bars, beats_per_bar) if clip else []
            events_by_track[track_name] = events
            intervals = [(item["start"], item["start"] + item["duration"]) for item in events]
            durations = [item["duration"] for item in events]
            velocities = [item["velocity"] for item in events]
            onsets = [item["start"] for item in events]
            phases = [item["loop_phase"] for item in events]
            on_grid = sum(abs(onset * 2 - round(onset * 2)) < 1e-6 for onset in onsets)
            repetition = 0.0
            if phases:
                repetition = 1.0 - len(set(round(phase, 3) for phase in phases)) / len(phases)
            metric = TrackSectionMetrics(
                note_density=sum(item["notes"] for item in events) / max(1, bars),
                rest_ratio=1.0 - _union_coverage(intervals, total_beats),
                duration_entropy=_entropy(durations),
                same_grid_ratio=on_grid / len(onsets) if onsets else 0.0,
                velocity_variance=float(np.var(velocities)) if velocities else 0.0,
                pattern_repetition=max(0.0, repetition),
                event_count=len(events),
            )
            track_metrics.setdefault(track_name, {})[section_name] = asdict(metric)

        active = [name for name, events in events_by_track.items() if events]
        onset_sets = {name: {round(item["start"], 3) for item in events} for name, events in events_by_track.items() if events}
        pair_scores: list[float] = []
        names = list(onset_sets)
        for index, first in enumerate(names):
            for second in names[index + 1:]:
                union = onset_sets[first] | onset_sets[second]
                if union:
                    pair_scores.append(len(onset_sets[first] & onset_sets[second]) / len(union))
        total_events = sum(len(events) for events in events_by_track.values())
        profile = section_profiles[section_name]
        section_metrics[section_name] = {
            "section_density": total_events / max(1, bars),
            "active_tracks": len(active),
            "track_overlap_ratio": len(active) / max(1, len(composition["tracks"])),
            "onset_overlap_ratio": float(np.mean(pair_scores)) if pair_scores else 0.0,
            "target_budget": int(profile["budget"]),
            "declared_budget_total": sum(section.get("complexity_budget", {}).values()),
        }

        # Warnings are intentionally profile-aware: repetition is acceptable
        # in minimal music, while uncontrolled all-track activity is not.
        level = profile["level"]
        for track_name in active:
            metric = track_metrics[track_name][section_name]
            role_text = (str(composition["tracks"][track_name].get("role", "")) + " " + track_name).lower()
            melodic = any(word in role_text for word in ("melody", "lead", "hook", "主题", "旋律"))
            percussion = any(word in role_text for word in ("drum", "percussion", "鼓", "打击"))
            if melodic and bars >= 8 and metric["rest_ratio"] < profile["melody_rest_ratio_guide"][0] * 0.55:
                warnings.append({"code": "melody_no_breath", "section": section_name, "track": track_name, "message": "melodic track has too little phrase space"})
            if not percussion and metric["event_count"] >= bars * 4 and metric["duration_entropy"] < 0.35 and metric["same_grid_ratio"] > 0.9:
                warnings.append({"code": "mechanical_equal_duration", "section": section_name, "track": track_name, "message": "long equal-duration grid pattern; confirm a stylistic reason"})
        overlap = float(section_metrics[section_name]["onset_overlap_ratio"])
        if len(active) >= 3 and overlap > 0.62:
            warnings.append({"code": "tracks_speak_together", "section": section_name, "track": "*", "message": "multiple tracks share most onsets; create rhythmic identities or call-and-response"})
        all_active = (
            len(active) == len(composition["tracks"])
            and len(active) >= 4
            and all(track_metrics[name][section_name]["rest_ratio"] < 0.40 for name in active)
        )
        if bars >= 8 and all_active:
            warnings.append({"code": "all_tracks_continuous", "section": section_name, "track": "*", "message": "all tracks remain active for a long section; confirm foreground/background hierarchy"})
        density = float(section_metrics[section_name]["section_density"])
        if level == "minimal" and (density > 14 or len(active) > 3 or (overlap > 0.55 and density > 6)):
            warnings.append({"code": "target_mismatch_minimal", "section": section_name, "track": "*", "message": "measured density/overlap is high for minimal"})
        if level in ("rich", "dense") and density < 4 and len(active) < 3:
            warnings.append({"code": "target_mismatch_rich", "section": section_name, "track": "*", "message": "section is sparse and under-developed for its rich/dense target"})

        # Distributed budget proxy: count how many tracks are simultaneously
        # high-density/high-rhythm. It warns rather than rewriting music.
        busy_tracks = sum(
            1 for track_name in active
            if track_metrics[track_name][section_name]["note_density"] >= 6
            and track_metrics[track_name][section_name]["duration_entropy"] >= 1.0
        )
        if busy_tracks >= 4:
            warnings.append({"code": "budget_duplicated", "section": section_name, "track": "*", "message": "four or more tracks are independently busy; distribute complexity instead of duplicating it"})
        declared_total = int(section_metrics[section_name]["declared_budget_total"])
        if declared_total > int(profile["budget"]):
            warnings.append({"code": "budget_over_target", "section": section_name, "track": "*", "message": f"declared role budget {declared_total} exceeds the {level} guide {profile['budget']}"})

    return {
        "global_target": resolve_section_complexities(composition),
        "track_metrics": track_metrics,
        "section_metrics": section_metrics,
        "warnings": warnings,
        "warning_count": len(warnings),
    }
