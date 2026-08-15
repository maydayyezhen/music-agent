---
id: expressive-target-note
name: Expressive Lead-Guitar Target Note
kind: instrument_gesture
status: active
---

# Expressive Lead-Guitar Target Note

## Identity

A lead-guitar arrival gesture in which an important held target note develops over time instead of behaving like a static MIDI block.

The reusable shape is:

```text
approach / burst
-> target note attack
-> early pitch shaping when musically needed
-> target establishes itself
-> delayed vibrato / modulation growth when supported
-> optional target re-articulation
-> release / next phrase
```

This Material describes the **musical lifecycle of an expressive target note**. It does not prescribe a specific song melody, bend interval, vibrato rate, plugin keyswitch or guitar tone.

Useful tags:

```text
lead-guitar
target-note
held-note
expressive-arrival
early-pitch-shaping
delayed-vibrato
re-articulation
phrase-tail
```

## Core behavior

Treat short connective notes and held arrival notes as different jobs.

Short notes usually carry motion toward or away from a target. Important held notes may carry a larger share of the expressive performance information.

Prefer:

```text
movement -> arrival -> development
```

rather than:

```text
same articulation intensity on every note
```

A held note is not empty time waiting to be filled with more pitches. Its pitch trajectory, stability, modulation envelope and possible re-pick can all be musical content.

## Stage 1: arrival

An expressive target should have a clear phrase reason to matter. It may be a harmonic anchor, color tone, high point, phrase tail, answer tone or other deliberate arrival.

Do not add expression merely because the note is long.

When pitch shaping is used near the attack, let it serve the arrival:

```text
nominal or approached pitch
-> continuous pitch motion
-> target region
```

The pitch motion may begin almost immediately after the attack or after a short establishment period depending on the phrase.

Do not automatically label every continuous pitch approach as a physical `slide`. MIDI pitch-wheel data alone may not reveal whether the player used a bend, slide, pre-bend release, whammy motion or another physical technique.

## Stage 2: establish the target

After the initial arrival gesture, allow the listener to perceive the target as a stable musical point.

Do not force continuous modulation from note-on simply to make the line sound more guitar-like.

A useful conceptual shape is:

```text
attack / pitch approach
________ target ________
```

before later expressive development.

## Stage 3: delayed vibrato or modulation growth

When the source, instrument Profile or current performance design supports vibrato, it may enter **after** the target has begun sounding rather than at the exact note-on instant.

Prefer an envelope concept such as:

```text
stable attack
-> delayed modulation onset
-> gradual growth
-> optional relaxation before release
```

Do not hard-code one universal delay, depth or growth time.

The important reusable distinction is:

```text
bend / pitch approach often belongs to arrival
vibrato / modulation often belongs to sustained development
```

They are not interchangeable decorations.

## Stage 4: optional target re-articulation

A held target may be followed by another picked attack on the same pitch before the phrase moves on.

This can reinforce the target without requiring a new pitch:

```text
target hold
-> same-pitch re-pick
-> continuation / answer
```

Repeated-pitch re-articulation is optional and source/style dependent. Do not turn it into a mandatory pattern.

## Expression density

Do not distribute expressive gestures uniformly across the lead line.

A useful hierarchy is:

```text
short connective notes
= primarily motion

important held targets
= stronger candidates for pitch shaping / modulation / re-articulation
```

This prevents the common failure mode where every note receives a bend, vibrato or slide and the lead becomes articulation noise.

## Separation from phrase design

This Material assumes the phrase already has a musical target.

Use phrase design first:

```text
short motion
-> target
-> phrase continuation / rest
```

Then decide whether the target deserves this expressive lifecycle.

Do not use expression to rescue a line with no contour, target-note logic or phrase boundary.

## Renderer / Profile boundary

This Material does not define how expression is encoded for a specific engine.

A target Profile may realize the same musical intent through:

- MIDI pitch wheel;
- CC-based modulation;
- per-note expression;
- sampler articulation;
- keyswitches;
- scripted bend or vibrato controls;
- another engine-specific representation.

