from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from statistics import mean

import mido

from _bootstrap import ROOT
from src.instruments import compile_instrument_phrase
from src.midi import generate_song_midis
from src.midi.generator import derive_foreground_activity


PROJECT = ROOT / "projects" / "sixteenth_strumming_demo"
SECTIONS = [("baseline", 4), ("sixteenth_grid", 4), ("per_string_sustain", 4), ("foreground_thinning", 4)]
CHORDS = ["Am", "F", "C", "G"]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def harmony():
    return [{"at": f"{bar}:1", "duration": 4, "chord": chord} for bar, chord in enumerate(CHORDS, 1)]


def guitar_phrase(section: str, *, before: bool, foreground_aware: bool):
    if before or section == "baseline":
        return {
            "instrument": "acoustic_guitar", "role": f"{section} fixed eighth baseline",
            "phrase_type": "continuous_strumming", "energy": .62,
            "subdivision": "eighth", "strumming_pattern": "steady_eighths",
            "harmony": harmony(), "performance_intent": {"seed": 1600 + len(section)},
        }
    return {
        "instrument": "acoustic_guitar", "role": f"{section} sixteenth continuous strumming",
        "phrase_type": "continuous_strumming", "energy": .62,
        "subdivision": "sixteenth", "strumming_pattern": "sixteenth_flow",
        "four_bar_variation": True,
        "per_string_sustain": section != "sixteenth_grid",
        "foreground_aware": foreground_aware and section == "foreground_thinning",
        "harmony": harmony(), "strum_spread": .024,
        "performance_intent": {"seed": 1616 + len(section)},
    }


def foreground_events():
    return [
        {"at": "1:1", "duration": 1.5, "pitch": "A4", "velocity": 82},
        {"at": "1:3", "duration": .75, "pitch": "C5", "velocity": 78},
        {"at": "2:1", "duration": 3.0, "pitch": "G4", "velocity": 84},
        {"at": "3:1.5", "duration": .5, "pitch": "E4", "velocity": 76},
        {"at": "3:2.5", "duration": .5, "pitch": "G4", "velocity": 79},
        {"at": "4:1", "duration": 2.0, "pitch": "A4", "velocity": 83},
    ]


def composition(*, before: bool, with_foreground: bool):
    guitar_sections = {
        name: {"loop_bars": bars, "sound_library_profile": "general_midi",
               "instrument_phrase": guitar_phrase(name, before=before, foreground_aware=with_foreground)}
        for name, bars in SECTIONS
    }
    tracks = {"acoustic_guitar": {"role": "acoustic guitar continuous strumming test", "sections": guitar_sections}}
    if with_foreground:
        tracks["foreground_melody"] = {"role": "main melody foreground activity probe", "sections": {
            "foreground_thinning": {"loop_bars": 4, "events": foreground_events()}
        }}
    return {
        "metadata": {"title": "Sixteenth Strumming State Test", "tempo": 108,
                     "time_signature": "4/4", "key": "A minor", "seed": 1616416},
        "complexity": {"level": "standard", "rhythm": 4, "harmony": 2,
                       "arrangement": 2, "melodic_ornamentation": 1, "density": 3, "variation": 4},
        "complexity_contour": "gradual_build",
        "sections": [{"name": name, "bars": bars, "energy": 3 + index * 2}
                     for index, (name, bars) in enumerate(SECTIONS)],
        "tracks": tracks,
    }


def prepare_phrase(data: dict, section: str):
    phrase = deepcopy(data["tracks"]["acoustic_guitar"]["sections"][section]["instrument_phrase"])
    if phrase.get("foreground_aware"):
        phrase["foreground_activity"] = derive_foreground_activity(data, "acoustic_guitar", section, 4)
    events = compile_instrument_phrase(phrase, 4)
    return phrase, events


def position(value: str) -> float:
    bar, beat = value.split(":")
    return (int(bar) - 1) * 4 + float(beat) - 1


