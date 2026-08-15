from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parent
SLUG = "halfway_to_sunrise_pop_rock"
TITLE = "Halfway to Sunrise"
TEMPO = 128

SECTIONS = [
    ("intro", 4),
    ("verse_1", 12),
    ("pre_1", 8),
    ("chorus_1", 12),
    ("verse_2", 12),
    ("pre_2", 8),
    ("chorus_2", 12),
    ("bridge", 8),
    ("final_chorus", 16),
    ("outro", 4),
]
SECTION_BARS = dict(SECTIONS)
SECTION_INDEX = {name: index for index, (name, _) in enumerate(SECTIONS)}
PROGRESSIONS = {
    "intro": ["Bm", "G", "D", "A"],
    "verse_1": ["Bm", "G", "D", "A", "Bm", "G", "D", "F#m", "G", "D", "Em", "A"],
    "pre_1": ["Em", "G", "D", "A", "Em", "G", "A", "A"],
    "chorus_1": ["D", "A", "Bm", "G", "D", "A", "Em", "G", "Bm", "A", "G", "A"],
    "verse_2": ["Bm", "G", "D", "A", "Bm", "G", "D", "F#m", "G", "D", "Em", "A"],
    "pre_2": ["Em", "G", "D", "A", "Em", "G", "A", "A"],
    "chorus_2": ["D", "A", "Bm", "G", "D", "A", "Em", "G", "Bm", "A", "G", "A"],
    "bridge": ["Em", "Bm", "G", "D", "C", "G", "A", "A"],
    "final_chorus": ["D", "A", "Bm", "G", "D", "A", "Em", "G", "Bm", "A", "G", "A", "D", "A", "G", "D"],
    "outro": ["D", "A", "G", "D"],
}
ENERGY = {
    "intro": 0.38, "verse_1": 0.48, "pre_1": 0.62, "chorus_1": 0.80,
    "verse_2": 0.54, "pre_2": 0.68, "chorus_2": 0.86, "bridge": 0.74,
    "final_chorus": 0.94, "outro": 0.36,
}
COMPLEXITY = {
    "intro": ("standard", {"lead": 2, "drums": 1, "bass": 1, "chords": 2}),
    "verse_1": ("standard", {"lead": 2, "drums": 2, "bass": 2, "chords": 2}),
    "pre_1": ("rich", {"lead": 1, "drums": 2, "bass": 2, "chords": 3}),
    "chorus_1": ("rich", {"lead": 2, "drums": 3, "bass": 2, "chords": 3}),
    "verse_2": ("rich", {"lead": 2, "drums": 2, "bass": 2, "chords": 2}),
    "pre_2": ("rich", {"lead": 1, "drums": 3, "bass": 2, "chords": 3}),
    "chorus_2": ("rich", {"lead": 3, "drums": 3, "bass": 2, "chords": 3}),
    "bridge": ("rich", {"lead": 4, "drums": 2, "bass": 3, "chords": 3}),
    "final_chorus": ("rich", {"lead": 4, "drums": 4, "bass": 3, "chords": 4}),
    "outro": ("standard", {"lead": 2, "drums": 1, "bass": 1, "chords": 2}),
}

VERSE_1 = [
    "Streetlights flicker by the river",
    "Last train rattles through the glass",
    "I count every red light",
    "Like it knows we're moving fast",
    "Your name wakes inside my pocket",
    "I let the whole screen fade",
    "Every block gets louder now",
    "Every turn says don't be late",
]
PRE_1 = [
    "I don't need a perfect answer",
    "Just a reason not to hide",
    "If we're going down together",
    "Let's at least go down alive",
]
CHORUS = [
    "We're halfway to sunrise",
    "Headlights cutting through the blue",
    "If the night won't show us mercy",
    "I'll keep burning next to you",
    "Let the old signs fall behind us",
    "Let the engine tell the truth",
    "We're halfway to sunrise",
    "And I'm finally coming through",
]
VERSE_2 = [
    "Cold coffee shaking in the holder",
    "Rain keeps drawing on the door",
    "You laugh like nothing ever happened",
    "Then ask what we're running for",
    "I say maybe we were waiting",
    "For the fear to lose its name",
    "Maybe every wrong direction",
    "Brought us close enough to change",
]
PRE_2 = [
    "Now the skyline starts to open",
    "Black is turning silver white",
    "No I don't need forever",
    "I just need you here tonight",
]
BRIDGE = [
    "Kill the radio hear the tires",
    "Every mile becomes a wire",
    "No map no promise no disguise",
    "Just this road and both our lives",
]

