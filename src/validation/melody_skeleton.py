from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import mido

from src.midi.pitches import note_number


def validate_melody_skeleton(plan: dict[str, Any], notes: list[dict[str, Any]], midi_path: Path) -> dict[str, Any]:
    events = sorted(notes, key=lambda item: float(item["start_beat"]))
    overlaps = 0
    longest_silence = 0.0
    previous_end = 0.0
    for event in events:
        start = float(event["start_beat"]); end = start + float(event["duration_beats"])
        if start < previous_end - 1e-6: overlaps += 1
        longest_silence = max(longest_silence, max(0.0, start - previous_end))
        previous_end = max(previous_end, end)
    longest_silence = max(longest_silence, 32.0 - previous_end)
    pitches = [note_number(event["pitch"]) for event in events]
    peak = max(pitches)
    peak_bar = min(int(float(event["start_beat"]) // 4) + 1 for event, pitch in zip(events, pitches) if pitch == peak)
    cross_reasoned = sum(
        int(float(event["start_beat"]) // 4) != int((float(event["start_beat"]) + float(event["duration_beats"]) - 1e-6) // 4)
        and bool(event.get("cross_bar_reason")) for event in events
    )
    motif_occurrences = sum(
        item.get("function") in {"introduce", "develop", "expand", "climax_and_resolve"}
        for item in plan["phrase_plan"]
    )
    developments = len({event.get("motif_operation") for event in events if event.get("motif_operation") not in {None, "original"}})
    resets = sum(1 for item in plan["phrase_plan"][1:-1] if item.get("reset_state", False))
    unrelated = sum(1 for event in events if event.get("motif_id") != plan["motif"]["id"])
    premature_strong = sum(1 for item in plan["phrase_plan"][:-1] if item.get("resolution") == "strong")

    active: set[tuple[int, int]] = set(); polyphonic = 0; pitch_bends = 0; keyswitches = 0; random_cc = 0
    for track in mido.MidiFile(midi_path).tracks:
        for message in track:
            if message.type == "pitchwheel": pitch_bends += 1
            elif message.type == "control_change" and message.control not in {0, 32}: random_cc += 1
            elif message.type == "note_on" and message.velocity > 0:
                key = (message.channel, message.note)
                if message.note < 36: keyswitches += 1
                active.add(key)
                if len(active) > 1: polyphonic += 1
            elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                active.discard((message.channel, message.note))

    metrics = {
        "bars": 8, "monophonic": overlaps == 0 and polyphonic == 0,
        "independent_phrase_resets": resets, "strong_cadences_before_bar_8": premature_strong,
        "primary_motif_occurrences": motif_occurrences, "motif_developments": developments,
        "unrelated_phrase_fragments": unrelated, "longest_silence_beats": round(longest_silence, 3),
        "peak_bar": peak_bar, "final_resolution_bar": plan["section"]["arc"]["resolution_bar"],
        "pitch_bends": pitch_bends, "overlapping_different_pitches": overlaps + polyphonic,
        "articulation_keyswitches": keyswitches, "random_cc": random_cc,
        "cross_bar_notes_with_explicit_reason": cross_reasoned,
        "unreasoned_long_sustains": sum(float(event["duration_beats"]) > 4 and not event.get("cross_bar_reason") for event in events),
    }
    failures = []
    checks = {
        "monophonic": metrics["monophonic"], "no_independent_resets": resets <= 1,
        "no_premature_strong_cadence": premature_strong <= 1, "motif_occurs_three_times": motif_occurrences >= 3,
        "two_development_types": developments >= 2, "no_unrelated_fragments": unrelated == 0,
        "delayed_peak": peak_bar > 2, "resolves_in_bar_8": metrics["final_resolution_bar"] == 8,
        "no_pitch_bend": pitch_bends == 0, "no_overlap": metrics["overlapping_different_pitches"] == 0,
        "no_keyswitch": keyswitches == 0, "no_random_cc": random_cc == 0,
        "silence_under_one_bar": longest_silence <= 4.0, "no_unreasoned_long_sustain": metrics["unreasoned_long_sustains"] == 0,
    }
    failures = [name for name, passed in checks.items() if not passed]
    return {"schema_version": 1, "metrics": metrics, "checks": checks, "failures": failures,
            "passed": not failures,
            "conclusion": ("The melody behaves as one developing eight-bar paragraph."
                           if not failures else "The melody still behaves as disconnected short fragments.")}
