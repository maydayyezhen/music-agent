# Guitar Performance Agent API

This document describes the creative-safe contract for guitar performance semantics.

It exists to prevent composition Agents from opening implementation source merely to discover what the current performance layer can and cannot execute.

## Architecture

```text
composition
-> guitar performance interpretation
-> executable composition fields / gesture sidecar
-> selected Profile
-> MIDI / renderer mapping
```

Do not put product-specific keyswitch notes into composition data.

## Current composition-level executable subset

The ordinary composition contract already permits note-level realization metadata through authored phrase note overrides.

Relevant fields include:

```text
action
gesture
velocity
velocity_delta
bend_semitones
slide_from_semitones
vibrato
```

Profile realization also supports event-level `articulations` where the selected Profile provides a mapping or fallback.

Pitch-bend realization depends on the selected Profile declaring pitch-bend support and a compatible bend range.

Do not invent additional note-override fields unless the implementation/debug task updates the contract and compiler together.

## Existing Gesture IR sidecar

The repository already provides:

```text
src/performance/gesture_ir.py
```

Schema:

```text
music-agent-gesture-ir
schema_version: 1
```

Current supported action kinds:

```text
pick
hammer_on
pull_off
slide
vibrato
release
```

This sidecar exists because PMT note events alone cannot preserve every physical relationship.

Conceptually:

```text
PMT / notes
= what notes sound and when

Gesture IR
= how notes are physically related or articulated
```

### Transition requirements currently encoded by Gesture IR

`hammer_on`, `pull_off`, and `slide` require:

```text
from_pitch
to_pitch
positive transition_ms
retrigger: false
```

`vibrato` currently requires semantic parameters for:

```text
delay_ms
rate_hz
depth_cents
```

The sidecar may also associate a gesture with `string_index`.

## Semantic authoring model

When reasoning about guitar performance, the Agent may conceptually plan richer state such as:

```text
performance mode
hand / preferred fret position
string / fret candidates
ringing strings
pick direction
tuning
capo
transition intent
strum direction / coverage / speed
```

However, conceptual planning is not the same as executable compiler support.

Do not claim that the current composition compiler automatically performs:

```text
full string/fret assignment
automatic hand-position optimization
capo/tuning-aware chord voicing
per-note polyphonic bend-channel allocation
native sampler strum-trigger generation
```

unless the relevant implementation/debug task has added and tested those capabilities.

## Renderer / Profile boundary

Profiles own product-specific realization details such as:

```text
keyswitch
CC
velocity mapping
pitch-bend range
fallback gate/velocity behavior
```

The semantic layer should say:

```text
palm_mute
hammer_on
slide
bend target +2 semitones
```

not:

```text
send C#0
send CC X
send pitchwheel 8191
```

unless writing a renderer adapter or profile itself.

## Graceful degradation

When the requested performance detail exceeds the selected renderer's capability, use this preference order:

```text
native renderer behavior
-> documented Profile mapping
-> musically conservative MIDI approximation
-> preserve the composition and omit unsupported ornament
```

Never replace an unsupported gesture with random ornamentation.

Examples for General MIDI / SoundFont approximation may include:

- note overlap/gate shaping for connected phrasing;
- explicit small onset spreads for ordinary-sample strums;
- partial chord note sets;
- velocity shaping for attack hierarchy;
- pitch bend only where the Profile supports it;
- simpler picked realization when native hammer/pull/slide samples are unavailable.

A fallback is an approximation, not proof of realistic guitar synthesis.

## Relationship to active Skills

Use:

```text
lead-guitar-phrase-design
```

for musical lead phrase construction.

Use:

```text
acoustic-guitar-continuous-strumming
```

for strumming pattern / hand-clock design.

Then use:

```text
guitar-performance-model
```

for physical/performance interpretation and renderer-safe degradation.

Style Skills and Materials remain upstream. For example, Britpop knowledge may choose a half-arpeggio or two-guitar role design, while the guitar performance layer decides how that chosen part is plausibly played.

## Validation boundary

Always distinguish:

```text
musical quality
physical plausibility
renderer support
rendered sound quality
```

Passing one layer does not prove the others.

Listening remains the final validation for renderer-dependent realization.
