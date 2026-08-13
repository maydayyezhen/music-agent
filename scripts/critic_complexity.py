from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT
from src.complexity.critic import analyze_complexity
from src.composition import load_composition
from src.utils import project_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze rhythm, density, interaction, and target complexity.")
    parser.add_argument("song")
    parser.add_argument("--json", action="store_true", help="print full JSON report")
    parser.add_argument("--write", action="store_true", help="write complexity-report.json in the song directory")
    args = parser.parse_args()
    try:
        song_dir = project_dir(args.song)
        report = analyze_complexity(load_composition(song_dir / "composition.json"))
        if args.write:
            path = song_dir / "complexity-report.json"
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"[OK] {path}")
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            for section, metrics in report["section_metrics"].items():
                print(
                    f"{section}: density={metrics['section_density']:.2f}/bar, "
                    f"active={metrics['active_tracks']}, onset_overlap={metrics['onset_overlap_ratio']:.2f}"
                )
            for warning in report["warnings"]:
                print(f"[WARN] {warning['section']} / {warning['track']}: {warning['code']} - {warning['message']}")
            print(f"Complexity critic completed with {report['warning_count']} warning(s).")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
