---
name: guitar-performance-model
description: Interpret authored guitar music as a stateful physical performance before renderer-specific MIDI mapping, covering fingering, transitions, picking, strumming, expression and graceful fallback.
status: active
---

# Guitar Performance Model

## Purpose

Use this Skill whenever a composed guitar part must be realized as something a guitarist could plausibly perform.

This Skill does **not** decide the song's style, melody, harmony, riff identity or amp tone. Those belong to style Skills, melody/harmony Skills, guitar phrase/strum Skills, Materials and Profiles.

Its job is the middle layer:

```text
musical part
-> guitar performance interpretation
-> renderer mapping
```

The core rule is:

> Do not treat guitar MIDI as ordinary keyboard notes played through a guitar patch.

## Layer boundaries

Keep these separate:

```text
Composition
= what pitches, rhythms, chords and phrases the music needs

Performance
= how a guitarist physically realizes those musical events

Renderer mapping
= how the selected sampler / VST / General MIDI target encodes that performance

Tone / production
= amp, cab, distortion, EQ, delay, reverb, layering and mix
```

Do not use distortion or FX to hide a keyboard-like performance.

## Performance modes

Choose the mode from the musical role before applying guitar mechanics.

Useful modes:

```text
mono_lead
poly_chord
picked_pattern
strum
mixed_role
```

A track may change mode by section when the arrangement requires it.

### Mono lead

Priorities:

- phrase continuity;
- local hand position;
- physically plausible transitions;
- controlled attack density;
- intentional expressive targets.

### Poly chord

Priorities:

- playable simultaneous string assignment;
- chord voicing and inversion;
- ringing/common-tone behavior;
- position and tuning constraints.

### Picked pattern

Priorities:

- separate harmony from picking order;
- preserve picking state;
- allow open strings when the texture calls for them;
- keep repeated patterns related rather than randomly regenerated.

### Strum

Priorities:

- separate chord/voicing from stroke action;
- direction, coverage, speed and strength are independent;
- do not make all chord tones simultaneous unless the renderer itself supplies a native strum articulation.

## Stateful guitar model

Reason from context rather than mapping every note independently.

Conceptually track:

```text
hand position
preferred fret region
previous string / fret
active or ringing strings
previous pick direction
performance mode
phrase boundary
articulation / transition state
tuning
capo
```

Do not invent exact string/fret data when the current project and compiler cannot preserve it. Use this state as reasoning even when the output must degrade to generic MIDI.

## Fingering principles

1. Prefer fingerings near the current hand position unless a deliberate phrase/register shift justifies moving.
2. Avoid rapid arbitrary jumps across the fretboard.
3. Treat lead and chord fingering as different optimization problems.
4. Open strings are a texture/timbre choice, not automatically the best fingering.
5. A forced string/fret choice must remain physically legal; otherwise fall back to a valid candidate.
6. Capo and alternate tuning change the playable/voicing environment; do not model capo as simple MIDI transposition.
7. Fret position may serve timbral intent as well as playability.

The current project does **not** yet claim a complete automatic fingering compiler. These are authoring and validation principles until that implementation exists.

## Transition model

Treat legato gestures as **relationships between notes**.

Useful transition kinds:

```text
picked
hammer_on
pull_off
legato_slide
slide
bend_arrival
release
```

Before choosing a non-picked transition, consider:

```text
same-string feasibility
interval size
temporal overlap
source hold time
phrase intent
voice context
```

Do not use:

```text
if overlap: legato
```

as a universal rule.

A picked note may overlap a previous note for sustain reasons. Conversely, a requested slide normally needs enough overlap/timing support for the target renderer.

Hammer/pull and slide should use different interval expectations. Do not impose one global threshold.

## Attack-density control

Fast guitar does not mean every note receives the same full pick attack.

For dense lead phrases, distribute attack energy through combinations such as:

```text
picked
-> lighter picked connection
-> hammer / pull when physically plausible
-> slide when phrase intent supports it
-> picked re-entry at a structural accent
```

The goal is a connected line, not a row of identical per-note attacks.

Do not add legato merely to make a line smoother if the phrase itself wants repeated picked articulation.

## Picking state

Picking direction is performance state, not random decoration.

Useful reasoning modes include:

```text
alternate
economy
beat_synced_8th
beat_synced_16th
down_only
up_only
```

For alternate picking, a sufficiently clear phrase break may reset the next attack to downstroke.

If the target renderer cannot express pick direction, keep the intent semantic and degrade through subtle velocity/timing differences only when musically useful. Do not fake a renderer capability.

## Strum model

Represent the act of strumming separately from the chord.

Conceptual dimensions:

