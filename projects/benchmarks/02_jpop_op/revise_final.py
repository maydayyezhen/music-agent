from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def is_at(event: dict, positions: set[str], pitch: str | None = None) -> bool:
    return event.get("at") in positions and (pitch is None or event.get("pitch") == pitch)


def main() -> None:
    path = ROOT / "composition_v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["metadata"]["version"] = "final"

    # 1) Intro: let the piano/guitar motif own the first two bars. Bass enters in bar 3;
    # drums enter with a light bar 3 and the original transition fill in bar 4.
    bass_intro = data["tracks"]["bass"]["sections"]["intro"]["events"]
    data["tracks"]["bass"]["sections"]["intro"]["events"] = [
        event for event in bass_intro if int(event["at"].split(":")[0]) >= 3
    ]
    drums_intro = data["tracks"]["drums"]["sections"]["intro"]["events"]
    data["tracks"]["drums"]["sections"]["intro"]["events"] = [
        event for event in drums_intro
        if int(event["at"].split(":")[0]) >= 3
        and not (event["at"].startswith("3:") and event.get("note") in {"snare", "open_hat"})
    ]

    # 2) Remove piano overlaps. Intro accompaniment repeats A3 while its chord is held;
    # shorten the held upper chords to leave clean space for the explicit arpeggio.
    piano_intro = data["tracks"]["piano"]["sections"]["intro"]["events"]
    for event in piano_intro:
        if event.get("type") == "chord" and event.get("at", "").endswith(":1.04"):
            event["duration"] = 1.25

    # The verse E4 pickup collided with the held A chord; omit that doubled pickup.
    piano_verse = data["tracks"]["piano"]["sections"]["verse"]["events"]
    data["tracks"]["piano"]["sections"]["verse"]["events"] = [
        event for event in piano_verse if not is_at(event, {"2:3.5"}, "E4")
    ]

    # Outro Bm chord releases before its explicit D4 melodic answer.
    piano_outro = data["tracks"]["piano"]["sections"]["outro"]["events"]
    for event in piano_outro:
        if event.get("type") == "chord" and event.get("at") == "9:1":
            event["duration"] = 1.45

    # 3) Remove string duplicated top notes in Pre: the counterline is the foreground,
    # so remove the same pitch from each sustained background chord.
    strings_pre = data["tracks"]["strings"]["sections"]["pre_chorus"]["events"]
    top_at_bar = {}
    for event in strings_pre:
        if event.get("type") == "note" and event.get("at", "").endswith(":3"):
            top_at_bar[event["at"].split(":")[0]] = event["pitch"]
    for event in strings_pre:
        if event.get("type") == "chord":
            bar = event["at"].split(":")[0]
            duplicate = top_at_bar.get(bar)
            if duplicate in event["pitches"]:
                event["pitches"] = [pitch for pitch in event["pitches"] if pitch != duplicate]

    # 4) Outro guitar is an explicit 12-bar clip with material only in bars 1–8;
    # a 12-bar loop prevents automatic repetition into the final cadence.
    guitar_outro = data["tracks"]["guitar"]["sections"]["outro"]
    guitar_outro["loop_bars"] = 12

    # 5) Outro drums: same technique, first 8 bars only, with a smaller final fill.
    drum_outro = data["tracks"]["drums"]["sections"]["outro"]
    drum_outro["loop_bars"] = 12
    drum_outro["events"] = [
        event for event in drum_outro["events"]
        if not (event["at"].startswith("8:") and event.get("note") in {"high_tom", "mid_tom"})
    ]

    # 6) Outro bass: keep forward motion for 8 bars, then half-note cadence movement.
    bass_outro = data["tracks"]["bass"]["sections"]["outro"]
    bass_outro["events"] = [
        event for event in bass_outro["events"] if int(event["at"].split(":")[0]) <= 8
    ] + [
        {"type": "note", "pitch": "B1", "at": "9:1", "duration": 1.8, "velocity": 72},
        {"type": "note", "pitch": "F#2", "at": "9:3", "duration": 1.7, "velocity": 68},
        {"type": "note", "pitch": "G1", "at": "10:1", "duration": 1.8, "velocity": 70},
        {"type": "note", "pitch": "D2", "at": "10:3", "duration": 1.7, "velocity": 67},
        {"type": "note", "pitch": "E2", "at": "11:1", "duration": 1.8, "velocity": 69},
        {"type": "note", "pitch": "A1", "at": "11:3", "duration": 1.7, "velocity": 72},
        {"type": "note", "pitch": "D2", "at": "12:1", "duration": 3.65, "velocity": 74},
    ]

    encoded = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "composition_v2.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition_final.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition.json").write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
