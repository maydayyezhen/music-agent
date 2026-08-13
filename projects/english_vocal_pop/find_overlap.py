from pathlib import Path
import mido

root = Path(__file__).resolve().parent
for path in sorted((root / "tracks").glob("*.mid")):
    midi = mido.MidiFile(path)
    for track in midi.tracks:
        tick = 0
        active = {}
        for msg in track:
            tick += msg.time
            if msg.type == "note_on" and msg.velocity:
                key = (msg.channel, msg.note)
                if key in active:
                    print(path.stem, "pitch", msg.note, "bar", tick / midi.ticks_per_beat / 4 + 1)
                active[key] = tick
            elif msg.type in ("note_off", "note_on"):
                active.pop((msg.channel, msg.note), None)
