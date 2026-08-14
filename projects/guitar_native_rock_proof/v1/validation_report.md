# V1 validation report

V1 is a real FluidSynth render of the current stable project before the targeted code change. Duration is 217.172 s. Mix peak is -10.61 dBFS and RMS is -27.10 dBFS; all five stems are non-silent and there is no clipping.

Lead Guitar contains 744 notes and sounds in 91/104 bars. The only consecutive blank region is the intentional eight-bar Bridge (global bars 41-48). Theme A and Theme B do not auto-reset at four-bar boundaries: their measured boundary gaps range from 0.010 to 0.090 beats.

Main Solo (global bars 49-80) contains 301 notes across all 32 bars. Continuous span is 127.996 beats; maximum internal gap is 0.090 beats; phrase islands at the explicit >0.5-beat rule: 1; rests over one beat: 0. Density by eight-bar group is 57 / 80 / 86 / 78 notes. The highest written note, E6 (MIDI 88), occurs at global bar 74 / Solo bar 26. This is a delayed peak, not an early climax.

MIDI safety: different-pitch overlaps 0; unsafe pitch-wheel messages 0. V1 contains 7 expressive pitch-wheel gestures (bend/vibrato) but **0 slide-in gestures**, although the composition explicitly declares position-changing slides. Concrete failures: the slides authored at global bars 13, 17, 21, 25, 29, 33, 37, 57, 65, 73, 77, 81, 87 and 93 are lost before MIDI output. Inspection also shows global bar 57's planned G4 at string 3/fret 12 being reassigned to string 5/fret 3.

The instrument critic reports repeated-bar warnings in Solo/Final/Outro and the complexity critic reports too little breath. These are contextual false positives here: motif sequence and repeated-note propulsion are intentional, exact four-bar lick repetition is 1, and the user explicitly prohibited vocal-style periodic breathing. No validator threshold was changed to silence them.
