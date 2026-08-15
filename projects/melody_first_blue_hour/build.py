from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.composition import validate_composition
from src.midi import generate_song_midis


TITLE = "Blue Hour Signal"
TEMPO = 112

SECTION_BARS = {
    "intro": 4,
    "A": 8,
    "A_prime": 8,
    "B": 8,
    "hook": 8,
    "outro": 4,
}

# Melody is the authored core. Each tuple is:
# (bar, beat, pitch, duration_in_beats, velocity)
#
# Germ identity:
#   F# -> A -> B, then a return/answer around A/F#/E/D.
# The later sections preserve that contour/rhythm family while sequencing,
# expanding register, changing phrase destination, and finally reaching F#6.
MELODY = {'intro': [(1, 2.0, 'F#5', 0.7, 76),
           (1, 3.0, 'A5', 0.45, 79),
           (1, 3.75, 'B5', 0.8, 82),
           (2, 2.0, 'A5', 0.65, 77),
           (2, 3.0, 'F#5', 0.45, 75),
           (2, 3.75, 'E5', 0.6, 73),
           (3, 1.5, 'F#5', 0.5, 78),
           (3, 2.25, 'A5', 0.5, 81),
           (3, 3.0, 'B5', 0.9, 84),
           (4, 2.0, 'A5', 0.6, 78),
           (4, 3.0, 'F#5', 0.45, 76),
           (4, 3.75, 'D5', 0.7, 80)],
 'A': [(1, 1.0, 'F#5', 0.72, 90),
       (1, 2.0, 'A5', 0.45, 93),
       (1, 2.75, 'B5', 0.9, 96),
       (1, 4.0, 'A5', 0.45, 89),
       (2, 1.0, 'F#5', 0.72, 88),
       (2, 2.0, 'E5', 0.45, 86),
       (2, 2.75, 'D5', 1.45, 91),
       (3, 1.0, 'F#5', 0.45, 91),
       (3, 1.75, 'A5', 0.45, 94),
       (3, 2.5, 'B5', 0.45, 96),
       (3, 3.25, 'D6', 1.15, 101),
       (4, 1.0, 'C#6', 0.7, 96),
       (4, 2.0, 'B5', 0.45, 92),
       (4, 2.75, 'A5', 1.0, 90),
       (5, 1.0, 'F#5', 0.72, 91),
       (5, 2.0, 'A5', 0.45, 94),
       (5, 2.75, 'B5', 0.9, 97),
       (5, 4.0, 'A5', 0.45, 90),
       (6, 1.0, 'G5', 0.7, 91),
       (6, 2.0, 'F#5', 0.45, 88),
       (6, 2.75, 'E5', 0.55, 86),
       (6, 3.5, 'F#5', 0.8, 90),
       (7, 1.0, 'A5', 0.5, 94),
       (7, 1.75, 'B5', 0.5, 96),
       (7, 2.5, 'D6', 0.5, 101),
       (7, 3.25, 'E6', 1.1, 105),
       (8, 1.0, 'C#6', 0.6, 97),
       (8, 1.9, 'B5', 0.45, 93),
       (8, 2.65, 'A5', 0.55, 91),
       (8, 3.5, 'F#5', 0.45, 88),
       (8, 4.0, 'D5', 0.7, 94)],
 'A_prime': [(1, 1.0, 'F#5', 0.45, 91),
             (1, 1.75, 'A5', 0.45, 94),
             (1, 2.5, 'B5', 1.15, 98),
             (1, 4.0, 'D6', 0.45, 101),
             (2, 1.0, 'C#6', 0.6, 96),
             (2, 2.0, 'A5', 0.5, 91),
             (2, 2.8, 'F#5', 0.45, 88),
             (2, 3.55, 'E5', 0.75, 87),
             (3, 1.0, 'G5', 0.5, 91),
             (3, 1.75, 'B5', 0.45, 95),
             (3, 2.5, 'D6', 0.85, 101),
             (3, 3.65, 'B5', 0.55, 94),
             (4, 1.0, 'A5', 0.7, 91),
             (4, 2.0, 'F#5', 0.5, 88),
             (4, 2.8, 'E5', 0.45, 86),
             (4, 3.5, 'D5', 0.8, 90),
             (5, 1.0, 'G5', 0.45, 92),
             (5, 1.75, 'B5', 0.45, 96),
             (5, 2.5, 'C#6', 0.9, 100),
             (5, 3.75, 'B5', 0.5, 94),
             (6, 1.0, 'A5', 0.65, 93),
             (6, 2.0, 'F#5', 0.45, 89),
             (6, 2.75, 'E5', 0.5, 87),
             (6, 3.5, 'F#5', 0.8, 91),
             (7, 1.0, 'A5', 0.45, 95),
             (7, 1.7, 'B5', 0.45, 98),
             (7, 2.4, 'D6', 0.45, 102),
             (7, 3.1, 'F#6', 1.25, 108),
             (8, 1.0, 'E6', 0.65, 101),
             (8, 2.0, 'D6', 0.5, 98),
             (8, 2.8, 'C#6', 0.45, 95),
             (8, 3.5, 'A5', 0.8, 92)],
 'B': [(1, 1.0, 'B4', 1.35, 86),
       (1, 2.75, 'D5', 0.55, 90),
       (1, 3.6, 'F#5', 0.7, 93),
       (2, 1.0, 'E5', 1.0, 89),
       (2, 2.5, 'C#5', 0.55, 86),
       (2, 3.4, 'B4', 0.8, 84),
       (3, 1.0, 'G4', 1.4, 83),
       (3, 2.9, 'B4', 0.5, 87),
       (3, 3.7, 'D5', 0.65, 90),
       (4, 1.0, 'F#5', 1.15, 92),
       (4, 2.6, 'E5', 0.5, 88),
       (4, 3.45, 'D5', 0.75, 87),
       (5, 1.0, 'E5', 0.7, 89),
       (5, 2.0, 'F#5', 0.5, 92),
       (5, 2.8, 'A5', 1.1, 96),
       (6, 1.0, 'B5', 0.75, 98),
       (6, 2.0, 'A5', 0.5, 94),
       (6, 2.8, 'F#5', 0.5, 91),
       (6, 3.55, 'E5', 0.75, 89),
       (7, 1.0, 'G5', 0.55, 93),
       (7, 1.85, 'A5', 0.45, 95),
       (7, 2.6, 'B5', 0.55, 98),
       (7, 3.45, 'C#6', 0.85, 101),
       (8, 1.0, 'D6', 0.8, 103),
       (8, 2.2, 'C#6', 0.45, 98),
       (8, 3.0, 'A5', 0.5, 93),
       (8, 3.75, 'F#5', 0.6, 91)],
 'hook': [(1, 1.0, 'F#5', 0.6, 98),
          (1, 1.9, 'A5', 0.45, 101),
          (1, 2.6, 'B5', 0.8, 105),
          (1, 3.7, 'D6', 0.65, 109),
          (2, 1.0, 'C#6', 0.65, 104),
          (2, 2.0, 'B5', 0.45, 100),
          (2, 2.75, 'A5', 0.5, 98),
          (2, 3.55, 'F#5', 0.75, 96),
          (3, 1.0, 'F#5', 0.45, 99),
          (3, 1.75, 'A5', 0.45, 102),
          (3, 2.5, 'B5', 0.45, 105),
          (3, 3.2, 'D6', 1.15, 110),
          (4, 1.0, 'E6', 0.6, 108),
          (4, 1.9, 'D6', 0.45, 104),
          (4, 2.6, 'B5', 0.55, 101),
          (4, 3.45, 'A5', 0.8, 98),
          (5, 1.0, 'A5', 0.5, 101),
          (5, 1.75, 'B5', 0.45, 104),
          (5, 2.5, 'D6', 0.5, 109),
          (5, 3.25, 'F#6', 1.1, 115),
          (6, 1.0, 'E6', 0.6, 109),
          (6, 2.0, 'D6', 0.45, 105),
          (6, 2.75, 'B5', 0.55, 101),
          (6, 3.6, 'A5', 0.7, 99),
          (7, 1.0, 'G5', 0.45, 99),
          (7, 1.7, 'A5', 0.45, 101),
          (7, 2.4, 'B5', 0.45, 104),
          (7, 3.1, 'C#6', 0.55, 108),
          (7, 3.9, 'E6', 0.5, 111),
          (8, 1.0, 'D6', 0.9, 112),
          (8, 2.25, 'B5', 0.45, 104),
          (8, 3.0, 'A5', 0.45, 101),
          (8, 3.7, 'F#5', 0.45, 97),
          (8, 4.2, 'D5', 0.45, 100)],
 'outro': [(1, 1.5, 'F#5', 0.55, 88),
           (1, 2.35, 'A5', 0.45, 91),
           (1, 3.05, 'B5', 0.8, 94),
           (2, 1.5, 'A5', 0.6, 89),
           (2, 2.5, 'F#5', 0.5, 86),
           (2, 3.35, 'E5', 0.7, 84),
           (3, 1.5, 'F#5', 0.5, 87),
           (3, 2.25, 'A5', 0.5, 90),
           (3, 3.0, 'D6', 0.9, 96),
           (4, 1.0, 'C#6', 0.6, 92),
           (4, 2.0, 'A5', 0.5, 88),
           (4, 3.0, 'F#5', 0.5, 85),
           (4, 3.8, 'D5', 1.0, 90)]}