def phrase_metrics(phrase: dict, events: list[dict]):
    groups = defaultdict(list)
    for event in events:
        groups[event["_attack_group"]].append(event)
    per_bar = []
    for bar in range(1, 5):
        per_bar.append(sum(int(group.split("-")[-2]) == bar for group in groups))
    sizes = Counter(len(group) for group in groups.values())
    total = max(1, sum(sizes.values()))
    categories = {
        "single": sizes[1] / total,
        "double": sizes[2] / total,
        "triple": sizes[3] / total,
        "four_or_more": sum(count for size, count in sizes.items() if size >= 4) / total,
    }
    grid = phrase["_strumming_debug"]["bars"]
    state = phrase.get("_per_string_state_debug", {}).get("steps", [])
    sounding_steps = [item for item in state if item["action"] != "air_strum"]
    sustain_ratio = (sum(item["previous_attack_still_sounding"] for item in sounding_steps) /
                     len(sounding_steps)) if sounding_steps else 0.0
    boundaries = [item for item in state if item["step"] == 0 and item["bar"] > 1]
    cross_bar_ratio = (sum(item["cross_bar_sustain"] for item in boundaries) / len(boundaries)) if boundaries else 0.0
    downbeat_ratio = sum(item["actions"][0] != "air_strum" for item in grid) / len(grid)
    variant_count = len({item.get("variant_id", item["pattern_id"]) for item in grid})
    attack_positions = []
    for bar in grid:
        unit = .25 if bar["subdivision"] == "sixteenth" else .5
        attack_positions.extend((bar["bar"] - 1) * 4 + step * unit
                                for step, action in enumerate(bar["actions"]) if action != "air_strum")
    long_gaps = sum(right - left > .75 for left, right in zip(attack_positions, attack_positions[1:]))
    return {
        "potential_hand_motions_per_bar": [item["hand_motion_count"] for item in grid],
        "actual_attacks_per_bar": per_bar,
        "attack_size_ratio": {key: round(value, 4) for key, value in categories.items()},
        "previous_attack_sustain_ratio": round(sustain_ratio, 4),
        "downbeat_reattack_ratio": round(downbeat_ratio, 4),
        "cross_bar_sustain_ratio": round(cross_bar_ratio, 4),
        "unique_variants_in_four_bars": variant_count,
        "average_velocity": round(mean(event["velocity"] for event in events), 2),
        "full_strum_attack_ratio": round(sum(group[0]["_strum_action"] == "full_strum" for group in groups.values()) / total, 4),
        "long_hand_gap_count": long_gaps,
        "event_count": len(events),
    }


def midi_audit(path: Path):
    midi = mido.MidiFile(path)
    overlaps = unmatched = stuck = 0
    active = defaultdict(list)
    for track in midi.tracks:
        now = 0
        for message in track:
            now += message.time
            if message.type == "note_on" and message.velocity > 0:
                key = (getattr(message, "channel", 0), message.note)
                overlaps += int(bool(active[key])); active[key].append(now)
            elif message.type in {"note_off", "note_on"} and (message.type == "note_off" or message.velocity == 0):
                key = (getattr(message, "channel", 0), message.note)
                if not active[key]: unmatched += 1
                else: active[key].pop(0)
    stuck = sum(map(len, active.values()))
    return {"same_pitch_overlaps": overlaps, "unmatched_note_offs": unmatched, "stuck_notes": stuck}


