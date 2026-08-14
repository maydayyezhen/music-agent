from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.project_facade import load_manifest, resolve_artifact


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a project through the standard artifact named by manifest.json."
    )
    parser.add_argument("project", help="project name under projects/")
    args = parser.parse_args()
    project_path = ROOT / "projects" / args.project

    try:
        manifest = load_manifest(project_path)
        performance = manifest["artifacts"].get("performance")
        if not performance:
            raise ValueError("manifest has no performance artifact")
        resolve_artifact(project_path, manifest, "performance")
        standard = str(performance["standard"])
        if not standard.startswith("PMT"):
            raise ValueError(
                f"no renderer adapter is registered for {standard!r}; "
                "the native artifact remains untouched"
            )
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        str(ROOT / "scripts" / "render_pmt_project.py"),
        args.project,
    ]
    return subprocess.run(command, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
