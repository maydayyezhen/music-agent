from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEMPO = 108


def at(bar: int) -> str:
    return f"{bar}:1"


def harmony(chords: list[str]) -> list[dict]:
    return [{"at": at(index + 1), "duration": 4, "chord": chord} for index, chord in enumerate(chords)]


def harmony_spans(chords: list[str], octave: int = 3) -> list[dict]:
    pcs = {
        "C": (0, 4, 7), "D": (2, 6, 9), "E": (4, 8, 11), "F": (5, 9, 0),
        "G": (7, 11, 2), "A": (9, 1, 4), "B": (11, 3, 6), "F#": (6, 10, 1),
        "Bm": (11, 2, 6), "Em": (4, 7, 11), "F#m": (6, 9, 1),
    }
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    result = []
    for index, chord in enumerate(chords):
        key = chord if chord in pcs else chord.rstrip("5")
        values = []
        for pc in pcs[key]:
            midi = (octave + 1) * 12 + pc
            while midi < 55:
                midi += 12
            while midi > 78:
                midi -= 12
            values.append(f"{names[midi % 12]}{midi // 12 - 1}")
        result.append({"at": at(index + 1), "duration": 4, "pitches": values})
    return result


def power(chords: list[str]) -> list[dict]:
    return harmony([f"{c.rstrip('m')}5" for c in chords])


def intent(seed: int, attack: str = "intentional", release: str = "phrase_shaped") -> dict:
    return {"attack": attack, "release": release, "humanization": "action_based", "seed": seed}


MOTIF_SLOW = [
    {"offset": 0.5, "duration": 0.9, "degree": 0, "action": "pick"},
    {"offset": 1.65, "duration": 0.65, "degree": 3, "action": "hammer_on", "cross_bar": 1},
    {"offset": 3.55, "duration": 1.15, "degree": 5, "action": "slide", "cross_bar": 1},
    {"offset": 5.25, "duration": 0.8, "degree": 3, "action": "pull_off"},
    {"offset": 6.35, "duration": 1.55, "degree": 7, "action": "pick", "cross_bar": 1, "rest_type_after": "breath"},
]

MOTIF_DRIVE = [
    {"offset": 0.25, "duration": 0.55, "degree": 0, "action": "pick"},
    {"offset": 0.95, "duration": 0.45, "degree": 3, "action": "hammer_on"},
    {"offset": 1.55, "duration": 0.75, "degree": 5, "action": "slide", "cross_bar": 1},
    {"offset": 3.55, "duration": 0.5, "degree": 7, "action": "pick", "cross_bar": 1},
    {"offset": 4.35, "duration": 0.45, "degree": 5, "action": "pull_off"},
    {"offset": 5.05, "duration": 0.8, "degree": 8, "action": "pick"},
    {"offset": 6.15, "duration": 1.5, "degree": 10, "action": "slide", "cross_bar": 1, "rest_type_after": "breath"},
]


def curves(bars: int, peak: int, opening: float, top: float, close: float) -> tuple[list[float], list[float]]:
    energy = []
    density = []
    for bar in range(1, bars + 1):
        if bar <= peak:
            fraction = (bar - 1) / max(1, peak - 1)
            value = opening + (top - opening) * fraction
        else:
            fraction = (bar - peak) / max(1, bars - peak)
            value = top + (close - top) * fraction
        energy.append(round(value, 3))
        density.append(round(max(0.22, min(0.86, value * 0.72)), 3))
    return energy, density