VERSE_TEMPLATES = [
    ["B3", "D4", "F#4", "E4", "D4", "C#4", "B3"],
    ["D4", "F#4", "A4", "F#4", "E4", "D4", "C#4"],
    ["B3", "D4", "E4", "F#4", "E4", "D4", "B3"],
    ["C#4", "E4", "F#4", "A4", "F#4", "E4", "D4"],
]
PRE_TEMPLATES = [
    ["E4", "F#4", "G4", "A4", "B4", "A4", "G4"],
    ["F#4", "G4", "A4", "B4", "C#5", "B4", "A4"],
    ["G4", "A4", "B4", "C#5", "D5", "C#5", "B4"],
    ["A4", "B4", "C#5", "D5", "E5", "D5", "C#5"],
]
CHORUS_TEMPLATES = [
    ["F#4", "A4", "B4", "D5"],
    ["A4", "A4", "B4", "D5", "C#5", "B4"],
    ["B4", "A4", "B4", "D5", "E5", "D5", "C#5"],
    ["A4", "B4", "D5", "E5", "D5", "C#5"],
    ["F#4", "A4", "B4", "D5", "C#5", "B4", "A4"],
    ["G4", "A4", "B4", "D5", "E5", "D5"],
    ["F#4", "A4", "B4", "D5"],
    ["A4", "B4", "C#5", "D5", "E5", "D5"],
]
BRIDGE_TEMPLATES = [
    ["E4", "G4", "A4", "B4", "A4", "G4"],
    ["G4", "A4", "B4", "D5", "B4"],
    ["A4", "B4", "D5", "E5", "D5", "B4"],
    ["B4", "D5", "E5", "F#5", "E5", "D5", "B4"],
]


def lead_note(at: str, pitch: str, duration: float, arts: str = "sustain", bend: float | None = None) -> dict:
    item = {"at": at, "pitch": pitch, "duration": duration, "articulations": arts.split("+")}
    if bend is not None:
        item["bend_semitones"] = bend
    return item


