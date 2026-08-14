from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT
from src.composition import load_composition
from src.utils import project_dir
from src.validation import analyze_instrument_aware


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze instrument-aware writing and physical performance issues.")
    parser.add_argument("song", help="project name under projects/")
    parser.add_argument("--write", action="store_true", help="write instrument-validation.json")
    args = parser.parse_args()
    try:
        folder = project_dir(args.song)
        report = analyze_instrument_aware(load_composition(folder / "composition.json"))
        if args.write:
            (folder / "instrument-validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    for item in report["diagnostics"]:
        print(f"[{item['severity'].upper()}] {item['track']}.{item['section']} {item['code']}: {item['message']}")
    print(f"Instrument critic: {report['error_count']} error(s), {report['warning_count']} warning(s), {report['info_count']} info")
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
