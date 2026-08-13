# Critique — v1 Render

## Render evidence

The first draft was rendered through the real local FluidSynth/GeneralUser GS pipeline and saved as `output/v1.wav` before any revision.

- Duration: **72.769 s**.
- Mix peak: **−6.86 dBFS**; integrated RMS: **−26.04 dBFS**; no clipping.
- Section RMS: cold open −26.47, verse −26.77, chorus −24.79, breakdown −30.09, final chorus −24.51, outro −24.24 dBFS.
- Stem RMS: guitar L −26.15, guitar R −23.52, bass −27.73, drums −24.28, organ −33.73 dBFS before song-level mix gain/pan.
- All five intended stems were non-silent. The mix tail ended at the intended score duration plus two seconds.

## Three concrete v1 problems and fixes

1. **The opening had no real entrance event.** Bass and full drums played from the first downbeat, so the 4-bar cold open measured almost the same loudness as the verse, and the verse was actually 0.30 dB quieter. That contradicted the planned entrance/density rise. **Fix:** expose the guitar riff for two bars, add one restrained side-stick pickup, then bring bass and the full kit in at bar 3.
2. **Right guitar masked the hook.** Its stem was 2.63 dB RMS louder than guitar L even though both shared the same preset and mix gain. The V1 right guitar sustained four attacks per verse bar, making the GM overdrive behave like a midrange wall while the left riff—the actual identity—sat behind it. **Fix:** rewrite the verse as three short offbeat power-chord chops per bar, lower its velocities, and preserve obvious gaps.
3. **Chorus width came at the cost of articulation.** Right-guitar chorus chords lasted 1.75 beats, overlapping most of the left riff's answer spaces. The chorus was correctly louder than the verse, but the payoff read more as continuous density than a sharper hook. **Fix:** retain the same D–A–E–G harmonic support while shortening those attacks to 0.92 beats and slightly lowering velocity.
4. **The final chorus needed development beyond velocity.** Its extra energy came mainly from louder repeats and quiet organ glue. **Fix:** add two brief chromatic bass anticipations (C#→D/E area and D#→E) so the last pass has forward-directed variation without replacing the established line.
5. **The MIDI scan found one duplicate kick at the final crash.** The V1 outro generator added a kick on a downbeat already present in the section groove. It did not clip, but it was an unnecessary doubled event. **Fix:** deduplicate matching drum-note/time pairs in the final composition builder; the final scan must report zero overlaps and zero stuck notes.

## Composer checklist

### Melody / motif

- [x] The left-guitar riff has a recognizable short-short/gap/short-long-short rhythm.
- [x] It repeats in cold open, verse, chorus, final chorus, and outro.
- [x] Variation comes from harmony, register, dynamics, support pattern, and breakdown fragmentation.
- [x] Chorus has a specific D–A–E–G power-chord hook with E as the strongest landing area.
- [x] Breakdown creates useful rests and answer phrases; final chorus carries the intensity peak.
- [x] There is no scale-safe wandering.

### Harmony

- [x] Verse modal motion, chorus release, and breakdown predominant tension have distinct functions.
- [x] D# and other chromatic notes are short approaches with destinations.
- [x] Low guitar voicings are open fifths rather than muddy closed triads.
- [x] The song develops the same harmonic vocabulary instead of swapping in unrelated progressions.

### Bass

- [x] Uses roots, fifths, chord tones, passing notes, chromatic approaches, anticipations, and rests.
- [x] Important attacks cooperate with kick while syncopated notes answer independently.
- [x] Activity increases in choruses without turning into constant filling.

### Guitar / organ

- [x] L and R guitars are independently written; neither is a piano transcription.
- [x] Roles change among riff, clipped chord answer, wider chorus support, and sparse breakdown response.
- [x] Final revision explicitly leaves more space for the main hook.
- [x] Organ is optional upper support only and is absent from intro/verse/first chorus.
- [x] No strings or pad are used.

### Drums / arrangement

- [x] Kick/snare relationship is coherent, with velocity-shaped eighth hats.
- [x] Verse, chorus, breakdown, and final chorus use distinct density/cymbal language.
- [x] Fills and crashes mark structural boundaries.
- [x] Revised entrances/exits make the cold-open → verse rise and breakdown contrast legible.
- [x] Anchor hits remain tight; looseness comes from syncopation, articulation, and unequal accents.

### MIDI / render

- [x] Velocities and durations reflect meter, phrase, and articulation.
- [x] Final event scan found no out-of-range pitches, tiny durations, same-pitch overlaps, or stuck notes; the single V1 duplicate outro kick was removed.
- [x] All intended stems are non-silent and duration is within the requested 60–90 seconds.
- [x] V1 was preserved, critiqued from its real render, revised compositionally, and final will be rendered separately.
