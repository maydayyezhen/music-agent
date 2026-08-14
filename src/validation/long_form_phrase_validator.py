from __future__ import annotations

import statistics
from collections import Counter
from copy import deepcopy
from typing import Any

from src.accompaniment.generator import materialize_clip
from src.instruments import compile_instrument_phrase
from src.instruments.common import position
from src.midi.pitches import note_number


def _diagnostic(severity: str, code: str, track: str, section: str, message: str, evidence: Any) -> dict[str, Any]:
    return {"severity": severity, "code": code, "track": track, "section": section,
            "message": message, "evidence": evidence}


def analyze_long_form_phrases(composition: dict[str, Any]) -> dict[str, Any]:
    beats = int(str(composition["metadata"]["time_signature"]).split("/")[0])
    reports: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    for track_name, track in composition["tracks"].items():
        for section_name, clip in track.get("sections", {}).items():
            phrase = clip.get("instrument_phrase")
            if not phrase or phrase.get("phrase_generation_mode", "legacy_stable") not in {"long_form_experimental", "long_form"}:
                continue
            if "_long_form_plan" not in phrase:
                compile_instrument_phrase(phrase, beats)
            events = [event for event in materialize_clip(deepcopy(clip), track, beats) if event.get("type", "note") == "note"]
            arc = phrase["section_arc"]; relationships = phrase["phrase_relationships"]
            bars = int(clip["loop_bars"]); rules = phrase["long_form_phrase_rules"]
            onsets = [(position(event["at"], beats), event) for event in events]
            cross_bar = sum(1 for start, event in onsets if start + float(event["duration"]) > (int(start // beats) + 1) * beats + 1e-6)
            peak_pitch = max(note_number(event["pitch"]) for event in events)
            peak_bars = [int(start // beats) + 1 for start, event in onsets if note_number(event["pitch"]) == peak_pitch]
            operations = [operation for rel in relationships for operation in rel.get("motif_operations", [])]
            development_count = sum(rel["relationship"] != "introduce" for rel in relationships)
            resets = sum(1 for index, rel in enumerate(relationships) if index and rel.get("continuation_from") is None)
            strong = [rel for rel in relationships if rel["resolution"] == "strong"]
            boundary_continuations = sum(1 for rel in relationships[:-1]
                                         if rel["resolution"] != "strong" and rel.get("continuation_to"))
            vibrato_bars = [int(start // beats) + 1 for start, event in onsets if "vibrato" in event.get("articulations", [])]
            phrase_lengths = [rel["bars"][1] - rel["bars"][0] + 1 for rel in relationships]
            signatures = Counter()
            for rel in relationships:
                start_beat = (rel["bars"][0] - 1) * beats
                end_beat = rel["bars"][1] * beats
                signature = tuple((round(start - start_beat, 3), note_number(event["pitch"]) - note_number(events[0]["pitch"]),
                                   round(float(event["duration"]), 3)) for start, event in onsets if start_beat <= start < end_beat)
                signatures[signature] += 1
            identical = sum(count - 1 for count in signatures.values() if count > 1)
            full_rest_bars = []
            register_curve = []
            for bar in range(1, bars + 1):
                bar_pitches = [note_number(event["pitch"]) for start, event in onsets
                               if (bar - 1) * beats <= start < bar * beats]
                register_curve.append(statistics.median(bar_pitches) if bar_pitches else None)
                if not bar_pitches:
                    full_rest_bars.append(bar)
            state_trace = phrase.get("_long_form_plan", {}).get("melodic_state_trace", [])
            breath_resets = sum(1 for item in state_trace if item.get("rest_type") == "breath" and not item.get("continuation_required"))
            phrase_ends = {rel["bars"][1] * beats for rel in relationships}
            expressive = [(start, event) for start, event in onsets
                          if set(event.get("articulations", [])) & {"slide", "hammer_on", "pull_off", "bend", "vibrato"}]
            ending_expression = sum(1 for start, event in expressive
                                    if any(abs((start + float(event["duration"])) - end) <= 0.8 for end in phrase_ends))
            articulation_end_ratio = ending_expression / len(expressive) if expressive else 0.0
            longest_rest_run = 0; run = 0
            for bar in range(1, bars + 1):
                run = run + 1 if bar in full_rest_bars else 0
                longest_rest_run = max(longest_rest_run, run)
            metrics = {
                "bars": bars, "average_phrase_length_bars": statistics.mean(phrase_lengths),
                "independent_phrase_resets": resets, "strong_cadences": len(strong),
                "strong_cadence_bars": [rel["bars"][1] for rel in strong],
                "cross_bar_notes": cross_bar, "motif_developments": development_count,
                "motif_operations": sorted(set(operations)), "identical_short_phrase_repetitions": identical,
                "breath_state_resets": breath_resets, "peak_pitch": peak_pitch, "peak_bars": peak_bars,
                "planned_peak_bar": arc["peak_bar"], "vibrato_bars": vibrato_bars,
                "boundary_continuations": boundary_continuations, "full_rest_bars": full_rest_bars,
                "maximum_consecutive_full_rest_bars": longest_rest_run,
                "register_curve_median_midi": register_curve,
                "register_curve_peak_bar": peak_bars[0],
                "articulation_end_concentration_ratio": articulation_end_ratio,
                "relationship_counts": dict(Counter(rel["relationship"] for rel in relationships)),
                "continuous_narrative_bars": arc["bars"][1] - arc["bars"][0] + 1 if boundary_continuations == len(relationships) - 1 else max(phrase_lengths),
                "sees_full_section_harmony": len(phrase.get("harmony", [])) >= bars,
            }
            reports.append({"track": track_name, "section": section_name, "assessment": metrics,
                            "section_arc": deepcopy(arc), "phrase_relationships": deepcopy(relationships),
                            "melodic_state_trace": deepcopy(state_trace)})
            minimum_cross = int(rules.get("minimum_cross_bar_notes_per_8_bars", 2)) * max(1, bars // 8)
            if cross_bar < minimum_cross:
                diagnostics.append(_diagnostic("warning", "too_few_cross_bar_notes", track_name, section_name,
                                               "too few notes connect across bar lines", {"actual": cross_bar, "target": minimum_cross}))
            if development_count < int(rules.get("minimum_motif_developments_per_section", 3)):
                diagnostics.append(_diagnostic("warning", "insufficient_motif_development", track_name, section_name,
                                               "motif is introduced but insufficiently developed", development_count))
            if resets > int(rules.get("maximum_independent_phrase_resets_per_8_bars", 1)) * max(1, bars // 8):
                diagnostics.append(_diagnostic("warning", "excessive_phrase_resets", track_name, section_name,
                                               "too many subphrases restart without a relationship", resets))
            if len(strong) > int(rules.get("maximum_strong_cadences_per_8_bars", 1)) * max(1, bars // 8):
                diagnostics.append(_diagnostic("warning", "excessive_strong_cadences", track_name, section_name,
                                               "too many strong endings inside one arc", metrics["strong_cadence_bars"]))
            if rules.get("require_delayed_peak", True) and min(peak_bars) < max(3, bars // 2):
                diagnostics.append(_diagnostic("warning", "early_peak", track_name, section_name,
                                               "highest pitch arrives before the long-form build matures", peak_bars))
            if arc["final_resolution_bar"] != bars or any(rel["resolution"] == "strong" for rel in relationships[:-1]):
                diagnostics.append(_diagnostic("warning", "resolution_not_delayed", track_name, section_name,
                                               "strong resolution occurs before the planned final bar", metrics["strong_cadence_bars"]))
            if boundary_continuations < len(relationships) - 1:
                diagnostics.append(_diagnostic("warning", "broken_relationship_graph", track_name, section_name,
                                               "one or more phrase boundaries discard unresolved state", boundary_continuations))
            if identical:
                diagnostics.append(_diagnostic("warning", "identical_short_phrase", track_name, section_name,
                                               "short phrase signatures repeat without transformation", identical))
            if breath_resets:
                diagnostics.append(_diagnostic("warning", "breath_resets_state", track_name, section_name,
                                               "a breath incorrectly resets melodic continuation", breath_resets))
            if len(vibrato_bars) >= max(2, len(relationships) - 1):
                diagnostics.append(_diagnostic("warning", "automatic_vibrato_endings", track_name, section_name,
                                               "vibrato is concentrated at local phrase endings", vibrato_bars))
            if not metrics["sees_full_section_harmony"]:
                diagnostics.append(_diagnostic("warning", "local_harmony_window", track_name, section_name,
                                               "planner does not receive the complete section harmony", len(phrase.get("harmony", []))))
            if longest_rest_run > int(rules.get("maximum_consecutive_full_rest_bars", 1)):
                diagnostics.append(_diagnostic("warning", "excessive_structural_silence", track_name, section_name,
                                               "full-bar silence breaks the planned narrative", longest_rest_run))
            if peak_bars[0] != int(arc["peak_bar"]):
                diagnostics.append(_diagnostic("warning", "register_curve_misses_peak", track_name, section_name,
                                               "actual highest register does not match planned peak bar", {"actual": peak_bars, "planned": arc["peak_bar"]}))
            if articulation_end_ratio > 0.75 and len(expressive) >= len(relationships):
                diagnostics.append(_diagnostic("warning", "articulation_concentrated_at_endings", track_name, section_name,
                                               "expressive actions act mostly as phrase punctuation", round(articulation_end_ratio, 3)))
    return {"schema_version": 1, "title": composition["metadata"]["title"], "sections": reports,
            "diagnostics": diagnostics,
            "error_count": sum(item["severity"] == "error" for item in diagnostics),
            "warning_count": sum(item["severity"] == "warning" for item in diagnostics)}
