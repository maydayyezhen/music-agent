from __future__ import annotations

import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parent
SOURCE_PATH = ROOT.parent / "comfortably_numb_midi_reconstruction" / "build_project.py"
TPB = 480
TOTAL_TICKS = 48 * TPB
NOTE_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


def load_source_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("comfortably_numb_source", SOURCE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load source table: {SOURCE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def absolute_notes(module: ModuleType, blob: str) -> list[dict[str, int]]:
    start_tick = 0
    result: list[dict[str, int]] = []
    for delta_tick, duration_tick, pitch, velocity in module.unpack(blob):
        start_tick += int(delta_tick)
        result.append({
            "start_tick": start_tick,
            "duration_tick": int(duration_tick),
            "pitch": int(pitch),
            "source_velocity": int(velocity),
        })
    return result


def number(value: float) -> float:
    return float(f"{value:.6f}".rstrip("0").rstrip("."))


def position(tick: int) -> str:
    total_beats = tick / TPB
    bar = int(total_beats // 4) + 1
    beat = total_beats % 4 + 1
    beat_text = f"{beat:.6f}".rstrip("0").rstrip(".")
    return f"{bar}:{beat_text}"


def note_name(pitch: int) -> str:
    return f"{NOTE_NAMES[pitch % 12]}{pitch // 12 - 1}"


def infer_lead_motif(notes: list[dict[str, int]]) -> tuple[list[dict[str, Any]], Counter[str]]:
    motif: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for index, source in enumerate(notes):
        previous = notes[index - 1] if index else None
        following = notes[index + 1] if index + 1 < len(notes) else None
        start_tick = source["start_tick"]
        duration_tick = source["duration_tick"]
        duration = duration_tick / TPB
        previous_end = (
            previous["start_tick"] + previous["duration_tick"]
            if previous is not None else None
        )
        gap_before = (
            (start_tick - previous_end) / TPB
            if previous_end is not None else 99.0
        )
        current_end = start_tick + duration_tick
        gap_after = (
            (following["start_tick"] - current_end) / TPB
            if following is not None else 99.0
        )
        interval = source["pitch"] - previous["pitch"] if previous is not None else 0

        articulations: list[str]
        slide_from: float | None = None
        if previous is None or gap_before >= 0.45:
            articulations = ["pick", "accent"]
        elif interval == 0:
            articulations = ["pick"]
            if duration >= 0.45:
                articulations.append("tenuto")
        elif gap_before <= 0.06 and abs(interval) <= 2:
            articulations = [
                "hammer_on" if interval > 0 else "pull_off",
                "legato",
            ]
        elif gap_before <= 0.10 and 2 < abs(interval) <= 5 and duration >= 0.20:
            articulations = ["slide", "legato"]
            slide_from = float(-interval)
        else:
            articulations = ["pick"]

        is_landing = gap_after >= 0.65 and duration >= 0.45
        if duration >= 0.75 or is_landing:
            if "sustain" not in articulations:
                articulations.append("sustain")
            if "vibrato" not in articulations:
                articulations.append("vibrato")
        if duration <= 0.13 and gap_before <= 0.10:
            articulations.append("grace_note")

        item: dict[str, Any] = {
            "pitch": note_name(source["pitch"]),
            "at": position(start_tick),
            "duration": number(duration),
            "articulations": articulations,
        }
        if slide_from is not None:
            item["slide_from_semitones"] = slide_from
        if "vibrato" in articulations:
            item["vibrato"] = {
                "delay": number(min(0.42, max(0.18, duration * 0.32))),
                "depth": 0.24 if duration < 1.5 else 0.32,
                "rate": 4.8,
            }
        motif.append(item)
        counts.update(articulations)
    return motif, counts


def infer_chord(pitches: list[int]) -> str:
    pitch_classes = {pitch % 12 for pitch in pitches}
    bass_class = min(pitches) % 12
    candidates: list[tuple[float, int, str]] = []
    for root in range(12):
        for quality, intervals, prior in (
            ("", {0, 4, 7}, 0.15),
            ("m", {0, 3, 7}, 0.0),
        ):
            triad = {(root + interval) % 12 for interval in intervals}
            score = (
                4.0 * len(pitch_classes & triad)
                - 3.0 * len(triad - pitch_classes)
                - 0.8 * len(pitch_classes - triad)
                + (1.5 if bass_class == root else 0.0)
                + (0.5 if root in pitch_classes else 0.0)
                + prior
            )
            candidates.append((score, root, quality))
    _, root, quality = max(candidates)
    return f"{NOTE_NAMES[root]}{quality}"


def infer_harmony(notes: list[dict[str, int]]) -> list[dict[str, Any]]:
    onsets: dict[int, list[int]] = defaultdict(list)
    for note in notes:
        onsets[note["start_tick"]].append(note["pitch"])

    chord_at_tick = [
        (tick, infer_chord(pitches))
        for tick, pitches in sorted(onsets.items())
    ]
    changes: list[tuple[int, str]] = []
    for tick, chord in chord_at_tick:
        if not changes or changes[-1][1] != chord:
            changes.append((tick, chord))

    harmony: list[dict[str, Any]] = []
    for index, (tick, chord) in enumerate(changes):
        end_tick = changes[index + 1][0] if index + 1 < len(changes) else TOTAL_TICKS
        if end_tick <= tick:
            continue
        harmony.append({
            "at": position(tick),
            "duration": number((end_tick - tick) / TPB),
            "chord": chord,
        })
    return harmony


def main() -> None:
    source = load_source_module()
    lead_notes = absolute_notes(source, source.LEAD_B85)
    rhythm_notes = absolute_notes(source, source.RHYTHM_B85)
    motif, articulation_counts = infer_lead_motif(lead_notes)
    harmony = infer_harmony(rhythm_notes)

    composition = {
        "metadata": {
            "title": "Comfortably Numb Agent Performance Reconstruction",
            "tempo": 60_000_000 / source.TEMPO_US_PER_BEAT,
            "time_signature": "4/4",
            "key": "D major with borrowed C",
            "description": (
                "Semantic reconstruction test. Source lead pitches and onsets are "
                "used as the score skeleton, while velocity, string/fret assignment, "
                "articulation realization, rhythm-guitar notes, voicings and thinning "
                "are produced by the current agent performance pipeline."
            ),
        },
        "sections": [{"name": "solo", "bars": 12}],
        "tracks": {
            "lead_guitar": {
                "role": "foreground lead melody reconstructed from reference phrasing",
                "sections": {
                    "solo": {
                        "loop_bars": 12,
                        "sound_library_profile": "general_midi",
                        "instrument_phrase": {
                            "instrument": "electric_lead_guitar",
                            "role": "expressive semantic lead",
                            "phrase_type": "melodic_lead",
                            "energy": 0.72,
                            "motif": motif,
                            "performance_intent": {
                                "attack": "picked phrase starts with connected inner notes",
                                "release": "landings sustain and receive delayed vibrato",
                                "humanization": "articulation_driven",
                                "source": "reference MIDI phrasing skeleton",
                            },
                        },
                    }
                },
            },
            "rhythm_guitar": {
                "role": "agent-regenerated supporting rhythm guitar",
                "sections": {
                    "solo": {
                        "loop_bars": 12,
                        "sound_library_profile": "general_midi",
                        "instrument_phrase": {
                            "instrument": "electric_rhythm_guitar",
                            "role": "continuous sixteenth-note harmonic support",
                            "section_function": "solo_support",
                            "phrase_type": "continuous_strumming",
                            "energy": 0.63,
                            "subdivision": "sixteenth",
                            "strumming_pattern": "sixteenth_flow",
                            "four_bar_variation": True,
                            "foreground_aware": True,
                            "gate": 0.76,
                            "strum_spread": 0.038,
                            "harmony": harmony,
                            "performance_intent": {
                                "picking": "continuous alternate hand motion",
                                "attack": "thin under active lead phrases",
                                "release": "retain motion across harmony boundaries",
                                "humanization": "action_based",
                                "seed": 8142026,
                            },
                        },
                    }
                },
            },
        },
    }

    (ROOT / "composition.json").write_text(
        json.dumps(composition, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = {
        "source_lead_notes": len(lead_notes),
        "source_rhythm_notes": len(rhythm_notes),
        "lead_motif_notes": len(motif),
        "inferred_articulations": dict(sorted(articulation_counts.items())),
        "inferred_harmony": harmony,
        "explicit_event_tracks": 0,
        "semantic_instrument_phrase_tracks": 2,
        "important_limitations": [
            "The lead score skeleton still preserves reference pitches and onsets.",
            "The source MIDI contains no bends, CC, aftertouch or articulation labels, so those are inferred heuristically.",
            "The current electric rhythm compiler realizes power-chord-oriented voicings rather than the source MIDI's exact full chord stacks.",
            "The output is an agent interpretation, not a tick-identical reconstruction.",
        ],
    }
    (ROOT / "semantic-analysis.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] wrote {ROOT / 'composition.json'}")
    print(f"[OK] lead semantic notes={len(motif)}")
    print(f"[OK] inferred harmony spans={len(harmony)}")
    print(f"[OK] articulations={dict(sorted(articulation_counts.items()))}")
    print("[OK] both tracks use instrument_phrase; no explicit event track is present")


if __name__ == "__main__":
    main()
