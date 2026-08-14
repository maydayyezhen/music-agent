from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TEMPO = 112
BEATS = 4

SECTIONS = [
    ("intro", 4, 3),
    ("verse_1", 12, 4),
    ("pre_1", 6, 6),
    ("chorus_1", 12, 8),
    ("interlude", 4, 6),
    ("verse_2", 12, 5),
    ("pre_2", 6, 7),
    ("chorus_2", 12, 8),
    ("bridge", 8, 5),
    ("final_chorus", 14, 9),
    ("outro", 6, 3),
]

LYRICS = {
    "verse_1": [
        "便利店的灯 还亮在街角", "我绕过那座 熟悉的天桥", "凌晨的巴士 沿旧路线开",
        "车窗里的人 都没有说话", "手机里那张 去年的合照", "没舍得删掉 也很少翻到",
    ],
    "pre_1": ["站牌上的时间 一格一格跳", "没说完的话 还留在口袋", "红灯转成绿色 我终于抬脚"],
    "chorus_1": [
        "下一站 还没有名字", "我先把旧车票 放回口袋", "不是忘了谁 只是该走了",
        "就算方向 暂时还空白", "等街灯一盏盏 退到背后", "我会跟着清晨 继续往前",
    ],
    "verse_2": [
        "那家唱片店 已换成花店", "旧海报还留在 玻璃门边", "我曾经以为 离开要有答案",
        "后来才懂得 决定也会失眠", "口袋里的票 被揉出折线", "可脚步比昨天 更靠前一些",
    ],
    "pre_2": ["风从十字路口 翻过我的肩", "我听见列车 正靠近站台", "这次我不等 谁替我安排"],
    "chorus_2": [
        "下一站 还是没有名字", "我把那张旧车票 握在手里", "不是告别谁 只是往前走",
        "有些路 出发才会清晰", "等熟悉的屋顶 退到背后", "我会记得这里 不再停留",
    ],
    "bridge": [
        "如果明天 仍然下着小雨", "如果出口 不在地图那里",
        "我也会在陌生街口 停一停", "再决定今天 往哪边走去",
    ],
    "final_chorus": [
        "下一站 还没有名字", "这一次我把车票 握紧", "不是忘了谁 也不是逃离",
        "只是我的脚步 该归我自己", "当整座城市 退到车窗外", "我会对过去 轻轻说声谢谢",
        "然后跟着清晨 继续往前",
    ],
    "outro": ["下一站 还没有名字"],
}

PROGRESSIONS = {
    "intro": ["Bm7", "Gmaj7", "Dadd9", "A"],
    "verse_1": ["Bm7", "Gmaj7", "Dadd9", "A", "Bm7", "Gmaj7", "Em7", "A", "Bm7", "Gmaj7", "Dadd9", "A"],
    "pre_1": ["Em7", "Gmaj7", "D/F#", "A", "Em7", "A"],
    "chorus_1": ["Gmaj7", "Dadd9", "A", "Bm7", "Gmaj7", "D/F#", "Em7", "A", "Gmaj7", "Dadd9", "A", "Bm7"],
    "interlude": ["Gmaj7", "Dadd9", "A", "Bm7"],
    "verse_2": ["Bm7", "Gmaj7", "Dadd9", "A", "Bm7", "Gmaj7", "Em7", "A", "Gmaj7", "D/F#", "Em7", "A"],
    "pre_2": ["Em7", "Gmaj7", "D/F#", "A", "Gmaj7", "A"],
    "chorus_2": ["Gmaj7", "Dadd9", "A", "Bm7", "Gmaj7", "D/F#", "Em7", "A", "Gmaj7", "Dadd9", "A", "Bm7"],
    "bridge": ["Bm7", "A", "Gmaj7", "D/F#", "Em7", "Bm7", "Gmaj7", "A"],
    "final_chorus": ["Gmaj7", "Dadd9", "A", "Bm7", "Gmaj7", "D/F#", "Em7", "A", "Gmaj7", "Dadd9", "A", "Bm7", "Gmaj7", "A"],
    "outro": ["Bm7", "Gmaj7", "Dadd9", "A", "Bm7", "Bm7"],
}

