# Electric Rhythm Guitar

## Scope and evidence

This document separates guitar writing from library-specific playback. It combines the
project's pinned arrangement/MIDI references with Ample Sound and Shreddage manuals.
Exact keyswitches are profile data, never universal composition rules.

## Band responsibility

- Establish harmonic rhythm and the subdivision felt by the band.
- Interlock with kick/snare and bass without duplicating either part continuously.
- Change energy by moving between rests, muted attacks, riffs, open power chords,
  arpeggios, and held feedback-like tones.
- Leave holes around lead or vocal phrases and use fills at phrase boundaries.

## Common range and register

- Standard six-string sounding range begins at E2; practical rhythm writing usually
  centres on E2-B4. Extensions below E2 require an explicit drop tuning/profile.
- Dense distorted voicings should normally stay compact and omit unnecessary thirds in
  the low register. Register is an intent (`low`, `low_mid`, `mid`), not a guessed fret.

## Physical playability

- A note or chord should have a plausible string/fret assignment. One string cannot
  produce two simultaneous pitches; wide chord shapes need a reachable fret span.
- Power chords are root/fifth/octave shapes, usually on adjacent strings. Parallel
  movement should prefer a stable shape and small position changes.
- Repeated tight attacks need a picking policy: downstroke has lower sustainable speed;
  alternate picking permits higher rates but changes accent character.
- A strum is one physical sweep. Its notes must be ordered low-to-high or high-to-low,
  offset by a small total spread, rather than perfectly simultaneous piano attacks.
- Palm-muted attacks are shorter and usually lower-register; open chords may ring across
  beats. Sustained notes cannot overlap a contradictory new fret on the same string.

## Phrase vocabulary by section

- Verse: `palm_muted_eighths`, sparse dyads, single-string riff, off-beat stabs,
  broken-chord figures with rests.
- Chorus: `open_power_chords`, wider strum, octave reinforcement, denser subdivision,
  strategically released final chord.
- Bridge/build: pedal-tone riff, displaced accents, call-and-response, register climb,
  or gradual mute-to-open transition.
- Transition: one- or two-beat slide, rake, octave answer, or compact turnaround; fills
  should not occur on every boundary.

## Interaction

- Lock selected chord attacks with kick, but allow the guitar to sustain or syncopate
  while bass connects harmony.
- Avoid duplicating a keyboard's register and voicing. If both comp, one should thin out,
  use a different rhythm, or answer the other.
- During lead phrases, rhythm guitar should reduce upper-register motion and reserve
  fills for lead rests.

## Articulation and MIDI expression

- Semantic articulations: `sustain`, `palm_mute`, `accent`, `staccato`, `dead_note`,
  `slide`, `hammer_on`, `pull_off`, `harmonic`, `strum_up`, `strum_down`.
- Notes encode onset, duration and velocity; ordered chord offsets encode a strum.
- Pitch bend may encode a slide only when the profile declares a bend range and the
  phrase is monophonic on that MIDI channel.
- Keyswitch/CC values come from the sound-library profile. General MIDI falls back to
  duration, velocity, voicing and optional program changes; it must not emit invented
  Ample/Shreddage switches.

## Piano-roll anti-patterns

- Every chord tone starts at the same tick with identical velocity.
- Six-note closed chords move in parallel regardless of tuning or hand position.
- Muted verse and open chorus use the same durations and density.
- Continuous eighth notes have no picking accents, rests, phrase endings, or transitions.
- Random timing is applied independently to chord tones, destroying the physical strum.

## Code-convertible rules

- Validate standard tuning range and reject impossible simultaneous string assignment.
- Generate power-chord shapes from tuning plus root, not from generic tertian voicing.
- Constrain fret span and prefer minimal position movement between adjacent shapes.
- Treat each strum as an onset group with one direction and bounded spread.
- Tie humanization to pick direction, metrical accent and phrase boundary.
- Report identical repeated phrase signatures and perfectly simultaneous chord attacks.

## Preferences, not hard laws

- Exact fret span, maximum picking rate, downstroke use, chord size and amount of mute
  depend on genre, player and tempo. Validators should warn with context, not ban them.
- Parallel shapes, mechanical timing and extreme registers are valid deliberate effects.

