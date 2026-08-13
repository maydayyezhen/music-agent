from __future__ import annotations

from pathlib import Path
import mido

ROOT = Path(__file__).resolve().parent

for path in sorted((ROOT / "tracks").glob("*.mid")):
    midi = mido.MidiFile(path)
    print(f"[{path.stem}]")
    for track in midi.tracks:
        tick = 0
        active: dict[tuple[int, int], int] = {}
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity:
                key = (msg.channel, msg.note)
                if key in active:
                    bar = tick / midi.ticks_per_beat / 4 + 1
                    print(f"overlap pitch={msg.note} bar={bar:.3f} previous_start={active[key]}")
                active[key] = tick
            elif msg.type in ("note_off", "note_on"):
                active.pop((msg.channel, msg.note), None)
