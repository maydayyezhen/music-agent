from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEMPO = 114

SECTIONS = [
    ("intro", 8, 3), ("verse_1", 12, 4), ("pre_1", 6, 6), ("chorus_1", 12, 8),
    ("interlude", 4, 6), ("verse_2", 12, 5), ("pre_2", 6, 7), ("chorus_2", 12, 8),
    ("bridge", 8, 5), ("final_chorus", 14, 9), ("outro", 6, 2),
]

LYRICS = {
    "verse_1": [
        "楼下的风 把衣架轻轻摇", "你把纸箱 一个个搬到门口", "隔壁的旧歌 又唱到副歌",
        "我们都装作 只是普通周末", "自动贩卖机 吞下最后硬币", "两罐热咖啡 在掌心冒着气",
    ],
    "pre_1": ["夜班车还有 十分钟才到", "你问我真的 都准备好了吗", "我把没发的消息 按成删除"],
    "chorus_1": [
        "你送我到 这盏灯就好", "前面的路 我想自己走", "别把再见 说得太郑重",
        "明天醒来 只是换个窗口", "我会记得 你把伞偏向我", "也会学会 不回头地走",
    ],
    "verse_2": [
        "耳机分给你 左边那一只", "那首旧歌走到 熟悉的副歌", "沿河的栏杆 还留着水汽",
        "鞋底认得 每一道旧裂缝", "没有发出去的 那句保重", "现在说出来 反而很轻松",
    ],
    "pre_2": ["远处的车灯 一盏一盏靠近", "你没有再问 我要去哪里", "我也终于不再 低头看手机"],
    "chorus_2": [
        "你送我到 这盏灯就好", "车门以后 我想自己走", "这次再见 不必太郑重",
        "我们都还有 各自的清晨", "我会记得 你把伞偏向我", "也会记得 我能自己走",
    ],
    "bridge": ["有些同行 不需要走到底", "才算没有辜负 这一段路", "等下一场雨 落在别的城市", "我会先替自己 把伞撑住"],
    "final_chorus": [
        "你送我到 这盏灯就好", "剩下的路 我会自己走", "不用把再见 说得太郑重",
        "有些同行 已经足够", "如果下雨 我会撑开那把伞", "如果想起你 我就听那首歌",
        "等到天亮 我会好好往前走",
    ],
    "outro": ["你送我到 这盏灯就好"],
}

PROGRESSIONS = {
    "intro": ["Em7", "Cadd9", "G6", "Dsus4/F#", "Em7", "Cadd9", "G6", "D"],
    "verse_1": ["Em7", "Cadd9", "G6", "Dsus4/F#", "Em7", "Cadd9", "G6", "D", "Am7", "Cadd9", "G6", "D"],
    "pre_1": ["Am7", "Cadd9", "G/B", "D", "Am7", "Dsus4/F#"],
    "chorus_1": ["Cadd9", "G6", "D", "Em7", "Cadd9", "G/B", "Am7", "D", "Cadd9", "G6", "D", "Em7"],
    "interlude": ["Am7", "Cadd9", "G6", "D"],
    "verse_2": ["Em7", "G/B", "Cadd9", "G6", "Em7", "Cadd9", "Am7", "D", "Em7", "G/B", "Cadd9", "D"],
    "pre_2": ["Am7", "Cadd9", "G/B", "D", "Cadd9", "Dsus4/F#"],
    "chorus_2": ["Cadd9", "G6", "D", "Em7", "Cadd9", "G/B", "Am7", "D", "Em7", "Cadd9", "G6", "D"],
    "bridge": ["Em7", "D", "Cadd9", "G/B", "Am7", "Em7", "Cadd9", "Dsus4/F#"],
    "final_chorus": ["Cadd9", "G6", "D", "Em7", "Cadd9", "G/B", "Am7", "D", "Em7", "Cadd9", "G6", "D", "Cadd9", "D"],
    "outro": ["Em7", "Cadd9", "G6", "D", "G6", "G6"],
}

# Sounding pitch, string (0 low E ... 5 high E), fret. The D4/G4 top pair is deliberately retained.
ACOUSTIC = {
    "Em7": [("E2", 0, 0), ("B2", 1, 2), ("E3", 2, 2), ("G3", 3, 0), ("D4", 4, 3), ("G4", 5, 3)],
    "Cadd9": [("C3", 1, 3), ("E3", 2, 2), ("G3", 3, 0), ("D4", 4, 3), ("G4", 5, 3)],
    "G6": [("G2", 0, 3), ("B2", 1, 2), ("D3", 2, 0), ("G3", 3, 0), ("B3", 4, 0), ("E4", 5, 0)],
    "Dsus4/F#": [("F#2", 0, 2), ("A2", 1, 0), ("D3", 2, 0), ("A3", 3, 2), ("D4", 4, 3), ("G4", 5, 3)],
    "D": [("D3", 2, 0), ("A3", 3, 2), ("D4", 4, 3), ("F#4", 5, 2)],
    "Am7": [("A2", 1, 0), ("E3", 2, 2), ("G3", 3, 0), ("C4", 4, 1), ("E4", 5, 0)],
    "G/B": [("B2", 1, 2), ("D3", 2, 0), ("G3", 3, 0), ("B3", 4, 0), ("G4", 5, 3)],
}

