from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT.name

TEMPO = 124
SECTIONS = [
    ("intro", 4, 0.28),
    ("verse_1", 12, 0.48),
    ("pre_1", 6, 0.62),
    ("chorus_1", 12, 0.82),
    ("verse_2", 12, 0.54),
    ("pre_2", 6, 0.68),
    ("chorus_2", 12, 0.86),
    ("bridge", 8, 0.58),
    ("final_chorus", 16, 0.94),
    ("outro", 4, 0.30),
]

CHORDS = {
    "intro": ["Bm", "G", "D", "A"],
    "verse_1": ["Bm", "G", "D", "A", "Bm", "G", "D", "A", "Em", "G", "D", "A"],
    "pre_1": ["G", "A", "Bm", "Bm", "G", "A"],
    "chorus_1": ["D", "A", "Bm", "G", "D", "A", "G", "G", "Bm", "A", "G", "A"],
    "verse_2": ["Bm", "G", "D", "A", "Bm", "G", "D", "A", "Em", "G", "A", "A"],
    "pre_2": ["G", "A", "Bm", "Bm", "G", "A"],
    "chorus_2": ["D", "A", "Bm", "G", "D", "A", "G", "G", "Bm", "A", "G", "A"],
    "bridge": ["Em", "Bm", "G", "D", "Em", "Bm", "G", "A"],
    "final_chorus": ["D", "A", "Bm", "G", "D", "A", "Bm", "G", "Bm", "A", "G", "D", "G", "A", "D", "D"],
    "outro": ["Bm", "G", "A", "D"],
}

SECTION_BARS = {name: bars for name, bars, _ in SECTIONS}
SECTION_ENERGY = {name: energy for name, _, energy in SECTIONS}