HARMONY = {
    "intro": ["Bm7", "Gmaj7", "Dadd9", "Aadd9"],
    "A": ["D", "A/C#", "Bm7", "Gmaj7", "D/F#", "Em7", "G", "A"],
    "A_prime": ["D", "A/C#", "Bm7", "Gmaj7", "Em7", "Bm/D", "G", "A"],
    "B": ["Bm", "A", "G", "D/F#", "Em", "G", "A", "Aadd9"],
    "hook": ["Dadd9", "Aadd9", "Bm7", "Gadd9", "D/F#", "Gadd9", "Aadd9", "Dadd9"],
    "outro": ["Bm7", "Gmaj7", "Dadd9", "Dadd9"],
}

CHORDS = {
    "D": ["D3", "A3", "D4", "F#4"],
    "Dadd9": ["D3", "A3", "D4", "E4", "F#4"],
    "A": ["A2", "E3", "A3", "C#4"],
    "Aadd9": ["A2", "E3", "A3", "B3", "C#4"],
    "A/C#": ["C#3", "A3", "C#4", "E4"],
    "Bm": ["B2", "F#3", "B3", "D4"],
    "Bm7": ["B2", "F#3", "A3", "D4"],
    "Bm/D": ["D3", "F#3", "A3", "B3"],
    "G": ["G2", "D3", "G3", "B3"],
    "Gadd9": ["G2", "D3", "G3", "A3", "B3"],
    "Gmaj7": ["G2", "D3", "F#3", "B3"],
    "D/F#": ["F#2", "A3", "D4", "F#4"],
    "Em": ["E3", "B3", "E4", "G4"],
    "Em7": ["E3", "B3", "D4", "G4"],
}

