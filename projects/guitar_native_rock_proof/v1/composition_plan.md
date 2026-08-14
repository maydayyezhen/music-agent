# V1 composition plan

## Core motif

`E4(1/8) G4(1/8) A4(1/8) B4(dotted-1/8) A4(1/16) G4(1/8) E4(1/4)` in a connected 7th-position E-minor shape. It is developed through upward sequence, rhythmic compression, extension, fragmentation and bend targets. The machine-readable form is in `../core_motif.json` and `composition.json.core_motif`.

## Solo plan

- Bars 1-8: Theme fragment in the mid register; steady connected eighth-note motion, no full resolution.
- Bars 9-16: Sequence upward into the 12th position; repeated B, hammer/pull groups and tighter subdivision.
- Bars 17-24: Longer sixteenth-note runs extend the same shape toward A5; bar 24 remains open.
- Bars 25-28: High-position acceleration, D6 bent toward the E6 target, continued motion, then bend release.
- Bars 29-32: Descending sequence reuses the motif tail and enters Final Theme without a phrase reset.

V1 intentionally uses the current stable compiler unchanged. Planned string/fret and `slide_from_semitones` fields are authored so the post-render audit can verify whether the current compiler preserves and realizes them.
