# Critique and Revision Log

## v1 render evidence

`output/v1.wav` was rendered from `composition_v1.json` with `render_v1.json`. The real render is 75.04 seconds long. All six intended stems are non-silent. MIDI inspection found no stuck notes and no overlaps except two same-pitch piano collisions described below.

Measured full-mix peak was **-21.18 dBFS** and RMS was **-38.53 dBFS**. Section RMS values were Intro -42.50, A -39.12, B -36.16, Return -38.72, Outro -43.39 dBFS. This verifies that B expands by about 3 dB over A and the return/outro fall correctly, but also reveals the following concrete problems.

## Problems found and targeted revisions

1. **The delivered level is impractically quiet.** A -21.18 dBFS peak leaves roughly 20 dB of unused headroom and makes the piece feel tentative even at the intended B-section peak. Revision: raise local per-track mix gains by 7–10 dB while preserving the section balance; retain the -1 dBFS peak safety ceiling.

2. **Strings occupy too much foreground in B.** The raw strings stem measures -30.8 dBFS RMS in B, louder than the piano stem's -33.3 dBFS there. Its nearly continuous 3.8-beat sustains blur phrase edges and compete with the melody. Revision: reduce string velocities by roughly 10–12, shorten sustained notes to about 3.45 beats, and keep the counter-line while allowing breath between chords.

3. **B is brighter than the nostalgic brief needs.** Mix spectral centroid rises from 1434 Hz in A to 2130 Hz in B. The repeated open hats on every other bar are a significant brittle accent in the GeneralUser kit. Revision: replace those four open hats with quieter pedal hats and reduce adjacent hat velocities, keeping the B groove fuller without an EDM-like sheen.

4. **Stereo image is too narrow.** Full-mix left/right correlation is 0.98 even though guitar and strings have different roles. Revision: widen the complementary pans for piano/strings versus guitar/pad while leaving bass centered and drums nearly centered.

5. **Two piano accompaniment notes collide with melody D4 attacks.** MIDI inspection found same-pitch overlaps at absolute beats 25.5 and 89.5 (A and Return equivalents). Revision: revoice the B-minor shell from F#3–D4 to F#3–B3 at both locations, removing the duplicate onset while retaining harmony.

## Checklist summary

- Motif and hook: clear F#–A–B–A identity, repeated in Intro/A/Return and expanded upward in B.
- Harmony: functional D-major motion with inversions and delayed tonic return; upper parts retain common tones.
- Bass: uses fifths, chord tones, chromatic/diatonic approaches, and rests rather than root-only copying.
- Guitar: arpeggios and off-beat dyads are distinct from piano and remain in playable clean-guitar range.
- Piano: sparse shells and melodic phrases leave audible rests; no low closed-position blocks.
- Strings/pad: strings enter only in B and withdraw during Return; pad remains atmospheric above bass range.
- Drums: A side-stick, B snare/denser hat language, boundary fills, and Return simplification make form audible.
- Arrangement: entrances, register, and density follow the energy map; B is a payoff rather than a louder copy.
- MIDI/render: velocities and durations are purposeful; final candidate must be rechecked for duplicates, stuck notes, silence, duration, clipping, density, and tail.

## Final verification

The selected revision is saved as both `composition_final.json` and `composition.json` (byte-identical), with a recoverable `composition_v2.json` copy. The final MIDI pass contains 548 note events across six tracks, with **zero overlapping same-pitch starts, zero stuck notes, and zero tiny notes**. Every final stem is non-silent and the mix remains 75.04 seconds.

After the compositional/timbral revision, B-section spectral centroid fell from **2130 Hz to 1629 Hz**, strings became more subordinate, and stereo correlation improved from **0.980 to 0.957**. Section dynamics remain correctly shaped: Intro < A < B > Return > Outro. A final uniform gain-stage lift preserves that balance while placing the finished peak near -3 dBFS with no clipping.
