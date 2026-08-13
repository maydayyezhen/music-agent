# Composition Guidelines

Read this before creating a song or performing a major rewrite. It is a decision guide for this repository's structured MIDI workflow—not a music grammar checker. The brief wins: experimental, minimal, noisy, dissonant, or non-traditional music may deliberately break these defaults.

## Start with an audible idea, not note accumulation

Good music is not produced by repeatedly choosing “the next note that sounds plausible.” Establish a small identity first:

```text
motif -> repetition -> variation -> contrast -> return
```

Before filling tracks, write down the musical brief, structure, energy map, core motif, and harmony. Test the motif over the harmony at a small scale. Only then expand parts and sections.

## Musical brief and energy map

Record genre, mood, key/mode, tempo, length, instruments, production character, and exclusions in `projects/<song>/musical-brief.md`. Translate adjectives into decisions: “urgent” may mean a short pickup, rising contour, tighter subdivisions, and stronger harmonic drive—not simply higher velocity.

Assign each section an energy value from 1–10. For every section decide:

- which instruments enter, leave, or rest;
- rhythmic density and subdivision;
- melodic register and phrase activity;
- harmonic stability, extensions, inversions, and tension;
- velocity/articulation range and drum intensity;
- transition into the next section.

Energy is perceived contrast, not track count alone. Silence, register, note length, and harmonic rhythm can create as much contrast as adding instruments. Avoid having every track play continuously from bar 1 to the end.

## Melody

- **Motif first:** use a short pitch/rhythm cell that can be recognized after transposition or rhythmic variation.
- Build phrases as question/answer. An antecedent can rise or remain open; the response can redirect, resolve, or deliberately evade resolution.
- Repeat enough to establish memory, then vary one dimension at a time: ending, rhythm, interval, octave, harmony, or instrumentation.
- Give the motif a rhythmic fingerprint; scale-safe wandering without a rhythmic identity is still random wandering.
- Shape a contour. Reserve the highest or most intense note for a meaningful phrase or section climax rather than reaching it casually.
- Control register: verse usually leaves room; chorus can rise or widen. This is a default, not a prohibition against inversion.
- Prefer phrase lengths the listener can parse (often 2, 4, or 8 bars), with pickups or extensions used intentionally.
- The chorus needs a hook: a concise, repeatable musical event with a clear landing point. It should not merely be the verse melody played louder.
- Use rests. A motif with space is easier to recognize than a continuous stream of eighth notes.

## Harmony

- Choose progressions for harmonic function: tonic/stability, predominant/motion, dominant/tension, resolution or deliberate non-resolution.
- Design section-dependent harmony. Verse may sit on longer or inverted chords; pre-chorus can accelerate harmonic rhythm or delay resolution; chorus can clarify the tonic while adding width/color.
- Connect upper voices smoothly. Retain common tones and prefer stepwise or small movements unless a leap is an expressive event.
- Use inversions and slash chords to shape the bass and reduce blocky root-position movement.
- Extensions (6, 7, 9, sus, add9) are color and voice-leading tools, not decorations to add everywhere.
- Dissonance is valid when voiced, timed, and resolved—or intentionally sustained by the brief. Do not treat every semitone as forbidden.
- Avoid changing to an unrelated four-bar progression merely to create novelty. Develop or recontextualize established harmonic material.
- Spread low-register voicings. Dense thirds below middle C quickly become muddy, especially when bass and pad share the area.

## Instrument-specific writing

### Bass

**Bass must not remain a chord-root transcription.** Build lines from roots, fifths, other chord tones, passing tones, approach notes, anticipations, and rests. Aim movement toward the next chord. Relate important attacks to the kick, but allow syncopated answers and pickups so the two parts are partners rather than duplicates. Use inversions consciously. Preserve the low-end foundation and avoid constant fills or high-register virtuosity unless requested.

### Guitar

**Guitar is not Piano MIDI copied to another program.** Respect playable range and fretboard-like shapes. Choose a section role: open/drop-style voicing, power chord, muted pulse, strum, arpeggio, riff, octave line, or lead response. Change articulation with the arrangement—for example, sparse muted verse comping, sustained pre-chorus chords, then power chords or a hook response in the chorus. Leave physical and rhythmic space between attacks.

### Piano

Separate left- and right-hand functions. The left may use bass-independent shells, octaves, fifths, or occasional approaches; the right may comp, arpeggiate, answer the melody, or carry the motif. Voice chords across registers, vary density with sections, and avoid thick low closed-position blocks. Chord attacks need not all be simultaneous or identical in length.

### Strings

**Strings are not a copy of Piano chord blocks.** Choose sustained harmonic support, octave reinforcement, counter-melody, inner-voice movement, swells, or a climax line. Enter and leave strategically. Keep individual lines singable and within plausible ranges; long notes still need direction through dynamics, suspensions, or movement.

### Pad

Pad supplies atmosphere, harmonic glue, and section width. Use broad voicings, slow movement, and lower velocities. Keep it out of the bass's muddy register and out of the lead's rhythmic foreground. A pad may disappear in a sparse section so its return feels wider.

### Drums

- Establish the kick/snare relationship and recognizable backbeat first.
- Choose hi-hat subdivision and accents for the section; repeated hats should not all share the same velocity.
- Use ghost notes, open hats, syncopation, and extra kicks sparingly to develop groove.
- Verse, pre-chorus, and chorus need distinct density, cymbal language, and/or kick pattern.
- Use fills to point toward structural boundaries. A fill is phrasing, not random tom activity.
- Crashes should confirm important arrivals, not occur mechanically every bar.
- Keep anchor hits tight; apply more timing variation to hats, ghost notes, guitar/piano comping, and secondary percussion than to the main downbeat.

## Arrangement development

- Establish a hierarchy: lead/hook, harmonic support, groove foundation, texture. Not every track can be foreground.
- Introduce material in layers. Withhold something valuable—higher register, full hats, strong bass subdivision, strings, or guitar hook—until the section earns it.
- Pre-chorus should create expectation by rising contour, increasing density/tension, shortening phrases, withholding tonic, or stripping down before impact.
- Chorus should deliver a perceivable payoff through hook clarity, register, rhythmic drive, width, and/or harmonic release.
- Transitions can use a pickup, fill, held dominant, crash, rest, inversion, or texture change. Use the smallest device that makes the boundary legible.
- Repetition creates identity; variation keeps identity alive. Change a few consequential elements rather than replacing everything each section.

## MIDI cleanup and humanization

- Vary velocity according to meter, phrase, articulation, and section—not with unbounded randomness.
- Vary note length to distinguish staccato, muted, connected, and sustained roles.
- Preserve intentional accents and the first downbeat as anchors.
- For human-feeling parts, use restrained timing offsets (often a few milliseconds; rarely beyond about 20–25 ms). Avoid independently randomizing chord tones unless a roll is intended.
- Keep kick and main snare tighter than hats and secondary parts. Do not humanize all instruments with the same algorithm.
- Check overlaps, stuck notes, tiny accidental notes, out-of-range pitches, and collisions between tracks.

## Render, critique, revise

The first successful WAV is a draft. Save `composition_v1.json`, render, then inspect the actual audio and complete `references/composer-checklist.md`. Write concrete issues to `projects/<song>/critique.md`; make at least one targeted revision and save it as `composition_v2.json`. Critique decisions, not intentions: “chorus hook is obscured by guitar chord attacks” is actionable; “make it better” is not.

References are retained under `references/` for deeper reading. See `references/SOURCES.md` for provenance and `AGENTS.md` for progressive disclosure routes.
