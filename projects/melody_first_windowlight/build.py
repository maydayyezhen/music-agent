from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.composition import load_composition
from src.midi import generate_song_midis


def main() -> None:
    composition = load_composition(PROJECT / "composition.json")
    instruments = json.loads((PROJECT / "instruments.json").read_text(encoding="utf-8"))
    paths = generate_song_midis(composition, instruments, PROJECT)
    for name, path in paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