LEAD = {
    "intro": [
        lead_note("1:1.5", "F#4", 0.5), lead_note("1:2", "B4", 0.75),
        lead_note("1:3.25", "A4", 0.5), lead_note("1:4", "F#4", 1.0, "sustain+vibrato"),
        lead_note("2:1.5", "D5", 1.25, "sustain+vibrato"), lead_note("2:3", "B4", 0.5),
        lead_note("2:4", "A4", 0.8), lead_note("3:1", "F#4", 0.65),
        lead_note("3:2", "A4", 0.65), lead_note("3:3", "B4", 0.75),
        lead_note("3:4", "D5", 1.0, "sustain+vibrato"), lead_note("4:2", "C#5", 0.6),
        lead_note("4:3", "B4", 0.6), lead_note("4:4", "A4", 0.9, "bend+vibrato", 2),
    ],
    "verse_1": [
        lead_note("4:3.25", "B4", 0.5), lead_note("4:3.75", "A4", 0.5),
        lead_note("5:1.25", "F#4", 0.7, "sustain+vibrato"),
        lead_note("8:3.25", "A4", 0.5), lead_note("8:3.75", "B4", 0.5),
        lead_note("9:1.25", "C#5", 0.7),
        lead_note("12:3", "D5", 0.7), lead_note("12:4", "C#5", 0.85, "sustain+vibrato"),
    ],
    "chorus_1": [
        lead_note("4:3", "A4", 0.7), lead_note("4:4", "B4", 1.3, "sustain+vibrato"),
        lead_note("8:3", "D5", 0.7), lead_note("8:4", "C#5", 1.3, "sustain+vibrato"),
        lead_note("12:2.5", "B4", 0.65), lead_note("12:3.25", "A4", 0.65),
        lead_note("12:4", "F#4", 1.0, "bend+vibrato", 2),
    ],
    "verse_2": [
        lead_note("4:3", "F#4", 0.6), lead_note("4:3.75", "A4", 0.6),
        lead_note("5:1.5", "B4", 0.5),
        lead_note("8:3", "C#5", 0.55), lead_note("8:3.75", "B4", 0.55),
        lead_note("9:1.5", "A4", 0.5),
        lead_note("12:3", "B4", 0.7), lead_note("12:4", "D5", 0.9, "sustain+vibrato"),
    ],
    "chorus_2": [
        lead_note("4:3", "A4", 0.65), lead_note("4:4", "D5", 1.4, "sustain+vibrato"),
        lead_note("8:3", "B4", 0.65), lead_note("8:4", "E5", 1.35, "bend+vibrato", 2),
        lead_note("12:2.5", "D5", 0.6), lead_note("12:3.25", "C#5", 0.6),
        lead_note("12:4", "A4", 1.0, "sustain+vibrato"),
    ],
    "bridge": [
        lead_note("1:3", "G4", 0.75), lead_note("1:4", "B4", 1.5, "sustain+vibrato"),
        lead_note("2:3.25", "A4", 0.55), lead_note("2:4", "F#4", 0.9),
        lead_note("3:3", "B4", 0.75), lead_note("3:4", "D5", 1.4, "sustain+vibrato"),
        lead_note("4:3", "C#5", 0.65), lead_note("4:4", "A4", 1.0, "bend+vibrato", 2),
        lead_note("5:1", "E5", 1.5, "sustain+vibrato"), lead_note("5:3", "D5", 0.65),
        lead_note("5:4", "B4", 0.85), lead_note("6:1", "G4", 0.75),
        lead_note("6:2", "B4", 0.75), lead_note("6:3", "D5", 1.5, "sustain+vibrato"),
        lead_note("7:1", "C#5", 0.75), lead_note("7:2", "B4", 0.75),
        lead_note("7:3", "A4", 1.5, "sustain+vibrato"), lead_note("8:1", "E5", 0.75),
        lead_note("8:2", "F#5", 0.75, "bend+vibrato", 2), lead_note("8:3", "E5", 0.75),
        lead_note("8:4", "D5", 1.0, "sustain+vibrato"),
    ],
    "final_chorus": [
        lead_note("4:3", "A4", 0.65), lead_note("4:4", "D5", 1.35, "sustain+vibrato"),
        lead_note("8:3", "B4", 0.65), lead_note("8:4", "E5", 1.35, "bend+vibrato", 2),
        lead_note("12:3", "D5", 0.65), lead_note("12:4", "F#5", 1.4, "sustain+vibrato"),
        lead_note("13:1", "F#4", 0.5), lead_note("13:1.5", "A4", 0.5),
        lead_note("13:2", "B4", 0.75), lead_note("13:3", "D5", 1.0, "sustain+vibrato"),
        lead_note("14:1", "E5", 0.75), lead_note("14:2", "D5", 0.75),
        lead_note("14:3", "B4", 0.75), lead_note("14:4", "A4", 1.0),
        lead_note("15:1", "B4", 0.75), lead_note("15:2", "D5", 0.75),
        lead_note("15:3", "E5", 0.75), lead_note("15:4", "F#5", 1.0, "bend+vibrato", 2),
        lead_note("16:1", "E5", 0.75), lead_note("16:2", "D5", 0.75),
        lead_note("16:3", "B4", 0.75), lead_note("16:4", "A4", 1.0, "sustain+vibrato"),
    ],
    "outro": [
        lead_note("1:1", "F#4", 0.75), lead_note("1:2", "A4", 0.75),
        lead_note("1:3", "B4", 1.5, "sustain+vibrato"), lead_note("2:1", "D5", 1.5, "sustain+vibrato"),
        lead_note("2:3", "B4", 0.75), lead_note("3:1", "A4", 1.5),
        lead_note("4:1", "F#4", 2.8, "sustain+vibrato"),
    ],
}


def harmony(name: str, start_bar: int = 1, end_bar: int | None = None) -> list[dict]:
    chords = PROGRESSIONS[name]
    end_bar = end_bar or len(chords)
    return [
        {"at": f"{bar}:1", "duration": 4, "chord": chords[bar - 1]}
        for bar in range(start_bar, end_bar + 1)
    ]


def performance(seed: int, picking: str | None = None) -> dict:
    result = {
        "attack": "section_shaped",
        "release": "phrase_shaped",
        "humanization": "action_based",
        "seed": seed,
    }
    if picking:
        result["picking"] = picking
    return result