def main():
    PROJECT.mkdir(parents=True, exist_ok=True)
    instruments = {"acoustic_guitar": {"engine": "fluidsynth", "bank": 0, "program": 25, "gm_name": "Steel Guitar"},
                   "foreground_melody": {"engine": "fluidsynth", "bank": 0, "program": 73, "gm_name": "Flute"}}
    before, after, with_foreground = composition(before=True, with_foreground=False), composition(before=False, with_foreground=False), composition(before=False, with_foreground=True)
    builds = []
    for name, data, mapping in [
        ("before", before, {"acoustic_guitar": instruments["acoustic_guitar"]}),
        ("after", after, {"acoustic_guitar": instruments["acoustic_guitar"]}),
        ("with_foreground", with_foreground, instruments),
    ]:
        folder = PROJECT / f"_{name}_render"
        paths = generate_song_midis(data, mapping, folder)
        destination = PROJECT / ("strumming_after_with_foreground.mid" if name == "with_foreground" else f"strumming_{name}.mid")
        shutil.copy2(paths["full_song"], destination)
        builds.append((name, data, destination))

    debug_data = deepcopy(with_foreground)
    foreground_info = derive_foreground_activity(debug_data, "acoustic_guitar", "foreground_thinning", 4)
    debug_data["tracks"]["acoustic_guitar"]["sections"]["foreground_thinning"]["instrument_phrase"]["foreground_activity"] = foreground_info
    per_string_debug = {"schema_version": 1, "sections": {}}
    variation_debug = {"schema_version": 1, "sections": {}}
    metrics = {"before": {}, "after": {}, "with_foreground": {}}
    prepared = {}
    for name, data, destination in builds:
        working = debug_data if name == "with_foreground" else data
        for section, _ in SECTIONS:
            phrase, events = prepare_phrase(working, section)
            prepared[(name, section)] = (phrase, events)
            metrics[name][section] = phrase_metrics(phrase, events)
            if name == "with_foreground" and phrase.get("_per_string_state_debug"):
                offset = {"baseline": 0, "sixteenth_grid": 4, "per_string_sustain": 8, "foreground_thinning": 12}[section]
                item = deepcopy(phrase["_per_string_state_debug"])
                for step in item["steps"]:
                    step["global_bar"] = offset + step["bar"]
                per_string_debug["sections"][section] = item
            if name == "with_foreground" and phrase.get("_four_bar_variation_debug"):
                variation_debug["sections"][section] = phrase["_four_bar_variation_debug"]
        metrics[name]["midi_integrity"] = midi_audit(destination)

    write_json(PROJECT / "per_string_state_debug.json", per_string_debug)
    write_json(PROJECT / "four_bar_variation_debug.json", variation_debug)
    normal = metrics["after"]["foreground_thinning"]
    thinned = metrics["with_foreground"]["foreground_thinning"]
    comparison = {
        "schema_version": 1, "metrics": metrics,
        "foreground_before_after": {
            "attacks_per_bar": [round(mean(normal["actual_attacks_per_bar"]), 2), round(mean(thinned["actual_attacks_per_bar"]), 2)],
            "average_velocity": [normal["average_velocity"], thinned["average_velocity"]],
            "full_strum_attack_ratio": [normal["full_strum_attack_ratio"], thinned["full_strum_attack_ratio"]],
            "hand_motions_per_bar": [normal["potential_hand_motions_per_bar"], thinned["potential_hand_motions_per_bar"]],
        },
        "foreground_activity": foreground_info,
    }
    write_json(PROJECT / "strumming-comparison.json", comparison)

    report = ["# Strumming Comparison", "",
              "This test uses an original neutral skeleton. It does not contain a copied reference pattern, melody or chord sequence.", "",
              "## Sixteen-bar stages", "",
              f"- Bars 1-4 baseline: {metrics['with_foreground']['baseline']['potential_hand_motions_per_bar']} potential motions; attacks {metrics['with_foreground']['baseline']['actual_attacks_per_bar']}.",
              f"- Bars 5-8 sixteenth grid: {metrics['with_foreground']['sixteenth_grid']['potential_hand_motions_per_bar']} potential motions; attacks {metrics['with_foreground']['sixteenth_grid']['actual_attacks_per_bar']}.",
              f"- Bars 9-12 per-string sustain: previous-attack sustain ratio {metrics['with_foreground']['per_string_sustain']['previous_attack_sustain_ratio']:.1%}; cross-bar sustain {metrics['with_foreground']['per_string_sustain']['cross_bar_sustain_ratio']:.1%}.",
              f"- Bars 13-16 foreground-aware: attacks/bar {comparison['foreground_before_after']['attacks_per_bar'][0]} -> {comparison['foreground_before_after']['attacks_per_bar'][1]}, velocity {normal['average_velocity']} -> {thinned['average_velocity']}, full-strum ratio {normal['full_strum_attack_ratio']:.1%} -> {thinned['full_strum_attack_ratio']:.1%}.", "",
              "## Acceptance", "",
              f"- Four related variants in each new four-bar phrase: {metrics['with_foreground']['per_string_sustain']['unique_variants_in_four_bars']}.",
              f"- First-beat reattack ratio after: {metrics['with_foreground']['per_string_sustain']['downbeat_reattack_ratio']:.1%}; one related variant carries strings across an air downbeat.",
              f"- Long hand gaps caused by chord changes: {metrics['with_foreground']['per_string_sustain']['long_hand_gap_count']}.",
              f"- After MIDI same-pitch overlaps: {metrics['after']['midi_integrity']['same_pitch_overlaps']}; foreground MIDI same-pitch overlaps: {metrics['with_foreground']['midi_integrity']['same_pitch_overlaps']}.",
              "- Unselected strings retain state; selected strings alone are retriggered. Chord changes close only strings whose pitch/fret assignment moves.", ""]
    (PROJECT / "strumming_comparison.md").write_text("\n".join(report), encoding="utf-8")

    write_json(PROJECT / "composition.json", with_foreground)
    write_json(PROJECT / "composition.normalized.json", with_foreground)
    write_json(PROJECT / "instruments.json", instruments)
    write_json(PROJECT / "render.json", {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2",
                                         "fluidsynth_gain": .82, "tail_seconds": 2, "master_peak_db": -1,
                                         "mix": {"acoustic_guitar": {"volume_db": 2, "pan": -.2, "mute": False},
                                                 "foreground_melody": {"volume_db": -2, "pan": .18, "mute": False}}})
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_song.py"), "sixteenth_strumming_demo"], cwd=ROOT)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    shutil.copy2(PROJECT / "output" / "mix.wav", PROJECT / "strumming_after_with_foreground.wav")
    print(json.dumps(comparison["foreground_before_after"], ensure_ascii=False, indent=2))
    print(f"[OK] {PROJECT}")


if __name__ == "__main__":
    main()
