from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from _bootstrap import ROOT
from src.midi.pitches import note_number


SOURCE = ROOT / "projects" / "benchmarks" / "01_galgame"
DEMO = ROOT / "projects" / "accompaniment_continuity_demo"


HARMONY = {
    "intro": [("D3", "F#3", "A3"), ("C#3", "E3", "A3"), ("B2", "D3", "F#3"), ("G2", "B2", "D3")],
    "a": [("D3", "F#3", "A3"), ("C#3", "E3", "A3"), ("B2", "D3", "F#3"), ("G2", "B2", "D3"), ("F#2", "A2", "D3"), ("F#2", "A2", "C#3"), ("E2", "G2", "B2"), ("A2", "C#3", "E3", "G3")],
    "b": [("B2", "D3", "F#3"), ("A2", "C#3", "F#3"), ("G2", "B2", "D3", "F#3"), ("F#2", "A2", "D3"), ("E2", "G2", "B2", "D3"), ("D2", "F#2", "B2"), ("G2", "B2", "D3"), ("A2", "C#3", "E3", "G3")],
    "return": [("D3", "F#3", "A3"), ("C#3", "E3", "A3"), ("B2", "D3", "F#3"), ("G2", "B2", "D3"), ("E2", "G2", "B2"), ("A2", "C#3", "E3", "G3")],
    "outro": [("D3", "F#3", "A3"), ("D3", "F#3", "A3")],
}


def spans(section: str) -> list[dict]:
    return [
        {"at": f"{bar}:1", "duration": 4.0, "pitches": list(chord)}
        for bar, chord in enumerate(HARMONY[section], start=1)
    ]


def melody_only(clip: dict) -> list[dict]:
    # The source piano combines melody and accompaniment. Its intended melody
    # is the voiced single-note material at/above D4; lower quiet notes and
    # chord events are accompaniment. Values are copied byte-for-byte at event
    # level: pitch, onset, duration, and velocity never change.
    return [
        deepcopy(event)
        for event in clip.get("events", [])
        if event.get("type", "note") == "note"
        and note_number(event["pitch"]) >= note_number("D4")
        and int(event["velocity"]) >= 62
    ]


def generated_clip(
    section: str,
    texture: str,
    pattern: dict,
    explicit_events: list[dict] | None = None,
    continuity: dict | None = None,
) -> dict:
    clip = {
        "loop_bars": len(HARMONY[section]),
        "texture": texture,
        "harmony_spans": spans(section),
        "texture_pattern": pattern,
        "events": explicit_events or [],
    }
    if continuity:
        clip["continuity"] = continuity
    return clip


