from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from src.project_facade import (
    ProjectManifestError,
    build_midi_import_manifest,
    load_manifest,
    resolve_artifact,
    validate_manifest,
)
from src.project_facade.midi_adapter import write_midi_import_facade


class ProjectFacadeTests(unittest.TestCase):
    def fake_result(self) -> dict:
        return {
            "metadata": {"title": "Facade Test"},
            "fingerprint": {
                "source_filename": "source.mid",
                "source_sha256": "a" * 64,
                "note_count": 3,
                "active_tracks": 1,
                "channel_event_count": 2,
                "conductor_event_count": 1,
                "unmatched_note_events": 0,
                "unsupported_messages": {},
            },
        }

    def test_manifest_is_only_an_index(self) -> None:
        manifest = build_midi_import_manifest(
            title="Facade Test",
            source_filename="source.mid",
            source_sha256="a" * 64,
        )
        validate_manifest(manifest)
        serialized = json.dumps(manifest)
        self.assertNotIn("PITCH_", serialized)
        self.assertNotIn("notes", manifest)
        self.assertEqual(
            manifest["artifacts"]["performance"]["standard"],
            "PMT performance-timed tokens",
        )
        self.assertEqual(
            manifest["artifacts"]["execution_midi"]["authority"],
            "derived",
        )

    def test_facade_writes_manifest_and_conversion_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for name in (
                "performance.pmt",
                "performance.meta.json",
                "performance.midi-sidecar.json",
                "render.json",
                "instruments.json",
            ):
                (project / name).write_text("{}\n", encoding="utf-8")
            write_midi_import_facade(project, self.fake_result())

            manifest = load_manifest(project)
            self.assertEqual(manifest["project"]["title"], "Facade Test")
            self.assertEqual(
                resolve_artifact(project, manifest, "performance"),
                project / "performance.pmt",
            )
            report = json.loads(
                (project / "reports" / "midi-import.json").read_text(
                    encoding="utf-8"
                )
            )
            statuses = {item["status"] for item in report["mappings"]}
            self.assertIn("lossless", statuses)
            self.assertIn("quantized", statuses)
            self.assertIn("preserved_in_sidecar", statuses)

    def test_manifest_rejects_parent_path_escape(self) -> None:
        manifest = build_midi_import_manifest(
            title="Facade Test",
            source_filename="source.mid",
            source_sha256="a" * 64,
        )
        manifest["artifacts"]["performance"]["path"] = "../outside.pmt"
        with self.assertRaises(ProjectManifestError):
            validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