Keep musical intent separate from renderer mechanics.

For ordinary channel-wide MIDI pitch bend, avoid applying independent simultaneous bends to polyphonic notes on the same channel unless the target system supports per-note pitch expression.

## Failure modes

### Expression sprayed everywhere

Symptom: short passing notes and long arrivals receive similar amounts of bend/vibrato.

Fix: concentrate expressive development on musically important targets.

### Vibrato from note-on by default

Symptom: every held note begins fully modulated at attack.

Fix: allow the note to establish itself; use delayed onset when the phrase and source support it.

### Bend without destination

Symptom: pitch wheel moves because the instrument is a guitar, but the motion has no target-note role.

Fix: make pitch shaping serve arrival, tension or release.

### Fake slide certainty

Symptom: any continuous pitch movement is labelled `slide` despite no string/fret or articulation evidence.

Fix: preserve the neutral concept `continuous pitch approach` until the physical technique is actually supported.

### Static long note

Symptom: an important target is held for a long duration but has no expressive development even when the chosen source/Profile can support it.

Fix: consider pitch shaping, delayed vibrato growth or a purposeful re-pick, but only when musically motivated.

### Mandatory re-pick

Symptom: every target note is automatically repeated at the same pitch.

Fix: keep re-articulation optional and phrase-dependent.

## Study provenance: user-provided Still Got The Blues MIDI

This Material was abstracted from a user-provided Type-0 MIDI study at 384 ticks per beat containing multiple layered electric-guitar channels.

Two major GM program 29 Overdriven Guitar channels supplied the strongest expression evidence.

Observed in zero-based channel 3:

- 428 note-on attacks;
- 1440 pitch-wheel events;
- 2233 CC1 modulation events;
- 110 notes lasted at least 0.7 quarter-note beats;
- every one of those 110 long notes contained pitch-wheel activity, CC1 activity, or both under the study's event-window analysis;
- among long notes with non-zero pitch shaping, first non-zero pitch-wheel activity occurred very near note attack, with median delay about 0.016 beat;
- among long notes with positive CC1 activity, first CC1 activity occurred later, with median delay about 0.56 beat;
- when both non-zero pitch-wheel and positive CC1 appeared inside the same long note, pitch-wheel activity preceded CC1 in all 56 analyzed cases;
- positive CC1 typically grew over time rather than appearing only as a single on/off switch; median time from first positive CC1 to that note's local CC1 maximum was about 0.33 beat.

Observed in zero-based channel 7:

- 784 note-on attacks;
- 1129 pitch-wheel events;
- 853 CC1 modulation events;
- 82 notes lasted at least 0.7 quarter-note beats;
- only one of those long notes contained neither pitch-wheel nor CC1 activity under the study's event-window analysis;
- among long notes with non-zero pitch shaping, first non-zero pitch-wheel activity had median delay about 0.083 beat;
- among long notes with positive CC1 activity, first CC1 activity had median delay about 0.48 beat;
- in 23 of 27 analyzed long notes containing both non-zero pitch-wheel and positive CC1, pitch-wheel activity began first;
- median time from first positive CC1 to that note's local CC1 maximum was about 0.31 beat;
- same-pitch re-articulation shortly after a long target occurred repeatedly in this channel, supporting it as an optional phrase device rather than a defect.

The source also contained strongly aligned overdriven and distortion-guitar layers, but that layering behavior is not encoded in this Material because timbral doubling and expression lifecycle are separate reusable concerns.

## Evidence boundaries

This source supports timing relationships between note attack, pitch-wheel activity and CC1 modulation. It does **not** establish universal physical-technique labels or universal numeric defaults.

Do not infer from this source alone:

- the exact bend interval represented by a given pitch-wheel value;
- a universal pitch-bend sensitivity;
- physical slide versus bend versus whammy technique from pitch wheel alone;
- real finger-vibrato rate or depth from CC1 values;
- a universal delay before vibrato;
- a universal percentage of long notes that require expression.

The source's exact melody, harmony, controller curves and song-specific phrase sequence are intentionally omitted.
