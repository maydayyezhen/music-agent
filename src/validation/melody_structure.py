from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from src.midi.pitches import note_number


def analyze_melody_structure(plan: dict[str, Any], notes: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate declared melody hierarchy without pretending to score musical taste.

    This validator checks whether a foreground melody actually records structural targets,
    motif recurrence/development, phrase identity and surface embellishment relationships.
    Descriptive statistics such as local-motion ratio, repeated-pitch ratio, density and apex
    position are reported but intentionally are not universal pass/fail thresholds.
    """
    events = sorted(notes, key=lambda item: float(item["start_beat"]))
    if not events:
        return {
            "schema_version": 1,
            "metrics": {"notes": 0},
            "checks": {"has_notes": False},
            "failures": ["has_notes"],
            "passed": False,
        }

    pitches = [note_number(item["pitch"]) for item in events]
    intervals = [abs(b - a) for a, b in zip(pitches, pitches[1:])]
    structural = [item for item in events if item.get("structural_role") == "structural"]
    surface = [item for item in events if item.get("structural_role") == "surface"]

    phrase_plan = list(plan.get("phrase_plan", []))
    phrase_ids = [str(item["id"]) for item in phrase_plan]
    phrase_structural = Counter(str(item.get("phrase_id")) for item in structural)
    phrase_note_counts = Counter(str(item.get("phrase_id")) for item in events)

    target_ids = {str(item["id"]) for item in plan.get("structural_targets", [])}
    realized_target_ids = {
        str(item["target_id"]) for item in structural if item.get("target_id") is not None
    }
    orphan_surface = [
        item for item in surface
        if item.get("parent_target") is not None and str(item["parent_target"]) not in target_ids
    ]
    surface_without_role = [item for item in surface if not item.get("embellishment_type")]

    motif_phrases: dict[str, set[str]] = defaultdict(set)
    for item in events:
        motif_id = item.get("motif_id")
        phrase_id = item.get("phrase_id")
        if motif_id is not None and phrase_id is not None:
            motif_phrases[str(motif_id)].add(str(phrase_id))
    recurring_motifs = {
        motif_id: sorted(phrases)
        for motif_id, phrases in motif_phrases.items()
        if len(phrases) >= 2
    }

    development_ops = sorted({
        str(item["motif_operation"])
        for item in events
        if item.get("motif_operation") not in {None, "original"}
    })

    overlap_count = 0
    maximum_gap = 0.0
    previous_end: float | None = None
    for item in events:
        start = float(item["start_beat"])
        end = start + float(item["duration_beats"])
        if previous_end is not None:
            if start < previous_end - 1e-6:
                overlap_count += 1
            maximum_gap = max(maximum_gap, max(0.0, start - previous_end))
            previous_end = max(previous_end, end)
        else:
            previous_end = end

    apex = max(pitches)
    apex_index = pitches.index(apex)
    active_start = float(events[0]["start_beat"])
    active_end = float(events[-1]["start_beat"]) + float(events[-1]["duration_beats"])
    active_span = max(1e-9, active_end - active_start)
    apex_position_ratio = (float(events[apex_index]["start_beat"]) - active_start) / active_span

    metrics = {
        "notes": len(events),
        "phrases": len(phrase_ids),
        "structural_notes": len(structural),
        "surface_notes": len(surface),
        "surface_ratio": round(len(surface) / len(events), 3),
        "development_operation_count": len(development_ops),
        "development_operations": development_ops,
        "recurring_motif_families": recurring_motifs,
        "local_motion_le_5_ratio": round(
            (sum(interval <= 5 for interval in intervals) / len(intervals)) if intervals else 1.0,
            3,
        ),
        "large_leaps_ge_7": sum(interval >= 7 for interval in intervals),
        "repeated_pitch_ratio": round(
            (sum(interval == 0 for interval in intervals) / len(intervals)) if intervals else 0.0,
            3,
        ),
        "apex_pitch_midi": apex,
        "apex_position_ratio": round(apex_position_ratio, 3),
        "max_inter_note_gap_beats": round(maximum_gap, 3),
        "monophonic_overlap_count": overlap_count,
        "ornament_counts": dict(Counter(item.get("embellishment_type") for item in surface)),
        "phrase_note_counts": dict(phrase_note_counts),
    }

    checks = {
        "has_notes": bool(events),
        "has_structural_tones": bool(structural),
        "all_phrases_have_structural_tones": all(phrase_structural[phrase_id] > 0 for phrase_id in phrase_ids),
        "all_declared_targets_are_realized": target_ids <= realized_target_ids,
        "surface_notes_reference_known_targets": not orphan_surface,
        "surface_notes_have_embellishment_role": not surface_without_role,
        "motif_identity_recurs_across_phrases": bool(recurring_motifs),
        "has_development_beyond_literal_repeat": bool(development_ops),
        "positive_durations": all(float(item["duration_beats"]) > 0 for item in events),
        "monophonic_foreground_has_no_overlap": overlap_count == 0,
    }

    failures = [name for name, passed in checks.items() if not passed]
    return {
        "schema_version": 1,
        "metrics": metrics,
        "checks": checks,
        "failures": failures,
        "passed": not failures,
        "interpretation": {
            "descriptive_not_normative": [
                "local_motion_le_5_ratio",
                "large_leaps_ge_7",
                "repeated_pitch_ratio",
                "apex_position_ratio",
                "surface_ratio",
                "max_inter_note_gap_beats",
            ],
            "note": (
                "A pass means the declared hierarchy is internally coherent. "
                "It does not prove that the melody sounds good."
            ),
        },
    }
