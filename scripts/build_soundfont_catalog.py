from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from _bootstrap import ROOT
from src.render.fluidsynth import find_fluidsynth


PRESET_PATTERN = re.compile(r"^(\d{3})-(\d{3})\s+(.+?)\s*$")
MELODIC_FAMILIES = (
    "piano", "chromatic_percussion", "organ", "guitar", "bass", "orchestral_strings",
    "ensemble_and_voice", "brass", "reed", "pipe", "synth_lead", "synth_pad",
    "synth_effect", "world", "pitched_percussion", "sound_effect",
)


def family_for(bank: int, program: int) -> str:
    if bank in (120, 128):
        return "drum_kit"
    return MELODIC_FAMILIES[min(program // 8, len(MELODIC_FAMILIES) - 1)]


def inspect_soundfont(soundfont: Path) -> list[dict[str, object]]:
    executable = find_fluidsynth()
    if executable is None:
        raise FileNotFoundError("FluidSynth not found; run scripts/setup_assets.py")
    completed = subprocess.run(
        [str(executable), "-n", str(soundfont)],
        input="inst 1\nquit\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    combined = completed.stdout + "\n" + completed.stderr
    presets: list[dict[str, object]] = []
    for line in combined.splitlines():
        match = PRESET_PATTERN.match(line.strip().lstrip("> "))
        if not match:
            continue
        bank, program = int(match.group(1)), int(match.group(2))
        presets.append({
            "bank": bank,
            "program": program,
            "name": match.group(3),
            "family": family_for(bank, program),
            "bank_msb": (bank >> 7) & 0x7F,
            "bank_lsb": bank & 0x7F,
            "channel": 10 if bank in (120, 128) else None,
        })
    unique = {(item["bank"], item["program"], item["name"]): item for item in presets}
    result = sorted(unique.values(), key=lambda item: (int(item["bank"]), int(item["program"])))
    if not result:
        raise RuntimeError("FluidSynth returned no presets for the SoundFont")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a complete machine-readable SoundFont preset catalog.")
    parser.add_argument(
        "--soundfont", default="assets/soundfonts/GeneralUser-GS.sf2",
        help="path relative to the project root",
    )
    parser.add_argument(
        "--output", default="config/soundfont-catalog.json",
        help="catalog path relative to the project root",
    )
    args = parser.parse_args()
    try:
        soundfont = (ROOT / args.soundfont).resolve()
        if not soundfont.is_file():
            raise FileNotFoundError(soundfont)
        presets = inspect_soundfont(soundfont)
        output = (ROOT / args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        catalog = {
            "schema_version": 1,
            "soundfont": args.soundfont.replace("\\", "/"),
            "preset_count": len(presets),
            "selection": {
                "melodic": "set bank and zero-based program; omit channel or use a non-10 channel",
                "drums": "set channel=10, bank=128 (or 120), and the listed zero-based program",
            },
            "presets": presets,
        }
        output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[OK] {len(presets)} presets -> {output}")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
