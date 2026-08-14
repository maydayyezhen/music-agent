# Strumming Flow Report

## Eight-bar A/B result

- Bars 1-2 are the intentional failure baseline: one sounding downbeat hit per bar, with the remaining seven hand-grid positions preserved as air motion.
- Bars 3-4 Acoustic Verse: 8.0 hand motions/bar, 6.0 sounding strums/bar, upstroke ratio 50%.
- Bars 5-6 Acoustic Pre-Chorus: 7.0 sounding strums/bar; the pattern changes from Verse A to steady eighths without resetting the hand direction.
- Bars 7-8 Acoustic Chorus: 8.0 sounding strums/bar, [] one-hit bars.
- Electric Verse/Pre/Chorus densities: 8.0 / 7.0 / 6.0.
- Every non-final bar declares last hand direction `up`, next expected direction `down`, and `pattern_continues_across_bar=true`.
- Air strums remain in `strumming_pattern_debug.json`; they are not converted into fake pitched notes.
- Validator warnings: 0. The two baseline bars are explicitly labeled and excluded from Verse/Chorus acceptance.