def relation_plan(bars: int, peak: int, final_ops: list[str], climax_ops: list[str]) -> list[dict]:
    if bars == 16 and peak == 14:
        ranges = [(1, 4), (5, 8), (9, 14), (15, 16)]
    elif bars == 16:
        ranges = [(1, 4), (5, 8), (9, 12), (13, 16)]
    elif bars == 12 and peak == 10:
        ranges = [(1, 3), (4, 6), (7, 10), (11, 12)]
    elif bars == 12:
        ranges = [(1, 3), (4, 6), (7, 9), (10, 12)]
    elif bars == 8 and peak == 7:
        ranges = [(1, 2), (3, 4), (5, 7), (8, 8)]
    else:
        ranges = [(1, 2), (3, 4), (5, 6), (7, 8)]
    ids = ["A1", "A2", "B", "C"]
    kinds = ["introduce", "variation", "climax", "resolution"]
    ops = [[], ["transpose_up", "change_ending"], climax_ops, final_ops]
    result = []
    for index, ((start, end), phrase_id, kind, operations) in enumerate(zip(ranges, ids, kinds, ops)):
        result.append({
            "phrase_id": phrase_id,
            "bars": [start, end],
            "relationship": kind,
            "continuation_from": ids[index - 1] if index else None,
            "continuation_to": ids[index + 1] if index < 3 else None,
            "resolution": "strong" if index == 3 else ("weak" if index == 1 else "deferred"),
            "motif_operations": operations,
        })
    return result


