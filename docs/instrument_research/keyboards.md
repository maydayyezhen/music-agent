# Piano, Organ and Keyboard

## Band responsibility

- Supply harmony, countermelody, rhythmic comping, atmosphere or a foreground hook.
- Use two-hand/register planning and adapt density around guitar, bass and lead parts.
- Piano is percussive and pedal-resonant; organ is continuously sustained and shaped by
  fingering, expression and rotary state. They are not interchangeable piano rolls.

## Common range and register

- Full piano range is broad, but ensemble writing should reserve the bass register when a
  bass player is active and avoid masking the lead in its strongest octave.
- Organ has no natural note decay. Low sustained voicings accumulate mud quickly; rock
  organ often uses mid-register compact voicings or right-hand-only support.

## Physical playability

- Simultaneous notes should fit two hands; very wide grips should be rolled, redistributed
  or reduced. Independent lines require plausible hand allocation.
- Piano pedalling follows harmonic/phrase changes; pedal is not held through unrelated
  harmony without deliberate blur.
- Organ should not use piano sustain pedal logic. Legato chord changes use finger
  substitution/common tones and controlled overlaps.

## Phrase vocabulary by section

- Piano verse: sparse shells, broken chord, bass-plus-upper answer, offbeat comping.
- Piano chorus: broader voicings, octave reinforcement, rhythmic figures with clear gaps.
- Organ verse: held two/three-note support, short responses, restrained rotary state.
- Organ chorus/bridge: sustained close voicing, rhythmic stabs, counterline, rotary change.

## Interaction

- With rhythm guitar, reduce chord size, change register or use an answering rhythm.
- With bass, omit/limit left-hand roots unless intentionally doubling a climax.
- Fill melodic gaps instead of continuously competing with a foreground phrase.

## Articulation and MIDI expression

- Semantic controls: `pedal`, `pedal_retake`, `staccato`, `tenuto`, `accent`, `rolled`,
  `legato`, `rotary_slow`, `rotary_fast`, `expression_swell`.
- Piano sustain maps to CC64 when supported. Organ rotary/expression mappings are profile
  specific and must degrade to note shaping or static timbre if unavailable.
- Voice-leading remains semantic chord voices until performance encoding.

## Piano-roll anti-patterns

- Both hands play full root-position chords on every beat.
- Every voice mechanically changes at each chord boundary; common tones never remain.
- Piano pedal remains down for the entire song; organ receives piano pedal events.
- Keyboard duplicates guitar voicing/rhythm and bass register simultaneously.

## Code-convertible rules

- Plan smooth voicings with common-tone retention and register bounds.
- Allocate notes to hands and flag spans beyond configurable reach.
- Generate CC64 pedal regions from harmonic spans with retakes before changes.
- Detect low-register collisions, full-block repetition and missing inner movement.

## Preferences, not hard laws

- Hand span, root omission, pedal blur and voice-leading distance depend on player/style.
- Parallel block chords and sustained clusters are legitimate declared textures.

