from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from typing import Any

from src.instruments import compile_instrument_phrase


GUITAR_NAMES = {"acoustic_guitar", "steel_guitar", "nylon_guitar", "electric_guitar", "electric_rhythm_guitar"}


def _position(value: str, beats_per_bar: int) -> float:
    bar, beat = value.split(":", 1)
    return (int(bar) - 1) * beats_per_bar + float(beat) - 1


def _instrument(track_name: str, track: dict[str, Any]) -> str:
    for clip in track.get("sections", {}).values():
        phrase = clip.get("instrument_phrase")
        if phrase:
            return str(phrase.get("instrument", "")).lower()
    text = f"{track_name} {track.get('instrument', '')} {track.get('role', '')}".lower()
    if "acoustic" in text or "steel guitar" in text: return "acoustic_guitar"
    if "electric" in text and "guitar" in text: return "electric_rhythm_guitar"
    return ""


def _grid(clip: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    if isinstance(clip.get("strumming_grid"), list):
        return deepcopy(clip["strumming_grid"])
    phrase = clip.get("instrument_phrase")
    if not phrase:
        return []
    if "_strumming_debug" not in phrase:
        compile_instrument_phrase(phrase, beats_per_bar)
    return deepcopy(phrase.get("_strumming_debug", {}).get("bars", []))


def _sounding_actions(bar: dict[str, Any]) -> list[tuple[int, str]]:
    return [(index, action) for index, action in enumerate(bar.get("actions", [])) if action != "air_strum"]


def analyze_strumming_flow(composition: dict[str, Any]) -> dict[str, Any]:
    beats = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    tracks: dict[str, Any] = {}
    diagnostics: list[dict[str, Any]] = []
    vocal_active: dict[str, set[int]] = defaultdict(set)
    for track_name, track in composition.get("tracks", {}).items():
        if "vocal" not in f"{track_name} {track.get('role', '')}".lower(): continue
        for section, clip in track.get("sections", {}).items():
            for event in clip.get("events", []):
                vocal_active[section].add(int(str(event["at"]).split(":", 1)[0]))

    for track_name, track in composition.get("tracks", {}).items():
        instrument = _instrument(track_name, track)
        if instrument not in GUITAR_NAMES: continue
        section_reports = {}
        for section in composition["sections"]:
            name, bars = str(section["name"]), int(section["bars"])
            clip = track.get("sections", {}).get(name)
            if not clip:
                continue
            grid = _grid(clip, beats)
            if not grid:
                continue
            actions = [action for bar in grid for action in bar.get("actions", [])]
            sounding = [_sounding_actions(bar) for bar in grid]
            one = [index + 1 for index, values in enumerate(sounding) if len(values) == 1]
            first_only = [index + 1 for index, values in enumerate(sounding) if values and [step for step, _ in values] == [0]]
            sustained_without_followup = []
            for bar_number in first_only:
                events = clip.get("events", [])
                in_bar = [event for event in events if int(str(event["at"]).split(":", 1)[0]) == bar_number]
                if any(float(event.get("duration", 0)) >= beats - .1 for event in in_bar) or grid[bar_number - 1].get("pattern_id") == "single_hit":
                    sustained_without_followup.append(bar_number)
            reset_bars = []
            for left, right in zip(grid, grid[1:]):
                if not left.get("pattern_continues_across_bar", True) or left.get("next_expected_direction") != right.get("hand_motion", [None])[0]:
                    reset_bars.append(int(right["bar"]))
            changes_interrupted = [int(bar["bar"]) for bar in grid[:-1] if not bar.get("pattern_continues_across_bar", True)]
            audible = [len(values) for values in sounding]
            active = vocal_active.get(name, set())
            active_counts = [audible[index - 1] for index in active if 1 <= index <= len(audible)]
            rest_counts = [count for index, count in enumerate(audible, 1) if index not in active]
            report = {
                "bars": bars,
                "average_hand_motions_per_bar": sum(len(bar.get("hand_motion", [])) for bar in grid) / len(grid),
                "average_sounding_strums_per_bar": sum(audible) / len(audible),
                "only_one_strum_bars": one,
                "only_downbeat_strum_bars": first_only,
                "sustained_four_beats_without_followup_bars": sustained_without_followup,
                "ghost_strums": actions.count("ghost_strum"),
                "muted_strums": actions.count("muted_strum"),
                "air_strums": actions.count("air_strum"),
                "upstroke_ratio": sum(direction == "up" for bar in grid for direction in bar.get("hand_motion", [])) / max(1, sum(len(bar.get("hand_motion", [])) for bar in grid)),
                "bar_pattern_reset_count": len(reset_bars), "pattern_reset_bars": reset_bars,
                "chord_change_interruption_count": len(changes_interrupted),
                "vocal_active_average_sounding_strums": sum(active_counts) / len(active_counts) if active_counts else None,
                "vocal_rest_average_sounding_strums": sum(rest_counts) / len(rest_counts) if rest_counts else None,
                "sustained_only_section": all(bar.get("pattern_id") == "single_hit" for bar in grid),
                "behaves_like_pad": len(first_only) >= max(2, math_ceil(len(grid) * .5)),
                "bar_details": grid,
            }
            section_reports[name] = report
            lowered = name.lower()
            minimum = 5 if "chorus" in lowered else 3 if "verse" in lowered or "pre" in lowered else 0
            if minimum and report["average_sounding_strums_per_bar"] < minimum:
                diagnostics.append({"severity": "warning", "code": "insufficient_continuous_strumming", "track": track_name,
                                    "section": name, "message": f"average audible strums are below {minimum}/bar",
                                    "evidence": {"average": report["average_sounding_strums_per_bar"], "bars": first_only}})
            if report["behaves_like_pad"] and ("verse" in lowered or "chorus" in lowered):
                diagnostics.append({"severity": "warning", "code": "guitar_behaves_like_pad", "track": track_name,
                                    "section": name, "message": "guitar has only one sounding downbeat in at least half the bars", "evidence": first_only})
        tracks[track_name] = {"instrument": instrument, "sections": section_reports}
    return {"schema_version": 1, "title": composition.get("metadata", {}).get("title"), "tracks": tracks,
            "diagnostics": diagnostics, "warning_count": len(diagnostics)}


def math_ceil(value: float) -> int:
    return int(value) if value == int(value) else int(value) + 1