def clip(phrase: dict, bars: int) -> dict:
    return {
        "loop_bars": bars,
        "sound_library_profile": "general_midi",
        "instrument_phrase": phrase,
    }


def foreground_activity(bars: int) -> list[dict]:
    return [
        {"bar": bar, "active_steps": list(range(12)), "release_steps": [12, 13, 14, 15]}
        for bar in range(1, bars + 1)
    ]


def rest_steps(bars: int, extra: bool = False) -> list[int]:
    result: set[int] = set()
    for block_start in range(0, bars, 4):
        last_bar = min(block_start + 4, bars) - 1
        result.update({last_bar * 8 + 6, last_bar * 8 + 7})
    if extra:
        for bar in range(1, bars, 4):
            result.add(bar * 8 + 7)
    return sorted(value for value in result if value < bars * 8)


def build_composition() -> dict:
    sections = [
        {"name": name, "bars": bars, "complexity": COMPLEXITY[name][0], "complexity_budget": COMPLEXITY[name][1]}
        for name, bars in SECTIONS
    ]
    tracks: dict[str, dict] = {
        "acoustic_guitar": {"role": "steel-string rhythmic accompaniment and vocal-support motion", "sections": {}},
        "muted_guitar": {"role": "dry palm-muted electric-guitar drive for restrained/build sections", "sections": {}},
        "overdrive_rhythm": {"role": "connected overdriven rhythm bed for open sections", "sections": {}},
        "lead_guitar": {"role": "melodic answer voice, hook carrier and bridge solo", "sections": {}},
        "bass": {"role": "electric bass foundation with connective phrase identity", "sections": {}},
        "drums": {"role": "drum-kit groove, section lift and transitions", "sections": {}},
        "piano": {"role": "voice-led harmonic color and bridge contrast", "sections": {}},
    }

    for index, (name, bars) in enumerate(SECTIONS):
        pattern = "sixteenth_continuous" if name in {"pre_1", "pre_2", "final_chorus"} else "sixteenth_flow"
        vocal_section = name not in {"intro", "outro"}
        acoustic = {
            "instrument": "acoustic_guitar",
            "role": "vocal_support" if vocal_section else "rhythmic_accompaniment",
            "phrase_type": "continuous_strumming",
            "energy": max(0.30, ENERGY[name] - 0.12),
            "performance_intent": performance(1100 + index, "alternate"),
            "harmony": harmony(name),
            "subdivision": "sixteenth",
            "strumming_pattern": pattern,
            "four_bar_variation": True,
            "foreground_aware": vocal_section,
            "gate": 0.86 if pattern == "sixteenth_flow" else 0.78,
            "strum_spread": 0.028,
        }
        if vocal_section:
            acoustic["foreground_activity"] = foreground_activity(bars)
        tracks["acoustic_guitar"]["sections"][name] = clip(acoustic, bars)

        tracks["bass"]["sections"][name] = clip({
            "instrument": "electric_bass",
            "role": "bass_foundation",
            "phrase_type": "connecting_bass" if name in {"bridge", "final_chorus"} else "supportive_bass",
            "energy": min(1.0, ENERGY[name] - 0.04),
            "performance_intent": performance(2100 + index),
            "harmony": harmony(name),
            "kick_offsets": [0, 1, 2] if name in {"chorus_1", "chorus_2", "final_chorus"} else [0, 2],
            "register_midi": [28, 52],
            "articulations": ["finger"],
        }, bars)

        chorus_like = name in {"chorus_1", "chorus_2", "bridge", "final_chorus"}
        tracks["drums"]["sections"][name] = clip({
            "instrument": "drum_kit",
            "role": "drums",
            "phrase_type": "chorus_with_fill" if chorus_like else "rock_verse",
            "energy": 0.32 if name == "intro" else ENERGY[name],
            "performance_intent": performance(3100 + index),
            "bars": bars,
            "transition_fill": name != "outro",
        }, bars)

    for name in ("verse_1", "pre_1", "verse_2", "pre_2"):
        bars = SECTION_BARS[name]
        tracks["muted_guitar"]["sections"][name] = clip({
            "instrument": "electric_rhythm_guitar",
            "role": "section_drive",
            "phrase_type": "palm_muted_eighths",
            "energy": ENERGY[name] - 0.06,
            "performance_intent": performance(4100 + SECTION_INDEX[name], "alternate"),
            "harmony": harmony(name),
            "subdivision": 0.5,
            "gate": 0.46 if "pre" not in name else 0.38,
            "strum_spread": 0.036,
            "rest_steps": rest_steps(bars, extra="verse" in name),
            "articulations": ["palm_mute"],
        }, bars)
    tracks["muted_guitar"]["sections"]["bridge"] = clip({
        "instrument": "electric_rhythm_guitar",
        "role": "section_drive",
        "phrase_type": "palm_muted_eighths",
        "energy": 0.52,
        "performance_intent": performance(4177, "alternate"),
        "harmony": harmony("bridge", 1, 4),
        "subdivision": 0.5,
        "gate": 0.34,
        "strum_spread": 0.034,
        "rest_steps": [14, 15, 30, 31],
        "articulations": ["palm_mute"],
    }, 8)

    tracks["overdrive_rhythm"]["sections"]["intro"] = clip({
        "instrument": "electric_rhythm_guitar", "role": "rock_foundation", "phrase_type": "open_power_chords",
        "energy": 0.56, "performance_intent": performance(5100, "alternate"), "harmony": harmony("intro", 3, 4),
        "subdivision": 1.0, "gate": 0.98, "strum_spread": 0.058, "articulations": ["sustain", "accent"],
    }, 4)
    for name in ("chorus_1", "chorus_2", "final_chorus"):
        tracks["overdrive_rhythm"]["sections"][name] = clip({
            "instrument": "electric_rhythm_guitar", "role": "continuous_guitar_bed", "phrase_type": "open_power_chords",
            "energy": ENERGY[name], "performance_intent": performance(5200 + SECTION_INDEX[name], "alternate"),
            "harmony": harmony(name), "subdivision": 1.0, "gate": 0.99, "strum_spread": 0.060,
            "articulations": ["sustain", "accent"],
        }, SECTION_BARS[name])
    tracks["overdrive_rhythm"]["sections"]["bridge"] = clip({
        "instrument": "electric_rhythm_guitar", "role": "continuous_guitar_bed", "phrase_type": "open_power_chords",
        "energy": 0.78, "performance_intent": performance(5277, "alternate"), "harmony": harmony("bridge", 5, 8),
        "subdivision": 1.0, "gate": 0.99, "strum_spread": 0.060, "articulations": ["sustain", "accent"],
    }, 8)
    tracks["overdrive_rhythm"]["sections"]["outro"] = clip({
        "instrument": "electric_rhythm_guitar", "role": "release_layer", "phrase_type": "open_power_chords",
        "energy": 0.42, "performance_intent": performance(5299, "alternate"), "harmony": harmony("outro", 1, 2),
        "subdivision": 1.0, "gate": 0.94, "strum_spread": 0.060, "articulations": ["sustain"],
    }, 4)

    for name, motif in LEAD.items():
        tracks["lead_guitar"]["sections"][name] = clip({
            "instrument": "electric_lead_guitar",
            "role": "lead" if name in {"intro", "bridge", "final_chorus", "outro"} else "melodic_fill",
            "phrase_type": "melodic_lead",
            "energy": min(1.0, ENERGY[name] + 0.02),
            "performance_intent": performance(6100 + SECTION_INDEX[name], "alternate"),
            "motif": motif,
        }, SECTION_BARS[name])

    piano_energy = {
        "intro": 0.34, "pre_1": 0.46, "pre_2": 0.52, "chorus_2": 0.42,
        "bridge": 0.62, "final_chorus": 0.52, "outro": 0.30,
    }
    for name, level in piano_energy.items():
        tracks["piano"]["sections"][name] = clip({
            "instrument": "piano", "role": "harmonic_color", "phrase_type": "piano_voice_led_chords",
            "energy": level, "performance_intent": performance(7100 + SECTION_INDEX[name]), "harmony": harmony(name),
            "register_midi": [55, 79], "voices": 3, "pedal": True, "articulations": ["tenuto"],
        }, SECTION_BARS[name])

    return {
        "metadata": {"title": TITLE, "tempo": TEMPO, "time_signature": "4/4", "key": "D major / B minor"},
        "complexity": "rich",
        "complexity_contour": "custom",
        "sections": sections,
        "tracks": tracks,
    }


