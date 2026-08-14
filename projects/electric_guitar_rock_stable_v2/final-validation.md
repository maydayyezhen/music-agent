# Final Validation — Lanterns Against the Rain

## Selected result

- Composition: V3 (`composition.json` and `composition_final.json` are byte-identical)
- Structure: 96 bars, D minor, 106 BPM, 4/4
- Rendered duration: 219.358 s (3:39.36)
- Renderer: local FluidSynth + GeneralUser GS
- Tracks: Lead Guitar, Rhythm Guitar, Electric Bass, Drums, Rock Organ, Strings
- Vocals: none; no `vocals.json`

## Structure and measured energy

| Section | Bars | Mix RMS dBFS | Evidence |
|---|---:|---:|---|
| Intro | 8 | -35.51 | Lowest opening energy; lead waits until bar 5 |
| Verse 1 | 12 | -34.76 | Sparse two-bar lead calls; organ absent |
| Pre-Chorus | 8 | -31.93 | Rising motif sequence and fuller planes |
| Chorus 1 | 16 | -29.49 | Open power chords and eighth-hat propulsion |
| Verse 2 | 12 | -32.81 | Real pullback, then motif fragmentation |
| Bridge Relay | 16 | -31.92 | Lead absent; accompaniment builds in two stages |
| Final Chorus | 16 | **-28.01** | Highest measured energy and highest lead register |
| Outro | 8 | -33.19 | Low-register theme return and release |

Final Chorus is 1.48 dB RMS above Chorus 1 and is the loudest section. The final mix has
0 clipped samples; its peak is -13.33 dBFS, so the energy result is arrangement-driven rather
than limiter clipping.

## Stable Lead audit

- Every active Lead clip explicitly declares `phrase_generation_mode: legacy_stable`.
- No `long_form_experimental` or migration alias is present.
- Lead Guitar MIDI note count: 175.
- Strict monophony: 0 different-pitch overlap and 0 same-pitch overlap.
- Pitch Bend messages: 0.
- Stuck notes: 0; unmatched Note Off: 0; tiny notes: 0.
- Bridge Relay (absolute beats 224–288): **0 Lead Guitar Note On events**.
- Lead register develops from MIDI 60–69 in Intro, through 67–81 in Pre-Chorus, to 77–88
  in Final Chorus. The final climax is E6 (MIDI 88), inside the validated guitar range.

Theme development evidence: the D–F–A–G long/short call appears quietly an octave lower in Intro,
is answered every two bars in Verse 1, rises by sequence in Pre-Chorus, is rhythmically compressed
in Chorus 1, fragmented in Verse 2, withheld for the entire Bridge, and returns with extra bar-4,
bar-8 and bar-12 answers plus the E6 arrival in Final Chorus. This is conventional stable MIDI
realization guided by a section-level brief, not the experimental Long-Form compiler.

## Bridge Relay audit

Lead Guitar has no section clip and the final MIDI confirms zero bridge events. The remaining five
parts are not merely static accompaniment:

| Role | Bars 1–8 | Bars 9–16 | Quantified change |
|---|---|---|---:|
| Organ | Long ascending statements and short pickups | Higher three-attack phrases plus closing D–F–A–C pickup | 16 → 28 events |
| Strings | One displaced answering tone per bar | Two-note rising answers plus F–A–D launch | 8 → 19 events |
| Bass | Root/fifth/octave/approach connecting line | New Gm–Bb–F–C–Dm–Bb–A–Dm harmonic route | 28 → 28 events; pitch/harmony changes |
| Rhythm Guitar | Pedal/power-shape propulsion | New second-half chord path under the relay | 192 → 192 note events; pitch/harmony changes |
| Drums | Chorus-level groove | Continues propulsion and closes with transition fill | 114 → 115 hits |

At least organ, strings, bass and rhythm guitar therefore carry recognizable changing material.

## Return variation

- Chorus 1 bars 9–16 add separate D–F–A and C–A–G answering cells instead of copying bars 1–8.
- Verse 2 replaces several full calls with three- and four-note fragments.
- Bridge second half changes harmony instead of looping its first eight bars.
- Final Chorus changes the middle harmony, introduces answers in even bars 4/8/12, reaches E6 in
  bar 14 and reserves the long D6 resolution for bar 16.

## Critic and MIDI results

- Instrument critic: 0 errors, 0 warnings, 4 informational register observations.
- Complexity critic: 0 warnings.
- Continuity critic: 0 warnings.
- All six standalone MIDI tracks and `full_song.mid`: 0 same-pitch overlap, 0 stuck notes,
  0 unmatched Note Off and 0 tiny notes.
- All six stems are non-silent and contain no clipped samples.
- Final WAV: 44.1 kHz stereo, 0 clipped samples.

## Revision proof

- V1 WAV SHA-256: `5978ccc0dc2b842b0b468b429705e4efaddc6ab7f4370d988f5d17d5b40af555`
- Final WAV SHA-256: `418eb1dabcb2f33e01f80f4006c593dfcc03600f32c133c1b0f683521f080b2a`

The hashes differ, and V1/V2/V3 compositions remain saved. No shared source, script, profile,
documentation, skill or configuration file was modified by this Composer Agent.
