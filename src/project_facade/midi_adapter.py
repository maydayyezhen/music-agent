from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .manifest import build_midi_import_manifest, write_manifest


def _conversion_report(result: Mapping[str, Any]) -> dict[str, Any]:
    fingerprint = result["fingerprint"]
    unsupported = dict(fingerprint.get("unsupported_messages", {}))
    dropped_count = sum(int(value) for value in unsupported.values())
    return {
        "schema": "music-agent-conversion-report",
        "schema_version": 1,
        "adapter": "midi-1-smf-to-pmt-plus-midi-sidecar",
        "source": {
            "standard": "MIDI 1.0 Standard MIDI File",
            "filename": fingerprint["source_filename"],
            "sha256": fingerprint["source_sha256"],
        },
        "targets": [
            "performance.pmt",
            "performance.meta.json",
            "performance.midi-sidecar.json",
        ],
        "summary": {
            "note_count": int(fingerprint["note_count"]),
            "active_tracks": int(fingerprint["active_tracks"]),
            "sidecar_channel_events": int(fingerprint["channel_event_count"]),
            "sidecar_conductor_events": int(fingerprint["conductor_event_count"]),
            "unmatched_note_events": int(fingerprint["unmatched_note_events"]),
            "dropped_message_count": dropped_count,
        },
        "mappings": [
            {
                "source": "MIDI note pitch / track / program",
                "target": "PMT PITCH / TRACK / PROG",
                "status": "lossless",
            },
            {
                "source": "MIDI note onset / duration",
                "target": "PMT TSHIFT / DURP",
                "status": "quantized",
                "detail": "10 ms PMT time quantum",
            },
            {
                "source": "MIDI note velocity",
                "target": "PMT VEL",
                "status": "quantized",
                "detail": "32 velocity bins; decoded error is at most 2 MIDI units",
            },
            {
                "source": "tempo, meter, key, SysEx, program, CC, pitch bend and pressure",
                "target": "performance.midi-sidecar.json",
                "status": "preserved_in_sidecar",
            },
            {
                "source": "unsupported MIDI messages",
                "target": None,
                "status": "dropped" if dropped_count else "not_present",
                "counts": unsupported,
            },
        ],
    }


def write_midi_import_facade(project_path: Path, result: Mapping[str, Any]) -> None:
    fingerprint = result["fingerprint"]
    metadata = result["metadata"]
    reports = project_path / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "midi-import.json").write_text(
        json.dumps(_conversion_report(result), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_manifest(
        project_path,
        build_midi_import_manifest(
            title=str(metadata["title"]),
            source_filename=str(fingerprint["source_filename"]),
            source_sha256=str(fingerprint["source_sha256"]),
        ),
    )
