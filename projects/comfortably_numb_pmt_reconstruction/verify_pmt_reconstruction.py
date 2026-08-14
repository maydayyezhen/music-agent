from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.performance import decode_tokens  # noqa: E402


ROOT = Path(__file__).resolve().parent
SOURCE_PATH = (
    ROOT.parent
    / "comfortably_numb_midi_reconstruction"
    / "build_project.py"
)


def load_source_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "comfortably_numb_source_verify",
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


def source_rows(
    module: ModuleType,
    blob: str,
    *,
    track: int,
    program: int,
) -> list[tuple[int, int, int, int, int, int]]:
    start_tick = 0
    rows = []
    for delta_tick, duration_tick, pitch, velocity in module.unpack(blob):
        start_tick += int(delta_tick)
        rows.append(
            (
                track,
                program,
                int(pitch),
                ticks_to_ms(start_tick, module),
                max(1, ticks_to_ms(int(duration_tick), module)),
                int(velocity),
            )
        )
    return rows


def main() -> None:
    source = load_source_module()
    expected = source_rows(
        source,
        source.LEAD_B85,
        track=0,
        program=30,
    ) + source_rows(
        source,
        source.RHYTHM_B85,
        track=1,
        program=25,
    )
    expected.sort(key=lambda row: (row[3], row[0], row[2]))

    decoded = decode_tokens(
        (ROOT / "performance.pmt").read_text(encoding="utf-8")
    )
    actual = [
        (
            note.track,
            note.program,
            note.pitch,
            note.onset_ms,
            note.duration_ms,
            note.velocity,
        )
        for note in decoded
    ]

    if len(expected) != len(actual):
        raise AssertionError(
            f"note count mismatch: {len(expected)} != {len(actual)}"
        )

    max_onset_error = 0
    max_duration_error = 0
    max_velocity_error = 0
    identity_mismatches = 0
    for source_row, actual_row in zip(expected, actual):
        if source_row[:3] != actual_row[:3]:
            identity_mismatches += 1
        max_onset_error = max(
            max_onset_error,
            abs(source_row[3] - actual_row[3]),
        )
        max_duration_error = max(
            max_duration_error,
            abs(source_row[4] - actual_row[4]),
        )
        max_velocity_error = max(
            max_velocity_error,
            abs(source_row[5] - actual_row[5]),
        )

    gestures = json.loads(
        (ROOT / "performance.gestures.json").read_text(
            encoding="utf-8"
        )
    )
    metadata = json.loads(
        (ROOT / "performance.meta.json").read_text(
            encoding="utf-8"
        )
    )

    if identity_mismatches:
        raise AssertionError(
            f"track/program/pitch mismatches: {identity_mismatches}"
        )
    if max_onset_error > 5:
        raise AssertionError(
            f"max onset error exceeds 5 ms: {max_onset_error}"
        )
    if max_duration_error > 5:
        raise AssertionError(
            f"max duration error exceeds 5 ms: {max_duration_error}"
        )
    if max_velocity_error > 2:
        raise AssertionError(
            f"max velocity error exceeds 2: {max_velocity_error}"
        )
    if not metadata.get("pmt_extensions", {}).get(
        "long_duration_tiling"
    ):
        raise AssertionError("long-duration PMT extension is not enabled")
    if not gestures.get("gestures"):
        raise AssertionError("gesture sidecar contains no lead gestures")

    lead_count = sum(note.track == 0 for note in decoded)
    rhythm_count = sum(note.track == 1 for note in decoded)
    print(f"[PASS] lead notes: {lead_count}")
    print(f"[PASS] rhythm notes: {rhythm_count}")
    print(
        "[PASS] PMT round-trip: "
        f"onset<={max_onset_error}ms, "
        f"duration<={max_duration_error}ms, "
        f"velocity<={max_velocity_error}"
    )
    print(
        f"[PASS] gesture sidecar phrases: "
        f"{len(gestures['gestures'])}"
    )
    print(
        "[PASS] the reference performance survives the PMT path "
        "without long-note truncation"
    )


if __name__ == "__main__":
    main()
