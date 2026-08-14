"""Build the browser-ready two-song catalog from project source files."""

from __future__ import annotations

import json
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECTS = HERE.parent.parent
VOCAL_PROJECT = HERE.parent
ROCK_PROJECT = PROJECTS / "instrument_aware_full_song"
GUITAR_PROJECT = PROJECTS / "guitar_native_rock_proof"
TARGET = HERE / "songs-data.js"


def read_varlen(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    while True:
        byte = data[offset]
        offset += 1
        value = (value << 7) | (byte & 0x7F)
        if not byte & 0x80:
            return value, offset


def midi_note_ons(path: Path) -> tuple[int, list[dict]]:
    """Read note-on events from a standard PPQ MIDI using only stdlib."""
    data = path.read_bytes()
    if data[:4] != b"MThd":
        raise ValueError(f"Not a MIDI file: {path}")
    header_len = struct.unpack(">I", data[4:8])[0]
    _, track_count, division = struct.unpack(">HHH", data[8:14])
    if division & 0x8000:
        raise ValueError("SMPTE MIDI timing is not supported")
    offset = 8 + header_len
    events: list[dict] = []
    for track_index in range(track_count):
        if data[offset : offset + 4] != b"MTrk":
            raise ValueError(f"Missing MTrk at track {track_index}")
        length = struct.unpack(">I", data[offset + 4 : offset + 8])[0]
        track = data[offset + 8 : offset + 8 + length]
        offset += 8 + length
        cursor = 0
        tick = 0
        running_status: int | None = None
        while cursor < len(track):
            delta, cursor = read_varlen(track, cursor)
            tick += delta
            status = track[cursor]
            if status & 0x80:
                cursor += 1
                if status < 0xF0:
                    running_status = status
            elif running_status is not None:
                status = running_status
            else:
                raise ValueError("Running status appeared before a channel event")

            if status == 0xFF:
                cursor += 1  # meta type
                size, cursor = read_varlen(track, cursor)
                cursor += size
                continue
            if status in (0xF0, 0xF7):
                size, cursor = read_varlen(track, cursor)
                cursor += size
                continue

            kind = status & 0xF0
            channel = status & 0x0F
            first = track[cursor]
            cursor += 1
            second = None
            if kind not in (0xC0, 0xD0):
                second = track[cursor]
                cursor += 1
            if kind == 0x90 and second and second > 0:
                events.append(
                    {
                        "tick": tick,
                        "beat": tick / division,
                        "note": first,
                        "velocity": second,
                        "channel": channel,
                    }
                )
    return division, events


def vocal_song() -> dict:
    score = json.loads((VOCAL_PROJECT / "vocal-score.json").read_text(encoding="utf-8"))
    bpm = score["metadata"]["tempo"]
    seconds_per_beat = 60 / bpm
    notes = []
    phrases = []
    for phrase_index, phrase in enumerate(score["phrases"]):
        phrases.append(
            {
                "text": phrase["text"],
                "section": phrase["section"],
                "start": phrase["start_beat"] * seconds_per_beat,
                "end": phrase["end_beat"] * seconds_per_beat,
            }
        )
        for note_index, note in enumerate(phrase["notes"]):
            pitch = pitch_to_midi(note["pitch"])
            notes.append(
                {
                    "id": f"v-{phrase_index}-{note_index}",
                    "time": round(note["start_beat"] * seconds_per_beat, 6),
                    "duration": round(note["duration"] * seconds_per_beat, 6),
                    "lane": vocal_lane(pitch),
                }
            )
    sections = section_ranges(
        [("intro", 4), ("verse_1", 8), ("pre_1", 4), ("chorus_1", 8),
         ("verse_2", 8), ("pre_2", 4), ("chorus_2", 8), ("bridge", 8),
         ("final_chorus", 12), ("outro", 4)],
        bpm,
    )
    return {
        "id": "different-windows",
        "title": "Different Windows",
        "subtitle": "Vocal Pop · Melody Chart",
        "bpm": bpm,
        "key": score["metadata"]["key"],
        "duration": 153.111,
        "audio": "../output/vocal_mix.wav",
        "intro": "Two rooms. One sky. Keep the light on.",
        "accent": "#ffc967",
        "notes": notes,
        "phrases": phrases,
        "sections": sections,
    }


def rock_song() -> dict:
    composition = json.loads((ROCK_PROJECT / "composition_final.json").read_text(encoding="utf-8"))
    bpm = composition["metadata"]["tempo"]
    seconds_per_beat = 60 / bpm
    section_spec = [(section["name"], section["bars"]) for section in composition["sections"]]
    sections = section_ranges(section_spec, bpm)
    lead_division, lead_events = midi_note_ons(ROCK_PROJECT / "tracks" / "lead_guitar.mid")
    drum_division, drum_events = midi_note_ons(ROCK_PROJECT / "tracks" / "drums.mid")
    assert lead_division == drum_division

    notes: list[dict] = []
    for index, event in enumerate(lead_events):
        notes.append(
            {
                "id": f"g-{index}",
                "time": round(event["beat"] * seconds_per_beat, 6),
                "duration": 0.14,
                "lane": rock_lead_lane(event["note"]),
                "source": "lead",
            }
        )

    # Outside the guitar-free bridge, drums are accents rather than a second full
    # chart: one downbeat kick per bar plus a crash at section changes. The bridge
    # keeps its strong drum voices because the lead guitar deliberately drops out.
    allowed_drums = {35, 36, 37, 38, 40, 41, 43, 45, 47, 48, 49, 50, 51, 52, 55, 57}
    last_by_lane = [-99.0] * 4
    for index, event in enumerate(drum_events):
        if event["note"] not in allowed_drums or event["velocity"] < 65:
            continue
        event_time = event["beat"] * seconds_per_beat
        section = next(
            (item for item in sections if item["start"] <= event_time < item["end"]),
            sections[-1],
        )
        in_bridge = section["name"] == "bridge"
        beat_in_bar = event["beat"] % 4
        is_downbeat_kick = event["note"] in {35, 36} and abs(beat_in_bar) < 0.001
        is_section_crash = event["note"] >= 49 and abs(event_time - section["start"]) < 0.04
        if not in_bridge and not (is_downbeat_kick or is_section_crash):
            continue
        lane = drum_lane(event["note"])
        time = event_time
        if time - last_by_lane[lane] < 0.105:
            continue
        last_by_lane[lane] = time
        notes.append(
            {
                "id": f"d-{index}",
                "time": round(time, 6),
                "duration": 0.1,
                "lane": lane,
                "source": "drums",
            }
        )

    notes.sort(key=lambda item: (item["time"], item["lane"]))
    # Remove same-lane collisions between guitar and drum notes.
    cleaned: list[dict] = []
    for note in notes:
        if cleaned and note["lane"] == cleaned[-1]["lane"] and abs(note["time"] - cleaned[-1]["time"]) < 0.07:
            if note.get("source") == "lead":
                cleaned[-1] = note
            continue
        cleaned.append(note)

    section_copy = {
        "intro": "Hands find the rhythm before the mind names the notes.",
        "verse": "Wood, wire and pulse settle into motion.",
        "chorus": "The whole band opens up. Follow the lead guitar.",
        "bridge": "The lead steps away. Let the rhythm section carry you.",
        "final_chorus": "Every hand returns. The melody rises one last time.",
        "outro": "Leave the final chord ringing in the room.",
    }
    phrases = [
        {"text": section_copy[item["name"]], "section": item["name"], "start": item["start"], "end": item["end"]}
        for item in sections
    ]
    return {
        "id": "hands-before-notes",
        "title": composition["metadata"]["title"],
        "subtitle": "Instrumental Rock · Guitar & Drum Chart",
        "bpm": bpm,
        "key": composition["metadata"]["key"],
        "duration": 187.615,
        "audio": "../../instrument_aware_full_song/output/final.wav",
        "intro": "Hands find the rhythm before the mind names the notes.",
        "accent": "#63e6df",
        "notes": cleaned,
        "phrases": phrases,
        "sections": sections,
    }


def guitar_proof_song() -> dict:
    composition = json.loads((GUITAR_PROJECT / "composition.json").read_text(encoding="utf-8"))
    bpm = composition["metadata"]["tempo"]
    seconds_per_beat = 60 / bpm
    section_spec = [(section["name"], section["bars"]) for section in composition["sections"]]
    sections = section_ranges(section_spec, bpm)
    _, lead_events = midi_note_ons(GUITAR_PROJECT / "tracks" / "lead_guitar.mid")
    _, drum_events = midi_note_ons(GUITAR_PROJECT / "tracks" / "drums.mid")

    notes: list[dict] = [
        {
            "id": f"fire-g-{index}",
            "time": round(event["beat"] * seconds_per_beat, 6),
            "duration": 0.11,
            "lane": guitar_fire_lane(event["note"]),
            "source": "lead",
        }
        for index, event in enumerate(lead_events)
    ]

    # The lead is the complete authored guitar performance. Drums only take over
    # the guitar-free bridge and mark section entrances with crashes elsewhere.
    allowed_bridge_drums = {35, 36, 37, 38, 40, 41, 43, 45, 47, 48, 49, 50}
    last_by_lane = [-99.0] * 4
    for index, event in enumerate(drum_events):
        event_time = event["beat"] * seconds_per_beat
        section = next(
            (item for item in sections if item["start"] <= event_time < item["end"]),
            sections[-1],
        )
        in_bridge = section["name"] == "bridge"
        is_section_crash = event["note"] >= 49 and abs(event_time - section["start"]) < 0.04
        if in_bridge:
            if event["note"] not in allowed_bridge_drums or event["velocity"] < 65:
                continue
        elif not is_section_crash:
            continue
        lane = drum_lane(event["note"])
        if event_time - last_by_lane[lane] < 0.105:
            continue
        last_by_lane[lane] = event_time
        notes.append(
            {
                "id": f"fire-d-{index}",
                "time": round(event_time, 6),
                "duration": 0.09,
                "lane": lane,
                "source": "drums",
            }
        )

    notes.sort(key=lambda item: (item["time"], item["lane"], item["source"] != "lead"))
    cleaned: list[dict] = []
    last_lane_time = [-99.0] * 4
    for note in notes:
        lane = note["lane"]
        if note["time"] - last_lane_time[lane] < 0.065:
            continue
        cleaned.append(note)
        last_lane_time[lane] = note["time"]

    section_copy = {
        "intro": "A spark catches on steel strings.",
        "theme_a": "The core riff locks in and starts to burn.",
        "theme_b": "The motif climbs higher and hits harder.",
        "bridge": "The guitar vanishes. Hold the pulse before the launch.",
        "main_solo": "Thirty-two bars. One continuous guitar arc. Don't blink.",
        "final_theme": "Everything returns at full voltage.",
        "outro": "The last flame descends into E minor.",
    }
    phrases = [
        {"text": section_copy[item["name"]], "section": item["name"], "start": item["start"], "end": item["end"]}
        for item in sections
    ]
    return {
        "id": "distance-still-burns",
        "title": composition["metadata"]["title"],
        "subtitle": "Melodic Rock · Expert Lead Guitar Chart",
        "bpm": bpm,
        "key": composition["metadata"]["key"],
        "duration": 217.172,
        "audio": "../../guitar_native_rock_proof/output/mix.wav",
        "intro": "A spark catches on steel strings.",
        "accent": "#ff643d",
        "notes": cleaned,
        "phrases": phrases,
        "sections": sections,
    }


def pitch_to_midi(pitch: str) -> int:
    names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    letter = pitch[0]
    accidental = 1 if "#" in pitch else -1 if "b" in pitch else 0
    octave = int(pitch[-1])
    return (octave + 1) * 12 + names[letter] + accidental


def vocal_lane(note: int) -> int:
    return 0 if note <= 62 else 1 if note <= 66 else 2 if note <= 70 else 3


def rock_lead_lane(note: int) -> int:
    return 0 if note <= 64 else 1 if note <= 68 else 2 if note <= 72 else 3


def guitar_fire_lane(note: int) -> int:
    # Balanced around this song's actual E4-E6 guitar range.
    return 0 if note <= 67 else 1 if note <= 72 else 2 if note <= 78 else 3


def drum_lane(note: int) -> int:
    if note in {35, 36}:
        return 0
    if note in {37, 38, 40}:
        return 1
    if note in {41, 43, 45, 47, 48, 50}:
        return 2
    return 3


def section_ranges(spec: list[tuple[str, int]], bpm: float) -> list[dict]:
    seconds_per_beat = 60 / bpm
    beat_cursor = 0
    result = []
    for name, bars in spec:
        start_beat = beat_cursor
        beat_cursor += bars * 4
        result.append(
            {
                "name": name,
                "start": round(start_beat * seconds_per_beat, 6),
                "end": round(beat_cursor * seconds_per_beat, 6),
            }
        )
    return result


def main() -> None:
    songs = [vocal_song(), rock_song(), guitar_proof_song()]
    payload = json.dumps(songs, ensure_ascii=False, separators=(",", ":"))
    TARGET.write_text(
        "// Generated by build_songs.py from the music projects.\n"
        f"window.RHYTHM_GAME_SONGS={payload};\n",
        encoding="utf-8",
    )
    for song in songs:
        print(f"{song['title']}: {len(song['notes'])} notes, {song['duration']:.3f}s")
    print(f"Wrote {TARGET}")


if __name__ == "__main__":
    main()