ELECTRIC_LOW = {
    "Em7": [("E2", 0, 0), ("B2", 1, 2), ("E3", 2, 2)], "Cadd9": [("C3", 1, 3), ("G3", 2, 5), ("C4", 3, 5)],
    "G6": [("G2", 0, 3), ("D3", 1, 5), ("G3", 2, 5)], "Dsus4/F#": [("F#2", 0, 2), ("C#3", 1, 4), ("F#3", 2, 4)],
    "D": [("D3", 1, 5), ("A3", 2, 7), ("D4", 3, 7)], "Am7": [("A2", 0, 5), ("E3", 1, 7), ("A3", 2, 7)],
    "G/B": [("B2", 0, 7), ("F#3", 1, 9), ("B3", 2, 9)],
}

ELECTRIC_HIGH = {
    "Em7": [("G4", 4, 8), ("B4", 5, 7)], "Cadd9": [("G4", 4, 8), ("D5", 5, 10)],
    "G6": [("B4", 4, 12), ("E5", 5, 12)], "Dsus4/F#": [("A4", 4, 10), ("D5", 5, 10)],
    "D": [("A4", 4, 10), ("F#5", 5, 14)], "Am7": [("G4", 4, 8), ("C5", 5, 8)],
    "G/B": [("G4", 4, 8), ("B4", 5, 7)],
}

ROOTS = {"Em7": "E2", "Cadd9": "C2", "G6": "G1", "Dsus4/F#": "F#1", "D": "D2", "Am7": "A1", "G/B": "B1"}
FIFTHS = {"Em7": "B2", "Cadd9": "G2", "G6": "D2", "Dsus4/F#": "A1", "D": "A2", "Am7": "E2", "G/B": "D2"}
OCTAVES = {"Em7": "E3", "Cadd9": "C3", "G6": "G2", "Dsus4/F#": "F#2", "D": "D3", "Am7": "A2", "G/B": "B2"}

START = {}
cursor = 1
for name, bars, _ in SECTIONS:
    START[name] = cursor
    cursor += bars

NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi_number(pitch: str) -> int:
    letter, rest = pitch[0], pitch[1:]
    accidental = 1 if rest.startswith("#") else -1 if rest.startswith("b") else 0
    octave = int(rest[1:] if accidental else rest)
    return (octave + 1) * 12 + NOTE_BASE[letter] + accidental