# MIDI pitch names plus guitar-authored string/fret paths. Strings are 0=low E ... 5=high E.
VOICINGS = {
    "Bm7": [("B2", 1, 2), ("F#3", 2, 4), ("A3", 3, 2), ("D4", 4, 3)],
    "Gmaj7": [("G2", 0, 3), ("D3", 1, 5), ("F#3", 2, 4), ("B3", 3, 4)],
    "Dadd9": [("D3", 1, 5), ("A3", 3, 2), ("D4", 4, 3), ("E4", 5, 0)],
    "D/F#": [("F#2", 0, 2), ("A2", 1, 0), ("D3", 2, 0), ("A3", 3, 2)],
    "A": [("A2", 0, 5), ("E3", 1, 7), ("A3", 3, 2), ("C#4", 4, 2)],
    "Em7": [("E2", 0, 0), ("B2", 1, 2), ("D3", 2, 0), ("G3", 3, 0)],
}

HIGH = {
    "Bm7": [("D4", 4, 3), ("F#4", 5, 2), ("A4", 5, 5)],
    "Gmaj7": [("B3", 3, 4), ("D4", 4, 3), ("F#4", 5, 2)],
    "Dadd9": [("A3", 3, 2), ("D4", 4, 3), ("E4", 5, 0)],
    "D/F#": [("A3", 3, 2), ("D4", 4, 3), ("F#4", 5, 2)],
    "A": [("A3", 3, 2), ("C#4", 4, 2), ("E4", 5, 0)],
    "Em7": [("G3", 3, 0), ("D4", 4, 3), ("E4", 5, 0)],
}

ROOTS = {"Bm7": "B2", "Gmaj7": "G2", "Dadd9": "D3", "D/F#": "F#2", "A": "A2", "Em7": "E2"}
FIFTHS = {"Bm7": "F#3", "Gmaj7": "D3", "Dadd9": "A2", "D/F#": "A2", "A": "E3", "Em7": "B2"}

SECTION_START = {}
cursor = 1
for name, bars, _ in SECTIONS:
    SECTION_START[name] = cursor
    cursor += bars