# Bass stays subordinate: one harmonic anchor, one local connector, then air.
# This follows the active smooth-melodic-support-bass idea without copying a
# reference line or turning the bass into a second lead.
BASS_SHAPES = {
    "D": ("D2", "A2"),
    "Dadd9": ("D2", "A2"),
    "A": ("A2", "E3"),
    "Aadd9": ("A2", "E3"),
    "A/C#": ("C#3", "E3"),
    "Bm": ("B2", "F#2"),
    "Bm7": ("B2", "F#2"),
    "Bm/D": ("D2", "F#2"),
    "G": ("G2", "B2"),
    "Gadd9": ("G2", "B2"),
    "Gmaj7": ("G2", "B2"),
    "D/F#": ("F#2", "A2"),
    "Em": ("E2", "G2"),
    "Em7": ("E2", "G2"),
}

SECTION_LEVEL = {
    "intro": 0,
    "A": 1,
    "A_prime": 2,
    "B": 0,
    "hook": 3,
    "outro": 0,
}


def pos(bar: int, beat: float) -> str:
    return f"{bar}:{beat:g}"


def note_event(bar: int, beat: float, pitch: str, duration: float, velocity: int) -> dict:
    return {
        "type": "note",
        "at": pos(bar, beat),
        "pitch": pitch,
        "duration": duration,
        "velocity": velocity,
    }


def chord_event(bar: int, symbol: str, velocity: int) -> dict:
    return {
        "type": "chord",
        "at": pos(bar, 1),
        "pitches": CHORDS[symbol],
        "duration": 3.72,
        "velocity": velocity,
    }


def drum_event(bar: int, beat: float, name: str, velocity: int) -> dict:
    return {
        "type": "drum",
        "at": pos(bar, beat),
        "note": name,
        "duration": 0.08,
        "velocity": velocity,
    }


def build_lead(section: str) -> list[dict]:
    return [note_event(*item) for item in MELODY[section]]


def build_keys(section: str) -> list[dict]:
    base_velocity = {
        "intro": 43,
        "A": 49,
        "A_prime": 51,
        "B": 45,
        "hook": 55,
        "outro": 41,
    }[section]
    return [
        chord_event(bar, symbol, base_velocity + (bar % 2))
        for bar, symbol in enumerate(HARMONY[section], start=1)
    ]