```text
direction
string / register coverage
full vs partial stroke
stroke speed
strength
mute amount
within-stroke dynamic contour
subdivision / swing context
perceptual beat anchor
```

A slow stroke is a timed performance event. Its perceptual anchor may be the first, middle or last important string depending on the intended feel.

Use `acoustic-guitar-continuous-strumming` for pattern/hand-clock design. This Skill handles physical realization after that pattern exists.

## Expression

Keep musical intent independent from raw MIDI encoding.

Prefer semantics such as:

```text
bend target: +2 semitones
vibrato: delayed, depth, rate
slide: expressive speed or tempo-synced duration
palm mute: amount rather than only true/false
release: controlled intensity
```

Renderer adapters decide whether those semantics become pitch bend, CC, velocity ranges, keyswitches, note-off velocity or another mechanism.

For bend-in targets, preserve the intended final musical pitch. Do not write the target pitch and then bend above it.

## Humanization

Do not equate realism with random jitter.

Prefer variation caused by:

```text
meter / groove
pick direction
stroke role
phrase position
hand movement
section energy
repetition context
```

Random micro-variation is the last layer, not the musical engine.

Fret/release/string noises should be sparse and physically motivated. Do not sprinkle noise uniformly.

## Renderer adapter boundary

The semantic layer must not hard-code product-specific keyswitch notes.

Desired flow:

```text
Guitar Performance Intent
-> selected Profile / Adapter
-> Shreddage / Ample / Evolution / Generic MIDI realization
```

Velocity is renderer-dependent and must not be globally interpreted as loudness. A renderer may use it for mute depth, slide speed, strum timing or another control.

## Current executable boundary

The repository already has two useful mechanisms:

1. ordinary composition/profile realization for articulations, bend and slide approximations;
2. `src/performance/gesture_ir.py` sidecar semantics for `pick`, `hammer_on`, `pull_off`, `slide`, `vibrato` and `release` relationships.

Use the existing Agent API contract for fields that are currently executable. Do not invent unsupported composition fields and pretend the compiler consumes them.

Full automatic string/fret assignment, capo/tuning-aware voicing, polyphonic per-note bend lanes and renderer-native strum compilation are **not yet guaranteed executable** by the current contract.

When a semantic gesture exceeds target capability, degrade gracefully rather than silently rewriting the music.

## Generic MIDI fallback

With a General MIDI / SoundFont target, preserve what is still meaningful:

- authored note/rhythm structure;
- phrase-level note overlap or separation;
- explicit string-like sweep timing when needed;
- partial chord voicing;
- velocity/gate shaping;
- supported pitch-bend gestures;
- section-level attack-density differences.

Do not claim GM has native string selection, sampled hammer-ons, true fret-position timbre or product-specific articulations.

A weak approximation should remain musically coherent and report unsupported realization rather than hallucinating fidelity.

## Decision procedure

1. Finish the musical part first: melody/riff/chords/rhythm/section role.
2. Choose guitar performance mode for the section.
3. Establish a plausible hand/position strategy conceptually.
4. Decide which transitions are picked versus legato/slide/bend according to phrase intent and physical plausibility.
5. Choose picking or strum behavior when relevant.
6. Add expression mainly at structural targets, phrase endings and intentional gestures.
7. Check the selected Profile before deciding how the intent can be encoded.
8. Use the Agent API's executable fields and existing Gesture IR where appropriate.
9. Degrade unsupported details explicitly; never substitute random ornamentation.
10. Judge the result by listening. A mechanically valid guitar program may still sound bad on a particular renderer.

## Failure modes

Revise when:

- every note is chosen independently with no hand-state continuity;
- a fast lead sounds like equally attacked keyboard dots;
- slide/hammer/pull are inserted randomly;
- impossible same-string polyphony is treated as realistic;
- chord notes and strum actions are conflated;
- every strum is six equal simultaneous notes;
- palm mute is treated as a universal binary switch when graded intent matters;
- velocity is globally assumed to mean loudness;
- product keyswitches leak into composition semantics;
- humanization is only random timing/velocity jitter;
- distortion is used to compensate for bad performance programming;
- the Skill claims full physical execution that the current compiler/profile cannot actually produce.

## Study provenance

This Skill is a cross-source abstraction from user-provided notes derived from:

- Impact Soundworks Shreddage 3 Stratus FREE manual;
- Ample Sound Ample Guitar manual;
- Orange Tree Samples Evolution Engine manual.

The three sources differ in product mechanisms but strongly converge on stateful fingering, transition semantics, picking/strumming behavior and renderer-specific mapping.

Exact keyswitch values and product-only behaviors remain Profile/adapter concerns rather than universal guitar rules.
