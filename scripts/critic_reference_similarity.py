from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"

NOTE_RE = re.compile(r"^([A-Ga-g])([#b]?)(-?\d+)$")
CHORD_RE = re.compile(r"^([A-Ga-g])([#b]?)(.*)$")
PITCH_CLASS = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}
LEAD_WORDS = {"lead", "melody", "solo", "foreground", "theme", "hook"}


@dataclass(frozen=True)
class Features:
    form: tuple[int, ...]
    harmony: tuple[str, ...]
    intervals: tuple[int, ...]
    rhythm: tuple[tuple[int, int], ...]


def _note_to_midi(value: Any) -> int | None:
    if isinstance(value, int):
        return value if 0 <= value <= 127 else None
    if not isinstance(value, str):
        return None
    match = NOTE_RE.match(value.strip())
    if not match:
        return None
    letter, accidental, octave_text = match.groups()
    pitch_class = PITCH_CLASS[letter.upper()]
    if accidental == "#":
        pitch_class += 1
    elif accidental == "b":
        pitch_class -= 1
    return (int(octave_text) + 1) * 12 + pitch_class


def _at_to_units(value: Any) -> int | None:
    if isinstance(value, (int, float)):
        return round(float(value) * 24)
    if not isinstance(value, str) or ":" not in value:
        return None
    bar_text, beat_text = value.split(":", 1)
    try:
        bar = int(bar_text)
        beat = float(beat_text)
    except ValueError:
        return None
    return round((((bar - 1) * 4) + (beat - 1)) * 24)


def _duration_units(value: Any) -> int:
    try:
        return max(1, round(float(value) * 24))
    except (TypeError, ValueError):
        return 1


def _is_lead_track(name: str, track: dict[str, Any]) -> bool:
    text = " ".join(
        [
            name,
            str(track.get("role", "")),
            str(track.get("instrument", "")),
        ]
    ).lower()
    return any(word in text for word in LEAD_WORDS)


def _section_order(composition: dict[str, Any]) -> list[str]:
    result = []
    for row in composition.get("sections", []):
        if isinstance(row, dict) and row.get("name") is not None:
            result.append(str(row["name"]))
    return result


def _events_from_clip(clip: dict[str, Any]) -> list[dict[str, Any]]:
    events = clip.get("events")
    if isinstance(events, list):
        return [item for item in events if isinstance(item, dict)]
    phrase = clip.get("instrument_phrase")
    if isinstance(phrase, dict):
        for key in ("motif", "notes", "events"):
            value = phrase.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _harmony_from_clip(clip: dict[str, Any]) -> list[str]:
    phrase = clip.get("instrument_phrase")
    if isinstance(phrase, dict):
        harmony = phrase.get("harmony")
        if isinstance(harmony, list):
            chords = []
            for item in harmony:
                if isinstance(item, dict) and item.get("chord") is not None:
                    chords.append(str(item["chord"]))
            if chords:
                return chords
    harmony = clip.get("harmony")
    if isinstance(harmony, list):
        return [str(item.get("chord")) for item in harmony if isinstance(item, dict) and item.get("chord")]
    return []


def _normalize_harmony(chords: Sequence[str]) -> tuple[str, ...]:
    roots: list[tuple[int, str]] = []
    for chord in chords:
        match = CHORD_RE.match(chord.strip())
        if not match:
            roots.append((0, chord.strip().lower()))
            continue
        letter, accidental, suffix = match.groups()
        pitch_class = PITCH_CLASS[letter.upper()]
        if accidental == "#":
            pitch_class += 1
        elif accidental == "b":
            pitch_class -= 1
        roots.append((pitch_class % 12, suffix.strip().lower()))
    if not roots:
        return ()
    origin = roots[0][0]
    return tuple(f"{(root - origin) % 12}:{suffix}" for root, suffix in roots)


def extract_features(composition: dict[str, Any]) -> Features:
    form = tuple(
        int(row.get("bars", 0))
        for row in composition.get("sections", [])
        if isinstance(row, dict) and int(row.get("bars", 0)) > 0
    )
    order = _section_order(composition)
    tracks = composition.get("tracks", {})

    harmony_candidates: list[str] = []
    lead_events: list[tuple[int, int, int]] = []
    section_offsets: dict[str, int] = {}
    cursor = 0
    for row in composition.get("sections", []):
        if not isinstance(row, dict):
            continue
        name = str(row.get("name", ""))
        section_offsets[name] = cursor
        cursor += int(row.get("bars", 0)) * 4 * 24

    if isinstance(tracks, dict):
        for track_name, track_value in tracks.items():
            if not isinstance(track_value, dict):
                continue
            sections = track_value.get("sections", {})
            if not isinstance(sections, dict):
                continue
            for section_name in order or list(sections):
                clip = sections.get(section_name)
                if not isinstance(clip, dict):
                    continue
                if not harmony_candidates:
                    harmony_candidates.extend(_harmony_from_clip(clip))
                if not _is_lead_track(str(track_name), track_value):
                    continue
                offset = section_offsets.get(section_name, 0)
                for event in _events_from_clip(clip):
                    pitch = _note_to_midi(event.get("pitch"))
                    onset = _at_to_units(event.get("at", 0))
                    if pitch is None or onset is None:
                        continue
                    lead_events.append(
                        (offset + onset, pitch, _duration_units(event.get("duration", 0.25)))
                    )

    lead_events.sort(key=lambda item: (item[0], item[1], item[2]))
    pitches = [item[1] for item in lead_events]
    intervals = tuple(b - a for a, b in zip(pitches, pitches[1:]))
    rhythm = tuple(
        (max(0, nxt[0] - cur[0]), cur[2])
        for cur, nxt in zip(lead_events, lead_events[1:])
    )
    return Features(
        form=form,
        harmony=_normalize_harmony(harmony_candidates),
        intervals=intervals,
        rhythm=rhythm,
    )


