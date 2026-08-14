# V2 composition plan

V2 deliberately keeps V1's title, 116 BPM, E minor key, 104-bar form, harmony, seed 116042, instrument setup, motif and every authored note unchanged. `v1/composition.json` and `v2/composition.json` have the same SHA-256.

The single realized difference is that the existing lead compiler now honors an authored, physically valid `planned_string` / `planned_fret` path and passes `slide_from_semitones` through the profile into a smooth pitch-wheel approach. This makes the already-planned position changes at Theme A/B, Solo and Final Theme audible without changing melodic content.

Solo plan remains: motif-derived mid position (1-8), upward 12th-position sequence (9-16), denser extension (17-24), high-position bend climax (25-28), descending motif recovery into Final Theme (29-32).