def section_starts() -> dict[str, int]:
    result: dict[str, int] = {}
    beat = 0
    for name, bars in SECTIONS:
        result[name] = beat
        beat += bars * 4
    return result


def word_durations(count: int, total: float) -> list[float]:
    weights = [0.8] * count
    if count:
        weights[0] = 0.9
        weights[-1] = 1.7
    if count >= 6:
        weights[2] = 0.7
    scale = total / sum(weights)
    return [round(weight * scale, 3) for weight in weights]


def adapt_pitches(template: list[str], count: int) -> list[str]:
    if count <= len(template):
        if count == 1:
            return [template[0]]
        indexes = [round(index * (len(template) - 1) / (count - 1)) for index in range(count)]
        return [template[index] for index in indexes]
    return template + [template[-1]] * (count - len(template))


def vocal_phrase(start_beat: int, line: str, template: list[str], total: float) -> dict:
    words = line.split()
    pitches = adapt_pitches(template, len(words))
    durations = word_durations(len(words), total)
    return {
        "start_beat": start_beat,
        "notes": [
            {"lyric": word, "pitch": pitch, "duration": duration}
            for word, pitch, duration in zip(words, pitches, durations)
        ],
    }


def build_vocals() -> dict:
    starts = section_starts()
    phrases: list[dict] = []

    def add(section: str, lines: list[str], offsets: list[int], templates: list[list[str]], total: float) -> None:
        for index, (line, offset) in enumerate(zip(lines, offsets)):
            phrases.append(vocal_phrase(starts[section] + offset, line, templates[index % len(templates)], total))

    add("verse_1", VERSE_1, [0, 6, 12, 18, 24, 30, 36, 42], VERSE_TEMPLATES, 5.0)
    add("pre_1", PRE_1, [0, 8, 16, 24], PRE_TEMPLATES, 6.0)
    add("chorus_1", CHORUS, [0, 6, 12, 18, 24, 30, 36, 42], CHORUS_TEMPLATES, 5.0)
    add("verse_2", VERSE_2, [0, 6, 12, 18, 24, 30, 36, 42], VERSE_TEMPLATES[1:] + VERSE_TEMPLATES[:1], 5.0)
    add("pre_2", PRE_2, [0, 8, 16, 24], PRE_TEMPLATES[1:] + PRE_TEMPLATES[:1], 6.0)
    add("chorus_2", CHORUS, [0, 6, 12, 18, 24, 30, 36, 42], CHORUS_TEMPLATES, 5.0)
    add("bridge", BRIDGE, [0, 8, 16, 24], BRIDGE_TEMPLATES, 5.5)
    add("final_chorus", CHORUS, [0, 6, 12, 18, 24, 30, 36, 42], CHORUS_TEMPLATES, 5.0)

    return {
        "enabled": True,
        "language": "en",
        "engine": "soulx_singer",
        "device": "cuda",
        "seed": 4242,
        "phrases": phrases,
        "mix": {"volume_db": -1.8, "pan": 0.0, "mute": False},
    }


