from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT_NAME = "afterglow_signal_pop_rock"
PROJECT = ROOT / "projects" / PROJECT_NAME

TEMPO = 120
SECTIONS = [
    ("intro", 6, 0.36),
    ("verse_1", 12, 0.50),
    ("pre_1", 6, 0.66),
    ("chorus_1", 12, 0.86),
    ("verse_2", 12, 0.57),
    ("pre_2", 6, 0.73),
    ("chorus_2", 12, 0.91),
    ("bridge", 8, 0.67),
    ("final_chorus", 12, 1.00),
    ("outro", 4, 0.40),
]

HARMONY = {
    "intro": ["Bm", "G", "D", "A", "G", "A"],
    "verse_1": ["Bm", "G", "D", "A", "Bm", "G", "D", "A", "Em", "G", "D", "A"],
    "pre_1": ["Em", "G", "D", "A", "Em", "A"],
    "chorus_1": ["G", "D", "A", "Bm", "G", "D", "A", "A", "Em", "G", "D", "A"],
    "verse_2": ["Bm", "G", "D", "A", "Bm", "G", "D", "A", "Em", "G", "D", "A"],
    "pre_2": ["Em", "G", "D", "A", "Em", "A"],
    "chorus_2": ["G", "D", "A", "Bm", "G", "D", "A", "A", "Em", "G", "D", "A"],
    "bridge": ["Em", "Bm", "G", "D", "Em", "Bm", "A", "A"],
    "final_chorus": ["G", "D", "A", "Bm", "G", "D", "A", "A", "Em", "G", "A", "Bm"],
    "outro": ["G", "A", "Bm", "Bm"],
}

CHORD_TONES = {
    "Bm": ["B3", "D4", "F#4"],
    "G": ["G3", "B3", "D4"],
    "D": ["D4", "F#4", "A4"],
    "A": ["A3", "C#4", "E4"],
    "Em": ["E3", "G3", "B3"],
}

POWER_DYADS_LOW = {
    "Bm": ["B2", "F#3"],
    "G": ["G2", "D3"],
    "D": ["D3", "A3"],
    "A": ["A2", "E3"],
    "Em": ["E3", "B3"],
}

POWER_DYADS_HIGH = {
    "Bm": ["F#3", "B3"],
    "G": ["D3", "G3"],
    "D": ["A3", "D4"],
    "A": ["E3", "A3"],
    "Em": ["B3", "E4"],
}

BASS_ROOT = {"Bm": "B2", "G": "G2", "D": "D2", "A": "A2", "Em": "E2"}
BASS_COLOR = {"Bm": "D3", "G": "B2", "D": "F#2", "A": "C#3", "Em": "G2"}


def event_note(bar: int, beat: float, pitch: str, duration: float, velocity: int) -> dict[str, object]:
    return {"type": "note", "at": f"{bar}:{beat:g}", "pitch": pitch, "duration": duration, "velocity": velocity}


def event_chord(bar: int, beat: float, pitches: list[str], duration: float, velocity: int) -> dict[str, object]:
    return {"type": "chord", "at": f"{bar}:{beat:g}", "pitches": pitches, "duration": duration, "velocity": velocity}


def event_drum(bar: int, beat: float, note: int, duration: float, velocity: int) -> dict[str, object]:
    return {"type": "drum", "at": f"{bar}:{beat:g}", "note": note, "duration": duration, "velocity": velocity}


def clip(events: list[dict[str, object]], bars: int) -> dict[str, object]:
    return {"loop_bars": bars, "events": events}


def add_phrase(events: list[dict[str, object]], notes: list[tuple[int, float, str, float, int]]) -> None:
    for bar, beat, pitch, duration, velocity in notes:
        events.append(event_note(bar, beat, pitch, duration, velocity))


