from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

import mido


ROOT = Path(__file__).resolve().parent
EXPECTED = json.loads((ROOT / "source-fingerprint.json").read_text(encoding="utf-8"))


def note_rows(path: Path) -> tuple[list[tuple[int, int, int, int, int]], list[int]]:
    midi = mido.MidiFile(path)
    active: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    rows: list[tuple[int, int, int, int, int]] = []
    programs: list[int] = []
    for track in midi.tracks:
        tick = 0
        for message in track:
            tick += message.time
            if message.type == "program_change":
                programs.append(message.program)
            elif message.type == "note_on" and message.velocity > 0:
                active[(message.channel, message.note)].append((tick, message.velocity))
            elif message.type in {"note_off", "note_on"} and (
                message.type == "note_off" or message.velocity == 0
            ):
                key = (message.channel, message.note)
                if active[key]:
                    start, velocity = active[key].pop(0)
                    rows.append((start, tick - start, message.note, velocity, message.channel))
    return sorted(rows), programs


def digest(rows: list[tuple[int, int, int, int, int]]) -> str:
    payload = "\n".join(",".join(map(str, row)) for row in rows).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    failures: list[str] = []
    for track_name, expected in EXPECTED["tracks"].items():
        path = ROOT / "tracks" / f"{track_name}.mid"
        if not path.is_file():
            failures.append(f"missing generated track: {path}")
            continue
        rows, programs = note_rows(path)
        actual_hash = digest(rows)
        if len(rows) != expected["note_count"]:
            failures.append(
                f"{track_name}: note count {len(rows)} != {expected['note_count']}"
            )
        if actual_hash != expected["note_tuple_sha256"]:
            failures.append(
                f"{track_name}: note timing/pitch/velocity/channel fingerprint differs"
            )
        if expected["source_program"] not in programs:
            failures.append(
                f"{track_name}: program {expected['source_program']} not found in {programs}"
            )
        print(
            f"[{'PASS' if actual_hash == expected['note_tuple_sha256'] else 'FAIL'}] "
            f"{track_name}: {len(rows)} notes, sha256={actual_hash}"
        )

    full_song = ROOT / "output" / "full_song.mid"
    if full_song.is_file():
        midi = mido.MidiFile(full_song)
        tempos = [
            message.tempo
            for track in midi.tracks
            for message in track
            if message.type == "set_tempo"
        ]
        if not tempos or tempos[0] != EXPECTED["tempo_microseconds_per_beat"]:
            failures.append(
                f"tempo differs: {tempos[:1]} != "
                f"{EXPECTED['tempo_microseconds_per_beat']}"
            )

    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}")
        return 1
    print("[PASS] Existing project schema reproduced every source note event exactly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
