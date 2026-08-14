from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.skills_v2.acoustic_strumming import (
    analyze_midi,
    generate_demo_midi,
    list_candidates,
    write_analysis,
)


def _print_candidates(midi_path: Path) -> None:
    rows = list_candidates(midi_path)
    if not rows:
        print("[WARN] no playable note candidates found")
        return
    print("track channel programs notes chord-ratio score")
    for row in rows:
        print(
            f"{row['track']:>5} {row['channel']:>7} "
            f"{str(row['programs']):>12} {row['note_count']:>5} "
            f"{row['chord_note_ratio']:>11.4f} "
            f"{row['selection_score']:>5.2f}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Extract a tempo/key/program-invariant acoustic "
            "strumming model from MIDI."
        )
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    list_parser = subparsers.add_parser(
        "list",
        help="list candidate MIDI track/channels",
    )
    list_parser.add_argument("midi", type=Path)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help=(
            "analyze one acoustic-guitar track and write a study package"
        ),
    )
    analyze_parser.add_argument("midi", type=Path)
    analyze_parser.add_argument(
        "study",
        help="directory name under studies/",
    )
    analyze_parser.add_argument("--track", type=int)
    analyze_parser.add_argument("--channel", type=int)
    analyze_parser.add_argument(
        "--cluster-window-beats",
        type=float,
        default=0.12,
        help=(
            "maximum onset span grouped as one stroke, "
            "in quarter-note beats"
        ),
    )
    analyze_parser.add_argument(
        "--no-demo",
        action="store_true",
        help="skip synthetic four-bar demo generation",
    )

    generate_parser = subparsers.add_parser(
        "generate",
        help="generate a synthetic MIDI demo from a model.json",
    )
    generate_parser.add_argument("model", type=Path)
    generate_parser.add_argument("output", type=Path)
    generate_parser.add_argument("--tempo", type=float, default=104.0)
    generate_parser.add_argument("--program", type=int, default=25)

    args = parser.parse_args()
    if args.command == "list":
        _print_candidates(args.midi.expanduser().resolve())
        return 0

    if args.command == "analyze":
        midi_path = args.midi.expanduser().resolve()
        if not midi_path.is_file():
            print(
                f"[FAIL] MIDI file not found: {midi_path}",
                file=sys.stderr,
            )
            return 1
        study_dir = ROOT / "studies" / args.study
        try:
            result = analyze_midi(
                midi_path,
                track_index=args.track,
                channel=args.channel,
                cluster_window_beats=args.cluster_window_beats,
            )
            write_analysis(result, study_dir)
            if not args.no_demo:
                generate_demo_midi(
                    result["model"],
                    study_dir / "synthetic_demo.mid",
                )
        except Exception as error:
            print(f"[FAIL] {error}", file=sys.stderr)
            return 1
        model = result["model"]
        print(f"[OK] study: {study_dir}")
        print(
            "[OK] selected track/channel: "
            f"{result['selection']['track']}/"
            f"{result['selection']['channel']}"
        )
        print(
            f"[OK] stroke candidates: "
            f"{model['evidence']['stroke_count']}"
        )
        print(f"[OK] attack mask: {model['attack_mask']}")
        print(
            "[OK] alternating direction confidence: "
            f"{model['motion']['alternate_direction_confidence']:.3f}"
        )
        print(f"[OK] model: {study_dir / 'model.json'}")
        if not args.no_demo:
            print(
                f"[OK] demo: {study_dir / 'synthetic_demo.mid'}"
            )
        return 0

    model_path = args.model.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    try:
        model = json.loads(
            model_path.read_text(encoding="utf-8")
        )
        generate_demo_midi(
            model,
            output_path,
            tempo_bpm=args.tempo,
            program=args.program,
        )
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1
    print(f"[OK] generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
