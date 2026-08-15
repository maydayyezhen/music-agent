# Guitar Performance Manuals Synthesis

> Source-study only. This document records reusable evidence distilled from three user-provided manual notes:
>
> - `shreddage3_midi_guitar_performance_notes.md`
> - `ample_guitar_midi_performance_notes.md`
> - `evolution_engine_midi_guitar_performance_notes.md`
>
> Do not load this file during ordinary composition. Promote only compact, style-neutral principles into active Skills or Agent API contracts.

## 1. Cross-source conclusion

All three sources converge on the same architecture:

```text
musical composition
-> guitar performance interpretation
-> physical/fingering decisions
-> articulation / transition / picking / strum realization
-> renderer-specific MIDI mapping
-> instrument / amp / FX / mix
```

The reusable lesson is not a keyswitch table. A guitar part is a **stateful performance program**, not a list of unrelated `pitch + onset + duration + velocity` notes.

## 2. Shared performance state

Useful semantic state includes:

- current hand / preferred fret position;
- string and fret candidates;
- active/ringing strings;
- previous pick direction;
- performance mode such as mono lead, poly chord, picking, or strumming;
- articulation and transition intent;
- tuning and capo environment;
- phrase role and section role.

String/fret choice is contextual. The same pitch can have different playability and timbre depending on string and position.

## 3. Fingering and physical legality

Promoted principles:

- prefer local hand continuity unless phrase intent requires a position shift;
- chord and lead parts need different fingering objectives;
- realistic mode should reject impossible same-string polyphony;
- open strings are special resources, not ordinary interchangeable duplicates;
- capo and alternate tuning modify the fingering/voicing environment rather than merely transposing output notes;
- forced string requests need legality fallback rather than blindly creating impossible fingerings;
- fretting position can serve timbral intent as well as playability.

## 4. Transitions are relationships

Hammer-on, pull-off, slide and related legato gestures are best represented as relations between notes.

Useful legality dimensions include:

```text
same-string feasibility
interval range
temporal overlap
minimum / maximum source hold time
voice context
explicit phrase intent
```

Do not infer `overlap == legato` universally. A picked transition may intentionally overlap for sequencing or sustain reasons.

Hammer/pull and slide should not share one universal interval threshold. Slides may legitimately span wider distances.

## 5. Expression

Useful semantic expression includes:

- bend target in musical semitones rather than raw pitch-wheel value;
- delayed vibrato with onset, rate and depth;
- slide speed as expressive time or tempo-synchronized time;
- release behavior and note-off intensity where supported;
- string bend and whammy-bar gestures as separate concepts when the renderer supports them;
- independent expressive voices / MIDI channels when polyphonic bend or legato isolation is required.

## 6. Picking

Picking is stateful.

Reusable modes evidenced across the manuals include:

```text
alternate
economy
beat-synced eighth
beat-synced sixteenth
down-only
up-only
```

A phrase break may reset alternate picking to downstroke. Fast lead passages should not be treated with chord-oriented lookahead, and attack energy should not be identical on every dense note.

## 7. Strumming

A chord and the act of strumming it are separate layers.

A useful strum semantic event contains independent dimensions such as:

```text
chord / voicing
stroke direction
string range / partial coverage
speed / total stroke time
strength
within-stroke velocity contour
articulation / mute amount
swing or subdivision context
perceptual beat anchor
controlled humanization
```

Slow strums should preserve perceptual beat alignment rather than simply starting every string exactly on the grid.

## 8. Humanization

Do not reduce realism to random timing and velocity jitter.

Prefer:

```text
groove intent
+ pick direction
+ metric accent
+ phrase position
+ hand/fret movement
+ controlled variation
+ sparse context-caused noises
```

Fret, release, stroke and resonance noises should have musical/physical causes and remain sparse.

## 9. Renderer separation

The sources strongly support semantic authoring followed by adapter mapping:

```text
Semantic Guitar Intent
-> Shreddage mapping
-> Ample mapping
-> Evolution mapping
-> Generic MIDI approximation
```

Do not store product-specific keyswitch notes as composition semantics.

Velocity is especially renderer-dependent: it may encode loudness, mute depth, slide speed, strum time, or another control. The semantic layer should therefore keep musical parameters separate and let the adapter decide how to encode them.

## 10. Relationship to existing project architecture

The repository already has a useful split:

- PMT stores performance-timed notes;
- `src/performance/gesture_ir.py` stores physical relationships PMT cannot express;
- Profiles map generic articulations to renderer-specific controls;
- composition remains structured and editable.

Do not create a second competing Guitar IR. Extend or document the existing performance/gesture layer when new executable capabilities are added.

## 11. Current promotion decision

Promote now:

- stateful guitar-performance reasoning;
- fingering/physical-legality principles;
- transition legality and note-to-note relationship model;
- picking-state reasoning;
- chord/voicing/strum separation;
- semantic-to-renderer adapter boundary;
- graceful degradation rules for generic MIDI.

Do not claim as fully executable until compiler/profile support exists:

- automatic string/fret assignment;
- per-note voice/channel allocation;
- full polyphonic bend;
- renderer-native strum trigger generation;
- automatic capo/tuning-aware chord voicing;
- all source-specific articulation condition systems.

These remain implementation targets rather than hidden promises.
