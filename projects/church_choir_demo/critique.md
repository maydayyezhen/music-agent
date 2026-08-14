# v1 Critique and Revision Decisions

The first complete MIDI → GeneralUser GS → stem → mix render was inspected rather than accepted as a draft artifact. `output/v1.wav` is 134.43 seconds, has a peak of only -22.24 dBFS and RMS -38.21 dBFS, and contains no clipped samples. All six stems are non-silent. MIDI inspection found 567 notes across the six standalone tracks, with zero same-pitch overlaps, zero stuck notes and zero tiny notes under 24 ticks.

## Concrete findings

1. **The v1 mix is unnecessarily quiet.** The measured mix peak is -22.24 dBFS even though the render is clean. The pipe organ stem peaks at -15.83 dBFS and therefore has ample headroom. Revision: raise FluidSynth gain from 0.58 to 1.0 and lift track mix gains while preserving the theme-over-support hierarchy; retain a -1 dBFS master ceiling.
2. **The strings read as separated swells instead of a connected counterline.** The continuity critic flagged `line_is_disconnected` in Procession, Sanctus, Great Amen and Benediction. Revision: lengthen alternating string gestures to meet or overlap the following onset, while keeping their beat-1/beat-1.5 identity distinct from the choir theme.
3. **The Great Amen needs a clearer earned summit rather than merely sustained density.** v1 measured 9.80 events/bar with all six roles active. Revision: reserve the theme's G5 arrival for bar 8, raise the organ top voice through C–A–D, and add a three-note string ascent into the cadence. The change is registral and directional, not a blanket note-density increase.
4. **Bells are too regularly distributed for architectural punctuation.** v1 contains 21 bell notes, making the point layer feel like a recurring marker rather than distant tower tolls. Revision: reduce bells to 13 attacks, retaining entrances, the Great Amen portal/climax, and the final blessing.
5. **The opening Invocation is more layered than the energy map implies.** Inner choir begins immediately at 11.54 seconds alongside theme, organ, bass and bell. Revision: withhold Voice Oohs for the first two Invocation bars so the principal chant establishes itself before the choir plane widens.
6. **Declared budgets exceeded profile guides in two sections.** The critic reported Procession 13 vs standard 11, and Benediction 10 vs simple 8. Revision: rebalance the declared attention budgets to 11 and 8 respectively. No notes are added merely to satisfy a metric.
7. **The final cadence should release motion.** Revision: remove the last bass answer/approach, simplify the final theme to a 3.55-beat D4, and let organ/choir decay carry the room.

## Checklist review

- Motif, question/answer phrasing, deliberate summit and phrase breaths: present; Great Amen arrival strengthened in v2.
- Functional harmony and smooth upper movement: present; organ uses broad Dm/Bb/F/Gm/A colours and controlled dominant C-sharp.
- Point/Line/Plane: present in every section (Narthex 1/1/1; later sections 1/2–3/2), with intentional opening silence.
- Bass is not roots-only: held roots, fifths and semitone approaches appear; closing motion is reduced in v2.
- Organ and inner choir are true sustained planes, not short-point accompaniment.
- Strings have an independent contour and are lengthened in v2 to meet their stated continuity target.
- Bell attacks are tied to structure and reduced after v1.
- MIDI/render checks: v1 passes overlap, stuck, tiny-note, stem-silence and clipping checks; final must be checked again after render.

The warnings are treated as evidence. The connected-string and budget warnings are directly addressed; full-role activity at the climax is intentional because the hierarchy remains theme → organ/choir plane → counterline/bass → sparse bell.

## Final verification after revision

- Duration: 134.43 seconds including a 3-second render tail; score length is 131.43 seconds.
- Mix: peak -12.16 dBFS, RMS -28.03 dBFS, zero clipped samples. Section RMS rises coherently from Narthex -32.22 to Great Amen -26.19 dBFS, then falls to Benediction -29.64 dBFS.
- Stems: 6 of 6 are non-silent. Final stem peaks range from -21.59 dBFS (Double Bass) to -11.10 dBFS (Pipe Organ).
- MIDI: 552 note events; zero same-pitch overlaps, zero stuck notes, zero notes under 24 ticks. Shortest intentional note is 216 ticks (0.45 beat).
- Critics: final complexity report has 0 warnings; final continuity report has 0 warnings. Every section has at least one Point, one Line and one Plane, with opening silence preserved.
