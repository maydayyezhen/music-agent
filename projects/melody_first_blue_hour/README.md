# Blue Hour Signal

Melody-first composition test for the V2 Music Agent.

## Intent

The arrangement is deliberately secondary. The lead melody is the test target:

- one small F#-A-B germ;
- recurrence before new material;
- A -> A' controlled variation;
- a lower, longer-note B section for contrast;
- a higher-register hook with the main climax on F#6;
- an outro that recalls the opening material.

## Setup

- 112 BPM
- 4/4
- D major with B minor color
- 40 bars, about 85.7 seconds
- lead: GM square lead
- support: electric piano, finger bass, light drums

The bass uses the active `smooth-melodic-support-bass` idea only as a behavior constraint: anchor + compact connector + breathing room. No source melody or reference arrangement is copied.

## Build

From the repository root:

```powershell
python projects/melody_first_blue_hour/build.py
```

Generated files:

```text
projects/melody_first_blue_hour/composition.generated.json
projects/melody_first_blue_hour/tracks/lead_square.mid
projects/melody_first_blue_hour/tracks/electric_piano.mid
projects/melody_first_blue_hour/tracks/finger_bass.mid
projects/melody_first_blue_hour/tracks/drums.mid
projects/melody_first_blue_hour/output/full_song.mid
projects/melody_first_blue_hour/reports/melody_design.json
```

For judging the writing itself, listen to `tracks/lead_square.mid` first, then `output/full_song.mid`.
