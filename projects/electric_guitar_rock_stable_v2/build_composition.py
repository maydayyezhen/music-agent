from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent


SECTIONS = [
    ("intro", 8),
    ("verse_1", 12),
    ("pre_chorus", 8),
    ("chorus_1", 16),
    ("verse_2", 12),
    ("bridge_relay", 16),
    ("final_chorus", 16),
    ("outro", 8),
]

PROGRESSIONS = {
    "intro": ["Dm", "Bb", "F", "C", "Dm", "Bb", "F", "C"],
    "verse_1": ["Dm", "Bb", "F", "C"] * 3,
    "pre_chorus": ["Gm", "Bb", "C", "A"] * 2,
    "chorus_1": ["Bb", "F", "C", "Dm", "Bb", "F", "A", "Dm"] * 2,
    "verse_2": ["Dm", "C", "Bb", "F", "Dm", "C", "Bb", "A"] + ["Gm", "Bb", "C", "A"],
    "bridge_relay": ["Dm", "C", "Bb", "Gm", "Dm", "C", "Bb", "A",
                     "Gm", "Bb", "F", "C", "Dm", "Bb", "A", "Dm"],
    "final_chorus": ["Bb", "F", "C", "Dm", "Bb", "F", "A", "Dm", "Gm", "Bb", "F", "C", "Bb", "C", "A", "Dm"],
    "outro": ["Dm", "Bb", "F", "C", "Dm", "Bb", "A", "Dm"],
}


def harmony(section: str) -> list[dict]:
    return [
        {"at": f"{bar}:1", "duration": 4, "chord": chord}
        for bar, chord in enumerate(PROGRESSIONS[section], 1)
    ]


def event(pitch: str, bar: int, beat: float, duration: float, velocity: int, arts: list[str] | None = None) -> dict:
    item = {
        "type": "note",
        "pitch": pitch,
        "at": f"{bar}:{beat:g}",
        "duration": duration,
        "velocity": velocity,
    }
    if arts:
        item["articulations"] = arts
    return item


def add_cell(target: list[dict], bar: int, notes: list[tuple], velocity: int, transpose: int = 0) -> None:
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    for pitch, beat, duration, accent in notes:
        name, octave = pitch[:-1], int(pitch[-1])
        midi = (octave + 1) * 12 + names.index(name) + transpose
        rendered = f"{names[midi % 12]}{midi // 12 - 1}"
        arts = ["sustain"]
        if accent == "slide":
            arts.append("slide")
        target.append(event(rendered, bar, beat, duration, velocity + (5 if accent else 0), arts))


THEME_A = [
    ("D5", 1, 1.25, ""), ("F5", 2.5, 0.55, ""),
    ("A5", 3.25, 0.65, "slide"), ("G5", 4, 0.72, ""),
]
ANSWER_A = [
    ("F5", 1, 0.75, ""), ("E5", 2, 0.45, ""),
    ("D5", 2.75, 0.7, ""), ("C5", 3.75, 0.85, ""),
]
HOOK = [
    ("F5", 1, 0.5, ""), ("A5", 1.75, 0.5, ""),
    ("C6", 2.5, 0.75, "slide"), ("A5", 3.5, 0.45, ""),
    ("G5", 4, 0.8, ""),
]


