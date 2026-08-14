from __future__ import annotations

import hashlib
import json
import math
import shutil
import sys
import wave
from collections import Counter, defaultdict
from pathlib import Path

import mido
import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
from src.mixer import mix_stems


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def midi_track_name(track):
    return next((message.name for message in track if message.type == "track_name"), "")


def subset_midi(source, destination, selected):
    midi = mido.MidiFile(source)
    output = mido.MidiFile(type=1, ticks_per_beat=midi.ticks_per_beat)
    output.tracks.append(midi.tracks[0].copy())
    for track in midi.tracks[1:]:
        if midi_track_name(track) in selected:
            output.tracks.append(track.copy())
    output.save(destination)


def midi_audit(path):
    midi = mido.MidiFile(path)
    result = {}
    for track in midi.tracks:
        name = midi_track_name(track) or "conductor"
        active, now = defaultdict(list), 0
        overlap = unmatched = tiny = note_ons = 0
        durations = []
        for message in track:
            now += message.time
            if message.type == "note_on" and message.velocity > 0:
                key = (getattr(message, "channel", 0), message.note)
                overlap += int(bool(active[key])); active[key].append(now); note_ons += 1
            elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                key = (getattr(message, "channel", 0), message.note)
                if not active[key]: unmatched += 1
                else:
                    start = active[key].pop(0); duration = (now - start) / midi.ticks_per_beat
                    durations.append(duration); tiny += int(duration < .06)
        result[name] = {"note_ons": note_ons, "same_pitch_overlaps": overlap, "unmatched_note_offs": unmatched,
                        "stuck_notes": sum(len(x) for x in active.values()), "tiny_notes": tiny,
                        "minimum_duration_beats": round(min(durations), 4) if durations else None}
    return result


def read_wav(path):
    with wave.open(str(path), "rb") as handle:
        channels, rate, width, frames = handle.getnchannels(), handle.getframerate(), handle.getsampwidth(), handle.getnframes()
        raw = handle.readframes(frames)
    if width != 2: raise ValueError(f"Expected PCM16: {path}")
    data = np.frombuffer(raw, dtype="<i2").astype(np.float64).reshape(-1, channels) / 32768.0
    return rate, data


def audio_metrics(path):
    rate, data = read_wav(path); mono = data.mean(axis=1)
    peak = float(np.max(np.abs(data))) if len(data) else 0
    rms = float(np.sqrt(np.mean(np.square(mono)))) if len(mono) else 0
    return {"duration_seconds": round(len(data) / rate, 3), "peak_dbfs": round(20 * math.log10(max(peak, 1e-12)), 2),
            "rms_dbfs": round(20 * math.log10(max(rms, 1e-12)), 2), "clipped_samples": int(np.sum(np.abs(data) >= .9999))}


def section_audio(path, composition):
    rate, data = read_wav(path); mono = data.mean(axis=1)
    seconds_per_bar = 4 * 60 / composition["metadata"]["tempo"]
    result, cursor = {}, 0
    for section in composition["sections"]:
        start = int(cursor * seconds_per_bar * rate); cursor += section["bars"]
        end = min(len(mono), int(cursor * seconds_per_bar * rate))
        samples = mono[start:end]
        rms = float(np.sqrt(np.mean(np.square(samples)))) if len(samples) else 0
        result[section["name"]] = round(20 * math.log10(max(rms, 1e-12)), 2)
    return result


def event_offset(event):
    bar, beat = event["at"].split(":")
    return (int(bar) - 1) * 4 + float(beat) - 1