def build_instruments() -> dict:
    return {
        "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25},
        "muted_guitar": {"engine": "fluidsynth", "bank": 0, "program": 28},
        "overdrive_rhythm": {"engine": "fluidsynth", "bank": 0, "program": 29},
        "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30},
        "bass": {"engine": "fluidsynth", "bank": 0, "program": 33},
        "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16},
        "piano": {"engine": "fluidsynth", "bank": 0, "program": 0},
    }


def build_render() -> dict:
    return {
        "sample_rate": 44100,
        "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
        "fluidsynth_gain": 0.74,
        "tail_seconds": 3,
        "master_peak_db": -1,
        "mix": {
            "acoustic_guitar": {"volume_db": -8.0, "pan": -0.34, "mute": False},
            "muted_guitar": {"volume_db": -8.5, "pan": 0.30, "mute": False},
            "overdrive_rhythm": {"volume_db": -7.2, "pan": -0.26, "mute": False},
            "lead_guitar": {"volume_db": -4.4, "pan": 0.22, "mute": False},
            "bass": {"volume_db": -4.6, "pan": 0.0, "mute": False},
            "drums": {"volume_db": -6.4, "pan": 0.0, "mute": False},
            "piano": {"volume_db": -10.2, "pan": 0.16, "mute": False},
        },
    }


