from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
v1 = json.loads((ROOT / "composition_v1.json").read_text(encoding="utf-8"))
final = deepcopy(v1)
final["metadata"]["composer_note"] = (
    "Final revision: riff-first British/alternative rock. Sparse cold-open rhythm section, "
    "offbeat right-guitar verse chops, shortened chorus support, clearer final lift."
)

tracks = final["tracks"]

# Revision 0: remove the V1 duplicate kick layered at the final crash/downbeat.
outro_drum_events = tracks["drums"]["sections"]["outro"]["events"]
seen_drum_hits: set[tuple[str, str]] = set()
clean_outro: list[dict] = []
for event in outro_drum_events:
    hit = (str(event["note"]), str(event["at"]))
    if hit in seen_drum_hits:
        continue
    seen_drum_hits.add(hit)
    clean_outro.append(event)
tracks["drums"]["sections"]["outro"]["events"] = clean_outro

# Revision 1: expose the core riff for two bars, then let bass/drums burst in.
tracks["bass"]["sections"]["cold_open"] = {
    "loop_bars": 4,
    "events": [
        {"type": "note", "pitch": "E2", "at": "3:1", "duration": 0.7, "velocity": 104},
        {"type": "note", "pitch": "B2", "at": "3:2", "duration": 0.35, "velocity": 92},
        {"type": "note", "pitch": "D3", "at": "3:2.75", "duration": 0.35, "velocity": 89},
        {"type": "note", "pitch": "E3", "at": "3:3.5", "duration": 0.45, "velocity": 99},
        {"type": "note", "pitch": "G2", "at": "4:1", "duration": 0.7, "velocity": 103},
        {"type": "note", "pitch": "D3", "at": "4:2", "duration": 0.35, "velocity": 91},
        {"type": "note", "pitch": "F#2", "at": "4:3", "duration": 0.35, "velocity": 88},
        {"type": "note", "pitch": "G2", "at": "4:3.5", "duration": 0.6, "velocity": 98},
        {"type": "note", "pitch": "D#2", "at": "4:4.5", "duration": 0.25, "velocity": 91},
    ],
}

def d(note: str, at: str, velocity: int, duration: float = 0.12) -> dict:
    return {"type": "drum", "note": note, "at": at, "duration": duration, "velocity": velocity}

cold_drums = [d("side_stick", "2:4", 65)]
for bar in (3, 4):
    for i in range(8):
        beat = 1 + i * 0.5
        cold_drums.append(d("closed_hat", f"{bar}:{beat:g}", 78 + (8 if i % 2 == 0 else -7)))
    cold_drums += [d("kick", f"{bar}:1", 112), d("kick", f"{bar}:2.75", 98), d("kick", f"{bar}:3.5", 101)]
    cold_drums += [d("snare", f"{bar}:2", 105), d("snare", f"{bar}:4", 109)]
cold_drums += [d("low_tom", "4:3", 94), d("mid_tom", "4:3.5", 101), d("high_tom", "4:4", 109), d("snare", "4:4.5", 117)]
tracks["drums"]["sections"]["cold_open"] = {"loop_bars": 4, "events": cold_drums}

# Revision 2: replace the V1 right-guitar quarter-note wall with clipped offbeat answers.
verse_roots = [(["E4", "B4"], 1), (["G4", "D5"], 2), (["A4", "E5"], 3), (["G4", "D5"], 4)]
verse_events = []
for pitches, bar in verse_roots:
    for beat, vel in ((1.5, 87), (2.5, 91), (4.0, 94)):
        verse_events.append({"type": "chord", "pitches": pitches, "at": f"{bar}:{beat:g}", "duration": 0.28, "velocity": vel + (3 if bar == 3 else 0)})
tracks["guitar_r"]["sections"]["verse"] = {"loop_bars": 4, "events": verse_events}

# Revision 3: shorten chorus support so the left-hand riff remains the foreground hook.
for section_name in ("chorus", "final_chorus"):
    for event in tracks["guitar_r"]["sections"][section_name]["events"]:
        event["duration"] = 0.92
        event["velocity"] = max(1, event["velocity"] - 3)

# Revision 4: make the final chorus a true lift with two small bass anticipations.
final_bass = deepcopy(tracks["bass"]["sections"]["chorus"])
final_bass["events"] += [
    {"type": "note", "pitch": "C#3", "at": "2:4.75", "duration": 0.18, "velocity": 97},
    {"type": "note", "pitch": "D#3", "at": "4:4.75", "duration": 0.18, "velocity": 101},
]
tracks["bass"]["sections"]["final_chorus"] = final_bass

(ROOT / "composition_final.json").write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "composition.json").write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
