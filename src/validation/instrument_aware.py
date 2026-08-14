from __future__ import annotations

import math
import statistics
from collections import Counter, defaultdict
from typing import Any

from src.accompaniment.generator import materialize_clip
from src.midi.pitches import drum_number, note_number

RANGES = {
    "acoustic_guitar": (40, 88), "steel_guitar": (40, 88), "nylon_guitar": (40, 88),
    "electric_guitar": (40, 88), "electric_rhythm_guitar": (40, 88), "electric_lead_guitar": (40, 88),
    "electric_bass": (28, 64), "bass": (28, 64), "piano": (21, 108), "keyboard": (21, 108),
    "organ": (36, 96), "strings": (36, 103), "string_ensemble": (36, 103), "pad": (24, 108),
}


def _position(value: str, beats_per_bar: int) -> float:
    bar, beat = value.split(":", 1)
    return (int(bar) - 1) * beats_per_bar + float(beat) - 1.0


def _pitches(event: dict[str, Any]) -> list[int]:
    if event.get("type") == "drum":
        return [drum_number(event["note"])]
    if event.get("type") == "chord":
        return [note_number(value) for value in event["pitches"]]
    if event.get("type", "note") == "note":
        return [note_number(event["pitch"])]
    return []


def _expanded(composition: dict[str, Any]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    beats = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    result: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(dict)
    for section in composition["sections"]:
        name, bars = str(section["name"]), int(section["bars"])
        for track_name, track in composition["tracks"].items():
            clip = track.get("sections", {}).get(name)
            if not clip:
                result[track_name][name] = []
                continue
            source = materialize_clip(clip, track, beats)
            events = []
            for loop_bar in range(0, bars, int(clip["loop_bars"])):
                for event in source:
                    start = loop_bar * beats + _position(event["at"], beats)
                    if start >= bars * beats:
                        continue
                    events.append({**event, "_start": start, "_pitches": _pitches(event)})
            result[track_name][name] = sorted(events, key=lambda item: (item["_start"], item.get("pitch", item.get("note", ""))))
    return result


def _instrument(track: dict[str, Any]) -> str:
    for clip in track.get("sections", {}).values():
        if clip.get("instrument_phrase"):
            return str(clip["instrument_phrase"]["instrument"]).lower()
    return str(track.get("instrument", track.get("role", "unknown"))).lower()


def _warning(code: str, track: str, section: str, message: str, evidence: Any,
             severity: str = "warning") -> dict[str, Any]:
    return {"severity": severity, "code": code, "track": track, "section": section,
            "message": message, "evidence": evidence}


def _note_spacing(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Measure per-pitch gaps and overlaps in the semantic performance events."""
    lanes: dict[int, list[tuple[float, float]]] = defaultdict(list)
    for event in events:
        if event.get("type") in {"drum", "control_change"}:
            continue
        start = float(event["_start"])
        end = start + max(0.0, float(event.get("duration", 0.0)))
        for pitch in event["_pitches"]:
            lanes[pitch].append((start, end))

    gaps: list[float] = []
    overlaps: list[float] = []
    for intervals in lanes.values():
        intervals.sort()
        previous_end: float | None = None
        for start, end in intervals:
            if previous_end is not None:
                distance = start - previous_end
                if distance < -1e-6:
                    overlaps.append(-distance)
                else:
                    gaps.append(distance)
            previous_end = max(previous_end or end, end)
    return {
        "same_pitch_overlap_count": len(overlaps),
        "max_same_pitch_overlap_beats": max(overlaps, default=0.0),
        "median_same_pitch_gap_beats": statistics.median(gaps) if gaps else None,
    }


def analyze_instrument_aware(composition: dict[str, Any]) -> dict[str, Any]:
    expanded = _expanded(composition)
    beats = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    diagnostics: list[dict[str, Any]] = []
    tracks_report: dict[str, Any] = {}
    section_density: dict[str, Any] = {}
    articulation_totals: Counter[str] = Counter()

    for track_name, track in composition["tracks"].items():
        instrument = _instrument(track)
        section_reports: dict[str, Any] = {}
        for section in composition["sections"]:
            section_name, bars = str(section["name"]), int(section["bars"])
            events = expanded[track_name].get(section_name, [])
            tonal = [event for event in events if event["_pitches"] and event.get("type") != "drum"]
            notes = [pitch for event in tonal for pitch in event["_pitches"]]
            velocities = [int(event["velocity"]) for event in events if "velocity" in event]
            onsets = sorted({round(float(event["_start"]), 4) for event in events if event.get("type") != "control_change"})
            gaps = [right - left for left, right in zip(onsets, onsets[1:])]
            articulations = Counter(art for event in tonal for art in event.get("articulations", []))
            articulation_totals.update(articulations)
            signatures: Counter[tuple[Any, ...]] = Counter()
            for bar in range(bars):
                bar_events = [event for event in events if bar * beats <= event["_start"] < (bar + 1) * beats]
                signature = tuple((round(event["_start"] - bar * beats, 3), tuple(event["_pitches"]),
                                   round(float(event.get("duration", 0)), 3)) for event in bar_events)
                if signature:  # silence is intentional phrase space, not a repeated phrase
                    signatures[signature] += 1
            repeated_bars = max(signatures.values(), default=0)
            report = {
                "instrument": instrument, "event_count": len(events), "note_count": len(notes),
                "range": [min(notes), max(notes)] if notes else None,
                "median_gap_beats": statistics.median(gaps) if gaps else None,
                "velocity_unique": len(set(velocities)),
                "velocity_stddev": statistics.pstdev(velocities) if len(velocities) > 1 else 0.0,
                "articulations": dict(articulations), "max_identical_bar_repetitions": repeated_bars,
                "events_per_bar": len(events) / bars,
                "note_spacing": _note_spacing(events),
            }
            section_reports[section_name] = report

            if notes and instrument in RANGES:
                low, high = RANGES[instrument]
                outside = [value for value in notes if value < low or value > high]
                if outside:
                    diagnostics.append(_warning("instrument_range", track_name, section_name,
                                                "notes fall outside configured instrument range", sorted(set(outside)), "error"))
            if instrument in {"acoustic_guitar", "steel_guitar", "nylon_guitar", "electric_guitar", "electric_rhythm_guitar", "electric_lead_guitar"}:
                missing = sum(1 for event in tonal if "_string" not in event or "_fret" not in event)
                simultaneous: dict[float, list[dict[str, Any]]] = defaultdict(list)
                for event in tonal:
                    simultaneous[round(event["_start"], 4)].append(event)
                conflicts = sum(1 for group in simultaneous.values()
                                if len([event.get("_string") for event in group]) != len(set(event.get("_string") for event in group)))
                perfectly_simultaneous_chords = sum(1 for group in simultaneous.values() if len(group) >= 2)
                if missing:
                    diagnostics.append(_warning("guitar_assignment_missing", track_name, section_name,
                                                "guitar notes lack string/fret assignment", missing))
                if conflicts:
                    diagnostics.append(_warning("guitar_string_conflict", track_name, section_name,
                                                "simultaneous notes compete for one string", conflicts, "error"))
                if perfectly_simultaneous_chords and not any(event.get("_attack_group") for event in tonal):
                    diagnostics.append(_warning("keyboard_like_chords", track_name, section_name,
                                                "all chord tones attack simultaneously with no strum grouping",
                                                perfectly_simultaneous_chords))
                if "lead" in instrument and len(tonal) >= bars * 2 and not ({"bend", "slide", "legato", "hammer_on", "pull_off"} & set(articulations)):
                    diagnostics.append(_warning("lead_no_expression", track_name, section_name,
                                                "active lead phrase has no expressive transition articulation",
                                                dict(articulations)))
            if instrument in {"drum_kit", "drums"}:
                onset_groups: dict[float, list[dict[str, Any]]] = defaultdict(list)
                for event in events:
                    onset_groups[round(event["_start"], 4)].append(event)
                conflicts = []
                for onset, group in onset_groups.items():
                    limbs = [event.get("_limb") for event in group]
                    if None in limbs or len(limbs) != len(set(limbs)):
                        conflicts.append({"beat": onset, "voices": [event.get("note") for event in group], "limbs": limbs})
                if conflicts:
                    diagnostics.append(_warning("drum_limb_conflict", track_name, section_name,
                                                "simultaneous kit hits cannot be assigned to declared limbs", conflicts[:8], "error"))
            if repeated_bars >= 5 and len(events) >= bars:
                diagnostics.append(_warning("excessive_repetition", track_name, section_name,
                                            "many bars repeat an identical event signature", repeated_bars))
            if len(velocities) >= 8 and len(set(velocities)) <= 2:
                diagnostics.append(_warning("flat_velocity_pattern", track_name, section_name,
                                            "velocity pattern has almost no accent hierarchy", report["velocity_unique"]))
        tracks_report[track_name] = {"instrument": instrument, "sections": section_reports}

    # Cross-track metrics: density, register collision, and bass/kick relation.
    for section in composition["sections"]:
        name, bars = str(section["name"]), int(section["bars"])
        per_track = {track_name: len(expanded[track_name].get(name, [])) / bars for track_name in composition["tracks"]}
        section_density[name] = {"events_per_bar": sum(per_track.values()), "by_track": per_track,
                                 "active_tracks": sum(value > 0 for value in per_track.values())}
        tonal_ranges = []
        for track_name, track in composition["tracks"].items():
            pitches = [pitch for event in expanded[track_name].get(name, []) if event.get("type") != "drum" for pitch in event["_pitches"]]
            if pitches:
                tonal_ranges.append((track_name, statistics.median(pitches), min(pitches), max(pitches)))
        for index, first in enumerate(tonal_ranges):
            for second in tonal_ranges[index + 1:]:
                if abs(first[1] - second[1]) <= 2 and max(first[2], second[2]) <= min(first[3], second[3]):
                    diagnostics.append(_warning("register_collision", f"{first[0]}+{second[0]}", name,
                                                "tracks share nearly identical median register", [first[1], second[1]], "info"))

        bass_tracks = [track_name for track_name, track in composition["tracks"].items() if _instrument(track) in {"electric_bass", "bass"}]
        drum_tracks = [track_name for track_name, track in composition["tracks"].items() if _instrument(track) in {"drum_kit", "drums"}]
        for bass_name in bass_tracks:
            bass_onsets = {round(event["_start"], 3) for event in expanded[bass_name].get(name, []) if event.get("type") == "note"}
            for drum_name in drum_tracks:
                kick_onsets = {round(event["_start"], 3) for event in expanded[drum_name].get(name, []) if event.get("note") == "kick"}
                if bass_onsets and kick_onsets:
                    ratio = len(bass_onsets & kick_onsets) / len(bass_onsets)
                    tracks_report[bass_name]["sections"][name]["kick_alignment_ratio"] = ratio
                    if ratio < 0.2 or ratio > 0.9:
                        diagnostics.append(_warning("bass_kick_relationship", bass_name, name,
                                                    "bass is weakly related to kick or copies it almost completely", round(ratio, 3)))

    profile_coverage: dict[str, Any] = {}
    for track_name, track in composition["tracks"].items():
        for section_name, clip in track.get("sections", {}).items():
            if clip.get("_profile_report"):
                profile_coverage[f"{track_name}.{section_name}"] = clip["_profile_report"]
    return {
        "schema_version": 1,
        "title": composition["metadata"]["title"],
        "track_metrics": tracks_report,
        "section_density": section_density,
        "articulation_coverage": dict(articulation_totals),
        "profile_coverage": profile_coverage,
        "phrase_variation": {"diagnostic_count": sum(item["code"] == "excessive_repetition" for item in diagnostics)},
        "diagnostics": diagnostics,
        "error_count": sum(item["severity"] == "error" for item in diagnostics),
        "warning_count": sum(item["severity"] == "warning" for item in diagnostics),
        "info_count": sum(item["severity"] == "info" for item in diagnostics),
    }