# This used to be the vocal topline. It is now instrument-only melodic data:
# absolute start beat, pitch sequence, duration sequence. Repeated adjacent notes
# are merged below so the clean guitar phrases breathe like guitar rather than
# re-articulating every former lyric syllable.
MELODY_PHRASES: list[tuple[float, list[str], list[float]]] = [
    (20, ["F#4", "F#4", "A4", "B4", "A4", "F#4", "E4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
    (30, ["F#4", "A4", "B4", "D5", "B4", "A4", "F#4"], [0.5, 0.75, 0.5, 1.0, 0.75, 0.5, 1.5]),
    (40, ["E4", "F#4", "A4", "B4", "A4", "F#4", "E4", "F#4", "D4"], [0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 1.5]),
    (50, ["F#4", "A4", "B4", "A4", "D5", "B4", "A4"], [0.5, 0.5, 0.75, 0.5, 1.25, 0.75, 1.75]),
    (66, ["G4", "A4", "B4", "B4", "A4", "G4", "A4", "B4"], [0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 1.0, 1.5]),
    (74, ["A4", "B4", "D5", "B4", "A4", "B4"], [0.5, 0.5, 1.0, 0.75, 0.5, 2.0]),
    (82, ["B4", "D5", "E5", "D5", "B4", "A4"], [0.5, 0.5, 0.75, 1.0, 0.5, 2.0]),
    (90, ["A4", "A4", "B4", "D5", "D5", "B4", "A4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
    (98, ["F#4", "A4", "B4", "D5", "B4", "A4", "F#4", "E4"], [0.5, 0.5, 0.75, 0.75, 0.75, 0.5, 0.5, 1.25]),
    (106, ["A4", "B4", "D5", "E5", "D5", "B4"], [0.5, 0.5, 0.75, 0.75, 0.75, 2.0]),
    (114, ["F#4", "A4", "B4", "D5", "E5", "D5"], [0.5, 0.5, 1.0, 0.5, 1.0, 2.0]),
    (122, ["B4", "D5", "E5", "D5", "B4", "A4"], [0.75, 0.75, 0.5, 1.0, 0.75, 1.75]),
    (130, ["A4", "B4", "D5", "E5", "D5", "D5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
    (140, ["F#4", "A4", "B4", "A4", "F#4", "E4", "F#4", "D4"], [0.5, 0.5, 0.75, 1.0, 0.5, 0.5, 0.75, 1.5]),
    (150, ["F#4", "A4", "B4", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.5]),
    (160, ["E4", "F#4", "A4", "B4", "A4", "F#4", "A4", "B4"], [0.5, 0.5, 1.0, 0.75, 0.5, 0.5, 0.5, 1.5]),
    (170, ["F#4", "A4", "B4", "A4", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 0.75, 0.5, 1.0, 0.75, 0.75, 1.5]),
    (186, ["G4", "A4", "B4", "D5", "B4", "A4", "B4"], [0.75, 0.5, 0.5, 1.0, 0.5, 0.75, 1.75]),
    (194, ["A4", "B4", "D5", "B4", "A4", "B4"], [0.5, 0.5, 1.0, 0.75, 0.5, 2.0]),
    (202, ["B4", "D5", "E5", "D5", "B4", "A4"], [0.5, 0.5, 0.75, 1.0, 0.5, 2.0]),
    (210, ["B4", "B4", "D5", "E5", "E5", "D5", "B4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
    (218, ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 0.75, 0.75, 0.75, 0.5, 0.5, 1.25]),
    (226, ["B4", "D5", "E5", "F#5", "E5", "D5"], [0.5, 0.5, 0.75, 0.75, 0.75, 2.0]),
    (234, ["A4", "B4", "D5", "E5", "F#5", "E5"], [0.5, 0.5, 1.0, 0.5, 1.0, 2.0]),
    (242, ["D5", "E5", "F#5", "E5", "D5", "B4"], [0.75, 0.75, 0.5, 1.0, 0.75, 1.75]),
    (250, ["B4", "D5", "E5", "F#5", "E5", "E5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
    (273, ["G4", "A4", "B4", "D5", "B4", "A4", "G4", "A4"], [0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 0.75, 1.75]),
    (281, ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "B4", "D5"], [0.5, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 1.5]),
    (290, ["B4", "B4", "D5", "E5", "E5", "D5", "B4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
    (298, ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 0.75, 0.75, 0.75, 0.5, 0.5, 1.25]),
    (306, ["B4", "D5", "E5", "F#5", "E5", "D5"], [0.5, 0.5, 0.75, 0.75, 0.75, 2.0]),
    (314, ["A4", "B4", "D5", "E5", "F#5", "E5"], [0.5, 0.5, 1.0, 0.5, 1.0, 2.0]),
    (322, ["D5", "E5", "F#5", "E5", "D5", "B4"], [0.75, 0.75, 0.5, 1.0, 0.75, 1.75]),
    (330, ["B4", "D5", "E5", "F#5", "E5", "E5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
    (338, ["B4", "D5", "E5", "F#5", "E5", "D5", "B4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
    (346, ["B4", "D5", "E5", "F#5", "E5", "D5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
]


def harmony(name: str) -> list[dict[str, object]]:
    return [
        {"at": f"{index + 1}:1", "duration": 4, "chord": chord}
        for index, chord in enumerate(CHORDS[name])
    ]


def phrase(
    instrument: str,
    role: str,
    phrase_type: str,
    energy: float,
    seed: int,
    **extra: object,
) -> dict[str, object]:
    result: dict[str, object] = {
        "instrument": instrument,
        "role": role,
        "phrase_type": phrase_type,
        "energy": energy,
        "performance_intent": {
            "attack": "section_shaped",
            "release": "phrase_shaped",
            "humanization": "action_based",
            "seed": seed,
        },
    }
    result.update(extra)
    return result


def clip(data: dict[str, object], bars: int) -> dict[str, object]:
    return {
        "loop_bars": bars,
        "sound_library_profile": "general_midi",
        "instrument_phrase": data,
    }


def lead_intro() -> list[dict[str, object]]:
    return [
        {"at": "1:1", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "1:1.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "1:2", "pitch": "B4", "duration": 1.5, "articulations": ["sustain", "accent"]},
        {"at": "2:1", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "2:1.5", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "2:2", "pitch": "E4", "duration": 1.5, "articulations": ["sustain"]},
        {"at": "3:1", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "3:1.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "3:2", "pitch": "D5", "duration": 2.0, "articulations": ["sustain", "accent"]},
        {"at": "4:3", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "4:3.5", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "4:4", "pitch": "E4", "duration": 0.75, "articulations": ["sustain"]},
    ]


def bridge_solo_first_half() -> list[dict[str, object]]:
    return [
        {"at": "1:1", "pitch": "E4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "1:1.5", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "1:2", "pitch": "A4", "duration": 1.5, "articulations": ["sustain", "accent"]},
        {"at": "2:1", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "2:1.5", "pitch": "E4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "2:2", "pitch": "D4", "duration": 1.5, "articulations": ["sustain"]},
        {"at": "3:2", "pitch": "G4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "3:2.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "3:3", "pitch": "B4", "duration": 1.0, "articulations": ["sustain", "accent"]},
        {"at": "4:1", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "4:1.5", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "4:2", "pitch": "D5", "duration": 2.0, "articulations": ["sustain", "accent"]},
    ]


def section_windows() -> dict[str, tuple[float, float]]:
    windows: dict[str, tuple[float, float]] = {}
    cursor = 0.0
    for name, bars, _ in SECTIONS:
        end = cursor + bars * 4.0
        windows[name] = (cursor, end)
        cursor = end
    return windows


def format_at(absolute_beat: float, section_start: float) -> str:
    local = absolute_beat - section_start
    bar = int(local // 4.0) + 1
    beat = (local % 4.0) + 1.0
    if abs(beat - round(beat)) < 1e-9:
        beat_text = str(int(round(beat)))
    else:
        beat_text = f"{beat:.2f}".rstrip("0").rstrip(".")
    return f"{bar}:{beat_text}"


def melody_motifs_by_section() -> dict[str, list[dict[str, object]]]:
    windows = section_windows()
    result: dict[str, list[dict[str, object]]] = {name: [] for name, _, _ in SECTIONS}

    for phrase_start, pitches, durations in MELODY_PHRASES:
        if len(pitches) != len(durations):
            raise ValueError("melody phrase pitches and durations must have equal length")

        cursor = float(phrase_start)
        merged: list[dict[str, object]] = []
        for pitch, duration in zip(pitches, durations):
            duration = float(duration)
            if merged and merged[-1]["pitch"] == pitch:
                previous_end = float(merged[-1]["absolute_start"]) + float(merged[-1]["duration"])
                if abs(previous_end - cursor) < 1e-9:
                    merged[-1]["duration"] = float(merged[-1]["duration"]) + duration
                    cursor += duration
                    continue
            merged.append({"absolute_start": cursor, "pitch": pitch, "duration": duration})
            cursor += duration

        for note_index, note in enumerate(merged):
            absolute_start = float(note["absolute_start"])
            duration = float(note["duration"])
            section_name = next(
                (name for name, (start, end) in windows.items() if start <= absolute_start < end),
                None,
            )
            if section_name is None:
                raise ValueError(f"melody note at absolute beat {absolute_start} is outside the song")

            section_start, section_end = windows[section_name]
            if absolute_start + duration > section_end + 1e-9:
                raise ValueError(f"melody note crosses section boundary at beat {absolute_start}")

            articulations = ["sustain"]
            if duration >= 1.5 or note_index == len(merged) - 1:
                articulations.append("accent")
            result[section_name].append({
                "at": format_at(absolute_start, section_start),
                "pitch": str(note["pitch"]),
                "duration": duration,
                "articulations": articulations,
            })

    return {name: motif for name, motif in result.items() if motif}


def build_composition() -> dict[str, object]:
    tracks: dict[str, dict[str, object]] = {
        "acoustic_guitar": {"role": "steel-string acoustic guitar rhythmic bed / primary melody support", "sections": {}},
        "muted_guitar": {"role": "palm-muted electric guitar verse/pre drive", "sections": {}},
        "rhythm_guitar": {"role": "overdriven electric guitar open-section bed", "sections": {}},
        "melody_guitar": {"role": "clean electric guitar primary melody / vocal substitute", "sections": {}},
        "lead_guitar": {"role": "distorted electric lead intro hook / bridge handoff / outro tail", "sections": {}},
        "bass": {"role": "finger bass foundation with connective motion", "sections": {}},
        "drums": {"role": "drum kit pulse and section lift", "sections": {}},
        "organ": {"role": "thin sustained harmonic color", "sections": {}},
    }

    acoustic_sections = [
        "intro", "verse_1", "pre_1", "chorus_1", "verse_2",
        "pre_2", "chorus_2", "final_chorus", "outro",
    ]
    for index, name in enumerate(acoustic_sections):
        tracks["acoustic_guitar"]["sections"][name] = clip(phrase(
            "acoustic_guitar",
            "rhythmic_accompaniment_primary_melody_support",
            "continuous_strumming",
            max(0.25, SECTION_ENERGY[name] - 0.07),
            1100 + index,
            harmony=harmony(name),
            subdivision="sixteenth",
            strumming_pattern="sixteenth_flow",
            strumming_continuity="selective-flow",
            four_bar_variation=True,
            foreground_aware=True,
            strum_spread=0.032,
            gate=0.88,
            articulations=["sustain"],
        ), SECTION_BARS[name])

    muted_sections = ["verse_1", "pre_1", "verse_2", "pre_2", "bridge"]
    for index, name in enumerate(muted_sections):
        bars = SECTION_BARS[name]
        rest_steps = [step for step in range(bars * 8) if (step + 1) % 16 == 0]
        if name == "bridge":
            rest_steps += [3, 7, 11, 19]
        tracks["muted_guitar"]["sections"][name] = clip(phrase(
            "electric_rhythm_guitar",
            "section_drive",
            "palm_muted_eighths",
            max(0.35, SECTION_ENERGY[name] - 0.05),
            1200 + index,
            harmony=harmony(name),
            subdivision=0.5,
            gate=0.42,
            strum_spread=0.026,
            rest_steps=sorted(set(rest_steps)),
            articulations=["palm_mute"],
        ), bars)

    for index, name in enumerate(["chorus_1", "chorus_2", "final_chorus"]):
        tracks["rhythm_guitar"]["sections"][name] = clip(phrase(
            "electric_rhythm_guitar",
            "continuous_guitar_bed",
            "open_power_chords",
            SECTION_ENERGY[name],
            1300 + index,
            harmony=harmony(name),
            subdivision=1.0,
            gate=0.96,
            strum_spread=0.052,
            rest_steps=[],
            articulations=["sustain", "accent"],
        ), SECTION_BARS[name])

    melody_sections = melody_motifs_by_section()
    for index, (name, motif) in enumerate(melody_sections.items()):
        tracks["melody_guitar"]["sections"][name] = clip(phrase(
            "electric_lead_guitar",
            "primary_melody",
            "melodic_lead",
            min(0.98, SECTION_ENERGY[name] + 0.10),
            1350 + index,
            motif=motif,
            articulations=["sustain"],
        ), SECTION_BARS[name])

    # The distorted lead no longer competes with the primary melody in choruses.
    # It frames the song, then hands the bridge to the clean melody guitar.
    tracks["lead_guitar"]["sections"]["intro"] = clip(phrase(
        "electric_lead_guitar", "hook", "melodic_lead", 0.58, 1400,
        motif=lead_intro(), articulations=["sustain"],
    ), 4)
    tracks["lead_guitar"]["sections"]["bridge"] = clip(phrase(
        "electric_lead_guitar", "bridge_solo_handoff", "melodic_lead", 0.77, 1401,
        motif=bridge_solo_first_half(), articulations=["sustain"],
    ), 8)
    tracks["lead_guitar"]["sections"]["outro"] = clip(phrase(
        "electric_lead_guitar", "phrase_tail", "melodic_lead", 0.42, 1402,
        motif=[
            {"at": "1:1", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
            {"at": "1:1.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
            {"at": "1:2", "pitch": "B4", "duration": 1.5, "articulations": ["sustain"]},
            {"at": "2:1", "pitch": "G4", "duration": 1.0, "articulations": ["sustain"]},
            {"at": "3:1", "pitch": "A4", "duration": 1.0, "articulations": ["sustain"]},
            {"at": "4:1", "pitch": "D5", "duration": 3.0, "articulations": ["sustain", "accent"]},
        ],
        articulations=["sustain"],
    ), 4)

    bass_sections = [
        "verse_1", "pre_1", "chorus_1", "verse_2",
        "pre_2", "chorus_2", "bridge", "final_chorus",
    ]
    for index, name in enumerate(bass_sections):
        if "chorus" in name:
            kick_offsets = [0.0, 1.5, 2.0, 3.5]
        elif "pre" in name:
            kick_offsets = [0.0, 2.0, 3.25]
        else:
            kick_offsets = [0.0, 2.0]
        tracks["bass"]["sections"][name] = clip(phrase(
            "electric_bass",
            "bass_foundation_melodic_support",
            "supportive_bass",
            min(0.95, SECTION_ENERGY[name] + 0.02),
            1500 + index,
            harmony=harmony(name),
            kick_offsets=kick_offsets,
            register_midi=[28, 50],
            articulations=["finger"],
        ), SECTION_BARS[name])

    drum_sections = [
        "verse_1", "pre_1", "chorus_1", "verse_2",
        "pre_2", "chorus_2", "bridge", "final_chorus",
    ]
    for index, name in enumerate(drum_sections):
        chorus = "chorus" in name
        tracks["drums"]["sections"][name] = clip(phrase(
            "drum_kit",
            "drums",
            "chorus_with_fill" if chorus else "rock_verse",
            SECTION_ENERGY[name],
            1600 + index,
            bars=SECTION_BARS[name],
            transition_fill=name not in {"verse_1", "verse_2"},
        ), SECTION_BARS[name])

    for index, name in enumerate(["pre_1", "chorus_1", "pre_2", "chorus_2", "bridge", "final_chorus"]):
        tracks["organ"]["sections"][name] = clip(phrase(
            "organ",
            "sustained_harmonic_support",
            "organ_voice_led_chords",
            max(0.22, SECTION_ENERGY[name] - 0.22),
            1700 + index,
            harmony=harmony(name),
            register_midi=[57, 76],
            voices=3,
            pedal=False,
            articulations=["legato"],
        ), SECTION_BARS[name])

    section_data = []
    for name, bars, energy in SECTIONS:
        section_data.append({
            "name": name,
            "bars": bars,
            "complexity": "rich" if energy >= 0.78 else ("standard" if energy >= 0.45 else "simple"),
            "complexity_budget": {
                "lead": 3 if name in {"bridge", "final_chorus"} else (2 if "chorus" in name or name == "intro" else 1),
                "drums": 3 if "chorus" in name else (2 if name not in {"intro", "outro"} else 0),
                "bass": 2 if name not in {"intro", "outro"} else 0,
                "chords": 3 if "chorus" in name else 2,
            },
        })

    return {
        "metadata": {
            "title": "Signal Through the Static",
            "tempo": TEMPO,
            "time_signature": "4/4",
            "key": "D major / B minor",
        },
        "complexity": "rich",
        "complexity_contour": "custom",
        "sections": section_data,
        "tracks": tracks,
    }


def build_instruments() -> dict[str, object]:
    return {
        "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25},
        "muted_guitar": {"engine": "fluidsynth", "bank": 0, "program": 28},
        "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29},
        "melody_guitar": {"engine": "fluidsynth", "bank": 0, "program": 27},
        "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30},
        "bass": {"engine": "fluidsynth", "bank": 0, "program": 33},
        "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 0},
        "organ": {"engine": "fluidsynth", "bank": 0, "program": 18},
    }


def build_render() -> dict[str, object]:
    return {
        "sample_rate": 44100,
        "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
        "fluidsynth_gain": 0.72,
        "tail_seconds": 4,
        "master_peak_db": -1,
        "mix": {
            "acoustic_guitar": {"volume_db": -7.5, "pan": -0.34, "mute": False},
            "muted_guitar": {"volume_db": -9.0, "pan": 0.30, "mute": False},
            "rhythm_guitar": {"volume_db": -8.2, "pan": 0.42, "mute": False},
            "melody_guitar": {"volume_db": -3.2, "pan": -0.05, "mute": False},
            "lead_guitar": {"volume_db": -5.4, "pan": 0.14, "mute": False},
            "bass": {"volume_db": -5.0, "pan": 0.0, "mute": False},
            "drums": {"volume_db": -6.5, "pan": 0.0, "mute": False},
            "organ": {"volume_db": -12.0, "pan": -0.14, "mute": False},
        },
    }


def write_project_files() -> None:
    files = {
        "composition.json": build_composition(),
        "instruments.json": build_instruments(),
        "render.json": build_render(),
    }
    for filename, data in files.items():
        (PROJECT / filename).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[OK] wrote {PROJECT / filename}")

    stale_vocals = PROJECT / "vocals.json"
    if stale_vocals.exists():
        stale_vocals.unlink()
        print(f"[OK] removed stale {stale_vocals}")


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Signal Through the Static with clean electric guitar as the primary melody."
    )
    parser.add_argument("--write-only", action="store_true", help="write project JSON files but do not render")
    args = parser.parse_args()

    write_project_files()
    bars = sum(bars for _, bars, _ in SECTIONS)
    seconds = bars * 4 * 60.0 / TEMPO
    print(f"[INFO] score length: {bars} bars, {seconds:.2f}s before render tail")
    print("[INFO] primary melody: clean electric guitar (GM program 27); no vocal renderer")
    if args.write_only:
        return 0

    run([sys.executable, str(ROOT / "scripts" / "render_song.py"), PROJECT_NAME])

    for script in ("critic_instruments.py", "critic_complexity.py", "critic_continuity.py"):
        run([sys.executable, str(ROOT / "scripts" / script), PROJECT_NAME, "--write"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
