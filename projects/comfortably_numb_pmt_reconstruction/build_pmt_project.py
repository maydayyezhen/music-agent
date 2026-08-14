from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.performance import (  # noqa: E402
    GestureAction,
    PMTNote,
    PerformanceGesture,
    build_sidecar,
    decode_tokens,
    encode_notes,
    serialize_tokens,
)


ROOT = Path(__file__).resolve().parent
SOURCE_PATH = (
    ROOT.parent
    / "comfortably_numb_midi_reconstruction"
    / "build_project.py"
)
LEAD_PROGRAM = 30
RHYTHM_PROGRAM = 25
PHRASE_GAP_MS = 450


def load_source_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "comfortably_numb_source",
        SOURCE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load source table: {SOURCE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ticks_to_ms(ticks: int, module: ModuleType) -> int:
    return round(
        ticks
        * int(module.TEMPO_US_PER_BEAT)
        / int(module.TPB)
        / 1000.0
    )


def decode_source_track(
    module: ModuleType,
    blob: str,
    *,
    track: int,
    program: int,
) -> list[PMTNote]:
    start_tick = 0
    notes: list[PMTNote] = []
    for delta_tick, duration_tick, pitch, velocity in module.unpack(blob):
        start_tick += int(delta_tick)
        notes.append(
            PMTNote(
                track=track,
                program=program,
                pitch=int(pitch),
                onset_ms=ticks_to_ms(start_tick, module),
                duration_ms=max(1, ticks_to_ms(int(duration_tick), module)),
                velocity=int(velocity),
            )
        )
    return notes


def split_phrases(notes: list[PMTNote]) -> list[list[PMTNote]]:
    if not notes:
        return []
    phrases: list[list[PMTNote]] = [[notes[0]]]
    for note in notes[1:]:
        previous = phrases[-1][-1]
        gap = note.onset_ms - (previous.onset_ms + previous.duration_ms)
        if gap >= PHRASE_GAP_MS:
            phrases.append([note])
        else:
            phrases[-1].append(note)
    return phrases


def phrase_gesture(
    phrase: list[PMTNote],
    phrase_index: int,
) -> PerformanceGesture:
    actions: list[GestureAction] = []
    for index, note in enumerate(phrase):
        note_id = f"lead-n{phrase_index:02d}-{index:03d}"
        previous = phrase[index - 1] if index else None
        if previous is None:
            actions.append(
                GestureAction(
                    action_id=f"{note_id}-attack",
                    kind="pick",
                    time_ms=note.onset_ms,
                    note_id=note_id,
                    pitch=note.pitch,
                    velocity=note.velocity,
                )
            )
        else:
            previous_end = previous.onset_ms + previous.duration_ms
            gap = note.onset_ms - previous_end
            interval = note.pitch - previous.pitch
            if gap <= 70 and 0 < abs(interval) <= 2:
                kind = "hammer_on" if interval > 0 else "pull_off"
                actions.append(
                    GestureAction(
                        action_id=f"{note_id}-{kind}",
                        kind=kind,
                        time_ms=note.onset_ms,
                        note_id=note_id,
                        from_pitch=previous.pitch,
                        to_pitch=note.pitch,
                        transition_ms=35,
                        retrigger=False,
                    )
                )
            elif gap <= 100 and 2 < abs(interval) <= 5:
                actions.append(
                    GestureAction(
                        action_id=f"{note_id}-slide",
                        kind="slide",
                        time_ms=note.onset_ms,
                        note_id=note_id,
                        from_pitch=previous.pitch,
                        to_pitch=note.pitch,
                        transition_ms=min(160, max(60, note.duration_ms // 3)),
                        retrigger=False,
                    )
                )
            else:
                actions.append(
                    GestureAction(
                        action_id=f"{note_id}-attack",
                        kind="pick",
                        time_ms=note.onset_ms,
                        note_id=note_id,
                        pitch=note.pitch,
                        velocity=note.velocity,
                    )
                )

        if note.duration_ms >= 700:
            delay_ms = min(420, max(180, round(note.duration_ms * 0.32)))
            actions.append(
                GestureAction(
                    action_id=f"{note_id}-vibrato",
                    kind="vibrato",
                    time_ms=note.onset_ms,
                    note_id=note_id,
                    pitch=note.pitch,
                    parameters={
                        "delay_ms": float(delay_ms),
                        "rate_hz": 4.8,
                        "depth_cents": 24.0
                        if note.duration_ms < 1500
                        else 32.0,
                    },
                )
            )

    final = phrase[-1]
    actions.append(
        GestureAction(
            action_id=f"lead-g{phrase_index:02d}-release",
            kind="release",
            time_ms=final.onset_ms + final.duration_ms,
            note_id=f"lead-n{phrase_index:02d}-{len(phrase) - 1:03d}",
            pitch=final.pitch,
        )
    )
    actions.sort(key=lambda action: (action.time_ms, action.action_id))
    return PerformanceGesture(
        gesture_id=f"lead-g{phrase_index:02d}",
        track=0,
        program=LEAD_PROGRAM,
        instrument="electric_guitar",
        string_index=None,
        actions=tuple(actions),
    )


def quantization_report(
    source_notes: list[PMTNote],
    decoded_notes: list[PMTNote],
) -> dict[str, Any]:
    ordered_source = sorted(
        source_notes,
        key=lambda note: (note.onset_ms, note.track, note.pitch),
    )
    if len(ordered_source) != len(decoded_notes):
        raise AssertionError(
            f"PMT note count changed: {len(ordered_source)} -> "
            f"{len(decoded_notes)}"
        )

    onset_errors: list[int] = []
    duration_errors: list[int] = []
    velocity_errors: list[int] = []
    identity_mismatches = 0
    for source, decoded in zip(ordered_source, decoded_notes):
        if (
            source.track,
            source.program,
            source.pitch,
        ) != (
            decoded.track,
            decoded.program,
            decoded.pitch,
        ):
            identity_mismatches += 1
        onset_errors.append(abs(source.onset_ms - decoded.onset_ms))
        duration_errors.append(abs(source.duration_ms - decoded.duration_ms))
        velocity_errors.append(abs(source.velocity - decoded.velocity))

    return {
        "source_note_count": len(ordered_source),
        "decoded_note_count": len(decoded_notes),
        "identity_mismatches": identity_mismatches,
        "max_onset_error_ms": max(onset_errors, default=0),
        "max_duration_error_ms": max(duration_errors, default=0),
        "max_velocity_error": max(velocity_errors, default=0),
        "longest_source_note_ms": max(
            (note.duration_ms for note in ordered_source),
            default=0,
        ),
        "longest_decoded_note_ms": max(
            (note.duration_ms for note in decoded_notes),
            default=0,
        ),
    }


def main() -> None:
    source = load_source_module()
    lead = decode_source_track(
        source,
        source.LEAD_B85,
        track=0,
        program=LEAD_PROGRAM,
    )
    rhythm = decode_source_track(
        source,
        source.RHYTHM_B85,
        track=1,
        program=RHYTHM_PROGRAM,
    )
    notes = lead + rhythm

    tokens = encode_notes(notes, tile_long_durations=True)
    decoded = decode_tokens(tokens)
    report = quantization_report(notes, decoded)
    if report["identity_mismatches"]:
        raise AssertionError(f"PMT identity mismatch: {report}")
    if report["max_onset_error_ms"] > 5:
        raise AssertionError(f"PMT onset error exceeded 5 ms: {report}")
    if report["max_duration_error_ms"] > 5:
        raise AssertionError(f"PMT duration error exceeded 5 ms: {report}")
    if report["max_velocity_error"] > 2:
        raise AssertionError(f"PMT velocity error exceeded 2: {report}")

    gestures = [
        phrase_gesture(phrase, index)
        for index, phrase in enumerate(split_phrases(lead))
    ]
    sidecar = build_sidecar(
        gestures,
        source="user-supplied reference MIDI",
    )

    metadata = {
        "schema": "music-agent-pmt-project",
        "schema_version": 1,
        "title": "Comfortably Numb PMT Reconstruction",
        "tempo_microseconds_per_beat": int(
            source.TEMPO_US_PER_BEAT
        ),
        "ticks_per_beat": int(source.TPB),
        "time_signature": [4, 4],
        "tracks": {
            "0": {
                "name": "lead_guitar",
                "channel": 0,
                "bank": 0,
            },
            "1": {
                "name": "rhythm_guitar",
                "channel": 2,
                "bank": 0,
            },
        },
        "source": {
            "kind": "embedded_reference_midi",
            "lead_notes": len(lead),
            "rhythm_notes": len(rhythm),
        },
        "pmt_extensions": {
            "long_duration_tiling": True,
        },
    }

    (ROOT / "performance.pmt").write_text(
        serialize_tokens(tokens),
        encoding="utf-8",
    )
    (ROOT / "performance.gestures.json").write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "performance.meta.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report["token_count"] = len(tokens)
    report["gesture_count"] = len(gestures)
    (ROOT / "roundtrip-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] wrote {ROOT / 'performance.pmt'}")
    print(
        f"[OK] PMT notes={len(decoded)} "
        f"(lead={len(lead)}, rhythm={len(rhythm)})"
    )
    print(
        "[OK] round-trip errors: "
        f"onset<={report['max_onset_error_ms']}ms, "
        f"duration<={report['max_duration_error_ms']}ms, "
        f"velocity<={report['max_velocity_error']}"
    )
    print(
        f"[OK] gesture sidecar phrases={len(gestures)}; "
        "audio rendering still uses PMT note performance"
    )


if __name__ == "__main__":
    main()