def lead_phrase(section: str, variant: int) -> dict:
    bars = dict(SECTIONS)[section]
    motif: list[dict] = []
    if section == "intro":
        add_cell(motif, 5, THEME_A, 73, -12)
        add_cell(motif, 7, ANSWER_A, 70, -12)
    elif section == "verse_1":
        add_cell(motif, 1, THEME_A, 76, -12)
        add_cell(motif, 3, ANSWER_A, 72, -12)
        add_cell(motif, 5, THEME_A, 78, -10)
        add_cell(motif, 7, ANSWER_A, 74, -12)
        add_cell(motif, 9, THEME_A, 80, -7)
        add_cell(motif, 11, ANSWER_A, 76, -7)
    elif section == "pre_chorus":
        for bar, shift in ((1, -7), (3, -5), (5, -2), (7, 0)):
            add_cell(motif, bar, THEME_A, 78 + bar, shift)
    elif section == "chorus_1":
        for bar, shift in ((1, 0), (3, -2), (5, 0), (7, 2), (9, 0), (11, 3), (13, 4), (15, 2)):
            add_cell(motif, bar, HOOK if bar not in {7, 15} else THEME_A, 84 + min(6, bar // 3), shift)
        if variant >= 200:
            # Second eight-bar pass answers rather than cloning the first pass.
            motif.extend([
                event("D5", 12, 1.5, .42, 88, ["sustain"]),
                event("F5", 12, 2.25, .42, 91, ["sustain"]),
                event("A5", 12, 3, .7, 94, ["sustain", "slide"]),
                event("C6", 14, 1.5, .55, 96, ["sustain"]),
                event("A5", 14, 2.5, .45, 92, ["sustain"]),
                event("G5", 14, 3.25, .8, 90, ["sustain"]),
            ])
    elif section == "verse_2":
        add_cell(motif, 1, THEME_A, 78, -7)
        add_cell(motif, 3, ANSWER_A, 74, -5)
        # The middle of Verse 2 answers in shorter rising fragments instead of copying Verse 1.
        for bar, shift in ((5, -3), (7, 0), (9, 2), (11, 4)):
            fragment = THEME_A[:3] if bar < 9 else HOOK[:4]
            add_cell(motif, bar, fragment, 78 + bar // 2, shift)
    elif section == "final_chorus":
        for bar, shift in ((1, 0), (3, 2), (5, 3), (7, 4), (9, 2), (11, 5), (13, 4), (15, 7)):
            source = HOOK if bar not in {11, 15} else THEME_A
            add_cell(motif, bar, source, 90 + min(8, bar // 3), shift)
        # Final answer changes rhythm and lands only in the last bar.
        motif.extend([
            event("C6", 14, 1.5, 0.42, 99, ["sustain"]),
            event("D6", 14, 2.25, 0.42, 101, ["sustain"]),
            event("E6", 14, 3, 0.55, 104, ["sustain", "slide"]),
            event("D6", 16, 1, 2.6, 100, ["sustain"]),
        ])
        if variant >= 200:
            # Three new answering cells make the return a developed reprise, not an octave copy.
            motif.extend([
                event("A5", 4, 1.5, .45, 94, ["sustain"]), event("C6", 4, 2.25, .45, 97, ["sustain"]),
                event("D6", 4, 3, .85, 100, ["sustain", "slide"]),
                event("G5", 8, 1.25, .55, 96, ["sustain"]), event("A5", 8, 2.25, .55, 99, ["sustain"]),
                event("C6", 8, 3.25, .65, 101, ["sustain"]),
                event("D6", 12, 1.5, .42, 101, ["sustain"]), event("C6", 12, 2.25, .42, 98, ["sustain"]),
                event("A5", 12, 3, .8, 96, ["sustain"]),
            ])
    elif section == "outro":
        add_cell(motif, 1, THEME_A, 78, -12)
        add_cell(motif, 3, ANSWER_A, 74, -12)
        motif.extend([event("F4", 6, 1, 1.2, 69, ["sustain"]), event("D4", 8, 1, 2.6, 66, ["sustain"])])
    return {
        "instrument": "electric_lead_guitar",
        "role": "primary melody",
        "phrase_type": "melodic_lead",
        "phrase_generation_mode": "legacy_stable",
        "energy": {"intro": .28, "verse_1": .42, "pre_chorus": .62, "chorus_1": .82,
                   "verse_2": .52, "final_chorus": 1.0, "outro": .3}[section],
        "motif": motif,
        "articulations": ["sustain"],
        "performance_intent": {"attack": "picked", "release": "clean", "humanization": "none", "seed": 6100 + variant},
    }


def rhythm_phrase(section: str, variant: int) -> dict:
    chorus = section in {"chorus_1", "final_chorus"}
    bridge = section == "bridge_relay"
    intro = section == "intro"
    open_chords = chorus or section == "outro"
    phrase_type = "open_power_chords" if open_chords else "palm_muted_eighths"
    if bridge:
        # First half pedals in wider quarters; second half compresses into eighth-note propulsion.
        phrase_type = "palm_muted_eighths"
    rest_steps = []
    if intro:
        rest_steps = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26, 27, 29, 30, 31]
    elif section in {"verse_1", "verse_2"}:
        rest_steps = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]
    return {
        "instrument": "electric_rhythm_guitar",
        "role": "rhythmic harmony" if not bridge else "bridge pedal-riff carrier",
        "phrase_type": phrase_type,
        "energy": {"intro": .2, "verse_1": .38, "pre_chorus": .6, "chorus_1": .8,
                   "verse_2": .46, "bridge_relay": .72, "final_chorus": .96, "outro": .34}[section],
        "harmony": harmony(section),
        "subdivision": 1.0 if (intro or open_chords) else .5,
        "gate": .42 if not open_chords else .86,
        "strum_spread": .04 if not open_chords else .075,
        "rest_steps": rest_steps,
        "articulations": ["sustain"] if open_chords else ["palm_mute", "accent"],
        "performance_intent": {"attack": "tight", "release": "controlled", "picking": "alternate", "humanization": "action_based", "seed": 6200 + variant},
    }


def bass_phrase(section: str, variant: int) -> dict:
    energy = {"intro": .24, "verse_1": .4, "pre_chorus": .58, "chorus_1": .78,
              "verse_2": .5, "bridge_relay": .74, "final_chorus": .92, "outro": .32}[section]
    return {
        "instrument": "electric_bass", "role": "groove connector" if section != "bridge_relay" else "rising relay line",
        "phrase_type": "connecting_bass", "energy": energy, "harmony": harmony(section),
        "register_midi": [29, 52], "kick_offsets": [0, 2], "articulations": ["finger"],
        "performance_intent": {"attack": "finger", "release": "connected", "humanization": "action_based", "seed": 6300 + variant},
    }


def drum_phrase(section: str, variant: int) -> dict:
    chorus = section in {"chorus_1", "final_chorus"}
    energy = {"intro": .18, "verse_1": .36, "pre_chorus": .56, "chorus_1": .82,
              "verse_2": .46, "bridge_relay": .76, "final_chorus": 1.0, "outro": .3}[section]
    return {
        "instrument": "drum_kit", "role": "groove and structural propulsion",
        "phrase_type": "rock_chorus" if chorus or section == "bridge_relay" else "rock_verse",
        "bars": dict(SECTIONS)[section], "energy": energy,
        "transition_fill": section not in {"outro"},
        "performance_intent": {"attack": "tight", "release": "natural", "humanization": "limb_based", "seed": 6400 + variant},
    }


def organ_phrase(section: str, variant: int) -> dict:
    return {
        "instrument": "organ", "role": "voice-led harmonic plane",
        "phrase_type": "organ_voice_led_chords", "energy": {"intro": .24, "verse_1": .26, "pre_chorus": .46,
            "chorus_1": .6, "verse_2": .34, "final_chorus": .78, "outro": .28}[section],
        "harmony": harmony(section), "register_midi": [55, 76], "voices": 3,
        "performance_intent": {"attack": "soft", "release": "connected", "humanization": "voice_led", "seed": 6500 + variant},
    }


def strings_phrase(section: str, variant: int) -> dict:
    return {
        "instrument": "strings", "role": "emotional plane and inner movement",
        "phrase_type": "long_tones_inner_movement", "energy": {"intro": .18, "pre_chorus": .4, "chorus_1": .56,
            "verse_2": .32, "final_chorus": .82, "outro": .3}[section],
        "harmony": harmony(section), "register_midi": [60, 84], "voices": 3,
        "performance_intent": {"attack": "bowed", "release": "connected", "humanization": "voice_led", "seed": 6600 + variant},
    }


def bridge_counter_events(version: int) -> tuple[list[dict], list[dict]]:
    organ: list[dict] = []
    strings: list[dict] = []
    organ_pitches_a = ["D4", "F4", "G4", "A4", "C5", "D5", "E5", "F5"]
    organ_pitches_b = ["A4", "C5", "D5", "E5", "F5", "G5", "A5", "C6"]
    string_pitches_a = ["A4", "G4", "F4", "D4", "F4", "G4", "A4", "C5"]
    string_pitches_b = ["D5", "E5", "F5", "G5", "A5", "C6", "D6", "E6"]
    for bar in range(1, 9):
        organ.append(event(organ_pitches_a[bar - 1], bar, 1, 2.35, 66 + bar, ["tenuto"]))
        organ.append(event(organ_pitches_a[min(7, bar)], bar, 3.5, .42, 62 + bar, ["tenuto"]))
        strings.append(event(string_pitches_a[bar - 1], bar, 2, 1.65, 60 + bar, ["sustain"]))
    for bar in range(9, 17):
        idx = bar - 9
        organ.append(event(organ_pitches_b[idx], bar, 1, 1.15, 76 + idx, ["tenuto"]))
        organ.append(event(organ_pitches_b[min(7, idx + 1)], bar, 2.5, .65, 73 + idx, ["tenuto"]))
        organ.append(event(organ_pitches_b[idx], bar, 3.5, .38, 71 + idx, ["tenuto"]))
        strings.append(event(string_pitches_b[idx], bar, 1.5, 1.05, 69 + idx, ["sustain"]))
        strings.append(event(string_pitches_b[min(7, idx + 1)], bar, 3, .8, 67 + idx, ["sustain"]))
    if version >= 2:
        # Revision: clearer four-bar dialogue and a last-bar ascending handoff.
        organ.extend([event("D5", 15, 2, .38, 84, ["tenuto"]), event("F5", 15, 2.75, .38, 87, ["tenuto"]),
                      event("A5", 16, 2, .38, 91, ["tenuto"]), event("C6", 16, 2.75, .38, 94, ["tenuto"])])
        strings.extend([event("F5", 16, 1, .38, 86, ["sustain"]), event("A5", 16, 1.75, .38, 89, ["sustain"]),
                        event("D6", 16, 3.5, .42, 94, ["sustain"])])
    return organ, strings


def build(version: int) -> dict:
    section_defs = []
    energies = {"intro": "simple" if version >= 2 else "minimal", "verse_1": "simple", "pre_chorus": "standard", "chorus_1": "rich",
                "verse_2": "standard", "bridge_relay": "rich", "final_chorus": "rich", "outro": "simple"}
    budgets = {
        "intro": {"lead": 1, "rhythm": 2, "bass": 1, "drums": 1},
        "verse_1": {"lead": 3, "rhythm": 2, "bass": 2, "drums": 1},
        "pre_chorus": {"lead": 3, "rhythm": 3, "bass": 2, "drums": 2, "texture": 1},
        "chorus_1": {"lead": 4, "rhythm": 3, "bass": 2, "drums": 3, "texture": 3},
        "verse_2": {"lead": 3, "rhythm": 2, "bass": 2, "drums": 2, "texture": 2},
        "bridge_relay": {"lead": 0, "rhythm": 3, "bass": 3, "drums": 3, "texture": 5},
        "final_chorus": {"lead": 5, "rhythm": 3, "bass": 2, "drums": 3, "texture": 2},
        "outro": {"lead": 2, "rhythm": 2, "bass": 1, "drums": 1, "texture": 2},
    }
    for name, bars in SECTIONS:
        section_defs.append({"name": name, "bars": bars, "complexity": {"level": energies[name]}, "complexity_budget": budgets[name]})

    tracks = {
        "lead_guitar": {"role": "primary melody / lead guitar", "sound_library_profile": "general_midi", "sections": {}},
        "rhythm_guitar": {"role": "rhythmic harmony / bridge riff", "sound_library_profile": "general_midi", "sections": {}},
        "bass": {"role": "bass line / melodic bridge relay", "sound_library_profile": "general_midi", "sections": {}},
        "drums": {"role": "drums / propulsion", "sound_library_profile": "general_midi", "sections": {}},
        "organ": {"role": "harmonic plane / bridge counterline", "sound_library_profile": "general_midi", "sections": {}},
        "strings": {"role": "strings plane / bridge counterline", "sound_library_profile": "general_midi", "sections": {}},
    }
    for index, (name, bars) in enumerate(SECTIONS):
        if name != "bridge_relay":
            tracks["lead_guitar"]["sections"][name] = {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": lead_phrase(name, version * 100 + index)}
        tracks["rhythm_guitar"]["sections"][name] = {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": rhythm_phrase(name, version * 100 + index)}
        tracks["bass"]["sections"][name] = {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": bass_phrase(name, version * 100 + index)}
        tracks["drums"]["sections"][name] = {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": drum_phrase(name, version * 100 + index)}
        if name == "bridge_relay":
            organ, strings = bridge_counter_events(version)
            tracks["organ"]["sections"][name] = {"loop_bars": bars, "events": organ}
            tracks["strings"]["sections"][name] = {"loop_bars": bars, "events": strings}
        else:
            if name not in {"verse_1"}:
                tracks["organ"]["sections"][name] = {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": organ_phrase(name, version * 100 + index)}
            if name in {"intro", "pre_chorus", "chorus_1", "verse_2", "final_chorus", "outro"}:
                tracks["strings"]["sections"][name] = {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": strings_phrase(name, version * 100 + index)}

    return {
        "metadata": {"title": "Lanterns Against the Rain", "tempo": 106, "time_signature": "4/4", "key": "D minor", "composer_agent": "stable_epic_rock_composer"},
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 3, "arrangement": 5, "melodic_ornamentation": 3, "density": 3, "variation": 5},
        "complexity_contour": "custom",
        "rhythm_motifs": {
            "lantern_call": [{"offset": 0, "duration": 1.25}, {"offset": 1.5, "duration": .55}, {"offset": 2.25, "duration": .65}, {"offset": 3, "duration": .72}],
            "chorus_drive": [{"offset": 0, "duration": .5}, {"offset": .75, "duration": .5}, {"offset": 1.5, "duration": .75}, {"offset": 2.5, "duration": .45}, {"offset": 3, "duration": .8}],
        },
        "sections": section_defs,
        "tracks": tracks,
    }


def main() -> None:
    version = int(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else 1
    composition = build(version)
    target = ROOT / f"composition_v{version}.json"
    target.write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "composition.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