def dump(name, data):
    (ROOT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def at(offset: float) -> str:
    bar = int(offset // 4) + 1
    beat = offset - (bar - 1) * 4 + 1
    return f"{bar}:{beat:g}"


def local_offset(event):
    bar, beat = event["at"].split(":")
    return (int(bar) - 1) * 4 + float(beat) - 1


def note(pitch, offset, duration, velocity, **extra):
    result = {"type": "note", "pitch": pitch, "at": at(offset), "duration": round(duration, 3), "velocity": int(velocity)}
    result.update(extra)
    return result


def drum(number, offset, velocity, **extra):
    result = {"type": "drum", "note": number, "at": at(offset), "duration": .1, "velocity": int(velocity)}
    result.update(extra)
    return result


def clean_chars(text):
    return [char for char in text if char not in " ，。！？、"]


MELODY_POOLS = {
    "verse": ["B3", "D4", "E4", "G4", "E4", "D4", "B3", "D4", "E4", "D4", "B3", "A3", "B3"],
    "pre": ["D4", "E4", "G4", "A4", "G4", "A4", "B4", "A4", "G4", "E4", "G4", "A4", "B4"],
    "chorus": ["G4", "G4", "A4", "B4", "D5", "B4", "A4", "G4", "E4", "G4", "A4", "B4", "D5", "B4"],
    "bridge": ["B3", "D4", "E4", "F#4", "E4", "D4", "B3", "D4", "E4", "G4", "A4", "G4"],
    "outro": ["G4", "A4", "B4", "D5", "B4", "A4", "G4", "E4", "G4"],
}


def melody_section(section, bars):
    lines = LYRICS.get(section, [])
    if not lines:
        return [], [], []
    family = "verse" if section.startswith("verse") else "pre" if section.startswith("pre") else "chorus" if "chorus" in section else section
    pool = MELODY_POOLS[family]
    events, mappings, phrases = [], [], []
    for line_index, lyric in enumerate(lines):
        chars = clean_chars(lyric)
        phrase_start = line_index * 8
        usable = 6.25 if len(chars) >= 10 else 6.0
        step = usable / max(1, len(chars) - 1)
        onsets = [round((.35 + index * step) * 4) / 4 for index in range(len(chars))]
        for index in range(1, len(onsets)):
            if onsets[index] <= onsets[index - 1]:
                onsets[index] = onsets[index - 1] + .5
        if onsets[-1] > 7.3:
            scale = 6.95 / (onsets[-1] - onsets[0])
            onsets = [onsets[0] + (value - onsets[0]) * scale for value in onsets]
        phrase_notes = []
        for index, (char, onset) in enumerate(zip(chars, onsets)):
            next_onset = onsets[index + 1] if index + 1 < len(onsets) else 7.7
            duration = min(1.35 if index == len(chars) - 1 else .92, max(.32, (next_onset - onset) * .8))
            if index == len(chars) - 1:
                duration = min(1.2, max(1.0, 7.65 - onset))
            cross = False
            if 3.65 <= onset < 4 and next_onset >= 4.3:
                duration = max(duration, 4.14 - onset); cross = True
            pitch = pool[(index + line_index * 2) % len(pool)]
            if section == "chorus_2" and line_index in {0, 5} and index == len(chars) - 1:
                pitch = "D5"
            if section == "final_chorus" and line_index >= 4 and index in {3, 6, 9}:
                pitch = "E5"
            stress = index in {0, len(chars) - 1} or char in "送灯好路走伞自己再见清晨"
            velocity = (90 if family == "chorus" else 77 if family == "verse" else 83) + (7 if stress else 0) + ((index + 2 * line_index) % 4 - 1)
            position = phrase_start + onset
            events.append(note(pitch, position, duration, velocity, _lyric=char, _phrase=line_index + 1,
                               _stress=stress, _cross_bar=cross, _vocal_proxy=True))
            entry = {"text": char, "bar": START[section] + int(position // 4), "beat": round(position % 4 + 1, 3),
                     "duration": round(duration, 3), "pitch": midi_number(pitch), "pitch_name": pitch,
                     "stress": stress, "crosses_barline": cross}
            mappings.append({"section": section, "line": line_index + 1, **entry})
            phrase_notes.append(entry)
        breath = round(8 - (onsets[-1] + events[-1]["duration"]), 3)
        phrases.append({"section": section, "bars": [START[section] + line_index * 2, START[section] + line_index * 2 + 1],
                        "lyric": lyric, "syllables": phrase_notes, "breath_after": True, "breath_beats": breath})
    return events, mappings, phrases


def guitar_note(item, offset, duration, velocity, group, direction, action, **extra):
    pitch, string, fret = item
    return note(pitch, offset, duration, velocity, _string=string, _fret=fret, _attack_group=group,
                _strum_direction=direction, _right_hand=action, **extra)


def sweep(events, voicing, base, start, indices, direction, duration, velocity, group, action, spread=.034, **extra):
    order = indices if direction == "down" else list(reversed(indices))
    for order_index, tone_index in enumerate(order):
        events.append(guitar_note(voicing[tone_index], base + start + order_index * spread, duration - order_index * .015,
                                  velocity + order_index, group, direction, action, **extra))


def acoustic_events(section, bars):
    events = []
    progression = PROGRESSIONS[section]
    for bar_index, chord in enumerate(progression):
        base, voicing = bar_index * 4, ACOUSTIC[chord]
        top = len(voicing) - 1
        if section == "intro":
            pattern = [(0, 0, .92), (.72, min(2, top), .64), (1.42, top, .68), (2.1, min(3, top), .66), (2.82, max(1, top - 1), .61), (3.46, top, .48)]
            for idx, (off, tone, dur) in enumerate(pattern):
                events.append(guitar_note(voicing[tone], base + off, dur, 58 + idx + (3 if bar_index >= 4 else 0),
                                          f"intro-{bar_index+1}-arp-{idx+1}", "alternate", "fingerpicked_connection",
                                          _common_tone_candidate=tone >= top - 1))
            if bar_index >= 4 and bar_index % 2 == 1:
                sweep(events, voicing, base, 3.55, list(range(max(0, top - 3), top + 1)), "up", .38, 61,
                      f"intro-{bar_index+1}-pickup", "breath_pickup", _anticipated_change=True)
        elif section == "interlude":
            # Vocal-free development: brighter high-string arpeggio plus a low-to-high connector.
            pattern = [(0, 0, .82), (.58, min(2, top), .52), (1.12, top, .62), (1.78, max(1, top - 1), .55)]
            for idx, (off, tone, dur) in enumerate(pattern):
                events.append(guitar_note(voicing[tone], base + off, dur, 63 + idx + bar_index,
                                          f"interlude-{bar_index+1}-arp-{idx+1}", "alternate", "high_string_interlude_connection",
                                          _common_tone_candidate=tone >= top - 1))
            sweep(events, voicing, base, 2.48, list(range(len(voicing))), "down", .72, 66 + bar_index,
                  f"interlude-{bar_index+1}-sweep", "interlude_bass_to_high_sweep", _full_strum=True)
            sweep(events, voicing, base, 3.46, list(range(max(1, top - 2), top + 1)), "up", .42, 61 + bar_index,
                  f"interlude-{bar_index+1}-up", "interlude_high_return", _partial_strum=True,
                  _anticipated_change=bar_index == bars - 1)
        elif section == "verse_1":
            events.append(guitar_note(voicing[0], base, .78, 63, f"v1-{bar_index+1}-bass", "down", "bass_note_first", _palm_muted=True))
            sweep(events, voicing, base, .54, list(range(1, min(4, top + 1))), "down", .48, 60,
                  f"v1-{bar_index+1}-partial1", "light_partial_strum", _palm_muted=True, _partial_strum=True)
            ghost_item = voicing[min(2, top)]
            events.append(guitar_note(ghost_item, base + 1.48, .16, 38, f"v1-{bar_index+1}-ghost", "up", "ghost_upstroke", _ghost_strum=True, _muted_strum=True))
            sweep(events, voicing, base, 2.02, list(range(0, min(4, top + 1))), "down", .56, 64,
                  f"v1-{bar_index+1}-partial2", "downstroke_pulse", _palm_muted=bar_index < 8, _partial_strum=True)
            indices = list(range(max(1, top - (3 if bar_index % 2 else 2)), top + 1))
            sweep(events, voicing, base, 3.45, indices, "up", .42 if bar_index % 2 else .34, 57,
                  f"v1-{bar_index+1}-up", "phrase_continuation", _partial_strum=True, _breath_emphasis=bar_index % 2 == 1)
        elif section.startswith("pre"):
            openness = bar_index / max(1, bars - 1)
            groups = [0, 1.0, 2.0, 3.0] if bar_index < 2 else [0, .75, 1.5, 2.25, 3.0, 3.5]
            for group_index, off in enumerate(groups):
                direction = "down" if group_index % 2 == 0 else "up"
                count = min(len(voicing), 3 + int(openness * 3) + (1 if group_index == 0 else 0))
                indices = list(range(count)) if direction == "down" else list(range(max(0, len(voicing) - count), len(voicing)))
                sweep(events, voicing, base, off, indices, direction, .42 + openness * .25, 62 + bar_index * 2 + group_index,
                      f"{section}-{bar_index+1}-{group_index+1}", "gradual_opening_sweep",
                      _palm_muted=bar_index < 2, _partial_strum=count < len(voicing), _full_strum=count == len(voicing))
            if bar_index >= (3 if section == "pre_2" else 4):
                next_chord = progression[(bar_index + 1) % len(progression)]
                item = ACOUSTIC[next_chord][0]
                events.append(guitar_note(item, base + 3.72, .22, 72, f"{section}-{bar_index+1}-anticipation",
                                          "down", "anticipated_bass_change", _anticipated_change=True))
        elif section in {"chorus_1", "chorus_2", "final_chorus"}:
            attacks = [(0, "down", True), (.5, "up", False), (1.5, "up", False), (2.0, "down", True), (2.75, "down", False), (3.5, "up", False)]
            if section == "chorus_2": attacks.insert(4, (2.5, "up", False))
            if section == "final_chorus":
                attacks = [(0, "down", True), (.5, "up", False), (1.25, "up", False), (2.0, "down", True),
                           (2.65, "up", False), (3.25, "down", bar_index >= 6), (3.7, "up", False)]
            for group_index, (off, direction, strong) in enumerate(attacks):
                if strong:
                    indices = list(range(len(voicing)))
                elif group_index % 3 == 1:
                    indices = [min(2, top)]  # audible muted/ghost continuation of the right hand
                else:
                    indices = list(range(max(1, top - 2), top + 1))
                action = "full_open_sweep" if strong else "ghost_continuation" if len(indices) == 1 else "upper_partial_upstroke"
                sweep(events, voicing, base, off, indices, direction, .62 if strong else .34, 70 + (8 if strong else 0) + (3 if section == "final_chorus" else 0),
                      f"{section}-{bar_index+1}-{group_index+1}", action,
                      _full_strum=strong, _partial_strum=not strong and len(indices) > 1,
                      _ghost_strum=len(indices) == 1, _muted_strum=len(indices) == 1)
            if bar_index % 4 == 3 and bar_index < bars - 1:
                next_voicing = ACOUSTIC[progression[bar_index + 1]]
                events.append(guitar_note(next_voicing[0], base + 3.72, .24, 75, f"{section}-{bar_index+1}-anticipation",
                                          "down", "anticipated_bass_change", _anticipated_change=True))
        elif section == "verse_2":
            arpeggio = [(0, 0, .72), (.62, min(2, top), .50), (1.18, top, .54)]
            for idx, (off, tone, dur) in enumerate(arpeggio):
                events.append(guitar_note(voicing[tone], base + off, dur, 61 + idx, f"v2-{bar_index+1}-arp-{idx+1}",
                                          "alternate", "bass_to_high_arpeggio", _common_tone_candidate=tone == top))
            sweep(events, voicing, base, 2.0, list(range(1, min(5, top + 1))), "down", .64, 65,
                  f"v2-{bar_index+1}-partial", "flowing_partial_strum", _partial_strum=True)
            events.append(guitar_note(voicing[min(3, top)], base + 2.96, .17, 40, f"v2-{bar_index+1}-ghost", "up", "ghost_upstroke",
                                      _ghost_strum=True, _muted_strum=True))
            sweep(events, voicing, base, 3.47, list(range(max(1, top - 2), top + 1)), "up", .40, 60 + bar_index % 3,
                  f"v2-{bar_index+1}-up", "high_string_connection", _partial_strum=True, _anticipated_change=bar_index % 3 == 2)
        elif section == "bridge":
            if bar_index < 4:
                pattern = [(0, 0, 1.15), (1.0, top, .85), (2.0, min(2, top), .86), (3.0, max(1, top - 1), .78)]
                for idx, (off, tone, dur) in enumerate(pattern):
                    events.append(guitar_note(voicing[tone], base + off, dur, 57 + idx + bar_index,
                                              f"bridge-{bar_index+1}-arp-{idx+1}", "alternate", "foreground_arpeggio",
                                              _common_tone_candidate=tone >= top - 1))
            else:
                for group_index, off in enumerate([0, 1.0, 2.0, 3.0, 3.5][:bar_index - 1]):
                    direction = "down" if group_index % 2 == 0 else "up"
                    indices = list(range(min(len(voicing), 3 + (bar_index - 4))))
                    sweep(events, voicing, base, off, indices, direction, .55, 63 + bar_index + group_index,
                          f"bridge-{bar_index+1}-build-{group_index+1}", "rebuilding_sweep", _partial_strum=len(indices) < len(voicing))
        elif section == "outro":
            if bar_index < 4:
                pattern = [(0, 0, 1.0), (.9, min(2, top), .78), (1.8, top, .92), (2.8, max(1, top - 1), .82)]
                for idx, (off, tone, dur) in enumerate(pattern):
                    events.append(guitar_note(voicing[tone], base + off, dur, 54 - bar_index + idx,
                                              f"outro-{bar_index+1}-{idx+1}", "alternate", "intro_texture_return"))
            else:
                sweep(events, voicing, base, 0, list(range(len(voicing))), "down", 3.7 if bar_index == bars - 1 else 3.0,
                      54 - bar_index, f"outro-{bar_index+1}-final", "natural_final_sweep", _full_strum=True, _natural_release=True)
    return events


HAND_MOTION = ["down", "up", "down", "up", "down", "up", "down", "up"]


def _grid_action(group_events):
    if any(event.get("_ghost_strum") for event in group_events):
        return "ghost_strum"
    if any(event.get("_muted_strum") or event.get("_palm_muted") for event in group_events):
        return "muted_strum"
    if any(event.get("_full_strum") or event.get("_open_power") for event in group_events):
        return "accent_strum"
    if any(event.get("_sustain") for event in group_events):
        return "sustained_chord_hit"
    return "partial_strum"


def strumming_grid_from_events(events, bars, section, instrument):
    """Preserve silent right-hand travel while keeping the authored MIDI events unchanged."""
    by_bar = defaultdict(lambda: defaultdict(list))
    for event in events:
        bar = int(event["at"].split(":", 1)[0])
        group = event.get("_attack_group", f"event-{len(by_bar[bar])}")
        by_bar[bar][group].append(event)
    result = []
    for bar in range(1, bars + 1):
        actions = ["air_strum"] * 8
        occupied = set()
        ordered = sorted(by_bar[bar].values(), key=lambda group: local_offset(group[0]) % 4)
        for group in ordered:
            ideal = max(0, min(7, int(round((local_offset(group[0]) % 4) * 2))))
            available = [step for step in range(8) if step not in occupied]
            if not available:
                break
            authored_direction = group[0].get("_strum_direction")
            direction_matched = [step for step in available if HAND_MOTION[step] == authored_direction]
            candidates = direction_matched or available
            step = min(candidates, key=lambda value: (abs(value - ideal), value))
            occupied.add(step)
            actions[step] = _grid_action(group)
        sounding = sum(action != "air_strum" for action in actions)
        result.append({
            "bar": bar, "subdivision": "eighth", "hand_motion": HAND_MOTION,
            "actions": actions, "sounding_strum_count": sounding, "hand_motion_count": 8,
            "pattern_id": f"{instrument}_{section}", "last_hand_direction": "up",
            "next_expected_direction": "down", "pattern_continues_across_bar": not (section == "outro" and bar == bars),
        })
    return result


def electric_rhythm_events(section, bars):
    events = []
    for bar_index, chord in enumerate(PROGRESSIONS[section]):
        base, shape = bar_index * 4, ELECTRIC_LOW[chord]
        if section == "intro":
            if bar_index < 4: continue
            attacks = [(0, "down", [0, 1]), (1.5, "up", [1, 2]), (2.5, "down", [0, 1]), (3.5, "up", [1, 2])]
            for idx, (off, direction, indices) in enumerate(attacks):
                sweep(events, shape, base, off, indices, direction, .42, 49 + bar_index + idx,
                      f"er-intro-{bar_index+1}-{idx+1}", "restrained_entry_motion", spread=.04,
                      _partial_strum=True, _palm_muted=True)
        elif section == "verse_1":
            attacks = [(0, "down", [0, 1]), (1, "down", [0]), (1.5, "up", [1, 2]),
                       (2.5, "up", [0, 1]), (3.5, "up", [1, 2])]
            for idx, (off, direction, indices) in enumerate(attacks):
                sweep(events, shape, base, off, indices, direction, .26 if len(indices) == 1 else .38,
                      47 + bar_index % 4 + idx, f"er-v1-{bar_index+1}-{idx+1}",
                      "palm_muted_continuous_cell", spread=.035, _palm_muted=True,
                      _muted_strum=len(indices) == 1, _partial_strum=True)
        elif section == "verse_2":
            attacks = [(0, "down", [0, 1]), (.5, "up", [1, 2]), (1.5, "up", [0, 1]),
                       (2, "down", [0]), (3, "down", [0, 1]), (3.5, "up", [1, 2])]
            for idx, (off, direction, indices) in enumerate(attacks):
                sweep(events, shape, base, off, indices, direction, .28 if len(indices) == 1 else .42,
                      51 + bar_index % 4 + idx, f"er-v2-{bar_index+1}-{idx+1}",
                      "developed_muted_electric_cell", spread=.038, _palm_muted=idx < 4,
                      _muted_strum=len(indices) == 1, _partial_strum=True)
        elif section.startswith("pre"):
            offsets = [0, 1, 2, 3] if bar_index < 3 else [0, .75, 1.5, 2.25, 3, 3.5]
            for idx, off in enumerate(offsets):
                sweep(events, shape, base, off, [0, 1], "down" if idx % 2 == 0 else "up", .42 + bar_index * .035,
                      57 + bar_index * 2 + idx, f"er-{section}-{bar_index+1}-{idx+1}", "muted_to_open_dyad",
                      spread=.04, _palm_muted=bar_index < 3, _partial_strum=True)
        elif section in {"chorus_1", "chorus_2", "final_chorus"}:
            attacks = [(0, "down"), (.5, "up"), (1.5, "up"), (2, "down"), (3, "down"), (3.5, "up")]
            if section == "chorus_2": attacks.insert(4, (2.5, "up"))
            if section == "final_chorus": attacks = [(step / 2, HAND_MOTION[step]) for step in range(8)]
            for idx, (off, direction) in enumerate(attacks):
                full = idx in {0, 3} or (section == "final_chorus" and idx in {4, 6})
                indices = list(range(len(shape))) if full else ([0] if idx % 3 == 1 else [1, 2])
                sweep(events, shape, base, off, indices, direction, .52 if full else .28,
                      66 + idx * 2 + (5 if section == "final_chorus" else 0),
                      f"er-{section}-{bar_index+1}-{idx+1}",
                      "open_power_accent" if full else "short_power_continuation", spread=.042,
                      _open_power=full, _electric_width=True, _partial_strum=not full,
                      _muted_strum=len(indices) == 1)
        elif section == "interlude":
            sweep(events, shape, base, 0, list(range(len(shape))), "down", 2.4, 61 + bar_index,
                  f"er-interlude-{bar_index+1}", "open_interlude_chord", spread=.05, _open_power=True)
        elif section == "bridge":
            if bar_index < 6: continue
            sweep(events, shape, base, 0, [0, 1], "down", 3.0, 58 + bar_index,
                  f"er-bridge-{bar_index+1}", "late_bridge_sustain", spread=.055, _sustain=True)
        elif section == "outro":
            if bar_index < 2:
                sweep(events, shape, base, 0, [1, 2], "down", 2.7, 48 - bar_index,
                      f"er-outro-{bar_index+1}", "electric_exit_sustain", spread=.05, _sustain=True)
    return events


def electric_texture_events(section, bars):
    events = []
    if section not in {"chorus_1", "interlude", "verse_2", "chorus_2", "final_chorus"}:
        return events
    for bar_index, chord in enumerate(PROGRESSIONS[section]):
        base, shape = bar_index * 4, ELECTRIC_HIGH[chord]
        active = section == "interlude" or (section == "verse_2" and bar_index % 4 == 3) or ("chorus" in section and bar_index % 4 in {1, 3})
        if not active: continue
        if section == "interlude":
            pitches = [shape[0], shape[1], shape[0]]
            offsets = [.5, 1.75, 3.0]
            for idx, (item, off) in enumerate(zip(pitches, offsets)):
                durations = [.82, .96, .70]
                events.append(guitar_note(item, base + off, durations[idx], 57 + idx + bar_index, f"et-int-{bar_index+1}-{idx+1}",
                                          "alternate", "compact_interlude_fill", _fill=True))
        else:
            start = 3.05 if bar_index % 4 == 1 else 2.75
            for idx, item in enumerate(shape):
                events.append(guitar_note(item, base + start + idx * .08, .72 - idx * .05, 55 + idx * 3 + bar_index % 4 + (4 if section == "final_chorus" else 0),
                                          f"et-{section}-{bar_index+1}", "up", "phrase_gap_response", _fill=True))
    return events


def bass_events(section, bars):
    events, progression = [], PROGRESSIONS[section]
    for bar_index, chord in enumerate(progression):
        base = bar_index * 4
        root, fifth, octave = ROOTS[chord], FIFTHS[chord], OCTAVES[chord]
        if section == "bridge" and bar_index < 4:
            pattern = [(0, root, 2.35, "root"), (2.5, fifth, 1.15, "fifth")]
        elif section.startswith("verse") or section == "intro":
            pattern = [(0, root, 1.4, "root"), (1.5, fifth, .85, "fifth"), (2.5, root, .82, "root"), (3.5, octave, .38, "approach")]
        elif "chorus" in section:
            pattern = [(0, root, .72, "root"), (1, fifth, .68, "fifth"), (2, octave, .68, "octave"), (3, fifth, .44, "fifth"), (3.5, root, .38, "approach")]
        else:
            pattern = [(0, root, .9, "root"), (1.25, fifth, .7, "fifth"), (2.25, octave, .7, "octave"), (3.25, root, .55, "approach")]
        for idx, (off, pitch, duration, function) in enumerate(pattern):
            events.append(note(pitch, base + off, duration, 68 + idx * 3 + (6 if "chorus" in section else 0), _bass_function=function,
                               _picking="pick", _cross_bar_connection=off >= 3.25))
    return events


def drum_events(section, bars):
    events = []
    energy = next(e for name, _, e in SECTIONS if name == section)
    for bar in range(bars):
        base = bar * 4
        if section == "intro" and bar < 4:
            if bar >= 2:
                events.append(drum(42, base + 2, 35 + bar, _limb="right_hand", _role="soft_count"))
            continue
        if bar == 0 or ("chorus" in section and bar % 4 == 0):
            events.append(drum(49, base, 78 + energy * 2, _limb="right_hand", _role="section_crash"))
        half_time = section == "bridge" and bar < 4
        if "chorus" in section:
            cymbal = 51 if section == "final_chorus" and bar >= 6 else 42
            hat_offsets = [x * .5 for x in range(8)]
        elif half_time:
            cymbal, hat_offsets = 42, [0, 1, 2, 3]
        else:
            cymbal, hat_offsets = 42, [x * .5 for x in range(8)]
        for idx, off in enumerate(hat_offsets):
            note_num = 46 if section.startswith("pre") and bar >= bars - 2 and idx == len(hat_offsets) - 1 else cymbal
            events.append(drum(note_num, base + off, 44 + (idx % 2) * 7 + energy + bar % 3, _limb="right_hand", _role="pulse"))
        if section.startswith("verse"):
            kick_variants = [[0, 2.5], [0, 2], [0, .75, 2.5], [0, 2.25, 3.25]]
        elif half_time:
            kick_variants = [[0, 2.75], [0, 3.0], [0, 1.5, 3], [0, 2.5]]
        else:
            kick_variants = [[0, 1.5, 2.5], [0, 1.75, 2.5], [0, .75, 2.5], [0, 1.5, 2.5, 3.25]]
        for off in kick_variants[bar % 4]:
            events.append(drum(36, base + off, 73 + energy * 2, _limb="right_foot", _role="kick"))
        snare_offsets = [2] if half_time else [1, 3]
        for off in snare_offsets:
            events.append(drum(38, base + off, 76 + energy * 2, _limb="left_hand", _role="backbeat"))
        if bar == bars - 1 and section not in {"verse_1", "verse_2", "outro"}:
            for idx, off in enumerate([3, 3.25, 3.5, 3.75]):
                events.append(drum([45, 47, 48, 50][idx], base + off, 67 + idx * 6, _limb="left_hand" if idx % 2 == 0 else "right_hand", _role="boundary_fill"))
    return events


def pad_events(section, bars):
    if section not in {"bridge", "final_chorus", "outro"}: return []
    events = []
    for bar_index, chord in enumerate(PROGRESSIONS[section]):
        if section == "final_chorus" and bar_index < 6: continue
        if section == "outro" and bar_index < 2: continue
        shape = ELECTRIC_HIGH[chord]
        for idx, item in enumerate(shape):
            events.append(note(item[0], bar_index * 4 + idx * .025, 3.72, 38 + idx * 3 + bar_index % 3, _role="late_harmonic_plane", _common_tone=True))
    return events


def trim_same_pitch_overlaps(track, section_defs):
    by_pitch, section_offset = defaultdict(list), 0.0
    for section, bars, _ in section_defs:
        clip = track.get("sections", {}).get(section)
        if clip:
            for event in clip["events"]:
                by_pitch[event["pitch"]].append((section_offset + local_offset(event), event))
        section_offset += bars * 4
    count = 0
    for entries in by_pitch.values():
        entries.sort(key=lambda item: item[0])
        for (start, event), (next_start, _) in zip(entries, entries[1:]):
            if start + event["duration"] > next_start:
                event["duration"] = round(max(.08, next_start - start - .035), 3)
                event["_controlled_release_before_reattack"] = True
                count += 1
    return count


def clip(events, bars, *, strumming_grid=None):
    value = {"loop_bars": bars, "events": events}
    if strumming_grid is not None:
        value["strumming_grid"] = strumming_grid
    return value


def build(include_full=True):
    mapping, phrases = [], []
    tracks = {
        "vocal_melody": {"role": "strictly monophonic main melody proxy", "sections": {}},
        "acoustic_guitar": {"role": "continuous acoustic guitar strum arpeggio line", "sections": {}},
    }
    if include_full:
        tracks.update({
            "electric_rhythm_guitar": {"role": "sectional electric rhythm width and propulsion", "sections": {}},
            "electric_texture_guitar": {"role": "restrained high guitar texture and phrase-gap fills", "sections": {}},
            "bass": {"role": "independent connected electric bass line", "sections": {}},
            "drums": {"role": "pop rock drum kit groove", "sections": {}},
            "orchestra_pad": {"role": "late sustained harmonic plane", "sections": {}},
        })
    for section, bars, _ in SECTIONS:
        melody, section_mapping, section_phrases = melody_section(section, bars)
        mapping += section_mapping; phrases += section_phrases
        if melody: tracks["vocal_melody"]["sections"][section] = clip(melody, bars)
        acoustic = acoustic_events(section, bars)
        tracks["acoustic_guitar"]["sections"][section] = clip(
            acoustic, bars, strumming_grid=strumming_grid_from_events(acoustic, bars, section, "acoustic")
        )
        if include_full:
            electric = electric_rhythm_events(section, bars)
            texture = electric_texture_events(section, bars)
            if electric:
                tracks["electric_rhythm_guitar"]["sections"][section] = clip(
                    electric, bars, strumming_grid=strumming_grid_from_events(electric, bars, section, "electric")
                )
            if texture: tracks["electric_texture_guitar"]["sections"][section] = clip(texture, bars)
            tracks["bass"]["sections"][section] = clip(bass_events(section, bars), bars)
            tracks["drums"]["sections"][section] = clip(drum_events(section, bars), bars)
            pad = pad_events(section, bars)
            if pad: tracks["orchestra_pad"]["sections"][section] = clip(pad, bars)
    releases = {name: trim_same_pitch_overlaps(track, SECTIONS) for name, track in tracks.items() if "guitar" in name}
    composition = {
        "metadata": {"title": "送到这盏灯就好", "english_title": "Walk Me to This Streetlamp", "tempo": TEMPO,
                     "time_signature": "4/4", "key": "G major / E minor", "language": "zh-CN", "seed": 114100,
                     "vocal_rendering": "disabled; Sine Wave monophonic proxy only", "guitar_controlled_releases": releases,
                     "stage": "full" if include_full else "acoustic_skeleton"},
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 4, "arrangement": 4, "melodic_ornamentation": 2, "density": 3, "variation": 5},
        "complexity_contour": "verse_chorus",
        "sections": [{"name": name, "bars": bars, "energy": energy, "complexity": {"level": "rich" if energy >= 8 else "standard"},
                      "complexity_budget": ({"lead": 4, "acoustic": 5, "electric": 2, "rhythm": 3, "texture": 1}
                                            if energy >= 8 else {"lead": 3, "acoustic": 4, "electric": 1, "rhythm": 2, "texture": 1})}
                     for name, bars, energy in SECTIONS],
        "tracks": tracks,
    }
    return composition, mapping, phrases


def configs(acoustic_only=False):
    instruments = {
        "vocal_melody": {"engine": "fluidsynth", "bank": 8, "program": 80, "gm_name": "Sine Wave"},
        "acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25, "gm_name": "Steel Guitar"},
    }
    mix = {"vocal_melody": {"volume_db": 4.0, "pan": 0.0, "mute": False},
           "acoustic_guitar": {"volume_db": 3.0, "pan": -0.18, "mute": False}}
    if not acoustic_only:
        instruments.update({
            "electric_rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29, "gm_name": "Overdrive Guitar"},
            "electric_texture_guitar": {"engine": "fluidsynth", "bank": 12, "program": 27, "gm_name": "Clean Guitar 2"},
            "bass": {"engine": "fluidsynth", "bank": 0, "program": 34, "gm_name": "Electric Bass (pick)"},
            "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16, "gm_name": "Power Drum Kit"},
            "orchestra_pad": {"engine": "fluidsynth", "bank": 8, "program": 48, "gm_name": "Orchestra Pad"},
        })
        mix.update({
            "electric_rhythm_guitar": {"volume_db": -1.2, "pan": 0.38, "mute": False},
            "electric_texture_guitar": {"volume_db": -4.5, "pan": 0.58, "mute": False},
            "bass": {"volume_db": 3.0, "pan": 0.0, "mute": False}, "drums": {"volume_db": 3.2, "pan": 0.0, "mute": False},
            "orchestra_pad": {"volume_db": -8.0, "pan": 0.12, "mute": False},
        })
    dump("instruments.json", instruments)
    dump("render.json", {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": .82,
                         "tail_seconds": 2.0, "master_peak_db": -1.0, "mix": mix})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["acoustic", "full"], default="full")
    args = parser.parse_args()
    full = args.stage == "full"
    composition, mapping, phrases = build(include_full=full)
    dump("lyric_note_mapping.json", {"title": composition["metadata"]["title"], "tempo": TEMPO, "phrases": phrases, "mapping": mapping})
    dump("acoustic_guitar_arrangement.json", {
        "principle": "continuous right-hand motion and voicing path before notes", "tuning": "E2 A2 D3 G3 B3 E4",
        "section_strategies": {"intro": "arpeggio plus late pickups", "verse_1": "bass-first partial/ghost sweep",
                               "pre": "gradual mute-to-open sweeps", "chorus": "continuous unequal full/partial down-up cells",
                               "verse_2": "arpeggio plus high-string and ghost-upstroke variation", "bridge": "foreground arpeggio then rebuild",
                               "final": "developed extra-group sweep", "outro": "intro texture and natural sustain"},
        "voicings": {chord: [{"pitch": p, "string": s, "fret": f} for p, s, f in shape] for chord, shape in ACOUSTIC.items()},
        "prohibited": ["simultaneous block chord", "vocal syllable following", "one pattern for all sections", "electric guitar copy"],
    })
    dump("electric_guitar_arrangement.json", {
        "rhythm_role": "low-mid sectional width; sparse verse, propulsion pre, open chorus, near-silent bridge",
        "texture_role": "high phrase-gap responses and compact interlude fill; at most two visible fills per eight bars",
        "separation": {"voicing": "power/dyad versus six-string open acoustic", "register": "low-mid rhythm plus high texture",
                       "rhythm": "sustains/pulses versus continuous acoustic sweeps", "stereo": "electric right, acoustic left"},
    })
    if full:
        if not (ROOT / "composition_v1.json").exists(): dump("composition_v1.json", composition)
        dump("composition.json", composition); dump("composition.normalized.json", composition)
    else:
        dump("composition_acoustic_skeleton.json", composition); dump("composition.json", composition); dump("composition.normalized.json", composition)
    configs(acoustic_only=not full)
    print(f"Built {args.stage}: {sum(bars for _, bars, _ in SECTIONS)} bars, {len(mapping)} lyric notes")


if __name__ == "__main__":
    main()
