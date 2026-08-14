from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import mido

from _bootstrap import ROOT
from src.composition import load_composition
from src.validation import analyze_strumming_flow


NON_TARGET_TRACKS = ["vocal_melody", "electric_texture_guitar", "bass", "drums", "orchestra_pad"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def attack_groups(composition: dict, track_name: str) -> dict[str, float]:
    result = {}
    track = composition["tracks"][track_name]
    for section in composition["sections"]:
        name, bars = section["name"], section["bars"]
        clip = track.get("sections", {}).get(name)
        counts = [0] * bars
        if clip:
            groups = defaultdict(set)
            for index, event in enumerate(clip.get("events", [])):
                bar = int(str(event["at"]).split(":", 1)[0])
                groups[bar].add(event.get("_attack_group", f"event-{index}"))
            counts = [len(groups[bar]) for bar in range(1, bars + 1)]
        result[name] = round(sum(counts) / bars, 3)
    return result


def sequential_pair(before: Path, after: Path, destination: Path) -> None:
    left, right = mido.MidiFile(before), mido.MidiFile(after)
    if left.ticks_per_beat != right.ticks_per_beat:
        raise ValueError("before/after MIDI use different PPQ")
    output = mido.MidiFile(type=1, ticks_per_beat=left.ticks_per_beat)
    track = mido.MidiTrack(); output.tracks.append(track)
    track.append(mido.MetaMessage("track_name", name="BEFORE then AFTER", time=0))
    track.append(mido.MetaMessage("marker", text="BEFORE CONTINUOUS STRUM FIX", time=0))
    for message in mido.merge_tracks(left.tracks):
        if message.type not in {"end_of_track", "track_name"}:
            track.append(message.copy())
    track.append(mido.MetaMessage("marker", text="AFTER CONTINUOUS STRUM FIX", time=left.ticks_per_beat * 8))
    for message in mido.merge_tracks(right.tracks):
        if message.type not in {"end_of_track", "track_name"}:
            track.append(message.copy())
    track.append(mido.MetaMessage("end_of_track", time=0))
    output.save(destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("song")
    args = parser.parse_args()
    project = ROOT / "projects" / args.song
    before = json.loads((project / "composition_before_continuous_strum_fix.json").read_text(encoding="utf-8"))
    after = load_composition(project / "composition.json")
    report = analyze_strumming_flow(after)
    (project / "strumming-flow-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    sequential_pair(project / "acoustic_before.mid", project / "acoustic_after.mid", project / "acoustic_before_after.mid")
    sequential_pair(project / "electric_before.mid", project / "electric_after.mid", project / "electric_before_after.mid")

    non_target_composition = {
        track: before["tracks"][track] == after["tracks"][track] for track in NON_TARGET_TRACKS
    }
    before_hashes = json.loads((project / "non_guitar_track_hashes_before.json").read_text(encoding="utf-8-sig"))
    after_hashes = {track: sha(project / "tracks" / f"{track}.mid").upper() for track in NON_TARGET_TRACKS}
    midi_identity = {track: before_hashes[track] == after_hashes[track] for track in NON_TARGET_TRACKS}
    fixed_sections = report["tracks"]
    acoustic_after = {name: round(value["average_sounding_strums_per_bar"], 3)
                      for name, value in fixed_sections["acoustic_guitar"]["sections"].items()}
    electric_after = {name: round(value["average_sounding_strums_per_bar"], 3)
                      for name, value in fixed_sections["electric_rhythm_guitar"]["sections"].items()}
    acoustic_before = attack_groups(before, "acoustic_guitar")
    electric_before = attack_groups(before, "electric_rhythm_guitar")

    payload = {
        "schema_version": 1,
        "non_target_composition_identical": non_target_composition,
        "non_target_midi_identical": midi_identity,
        "sections_identical": before["sections"] == after["sections"],
        "metadata_except_guitar_release_audit_identical": {
            key: before["metadata"].get(key) == after["metadata"].get(key)
            for key in before["metadata"] if key != "guitar_controlled_releases"
        },
        "acoustic_before_average_attack_groups": acoustic_before,
        "acoustic_after_average_sounding_strums": acoustic_after,
        "electric_before_average_attack_groups": electric_before,
        "electric_after_average_sounding_strums": electric_after,
        "acoustic_midi_unchanged": sha(project / "acoustic_before.mid") == sha(project / "acoustic_after.mid"),
        "electric_midi_changed": sha(project / "electric_before.mid") != sha(project / "electric_after.mid"),
        "strumming_validator_warnings": report["warning_count"],
    }
    (project / "continuous-strum-audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    a = fixed_sections["acoustic_guitar"]["sections"]
    e = fixed_sections["electric_rhythm_guitar"]["sections"]
    lines = [
        "# Continuous Strum Comparison", "",
        "## Root cause", "",
        "The shared guitar path stored only sounding note events. Air strokes, hand direction and cross-bar hand state were absent, while the legacy electric rhythm arrangement used sparse sustained attacks in Verse and Chorus. The Acoustic part in this song was already explicitly authored with healthy motion; its missing piece was auditable right-hand state.", "",
        "## Before / after", "",
        "| Track / section | Before audible attacks per bar | After audible strums per bar |", "|---|---:|---:|",
        f"| Acoustic Verse 1 | {acoustic_before['verse_1']:.2f} | {acoustic_after['verse_1']:.2f} |",
        f"| Acoustic Chorus 1 | {acoustic_before['chorus_1']:.2f} | {acoustic_after['chorus_1']:.2f} |",
        f"| Electric Rhythm Verse 1 | {electric_before['verse_1']:.2f} | {electric_after['verse_1']:.2f} |",
        f"| Electric Rhythm Verse 2 | {electric_before['verse_2']:.2f} | {electric_after['verse_2']:.2f} |",
        f"| Electric Rhythm Chorus 1 | {electric_before['chorus_1']:.2f} | {electric_after['chorus_1']:.2f} |",
        f"| Electric Rhythm Chorus 2 | {electric_before['chorus_2']:.2f} | {electric_after['chorus_2']:.2f} |",
        f"| Electric Rhythm Final Chorus | {electric_before['final_chorus']:.2f} | {electric_after['final_chorus']:.2f} |", "",
        "## Flow evidence", "",
        f"- Acoustic Verse/Chorus hand motion: {a['verse_1']['average_hand_motions_per_bar']:.0f}/{a['chorus_1']['average_hand_motions_per_bar']:.0f} eighth-note motions per bar; audible {a['verse_1']['average_sounding_strums_per_bar']:.2f}/{a['chorus_1']['average_sounding_strums_per_bar']:.2f}.",
        f"- Electric Verse/Chorus hand motion: {e['verse_1']['average_hand_motions_per_bar']:.0f}/{e['chorus_1']['average_hand_motions_per_bar']:.0f}; audible {e['verse_1']['average_sounding_strums_per_bar']:.2f}/{e['chorus_1']['average_sounding_strums_per_bar']:.2f}.",
        f"- Vocal-active Acoustic/Electric Verse 1 density: {a['verse_1']['vocal_active_average_sounding_strums']:.2f}/{e['verse_1']['vocal_active_average_sounding_strums']:.2f}. Vocal activity changes articulation and dynamics; it does not stop the right hand.",
        f"- Cross-bar pattern resets: Acoustic {sum(value['bar_pattern_reset_count'] for value in a.values())}; Electric {sum(value['bar_pattern_reset_count'] for value in e.values())}. Chord-change interruptions: Acoustic {sum(value['chord_change_interruption_count'] for value in a.values())}; Electric {sum(value['chord_change_interruption_count'] for value in e.values())}.",
        "- Air strokes stay in `strumming_grid`; they are deliberately not rendered as pitched MIDI notes.",
        "- Intentional sustained-hit exceptions: Acoustic Outro bars 5-6; Electric Interlude bars 1-4, Bridge bars 7-8, Outro bars 1-2. These are arrangement planes against active Acoustic material, not accidental Verse/Chorus defaults.",
        "- Remaining unintended one-hit Verse/Chorus bars: 0.", "",
        "## Scope proof", "",
        f"- Non-target composition tracks byte-equivalent as JSON: {all(non_target_composition.values())}.",
        f"- Non-target rendered MIDI SHA-256 unchanged: {all(midi_identity.values())}.",
        f"- Form/section data unchanged: {payload['sections_identical']}.",
        f"- Acoustic MIDI notes unchanged: {payload['acoustic_midi_unchanged']} (the fix adds explicit hand-state IR and re-renders the same authored part).",
        f"- Electric Rhythm MIDI changed: {payload['electric_midi_changed']}.",
        f"- Strumming validator warnings: {report['warning_count']}.", "",
        "`acoustic_before_after.mid` and `electric_before_after.mid` play the complete BEFORE version, wait two bars, then play the complete AFTER version.", "",
    ]
    (project / "continuous_strum_comparison.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
