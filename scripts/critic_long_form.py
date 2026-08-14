from __future__ import annotations

import argparse
import json
import sys

from _bootstrap import ROOT
from src.composition import load_composition
from src.utils import project_dir
from src.validation import analyze_long_form_phrases


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze 8-16 bar melodic narrative and phrase-state continuity.")
    parser.add_argument("song", help="project name under projects/")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        folder = project_dir(args.song)
        report = analyze_long_form_phrases(load_composition(folder / "composition.json"))
        if args.write:
            (folder / "long-form-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr); return 1
    for section in report["sections"]:
        metrics = section["assessment"]
        print(f"{section['track']}.{section['section']}: narrative={metrics['continuous_narrative_bars']} bars, "
              f"developments={metrics['motif_developments']}, cross_bar={metrics['cross_bar_notes']}, "
              f"resets={metrics['independent_phrase_resets']}, strong_cadences={metrics['strong_cadences']}, "
              f"peak_bar={metrics['peak_bars']}")
    for item in report["diagnostics"]:
        print(f"[{item['severity'].upper()}] {item['track']}.{item['section']} {item['code']}: {item['message']}")
    print(f"Long-form critic: {report['error_count']} error(s), {report['warning_count']} warning(s)")
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
