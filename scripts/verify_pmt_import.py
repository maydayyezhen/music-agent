from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.performance import decode_tokens
from src.performance.midi_import import import_midi


def note_hash(notes) -> str:
    normalized = sorted(
        (n.track, n.program, n.pitch, n.onset_ms, n.duration_ms, n.velocity)
        for n in notes
    )
    return sha256(
        json.dumps(normalized, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify a PMT MIDI import against its fingerprint and optional "
            "source MIDI."
        )
    )
    parser.add_argument("project", help="project name under projects/")
    parser.add_argument(
        "source_midi",
        nargs="?",
        type=Path,
        help="optional original MIDI for a fresh comparison",
    )
    args = parser.parse_args()
    project = ROOT / "projects" / args.project
    try:
        fingerprint = json.loads(
            (project / "source-fingerprint.json").read_text(encoding="utf-8")
        )
        notes = decode_tokens(
            (project / "performance.pmt").read_text(encoding="utf-8")
        )
        sidecar = json.loads(
            (project / "performance.midi-sidecar.json").read_text(
                encoding="utf-8"
            )
        )
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if len(notes) != int(fingerprint["note_count"]):
        errors.append(f"note count {len(notes)} != {fingerprint['note_count']}")
    if note_hash(notes) != fingerprint["pmt_note_tuple_sha256"]:
        errors.append("PMT note hash differs from import fingerprint")
    channel_events = sum(
        len(track.get("events", []))
        for track in sidecar["tracks"].values()
    )
    if channel_events != int(fingerprint["channel_event_count"]):
        errors.append(
            f"channel event count {channel_events} != "
            f"{fingerprint['channel_event_count']}"
        )
    if len(sidecar.get("conductor_events", [])) != int(
        fingerprint["conductor_event_count"]
    ):
        errors.append("conductor event count differs from import fingerprint")

    if args.source_midi is not None:
        source = args.source_midi.expanduser().resolve()
        fresh = import_midi(source)
        fresh_fingerprint = fresh["fingerprint"]
        if fresh_fingerprint["source_sha256"] != fingerprint["source_sha256"]:
            errors.append("source MIDI SHA-256 differs from imported source")
        if (
            fresh_fingerprint["pmt_note_tuple_sha256"]
            != fingerprint["pmt_note_tuple_sha256"]
        ):
            errors.append("fresh source import produces different PMT notes")
        if fresh_fingerprint["channel_event_count"] != channel_events:
            errors.append("fresh source import produces different channel events")

    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print(f"[PASS] PMT notes: {len(notes)}")
    print(f"[PASS] active tracks: {fingerprint['active_tracks']}")
    print(f"[PASS] channel events: {channel_events}")
    print(
        f"[PASS] conductor/SysEx events: "
        f"{len(sidecar.get('conductor_events', []))}"
    )
    print("[PASS] PMT and MIDI sidecar match the import fingerprint")
    if args.source_midi is not None:
        print("[PASS] source MIDI re-import matches the project")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