def build_bass(section: str) -> list[dict]:
    level = SECTION_LEVEL[section]
    anchor_velocity = 61 + level * 4
    connector_velocity = anchor_velocity - 5
    events: list[dict] = []
    for bar, symbol in enumerate(HARMONY[section], start=1):
        anchor, connector = BASS_SHAPES[symbol]
        hold = 2.25 if section in {"intro", "B", "outro"} else 1.72
        events.append(note_event(bar, 1.0, anchor, hold, anchor_velocity + (bar % 2)))
        events.append(note_event(bar, 3.18, connector, 0.58, connector_velocity))
    return events


def build_drums(section: str) -> list[dict]:
    level = SECTION_LEVEL[section]
    events: list[dict] = []
    for bar in range(1, SECTION_BARS[section] + 1):
        if section in {"intro", "outro"}:
            for beat in (1.0, 2.0, 3.0, 4.0):
                events.append(drum_event(bar, beat, "closed_hat", 40 + (2 if beat in (2.0, 4.0) else 0)))
            events.append(drum_event(bar, 1.0, "kick", 54))
            if bar % 2 == 0:
                events.append(drum_event(bar, 3.0, "side_stick", 48))
            continue

        if section == "B":
            for beat in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
                events.append(drum_event(bar, beat, "closed_hat", 43 if beat % 1 else 47))
            events.append(drum_event(bar, 1.0, "kick", 57))
            events.append(drum_event(bar, 3.0, "snare", 55))
            continue

        for beat in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
            events.append(drum_event(bar, beat, "closed_hat", 47 + (3 if beat % 1 == 0 else 0)))
        events.extend([
            drum_event(bar, 1.0, "kick", 61 + level),
            drum_event(bar, 2.0, "snare", 58 + level),
            drum_event(bar, 3.0, "kick", 56 + level),
            drum_event(bar, 4.0, "snare", 60 + level),
        ])
        if section == "hook":
            events.append(drum_event(bar, 3.5, "kick", 54))
            if bar in {1, 5}:
                events.append(drum_event(bar, 1.0, "crash", 67))
        elif bar == 1:
            events.append(drum_event(bar, 1.0, "crash", 62))
    return events


def make_composition() -> dict:
    sections = [{"name": name, "bars": bars} for name, bars in SECTION_BARS.items()]

    def clips(builder):
        return {
            name: {
                "loop_bars": bars,
                "events": builder(name),
            }
            for name, bars in SECTION_BARS.items()
        }

    return {
        "metadata": {
            "title": TITLE,
            "tempo": TEMPO,
            "time_signature": "4/4",
            "key": "D major / B minor color",
        },
        "complexity_contour": "wave",
        "sections": sections,
        "tracks": {
            "lead_square": {
                "role": "main melody / foreground hook",
                "sections": clips(build_lead),
            },
            "electric_piano": {
                "role": "harmonic support / low-pressure bed",
                "sections": clips(build_keys),
            },
            "finger_bass": {
                "role": "bass foundation / connective low line",
                "sections": clips(build_bass),
            },
            "drums": {
                "role": "light pulse / section framing",
                "sections": clips(build_drums),
            },
        },
    }


def main() -> None:
    composition = make_composition()
    validate_composition(composition)

    source_path = PROJECT / "composition.generated.json"
    source_path.write_text(
        json.dumps(composition, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    instruments = {
        # GM program numbers here are zero-based, matching src/midi/generator.py.
        "lead_square": {"program": 80, "channel": 1},
        "electric_piano": {"program": 4, "channel": 2},
        "finger_bass": {"program": 33, "channel": 3},
        "drums": {"program": 0, "channel": 10, "bank": 128},
    }

    generated = generate_song_midis(composition, instruments, PROJECT)

    report_dir = PROJECT / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "title": TITLE,
        "tempo": TEMPO,
        "bars": sum(SECTION_BARS.values()),
        "approx_seconds": round(sum(SECTION_BARS.values()) * 4 * 60 / TEMPO, 1),
        "melody_notes": sum(len(items) for items in MELODY.values()),
        "design": {
            "germ": "F#-A-B rise with returning answer tones",
            "phrase_relations": ["intro fragment", "A statement", "A' variation/sequence", "B contrast", "hook expansion", "outro recall"],
            "climax": "F#6 in hook bar 5",
            "foreground_rule": "backing stays lower in register and velocity than the lead",
        },
        "generated": {name: str(path) for name, path in generated.items()},
    }
    report_path = report_dir / "melody_design.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(source_path)
    for name, path in generated.items():
        print(f"{name}: {path}")
    print(report_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
