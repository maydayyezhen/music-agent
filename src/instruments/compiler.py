from __future__ import annotations

from copy import deepcopy
from typing import Any


def compile_instrument_phrase(phrase: dict[str, Any], beats_per_bar: int) -> list[dict[str, Any]]:
    instrument = str(phrase.get("instrument", "")).lower()
    if instrument in {"electric_guitar", "electric_rhythm_guitar", "electric_lead_guitar", "acoustic_guitar", "steel_guitar", "nylon_guitar"}:
        from .electric_guitar import compile_phrase
    elif instrument in {"electric_bass", "bass"}:
        from .electric_bass import compile_phrase
    elif instrument in {"drum_kit", "drums"}:
        from .drums import compile_phrase
    elif instrument in {"piano", "organ", "keyboard", "keyboards"}:
        from .keyboards import compile_phrase
    elif instrument in {"strings", "string_ensemble", "pad"}:
        from .strings import compile_phrase
    else:
        raise ValueError(f"unsupported instrument_phrase instrument: {instrument!r}")
    if phrase.get("phrase_generation_mode") in {"long_form_experimental", "long_form"}:
        # The compiler receives a copy so composition remains declarative; expose the
        # generated state trace for validators and artifact export on the source object.
        copied = deepcopy(phrase)
        events = compile_phrase(copied, beats_per_bar)
        if copied.get("_long_form_plan"):
            phrase["_long_form_plan"] = copied["_long_form_plan"]
    else:
        copied = deepcopy(phrase)
        events = compile_phrase(copied, beats_per_bar)
        if copied.get("_strumming_debug"):
            phrase["_strumming_debug"] = copied["_strumming_debug"]
        if copied.get("_per_string_state_debug"):
            phrase["_per_string_state_debug"] = copied["_per_string_state_debug"]
        if copied.get("_four_bar_variation_debug"):
            phrase["_four_bar_variation_debug"] = copied["_four_bar_variation_debug"]
    for event in events:
        event["_semantic_instrument"] = instrument
        event["_phrase_type"] = phrase["phrase_type"]
    return events


def export_semantic_phrases(composition: dict[str, Any]) -> dict[str, Any]:
    phrases = []
    for track_name, track in composition.get("tracks", {}).items():
        for section_name, clip in track.get("sections", {}).items():
            phrase = clip.get("instrument_phrase")
            if phrase:
                phrases.append({"track": track_name, "section": section_name, **deepcopy(phrase)})
    return {"schema_version": 1, "title": composition.get("metadata", {}).get("title"), "phrases": phrases}


def export_long_form_plans(composition: dict[str, Any], beats_per_bar: int) -> dict[str, Any]:
    plans = []
    for track_name, track in composition.get("tracks", {}).items():
        for section_name, clip in track.get("sections", {}).items():
            phrase = clip.get("instrument_phrase")
            if not phrase or phrase.get("phrase_generation_mode") not in {"long_form_experimental", "long_form"}:
                continue
            compile_instrument_phrase(phrase, beats_per_bar)
            plan = phrase.get("_long_form_plan")
            if plan:
                plans.append({"track": track_name, "section": section_name, **deepcopy(plan)})
    return {"schema_version": 1, "title": composition.get("metadata", {}).get("title"), "plans": plans}
