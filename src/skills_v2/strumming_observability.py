from __future__ import annotations

from copy import deepcopy
from statistics import median
from typing import Any, Mapping


DEFAULT_MIN_DIRECTION_SPREAD_BEATS = 0.008


def annotate_direction_observability(
    analysis: Mapping[str, Any],
    *,
    min_direction_spread_beats: float = DEFAULT_MIN_DIRECTION_SPREAD_BEATS,
) -> dict[str, Any]:
    """Annotate whether stroke direction is actually observable in the MIDI.

    A quantized block-chord MIDI can preserve attack rhythm, voicing, velocity,
    and duration while containing no within-stroke onset order. In that case the
    analyzer must not promote an alternating-hand assumption into learned data.
    """

    result = deepcopy(dict(analysis))
    strokes = list(result.get("strokes", []))
    multi_note = [stroke for stroke in strokes if len(stroke.get("pitches", [])) >= 3]
    measurable = [
        stroke
        for stroke in multi_note
        if float(stroke.get("spread_beats", 0.0))
        >= min_direction_spread_beats
    ]
    zero_spread = [
        stroke
        for stroke in multi_note
        if abs(float(stroke.get("spread_beats", 0.0))) <= 1e-12
    ]
    spreads = [float(stroke.get("spread_beats", 0.0)) for stroke in multi_note]

    if not multi_note:
        status = "no_chordal_strokes"
    elif not measurable:
        status = "unobservable_quantized_onsets"
    elif len(measurable) / len(multi_note) < 0.10:
        status = "weak_partial_evidence"
    else:
        status = "observable"

    observability = {
        "status": status,
        "minimum_measurable_spread_beats": min_direction_spread_beats,
        "multi_note_strokes": len(multi_note),
        "measurable_direction_strokes": len(measurable),
        "zero_spread_strokes": len(zero_spread),
        "zero_spread_ratio": round(
            len(zero_spread) / len(multi_note), 4
        )
        if multi_note
        else 0.0,
        "median_spread_beats": round(median(spreads), 6) if spreads else 0.0,
        "maximum_spread_beats": round(max(spreads), 6) if spreads else 0.0,
        "learned_fields": [
            "attack grid",
            "relative velocity",
            "voicing coverage",
            "note duration and overlap",
        ],
        "unlearned_fields": (
            ["down/up direction", "sweep timing"]
            if status != "observable"
            else []
        ),
    }
    result["observability"] = {"direction": observability}

    model = result["model"]
    model.setdefault("evidence", {}).update(
        {
            "direction_observability": status,
            "multi_note_strokes": len(multi_note),
            "measurable_direction_strokes": len(measurable),
            "zero_spread_strokes": len(zero_spread),
            "zero_spread_ratio": observability["zero_spread_ratio"],
            "median_spread_beats": observability["median_spread_beats"],
            "maximum_spread_beats": observability["maximum_spread_beats"],
        }
    )
    model["motion"]["direction_observability"] = status

    if status == "unobservable_quantized_onsets":
        model["technique"] = (
            "continuous_eighth_chord_attacks_direction_unobserved"
        )
        model["motion"].update(
            {
                "type": "unknown",
                "slot_zero_direction": "unknown",
                "continuous_motion": False,
                "cross_bar_continuity": False,
                "alternate_direction_confidence": 0.0,
            }
        )
        for profile in model.get("slot_profiles", []):
            profile["expected_direction"] = "unknown"
        model["invariance_fingerprint"]["slot_zero_direction"] = "unknown"
        model["limitations"].append(
            "Every multi-note stroke is onset-quantized; down/up direction and sweep timing are not observable in this source."
        )

    return result


def can_generate_directional_demo(model: Mapping[str, Any]) -> bool:
    return (
        model.get("motion", {}).get("direction_observability")
        == "observable"
    )


def apply_alternate_generation_assumption(
    model: Mapping[str, Any],
    *,
    slot_zero_direction: str = "down",
) -> dict[str, Any]:
    """Prepare an unobservable model for an explicitly assumed D/U demo.

    This does not change the stored study model. It is only a rendering-time
    assumption and must never be presented as source-derived evidence.
    """

    if slot_zero_direction not in {"down", "up"}:
        raise ValueError("slot_zero_direction must be 'down' or 'up'")
    result = deepcopy(dict(model))
    result["motion"]["type"] = "alternate"
    result["motion"]["slot_zero_direction"] = slot_zero_direction
    result["motion"]["generation_assumption"] = "alternate_down_up_not_learned"
    for profile in result.get("slot_profiles", []):
        slot = int(profile["slot"])
        direction = slot_zero_direction if slot % 2 == 0 else (
            "up" if slot_zero_direction == "down" else "down"
        )
        profile["expected_direction"] = direction
    return result
