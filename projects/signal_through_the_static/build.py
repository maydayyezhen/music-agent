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


def chorus_fills(*, lift: bool = False, final: bool = False) -> list[dict[str, object]]:
    notes: list[dict[str, object]] = [
        {"at": "4:3", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "4:3.5", "pitch": "B4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "4:4", "pitch": "D5", "duration": 1.5, "articulations": ["sustain", "accent"]},
        {"at": "8:3", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "8:3.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "8:4", "pitch": "B4", "duration": 1.5, "articulations": ["sustain", "accent"]},
        {"at": "12:2.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "12:3", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "12:3.5", "pitch": "E4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "12:4", "pitch": "D4", "duration": 1.0, "articulations": ["sustain", "accent"]},
    ]
    if lift:
        replacement = {"D5": "F#5", "B4": "D5"}
        for item in notes:
            item["pitch"] = replacement.get(str(item["pitch"]), item["pitch"])
    if final:
        notes.extend([
            {"at": "15:3", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
            {"at": "15:3.5", "pitch": "B4", "duration": 0.5, "articulations": ["sustain"]},
            {"at": "15:4", "pitch": "D5", "duration": 1.0, "articulations": ["sustain", "accent"]},
            {"at": "16:2", "pitch": "F#5", "duration": 0.5, "articulations": ["sustain"]},
            {"at": "16:2.5", "pitch": "E5", "duration": 0.5, "articulations": ["sustain"]},
            {"at": "16:3", "pitch": "D5", "duration": 2.0, "articulations": ["sustain", "accent"]},
        ])
    return notes


def bridge_solo() -> list[dict[str, object]]:
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
        {"at": "5:3", "pitch": "E5", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "5:3.5", "pitch": "D5", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "5:4", "pitch": "B4", "duration": 1.0, "articulations": ["sustain"]},
        {"at": "6:2", "pitch": "F#4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "6:2.5", "pitch": "A4", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "6:3", "pitch": "B4", "duration": 1.5, "articulations": ["sustain", "accent"]},
        {"at": "7:1", "pitch": "D5", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "7:1.5", "pitch": "E5", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "7:2", "pitch": "F#5", "duration": 1.5, "articulations": ["sustain", "accent"]},
        {"at": "8:2", "pitch": "E5", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "8:2.5", "pitch": "D5", "duration": 0.5, "articulations": ["sustain"]},
        {"at": "8:3", "pitch": "A4", "duration": 1.5, "articulations": ["sustain", "accent"]},
    ]


def build_composition() -> dict[str, object]:
    tracks: dict[str, dict[str, object]] = {
        "acoustic_guitar": {"role": "steel-string acoustic guitar rhythmic bed / vocal support", "sections": {}},
        "muted_guitar": {"role": "palm-muted electric guitar verse/pre drive", "sections": {}},
        "rhythm_guitar": {"role": "overdriven electric guitar open-section bed", "sections": {}},
        "lead_guitar": {"role": "electric lead guitar hook / answer / bridge solo", "sections": {}},
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
            "rhythmic_accompaniment_vocal_support",
            "continuous_strumming",
            max(0.25, SECTION_ENERGY[name] - 0.07),
            1100 + index,
            harmony=harmony(name),
            subdivision="sixteenth",
            strumming_pattern="sixteenth_flow",
            strumming_continuity="selective-flow",
            four_bar_variation=True,
            foreground_aware=False,
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

    tracks["lead_guitar"]["sections"]["intro"] = clip(phrase(
        "electric_lead_guitar", "hook", "melodic_lead", 0.58, 1400,
        motif=lead_intro(), articulations=["sustain"],
    ), 4)
    tracks["lead_guitar"]["sections"]["chorus_1"] = clip(phrase(
        "electric_lead_guitar", "answer_phrase", "melodic_lead", 0.68, 1401,
        motif=chorus_fills(), articulations=["sustain"],
    ), 12)
    tracks["lead_guitar"]["sections"]["chorus_2"] = clip(phrase(
        "electric_lead_guitar", "answer_phrase", "melodic_lead", 0.74, 1402,
        motif=chorus_fills(lift=True), articulations=["sustain"],
    ), 12)
    tracks["lead_guitar"]["sections"]["bridge"] = clip(phrase(
        "electric_lead_guitar", "bridge_solo", "melodic_lead", 0.80, 1403,
        motif=bridge_solo(), articulations=["sustain"],
    ), 8)
    tracks["lead_guitar"]["sections"]["final_chorus"] = clip(phrase(
        "electric_lead_guitar", "climax_answer", "melodic_lead", 0.88, 1404,
        motif=chorus_fills(final=True), articulations=["sustain"],
    ), 16)
    tracks["lead_guitar"]["sections"]["outro"] = clip(phrase(
        "electric_lead_guitar", "phrase_tail", "melodic_lead", 0.42, 1405,
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


def vocal_phrase(
    start_beat: float,
    words: list[str],
    pitches: list[str],
    durations: list[float],
) -> dict[str, object]:
    if not (len(words) == len(pitches) == len(durations)):
        raise ValueError("vocal phrase arrays must be the same length")
    return {
        "start_beat": start_beat,
        "notes": [
            {"lyric": word, "pitch": pitch, "duration": duration}
            for word, pitch, duration in zip(words, pitches, durations)
        ],
    }


def build_vocals() -> dict[str, object]:
    lines: list[tuple[float, list[str], list[str], list[float]]] = [
        (20, ["City", "lights", "are", "bleeding", "through", "the", "rain"], ["F#4", "F#4", "A4", "B4", "A4", "F#4", "E4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
        (30, ["Your", "name", "keeps", "ringing", "in", "the", "wires"], ["F#4", "A4", "B4", "D5", "B4", "A4", "F#4"], [0.5, 0.75, 0.5, 1.0, 0.75, 0.5, 1.5]),
        (40, ["I", "was", "running", "circles", "from", "the", "same", "old", "fear"], ["E4", "F#4", "A4", "B4", "A4", "F#4", "E4", "F#4", "D4"], [0.5, 0.5, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 1.5]),
        (50, ["Now", "the", "night", "is", "opening", "like", "fire"], ["F#4", "A4", "B4", "A4", "D5", "B4", "A4"], [0.5, 0.5, 0.75, 0.5, 1.25, 0.75, 1.75]),
        (66, ["Hold", "on", "do", "not", "let", "the", "moment", "fall"], ["G4", "A4", "B4", "B4", "A4", "G4", "A4", "B4"], [0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 1.0, 1.5]),
        (74, ["We", "are", "closer", "than", "we", "think"], ["A4", "B4", "D5", "B4", "A4", "B4"], [0.5, 0.5, 1.0, 0.75, 0.5, 2.0]),
        (82, ["Hear", "the", "room", "begin", "to", "sing"], ["B4", "D5", "E5", "D5", "B4", "A4"], [0.5, 0.5, 0.75, 1.0, 0.5, 2.0]),
        (90, ["Send", "me", "a", "signal", "through", "the", "static"], ["A4", "A4", "B4", "D5", "D5", "B4", "A4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
        (98, ["I", "can", "hear", "you", "under", "all", "the", "noise"], ["F#4", "A4", "B4", "D5", "B4", "A4", "F#4", "E4"], [0.5, 0.5, 0.75, 0.75, 0.75, 0.5, 0.5, 1.25]),
        (106, ["If", "the", "whole", "world", "turns", "automatic"], ["A4", "B4", "D5", "E5", "D5", "B4"], [0.5, 0.5, 0.75, 0.75, 0.75, 2.0]),
        (114, ["I", "will", "follow", "that", "imperfect", "voice"], ["F#4", "A4", "B4", "D5", "E5", "D5"], [0.5, 0.5, 1.0, 0.5, 1.0, 2.0]),
        (122, ["Stay", "until", "the", "morning", "finds", "us"], ["B4", "D5", "E5", "D5", "B4", "A4"], [0.75, 0.75, 0.5, 1.0, 0.75, 1.75]),
        (130, ["Maybe", "we", "are", "not", "too", "late"], ["A4", "B4", "D5", "E5", "D5", "D5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
        (140, ["I", "kept", "every", "answer", "in", "a", "locked", "room"], ["F#4", "A4", "B4", "A4", "F#4", "E4", "F#4", "D4"], [0.5, 0.5, 0.75, 1.0, 0.5, 0.5, 0.75, 1.5]),
        (150, ["Made", "a", "habit", "out", "of", "missing", "trains"], ["F#4", "A4", "B4", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.5]),
        (160, ["Then", "the", "window", "shakes", "and", "starts", "to", "move"], ["E4", "F#4", "A4", "B4", "A4", "F#4", "A4", "B4"], [0.5, 0.5, 1.0, 0.75, 0.5, 0.5, 0.5, 1.5]),
        (170, ["And", "I", "want", "to", "try", "this", "road", "again"], ["F#4", "A4", "B4", "A4", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 0.75, 0.5, 1.0, 0.75, 0.75, 1.5]),
        (186, ["Hold", "on", "the", "distance", "is", "getting", "small"], ["G4", "A4", "B4", "D5", "B4", "A4", "B4"], [0.75, 0.5, 0.5, 1.0, 0.5, 0.75, 1.75]),
        (194, ["We", "are", "closer", "than", "we", "think"], ["A4", "B4", "D5", "B4", "A4", "B4"], [0.5, 0.5, 1.0, 0.75, 0.5, 2.0]),
        (202, ["Hear", "the", "room", "begin", "to", "sing"], ["B4", "D5", "E5", "D5", "B4", "A4"], [0.5, 0.5, 0.75, 1.0, 0.5, 2.0]),
        (210, ["Send", "me", "a", "signal", "through", "the", "static"], ["B4", "B4", "D5", "E5", "E5", "D5", "B4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
        (218, ["I", "can", "hear", "you", "under", "all", "the", "noise"], ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 0.75, 0.75, 0.75, 0.5, 0.5, 1.25]),
        (226, ["If", "the", "whole", "world", "turns", "automatic"], ["B4", "D5", "E5", "F#5", "E5", "D5"], [0.5, 0.5, 0.75, 0.75, 0.75, 2.0]),
        (234, ["I", "will", "follow", "that", "imperfect", "voice"], ["A4", "B4", "D5", "E5", "F#5", "E5"], [0.5, 0.5, 1.0, 0.5, 1.0, 2.0]),
        (242, ["Stay", "until", "the", "morning", "finds", "us"], ["D5", "E5", "F#5", "E5", "D5", "B4"], [0.75, 0.75, 0.5, 1.0, 0.75, 1.75]),
        (250, ["Maybe", "we", "are", "not", "too", "late"], ["B4", "D5", "E5", "F#5", "E5", "E5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
        (273, ["Maybe", "I", "do", "not", "need", "a", "map", "tonight"], ["G4", "A4", "B4", "D5", "B4", "A4", "G4", "A4"], [0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 0.75, 1.75]),
        (281, ["One", "small", "sound", "can", "pull", "me", "back", "to", "life"], ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "B4", "D5"], [0.5, 0.75, 0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 1.5]),
        (290, ["Send", "me", "a", "signal", "through", "the", "static"], ["B4", "B4", "D5", "E5", "E5", "D5", "B4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
        (298, ["I", "can", "hear", "you", "under", "all", "the", "noise"], ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "F#4"], [0.5, 0.5, 0.75, 0.75, 0.75, 0.5, 0.5, 1.25]),
        (306, ["If", "the", "whole", "world", "turns", "automatic"], ["B4", "D5", "E5", "F#5", "E5", "D5"], [0.5, 0.5, 0.75, 0.75, 0.75, 2.0]),
        (314, ["I", "will", "follow", "that", "imperfect", "voice"], ["A4", "B4", "D5", "E5", "F#5", "E5"], [0.5, 0.5, 1.0, 0.5, 1.0, 2.0]),
        (322, ["Stay", "until", "the", "morning", "finds", "us"], ["D5", "E5", "F#5", "E5", "D5", "B4"], [0.75, 0.75, 0.5, 1.0, 0.75, 1.75]),
        (330, ["Maybe", "we", "are", "not", "too", "late"], ["B4", "D5", "E5", "F#5", "E5", "E5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
        (338, ["Send", "me", "a", "signal", "through", "the", "static"], ["B4", "D5", "E5", "F#5", "E5", "D5", "B4"], [0.5, 0.5, 0.5, 1.0, 0.75, 0.5, 1.75]),
        (346, ["Maybe", "we", "are", "not", "too", "late"], ["B4", "D5", "E5", "F#5", "E5", "D5"], [0.75, 0.5, 0.5, 0.75, 0.75, 2.25]),
    ]
    return {
        "enabled": True,
        "language": "en",
        "engine": "soulx_singer",
        "device": "cuda",
        "seed": 8086,
        "phrases": [vocal_phrase(*line) for line in lines],
        "mix": {"volume_db": -2.5, "pan": 0.0, "mute": False},
    }


def build_instruments() -> dict[str, object]:
    return {
        "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25},
        "muted_guitar": {"engine": "fluidsynth", "bank": 0, "program": 28},
        "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29},
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
            "acoustic_guitar": {"volume_db": -7.0, "pan": -0.32, "mute": False},
            "muted_guitar": {"volume_db": -9.0, "pan": 0.30, "mute": False},
            "rhythm_guitar": {"volume_db": -8.0, "pan": 0.42, "mute": False},
            "lead_guitar": {"volume_db": -4.2, "pan": 0.10, "mute": False},
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
        "vocals.json": build_vocals(),
    }
    for filename, data in files.items():
        (PROJECT / filename).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[OK] wrote {PROJECT / filename}")


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Signal Through the Static from its project-local song specification.")
    parser.add_argument("--write-only", action="store_true", help="write project JSON files but do not render")
    parser.add_argument("--with-vocals", action="store_true", help="render the optional English SoulX vocal score too")
    args = parser.parse_args()

    write_project_files()
    bars = sum(bars for _, bars, _ in SECTIONS)
    seconds = bars * 4 * 60.0 / TEMPO
    print(f"[INFO] score length: {bars} bars, {seconds:.2f}s before render tail")
    if args.write_only:
        return 0

    command = [sys.executable, str(ROOT / "scripts" / "render_song.py"), PROJECT_NAME]
    if args.with_vocals:
        command.append("--with-vocals")
    run(command)

    for script in ("critic_instruments.py", "critic_complexity.py", "critic_continuity.py"):
        run([sys.executable, str(ROOT / "scripts" / script), PROJECT_NAME, "--write"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
