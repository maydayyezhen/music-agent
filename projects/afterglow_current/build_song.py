from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BEATS_PER_BAR = 4
TEMPO = 108
SEED = 814108

SECTIONS = [
    ("intro", 4, 3),
    ("theme_a", 8, 5),
    ("theme_b", 8, 7),
    ("peak", 8, 9),
    ("outro", 4, 4),
]

HARMONY = {
    "intro": ["Em", "C", "G", "D"],
    "theme_a": ["Em", "C", "G", "D", "Em", "C", "G", "D"],
    "theme_b": ["C", "G", "D", "Em", "C", "G", "D", "B"],
    "peak": ["Em", "C", "G", "D", "C", "D", "Em", "B"],
    "outro": ["Em", "C", "G", "Em"],
}

# Standard tuning, string index 0 = low E, 5 = high E.
FRETBOARD: dict[str, dict[str, tuple[int, int]]] = {
    "mid_b_string": {
        "E4": (4, 5),
        "G4": (4, 8),
        "A4": (4, 10),
        "B4": (4, 12),
        "D5": (5, 10),
        "E5": (5, 12),
    },
    "upper_high_e": {
        "E4": (5, 0),
        "G4": (5, 3),
        "A4": (5, 5),
        "B4": (5, 7),
        "D5": (5, 10),
        "E5": (5, 12),
        "G5": (5, 15),
        "A5": (5, 17),
        "B5": (5, 19),
    },
}


