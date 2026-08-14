# Strings and Pad

## Band responsibility

- Strings provide long arcs, counter-motion, inner movement, rhythmic bow figures or a
  climax. Pads provide harmonic glue and atmosphere without implying acoustic bowing.
- Entries, exits, register and dynamics should follow the energy map.

## Common range and register

- Acoustic string ranges depend on section (violin, viola, cello, bass); a generic
  `strings` phrase must declare section or ensemble profile before strict validation.
- Pads are synthesis textures; their practical MIDI range is profile-defined, but mix
  register and collision constraints still apply.

## Physical playability

- One acoustic player cannot sustain arbitrary independent chord tones; ensemble chords
  imply divisi or playable multiple stops. The semantic phrase must distinguish these.
- Bowed phrases need bow/breath-like renewal points. Continuous long notes may cross
  harmony through common tones, while moving voices change smoothly.
- Fast repeated strings need an articulation such as spiccato/tremolo, not implausibly
  re-triggered long samples.

## Phrase vocabulary by section

- Verse: held common tones, sparse inner-voice response, soft counterline, or silence.
- Chorus: octave support, wider voicing, countermelody, rhythmic ostinato or swell.
- Bridge: pedal tone, contrary-motion line, divisi cluster, tremolo build.
- Ending: decrescendo, thinning voices, retained common tone or deliberate unresolved pad.

## Interaction

- Avoid copying keyboard chord blocks. Retain common tones and move one or two inner
  voices while other parts articulate rhythm.
- Keep low cello/bass material clear of electric bass unless reinforcing a climax.
- Counterlines should avoid constant unison with the main melody.

## Articulation and MIDI expression

- Semantic articulations: `sustain`, `legato`, `portamento`, `staccato`, `spiccato`,
  `pizzicato`, `tremolo`, `accent`, `crescendo`, `decrescendo`.
- Dynamics and expression are separate intents. A profile may map them to CC1/CC11,
  velocity, or static fallback. Articulation maps may use keyswitch, CC, channel or patch.
- Profile-specific examples such as Spitfire UACC CC32 remain outside composition logic.

## Piano-roll anti-patterns

- Four-note chords retrigger on every beat with identical gate/velocity.
- Every voice jumps to root position at every harmony change.
- Strings and pad duplicate identical notes and rhythm for an entire section.
- No dynamic curve, bow renewal, articulation change or inner movement appears.

## Code-convertible rules

- Preserve common tones and minimise per-voice motion subject to register/spacing.
- Store divisi/ensemble intent; warn when a solo-section profile receives dense chords.
- Create dynamic curves separately from notes and report articulation/dynamic coverage.
- Detect register collisions, duplicate layers and mechanical chord replacement.

## Preferences, not hard laws

- Maximum bow length, divisi balance, spacing and articulation frequency are library,
  tempo and orchestration dependent.
- Static drones, parallel planing and synthetic pad blocks are valid intentional styles.