def build_manifest() -> dict:
    return {
        "schema": "music-agent-project-facade",
        "schema_version": 1,
        "project": {
            "title": TITLE,
            "slug": SLUG,
            "status": "active",
            "duration_design": "96 bars at 128 BPM = 180 seconds before render tail",
        },
        "artifacts": {
            "song_source": {"standard": "music-agent song-specific Python source", "path": "build_song.py", "authority": "authoritative"},
            "composition": {"standard": "music-agent composition JSON", "path": "composition.json", "authority": "derived"},
            "vocal_score": {"standard": "music-agent vocal score JSON", "path": "vocals.json", "authority": "derived"},
            "instrument_config": {"standard": "music-agent instrument extension", "path": "instruments.json", "authority": "derived"},
            "render_config": {"standard": "music-agent render extension", "path": "render.json", "authority": "derived"},
            "lyrics": {"standard": "Markdown lyrics sheet", "path": "lyrics.md", "authority": "derived"},
            "semantic_phrases": {"standard": "music-agent semantic phrase export", "path": "semantic_phrases.json", "authority": "derived"},
            "execution_midi": {"standard": "MIDI 1.0 Standard MIDI File", "path": "output/full_song.mid", "authority": "derived"},
            "instrumental_mix": {"standard": "WAVE PCM audio", "path": "output/mix.wav", "authority": "derived"},
            "vocal_mix": {"standard": "WAVE PCM audio", "path": "output/vocal_mix.wav", "authority": "derived"},
        },
        "conversion_reports": ["instrument-validation.json"],
        "edit_protocols": {"pointer": "RFC 6901 JSON Pointer", "patch": "RFC 6902 JSON Patch"},
    }


def build_lyrics_md() -> str:
    sections = [
        ("Verse 1", VERSE_1), ("Pre-Chorus 1", PRE_1), ("Chorus", CHORUS),
        ("Verse 2", VERSE_2), ("Pre-Chorus 2", PRE_2), ("Chorus 2", CHORUS),
        ("Bridge", BRIDGE), ("Final Chorus", CHORUS),
    ]
    lines = [f"# {TITLE}", "", "Original English lyrics for the project.", ""]
    for heading, content in sections:
        lines.extend([f"## {heading}", "", *content, ""])
    lines.extend([
        "## Instrumental tag", "",
        "The last four bars of the final chorus are intentionally left without lead vocal so the guitar hook can answer the song.", "",
    ])
    return "\n".join(lines)


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_files() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    write_json(PROJECT / "composition.json", build_composition())
    write_json(PROJECT / "vocals.json", build_vocals())
    write_json(PROJECT / "instruments.json", build_instruments())
    write_json(PROJECT / "render.json", build_render())
    write_json(PROJECT / "manifest.json", build_manifest())
    (PROJECT / "lyrics.md").write_text(build_lyrics_md(), encoding="utf-8")
    print(f"[OK] Built structured project: {PROJECT}")
    print("[OK] Score length: 96 bars @ 128 BPM = 180.00 seconds (+ 3 second render tail)")


def run_render(with_vocals: bool) -> None:
    command = [sys.executable, str(ROOT / "scripts" / "render_song.py"), SLUG]
    if with_vocals:
        command.append("--with-vocals")
    subprocess.run(command, cwd=ROOT, check=True)


def run_audits() -> None:
    for script in ("critic_instruments.py", "critic_complexity.py", "critic_continuity.py"):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), SLUG, "--write"], cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Halfway to Sunrise as a structured V2 music-agent project.")
    parser.add_argument("--render", action="store_true", help="render MIDI, stems and instrumental mix after building")
    parser.add_argument("--with-vocals", action="store_true", help="render the SoulX-Singer English vocal mix (implies --render)")
    parser.add_argument("--audit", action="store_true", help="run instrument / complexity / continuity critics")
    args = parser.parse_args()
    try:
        build_files()
        if args.render or args.with_vocals:
            run_render(args.with_vocals)
        if args.audit:
            run_audits()
    except subprocess.CalledProcessError as error:
        print(f"[FAIL] command exited with {error.returncode}", file=sys.stderr)
        return error.returncode or 1
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