def at(beat: float) -> str:
    bar = int(beat // BEATS_PER_BAR) + 1
    local = beat % BEATS_PER_BAR + 1
    return f"{bar}:{local:.3f}".rstrip("0").rstrip(".")


def harmony(section: str) -> list[dict]:
    return [
        {"at": f"{bar}:1", "duration": 4, "chord": chord}
        for bar, chord in enumerate(HARMONY[section], 1)
    ]


def add_stream(
    target: list[dict],
    start: float,
    end: float,
    pitches: list[str],
    iois: list[float],
    position: str,
    velocity: int,
    *,
    slide_in: bool = False,
    accent_every: int = 0,
) -> None:
    cursor = start
    index = 0
    previous_pitch: str | None = target[-1]["pitch"] if target else None
    previous_fingering: tuple[int, int] | None = None
    if target:
        previous_fingering = (
            int(target[-1].get("planned_string", -1)),
            int(target[-1].get("planned_fret", -1)),
        )

    while cursor < end - 0.06:
        pitch = pitches[index % len(pitches)]
        ioi = min(iois[index % len(iois)], end - cursor)
        fingering = FRETBOARD[position][pitch]
        articulations: list[str] = ["pick"]

        if index == 0 and slide_in:
            articulations = ["slide", "accent"]
        elif previous_pitch == pitch:
            articulations = ["pick", "accent"]
        elif previous_fingering and fingering[0] == previous_fingering[0]:
            fret_delta = fingering[1] - previous_fingering[1]
            if 0 < fret_delta <= 3:
                articulations = ["hammer_on", "legato"]
            elif -3 <= fret_delta < 0:
                articulations = ["pull_off", "legato"]

        if accent_every and index % accent_every == 0 and "accent" not in articulations:
            articulations.append("accent")

        duration = max(
            0.09,
            ioi * (0.98 if set(articulations) & {"legato", "slide"} else 0.86),
        )
        event = {
            "pitch": pitch,
            "at": at(cursor),
            "duration": round(duration, 3),
            "velocity": min(
                115,
                velocity + (6 if "accent" in articulations else 0) + ((index % 3) - 1),
            ),
            "articulations": articulations,
            "planned_position": position,
            "planned_string": fingering[0],
            "planned_fret": fingering[1],
        }
        if "slide" in articulations:
            event["slide_from_semitones"] = -2.0
        target.append(event)
        previous_pitch = pitch
        previous_fingering = fingering
        cursor += ioi
        index += 1


def special_note(
    target: list[dict],
    start: float,
    pitch: str,
    duration: float,
    position: str,
    velocity: int,
    articulations: list[str],
    **extra: object,
) -> None:
    string, fret = FRETBOARD[position][pitch]
    target.append(
        {
            "pitch": pitch,
            "at": at(start),
            "duration": duration,
            "velocity": velocity,
            "articulations": articulations,
            "planned_position": position,
            "planned_string": string,
            "planned_fret": fret,
            **extra,
        }
    )


def theme_a(revision: str) -> list[dict]:
    events: list[dict] = []
    first_end = 14.75 if revision == "v2" else 16.0
    add_stream(
        events,
        0,
        first_end,
        ["E4", "G4", "A4", "G4", "E4", "G4", "A4", "B4"],
        [0.5, 0.5, 0.75, 0.25, 0.5, 0.5, 0.75, 0.75],
        "mid_b_string",
        78,
        accent_every=7,
    )
    add_stream(
        events,
        16,
        30.5,
        ["G4", "A4", "B4", "D5", "E5", "D5", "B4", "A4"],
        [0.5, 0.25, 0.25, 0.75, 0.25, 0.5, 0.75, 0.75],
        "upper_high_e",
        84,
        slide_in=True,
        accent_every=8,
    )
    special_note(
        events,
        30.5,
        "B4",
        1.35,
        "upper_high_e",
        92,
        ["sustain", "vibrato"],
        vibrato={"delay": 0.52, "depth": 0.16, "rate": 4.7},
    )
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def theme_b(revision: str) -> list[dict]:
    events: list[dict] = []
    add_stream(
        events,
        0,
        15.5,
        ["B4", "D5", "E5", "G5", "E5", "D5", "B4", "D5"],
        [0.5, 0.25, 0.25, 0.5, 0.5, 0.5, 0.75, 0.75],
        "upper_high_e",
        88,
        slide_in=True,
        accent_every=6,
    )
    special_note(
        events,
        15.5,
        "E5",
        1.4,
        "upper_high_e",
        98,
        ["sustain", "vibrato"],
        vibrato={"delay": 0.58, "depth": 0.18, "rate": 4.9},
    )
    add_stream(
        events,
        17,
        30.75,
        ["E5", "G5", "A5", "G5", "E5", "D5", "B4", "D5", "E5"],
        [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.75, 0.25, 0.5],
        "upper_high_e",
        94 if revision == "v2" else 91,
        slide_in=True,
        accent_every=7,
    )
    special_note(
        events,
        30.75,
        "B4",
        1.1,
        "upper_high_e",
        101,
        ["bend", "vibrato"],
        bend_semitones=2.0,
        vibrato={"delay": 0.62, "depth": 0.2, "rate": 5.0},
    )
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def peak(revision: str) -> list[dict]:
    events: list[dict] = []
    add_stream(
        events,
        0,
        14.0,
        ["E5", "G5", "A5", "G5", "E5", "D5", "E5", "G5"],
        [0.25, 0.25, 0.5, 0.25, 0.25, 0.5, 0.75, 0.25],
        "upper_high_e",
        97,
        slide_in=True,
        accent_every=8,
    )
    special_note(
        events,
        14.0,
        "A5",
        1.5,
        "upper_high_e",
        106,
        ["sustain", "vibrato"],
        vibrato={"delay": 0.68, "depth": 0.2, "rate": 5.1},
    )
    add_stream(
        events,
        15.5,
        25.5 if revision == "v2" else 21.5,
        ["G5", "A5", "B5", "A5", "G5", "E5", "G5", "A5"],
        [0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, 0.75],
        "upper_high_e",
        102,
        accent_every=5,
    )
    peak_time = 25.5 if revision == "v2" else 21.5
    special_note(
        events,
        peak_time,
        "B5",
        1.85,
        "upper_high_e",
        114,
        ["bend", "vibrato"],
        bend_semitones=2.0,
        vibrato={"delay": 0.82, "depth": 0.26, "rate": 5.3},
    )
    add_stream(
        events,
        peak_time + 1.85,
        32,
        ["A5", "G5", "E5", "D5", "B4", "D5", "E5", "B4"],
        [0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.75, 0.75],
        "upper_high_e",
        96,
        slide_in=True,
    )
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def outro() -> list[dict]:
    events: list[dict] = []
    add_stream(
        events,
        0,
        10.5,
        ["E5", "D5", "B4", "A4", "G4", "E4", "G4", "E4"],
        [0.5, 0.5, 0.75, 0.25, 1.0, 0.5, 0.5, 1.0],
        "upper_high_e",
        82,
        slide_in=True,
    )
    special_note(
        events,
        10.5,
        "E4",
        5.25,
        "mid_b_string",
        86,
        ["sustain", "vibrato"],
        vibrato={"delay": 1.4, "depth": 0.13, "rate": 4.3},
    )
    return sorted(events, key=lambda item: tuple(map(float, item["at"].split(":"))))


def acoustic_phrase(section: str, energy: float, seed: int, revision: str) -> dict:
    patterns = {
        "intro": ["steady_eighths"],
        "theme_a": ["classic_pop"],
        "theme_b": ["classic_pop", "chorus_open"],
        "peak": ["chorus_open"],
        "outro": ["steady_eighths"],
    }[section]
    return {
        "instrument": "acoustic_guitar",
        "role": "continuous open-chord acoustic accompaniment",
        "section_function": section,
        "phrase_type": "continuous_strumming",
        "energy": energy,
        "harmony": harmony(section),
        "subdivision": "eighth",
        "strumming_patterns": patterns,
        "four_bar_variation": True,
        "per_string_sustain": True,
        "foreground_aware": section != "intro",
        "gate": 0.88 if section in {"intro", "outro"} else 0.81,
        "strum_spread": 0.052,
        "performance_intent": {
            "picking": "continuous alternate down-up motion",
            "attack": "open low strings with lighter upper-string answers",
            "release": "let selected strings ring across air strokes and barlines",
            "humanization": "action_based",
            "seed": seed + (1 if revision == "v2" else 0),
        },
    }


def lead_clip(section: str, motif: list[dict], energy: float, seed: int) -> dict:
    bars = dict((name, count) for name, count, _ in SECTIONS)[section]
    return {
        "loop_bars": bars,
        "sound_library_profile": "general_midi",
        "instrument_phrase": {
            "instrument": "electric_lead_guitar",
            "role": "guitar-native melodic solo with connected hand path",
            "section_function": section,
            "phrase_type": "melodic_lead",
            "phrase_generation_mode": "legacy_stable",
            "energy": energy,
            "motif": motif,
            "articulations": ["sustain"],
            "performance_intent": {
                "attack": "picked phrase starts with legato inner motion",
                "release": "selected targets sustain into delayed vibrato",
                "humanization": "articulation_driven",
                "seed": seed,
            },
        },
    }


def build(revision: str) -> dict:
    section_rows = []
    for name, bars, energy in SECTIONS:
        section_rows.append(
            {
                "name": name,
                "bars": bars,
                "energy": energy,
                "complexity": {
                    "level": "simple" if name == "intro" else ("rich" if name == "peak" else "standard")
                },
                "complexity_budget": {
                    "lead": 0 if name == "intro" else (6 if name == "peak" else 4),
                    "acoustic": 4,
                    "texture": 1,
                },
            }
        )

    acoustic_sections = {}
    for index, (name, bars, energy) in enumerate(SECTIONS):
        acoustic_sections[name] = {
            "loop_bars": bars,
            "sound_library_profile": "general_midi",
            "instrument_phrase": acoustic_phrase(
                name,
                min(0.92, energy / 10 + 0.18),
                SEED + 100 + index,
                revision,
            ),
        }

    lead_sections = {
        "theme_a": lead_clip("theme_a", theme_a(revision), 0.62, SEED + 201),
        "theme_b": lead_clip("theme_b", theme_b(revision), 0.78, SEED + 202),
        "peak": lead_clip("peak", peak(revision), 0.96, SEED + 203),
        "outro": lead_clip("outro", outro(), 0.50, SEED + 204),
    }

    return {
        "metadata": {
            "title": "Afterglow Current",
            "tempo": TEMPO,
            "time_signature": "4/4",
            "key": "E minor",
            "seed": SEED,
            "stage": revision,
            "composer_note": "original acoustic accompaniment plus electric guitar solo proof",
        },
        "complexity": {
            "level": "standard",
            "rhythm": 3,
            "harmony": 2,
            "arrangement": 2,
            "melodic_ornamentation": 4,
            "density": 2,
            "variation": 4,
        },
        "complexity_contour": "sparse_to_climax",
        "rhythm_motifs": {
            "lead_cell": [
                {"offset": 0, "duration": 0.5},
                {"offset": 0.5, "duration": 0.5},
                {"offset": 1.0, "duration": 0.75},
                {"offset": 1.75, "duration": 0.25},
                {"offset": 2.0, "duration": 0.5},
                {"offset": 3.0, "duration": 0.75},
            ],
            "acoustic_hand": [
                {"offset": 0, "duration": 0.5},
                {"offset": 0.5, "duration": 0.5},
                {"offset": 1.0, "duration": 0.5},
                {"offset": 1.5, "duration": 0.5},
            ],
        },
        "core_motif": {
            "motif_id": "afterglow_lead_cell",
            "scale_basis": "E minor pentatonic with D and B landing tones",
            "register": "mid",
            "rhythmic_identity": "two eighths, a dotted pulse, compressed turn, held connection",
            "contour": "E4-G4-A4, fold to G4-E4, then climb toward B4",
            "guitar_position": "B-string fifth-to-twelfth fret shape, then high-E shift",
            "development_options": [
                "sequence_up",
                "rhythmic_compression",
                "position_shift",
                "delayed_bend_target",
                "descending_recovery",
            ],
        },
        "sections": section_rows,
        "tracks": {
            "acoustic_guitar": {
                "role": "open-chord continuous acoustic accompaniment",
                "sound_library_profile": "general_midi",
                "sections": acoustic_sections,
            },
            "lead_guitar": {
                "role": "electric guitar foreground solo",
                "sound_library_profile": "general_midi",
                "sections": lead_sections,
            },
        },
    }


def write_json(name: str, value: object) -> None:
    (HERE / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def manifest() -> dict:
    return {
        "schema": "music-agent-project-facade",
        "schema_version": 1,
        "project": {"title": "Afterglow Current"},
        "artifacts": {
            "composition": {
                "standard": "music-agent composition extension",
                "path": "composition.json",
                "authority": "authoritative",
            },
            "render_config": {
                "standard": "music-agent render extension",
                "path": "render.json",
                "authority": "authoritative",
            },
            "instrument_config": {
                "standard": "music-agent instrument extension",
                "path": "instruments.json",
                "authority": "authoritative",
            },
            "execution_midi": {
                "standard": "MIDI 1.0 Standard MIDI File",
                "path": "output/full_song.mid",
                "authority": "derived",
            },
            "final_audio": {
                "standard": "WAVE PCM audio",
                "path": "output/mix.wav",
                "authority": "derived",
            },
        },
        "conversion_reports": [],
        "edit_protocols": {
            "pointer": "RFC 6901 JSON Pointer",
            "patch": "RFC 6902 JSON Patch",
        },
    }


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    v1 = build("v1")
    v2 = build("v2")
    write_json("composition_v1.json", v1)
    write_json("composition_v2.json", v2)
    write_json("composition.json", v2)
    write_json("composition.normalized.json", v2)
    write_json("core_motif.json", v2["core_motif"])
    write_json("manifest.json", manifest())
    print(f"Built Afterglow Current: {sum(bars for _, bars, _ in SECTIONS)} bars at {TEMPO} BPM")


if __name__ == "__main__":
    main()
