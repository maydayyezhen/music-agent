from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT  # noqa: F401
from src.accompaniment import analyze_continuity
from src.composition import load_composition
from src.utils import project_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze accompaniment texture, continuity, and voice leading.")
    parser.add_argument("song", help="project name under projects/")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true", help="write continuity-report.json")
    args = parser.parse_args()
    try:
        song = project_dir(args.song)
        report = analyze_continuity(load_composition(song / "composition.json"))
        if args.write:
            path = song / "continuity-report.json"
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"[OK] {path}")
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            for section, metrics in report["section_metrics"].items():
                print(f"{section}: P/L/P={metrics['point_line_plane_balance']} textures={metrics['texture_distribution']}")
            for warning in report["warnings"]:
                print(f"[WARN] {warning['section']} / {warning['track']}: {warning['code']} - {warning['message']}")
            print(f"Continuity critic completed with {report['warning_count']} warning(s).")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