def lead_phrase(
    section: str,
    chords: list[str],
    seed: int,
    peak: int,
    target: str,
    energy: float,
    motif: list[dict],
    root_midi: int,
    revision: int,
) -> dict:
    bars = len(chords)
    opening = max(0.28, energy - 0.34)
    top = min(1.0, energy + 0.08)
    close = max(0.30, energy - 0.20)
    energy_curve, density_curve = curves(bars, peak, opening, top, close)
    climax_ops = ["transpose_up", "compression", "rhythmic_extension"]
    final_ops = ["augmentation", "fragmentation"]
    if section == "final_chorus" and revision >= 2:
        climax_ops = ["transpose_up", "compression", "rhythmic_extension", "change_ending"]
        final_ops = ["augmentation", "fragmentation", "transpose_down"]
    motif_material = deepcopy(motif)
    if section == "final_chorus" and revision >= 2:
        # Extend the core cell through the six-bar climax node so the bar-14 target
        # is approached as one sentence instead of after several empty bars.
        motif_material.extend([
            {"offset": 10.7, "duration": 1.0, "degree": 5, "action": "pull_off", "cross_bar": 1},
            {"offset": 16.0, "duration": 1.1, "degree": 7, "action": "slide", "cross_bar": 1},
            {"offset": 21.4, "duration": 0.8, "degree": 8, "action": "hammer_on"},
            {"offset": 22.0, "duration": 1.4, "degree": 10, "action": "pick", "cross_bar": 1},
        ])
    return {
        "instrument": "electric_lead_guitar",
        "role": "lead",
        "phrase_type": "melodic_lead",
        "phrase_generation_mode": "long_form",
        "energy": energy,
        "performance_intent": intent(seed, "singing", "arc_shaped"),
        "key_root": "B",
        "register_midi": [57, 88],
        "motif_root_midi": root_midi,
        "motif_id": "dawn_cell",
        "motif_seed": motif_material,
        "harmony": harmony(chords),
        "section_arc": {
            "section_id": f"{section}_arc",
            "bars": [1, bars],
            "opening_register": "mid",
            "peak_register": "high" if peak >= bars // 2 else "mid_high",
            "peak_bar": peak,
            "final_resolution_bar": bars,
            "energy_curve": energy_curve,
            "density_curve": density_curve,
            "cadence_plan": {
                "strong_cadences": [bars],
                "weak_cadences": [max(2, bars // 2)],
                "avoid_resolution_bars": [max(2, bars // 3), peak],
            },
            "breath_bars": [max(2, bars // 4), max(3, bars // 2), max(4, bars - 2)],
            "cross_bar_note_bars": [2, max(3, bars // 2), max(4, peak), max(5, bars - 2)],
            "delayed_target": {"pitch": target, "bar": peak},
        },
        "phrase_relationships": relation_plan(bars, peak, final_ops, climax_ops),
        "long_form_phrase_rules": {
            "planning_window_bars": bars,
            "minimum_connected_span_bars": min(8, bars),
            "maximum_strong_cadences_per_8_bars": 1,
            "minimum_cross_bar_notes_per_8_bars": 2,
            "minimum_motif_developments_per_section": 3,
            "maximum_independent_phrase_resets_per_8_bars": 1,
            "maximum_consecutive_full_rest_bars": 1,
            "require_delayed_peak": True,
            "require_delayed_resolution": True,
        },
    }


def phrase_clip(phrase: dict, bars: int) -> dict:
    return {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": phrase}


def rhythm_phrase(chords: list[str], seed: int, energy: float, kind: str, subdivision: float, rest_steps: list[int]) -> dict:
    return {
        "instrument": "electric_rhythm_guitar",
        "role": "rhythm",
        "phrase_type": kind,
        "energy": energy,
        "performance_intent": {**intent(seed, "pick_defined", "controlled"), "picking": "alternate"},
        "harmony": power(chords),
        "subdivision": subdivision,
        "gate": 0.38 if kind == "palm_muted_eighths" else 0.83,
        "strum_spread": 0.045 if kind == "palm_muted_eighths" else 0.07,
        "rest_steps": rest_steps,
        "articulations": ["palm_mute"] if kind == "palm_muted_eighths" else ["sustain"],
    }


def bass_phrase(chords: list[str], seed: int, energy: float, kicks: list[float]) -> dict:
    return {
        "instrument": "electric_bass", "role": "bass", "phrase_type": "connecting_bass",
        "energy": energy, "performance_intent": intent(seed, "fingered", "connected"),
        "harmony": harmony(chords), "kick_offsets": kicks, "register_midi": [28, 50],
        "articulations": ["finger"],
    }


def drum_phrase(bars: int, seed: int, energy: float, kind: str, fill: bool = True) -> dict:
    return {
        "instrument": "drum_kit", "role": "drums", "phrase_type": kind, "energy": energy,
        "performance_intent": intent(seed, "tight_anchors", "groove_shaped"),
        "bars": bars, "transition_fill": fill,
    }


def strings_phrase(chords: list[str], seed: int, energy: float, register: list[int]) -> dict:
    return {
        "instrument": "strings", "role": "counter_motion", "phrase_type": "long_tones_inner_movement",
        "energy": energy, "performance_intent": intent(seed, "bowed", "sustained_arc"),
        "harmony": harmony(chords), "register_midi": register, "voices": 3,
    }


def explicit_organ_bridge(build: bool, revision: int) -> list[dict]:
    if not build:
        notes = [(1, 2.5, "F#4", 1.2), (2, 3.0, "A4", 0.8), (3, 2.0, "B4", 1.4), (4, 3.25, "D5", 0.65),
                 (5, 2.5, "C#5", 1.1), (6, 3.0, "B4", 0.85), (7, 2.0, "A4", 1.5), (8, 3.25, "F#4", 0.65)]
    else:
        notes = [(1, 1.5, "G4", 0.7), (1, 3.0, "A4", 0.7), (2, 2.0, "B4", 0.9), (3, 1.5, "D5", 0.7),
                 (3, 3.0, "E5", 0.7), (4, 2.0, "F#5", 1.2), (5, 1.5, "A4", 0.6), (5, 2.5, "B4", 0.6),
                 (6, 1.5, "C#5", 0.6), (6, 2.5, "D5", 0.6), (7, 1.5, "E5", 0.6), (7, 2.5, "F#5", 0.8),
                 (8, 2.0, "A5" if revision >= 2 else "F#5", 1.6)]
    if revision >= 2:
        notes = [(bar, beat, pitch, duration * (1.22 if build else 1.12)) for bar, beat, pitch, duration in notes]
    return [{"type": "note", "pitch": pitch, "at": f"{bar}:{beat}", "duration": duration,
             "velocity": 68 + (bar if build else bar // 2)} for bar, beat, pitch, duration in notes]


def make_composition(revision: int) -> dict:
    progressions = {
        "intro": ["Bm", "G", "D", "A", "Bm", "G", "Em", "F#"],
        "verse1": ["Bm", "G", "D", "A", "Bm", "G", "Em", "F#", "Bm", "A", "G", "F#"],
        "pre_chorus": ["G", "A", "Bm", "Bm", "G", "A", "F#", "F#"],
        "chorus1": ["D", "A", "Bm", "G", "D", "A", "G", "A", "Bm", "G", "D", "A", "Em", "G", "A", "Bm"],
        "verse2": ["Bm", "A", "G", "D", "Em", "G", "D", "F#", "Bm", "G", "A", "F#"],
        "bridge_void": ["Bm", "Bm", "G", "G", "Em", "Em", "F#", "F#"],
        "bridge_build": ["G", "A", "Bm", "D", "Em", "G", "A", "F#"],
        "final_chorus": ["D", "A", "Bm", "G", "D", "A", "G", "A", "Bm", "G", "D", "A", "Em", "G", "A", "Bm"],
        "outro": ["Bm", "G", "D", "A", "Em", "G", "F#", "Bm"],
    }
    sections = [
        ("intro", 8, "simple", 0.28), ("verse1", 12, "standard", 0.42),
        ("pre_chorus", 8, "rich", 0.61), ("chorus1", 16, "rich", 0.84),
        ("verse2", 12, "standard", 0.48), ("bridge_void", 8, "simple", 0.36),
        ("bridge_build", 8, "rich", 0.76), ("final_chorus", 16, "dense", 1.0),
        ("outro", 8, "simple", 0.34),
    ]
    composition = {
        "metadata": {"title": "When the Horizon Answers", "tempo": TEMPO, "time_signature": "4/4", "key": "B minor"},
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 4, "arrangement": 5,
                       "melodic_ornamentation": 3, "density": 3, "variation": 5},
        "complexity_contour": "custom",
        "sections": [
            {"name": name, "bars": bars, "complexity": level,
             "complexity_budget": ({
                 "lead": 0, "rhythm": 2, "bass": 2, "drums": 2, "texture": 2,
             } if name == "bridge_void" else {
                 "lead": 0 if name == "bridge_build" else (4 if name in {"chorus1", "final_chorus"} else 2),
                 "rhythm": 3 if name in {"chorus1", "final_chorus", "bridge_build"} else 2,
                 "bass": 2 if name in {"chorus1", "pre_chorus"} else (3 if name in {"final_chorus", "bridge_build"} else 2),
                 "drums": 4 if name in {"chorus1", "final_chorus", "bridge_build"} else 1,
                 "texture": 3 if name == "bridge_build" or name == "final_chorus" else (2 if name == "chorus1" else 1),
             }),
             "energy_target": energy}
            for name, bars, level, energy in sections
        ],
        "rhythm_motifs": {
            "horizon_call": [{"offset": 0.5, "duration": 0.9}, {"offset": 1.65, "duration": 0.65},
                             {"offset": 3.55, "duration": 1.15}, {"offset": 5.25, "duration": 0.8}],
            "chorus_drive": [{"offset": 0.25, "duration": 0.55}, {"offset": 0.95, "duration": 0.45},
                              {"offset": 1.55, "duration": 0.75}, {"offset": 3.55, "duration": 0.5}],
        },
        "tracks": {},
    }

    # Lead: every substantial 8-16 bar statement is truly planned as one long form.
    lead_specs = {
        "intro": (6, "D5", 0.48, MOTIF_SLOW, 59),
        "verse1": (9, "F#5", 0.60, MOTIF_SLOW, 59),
        "pre_chorus": (7, "A5", 0.72, MOTIF_DRIVE, 62),
        "chorus1": (12, "D6", 0.88, MOTIF_DRIVE, 66),
        "verse2": (10, "B5", 0.66, MOTIF_SLOW, 62),
        "final_chorus": ((14 if revision >= 2 else 12), ("E6" if revision >= 2 else "D6"),
                          (1.0 if revision >= 2 else 0.89), MOTIF_DRIVE, 66),
        "outro": (6, "B5", 0.58, MOTIF_SLOW, 59),
    }
    lead_sections = {}
    for index, (name, (peak, target, energy, motif, root_midi)) in enumerate(lead_specs.items()):
        chords = progressions[name]
        phrase = lead_phrase(name, chords, 200 + index + revision * 20, peak, target,
                             energy, motif, root_midi, revision)
        if revision >= 2:
            phrase["long_form_phrase_rules"]["maximum_consecutive_full_rest_bars"] = 2
        lead_sections[name] = phrase_clip(phrase, len(chords))
    composition["tracks"]["lead_guitar"] = {"role": "primary melodic narrator", "sections": lead_sections}

    rhythm_sections = {}
    for index, (name, chords) in enumerate(progressions.items()):
        bars = len(chords)
        if name in {"chorus1", "final_chorus"}:
            kind, sub, energy = "open_power_chords", 0.5, 0.86 if name == "chorus1" else (0.98 if revision >= 2 else 0.87)
            rests = [step for step in range(bars * 8) if step % 16 in {14, 15}]
            if name == "final_chorus" and revision >= 2:
                rests = [step for step in range(bars * 8) if step % 32 in {30, 31}]
        elif name == "bridge_void":
            kind, sub, energy = "palm_muted_eighths", 1.0, 0.38
            rests = [step for step in range(bars * 4) if step % 4 in {1, 3}]
        elif name == "bridge_build":
            kind, sub, energy = "palm_muted_eighths", 0.5, 0.78
            rests = [step for step in range(bars * 8) if step < 16 and step % 2 == 1]
            if revision == 1:
                rests += [step for step in range(16, bars * 8) if step % 8 in {6, 7}]
            else:
                rests += [step for step in range(16, bars * 8) if step % 16 == 15]
        elif name == "pre_chorus":
            kind, sub, energy = "palm_muted_eighths", 0.5, 0.68
            rests = [step for step in range(bars * 8) if step % 16 in {7, 15}]
        else:
            kind, sub, energy = "palm_muted_eighths", 1.0, 0.42 if name != "verse2" else 0.49
            rests = [step for step in range(bars * 4) if step % 8 in {3, 7}]
        rhythm_sections[name] = phrase_clip(rhythm_phrase(chords, 300 + index + revision * 20, energy, kind, sub, rests), bars)
    composition["tracks"]["rhythm_guitar"] = {"role": "physical power-chord and pulse engine", "sections": rhythm_sections}

    bass_sections = {}
    for index, (name, chords) in enumerate(progressions.items()):
        energy = {"intro": .36, "verse1": .48, "pre_chorus": .64, "chorus1": .82, "verse2": .53,
                  "bridge_void": .48, "bridge_build": .75, "final_chorus": .94, "outro": .38}[name]
        kicks = [0, 2] if name not in {"chorus1", "bridge_build", "final_chorus"} else [0, 1.5, 2, 3.5]
        bass_sections[name] = phrase_clip(bass_phrase(chords, 400 + index + revision * 20, energy, kicks), len(chords))
    composition["tracks"]["bass"] = {"role": "harmonic connector and bridge relay", "sections": bass_sections}

    drum_sections = {}
    for index, (name, bars, _, _) in enumerate(sections):
        chorus = name in {"chorus1", "bridge_build", "final_chorus"}
        kind = "chorus_with_fill" if chorus else "rock_verse"
        energy = {"intro": .25, "verse1": .40, "pre_chorus": .59, "chorus1": .84, "verse2": .46,
                  "bridge_void": .34, "bridge_build": .78, "final_chorus": .98, "outro": .30}[name]
        drum_sections[name] = phrase_clip(drum_phrase(bars, 500 + index + revision * 20, energy, kind, name != "outro"), bars)
    composition["tracks"]["drums"] = {"role": "sectional pulse and explosive transitions", "sections": drum_sections}

    organ_sections = {}
    for name, chords in progressions.items():
        bars = len(chords)
        if name.startswith("bridge"):
            build = name == "bridge_build"
            organ_sections[name] = {
                "loop_bars": bars,
                "texture": "counterline",
                "continuity": {"sustain_ratio": .55, "legato_ratio": .78, "overlap": .04,
                               "common_tone_retention": .64, "voice_leading_strength": .9},
                "harmony_spans": harmony_spans(chords, 3 if not build else 4),
                "texture_pattern": {
                    "register": [60, 78] if not build else [64, 84], "voices": 4,
                    "velocity": 57 if not build else 68,
                    "offsets": [0.5, 2.0, 3.25] if not build else [0.25, 1.5, 2.5, 3.35],
                    "durations": ([1.55, 1.15, .85] if revision >= 2 else [1.2, .8, .55]) if not build else
                                 ([1.05, 1.0, .85, .7] if revision >= 2 else [.7, .7, .55, .45]),
                },
                "events": explicit_organ_bridge(build, revision),
            }
        else:
            if revision >= 2 and name in {"verse1", "verse2", "outro"}:
                organ_sections[name] = {
                    "loop_bars": bars, "texture": "sustain",
                    "continuity": {"sustain_ratio": .92, "legato_ratio": .92, "overlap": .03,
                                   "common_tone_retention": .95, "voice_leading_strength": .95},
                    "harmony_spans": harmony_spans(chords, 3),
                    "texture_pattern": {"register": [50, 69], "voices": 2, "velocity": 42,
                                        "strum_spread": .015},
                    "events": [],
                }
            else:
                organ_sections[name] = phrase_clip({
                    "instrument": "organ", "role": "harmonic_plane", "phrase_type": "organ_voice_led_chords",
                    "energy": .30 if name in {"intro", "outro"} else (.68 if "chorus" in name else .42),
                    "performance_intent": intent(600 + list(progressions).index(name) + revision * 20, "finger_legato", "held"),
                    "harmony": harmony(chords), "register_midi": [55, 76] if "chorus" not in name else [59, 80], "voices": 3,
                }, bars)
    composition["tracks"]["organ"] = {"role": "harmonic plane and bridge relay", "sections": organ_sections}

    string_sections = {}
    for index, (name, chords) in enumerate(progressions.items()):
        if name in {"verse1", "verse2"}:
            continue
        energy = {"intro": .32, "pre_chorus": .52, "chorus1": .67, "bridge_void": .45,
                  "bridge_build": .76, "final_chorus": .92, "outro": .38}[name]
        register = [55, 79] if name != "final_chorus" else ([60, 86] if revision >= 2 else [58, 82])
        string_sections[name] = phrase_clip(strings_phrase(chords, 700 + index + revision * 20, energy, register), len(chords))
    composition["tracks"]["strings"] = {"role": "emotional long arc and bridge ascent", "sections": string_sections}
    return composition


INSTRUMENTS = {
    "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30, "gm_name": "Distortion Guitar"},
    "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29, "gm_name": "Overdriven Guitar"},
    "bass": {"engine": "fluidsynth", "bank": 0, "program": 33, "gm_name": "Electric Bass finger"},
    "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16, "gm_name": "Power Drum Kit"},
    "organ": {"engine": "fluidsynth", "bank": 0, "program": 18, "gm_name": "Rock Organ"},
    "strings": {"engine": "fluidsynth", "bank": 0, "program": 48, "gm_name": "String Ensemble 1"},
}

RENDER = {
    "sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.72,
    "tail_seconds": 3.0, "master_peak_db": -1.0,
    "mix": {
        "lead_guitar": {"volume_db": -3.5, "pan": 0.16, "mute": False},
        "rhythm_guitar": {"volume_db": -6.0, "pan": -0.34, "mute": False},
        "bass": {"volume_db": -4.5, "pan": 0.0, "mute": False},
        "drums": {"volume_db": -8.0, "pan": 0.0, "mute": False},
        "organ": {"volume_db": -8.5, "pan": 0.30, "mute": False},
        "strings": {"volume_db": -10.0, "pan": -0.10, "mute": False},
    },
}


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("revision", type=int, choices=[1, 2])
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    composition = make_composition(args.revision)
    write_json(ROOT / f"composition_v{args.revision}.json", composition)
    write_json(ROOT / "composition.json", composition)
    write_json(ROOT / "instruments.json", INSTRUMENTS)
    write_json(ROOT / "render.json", RENDER)