def flute_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    if section == "intro":
        add_phrase(e, [
            (3, 1.5, "F#4", 0.75, 76), (3, 2.5, "A4", 0.50, 79), (3, 3.25, "B4", 1.30, 82),
            (4, 2.0, "A4", 0.75, 78), (4, 3.0, "F#4", 1.35, 75),
            (5, 1.5, "E4", 0.60, 77), (5, 2.25, "F#4", 0.60, 79), (5, 3.0, "A4", 1.50, 82),
            (6, 2.0, "C#5", 0.55, 84), (6, 2.75, "B4", 1.00, 81),
        ])
    elif section in {"verse_1", "verse_2"}:
        variant = section == "verse_2"
        vel = 82 if not variant else 86
        add_phrase(e, [
            (1, 1.5, "F#4", 0.50, vel), (1, 2.25, "A4", 0.50, vel + 1), (1, 3.0, "B4", 0.90, vel + 2),
            (2, 1.75, "A4", 0.55, vel), (2, 2.5, "F#4", 1.20, vel - 2),
            (3, 1.5, "E4", 0.55, vel - 1), (3, 2.25, "F#4", 0.50, vel), (3, 3.0, "A4", 0.90, vel + 2),
            (4, 2.0, "F#4", 0.75, vel - 1), (4, 3.0, "E4", 0.90, vel - 3),
            (5, 1.25, "F#4", 0.55, vel), (5, 2.0, "A4", 0.50, vel + 1), (5, 2.75, "B4", 0.55, vel + 3),
            (5, 3.5, "D5", 0.70, vel + 4), (6, 1.5, "B4", 0.70, vel + 1), (6, 2.5, "A4", 1.25, vel - 1),
            (7, 1.5, "F#4", 0.45, vel), (7, 2.0, "A4", 0.45, vel + 1), (7, 2.75, "B4", 1.05, vel + 3),
            (8, 2.0, "C#5", 0.55, vel + 3), (8, 2.75, "A4", 1.00, vel),
            (9, 1.5, "G4", 0.55, vel), (9, 2.25, "A4", 0.55, vel + 1), (9, 3.0, "B4", 0.80, vel + 2),
            (10, 1.5, "D5", 0.55, vel + 4), (10, 2.25, "B4", 0.55, vel + 1), (10, 3.0, "A4", 0.95, vel),
            (11, 1.5, "F#4", 0.55, vel - 1), (11, 2.25, "A4", 0.55, vel + 1), (11, 3.0, "D5", 0.95, vel + 4),
            (12, 2.0, "C#5", 0.55, vel + 3), (12, 2.75, "B4", 0.55, vel + 2), (12, 3.5, "A4", 0.45, vel),
        ])
        if variant:
            add_phrase(e, [(4, 4.0, "F#4", 0.35, vel), (8, 4.0, "E5", 0.35, vel + 4), (12, 4.0, "C#5", 0.35, vel + 3)])
    elif section in {"pre_1", "pre_2"}:
        boost = 4 if section == "pre_2" else 0
        add_phrase(e, [
            (1, 1.0, "G4", 0.75, 84 + boost), (1, 2.0, "A4", 0.75, 85 + boost), (1, 3.0, "B4", 1.20, 87 + boost),
            (2, 1.5, "D5", 0.70, 88 + boost), (2, 2.5, "B4", 1.00, 86 + boost),
            (3, 1.0, "A4", 0.70, 85 + boost), (3, 2.0, "B4", 0.70, 87 + boost), (3, 3.0, "D5", 1.20, 90 + boost),
            (4, 1.5, "E5", 0.65, 91 + boost), (4, 2.25, "D5", 0.65, 89 + boost), (4, 3.0, "C#5", 0.90, 88 + boost),
            (5, 1.0, "B4", 0.55, 88 + boost), (5, 1.75, "D5", 0.55, 90 + boost), (5, 2.5, "E5", 0.55, 92 + boost),
            (5, 3.25, "F#5", 0.70, 94 + boost), (6, 1.0, "E5", 0.55, 91 + boost),
            (6, 1.75, "F#5", 0.55, 94 + boost), (6, 2.5, "A5", 1.15, 98 + boost),
        ])
    elif section in {"chorus_1", "chorus_2", "final_chorus"}:
        final = section == "final_chorus"
        boost = 0 if section == "chorus_1" else 3 if section == "chorus_2" else 6
        add_phrase(e, [
            (1, 1.0, "D5", 0.60, 94 + boost), (1, 1.75, "D5", 0.35, 92 + boost), (1, 2.25, "F#5", 0.70, 98 + boost), (1, 3.25, "E5", 0.70, 95 + boost),
            (2, 1.0, "D5", 0.55, 94 + boost), (2, 1.75, "A4", 0.45, 90 + boost), (2, 2.5, "B4", 1.25, 95 + boost),
            (3, 1.0, "C#5", 0.55, 94 + boost), (3, 1.75, "E5", 0.55, 96 + boost), (3, 2.5, "F#5", 0.85, 99 + boost), (3, 3.5, "E5", 0.40, 95 + boost),
            (4, 1.0, "D5", 1.60, 97 + boost),
            (5, 1.0, "D5", 0.55, 94 + boost), (5, 1.75, "F#5", 0.55, 98 + boost), (5, 2.5, "A5", 0.85, 102 + boost), (5, 3.5, "F#5", 0.40, 98 + boost),
            (6, 1.0, "E5", 0.55, 96 + boost), (6, 1.75, "D5", 0.55, 94 + boost), (6, 2.5, "B4", 1.15, 93 + boost),
            (7, 1.0, "C#5", 0.55, 94 + boost), (7, 1.75, "E5", 0.55, 97 + boost), (7, 2.5, "F#5", 0.60, 100 + boost), (7, 3.25, "A5", 0.65, 103 + boost),
            (8, 1.0, "E5", 1.70, 96 + boost),
            (9, 1.0, "B4", 0.55, 92 + boost), (9, 1.75, "D5", 0.55, 95 + boost), (9, 2.5, "E5", 0.80, 97 + boost), (9, 3.5, "F#5", 0.40, 99 + boost),
            (10, 1.0, "D5", 0.55, 95 + boost), (10, 1.75, "B4", 0.55, 92 + boost), (10, 2.5, "A4", 1.10, 90 + boost),
            (11, 1.0, "F#4", 0.50, 91 + boost), (11, 1.75, "A4", 0.50, 93 + boost), (11, 2.5, "D5", 0.70, 97 + boost), (11, 3.35, "E5", 0.50, 98 + boost),
            (12, 1.0, "F#5" if final else "E5", 0.65, 102 + boost), (12, 1.85, "E5" if final else "C#5", 0.55, 99 + boost), (12, 2.6, "D5" if final else "B4", 1.20, 97 + boost),
        ])
        if final:
            add_phrase(e, [(4, 3.0, "F#5", 0.45, 104), (4, 3.55, "A5", 0.45, 106), (8, 3.0, "F#5", 0.45, 104), (8, 3.55, "A5", 0.45, 106)])
    elif section == "bridge":
        add_phrase(e, [
            (2, 1.5, "B4", 1.15, 84), (2, 3.0, "A4", 0.80, 82), (3, 1.5, "G4", 1.35, 80), (4, 2.0, "F#4", 1.40, 81),
            (5, 1.5, "B4", 0.70, 84), (5, 2.5, "D5", 0.70, 86), (5, 3.5, "E5", 0.45, 88), (6, 1.0, "F#5", 1.20, 92),
            (6, 2.75, "E5", 0.80, 88), (7, 1.5, "C#5", 0.65, 87), (7, 2.35, "E5", 0.65, 90), (7, 3.25, "F#5", 0.65, 93), (8, 1.0, "A5", 1.65, 98),
        ])
    elif section == "outro":
        add_phrase(e, [
            (1, 1.5, "D5", 0.60, 82), (1, 2.25, "B4", 0.60, 80), (1, 3.0, "A4", 0.95, 78),
            (2, 1.5, "C#5", 0.60, 80), (2, 2.25, "B4", 0.60, 78), (2, 3.0, "A4", 0.95, 76),
            (3, 1.5, "F#4", 0.60, 76), (3, 2.25, "A4", 0.60, 78), (3, 3.0, "B4", 1.35, 80), (4, 1.0, "F#4", 0.65, 74), (4, 2.0, "B4", 1.75, 78),
        ])
    return e


