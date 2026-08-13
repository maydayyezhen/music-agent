from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def bar_of(event: dict) -> int:
    return int(event["at"].split(":")[0])


def main() -> None:
    data = json.loads((ROOT / "composition_v1.json").read_text(encoding="utf-8"))
    data["metadata"]["version"] = "final"

    # Piano overlap at absolute bar 66 comes from Outro bar 2: held G4 from bar 1
    # intersects the Em voicing. Shorten the explicit G4 hook landing.
    outro_piano = data["tracks"]["piano"]["sections"]["outro"]["events"]
    for event in outro_piano:
        if event.get("type") == "note" and event.get("pitch") == "G4" and event.get("at") == "1:4":
            event["duration"] = 0.82

    # Bridge: bass waits through bars 1–2; guitar only appears in bars 7–8.
    bridge_bass = data["tracks"]["bass"]["sections"]["bridge"]["events"]
    data["tracks"]["bass"]["sections"]["bridge"]["events"] = [e for e in bridge_bass if bar_of(e) >= 3]
    bridge_guitar = data["tracks"]["guitar"]["sections"]["bridge"]["events"]
    data["tracks"]["guitar"]["sections"]["bridge"]["events"] = [e for e in bridge_guitar if bar_of(e) >= 7]

    # Pre breath: remove hats and extra kicks after beat 4.25 while retaining the
    # last tom/snare pickup. This creates an audible pocket before each chorus.
    for section in ("pre_1", "pre_2"):
        events = data["tracks"]["drums"]["sections"][section]["events"]
        filtered = []
        for event in events:
            bar_text, beat_text = event["at"].split(":")
            if int(bar_text) == 4 and float(beat_text) >= 4.25 and event.get("note") in {"closed_hat", "open_hat", "kick"}:
                continue
            filtered.append(event)
        data["tracks"]["drums"]["sections"][section]["events"] = filtered

    # Final chorus gets a real last-act lift without invading the topline:
    # accent rhythm foundation and add high string responses only on phrase tails.
    for track_name in ("bass", "guitar"):
        events = data["tracks"][track_name]["sections"]["final_chorus"]["events"]
        for event in events:
            if bar_of(event) >= 9:
                event["velocity"] = min(118, event["velocity"] + 9)
            elif bar_of(event) in (1, 5):
                event["velocity"] = min(116, event["velocity"] + 5)
    string_events = data["tracks"]["strings"]["sections"]["final_chorus"]["events"]
    string_events += [
        {"type": "note", "pitch": "G5", "at": "9:4", "duration": 0.72, "velocity": 85},
        {"type": "note", "pitch": "A5", "at": "10:4", "duration": 0.72, "velocity": 88},
        {"type": "note", "pitch": "B5", "at": "11:4", "duration": 0.72, "velocity": 92},
        {"type": "note", "pitch": "D6", "at": "12:3", "duration": 1.65, "velocity": 95},
    ]
    final_drums = data["tracks"]["drums"]["sections"]["final_chorus"]["events"]
    for event in final_drums:
        if bar_of(event) >= 9 and event.get("note") in {"kick", "snare", "open_hat", "crash"}:
            event["velocity"] = min(118, event["velocity"] + 7)

    encoded = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (ROOT / "composition_v2.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition_final.json").write_text(encoded, encoding="utf-8")
    (ROOT / "composition.json").write_text(encoded, encoding="utf-8")


if __name__ == "__main__":
    main()
