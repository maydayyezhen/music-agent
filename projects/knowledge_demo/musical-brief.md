# Knowledge Demo — Musical Brief

## Fixed brief shared with the old demo

- Style: 2000s Japanese galgame / anime opening instrumental
- Duration: about one minute
- Tempo: 120 BPM
- Key: A major
- Form: Intro → Verse → Pre-Chorus → Chorus
- Instruments: Piano, Bass, Guitar, Strings, Pad, Drums
- Local structured MIDI rendered through the existing FluidSynth/GeneralUser GS pipeline

No MIDI or note list from `old_demo` may be copied. The point is to re-compose from the same verbal brief after applying the knowledge workflow.

## Emotional and production target

“A window opening onto a bright summer morning”: immediately recognizable optimism, a conversational verse, a pre-chorus that leans forward, and a chorus with an unambiguous singable payoff. The arrangement should feel like a compact TV-size opening rather than a loop repeated at increasing volume.

Avoid random scale runs, continuous six-track density, root-only bass, piano-shaped guitar chords, copied string blocks, identical section drums, and unshaped velocities.

## Structure and energy map

| Section | Bars | Energy | Arrangement decision |
|---|---:|---:|---|
| Intro | 4 | 2/10 → 3/10 | Piano states the motif over pad; bass enters lightly; drums withhold full groove; strings only answer near the end. |
| Verse | 8 | 4/10 | Lower-register piano question/answer; bass uses space and approaches; tight hats/backbeat; guitar enters only in the second half with muted off-beats; strings provide one inner line. |
| Pre-Chorus | 4 | 6/10 → 8/10 | Harmonic rhythm and register rise; bass ascends; guitar sustains rather than comps; strings swell upward; hats open and tom fill points into chorus. Brief breath before impact. |
| Chorus A | 8 | 9/10 | Guitar carries the core hook; piano changes to high broken-chord drive; bass uses eighth-note direction; full drums and crash; strings answer rather than double. |
| Chorus A′ | 8 | 10/10 → resolution | Hook returns with a changed answer and higher climax; extra bass approach, string counter-line, and final drum fill; parts converge on a clear A-major landing. |

Total: 32 bars = 64 seconds of score plus a 2-second render tail.

## Core motif

Rhythmic identity: a short pickup followed by **short–short–long**, then a descending answer.

```text
pickup: E5 (eighth)
statement: A5 (quarter) – G#5 (eighth) – F#5 (eighth) – E5 (held)
answer: C#5 – E5 – F#5 – E5 – B4 (landing/open ending)
```

Development plan:

1. Intro Piano presents a restrained form in the upper register.
2. Verse Piano uses only the question rhythm at a lower register and leaves rests.
3. Pre-Chorus stretches fragments into an ascending sequence.
4. Chorus Guitar states the complete hook; Piano supplies a distinct broken-chord drive.
5. Chorus A′ changes the answer and reaches C#6 only once as the climax before returning to A5/A major.

## Harmony plan

The harmony grows from the same A-major world rather than replacing progressions randomly.

- Intro: `Aadd9 | E/G# | F#m7 | Dadd9 – Esus4`
- Verse: `A | E/G# | F#m7 | C#m7/E | Dmaj7 | A/C# | Bm7 | Esus4 – E`
- Pre-Chorus: `Dmaj7 | E | C#m7 – F#m7 | Bm7 – Esus4 – E`
- Chorus: `A | E/G# | F#m7 | Dmaj9 | A/C# | Bm7 | D/E – E | A`

Upper voices keep E/A/C# as common tones when useful. Slash chords give the bass a descending/stepwise skeleton; extensions create color without turning every instrument into the same five-note block.

## Instrument roles

- Piano: motif/answer in Intro and Verse; high broken-chord momentum in Chorus. Avoids low block chords.
- Bass: supports roots at arrivals, then uses fifths, thirds, passing/approach notes, anticipations, and rests; coordinates with kick but does not clone it.
- Guitar: absent/sparse early, muted off-beat comping late in Verse, sustained build in Pre, distinct single-note hook and occasional power-chord punctuation in Chorus.
- Strings: delayed entrance, inner movement and counter-lines, rising Pre swell, chorus answers/octave support—not Piano chord copies.
- Pad: quiet wide harmonic glue in Intro/Verse, reduced before the Chorus impact, broad but subordinate in Chorus.
- Drums: sparse Intro, tight Verse, opening Pre, full Chorus, transitions/fills at structural boundaries; velocity accents shaped by beat and phrase.

## Humanization policy

Anchor downbeats and main snare remain tight. Hats alternate accents and use small beat offsets; muted guitar attacks sit slightly around the grid; chord durations and velocities follow phrasing. No random pitch changes or global one-size-fits-all timing jitter.
