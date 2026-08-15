from __future__ import annotations

import statistics
from collections import Counter
from copy import deepcopy
from typing import Any

from src.accompaniment.generator import materialize_clip
from src.instruments import compile_instrument_phrase
from src.instruments.common import position
from src.midi.pitches import note_number


LONG_FORM_MODES = {"long_form_authored", "long_form_experimental", "long_form"}


def _diagnostic(
    severity: str,
    code: str,
    track: str,
    section: str,
    message: str,
    evidence: Any,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "code": code,
        "track": track,
        "section": section,
        "message": message,
        "evidence": evidence,
    }


def _scaled_rule(value: Any, bars: int) -> int:
    return int(value) * max(1, bars // 8)


def _explicit_development_count(relationships: list[dict[str, Any]]) -> int:
    """Count executable authored changes, not semantic labels."""
    return sum(
        bool(rel.get("transform") or rel.get("note_overrides"))
        for rel in relationships
    )


def _apply_explicit_rules(
    *,
    rules: dict[str, Any],
    arc: dict[str, Any],
    relationships: list[dict[str, Any]],
    metrics: dict[str, Any],
    track_name: str,
    section_name: str,
    diagnostics: list[dict[str, Any]],
) -> None:
    """Judge only rules that the active project explicitly requested.

    Measurements are always useful. A missing style rule is never silently replaced by
    an engine default, because doing so would turn validation into a hidden composer.
    """
    bars = int(metrics["bars"])

    if "minimum_cross_bar_notes_per_8_bars" in rules:
        target = _scaled_rule(rules["minimum_cross_bar_notes_per_8_bars"], bars)
        if metrics["cross_bar_notes"] < target:
            diagnostics.append(_diagnostic(
                "warning",
                "too_few_cross_bar_notes",
                track_name,
                section_name,
                "cross-bar continuity is below the active project's explicit target",
                {"actual": metrics["cross_bar_notes"], "target": target},
            ))

    if "minimum_motif_developments_per_section" in rules:
        target = int(rules["minimum_motif_developments_per_section"])
        if metrics["motif_developments"] < target:
            diagnostics.append(_diagnostic(
                "warning",
                "insufficient_motif_development",
                track_name,
                section_name,
                "explicit motif transformations are below the active project's target",
                {"actual": metrics["motif_developments"], "target": target},
            ))

    if "maximum_independent_phrase_resets_per_8_bars" in rules:
        limit = _scaled_rule(rules["maximum_independent_phrase_resets_per_8_bars"], bars)
        if metrics["independent_phrase_resets"] > limit:
            diagnostics.append(_diagnostic(
                "warning",
                "excessive_phrase_resets",
                track_name,
                section_name,
                "phrase resets exceed the active project's explicit limit",
                {"actual": metrics["independent_phrase_resets"], "limit": limit},
            ))

    if "maximum_strong_cadences_per_8_bars" in rules:
        limit = _scaled_rule(rules["maximum_strong_cadences_per_8_bars"], bars)
        if metrics["strong_cadences"] > limit:
            diagnostics.append(_diagnostic(
                "warning",
                "excessive_strong_cadences",
                track_name,
                section_name,
                "strong cadences exceed the active project's explicit limit",
                {"actual": metrics["strong_cadences"], "limit": limit},
            ))

    if rules.get("require_delayed_peak"):
        planned = arc.get("peak_bar")
        if planned is None:
            diagnostics.append(_diagnostic(
                "error",
                "missing_peak_plan",
                track_name,
                section_name,
                "require_delayed_peak needs section_arc.peak_bar",
                None,
            ))
        elif metrics["peak_bars"] and min(metrics["peak_bars"]) < int(planned):
            diagnostics.append(_diagnostic(
                "warning",
                "early_peak",
                track_name,
                section_name,
                "highest pitch arrives before the active project's explicit peak bar",
                {"actual": metrics["peak_bars"], "planned": planned},
            ))

    if rules.get("require_delayed_resolution"):
        planned = arc.get("final_resolution_bar")
        if planned is None:
            diagnostics.append(_diagnostic(
                "error",
                "missing_resolution_plan",
                track_name,
                section_name,
                "require_delayed_resolution needs section_arc.final_resolution_bar",
                None,
            ))
        else:
            strong_bars = metrics["strong_cadence_bars"]
            if int(planned) not in strong_bars or any(bar < int(planned) for bar in strong_bars):
                diagnostics.append(_diagnostic(
                    "warning",
                    "resolution_not_delayed",
                    track_name,
                    section_name,
                    "strong resolution does not follow the project's explicit resolution bar",
                    {"actual": strong_bars, "planned": planned},
                ))

    if rules.get("require_continuation_graph") and (
        metrics["boundary_continuations"] < max(0, len(relationships) - 1)
    ):
        diagnostics.append(_diagnostic(
            "warning",
            "broken_relationship_graph",
            track_name,
            section_name,
            "one or more phrase boundaries violate the explicit continuation rule",
            metrics["boundary_continuations"],
        ))

    if rules.get("reject_identical_short_phrase") and metrics["identical_short_phrase_repetitions"]:
        diagnostics.append(_diagnostic(
            "warning",
            "identical_short_phrase",
            track_name,
            section_name,
            "identical short phrases violate the active project's explicit rule",
            metrics["identical_short_phrase_repetitions"],
        ))

    if rules.get("preserve_state_across_breaths") and metrics["breath_state_resets"]:
        diagnostics.append(_diagnostic(
            "warning",
            "breath_resets_state",
            track_name,
            section_name,
            "a breath resets state despite the active project's explicit rule",
            metrics["breath_state_resets"],
        ))

    if rules.get("forbid_automatic_vibrato_endings") and metrics["ending_vibrato_bars"]:
        diagnostics.append(_diagnostic(
            "warning",
            "automatic_vibrato_endings",
            track_name,
            section_name,
            "phrase-ending vibrato violates the active project's explicit rule",
            metrics["ending_vibrato_bars"],
        ))

    if "maximum_consecutive_full_rest_bars" in rules:
        limit = int(rules["maximum_consecutive_full_rest_bars"])
        if metrics["maximum_consecutive_full_rest_bars"] > limit:
            diagnostics.append(_diagnostic(
                "warning",
                "excessive_structural_silence",
                track_name,
                section_name,
                "full-bar silence exceeds the active project's explicit limit",
                {"actual": metrics["maximum_consecutive_full_rest_bars"], "limit": limit},
            ))

    if rules.get("require_peak_bar_match"):
        planned = arc.get("peak_bar")
        if planned is None:
            diagnostics.append(_diagnostic(
                "error",
                "missing_peak_plan",
                track_name,
                section_name,
                "require_peak_bar_match needs section_arc.peak_bar",
                None,
            ))
        elif metrics["peak_bars"] and metrics["peak_bars"][0] != int(planned):
            diagnostics.append(_diagnostic(
                "warning",
                "register_curve_misses_peak",
                track_name,
                section_name,
                "actual highest register does not match this project's explicit peak bar",
                {"actual": metrics["peak_bars"], "planned": planned},
            ))

    if "maximum_articulation_end_concentration_ratio" in rules:
        limit = float(rules["maximum_articulation_end_concentration_ratio"])
        if metrics["articulation_end_concentration_ratio"] > limit:
            diagnostics.append(_diagnostic(
                "warning",
                "articulation_concentrated_at_endings",
                track_name,
                section_name,
                "ending articulation concentration exceeds the active project's explicit limit",
                {
                    "actual": metrics["articulation_end_concentration_ratio"],
                    "limit": limit,
                },
            ))


def analyze_long_form_phrases(composition: dict[str, Any]) -> dict[str, Any]:
    beats = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    reports: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []

    for track_name, track in composition["tracks"].items():
        for section_name, clip in track.get("sections", {}).items():
            phrase = clip.get("instrument_phrase")
            if not phrase or phrase.get("phrase_generation_mode", "legacy_stable") not in LONG_FORM_MODES:
                continue

            if "_long_form_plan" not in phrase:
                compile_instrument_phrase(phrase, beats)

            events = [
                event
                for event in materialize_clip(deepcopy(clip), track, beats)
                if event.get("type", "note") == "note"
            ]
            if not events:
                diagnostics.append(_diagnostic(
                    "error",
                    "empty_long_form_phrase",
                    track_name,
                    section_name,
                    "long-form phrase produced no note events",
                    None,
                ))
                continue

            arc = phrase["section_arc"]
            relationships = phrase["phrase_relationships"]
            bars = int(clip["loop_bars"])
            rules = phrase.get("long_form_phrase_rules", {})
            onsets = [(position(event["at"], beats), event) for event in events]

            cross_bar = sum(
                1
                for start, event in onsets
                if start + float(event["duration"])
                > (int(start // beats) + 1) * beats + 1e-6
            )
            peak_pitch = max(note_number(event["pitch"]) for event in events)
            peak_bars = [
                int(start // beats) + 1
                for start, event in onsets
                if note_number(event["pitch"]) == peak_pitch
            ]

            operations = [
                operation
                for rel in relationships
                for operation in rel.get("motif_operations", [])
            ]
            development_count = _explicit_development_count(relationships)
            resets = sum(
                1
                for index, rel in enumerate(relationships)
                if index and rel.get("continuation_from") is None
            )
            strong = [rel for rel in relationships if rel["resolution"] == "strong"]
            boundary_continuations = sum(
                1
                for rel in relationships[:-1]
                if rel["resolution"] != "strong" and rel.get("continuation_to")
            )
            vibrato_bars = [
                int(start // beats) + 1
                for start, event in onsets
                if "vibrato" in event.get("articulations", [])
            ]
            phrase_lengths = [
                rel["bars"][1] - rel["bars"][0] + 1 for rel in relationships
            ]

            signatures: Counter[tuple[Any, ...]] = Counter()
            reference_pitch = note_number(events[0]["pitch"])
            for rel in relationships:
                start_beat = (rel["bars"][0] - 1) * beats
                end_beat = rel["bars"][1] * beats
                signature = tuple(
                    (
                        round(start - start_beat, 3),
                        note_number(event["pitch"]) - reference_pitch,
                        round(float(event["duration"]), 3),
                    )
                    for start, event in onsets
                    if start_beat <= start < end_beat
                )
                signatures[signature] += 1
            identical = sum(count - 1 for count in signatures.values() if count > 1)

            full_rest_bars: list[int] = []
            register_curve: list[float | None] = []
            for bar in range(1, bars + 1):
                bar_pitches = [
                    note_number(event["pitch"])
                    for start, event in onsets
                    if (bar - 1) * beats <= start < bar * beats
                ]
                register_curve.append(
                    statistics.median(bar_pitches) if bar_pitches else None
                )
                if not bar_pitches:
                    full_rest_bars.append(bar)

            state_trace = phrase.get("_long_form_plan", {}).get(
                "melodic_state_trace", []
            )
            breath_resets = sum(
                1
                for item in state_trace
                if item.get("rest_type") == "breath"
                and not item.get("continuation_required")
            )

            phrase_ends = {rel["bars"][1] * beats for rel in relationships}
            expressive = [
                (start, event)
                for start, event in onsets
                if set(event.get("articulations", []))
                & {"slide", "hammer_on", "pull_off", "bend", "vibrato"}
            ]
            ending_expression = sum(
                1
                for start, event in expressive
                if any(
                    abs((start + float(event["duration"])) - end) <= 0.8
                    for end in phrase_ends
                )
            )
            articulation_end_ratio = (
                ending_expression / len(expressive) if expressive else 0.0
            )
            ending_vibrato_bars = sorted({
                int(start // beats) + 1
                for start, event in onsets
                if "vibrato" in event.get("articulations", [])
                and any(
                    abs((start + float(event["duration"])) - end) <= 0.8
                    for end in phrase_ends
                )
            })

            longest_rest_run = 0
            run = 0
            for bar in range(1, bars + 1):
                run = run + 1 if bar in full_rest_bars else 0
                longest_rest_run = max(longest_rest_run, run)

            plan = phrase.get("_long_form_plan", {})
            metrics = {
                "bars": bars,
                "execution_policy": plan.get("execution_policy", "unknown"),
                "average_phrase_length_bars": statistics.mean(phrase_lengths),
                "independent_phrase_resets": resets,
                "strong_cadences": len(strong),
                "strong_cadence_bars": [rel["bars"][1] for rel in strong],
                "cross_bar_notes": cross_bar,
                "motif_developments": development_count,
                "motif_operations": sorted(set(operations)),
                "identical_short_phrase_repetitions": identical,
                "breath_state_resets": breath_resets,
                "peak_pitch": peak_pitch,
                "peak_bars": peak_bars,
                "planned_peak_bar": arc.get("peak_bar"),
                "vibrato_bars": vibrato_bars,
                "ending_vibrato_bars": ending_vibrato_bars,
                "boundary_continuations": boundary_continuations,
                "full_rest_bars": full_rest_bars,
                "maximum_consecutive_full_rest_bars": longest_rest_run,
                "register_curve_median_midi": register_curve,
                "register_curve_peak_bar": peak_bars[0] if peak_bars else None,
                "articulation_end_concentration_ratio": articulation_end_ratio,
                "relationship_counts": dict(
                    Counter(rel["relationship"] for rel in relationships)
                ),
                "continuous_narrative_bars": (
                    arc["bars"][1] - arc["bars"][0] + 1
                    if boundary_continuations == max(0, len(relationships) - 1)
                    else max(phrase_lengths)
                ),
                "sees_full_section_harmony": len(phrase.get("harmony", [])) >= bars,
                "active_style_rules": sorted(rules),
            }

            reports.append({
                "track": track_name,
                "section": section_name,
                "assessment": metrics,
                "section_arc": deepcopy(arc),
                "phrase_relationships": deepcopy(relationships),
                "melodic_state_trace": deepcopy(state_trace),
            })

            _apply_explicit_rules(
                rules=rules,
                arc=arc,
                relationships=relationships,
                metrics=metrics,
                track_name=track_name,
                section_name=section_name,
                diagnostics=diagnostics,
            )

    return {
        "schema_version": 2,
        "title": composition["metadata"]["title"],
        "sections": reports,
        "diagnostics": diagnostics,
        "error_count": sum(item["severity"] == "error" for item in diagnostics),
        "warning_count": sum(item["severity"] == "warning" for item in diagnostics),
    }
