from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.performance.midi_import import write_project


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import a Standard MIDI File into PMT plus a MIDI sidecar."
    )
    parser.add_argument("midi", type=Path, help="source .mid file")
    parser.add_argument("project", help="project name under projects/")
    args = parser.parse_args()
    source = args.midi.expanduser().resolve()
    if not source.is_file():
        print(f"[FAIL] MIDI file not found: {source}", file=sys.stderr)
        return 1
    project_path = ROOT / "projects" / args.project
    try:
        result = write_project(source, project_path)
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    fingerprint = result["fingerprint"]
    print(f"[OK] project: {project_path}")
    print(
        f"[OK] PMT notes: {fingerprint['note_count']} across "
        f"{fingerprint['active_tracks']} active tracks"
    )
    print(f"[OK] channel events: {fingerprint['channel_event_count']}")
    print(
        f"[OK] conductor/SysEx events: "
        f"{fingerprint['conductor_event_count']}"
    )
    if fingerprint["unsupported_messages"]:
        print(f"[WARN] unsupported messages: {fingerprint['unsupported_messages']}")
    if fingerprint["unmatched_note_events"]:
        print(
            f"[WARN] unmatched note events: "
            f"{fingerprint['unmatched_note_events']}"
        )
    print(f"[OK] performance.pmt: {project_path / 'performance.pmt'}")
    print(
        f"[OK] MIDI sidecar: "
        f"{project_path / 'performance.midi-sidecar.json'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
