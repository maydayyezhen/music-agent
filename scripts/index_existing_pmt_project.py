from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.project_facade.midi_adapter import write_midi_import_facade


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add manifest.json and a conversion report to an existing PMT project."
    )
    parser.add_argument("project", help="project name under projects/")
    args = parser.parse_args()
    project_path = ROOT / "projects" / args.project
    try:
        metadata = json.loads(
            (project_path / "performance.meta.json").read_text(encoding="utf-8")
        )
        fingerprint = json.loads(
            (project_path / "source-fingerprint.json").read_text(encoding="utf-8")
        )
        write_midi_import_facade(
            project_path,
            {"metadata": metadata, "fingerprint": fingerprint},
        )
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print(f"[OK] manifest: {project_path / 'manifest.json'}")
    print(f"[OK] conversion report: {project_path / 'reports' / 'midi-import.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
