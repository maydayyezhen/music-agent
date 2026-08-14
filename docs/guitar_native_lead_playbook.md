# Guitar-native Lead Playbook

This playbook records the proven approach behind `projects/guitar_native_rock_proof`.
Read it before composing a substantial Electric Lead Guitar theme or solo. It is a
workflow and decision guide, not a fixed lick library and not a requirement that every
song contain 32 bars of continuous notes.

## Proven result

The reference song **The Distance Still Burns** was composed at E minor, 116 BPM and
104 bars. Its Main Solo spans 32 bars as one performance process:

- 32/32 solo bars active;
- 301 solo notes and one phrase island at the explicit gap threshold of 0.5 beat;
- maximum internal gap 0.09 beat and no rest over one beat;
- density arc 57 / 80 / 86 / 78 notes per eight-bar block;
- delayed E6 peak at solo bar 26;
- zero different-pitch overlap and zero unsafe pitch-wheel messages;
- one core motif is stated, sequenced upward, compressed, extended, driven into a bend
  target, released into a descent, and recovered in the Final Theme.

These numbers prove this particular result. They are useful diagnostics, not universal
targets. A slower or sparser guitar work may need more space.

## The central lesson

Do not compose a singable melody and replace its timbre with guitar. Compose a physical,
continuous guitar performance whose pitches and rhythm grow from:

```text
fretboard shape
-> repeated picking/legato pattern
-> position-preserving variation
-> connected position shift
-> rhythmic compression or expansion
-> delayed target and release
-> motif recovery
```

Articulation comes after this skeleton works. Slide, bend and vibrato cannot rescue an
unrelated lick collage.

## Mandatory workflow for substantial Lead Guitar

### 1. Design one playable core motif

Before arranging the song, store a real 1-2 bar motif with pitch, onset, duration,
rhythmic identity, contour and a plausible fretboard position. It should support at least
three of these operations:

- sequence up/down;
- rhythmic compression or expansion;
- fragmentation and extension;
- register displacement;
- repeated-note propulsion;
- approach to a bend target;
- descending recovery.

Do not settle for a scale-safe pitch list without rhythmic identity.

### 2. Plan the hand path before decorating notes

Divide the long span into a small number of physical regions, for example:

```text
mid position -> upper position -> high position -> descending return
```

Within a region, prefer reachable same-string hammer/pull motion, adjacent-string
movement, repeated picking patterns and modest fret motion. A new position must be a
development of the previous material, not a new unrelated lick.

### 3. Write a section arc, not repeated closed phrases

For a long solo, plan the entire contour before expanding notes:

1. establish motif and position;
2. vary it without resetting;
3. sequence it along the fretboard;
4. increase rhythmic or intervallic pressure;
5. reach the high target late;
6. continue after the target note;
7. release/descend into the next section.

Do not automatically use `long note -> vibrato -> rest -> new lick` every two or four
bars. A breath is allowed, but it must not erase direction, position or motif state.

### 4. Make every transition explainable

Every adjacent pattern should connect through at least one reason:

- shared boundary pitch;
- slide into the next position;
- bend release into the next pattern;
- retained picking/repeated-note rhythm;
- transposition, compression, expansion or fragmentation of the previous pattern;
- continuation of the current ascent/descent;
- reuse of the previous pattern's tail.

If the composer cannot answer “why does this follow the previous pattern?”, rewrite it.

### 5. Keep the skeleton monophonic and convincing

Before complex articulation, the plain-note version must already sound guitar-shaped:

- recognisable fretboard motion;
- repeated/sequence logic;
- rhythmic drive and changing density;
- short-note/long-note contrast;
- delayed climax;
- meaningful descent or thematic return.

Do not use different-pitch overlap to fake continuity. Ordinary Lead Guitar is
monophonic unless a deliberate double-stop/chord technique and safe channel strategy are
declared.

### 6. Realize only meaningful physical actions

- `hammer_on` / `pull_off`: reachable same-string groups.
- `slide`: a real connection into another fret or position, not periodic decoration.
- `bend`: enter an important target; keep the MIDI channel otherwise monophonic.
- `bend_release`: continue into the following pattern rather than acting as an ending
  stamp.
- `vibrato`: delayed and reserved for selected stable target notes.
- repeated notes / pick accents: preserve the rhythmic engine of the hand.

## Composition fields for an intentional hand path

The stable `melodic_lead` path supports optional explicit fingering on motif notes:

```json
{
  "pitch": "G4",
  "at": "9:1",
  "duration": 0.5,
  "velocity": 99,
  "articulations": ["slide", "accent"],
  "planned_position": "upper_12",
  "planned_string": 3,
  "planned_fret": 12,
  "slide_from_semitones": -2.0
}
```

`planned_string` is zero-based against the configured tuning. The compiler verifies that
the declared string/fret produces `pitch`; it rejects impossible pairs. Omit these fields
when fingering is not compositionally important and let the existing allocator choose.

`slide_from_semitones` is semantic performance intent. A pitch-bend-capable profile maps
it to a smooth approach curve. The MIDI channel safety gate suppresses pitch curves if
another note overlaps.

Never put library-specific keyswitch numbers in composition data.

## Arrangement around the lead

The guitar succeeds because the band supports its arc:

- Rhythm Guitar changes right-hand language by section: muted eighths, syncopated
  attacks, then open power-chord sustain. It stays out of the Lead's upper register.
- Bass connects harmony with roots, fifths, octaves, passing/approach notes and cross-bar
  motion. It aligns with selected kicks without copying every kick or rhythm-guitar hit.
- Drums maintain a clear backbeat, change cymbal/kick energy by section, and reserve fills
  for meaningful boundaries. The late solo should receive a real build.
- Organ/Pad is an optional plane. It supports space and climax without copying the Lead.
- A structural passage may remove Lead Guitar entirely; in that case another instrument
  must carry line-level motion rather than all accompaniment becoming chord blocks.

## Render-first diagnostic loop

For important guitar work, do not refactor from theory. Use:

```text
compose with current stable system
-> render real MIDI/WAV
-> inspect concrete bars and events
-> identify the smallest audible realization failure
-> change only that layer
-> regenerate the same song with the same seed/harmony/motif
-> compare
```

At minimum audit:

- active-bar ratio and continuous span;
- phrase islands under a documented gap threshold;
- rests over one beat and consecutive blank bars;
- automatic endings at four-bar boundaries;
- motif statements versus developments;
- exact repeated lick windows versus intentional sequence;
- density curve and peak bar;
- different-pitch overlap and same-pitch retrigger;
- bend/slide count and other active notes during pitch wheel;
- delayed vibrato rather than mechanical end stamping;
- whether planned string/fret/position survives compilation;
- rhythm-guitar, bass and drum independence.

Critic warnings are evidence, not musical law. A generic `melody_no_breath` warning must
not force a continuous guitar solo back into vocal phrasing. Record a justified exception
in `critique.md`; do not weaken the validator to hide it.

## What the reference V1/V2 proved

V1 already had a strong continuous melodic skeleton, but the realization layer silently
discarded authored fretboard positions and emitted no slide curves. The successful fix
did **not** add notes, change harmony, change seed, rewrite the rhythm section or relax
validation. It only:

1. preserved and validated `planned_string` / `planned_fret`;
2. preserved `slide_from_semitones` through the neutral/profile boundary;
3. emitted a smooth, channel-safe slide-in curve.

V1 and V2 therefore retained the same 744 Lead notes and identical rhythm-section MIDI,
while V2 gained 14 audible position-changing slide gestures. This is the preferred kind
of system improvement: a concrete musical intention survives the pipeline more faithfully.

Reference artifacts:

- `projects/guitar_native_rock_proof/core_motif.json`
- `projects/guitar_native_rock_proof/v1/validation_report.md`
- `projects/guitar_native_rock_proof/v2/validation_report.md`
- `projects/guitar_native_rock_proof/critique.md`
- `projects/guitar_native_rock_proof/comparison/v1_vs_v2.md`

Use the reference for principles and audit patterns. Do not copy its pitches, form,
density, E-minor harmony or exact fret path unless the new brief genuinely calls for it.

## Explicit anti-patterns

- vocal question/answer phrases with fixed breathing every two bars;
- full cadence and reset every four bars;
- random pentatonic notes or unrelated prefab licks;
- every new lick restarting in another register;
- long notes used as the only source of emotion;
- bend/vibrato mechanically stamped on every ending;
- random velocity/timing used to disguise weak phrase architecture;
- extensive overlap used to imitate legato;
- declared guitar fingering silently replaced downstream;
- adding more validators or architecture before rendering the actual song.

The target is a lead whose rhythm, contour, connection, climax and return could only
naturally have grown from an electric guitarist's hands.
