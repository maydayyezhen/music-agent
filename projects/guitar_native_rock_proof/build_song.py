from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BEATS = 4
SEED = 116042


def at(beat: float) -> str:
    bar = int(beat // BEATS) + 1
    local = beat % BEATS + 1
    return f"{bar}:{local:.3f}".rstrip("0").rstrip(".")


FRETBOARD: dict[str, dict[str, tuple[int, int]]] = {
    "mid_7": {
        "E4": (3, 9), "G4": (4, 8), "A4": (4, 10), "B4": (5, 7),
        "D5": (5, 10), "E5": (5, 12),
    },
    "upper_12": {
        "E4": (2, 14), "G4": (3, 12), "A4": (3, 14), "B4": (4, 12), "D5": (4, 15),
        "E5": (5, 12), "G5": (5, 15), "A5": (5, 17), "B5": (5, 19), "D6": (5, 22),
    },
    "high_17": {
        "B4": (3, 16), "D5": (4, 15), "E5": (4, 17), "G5": (5, 15),
        "A5": (5, 17), "B5": (5, 19), "D6": (5, 22), "E6": (5, 24),
    },
}


def add_stream(
    target: list[dict],
    start: float,
    end: float,
    pitches: list[str],
    iois: list[float],
    position: str,
    velocity: int,
    slide_in: bool = False,
    accent_every: int = 0,
) -> None:
    cursor = start
    index = 0
    previous_pitch: str | None = target[-1]["pitch"] if target else None
    previous_fingering: tuple[int, int] | None = None
    if target:
        previous_fingering = (int(target[-1].get("planned_string", -1)), int(target[-1].get("planned_fret", -1)))
    while cursor < end - 0.06:
        pitch = pitches[index % len(pitches)]
        ioi = min(iois[index % len(iois)], end - cursor)
        fingering = FRETBOARD[position][pitch]
        arts: list[str] = ["sustain"]
        if index == 0 and slide_in:
            arts = ["slide", "accent"]
        elif previous_pitch == pitch:
            arts = ["accent"]
        elif previous_fingering and fingering[0] == previous_fingering[0]:
            delta = fingering[1] - previous_fingering[1]
            if 0 < delta <= 3:
                arts = ["hammer_on", "legato"]
            elif -3 <= delta < 0:
                arts = ["pull_off", "legato"]
        if accent_every and index % accent_every == 0 and "accent" not in arts:
            arts.append("accent")
        duration = max(0.08, ioi * (0.98 if set(arts) & {"legato", "slide"} else 0.91))
        event = {
            "pitch": pitch,
            "at": at(cursor),
            "duration": round(duration, 3),
            "velocity": min(116, velocity + (6 if "accent" in arts else 0) + (index % 3 - 1)),
            "articulations": arts,
            "planned_position": position,
            "planned_string": fingering[0],
            "planned_fret": fingering[1],
        }
        if "slide" in arts:
            event["slide_from_semitones"] = -2.0
        target.append(event)
        previous_pitch = pitch
        previous_fingering = fingering
        cursor += ioi
        index += 1


def special_note(
    target: list[dict], start: float, pitch: str, duration: float, position: str,
    velocity: int, articulations: list[str], **extra: object,
) -> None:
    string, fret = FRETBOARD[position][pitch]
    target.append({
        "pitch": pitch, "at": at(start), "duration": duration, "velocity": velocity,
        "articulations": articulations, "planned_position": position,
        "planned_string": string, "planned_fret": fret, **extra,
    })


def theme_a() -> list[dict]:
    events: list[dict] = []
    add_stream(events, 0, 16, ["E4", "G4", "A4", "B4", "A4", "G4", "E4", "G4"],
               [0.5, 0.5, 0.5, 0.75, 0.25, 0.5, 0.75, 0.25], "mid_7", 84)
    add_stream(events, 16, 32, ["G4", "A4", "B4", "D5", "B4", "A4", "G4", "A4"],
               [0.5, 0.5, 0.75, 0.25, 0.5, 0.5, 1.0], "mid_7", 87, True)
    add_stream(events, 32, 48, ["B4", "B4", "D5", "E5", "D5", "B4", "A4", "B4"],
               [0.5, 0.25, 0.25, 0.5, 0.5, 0.75, 0.25, 1.0], "mid_7", 90, True, 4)
    add_stream(events, 48, 64, ["A4", "B4", "D5", "E5", "D5", "B4", "A4", "G4", "E4", "G4"],
               [0.25, 0.25, 0.5, 0.75, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75], "mid_7", 92, True)
    return events


def theme_b() -> list[dict]:
    events: list[dict] = []
    add_stream(events, 0, 16, ["G4", "A4", "B4", "D5", "E5", "D5", "B4", "A4"],
               [0.5, 0.5, 0.25, 0.25, 0.75, 0.25, 0.5, 1.0], "upper_12", 91, True)
    add_stream(events, 16, 32, ["B4", "D5", "E5", "G5", "E5", "D5", "B4", "D5"],
               [0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75], "upper_12", 94, True)
    add_stream(events, 32, 48, ["E5", "E5", "G5", "A5", "G5", "E5", "D5", "E5"],
               [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 1.0, 1.0], "upper_12", 96, True, 3)
    add_stream(events, 48, 62, ["D5", "E5", "G5", "A5", "G5", "E5", "D5", "B4"],
               [0.25, 0.25, 0.5, 0.75, 0.25, 0.5, 0.75, 0.75], "upper_12", 98, True)
    special_note(events, 62, "B4", 1.9, "upper_12", 102, ["bend", "vibrato"], bend_semitones=2.0,
                 vibrato={"delay": 0.8, "depth": 0.24, "rate": 5.0})
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def solo() -> list[dict]:
    events: list[dict] = []
    # Bars 1-8: motif-derived, mid-register, continuous and unresolved.
    add_stream(events, 0, 32, ["E4", "G4", "A4", "B4", "A4", "G4", "E4", "G4", "A4", "B4"],
               [0.5, 0.5, 0.75, 0.25, 0.5, 0.5, 1.0, 0.5], "mid_7", 88, False, 7)
    # Bars 9-16: sequence upward, repeated notes and legato groups.
    add_stream(events, 32, 64, ["G4", "A4", "B4", "B4", "D5", "E5", "D5", "B4", "A4", "B4"],
               [0.5, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.75, 0.25, 0.5], "upper_12", 94, True, 6)
    # Bars 17-24: denser long runs that approach, but do not settle in, the high register.
    add_stream(events, 64, 96, ["B4", "D5", "E5", "G5", "A5", "G5", "E5", "D5", "E5", "G5", "A5", "G5"],
               [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.75, 0.75], "upper_12", 99, True, 8)
    # Bars 25-28: acceleration into a bent E6 target; release keeps moving.
    add_stream(events, 96, 101.5, ["E5", "G5", "A5", "B5", "A5", "G5", "A5", "B5"],
               [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25], "high_17", 104, True, 5)
    special_note(events, 101.5, "D6", 2.0, "high_17", 113, ["bend", "vibrato"], bend_semitones=2.0,
                 vibrato={"delay": 1.1, "depth": 0.28, "rate": 5.4})
    add_stream(events, 103.5, 108.0, ["E6", "D6", "B5", "A5", "B5", "D6"],
               [0.5, 0.25, 0.25, 0.5, 0.5, 0.25], "high_17", 107)
    special_note(events, 108.0, "D6", 1.5, "high_17", 109, ["bend_release"], bend_semitones=2.0)
    add_stream(events, 109.5, 112.0, ["B5", "A5", "G5", "E5", "G5"],
               [0.25, 0.25, 0.5, 0.5, 0.5], "high_17", 103)
    # Bars 29-32: descend through the motif and walk directly into Final Theme.
    add_stream(events, 112, 128, ["B5", "A5", "G5", "E5", "D5", "B4", "A4", "G4", "E4", "G4", "A4", "B4"],
               [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.5, 0.75, 0.25, 0.5, 0.75], "upper_12", 96, True)
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def final_theme() -> list[dict]:
    events: list[dict] = []
    add_stream(events, 0, 24, ["E5", "G5", "A5", "B5", "A5", "G5", "E5", "G5"],
               [0.5, 0.5, 0.25, 0.25, 0.75, 0.25, 0.5, 1.0], "high_17", 100, True)
    add_stream(events, 24, 48, ["G5", "A5", "B5", "D6", "B5", "A5", "G5", "E5", "G5"],
               [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.75, 0.75, 0.5], "high_17", 105, True, 6)
    add_stream(events, 48, 62, ["E5", "G5", "A5", "B5", "D6", "B5", "A5", "G5", "E5"],
               [0.25, 0.25, 0.5, 0.75, 0.25, 0.5, 0.5, 0.75], "high_17", 108, True)
    special_note(events, 62, "E5", 1.95, "high_17", 112, ["sustain", "vibrato"],
                 vibrato={"delay": 0.9, "depth": 0.22, "rate": 4.8})
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def intro_lead() -> list[dict]:
    events: list[dict] = []
    add_stream(events, 16, 31.5, ["E4", "G4", "A4", "B4", "A4", "G4", "E4"],
               [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.5], "mid_7", 76)
    return events


def outro_lead() -> list[dict]:
    events: list[dict] = []
    add_stream(events, 0, 24, ["E5", "D5", "B4", "A4", "G4", "E4"],
               [0.5, 0.5, 0.75, 0.25, 1.0, 1.0], "upper_12", 87)
    special_note(events, 24, "E4", 7.5, "mid_7", 82, ["sustain", "vibrato"],
                 vibrato={"delay": 2.0, "depth": 0.16, "rate": 4.4})
    return events


SECTIONS = [
    ("intro", 8, 4), ("theme_a", 16, 7), ("theme_b", 16, 8),
    ("bridge", 8, 5), ("main_solo", 32, 9), ("final_theme", 16, 10), ("outro", 8, 3),
]


HARMONY = {
    "intro": ["Em", "C", "G", "D", "Em", "C", "Am", "B"],
    "theme_a": ["Em", "C", "G", "D", "Em", "C", "Am", "B"] * 2,
    "theme_b": ["C", "G", "D", "Em", "C", "G", "Am", "B"] * 2,
    "bridge": ["Am", "Em", "C", "B", "Am", "C", "D", "B"],
    "main_solo": (["Em", "D", "C", "B", "Em", "G", "Am", "B"] * 4),
    "final_theme": ["C", "G", "D", "Em", "C", "G", "Am", "B", "C", "G", "D", "Em", "Am", "C", "B", "Em"],
    "outro": ["Em", "D", "C", "B", "Em", "C", "B", "Em"],
}


def harmony(section: str) -> list[dict]:
    return [{"at": f"{index + 1}:1", "duration": 4, "chord": chord}
            for index, chord in enumerate(HARMONY[section])]


def phrase(instrument: str, role: str, phrase_type: str, section: str, energy: float, seed: int, **extra: object) -> dict:
    value = {
        "instrument": instrument, "role": role, "phrase_type": phrase_type,
        "energy": energy, "performance_intent": {
            "attack": "physical", "release": "controlled", "humanization": "action_based", "seed": seed,
        },
        **extra,
    }
    if phrase_type not in {"melodic_lead", "lead_melody"}:
        value["harmony"] = harmony(section)
    return value


def lead_clip(section: str, events: list[dict], energy: float, seed: int) -> dict:
    return {
        "loop_bars": dict((name, bars) for name, bars, _ in SECTIONS)[section],
        "sound_library_profile": "general_midi",
        "instrument_phrase": phrase(
            "electric_lead_guitar", "continuous guitar-native foreground", "melodic_lead",
            section, energy, seed, motif=events, phrase_generation_mode="legacy_stable",
            articulations=["sustain"],
        ),
    }


def build() -> dict:
    section_rows = []
    for name, bars, energy in SECTIONS:
        level = "rich" if name in {"theme_b", "main_solo"} else ("dense" if name == "final_theme" else "standard")
        section_rows.append({
            "name": name, "bars": bars, "energy": energy, "complexity": {"level": level},
            "complexity_budget": {"lead": 5 if name != "bridge" else 0, "rhythm": 3, "bass": 3, "drums": 4, "texture": 1},
        })

    lead_sections = {
        "intro": lead_clip("intro", intro_lead(), 0.45, SEED + 1),
        "theme_a": lead_clip("theme_a", theme_a(), 0.66, SEED + 2),
        "theme_b": lead_clip("theme_b", theme_b(), 0.78, SEED + 3),
        "main_solo": lead_clip("main_solo", solo(), 0.94, SEED + 4),
        "final_theme": lead_clip("final_theme", final_theme(), 1.0, SEED + 5),
        "outro": lead_clip("outro", outro_lead(), 0.5, SEED + 6),
    }

    rhythm_sections = {}
    bass_sections = {}
    drum_sections = {}
    organ_sections = {}
    for index, (name, bars, energy) in enumerate(SECTIONS):
        open_section = name in {"theme_b", "final_theme", "outro"}
        rhythm_sections[name] = {
            "loop_bars": bars, "sound_library_profile": "general_midi",
            "instrument_phrase": phrase(
                "electric_rhythm_guitar", "right-hand rock pulse", "open_power_chords" if open_section else "palm_muted_eighths",
                name, min(1.0, energy / 10 + 0.1), SEED + 100 + index,
                subdivision=1.0 if open_section else 0.5,
                gate=0.9 if open_section else 0.42,
                rest_steps=([1, 5, 13, 29] if name == "intro" else ([7, 15, 31, 47] if name == "main_solo" else [])),
                articulations=["sustain", "accent"] if open_section else ["palm_mute", "accent"],
            ),
        }
        bass_sections[name] = {
            "loop_bars": bars, "sound_library_profile": "general_midi",
            "instrument_phrase": phrase(
                "electric_bass", "connecting low line", "connecting_bass", name,
                min(1.0, energy / 10 + 0.08), SEED + 200 + index,
                register_midi=[28, 52], kick_offsets=[0, 2], articulations=["pick"],
            ),
        }
        drum_sections[name] = {
            "loop_bars": bars, "sound_library_profile": "general_midi",
            "instrument_phrase": phrase(
                "drum_kit", "sectional rock propulsion",
                "rock_chorus" if name in {"theme_b", "main_solo", "final_theme"} else "rock_verse",
                name, min(1.0, energy / 10 + 0.1), SEED + 300 + index,
                bars=bars, transition_fill=name not in {"intro", "outro"},
            ),
        }
        if name in {"bridge", "main_solo", "final_theme", "outro"}:
            organ_sections[name] = {
                "loop_bars": bars, "sound_library_profile": "general_midi",
                "instrument_phrase": phrase(
                    "organ", "slow upper harmonic plane", "organ_voice_led_chords", name,
                    0.30 if name == "bridge" else (0.46 if name == "main_solo" else 0.55),
                    SEED + 400 + index, register_midi=[57, 78], voices=3,
                ),
            }

    return {
        "metadata": {
            "title": "The Distance Still Burns", "tempo": 116, "time_signature": "4/4",
            "key": "E minor", "seed": SEED, "composer_note": "fixed V1/V2 proof song",
        },
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 3, "arrangement": 4,
                       "melodic_ornamentation": 4, "density": 3, "variation": 5},
        "complexity_contour": "wave",
        "rhythm_motifs": {
            "guitar_cell": [{"offset": 0, "duration": 0.5}, {"offset": 0.5, "duration": 0.5},
                            {"offset": 1.0, "duration": 0.75}, {"offset": 1.75, "duration": 0.25}],
            "rock_drive": [{"offset": 0, "duration": 0.5}, {"offset": 1, "duration": 0.5},
                           {"offset": 2, "duration": 0.5}, {"offset": 3.5, "duration": 0.5}],
        },
        "core_motif": {
            "motif_id": "main_guitar_motif",
            "scale_basis": "E minor pentatonic with natural minor color tones",
            "register": "mid",
            "rhythmic_identity": "two eighths, compressed ascent, syncopated turn, long connection",
            "contour": "E4-G4-A4-B4 then folds through A4-G4 toward E4",
            "guitar_position": "7th-position connected shape across G, B and high-E strings",
            "notes": [
                {"pitch": "E4", "offset": 0, "duration": 0.5}, {"pitch": "G4", "offset": 0.5, "duration": 0.5},
                {"pitch": "A4", "offset": 1, "duration": 0.5}, {"pitch": "B4", "offset": 1.5, "duration": 0.75},
                {"pitch": "A4", "offset": 2.25, "duration": 0.25}, {"pitch": "G4", "offset": 2.5, "duration": 0.5},
                {"pitch": "E4", "offset": 3, "duration": 1.0},
            ],
            "development_options": ["sequence_up", "rhythmic_compression", "extended_ending", "bend_target", "fragmentation"],
        },
        "sections": section_rows,
        "tracks": {
            "lead_guitar": {"role": "guitar-native melodic lead", "sound_library_profile": "general_midi", "sections": lead_sections},
            "rhythm_guitar": {"role": "physical rhythm guitar", "sound_library_profile": "general_midi", "sections": rhythm_sections},
            "bass": {"role": "independent connecting bass", "sound_library_profile": "general_midi", "sections": bass_sections},
            "drums": {"role": "rock drum kit", "sound_library_profile": "general_midi", "sections": drum_sections},
            "organ": {"role": "restrained harmonic plane", "sound_library_profile": "general_midi", "sections": organ_sections},
        },
    }


def main() -> None:
    composition = build()
    text = json.dumps(composition, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "composition.json").write_text(text, encoding="utf-8")
    (ROOT / "v1" / "composition.json").write_text(text, encoding="utf-8")
    (ROOT / "v1" / "composition.normalized.json").write_text(
        json.dumps(deepcopy(composition), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "core_motif.json").write_text(
        json.dumps(composition["core_motif"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
