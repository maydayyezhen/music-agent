from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


SCHEMA = "music-agent-project-facade"
SCHEMA_VERSION = 1
AUTHORITIES = {"authoritative", "derived", "cache"}


class ProjectManifestError(ValueError):
    """Raised when the thin project facade is invalid."""


def _safe_relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value.strip() == "":
        raise ProjectManifestError(f"artifact path must be safe and relative: {value!r}")
    return path.as_posix()


def validate_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("schema") != SCHEMA:
        raise ProjectManifestError(f"schema must be {SCHEMA!r}")
    if int(manifest.get("schema_version", 0)) != SCHEMA_VERSION:
        raise ProjectManifestError(
            f"unsupported schema_version: {manifest.get('schema_version')!r}"
        )
    project = manifest.get("project")
    if not isinstance(project, Mapping) or not str(project.get("title", "")).strip():
        raise ProjectManifestError("project.title is required")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, Mapping) or not artifacts:
        raise ProjectManifestError("artifacts must be a non-empty object")

    for name, artifact in artifacts.items():
        if not isinstance(artifact, Mapping):
            raise ProjectManifestError(f"artifact {name!r} must be an object")
        if not str(artifact.get("standard", "")).strip():
            raise ProjectManifestError(f"artifact {name!r} requires standard")
        _safe_relative_path(str(artifact.get("path", "")))
        authority = str(artifact.get("authority", ""))
        if authority not in AUTHORITIES:
            raise ProjectManifestError(
                f"artifact {name!r} authority must be one of {sorted(AUTHORITIES)}"
            )

    for report in manifest.get("conversion_reports", []):
        _safe_relative_path(str(report))


def write_manifest(project_path: Path, manifest: Mapping[str, Any]) -> Path:
    validate_manifest(manifest)
    path = project_path / "manifest.json"
    path.write_text(
        json.dumps(dict(manifest), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def load_manifest(project_path: Path) -> dict[str, Any]:
    path = project_path / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    return manifest


def resolve_artifact(
    project_path: Path,
    manifest: Mapping[str, Any],
    name: str,
    *,
    must_exist: bool = True,
) -> Path:
    artifacts = manifest.get("artifacts", {})
    if name not in artifacts:
        raise ProjectManifestError(f"manifest has no artifact named {name!r}")
    relative = _safe_relative_path(str(artifacts[name]["path"]))
    path = project_path / relative
    if must_exist and not path.is_file():
        raise ProjectManifestError(f"artifact {name!r} is missing: {path}")
    return path


def build_midi_import_manifest(
    *,
    title: str,
    source_filename: str,
    source_sha256: str,
) -> dict[str, Any]:
    """Build a thin index over native standard files.

    The manifest intentionally contains no notes, chords, automation, or plugin
    data. Those remain in their native artifacts.
    """

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "project": {
            "title": title,
            "source": {
                "standard": "MIDI 1.0 Standard MIDI File",
                "filename": source_filename,
                "sha256": source_sha256,
            },
        },
        "artifacts": {
            "performance": {
                "standard": "PMT performance-timed tokens",
                "path": "performance.pmt",
                "authority": "authoritative",
            },
            "performance_metadata": {
                "standard": "PMT adapter metadata",
                "path": "performance.meta.json",
                "authority": "authoritative",
            },
            "midi_sidecar": {
                "standard": "MIDI 1.0 preserved events",
                "path": "performance.midi-sidecar.json",
                "authority": "authoritative",
            },
            "render_config": {
                "standard": "music-agent render extension",
                "path": "render.json",
                "authority": "authoritative",
            },
            "instrument_config": {
                "standard": "music-agent instrument extension",
                "path": "instruments.json",
                "authority": "authoritative",
            },
            "execution_midi": {
                "standard": "MIDI 1.0 Standard MIDI File",
                "path": "output/full_song.mid",
                "authority": "derived",
            },
            "final_audio": {
                "standard": "WAVE PCM audio",
                "path": "output/mix.wav",
                "authority": "derived",
            },
        },
        "conversion_reports": ["reports/midi-import.json"],
        "edit_protocols": {
            "pointer": "RFC 6901 JSON Pointer",
            "patch": "RFC 6902 JSON Patch",
        },
    }
