# Electric Bass

## Band responsibility

- Connect harmony to groove: define roots while creating motion into the next chord.
- Lock selected attacks with kick, support snare backbeat indirectly, and bridge the
  rhythmic language of drums and guitars.
- Control low-frequency density through note length and rests, not merely velocity.

## Common range and register

- Standard four-string sounding range is E1 upward; D1 requires drop-D or a declared
  extended instrument. Typical band writing stays roughly E1-E4.
- Low close intervals and stacked chords are normally avoided; upper-register fills are
  occasional foreground events.

## Physical playability

- Lines should map to four strings with reachable position changes at the written tempo.
- Repeated notes need an alternating-finger or pick policy; dense leaps across strings
  should allow recovery time.
- Legato, slide and hammer/pull transitions need compatible positions. Long notes should
  release before a contradictory reattack on the same string.

## Phrase vocabulary by section

- Verse: root anchors, root-fifth patterns, sparse syncopation, occasional approach into
  the next chord.
- Chorus: eighth-note drive, octave/fifth expansion, kick-linked accents, melodic pickup
  into repeats.
- Bridge/build: pedal tone, ascending sequence, counterline or rhythmic displacement.
- Turnaround: chromatic/diatonic approach, enclosure, octave drop or brief fill.

## Interaction

- `kick_lock` is a weighted relationship: important bass attacks may align with kick,
  but copying every kick removes independent phrasing.
- Against palm-muted guitar, bass can sustain or connect. Against open chords, bass may
  articulate subdivisions and approaches.
- Avoid occupying the same low register as keyboard left hand; one role should thin out.

## Articulation and MIDI expression

- Semantic articulations: `finger`, `pick`, `palm_mute`, `staccato`, `accent`, `slide`,
  `hammer_on`, `pull_off`, `ghost`, `harmonic`.
- Note duration expresses gate; velocity expresses attack, not a universal loudness curve.
- Slides/legato are profile-mapped by keyswitch, CC or pitch bend only when documented.

## Piano-roll anti-patterns

- Root notes on every downbeat with identical one-beat duration for the entire song.
- Exact kick duplication or exact rhythm-guitar duplication throughout.
- Random scale tones unrelated to the current/next chord.
- Large low-register leaps at sixteenth-note speed with no position plan.

## Code-convertible rules

- Choose candidates by function: root, fifth, octave, chord tone, approach, passing,
  pedal or rest. Store the selected function in the semantic phrase.
- Score kick alignment ratio, but warn at both near-zero and near-total copying.
- Prefer small position movement, allow purposeful octave/section-boundary jumps.
- Validate range, same-string overlap, transition reach and cross-bar connection.

## Preferences, not hard laws

- Root frequency, kick-lock ratio, approach chromaticism and register depend on genre.
- Chords, tapping and extreme range are allowed when explicitly requested and playable.

