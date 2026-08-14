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
from src.skills_v2.strumming_observability import (
    annotate_direction_observability,
    apply_alternate_generation_assumption,
    can_generate_directional_demo,
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


def _append_observability_notes(result: dict, study_dir: Path) -> None:
    direction = result["observability"]["direction"]
    path = study_dir / "observations.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n## Direction observability\n\n")
        handle.write(f"- Status: `{direction['status']}`\n")
        handle.write(
            f"- Multi-note strokes: {direction['multi_note_strokes']}\n"
        )
        handle.write(
            "- Measurable direction strokes: "
            f"{direction['measurable_direction_strokes']}\n"
        )
        handle.write(
            f"- Zero-spread ratio: {direction['zero_spread_ratio']}\n"
        )
        handle.write(
            "- Median / maximum spread in beats: "
            f"{direction['median_spread_beats']} / "
            f"{direction['maximum_spread_beats']}\n"
        )
        if direction["unlearned_fields"]:
            handle.write(
                "- Not learned from this source: "
                + ", ".join(direction["unlearned_fields"])
                + "\n"
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
    analyze_parser.add_argument(
        "--assume-alternate-demo",
        action="store_true",
        help=(
            "when direction is unobservable, generate a demo under an "
            "explicit D/U assumption; the assumption is not written into "
            "the learned model"
        ),
    )

    generate_parser = subparsers.add_parser(
        "generate",
        help="generate a synthetic MIDI demo from a model.json",
    )
    generate_parser.add_argument("model", type=Path)
    generate_parser.add_argument("output", type=Path)
    generate_parser.add_argument("--tempo", type=float, default=104.0)
    generate_parser.add_argument("--program", type=int, default=25)
    generate_parser.add_argument(
        "--assume-alternate",
        action="store_true",
        help=(
            "explicitly impose D/U alternation when the model reports "
            "unobservable direction"
        ),
    )

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
        demo_written = False
        try:
            result = analyze_midi(
                midi_path,
                track_index=args.track,
                channel=args.channel,
                cluster_window_beats=args.cluster_window_beats,
            )
            result = annotate_direction_observability(result)
            write_analysis(result, study_dir)
            _append_observability_notes(result, study_dir)
            if not args.no_demo:
                demo_model = result["model"]
                if not can_generate_directional_demo(demo_model):
                    if args.assume_alternate_demo:
                        demo_model = apply_alternate_generation_assumption(
                            demo_model
                        )
                    else:
                        demo_model = None
                if demo_model is not None:
                    generate_demo_midi(
                        demo_model,
                        study_dir / "synthetic_demo.mid",
                    )
                    demo_written = True
        except Exception as error:
            print(f"[FAIL] {error}", file=sys.stderr)
            return 1
        model = result["model"]
        direction = result["observability"]["direction"]
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
            "[OK] direction observability: "
            f"{direction['status']}"
        )
        print(
            "[OK] measurable direction strokes: "
            f"{direction['measurable_direction_strokes']}/"
            f"{direction['multi_note_strokes']}"
        )
        if direction["status"] == "observable":
            print(
                "[OK] alternating direction confidence: "
                f"{model['motion']['alternate_direction_confidence']:.3f}"
            )
        else:
            print(
                "[WARN] down/up direction was not learned from this MIDI"
            )
        print(f"[OK] model: {study_dir / 'model.json'}")
        if demo_written:
            suffix = (
                " (explicit alternate-hand assumption)"
                if args.assume_alternate_demo
                and not can_generate_directional_demo(result["model"])
                else ""
            )
            print(
                f"[OK] demo: {study_dir / 'synthetic_demo.mid'}{suffix}"
            )
        elif not args.no_demo:
            print(
                "[WARN] demo skipped because source direction is "
                "unobservable; pass --assume-alternate-demo to make an "
                "explicit hypothesis demo"
            )
        return 0

    model_path = args.model.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    try:
        model = json.loads(
            model_path.read_text(encoding="utf-8")
        )
        if not can_generate_directional_demo(model):
            if not args.assume_alternate:
                raise ValueError(
                    "model does not contain observable down/up direction; "
                    "pass --assume-alternate to generate an explicitly "
                    "hypothetical D/U demo"
                )
            model = apply_alternate_generation_assumption(model)
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
