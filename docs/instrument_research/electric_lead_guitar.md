# Electric Lead Guitar

## Band responsibility

- Carry a recognisable motif, answer another foreground part, or create a solo arc.
- Shape tension through register, target notes, rhythm, articulation and silence rather
  than through note density alone.
- Lead into section boundaries with pickups, bends, slides or held resolutions.

## Common range and register

- Standard sounding range begins at E2, but melodic lead normally lives around E3-E6.
- Notes above the physical fretboard or below the configured tuning require an explicit
  extended-range profile. A comfortable register is preferable to permanent top-range
  intensity.

## Physical playability

- Monophonic lines should minimise impossible position jumps at high subdivision rates.
- Legato transitions generally require same-string/reachable-position planning; a bend
  must start from a fret with room and should resolve or release intentionally.
- When fingering is compositionally important, a motif note may preserve an explicit
  zero-based `planned_string` / `planned_fret` pair. The compiler validates the pitch
  against the configured tuning rather than silently substituting another position.
- Simultaneous independent bends are not safe on one ordinary MIDI channel. Polyphonic
  expression requires MPE or separate channels and profile support.
- Sustained notes need left-hand and string availability; overlapping same-string notes
  or a slide plus unrelated chord are suspect.

## Phrase vocabulary by section

- Verse: motif fragments, long answer notes, two- to four-note calls, breath after a
  landing tone.
- Chorus: compressed hook, octave displacement, repeated target tones, wider climax.
- Bridge/solo: sequence, motif inversion, pedal point, register expansion, bend-release,
  legato burst, then a clear landing.
- Final chorus: retain hook identity but add a response, altered ending or higher octave.

## Interaction

- Phrase endings should line up with drum fills or leave a gap for them, not compete.
- Bass may anticipate a lead landing but should not shadow every pitch.
- Keyboard/rhythm guitar should thin or move register beneath a lead climax.

## Articulation and MIDI expression

- Semantic articulations: `sustain`, `accent`, `bend`, `bend_release`, `vibrato`,
  `slide`, `hammer_on`, `pull_off`, `legato`, `harmonic`, `pinch_harmonic`, `mute`.
- Bend intent stores interval and curve independently of MIDI's 14-bit value. A profile
  maps it using its declared pitch-bend range or articulation trigger.
- A deliberate position shift may store `slide_from_semitones`; a pitch-bend-capable
  profile realizes it as a smooth approach to the target and the shared-channel safety
  gate suppresses it whenever another note overlaps.
- Vibrato stores delayed onset, depth and rate; a profile may use CC1, aftertouch,
  pitch-bend curves, a keyswitch, or a fallback repeated controller curve.
- Legato stores a transition relation between notes. Overlap is produced only when the
  target library requires it.

## Piano-roll anti-patterns

- A 32-bar solo contains only short detached scale notes and no phrase-level rests.
- All intervals are equally likely; position and target tones are ignored.
- Every repeat is byte-identical or every repeat is unrelated to the motif.
- Bends are absent in an expressive solo, or random pitch bends are added to chords.
- Note gaps and velocities are random rather than tied to pick/legato actions.

## Code-convertible rules

- Assign plausible string/fret paths and penalise large position movement at short IOIs.
- Enforce monophonic bends on a shared channel unless a profile declares MPE.
- Generate motif variations through rhythm, ending, octave or ornament transformations.
- Measure breath/gap distribution, phrase repetition, articulation coverage and target
  note landings.
- Use deterministic seeds only for bounded alternative choices, never for core intent.

## Preferences, not hard laws

- Maximum leap, bend frequency, vibrato amount and note density are style-dependent.
- A deliberately keyboard-like tapped passage or mechanically repeated note is valid
  when the phrase explicitly declares that technique.
