# V1 critique and V3 resolution — Hands Before Notes

## V1 findings

1. The instrument validator counted silent lead-guitar bars as repeated phrases. Silence is
   intentional phrase space, so the validator was corrected to exclude empty signatures rather
   than changing the music.
2. Rhythm guitar correctly used palm-muted short gates in Verse/Bridge, but the legacy
   continuity critic called that disconnected accompaniment. The critic now recognises an
   explicitly declared `palm_muted_eighths` action as intentional, while retaining its warning for
   anonymous short-note accompaniment.
3. Chorus/final-chorus drums repeated too many identical bars. V2 added four-bar kick variants;
   V3 added open-hat turnarounds and controlled ghost-note placement while preserving limb
   feasibility.
4. Final-chorus rhythm guitar repeated the same attack signature too often. V3 introduced a
   playable fourth-bar breath and a shortened accented turnaround before it.
5. Lead phrase velocity originally had insufficient action hierarchy in the minimum demo. The
   compiler now differentiates picked starts, hammer/pull transitions, slides and bend peaks.
6. The first full-song guitar compile failed on low minor triads. This was a genuine modelling
   issue: generic tertian voicings can be impossible as rock rhythm shapes. Harmony remains `Em`,
   but the rhythm-guitar compiler now realizes it as a globally assigned root-fifth-octave power
   shape.
7. Greedy per-note string assignment could consume the only string available to a later chord
   tone. It was replaced with whole-chord one-note-per-string optimisation.

## Final status

- Instrument critic: 0 errors, 0 warnings, 1 informational register-collision observation.
- Complexity critic: 0 warnings.
- Continuity critic: 0 warnings.
- Semantic note-spacing analysis and exported MIDI audit both report zero same-pitch
  overlaps; all six MIDI tracks also end with zero stuck or unmatched notes.
- All six tracks originate from semantic `instrument_phrase` objects.
- Bridge deliberately has no lead-guitar phrase; five other instrument roles carry it.
- General MIDI articulation fallbacks are reported and do not pretend to be sampled
  keyswitches.
