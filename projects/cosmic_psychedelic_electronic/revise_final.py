from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def bar(event: dict) -> int:
    return int(event["at"].split(":")[0])


def main() -> None:
    data = json.loads((ROOT/"composition_v1.json").read_text(encoding="utf-8"))
    data["metadata"]["version"] = "final"

    # Clean featured-lead overlap: the displaced answer's F6 at 11:4 runs into
    # the explicit F6 expansion at 11:4. Keep the expansion and omit the duplicate.
    apogee = data["tracks"]["lead"]["sections"]["apogee_bloom"]["events"]
    seen = False
    clean = []
    for event in apogee:
        if event.get("pitch") == "F6" and event.get("at") == "11:4":
            if seen:
                continue
            seen = True
        clean.append(event)
    data["tracks"]["lead"]["sections"]["apogee_bloom"]["events"] = clean
    for event in clean:
        if event.get("pitch") == "F6" and event.get("at") == "11:3.5":
            event["duration"] = 0.44

    # Prism energy reserve: first four bars thin drums and Bell Piano, while bars
    # 5–8 retain the directional drive toward Zero Gravity.
    prism_drums = data["tracks"]["drums"]["sections"]["prism_build"]["events"]
    data["tracks"]["drums"]["sections"]["prism_build"]["events"] = [
        e for e in prism_drums if not (bar(e) <= 4 and e.get("note") in {"kick", "closed_hat", "open_hat"} and float(e["at"].split(":")[1]) not in {1.0, 3.0})
    ]
    prism_bell = data["tracks"]["bell_piano"]["sections"]["prism_build"]["events"]
    data["tracks"]["bell_piano"]["sections"]["prism_build"]["events"] = [e for i,e in enumerate(prism_bell) if bar(e) > 4 or i % 2 == 0]

    # Wormhole bars 9–12: turn the broken pattern into full-drive anchors and
    # reinforce existing bass/chime events without altering the lead motif.
    worm_drums = data["tracks"]["drums"]["sections"]["wormhole"]["events"]
    for b in range(9, 13):
        worm_drums += [
            {"type":"drum","note":"kick","at":f"{b}:2","duration":.13,"velocity":101},
            {"type":"drum","note":"kick","at":f"{b}:3","duration":.13,"velocity":108},
            {"type":"drum","note":"open_hat","at":f"{b}:4.5","duration":.10,"velocity":84},
        ]
    for track_name in ("acid_bass", "chime"):
        for event in data["tracks"][track_name]["sections"]["wormhole"]["events"]:
            if bar(event) >= 9:
                event["velocity"] = min(116, event["velocity"] + (10 if track_name == "acid_bass" else 8))

    # Apogee: ensure final climax has a clear sustained energy advantage while
    # preserving Doctor Solo as sole melodic foreground.
    for track_name in ("lead", "acid_bass", "solar_pad", "night_pad", "drums"):
        for event in data["tracks"][track_name]["sections"]["apogee_bloom"]["events"]:
            event["velocity"] = min(120, event["velocity"] + (7 if track_name in {"lead", "drums"} else 5))

    encoded = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    for name in ("composition_v2.json", "composition_final.json", "composition.json"):
        (ROOT/name).write_text(encoded, encoding="utf-8")


if __name__ == "__main__": main()