def dump(name: str, value) -> None:
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def at(offset: float) -> str:
    bar = int(offset // 4) + 1
    beat = offset - (bar - 1) * 4 + 1
    return f"{bar}:{beat:g}"


def note(pitch, offset, duration, velocity, **extra):
    result = {"type": "note", "pitch": pitch, "at": at(offset), "duration": round(duration, 3), "velocity": int(velocity)}
    result.update(extra)
    return result


def drum(number, offset, duration, velocity, **extra):
    result = {"type": "drum", "note": number, "at": at(offset), "duration": duration, "velocity": int(velocity)}
    result.update(extra)
    return result


PITCH_POOLS = {
    "verse": ["D4", "E4", "F#4", "A4", "F#4", "E4", "D4", "B3", "D4", "E4", "F#4", "E4", "D4"],
    "pre": ["E4", "F#4", "A4", "B4", "A4", "B4", "C#5", "B4", "A4", "F#4", "A4", "B4", "C#5"],
    "chorus": ["A4", "A4", "B4", "D5", "C#5", "B4", "A4", "F#4", "A4", "B4", "C#5", "D5", "E5", "D5"],
    "bridge": ["F#4", "E4", "D4", "B3", "D4", "E4", "F#4", "A4", "F#4", "E4", "D4", "E4", "F#4"],
    "outro": ["A4", "B4", "D5", "C#5", "B4", "A4", "F#4", "E4", "D4"],
}


def clean_chars(line: str) -> list[str]:
    return [char for char in line if char not in " ，。！？、"]


def melody_for_section(section: str, bars: int):
    lines = LYRICS.get(section, [])
    events, mappings, phrases = [], [], []
    if not lines:
        return events, mappings, phrases
    family = "verse" if section.startswith("verse") else "pre" if section.startswith("pre") else "chorus" if "chorus" in section else section
    base = PITCH_POOLS[family]
    for line_index, line in enumerate(lines):
        chars = clean_chars(line)
        phrase_start = line_index * 8.0
        # Leave a real breath at the end, but allow notes around beat 4 to cross the internal barline.
        usable = 6.8 if len(chars) > 9 else 6.5
        step = usable / max(1, len(chars) - 1)
        raw = [round((0.35 + index * step) * 4) / 4 for index in range(len(chars))]
        for index in range(1, len(raw)):
            if raw[index] <= raw[index - 1]:
                raw[index] = raw[index - 1] + 0.5
        if raw[-1] > 7.25:
            shift = raw[-1] - 7.25
            raw = [max(0.25, value - shift * (idx / max(1, len(raw) - 1))) for idx, value in enumerate(raw)]
        phrase_entries = []
        for index, (char, local_onset) in enumerate(zip(chars, raw)):
            next_onset = raw[index + 1] if index + 1 < len(raw) else 7.65
            duration = min(1.25 if index == len(chars) - 1 else 0.9, max(0.32, (next_onset - local_onset) * 0.82))
            # Deliberately connect across the internal barline on selected syntactic pivots.
            cross_bar = False
            if 3.65 <= local_onset < 4.0 and next_onset >= 4.35:
                duration = max(duration, 4.12 - local_onset)
                cross_bar = True
            pitch_index = (index + line_index * 2) % len(base)
            pitch = base[pitch_index]
            if section == "final_chorus" and line_index >= 3 and index in {3, 7, 10}:
                pitch = "E5"
            stress = index in {0, len(chars) - 1} or char in "下站名票走路脚步清晨自己"
            velocity = (91 if family == "chorus" else 78 if family == "verse" else 84) + (7 if stress else 0) + ((index + line_index) % 3 - 1) * 2
            global_local = phrase_start + local_onset
            ev = note(pitch, global_local, duration, velocity, _lyric=char, _phrase=line_index + 1, _stress=stress, _cross_bar=cross_bar)
            events.append(ev)
            absolute_bar = SECTION_START[section] + int(global_local // 4)
            beat = global_local % 4 + 1
            mapping = {
                "section": section, "line": line_index + 1, "character_index": index + 1, "character": char,
                "bar": absolute_bar, "beat": round(beat, 3), "duration_beats": round(duration, 3), "pitch": pitch,
                "stress": stress, "crosses_barline": cross_bar,
            }
            mappings.append(mapping)
            phrase_entries.append(mapping)
        phrases.append({
            "section": section, "line": line_index + 1, "text": line,
            "bars": [SECTION_START[section] + line_index * 2, SECTION_START[section] + line_index * 2 + 1],
            "breath_after_beats": round(8 - (raw[-1] + events[-1]["duration"]), 3), "notes": phrase_entries,
        })
    return events, mappings, phrases


def guitar_one(section: str, bars: int):
    events = []
    progression = PROGRESSIONS[section]
    for bar_index, chord in enumerate(progression):
        base = bar_index * 4.0
        voicing = VOICINGS[chord]
        if section.startswith("verse"):
            pattern = [(0, 0), (.5, 1), (1, 0), (1.5, 2), (2, 0), (2.5, 1), (3, 0), (3.5, 2)]
            if section == "verse_2" and bar_index % 3 == 2:
                pattern[-2:] = [(3, 2), (3.5, 3)]
            for idx, (off, tone) in enumerate(pattern):
                p, string, fret = voicing[tone]
                events.append(note(p, base + off, .34 if idx % 2 else .39, 62 + (idx % 4) * 2,
                                   _string=string, _fret=fret, _attack_group=f"{section}-{bar_index+1}-{idx+1}",
                                   _strum_direction="down" if idx % 2 == 0 else "up", _palm_muted=True,
                                   _right_hand="continuous_eighths"))
        elif section.startswith("pre"):
            offsets = [0, .5, 1, 1.5, 2, 2.5, 3, 3.5]
            for idx, off in enumerate(offsets):
                tone = [0, 1, 2, 1, 0, 2, 3, 2][idx]
                p, string, fret = voicing[tone]
                events.append(note(p, base + off, .42 if idx < 5 else .52, 67 + idx,
                                   _string=string, _fret=fret, _attack_group=f"{section}-{bar_index+1}-{idx+1}",
                                   _strum_direction="down" if idx % 2 == 0 else "up", _palm_muted=idx < 3,
                                   _right_hand="opening_eighths"))
        elif section == "bridge":
            # Spacious swells; Guitar 2 carries the inner voice while this part preserves harmonic gravity.
            for idx, (p, string, fret) in enumerate(voicing[:3]):
                events.append(note(p, base + idx * .055, 2.7 - idx * .05, 58 + idx * 2,
                                   _string=string, _fret=fret, _attack_group=f"bridge-{bar_index+1}-swell",
                                   _strum_direction="down", _palm_muted=False, _right_hand="slow_brush"))
            if bar_index >= 4:
                p, string, fret = voicing[2]
                events.append(note(p, base + 3.5, .38, 68, _string=string, _fret=fret,
                                   _attack_group=f"bridge-{bar_index+1}-pickup", _strum_direction="up",
                                   _palm_muted=False, _right_hand="anticipation"))
        elif section == "outro":
            for idx, (p, string, fret) in enumerate(voicing):
                events.append(note(p, base + idx * .045, 2.5 if bar_index < 4 else 3.5, 56 + idx,
                                   _string=string, _fret=fret, _attack_group=f"outro-{bar_index+1}-brush",
                                   _strum_direction="down", _palm_muted=False, _right_hand="decaying_brush"))
        else:
            # Open pop-rock: staggered chord attacks plus upbeat continuation; never a simultaneous block.
            attacks = [(0, "down", 0), (1.5, "up", 1), (2, "down", 0), (3.5, "up", 2)]
            if section == "final_chorus" and bar_index >= 8:
                attacks.insert(3, (3, "down", 3))
            for group_index, (off, direction, start_tone) in enumerate(attacks):
                order = list(range(start_tone, 4)) if direction == "down" else list(reversed(range(start_tone, 4)))
                order = order[:3] if group_index else order
                for strum_index, tone in enumerate(order):
                    p, string, fret = voicing[tone]
                    events.append(note(p, base + off + strum_index * .045, .72 if group_index else 1.0,
                                       72 + group_index * 2 + strum_index,
                                       _string=string, _fret=fret, _attack_group=f"{section}-{bar_index+1}-{group_index+1}",
                                       _strum_direction=direction, _palm_muted=False, _right_hand="continuous_pop_strum"))
    return events


def guitar_two(section: str, bars: int):
    events = []
    for bar_index, chord in enumerate(PROGRESSIONS[section]):
        base = bar_index * 4.0
        voicing = HIGH[chord]
        if section in {"intro", "interlude"}:
            offsets = [0, .75, 1.5, 2.25, 3, 3.5]
            durations = [.72, .82, .68, .90, .62, .46]
            tones = [0, 1, 2, 1, 0, 1]
            for idx, (off, tone) in enumerate(zip(offsets, tones)):
                p, string, fret = voicing[tone]
                events.append(note(p, base + off, durations[idx], 62 + idx,
                                   _string=string, _fret=fret, _attack_group=f"{section}-{bar_index+1}-arp-{idx+1}",
                                   _strum_direction="alternate", _right_hand="clean_arpeggio",
                                   _voice_leading="shared_tone_path"))
        elif section == "verse_1":
            if bar_index % 2 == 1:
                for idx, tone in enumerate([0, 1, 2]):
                    p, string, fret = voicing[tone]
                    events.append(note(p, base + 2.5 + idx * .07, .75, 53 + idx * 2,
                                       _string=string, _fret=fret, _attack_group=f"v1-{bar_index+1}-answer",
                                       _strum_direction="up", _right_hand="restrained_answer"))
        elif section == "verse_2":
            offsets = [1.5, 2.5, 3.5] if bar_index % 2 == 0 else [.5, 2, 3]
            for idx, off in enumerate(offsets):
                p, string, fret = voicing[(idx + bar_index) % 3]
                events.append(note(p, base + off, [.52, .78, .88][idx], 58 + idx * 3,
                                   _string=string, _fret=fret, _attack_group=f"v2-{bar_index+1}-{idx+1}",
                                   _strum_direction="up" if idx % 2 else "down", _right_hand="upper_syncopation"))
        elif section.startswith("pre"):
            for idx, off in enumerate([1, 2.5, 3.5]):
                p, string, fret = voicing[idx]
                events.append(note(p, base + off, .7 if idx < 2 else .4, 61 + bar_index + idx,
                                   _string=string, _fret=fret, _attack_group=f"{section}-{bar_index+1}-{idx+1}",
                                   _strum_direction="up", _right_hand="ascending_partial"))
        elif section == "bridge":
            # Independent moving upper voice: descending shared-tone line, then rising anticipation.
            sequence = [2, 1, 0, 1] if bar_index < 4 else [0, 1, 2, 1, 2]
            offsets = [0.75, 1.75, 2.75, 3.5] if bar_index < 4 else [0.5, 1.25, 2, 2.75, 3.5]
            for idx, (tone, off) in enumerate(zip(sequence, offsets)):
                p, string, fret = voicing[tone]
                events.append(note(p, base + off, .62 if idx < len(offsets) - 1 else .38, 62 + idx * 2 + bar_index,
                                   _string=string, _fret=fret, _attack_group=f"bridge2-{bar_index+1}-{idx+1}",
                                   _strum_direction="alternate", _right_hand="independent_counterline",
                                   _voice_leading="stepwise_or_shared_tone"))
        elif section == "outro":
            for idx, tone in enumerate([2, 1, 0]):
                p, string, fret = voicing[tone]
                events.append(note(p, base + idx * 1.0, .85, 50 + idx,
                                   _string=string, _fret=fret, _attack_group=f"outro2-{bar_index+1}-{idx+1}",
                                   _strum_direction="alternate", _right_hand="decaying_arpeggio"))
        else:
            offsets = [.5, 1.5, 2.5, 3.5]
            if section == "final_chorus" and bar_index >= 8:
                offsets = [.5, 1.25, 2, 2.75, 3.5]
            for idx, off in enumerate(offsets):
                p, string, fret = voicing[(idx + (bar_index % 2)) % 3]
                duration_cycle = [.56, .78, .62, .86, .48]
                events.append(note(p, base + off, duration_cycle[idx], 64 + idx * 3 + (3 if section == "final_chorus" else 0),
                                   _string=string, _fret=fret, _attack_group=f"{section}2-{bar_index+1}-{idx+1}",
                                   _strum_direction="up" if idx % 2 == 0 else "down", _right_hand="offbeat_partial",
                                   _voice_leading="upper_common_tone"))
    return events


def bass_events(section: str, bars: int):
    result = []
    progression = PROGRESSIONS[section]
    for bar_index, chord in enumerate(progression):
        base = bar_index * 4
        root, fifth = ROOTS[chord], FIFTHS[chord]
        if section == "bridge" and bar_index < 4:
            pattern = [(0, root, 1.8), (2, fifth, 1.45)]
        elif section.startswith("verse"):
            pattern = [(0, root, .85), (1, root, .7), (2, fifth, .75), (3, root, .7)]
        else:
            pattern = [(0, root, .75), (1, fifth, .65), (2, root, .7), (3, fifth, .42), (3.5, root, .38)]
        for idx, (off, pitch, duration) in enumerate(pattern):
            result.append(note(pitch, base + off, duration, 70 + min(12, idx * 2 + (5 if "chorus" in section else 0)),
                               _role="root_motion" if idx == 0 else "pulse_or_approach"))
    return result


def drum_events(section: str, bars: int):
    result = []
    energy = next(value for name, _, value in SECTIONS if name == section)
    for bar in range(bars):
        base = bar * 4
        if section == "intro" and bar < 2:
            for off in [0, 1, 2, 3]: result.append(drum(42, base + off, .12, 38 + bar * 4, _limb="right_hand"))
            if bar == 1: result.append(drum(36, base + 2, .12, 52, _limb="right_foot"))
            continue
        if bar == 0 or ("chorus" in section and bar % 4 == 0):
            result.append(drum(49, base, .22, 76 + energy * 3, _limb="right_hand", _role="section_marker"))
        hat_step = 1.0 if section == "bridge" and bar < 4 else .5
        for step in range(int(4 / hat_step)):
            off = step * hat_step
            result.append(drum(42 if not ("chorus" in section and step == int(4 / hat_step) - 1) else 46,
                               base + off, .1, 48 + (step % 2) * 7 + energy + (bar % 3), _limb="right_hand", _role="pulse"))
        if section.startswith("verse"):
            kick_variants = [[0, 2.5], [0, 2], [0, .75, 2.5], [0, 2, 3.25]]
        else:
            kick_variants = [[0, 1.5, 2.5], [0, 1.75, 2.5], [0, .75, 2.5], [0, 1.5, 2.5, 3.25]]
        kicks = kick_variants[bar % 4]
        if "chorus" in section or section.startswith("pre"): kicks.append(3.5)
        for off in kicks: result.append(drum(36, base + off, .12, 73 + energy * 2, _limb="right_foot"))
        for off in [1, 3]: result.append(drum(38, base + off, .12, 76 + energy * 2, _limb="left_hand"))
        if bar == bars - 1 and section not in {"verse_1", "verse_2"}:
            for idx, off in enumerate([3, 3.25, 3.5, 3.75]):
                result.append(drum([45, 47, 48, 50][idx], base + off, .1, 68 + idx * 5, _limb="left_hand" if idx % 2 == 0 else "right_hand", _role="fill"))
    return result


def piano_events(section: str, bars: int):
    if section not in {"intro", "bridge", "final_chorus", "outro"}:
        return []
    result = []
    for bar_index, chord in enumerate(PROGRESSIONS[section]):
        if section == "final_chorus" and bar_index < 8:
            continue
        tones = HIGH[chord]
        base = bar_index * 4
        for idx, (pitch, _, _) in enumerate(tones):
            result.append(note(pitch, base + idx * .025, 2.9 if section != "outro" else 3.5, 43 + idx * 2,
                               _role="background_glue", _attack="soft_rolled"))
    return result


def clip(events, bars):
    return {"loop_bars": bars, "events": events}


def remove_same_pitch_overlaps(track, section_defs):
    """Keep independent-string continuity, but release a pitch before it is re-attacked."""
    section_offset = 0.0
    by_pitch = {}
    for section_name, bars, _ in section_defs:
        section = track.get("sections", {}).get(section_name)
        if section:
            for event in section["events"]:
                start = section_offset + event_offset_local(event)
                by_pitch.setdefault(event["pitch"], []).append((start, event))
        section_offset += bars * 4
    shortened = 0
    for entries in by_pitch.values():
        entries.sort(key=lambda item: item[0])
        for (start, event), (next_start, _) in zip(entries, entries[1:]):
            if start + float(event["duration"]) > next_start:
                event["duration"] = round(max(0.08, next_start - start - 0.035), 3)
                event["_controlled_release_before_reattack"] = True
                shortened += 1
    return shortened


def event_offset_local(event):
    bar_text, beat_text = event["at"].split(":", 1)
    return (int(bar_text) - 1) * 4 + float(beat_text) - 1


def build_composition():
    mapping, phrases = [], []
    tracks = {
        "vocal_melody": {"role": "strictly monophonic sung-melody proxy", "sections": {}},
        "rhythm_guitar_1": {"role": "continuous right-hand and harmonic engine", "sections": {}},
        "rhythm_guitar_2": {"role": "upper partials, arpeggios and restrained counter-motion", "sections": {}},
        "bass": {"role": "independent root/fifth motion and approaches", "sections": {}},
        "drums": {"role": "pop-rock time, fills and section lift", "sections": {}},
        "electric_piano": {"role": "sparse background glue only", "sections": {}},
    }
    for section, bars, _ in SECTIONS:
        melody, section_mapping, section_phrases = melody_for_section(section, bars)
        mapping.extend(section_mapping); phrases.extend(section_phrases)
        if melody: tracks["vocal_melody"]["sections"][section] = clip(melody, bars)
        g1 = guitar_one(section, bars)
        g2 = guitar_two(section, bars)
        if g1: tracks["rhythm_guitar_1"]["sections"][section] = clip(g1, bars)
        if g2: tracks["rhythm_guitar_2"]["sections"][section] = clip(g2, bars)
        tracks["bass"]["sections"][section] = clip(bass_events(section, bars), bars)
        tracks["drums"]["sections"][section] = clip(drum_events(section, bars), bars)
        piano = piano_events(section, bars)
        if piano: tracks["electric_piano"]["sections"][section] = clip(piano, bars)
    controlled_releases = remove_same_pitch_overlaps(tracks["rhythm_guitar_1"], SECTIONS)
    composition = {
        "metadata": {"title": "下一站还没有名字", "english_title": "Next Stop Has No Name", "tempo": TEMPO,
                     "time_signature": "4/4", "key": "D major / B minor", "language": "zh-CN", "seed": 112096,
                     "duration_target": "3:00-3:30", "vocal_rendering": "disabled; Clean Synth Lead proxy only",
                     "controlled_guitar_releases": controlled_releases},
        "complexity": {"level": "rich", "rhythm": 4, "harmony": 3, "arrangement": 4, "melodic_ornamentation": 2, "density": 3, "variation": 4},
        "complexity_contour": "verse_chorus",
        "sections": [{"name": name, "bars": bars, "energy": energy, "complexity": {"level": "rich" if energy >= 8 else "standard"}}
                     for name, bars, energy in SECTIONS],
        "tracks": tracks,
    }
    return composition, mapping, phrases


def write_docs(composition, mapping, phrases):
    total_bars = sum(item[1] for item in SECTIONS)
    seconds = total_bars * 4 * 60 / TEMPO + 2
    plan = f"""# 《下一站还没有名字》Composition Plan

- Style: Japanese melodic / alternative pop-rock, youthful game/anime ending tone
- Tempo / meter / key: 112 BPM, 4/4, D major with B minor center
- Length: {total_bars} bars; score {seconds-2:.2f}s, render target {seconds:.2f}s
- Foreground: monophonic Sine Wave Clean Synth Lead as an explicitly temporary vocal-melody proxy
- Story: a person leaves a familiar city without pretending to know the destination; the old ticket changes from an avoided memory into something they can hold while moving.

## Form and dramatic arc

| Global bars | Section | Bars | Function |
|---|---:|---:|---|
"""
    for name, bars, energy in SECTIONS:
        start = SECTION_START[name]; end = start + bars - 1
        function = {
            "intro": "Guitar 2 introduces shared-tone arpeggio; G1 enters as harmonic gravity",
            "verse_1": "Palm-muted G1; sparse G2 replies; close, observational vocal proxy",
            "pre_1": "Both guitars open progressively; upper partials rise",
            "chorus_1": "Open staggered strums and offbeat partials; first hook statement",
            "interlude": "Guitar-led instrumental breath; no vocal proxy",
            "verse_2": "Same identity, busier upper syncopation and altered harmony",
            "pre_2": "Stronger anticipations and drum lift",
            "chorus_2": "Lyric and accompaniment variation, not copy-paste",
            "bridge": "Vocal lowers; G1 swells while G2 becomes an independent counterline",
            "final_chorus": "Expanded 14-bar climax, denser G2 and melody peak E5",
            "outro": "Hook recall then instrumental decay",
        }[name]
        plan += f"| {start}-{end} | {name} | {bars} | {function} |\n"
    plan += """

## Electric-guitar writing contract

Guitar 1 is authored from playable four-string paths and continuous right-hand patterns. Verse attacks alternate down/up with palm muting; pre-choruses progressively release the mute; choruses use staggered down/up partial strums rather than simultaneous chord blocks. Guitar 2 occupies a higher register and moves through shared tones, arpeggios, and offbeat partials. It is deliberately sparse in Verse 1, more active in Verse 2, independently melodic in the bridge, and densest only in the latter half of the final chorus. Neither guitar is a soloist and neither duplicates the Clean Synth Lead.
"""
    (ROOT / "composition_plan.md").write_text(plan, encoding="utf-8")

    lyric_doc = "# 《下一站还没有名字》歌词\n\n> 中文原创歌词；空格表示自然语义分组，不代表额外音节。\n\n"
    for section, _, _ in SECTIONS:
        if section not in LYRICS: continue
        lyric_doc += f"## {section}\n\n" + "\n".join(LYRICS[section]) + "\n\n"
    lyric_doc += "## Vocal melody proxy\n\n实际人声未启用。`vocal_melody` 轨使用 GeneralUser GS bank 8 / program 80 `Sine Wave`，严格单声部，仅用于检查歌词重音、音域、呼吸与副歌记忆点。\n"
    (ROOT / "lyrics.md").write_text(lyric_doc, encoding="utf-8")

    dump("lyric_note_mapping.json", {"title": composition["metadata"]["title"], "tempo": TEMPO, "mapping": mapping, "phrases": phrases})
    dump("vocal_melody.json", {"rendering": "Clean Synth Lead proxy; no actual vocals", "monophonic": True,
                               "instrument": {"bank": 8, "program": 80, "name": "Sine Wave"},
                               "range": ["B3", "E5"], "phrases": phrases})
    guitar_plan = {
        "principle": "hands/voicings/right-hand motion before notes; accompaniment, never solo",
        "guitar_1": {"role": "continuous harmonic engine", "verse": "continuous palm-muted eighths", "pre": "gradually opening eighths",
                     "chorus": "staggered open down/up partial strums", "bridge": "slow three-string brushes plus late pickups",
                     "final": "same identity with added late-bar attack groups"},
        "guitar_2": {"role": "upper-register voice-leading", "intro": "six-note shared-tone arpeggio per bar",
                     "verse_1": "one restrained answer every two bars", "verse_2": "three syncopated upper tones per bar",
                     "chorus": "offbeat partial movement", "bridge": "independent descending/rising counterline",
                     "final": "five offbeat notes per bar after bar 8"},
        "voicings": {name: [{"pitch": p, "string": s, "fret": f} for p, s, f in values] for name, values in VOICINGS.items()},
        "prohibited": ["guitar solo", "lead-melody doubling", "simultaneous piano-block chords", "random velocity-only humanization"],
    }
    dump("guitar_arrangement.json", guitar_plan)


def main():
    composition, mapping, phrases = build_composition()
    write_docs(composition, mapping, phrases)
    if not (ROOT / "composition_v1.json").exists():
        dump("composition_v1.json", composition)
    dump("composition.json", composition)
    # Current loader normalization is intentionally non-mutating, so the source is already canonical.
    dump("composition.normalized.json", composition)
    dump("instruments.json", {
        "vocal_melody": {"engine": "fluidsynth", "bank": 8, "program": 80, "gm_name": "Sine Wave"},
        "rhythm_guitar_1": {"engine": "fluidsynth", "bank": 0, "program": 28, "gm_name": "Muted Guitar"},
        "rhythm_guitar_2": {"engine": "fluidsynth", "bank": 0, "program": 27, "gm_name": "Clean Guitar"},
        "bass": {"engine": "fluidsynth", "bank": 0, "program": 34, "gm_name": "Electric Bass (pick)"},
        "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16, "gm_name": "Power Drum Kit"},
        "electric_piano": {"engine": "fluidsynth", "bank": 0, "program": 4, "gm_name": "Electric Piano 1"},
    })
    dump("render.json", {
        "sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.82,
        "tail_seconds": 2.0, "master_peak_db": -1.0,
        "mix": {
            "vocal_melody": {"volume_db": 5.0, "pan": 0.0, "mute": False},
            "rhythm_guitar_1": {"volume_db": 2.8, "pan": -0.38, "mute": False},
            "rhythm_guitar_2": {"volume_db": 2.0, "pan": 0.36, "mute": False},
            "bass": {"volume_db": 3.8, "pan": 0.0, "mute": False},
            "drums": {"volume_db": 4.0, "pan": 0.0, "mute": False},
            "electric_piano": {"volume_db": -2.5, "pan": 0.12, "mute": False},
        },
    })
    print(f"Built {composition['metadata']['title']}: {sum(s[1] for s in SECTIONS)} bars, {len(mapping)} lyric notes")


if __name__ == "__main__":
    main()