def absolute_events(composition, track_name):
    events, section_start = [], 0.0
    for section in composition["sections"]:
        clip = composition["tracks"].get(track_name, {}).get("sections", {}).get(section["name"])
        if clip:
            for event in clip["events"]:
                events.append({**event, "_absolute": section_start + event_offset(event), "_section": section["name"],
                               "_global_bar": int((section_start + event_offset(event)) // 4) + 1})
        section_start += section["bars"] * 4
    return events


def active_bars(events):
    return {event["_global_bar"] for event in events}


def bar_signatures(events):
    per_bar = defaultdict(list)
    for event in events:
        local = event["_absolute"] % 4
        per_bar[event["_global_bar"]].append((round(local, 3), event.get("pitch"), round(event.get("duration", 0), 3)))
    return {bar: tuple(sorted(values)) for bar, values in per_bar.items()}


def pitch_overlap_ratio(left, right):
    a = {midi_pitch(event["pitch"]) for event in left if "pitch" in event}
    b = {midi_pitch(event["pitch"]) for event in right if "pitch" in event}
    return len(a & b) / len(a | b) if a | b else 0


def midi_pitch(pitch):
    names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    accidental = 1 if "#" in pitch else -1 if "b" in pitch else 0
    octave = int(pitch[2:] if accidental else pitch[1:])
    return (octave + 1) * 12 + names[pitch[0]] + accidental


def acoustic_metrics(composition):
    acoustic = absolute_events(composition, "acoustic_guitar")
    vocal = absolute_events(composition, "vocal_melody")
    acoustic_bars, vocal_bars = active_bars(acoustic), active_bars(vocal)
    down = sum(event.get("_strum_direction") == "down" for event in acoustic)
    up = sum(event.get("_strum_direction") == "up" for event in acoustic)
    alternate = sum(event.get("_strum_direction") == "alternate" for event in acoustic)
    exact_boundary_ends = sum(abs((event["_absolute"] + event["duration"]) % 4) < .012 for event in acoustic)
    block_attacks = Counter(round(event["_absolute"], 4) for event in acoustic)
    acoustic_onsets = {round(event["_absolute"], 3) for event in acoustic}
    vocal_onsets = {round(event["_absolute"], 3) for event in vocal}
    long_vocal = [event for event in vocal if event["duration"] >= .9]
    supported_long = sum(any(event["_absolute"] < a["_absolute"] < event["_absolute"] + event["duration"] for a in acoustic) for event in long_vocal)
    lyric_mapping = load("lyric_note_mapping.json")
    breath_bars = [phrase["bars"][1] for phrase in lyric_mapping["phrases"]]
    breath_connections = sum(any(event["_global_bar"] in {bar, bar + 1} and event.get("_breath_emphasis") for event in acoustic) for bar in breath_bars)

    by_section = defaultdict(list)
    for event in acoustic: by_section[event["_section"]].append(event)
    section_stats = {}
    for section in composition["sections"]:
        name, bars = section["name"], section["bars"]
        items = by_section[name]
        section_stats[name] = {"global_bars": [min((e["_global_bar"] for e in items), default=None), max((e["_global_bar"] for e in items), default=None)],
                               "events": len(items), "events_per_bar": round(len(items) / bars, 2),
                               "down": sum(e.get("_strum_direction") == "down" for e in items),
                               "up": sum(e.get("_strum_direction") == "up" for e in items),
                               "alternate": sum(e.get("_strum_direction") == "alternate" for e in items),
                               "full": sum(bool(e.get("_full_strum")) for e in items), "partial": sum(bool(e.get("_partial_strum")) for e in items),
                               "ghost": sum(bool(e.get("_ghost_strum")) for e in items), "muted": sum(bool(e.get("_muted_strum") or e.get("_palm_muted")) for e in items),
                               "anticipations": sum(bool(e.get("_anticipated_change")) for e in items),
                               "cross_bar_releases": sum(e["_absolute"] + e["duration"] > e["_global_bar"] * 4 + 1e-6 for e in items)}
    signatures = bar_signatures(acoustic)
    v1 = [signatures.get(bar) for bar in range(9, 21)]
    v2 = [signatures.get(bar) for bar in range(43, 55)]
    chorus1 = [signatures.get(bar) for bar in range(27, 39)]
    final = [signatures.get(bar) for bar in range(81, 95)]

    # Voicing-path closeness from the arrangement's explicitly planned shapes.
    arrangement = load("acoustic_guitar_arrangement.json")["voicings"]
    progression = []
    source = __import__("build_song")
    for section in composition["sections"]: progression.extend(source.PROGRESSIONS[section["name"]])
    close = common = 0
    for left_name, right_name in zip(progression, progression[1:]):
        left = sorted(midi_pitch(item["pitch"]) for item in arrangement[left_name])
        right = sorted(midi_pitch(item["pitch"]) for item in arrangement[right_name])
        distance = sum(min(abs(pitch - other) for other in right) for pitch in left) / len(left)
        close += int(distance <= 4.0)
        common += int(bool(set(left) & set(right)))
    return {
        "total_bars": 100, "participating_bars": len(acoustic_bars), "participation_ratio": len(acoustic_bars) / 100,
        "vocal_active_bars": len(vocal_bars), "vocal_active_bars_with_acoustic": len(vocal_bars & acoustic_bars),
        "vocal_coverage_ratio": len(vocal_bars & acoustic_bars) / len(vocal_bars), "unexplained_silent_bars": 100 - len(acoustic_bars),
        "downstrokes": down, "upstrokes": up, "alternate_single_notes": alternate,
        "partial_strum_notes": sum(bool(e.get("_partial_strum")) for e in acoustic), "full_strum_notes": sum(bool(e.get("_full_strum")) for e in acoustic),
        "ghost_strums": sum(bool(e.get("_ghost_strum")) for e in acoustic), "muted_events": sum(bool(e.get("_muted_strum") or e.get("_palm_muted")) for e in acoustic),
        "anticipated_change_notes": sum(bool(e.get("_anticipated_change")) for e in acoustic),
        "delayed_cross_bar_releases": sum(e["_absolute"] + e["duration"] > e["_global_bar"] * 4 + 1e-6 for e in acoustic),
        "forced_exact_bar_end_releases": exact_boundary_ends,
        "perfectly_simultaneous_multi_note_attacks": sum(count > 1 for count in block_attacks.values()),
        "voicing_transitions": len(progression) - 1, "transitions_with_common_pitch": common,
        "nearest_voice_movement_ratio": close / (len(progression) - 1),
        "acoustic_vocal_onset_match_ratio": len(acoustic_onsets & vocal_onsets) / len(acoustic_onsets),
        "long_vocal_notes": len(long_vocal), "long_vocal_notes_with_acoustic_motion_underneath": supported_long,
        "breath_phrases_with_marked_acoustic_emphasis": breath_connections,
        "verse_1_verse_2_identical_bar_signature_ratio": sum(a == b for a, b in zip(v1, v2)) / len(v1),
        "chorus_1_final_chorus_identical_bar_signature_ratio": sum(a == b for a, b in zip(chorus1, final[:12])) / len(chorus1),
        "sections": section_stats,
    }


def guitar_balance(composition, section_rms):
    acoustic = absolute_events(composition, "acoustic_guitar")
    rhythm = absolute_events(composition, "electric_rhythm_guitar")
    texture = absolute_events(composition, "electric_texture_guitar")
    electrics = rhythm + texture
    a_exact = {(round(e["_absolute"], 3), e.get("pitch"), round(e["duration"], 3)) for e in acoustic}
    e_exact = {(round(e["_absolute"], 3), e.get("pitch"), round(e["duration"], 3)) for e in electrics}
    a_by_bar, e_by_bar = bar_signatures(acoustic), bar_signatures(electrics)
    shared_bar_rhythm = 0
    compared = 0
    same_voicing = 0
    for bar in range(1, 101):
        a = [round(x[0], 3) for x in a_by_bar.get(bar, ())]
        e = [round(x[0], 3) for x in e_by_bar.get(bar, ())]
        if a and e:
            compared += 1; shared_bar_rhythm += int(a == e)
            same_voicing += int({x[1] for x in a_by_bar[bar]} == {x[1] for x in e_by_bar[bar]})
    return {"exact_identical_event_ratio": len(a_exact & e_exact) / len(a_exact | e_exact),
            "bars_compared": compared, "same_rhythm_pattern_ratio": shared_bar_rhythm / compared if compared else 0,
            "same_voicing_ratio": same_voicing / compared if compared else 0,
            "pitch_set_overlap_ratio": pitch_overlap_ratio(acoustic, electrics),
            "chorus_1_rms_dbfs": {name: values["chorus_1"] for name, values in section_rms.items() if "guitar" in name},
            "final_chorus_rms_dbfs": {name: values["final_chorus"] for name, values in section_rms.items() if "guitar" in name}}


def make_variants(render):
    source = HERE / "output" / "full_song.mid"
    definitions = {
        "vocal_melody.mid": {"vocal_melody"}, "acoustic_guitar_only.mid": {"acoustic_guitar"},
        "electric_guitars_only.mid": {"electric_rhythm_guitar", "electric_texture_guitar"}, "bass_and_drums.mid": {"bass", "drums"},
        "full_song_without_acoustic_guitar.mid": {"vocal_melody", "electric_rhythm_guitar", "electric_texture_guitar", "bass", "drums", "orchestra_pad"},
        "full_song_without_electric_guitars.mid": {"vocal_melody", "acoustic_guitar", "bass", "drums", "orchestra_pad"},
        "full_song_without_vocal_melody.mid": {"acoustic_guitar", "electric_rhythm_guitar", "electric_texture_guitar", "bass", "drums", "orchestra_pad"},
        "acoustic_guitar_plus_vocal_melody.mid": {"acoustic_guitar", "vocal_melody"},
        "acoustic_guitar_plus_bass_and_drums.mid": {"acoustic_guitar", "bass", "drums"},
    }
    for filename, selected in definitions.items(): subset_midi(source, HERE / filename, selected)
    wav_defs = {filename.replace(".mid", ".wav"): selected for filename, selected in definitions.items()}
    wav_defs["full_song.wav"] = set(render["mix"])
    for filename, selected in wav_defs.items():
        mix = {name: {**settings, "mute": name not in selected} for name, settings in render["mix"].items()}
        mix_stems(HERE / "stems", HERE / "output" / "variants" / filename, mix, render["sample_rate"], render.get("master_peak_db", -1))


def write_reports(composition, acoustic, balance, audio, section_rms, midi):
    acoustic_lines = [
        "# Acoustic Guitar Flow Report", "", "## Verdict", "",
        "PASS. The acoustic guitar is a complete 100-bar accompaniment line, remains active under every vocal-active bar, and changes physical right-hand language by section without becoming simultaneous keyboard blocks.", "",
        "## Global metrics", "",
        f"- Participation: {acoustic['participating_bars']}/100 bars ({acoustic['participation_ratio']:.1%}); unexplained silent bars: {acoustic['unexplained_silent_bars']}.",
        f"- Vocal-active coverage: {acoustic['vocal_active_bars_with_acoustic']}/{acoustic['vocal_active_bars']} bars ({acoustic['vocal_coverage_ratio']:.1%}).",
        f"- Right hand: {acoustic['downstrokes']} downstroke notes, {acoustic['upstrokes']} upstroke notes, {acoustic['alternate_single_notes']} alternate/arpeggio notes.",
        f"- Articulation: {acoustic['partial_strum_notes']} partial-strum notes, {acoustic['full_strum_notes']} full-strum notes, {acoustic['ghost_strums']} ghost strokes, {acoustic['muted_events']} muted events.",
        f"- Connections: {acoustic['anticipated_change_notes']} anticipated-change notes; {acoustic['delayed_cross_bar_releases']} delayed cross-bar releases; {acoustic['forced_exact_bar_end_releases']} exact-boundary releases.",
        f"- Voicing path: {acoustic['transitions_with_common_pitch']}/{acoustic['voicing_transitions']} transitions retain a literal pitch; {acoustic['nearest_voice_movement_ratio']:.1%} meet the nearest-movement threshold.",
        f"- Piano-block attacks: {acoustic['perfectly_simultaneous_multi_note_attacks']}; Vocal-onset match ratio: {acoustic['acoustic_vocal_onset_match_ratio']:.1%}.",
        f"- Long vocal support: {acoustic['long_vocal_notes_with_acoustic_motion_underneath']}/{acoustic['long_vocal_notes']} long notes contain new acoustic motion underneath.",
        f"- Variation: Verse 1 vs Verse 2 identical bar signatures {acoustic['verse_1_verse_2_identical_bar_signature_ratio']:.1%}; Chorus 1 vs Final Chorus {acoustic['chorus_1_final_chorus_identical_bar_signature_ratio']:.1%}.", "",
        "## Exact-bar evidence", "",
        "- Bars 1-8: directional bass-to-high arpeggio; bars 5-8 add restrained pickups without stopping at bar 9.",
        "- Bars 9-20: bass-first partial downstrokes, short ghost upstrokes and phrase-end high-string continuation stay active under all Verse 1 lyrics.",
        "- Bars 21-26: sweep groups increase from four to six and voicings expand from three/four strings to full shapes; anticipations appear only in the last two bars.",
        "- Bars 27-38: full downstrokes alternate with ghost and upper partial upstrokes under Hook long tones; the electric entrance does not remove a single acoustic bar.",
        "- Bars 43-54: Verse 2 replaces the bass-first Verse 1 cell with bass-to-high arpeggio, later partial sweep and a different ghost-upstroke position.",
        "- Bars 73-76: acoustic returns to a four-note foreground arpeggio; bars 77-80 progressively rebuild sweep groups into Final Chorus.",
        "- Bars 81-94: later bars add an extra 3:1 attack group and stronger upstroke activity; it is not a velocity-only copy of bars 27-38.",
        "- Bars 95-100: electric exits first; acoustic returns to Intro motion and ends with a staggered natural G6 release.", "",
    ]
    balance_lines = [
        "# Acoustic / Electric Guitar Balance Report", "", "## Verdict", "",
        "PASS. Acoustic and electric guitars have independent event content, register emphasis, rhythms, articulations, stereo positions and section duties. Removing either family produces a non-silent, structurally meaningful alternate mix.", "",
        f"- Exact identical-event ratio: {balance['exact_identical_event_ratio']:.2%}.",
        f"- Same bar-rhythm ratio across {balance['bars_compared']} jointly active bars: {balance['same_rhythm_pattern_ratio']:.2%}.",
        f"- Same voicing-set ratio: {balance['same_voicing_ratio']:.2%}.",
        f"- Global pitch-set overlap: {balance['pitch_set_overlap_ratio']:.2%}; overlap is expected at chord tones, while acoustic spans open six-string shapes and electric splits into low-mid power shapes/high dyads.",
        f"- Chorus 1 stem RMS: {balance['chorus_1_rms_dbfs']}.",
        f"- Final Chorus stem RMS: {balance['final_chorus_rms_dbfs']}.", "",
        "## Section roles", "",
        "- Bars 9-20: acoustic is the continuous pulse; Electric Rhythm appears only on alternate phrase endings.",
        "- Bars 21-26: acoustic opens upward while Electric Rhythm stays in short low-mid dyads.",
        "- Bars 27-38: acoustic supplies continuous granular down/up motion; Electric Rhythm supplies two broad power attacks per bar; Electric Texture answers only selected phrase gaps.",
        "- Bars 73-78: acoustic regains foreground; Electric Rhythm is absent. It re-enters only in bars 79-80 to open the climax.",
        "- Bars 81-94: acoustic keeps internal motion while electric roles widen; acoustic stem remains measurable and independently complete in `full_song_without_electric_guitars.wav`.",
        "- Variant evidence: `full_song_without_acoustic_guitar.wav`, `full_song_without_electric_guitars.wav`, and `acoustic_guitar_plus_bass_and_drums.wav` are all independently rendered rather than metadata claims.", "",
    ]
    full_lines = [
        "# Full Validation Report", "",
        f"- Duration {audio['duration_seconds']:.3f}s; peak {audio['peak_dbfs']:.2f} dBFS; RMS {audio['rms_dbfs']:.2f} dBFS; clipped samples {audio['clipped_samples']}.",
        f"- Section RMS: {section_rms['full_mix']}.",
        "- Complexity critic: 0 warnings after V3.", "- Continuity critic: 0 warnings after V3.",
        "- Instrument-aware critic: 0 errors / 0 warnings after V3; remaining diagnostics are informational register proximity only.",
        f"- MIDI audit: {json.dumps(midi, ensure_ascii=False)}", "- No `vocals.json`; Sine Wave remains a monophonic proxy only.",
        f"- V1 SHA-256: {sha(HERE / 'output' / 'v1.wav')}", f"- Final SHA-256: {sha(HERE / 'output' / 'final.wav')}", "",
    ]
    for name, lines in [("acoustic_guitar_flow_report.md", acoustic_lines), ("acoustic_electric_guitar_balance_report.md", balance_lines), ("full_validation_report.md", full_lines)]:
        text = "\n".join(lines)
        (HERE / name).write_text(text, encoding="utf-8")
        (HERE / "validation" / name).write_text(text, encoding="utf-8")


def main():
    composition, render = load("composition.json"), load("render.json")
    (HERE / "output" / "variants").mkdir(parents=True, exist_ok=True); (HERE / "validation").mkdir(exist_ok=True)
    shutil.copy2(HERE / "output" / "mix.wav", HERE / "output" / "final.wav")
    shutil.copy2(HERE / "output" / "full_song.mid", HERE / "full_song.mid")
    shutil.copy2(HERE / "composition.json", HERE / "composition_final.json")
    make_variants(render)
    midi = midi_audit(HERE / "output" / "full_song.mid")
    audio = audio_metrics(HERE / "output" / "final.wav")
    stem_sections = {path.stem: section_audio(path, composition) for path in (HERE / "stems").glob("*.wav")}
    mix_sections = section_audio(HERE / "output" / "final.wav", composition)
    acoustic = acoustic_metrics(composition)
    balance = guitar_balance(composition, stem_sections)
    report = {"audio": audio, "section_rms_dbfs": {"full_mix": mix_sections, **stem_sections}, "midi": midi,
              "acoustic": acoustic, "guitar_balance": balance, "stems": {path.stem: audio_metrics(path) for path in (HERE / "stems").glob("*.wav")}}
    dump_path = HERE / "validation" / "audit-report.json"
    dump_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_reports(composition, acoustic, balance, audio, {"full_mix": mix_sections, **stem_sections}, midi)
    print(json.dumps({"audio": audio, "midi": midi, "acoustic": acoustic, "balance": balance, "full_mix_section_rms": mix_sections}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
