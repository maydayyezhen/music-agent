# V1 Critique and Revision

1. V1 Guitar 2 used equal 0.38-beat offbeat durations across both choruses. Complexity critic flagged `mechanical_equal_duration`, and continuity critic classified six sections as `pointillistic_disconnected`.
2. V1 intro/interlude arpeggios had uniform short releases, so their shared-tone intent was visible in pitch but insufficiently continuous in duration.
3. V1 drum bars repeated exact onset/duration signatures too often in verses and choruses, producing five instrument-aware repetition warnings.
4. Vocal-proxy velocities had only stress/non-stress levels, which was insufficient to express internal Chinese word accents.
5. The composition passed physical schema validation, but V1 therefore did not yet meet the requested accompaniment-flow standard.

## V2 actions

- Rewrote Guitar 2 with unequal 0.48-0.90 beat releases, preserving the offbeat identity while connecting attacks into a line.
- Varied Verse 2 upper-voice durations and reserved the denser five-note pattern for the second half of the final chorus.
- Added four rotating kick-placement variants per section family; repetition warnings fell to zero.
- Added three-level within-phrase velocity contour around lyric stress.
- Re-rendered all six stems and final mix. Final status: Complexity 0 warning; Continuity 0 warning; Instrument 0 error / 0 warning.

## V3 MIDI release cleanup

The first post-V2 MIDI audit found 110 same-pitch overlaps in Guitar 1, caused by open-strum releases extending past a later re-attack of the same pitch. V3 applies controlled releases immediately before those re-attacks while preserving different-string and cross-bar harmonic continuity. The final full-song MIDI has 0 same-pitch overlaps on every track.