def build_after(source: dict) -> dict:
    composition = deepcopy(source)
    composition["metadata"]["title"] = "Platform Afterglow - After Continuity"
    composition["metadata"]["version"] = "after_continuity"
    composition["complexity"] = "standard"

    piano_source = source["tracks"]["piano"]["sections"]
    composition["tracks"]["piano"] = {
        "role": "lead melody + piano accompaniment",
        "continuity": {"common_tone_retention": 0.85, "voice_leading_strength": 0.90},
        "sections": {
            "intro": generated_clip("intro", "sustain", {"register": [55, 72], "voices": 3, "velocity": 48}, melody_only(piano_source["intro"])),
            "a": generated_clip("a", "broken_chord", {"register": [52, 72], "voices": 3, "velocity": 53, "indices": [0, 1, 2, 1, 0], "step": 0.8}, melody_only(piano_source["a"])),
            "b": generated_clip("b", "pulse", {"register": [55, 74], "voices": 3, "velocity": 57, "offsets": [0, 1.5, 3.25], "durations": [1.05, 0.55, 0.45], "accents": [1.0, 0.82, 0.9]}, melody_only(piano_source["b"])),
            "return": generated_clip("return", "broken_chord", {"register": [52, 72], "voices": 3, "velocity": 50, "indices": [0, 2, 1, 2], "step": 1.0}, melody_only(piano_source["return"])),
            "outro": generated_clip("outro", "sustain", {"register": [55, 74], "voices": 3, "velocity": 44}, melody_only(piano_source["outro"])),
        },
    }

    composition["tracks"]["bass"] = {
        "role": "continuous bass line",
        "texture": "counterline",
        "continuity": {"sustain_ratio": 0.55, "legato_ratio": 0.62, "overlap": 0.03},
        "texture_pattern": {"bass_line": True, "register": [31, 48], "voices": 3, "velocity": 66},
        "sections": {
            section: generated_clip(section, "counterline", {"bass_line": True, "register": [31, 48], "voices": 3, "velocity": 65 if section in {"intro", "outro"} else (72 if section == "b" else 68)})
            for section in HARMONY
        },
    }

    composition["tracks"]["guitar"] = {
        "role": "clean guitar held harmony / offbeat response / broken chord",
        "continuity": {"voice_leading_strength": 0.78, "common_tone_retention": 0.72},
        "sections": {
            "a": generated_clip("a", "sustain", {"register": [52, 69], "voices": 3, "velocity": 48, "strum_spread": 0.035}, continuity={"sustain_ratio": 0.82, "overlap": 0.03}),
            "b": generated_clip("b", "pulse", {"register": [52, 71], "voices": 3, "velocity": 56, "offsets": [0.5, 2.5], "durations": [0.65, 0.85], "accents": [0.86, 1.0]}),
            "return": generated_clip("return", "broken_chord", {"register": [52, 69], "voices": 3, "velocity": 49, "indices": [0, 1, 2, 1], "step": 1.0}),
            "outro": generated_clip("outro", "sustain", {"register": [55, 71], "voices": 3, "velocity": 43, "strum_spread": 0.045}, continuity={"sustain_ratio": 0.9, "overlap": 0.04}),
        },
    }

    composition["tracks"]["strings"] = {
        "role": "counterline then sustained inner voices",
        "continuity": {"legato_ratio": 0.78, "voice_leading_strength": 0.9, "common_tone_retention": 0.82},
        "sections": {
            "b": generated_clip("b", "counterline", {"register": [62, 79], "voices": 4, "velocity": 47, "offsets": [0.5, 2.0, 3.25], "durations": [1.55, 1.3, 0.75]}),
            "return": generated_clip("return", "sustain", {"register": [60, 77], "voices": 4, "velocity": 43}, continuity={"sustain_ratio": 0.92, "overlap": 0.08}),
        },
    }

    composition["tracks"]["pad"] = {
        "role": "sustained harmonic plane",
        "texture": "sustain",
        "continuity": {"sustain_ratio": 0.96, "legato_ratio": 0.92, "overlap": 0.08, "common_tone_retention": 0.95, "voice_leading_strength": 0.95},
        "texture_pattern": {"register": [55, 76], "voices": 4, "velocity": 36},
        "sections": {
            section: generated_clip(section, "sustain" if section != "outro" else "pedal", {"register": [55, 76], "voices": 4, "velocity": 34 if section in {"intro", "outro"} else (42 if section == "b" else 37), **({"pitch": "A3"} if section == "outro" else {})})
            for section in HARMONY
        },
    }

    # Drums remain exactly the original point layer.
    composition["tracks"]["drums"]["role"] = "drum groove / point"
    composition["tracks"]["drums"]["texture"] = "pulse"
    return composition


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    source = json.loads((SOURCE / "composition.json").read_text(encoding="utf-8"))
    before = deepcopy(source)
    before["metadata"]["title"] = "Platform Afterglow - Before Continuity"
    before["metadata"]["version"] = "before_continuity"
    after = build_after(source)

    instruments = json.loads((SOURCE / "instruments.json").read_text(encoding="utf-8"))
    render = json.loads((SOURCE / "render.json").read_text(encoding="utf-8"))
    for name, composition in (("before_continuity", before), ("after_continuity", after)):
        folder = DEMO / name
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / "composition.json", composition)
        write_json(folder / "instruments.json", instruments)
        write_json(folder / "render.json", render)
    (DEMO / "README.md").write_text(
        "# Galgame standard accompaniment continuity A/B\n\n"
        "Both versions keep 92 BPM, D major, 28 bars, form, instrument programs, harmony, and the source piano melody. "
        "Only accompaniment construction changes.\n",
        encoding="utf-8",
    )
    print(f"[OK] Built before/after compositions in {DEMO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