def _ngrams(values: Sequence[Any], size: int) -> Counter[tuple[Any, ...]]:
    if len(values) < size:
        return Counter()
    return Counter(tuple(values[index : index + size]) for index in range(len(values) - size + 1))


def _multiset_jaccard(a: Counter[Any], b: Counter[Any]) -> float:
    if not a and not b:
        return 0.0
    keys = set(a) | set(b)
    intersection = sum(min(a[key], b[key]) for key in keys)
    union = sum(max(a[key], b[key]) for key in keys)
    return intersection / union if union else 0.0


def _sequence_overlap(a: Sequence[Any], b: Sequence[Any]) -> float:
    if not a or not b:
        return 0.0
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    if len(shorter) == len(longer):
        return sum(x == y for x, y in zip(shorter, longer)) / len(shorter)
    windows = [longer[index : index + len(shorter)] for index in range(len(longer) - len(shorter) + 1)]
    return max(sum(x == y for x, y in zip(shorter, window)) / len(shorter) for window in windows)


def compare(target: Features, reference: Features) -> dict[str, float]:
    form = _sequence_overlap(target.form, reference.form)
    harmony = _multiset_jaccard(_ngrams(target.harmony, 3), _ngrams(reference.harmony, 3))
    intervals = _multiset_jaccard(_ngrams(target.intervals, 4), _ngrams(reference.intervals, 4))
    rhythm = _multiset_jaccard(_ngrams(target.rhythm, 4), _ngrams(reference.rhythm, 4))
    weighted = form * 0.20 + harmony * 0.25 + intervals * 0.30 + rhythm * 0.25
    return {
        "form": round(form, 4),
        "harmony": round(harmony, 4),
        "lead_intervals": round(intervals, 4),
        "lead_rhythm": round(rhythm, 4),
        "weighted": round(weighted, 4),
    }


def _load_project(name: str) -> dict[str, Any]:
    path = PROJECTS / name / "composition.json"
    if not path.is_file():
        raise FileNotFoundError(f"composition not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _discover_references(target: str) -> list[str]:
    result = []
    for path in sorted(PROJECTS.glob("*/composition.json")):
        if path.parent.name != target:
            result.append(path.parent.name)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect likely template reuse against repository project compositions."
    )
    parser.add_argument("song", help="target project under projects/")
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="reference project to compare; repeatable. Without it, scan all projects.",
    )
    parser.add_argument("--write", action="store_true", help="write reference-similarity-report.json")
    parser.add_argument("--warn", type=float, default=0.58, help="weighted warning threshold")
    args = parser.parse_args()

    try:
        target = extract_features(_load_project(args.song))
        references = args.reference or _discover_references(args.song)
        rows = []
        for name in references:
            try:
                scores = compare(target, extract_features(_load_project(name)))
            except (FileNotFoundError, json.JSONDecodeError, ValueError):
                continue
            rows.append({"reference": name, **scores})
        rows.sort(key=lambda row: row["weighted"], reverse=True)
        report = {
            "schema": "music-agent-reference-similarity-report",
            "schema_version": 1,
            "target": args.song,
            "warning_threshold": args.warn,
            "comparisons": rows,
            "warnings": [
                row for row in rows if float(row["weighted"]) >= args.warn
            ],
            "note": (
                "This is a template-reuse heuristic, not a copyright or musical-quality judgment. "
                "Review high scores in musical context."
            ),
        }
        if args.write:
            output = PROJECTS / args.song / "reference-similarity-report.json"
            output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    if not rows:
        print("[OK] no comparable reference projects found")
        return 0

    print("reference                         total   form harmony intervals rhythm")
    for row in rows[:10]:
        marker = "WARN" if row["weighted"] >= args.warn else "    "
        print(
            f"{marker} {row['reference'][:28]:28} "
            f"{row['weighted']:.3f}  {row['form']:.3f}  {row['harmony']:.3f}   "
            f"{row['lead_intervals']:.3f}    {row['lead_rhythm']:.3f}"
        )
    if report["warnings"]:
        print(
            "[WARN] high similarity is evidence to inspect form/harmony/motif reuse; "
            "do not fix it by randomizing notes."
        )
    else:
        print("[OK] no comparison exceeded the warning threshold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