def muted_guitar_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    if section not in {"verse_1", "verse_2", "pre_1", "pre_2", "bridge"}:
        return e
    chords = HARMONY[section]
    is_pre = section.startswith("pre")
    for bar, chord in enumerate(chords, 1):
        if section == "bridge":
            if bar <= 4:
                beats = [1.0, 2.0, 3.0, 4.0]
                gate = 0.38
            else:
                beats = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
                gate = 0.22
        else:
            beats = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
            if bar % 4 != 0 or is_pre:
                beats.append(4.5)
            gate = 0.22
        for idx, beat in enumerate(beats):
            base = 56 + (bar % 4) * 2 + min(idx, 4)
            if is_pre:
                base += 7
            if section == "verse_2":
                base += 3
            e.append(event_chord(bar, beat, POWER_DYADS_LOW[chord], gate, min(base, 78)))
    return e


def overdrive_events(section: str, side: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    if section not in {"intro", "chorus_1", "chorus_2", "final_chorus", "outro"}:
        return e
    high = side == "right"
    shapes = POWER_DYADS_HIGH if high else POWER_DYADS_LOW
    for bar, chord in enumerate(HARMONY[section], 1):
        if section == "intro":
            attacks = [1.0, 3.0] if bar < 5 else [1.0, 2.0, 3.0, 4.0]
            base = 61 if high else 65
            dur = 1.85 if bar < 5 else 1.08
        elif section == "outro":
            attacks = [1.0, 2.0, 3.0, 4.0] if bar < 3 else [1.0, 3.0]
            base = 65 if high else 69
            dur = 1.08 if bar < 3 else 1.85
        else:
            attacks = [1.0, 2.0, 3.0, 4.0]
            base = 72 if section == "chorus_1" else 76 if section == "chorus_2" else 82
            if high:
                base -= 5
            dur = 1.08
        for idx, beat in enumerate(attacks):
            accent = 5 if beat in {1.0, 3.0} else 0
            sounding_beat = beat + (0.035 if high and beat < 4.0 else 0.0)
            e.append(event_chord(bar, sounding_beat, shapes[chord], dur, min(base + accent + (idx % 2), 101)))
    return e


def clean_guitar_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    if section not in {"intro", "verse_1", "verse_2", "bridge", "outro"}:
        return e
    for bar, chord in enumerate(HARMONY[section], 1):
        tones = CHORD_TONES[chord]
        if section == "bridge":
            positions, order, vel, dur = [1.5, 2.5, 3.5], [0, 2, 1], 58, 0.75
        elif section == "outro":
            positions, order, vel, dur = [1.5, 2.5, 3.5], [0, 1, 2], 55, 0.55
        else:
            positions, order, vel, dur = [1.0, 1.75, 2.5, 3.25], [0, 2, 1, 2], 57 if section == "intro" else 53, 0.55
        for i, beat in enumerate(positions):
            e.append(event_note(bar, beat, tones[order[i] % len(tones)], dur, vel + (i % 2) * 3))
    return e


def bass_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    open_section = section in {"chorus_1", "chorus_2", "final_chorus", "intro", "outro"}
    for bar, chord in enumerate(HARMONY[section], 1):
        root, color = BASS_ROOT[chord], BASS_COLOR[chord]
        if section == "bridge" and bar <= 4:
            e += [event_note(bar, 1.0, root, 1.55, 72), event_note(bar, 3.0, root, 1.55, 74)]
        elif open_section:
            pitches = [root, root, color if bar % 2 == 0 else root, root]
            for idx, beat in enumerate([1.0, 2.0, 3.0, 4.0]):
                velocity = [82, 74, 84, 79][idx] + (5 if section == "final_chorus" else 0)
                e.append(event_note(bar, beat, pitches[idx], 0.84, velocity))
            if bar % 4 == 0 and section not in {"intro", "outro"}:
                e.append(event_note(bar, 4.75, color, 0.20, 86))
        else:
            e += [
                event_note(bar, 1.0, root, 0.72, 75),
                event_note(bar, 2.0, root, 1.52, 72),
                event_note(bar, 4.0, color if bar % 2 == 0 else root, 0.72, 77),
            ]
            if bar % 4 == 0:
                e.append(event_note(bar, 4.75, color, 0.20, 80))
    return e


def organ_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    if section not in {"pre_1", "pre_2", "chorus_1", "chorus_2", "bridge", "final_chorus"}:
        return e
    base_vel = 51 if section.startswith("pre") else 57 if section == "bridge" else 61
    for bar, chord in enumerate(HARMONY[section], 1):
        e.append(event_chord(bar, 1.0, CHORD_TONES[chord], 3.75, base_vel + (3 if section == "final_chorus" else 0)))
    return e


def lead_guitar_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    if section == "intro":
        add_phrase(e, [(1, 1.0, "B4", 1.4, 67), (1, 3.0, "F#5", 0.8, 72), (2, 1.5, "D5", 0.8, 70), (2, 3.0, "B4", 1.1, 66)])
    elif section in {"chorus_1", "chorus_2"}:
        v = 72 if section == "chorus_1" else 76
        add_phrase(e, [(4, 3.0, "F#4", 0.40, v), (4, 3.55, "A4", 0.40, v + 2), (8, 3.0, "E4", 0.40, v), (8, 3.55, "F#4", 0.40, v + 2), (12, 3.0, "A4", 0.35, v + 2), (12, 3.5, "B4", 0.35, v + 4)])
    elif section == "bridge":
        add_phrase(e, [(1, 1.0, "E4", 1.6, 73), (1, 3.0, "B4", 0.8, 77), (3, 1.0, "G4", 1.4, 74), (4, 3.0, "A4", 0.8, 77), (6, 1.0, "F#4", 0.6, 78), (6, 1.8, "A4", 0.6, 80), (6, 2.6, "B4", 0.9, 82), (8, 2.0, "E5", 0.55, 84), (8, 2.75, "F#5", 0.55, 87), (8, 3.5, "A5", 0.40, 90)])
    elif section == "final_chorus":
        add_phrase(e, [(4, 3.0, "A4", 0.45, 80), (4, 3.6, "B4", 0.35, 83), (8, 3.0, "B4", 0.45, 82), (8, 3.6, "D5", 0.35, 85), (10, 3.0, "F#5", 0.50, 87), (10, 3.7, "E5", 0.25, 84), (12, 3.1, "A5", 0.35, 90), (12, 3.55, "F#5", 0.35, 88)])
    elif section == "outro":
        add_phrase(e, [(1, 1.0, "D5", 1.1, 71), (2, 1.0, "E5", 1.1, 72), (3, 1.0, "F#5", 1.1, 74), (4, 1.0, "B4", 2.5, 69)])
    return e


def drum_events(section: str) -> list[dict[str, object]]:
    e: list[dict[str, object]] = []
    bars = len(HARMONY[section])
    chorus = section in {"chorus_1", "chorus_2", "final_chorus"}
    pre = section in {"pre_1", "pre_2"}
    bridge = section == "bridge"
    for bar in range(1, bars + 1):
        if chorus:
            e.append(event_drum(bar, 1.0, 49, 0.20, 104 if bar == 1 else 92))
            for beat in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
                e.append(event_drum(bar, beat, 42 if beat != 4.5 or bar % 4 else 46, 0.12, 72 + (4 if beat in {1.0, 3.0} else 0)))
            for beat in [1.0, 1.5, 3.0, 3.5]:
                e.append(event_drum(bar, beat, 36, 0.18, 94 if beat in {1.0, 3.0} else 84))
            e.append(event_drum(bar, 2.0, 38, 0.18, 96))
            e.append(event_drum(bar, 4.0, 38, 0.18, 100))
        elif pre:
            for beat in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
                e.append(event_drum(bar, beat, 42 if not (bar == bars and beat == 4.5) else 46, 0.12, 62 + bar * 2))
            kicks = [1.0, 3.0] + ([3.5] if bar >= 4 else [])
            for beat in kicks:
                e.append(event_drum(bar, beat, 36, 0.18, 82 + bar))
            e.append(event_drum(bar, 2.0, 38, 0.18, 89))
            e.append(event_drum(bar, 4.0, 38, 0.18, 92))
        elif bridge:
            for beat in [1.0, 2.0, 3.0, 4.0]:
                e.append(event_drum(bar, beat, 51, 0.15, 66 + (4 if beat == 1.0 else 0)))
            e.append(event_drum(bar, 1.0, 36, 0.18, 82))
            e.append(event_drum(bar, 3.0, 38, 0.18, 92))
            if bar >= 5:
                e.append(event_drum(bar, 3.5, 36, 0.18, 78))
        else:
            for beat in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
                e.append(event_drum(bar, beat, 42, 0.12, 58 + (4 if beat in {1.0, 3.0} else 0)))
            e.append(event_drum(bar, 1.0, 36, 0.18, 84))
            e.append(event_drum(bar, 3.5, 36, 0.18, 79))
            e.append(event_drum(bar, 2.0, 38, 0.18, 88))
            e.append(event_drum(bar, 4.0, 38, 0.18, 91))
        if bar % 4 == 0 and bar != bars:
            e.append(event_drum(bar, 4.25, 45, 0.16, 78))
            e.append(event_drum(bar, 4.5, 47, 0.16, 82))
            e.append(event_drum(bar, 4.75, 50, 0.16, 86))
    if section != "outro":
        last = bars
        e.append(event_drum(last, 3.25, 45, 0.16, 84))
        e.append(event_drum(last, 3.5, 47, 0.16, 88))
        e.append(event_drum(last, 3.75, 50, 0.16, 92))
        e.append(event_drum(last, 4.0, 38, 0.18, 108 if section == "final_chorus" else 98))
    return e


def build_composition() -> dict[str, object]:
    tracks: dict[str, object] = {
        "lead_flute": {"role": "vocal-like lead melody played by flute", "sections": {}},
        "muted_guitar": {"role": "palm-muted pulse guitar", "sections": {}},
        "overdrive_left": {"role": "continuous overdrive rhythm bed left", "sections": {}},
        "overdrive_right": {"role": "continuous overdrive rhythm bed right", "sections": {}},
        "clean_guitar": {"role": "clean guitar connective texture", "sections": {}},
        "lead_guitar": {"role": "electric guitar fills and bridge response", "sections": {}},
        "bass": {"role": "section-linked electric bass", "sections": {}},
        "drums": {"role": "rock drum kit", "sections": {}},
        "organ": {"role": "subtle rock organ harmonic support", "sections": {}},
    }
    for name, bars, _energy in SECTIONS:
        builders = {
            "lead_flute": flute_events(name),
            "muted_guitar": muted_guitar_events(name),
            "overdrive_left": overdrive_events(name, "left"),
            "overdrive_right": overdrive_events(name, "right"),
            "clean_guitar": clean_guitar_events(name),
            "lead_guitar": lead_guitar_events(name),
            "bass": bass_events(name),
            "drums": drum_events(name),
            "organ": organ_events(name),
        }
        for track_name, events in builders.items():
            if events:
                tracks[track_name]["sections"][name] = clip(events, bars)
    sections = []
    for name, bars, energy in SECTIONS:
        sections.append({
            "name": name,
            "bars": bars,
            "complexity": "rich" if energy >= 0.80 else "standard",
            "complexity_budget": {"lead": 3 if energy >= 0.80 else 2, "drums": 3 if energy >= 0.80 else 2, "bass": 2, "chords": 3 if energy >= 0.80 else 2},
        })
    return {
        "metadata": {"title": "Afterglow Signal", "tempo": TEMPO, "time_signature": "4/4", "key": "B minor / D major"},
        "complexity": "rich",
        "complexity_contour": "custom",
        "sections": sections,
        "tracks": tracks,
    }


def build_instruments() -> dict[str, object]:
    return {
        "lead_flute": {"engine": "fluidsynth", "bank": 0, "program": 73},
        "muted_guitar": {"engine": "fluidsynth", "bank": 0, "program": 28},
        "overdrive_left": {"engine": "fluidsynth", "bank": 0, "program": 29},
        "overdrive_right": {"engine": "fluidsynth", "bank": 0, "program": 29},
        "clean_guitar": {"engine": "fluidsynth", "bank": 0, "program": 27},
        "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30},
        "bass": {"engine": "fluidsynth", "bank": 0, "program": 33},
        "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16},
        "organ": {"engine": "fluidsynth", "bank": 0, "program": 18},
    }


def build_render() -> dict[str, object]:
    return {
        "sample_rate": 44100,
        "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
        "fluidsynth_gain": 0.78,
        "tail_seconds": 3,
        "master_peak_db": -1,
        "mix": {
            "lead_flute": {"volume_db": -2.0, "pan": 0.03, "mute": False},
            "muted_guitar": {"volume_db": -7.0, "pan": -0.22, "mute": False},
            "overdrive_left": {"volume_db": -7.0, "pan": -0.62, "mute": False},
            "overdrive_right": {"volume_db": -7.5, "pan": 0.62, "mute": False},
            "clean_guitar": {"volume_db": -10.0, "pan": -0.36, "mute": False},
            "lead_guitar": {"volume_db": -8.0, "pan": 0.30, "mute": False},
            "bass": {"volume_db": -5.0, "pan": 0.0, "mute": False},
            "drums": {"volume_db": -6.0, "pan": 0.0, "mute": False},
            "organ": {"volume_db": -11.5, "pan": 0.18, "mute": False},
        },
    }


def build_manifest() -> dict[str, object]:
    return {
        "schema": "music-agent-project-facade",
        "schema_version": 1,
        "project": {"title": "Afterglow Signal"},
        "artifacts": {
            "composition": {"standard": "music-agent structured composition JSON", "path": "composition.json", "authority": "authoritative"},
            "instruments": {"standard": "music-agent renderer instrument mapping", "path": "instruments.json", "authority": "authoritative"},
            "render": {"standard": "music-agent render and mix configuration", "path": "render.json", "authority": "authoritative"},
            "execution_midi": {"standard": "MIDI 1.0 Standard MIDI File", "path": "output/full_song.mid", "authority": "derived"},
            "audio_mix": {"standard": "PCM WAV", "path": "output/mix.wav", "authority": "derived"},
        },
    }


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    PROJECT.mkdir(parents=True, exist_ok=True)
    write_json(PROJECT / "composition.json", build_composition())
    write_json(PROJECT / "instruments.json", build_instruments())
    write_json(PROJECT / "render.json", build_render())
    write_json(PROJECT / "manifest.json", build_manifest())
    expected_seconds = sum(bars for _, bars, _ in SECTIONS) * 4 * 60 / TEMPO
    print(f"[PLAN] {sum(bars for _, bars, _ in SECTIONS)} bars @ {TEMPO} BPM = {expected_seconds:.1f}s before tail")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_song.py"), PROJECT_NAME], cwd=ROOT)
    if result.returncode:
        return result.returncode
    mix = PROJECT / "output" / "mix.wav"
    final = PROJECT / "output" / "final.wav"
    if mix.exists():
        shutil.copy2(mix, final)
        print(f"[OK] Listening copy: {final}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
