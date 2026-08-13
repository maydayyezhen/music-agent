from __future__ import annotations

import argparse
import json

from _bootstrap import ROOT  # noqa: F401
from src.complexity import normalize_complexity, parse_complexity_request


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a level/preset or natural-language brief into a complexity profile.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--level", help="minimal/simple/standard/rich/dense or a named preset")
    group.add_argument("--text", help="Chinese or English musical complexity request")
    args = parser.parse_args()
    result = normalize_complexity(args.level) if args.level else parse_complexity_request(args.text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
