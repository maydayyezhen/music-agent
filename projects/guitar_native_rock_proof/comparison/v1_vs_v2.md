# V1 versus V2

| Measure | V1 | V2 | Interpretation |
|---|---:|---:|---|
| Composition SHA-256 | `D9D925...07706` | `D9D925...07706` | exact same song data |
| Rhythm-section MIDI | `F0E422...` | `F0E422...` | exact same accompaniment |
| Lead notes | 744 | 744 | melody was not replaced |
| Solo notes | 301 | 301 | no density trick |
| Solo active bars | 32/32 | 32/32 | fully continuous in both |
| Solo phrase islands (>0.5 beat) | 1 | 1 | no lick collage |
| Solo rests >1 beat | 0 | 0 | no vocal breathing reset |
| Solo max internal gap | 0.090 beat | 0.090 beat | unchanged continuity |
| Solo density by eight bars | 57/80/86/78 | 57/80/86/78 | medium -> denser -> peak -> release |
| Highest note | E6, Solo bar 26 | E6, Solo bar 26 | delayed climax preserved |
| Different-pitch overlap | 0 | 0 | strictly monophonic |
| Unsafe pitch-wheel messages | 0 | 0 | bend/slide channel-safe |
| Recognized slide-in gestures | 0 | 14 | planned position shifts now audible |

V2 is more like one complete guitar performance because the continuous melodic skeleton now carries audible hand-position transitions between its established shapes. It does not become less fragmented by adding notes—the V1 melody was already continuous. It becomes more guitar-native by preserving physical fretboard intent at the exact transition points.

V2 still uses repeated cells and sequences, but it is not a chain of unrelated preset licks: exact identical four-bar-window repetition is 1, every Solo block derives from the core motif, the peak is delayed, and the final descent enters the returned theme.

The project modification was necessary only for realization fidelity. No Rhythm Guitar, Bass or Drum generator was changed because V1 did not expose a blocking defect there. No validation threshold was changed. No attempted change was reverted: the single targeted path passed 34 regression tests and produced the expected audible/MIDI delta.
