# Final Validation — When the Horizon Answers

## Build identity

- B minor, 108 BPM, 4/4, 96 bars.
- Final WAV duration: 216.333 seconds (3:36.3), stereo 44.1 kHz.
- Local rendering only: GeneralUser GS SF2 through FluidSynth.
- `composition.json` is byte-identical to `composition_final.json`.
- V1 and final SHA-256 hashes differ, proving that the revision reached audio output.

## Structure and energy

| Section | Bars | Energy | Measured events/bar | Active tracks |
|---|---:|---:|---:|---:|
| Intro | 8 | 0.28 | 28.38 | 6 |
| Verse 1 | 12 | 0.42 | 25.00 | 5 |
| Pre-Chorus | 8 | 0.61 | 40.62 | 6 |
| Chorus 1 | 16 | 0.84 | 44.88 | 6 |
| Verse 2 | 12 | 0.48 | 25.00 | 5 |
| Bridge Void | 8 | 0.36 | 24.00 | 5 |
| Bridge Build | 8 | 0.76 | 45.25 | 5 |
| Final Chorus | 16 | 1.00 | 46.62 | 6 |
| Outro | 8 | 0.34 | 27.25 | 6 |

The verse-to-chorus speed contrast is explicit: verse rhythm guitar uses quarter-note muted actions with omissions; chorus uses open eighth-note power chords and the chorus drum compiler's eighth hats/additional kicks.

## Long-form Lead Guitar

All seven active Lead Guitar sections use `phrase_generation_mode: long_form`. Every validator row has:

- independent resets: 0;
- strong cadences: 1, only at the final relationship;
- motif developments: 3;
- identical short-phrase repetitions: 0;
- breath state resets: 0;
- complete section harmony visible to the planner.

Cross-bar connections are 10–16 per section. Chorus 1 reaches its planned D6 peak in bar 12. Final Chorus delays a higher E6 peak until bar 14, contains seven distinct motif operations, and has 16 cross-bar connections. Long-form critic result: **0 error, 0 warning**.

## Sixteen-bar lead-free relay

There is no Lead Guitar clip for either `bridge_void` or `bridge_build`. MIDI evidence confirms exactly 0 Lead Guitar note events across all 16 bars.

Other players carry and transform the narrative:

| Player | Bridge Void | Build first 4 bars | Build last 4 bars | Evidence of development |
|---|---:|---:|---:|---|
| Rhythm Guitar | 48 events | 69 | 90 | explicit density acceleration and changed pitch set |
| Bass | 28 events | 14 | 14 | median pitch rises 38 -> 44 in Build, with 12 then 8 unique pitches |
| Organ | 30 events | 22 | 19 | median register rises 62 -> 71 -> 74 and line material changes |
| Drums | 78 events | 57 | 58 | restrained groove changes to chorus drive; fill vocabulary expands |
| Strings | 8 events | 10 | 9 | median register rises 67 -> 69 -> 70 with nine-pitch Build material |

Thus at least rhythm guitar, bass, organ, drums and strings have independent changing material; none is a static duplicate of Lead Guitar.

## Chorus and bridge variation

- Chorus 1 lead peak: bar 12, D6. Final Chorus: bar 14, E6.
- Final lead climax adds `change_ending`; resolution adds `transpose_down`; the core cell is extended through the six-bar climax node.
- Final rhythm guitar removes fewer attacks than Chorus 1 after the midpoint.
- Final strings move from the earlier chorus register into MIDI 60–86.
- Bridge Void and Bridge Build use different rhythms, register, drum language and event density; the latter is the actual pre-impact acceleration.

## Critics

- Instrument critic: 0 error, 0 warning, 8 informational register observations.
- Long-form critic: 0 error, 0 warning.
- Complexity critic: 0 warning.
- Continuity critic: 0 warning.

## MIDI and audio

All six standalone MIDI files pass with 0 same-pitch overlaps, 0 stuck notes, 0 unmatched note-offs and 0 tiny notes. Counts: Lead 144, Rhythm Guitar 1431, Bass 336, Drums 1115, Organ 216, Strings 146.

All six stems are stereo, non-silent and have 0 clipped samples. Final mix peak is -11.18 dBFS with 0 clipped samples. The low peak is intentional headroom, not normalization failure.

