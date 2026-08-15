---
id: expressive-target-note
name: Expressive Lead-Guitar Target Note
kind: instrument_gesture
status: active
---

# Expressive Lead-Guitar Target Note

## Identity

A lead-guitar arrival gesture in which an important held target note develops over time instead of behaving like a static MIDI block.

The reusable musical shape is:

```text
approach / burst
-> target-note arrival
-> optional early pitch shaping
-> target establishes itself
-> optional sustained development
-> optional target re-articulation
-> release / next phrase
```

This Material describes the **musical lifecycle of an expressive target note**. It does not prescribe a specific song melody, universal bend interval, vibrato rate, plugin keyswitch or guitar tone.

Useful tags:

```text
lead-guitar
target-note
held-note
expressive-arrival
bend-arrival
pitch-shaping
optional-vibrato
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

A held note is not empty time waiting to be filled with more pitches. Its pitch trajectory, stability and possible re-pick can all be musical content.

## Stage 1: choose a real target

An expressive target should have a clear phrase reason to matter. It may be a harmonic anchor, color tone, high point, phrase tail, answer tone or other deliberate arrival.

Do not add expression merely because the note is long.

Phrase design comes first. Expression must serve an already meaningful target.

## Stage 2: bend or pitch approach into the target

When a bend is intended to **arrive at** a target pitch, distinguish the played base pitch from the musical target pitch.

Prefer the semantic model:

```text
lower base pitch
-> progressive pitch rise
-> intended target pitch
```

Do **not** accidentally encode:

```text
intended target pitch
-> bend farther above the target
```

unless an intentional overshoot is actually part of the phrase.

For a renderer where pitch-wheel range is known, derive the base pitch and wheel destination from the intended target interval. Do not guess the relationship between pitch-wheel values and semitones when the bend sensitivity is unknown.

A bend curve may rise progressively instead of teleporting to the destination. The exact curve shape and duration remain style- and Profile-dependent.

Do not automatically label every continuous pitch approach as a physical `slide`. MIDI pitch-wheel data alone may not reveal whether the player used a bend, slide, pre-bend release, whammy motion or another physical technique.

## Stage 3: hold the reached target

After the bend reaches its target region, allow the target to remain stable long enough to read as the phrase arrival.

For ordinary monophonic MIDI pitch-bend realization, a safe default is:

```text
base note on
-> bend reaches target
-> hold target bend
-> note off
-> reset pitch wheel
```

Do not return the pitch wheel to center **before note-off** unless a falling release is an intentional audible gesture. Resetting early changes the sounding pitch and can create an unwanted downward tail.

This is an implementation-semantic rule, not a requirement that every held target use bend.

## Stage 4: optional sustained development

A held target may continue developing after arrival through a renderer-supported technique such as vibrato, modulation, a sampler articulation or another per-note expression mechanism.

The source study supports the musical distinction:

```text
pitch approach often belongs to arrival
later modulation can belong to sustained development
```

However, **do not treat generic MIDI CC1 as a universal guitar-vibrato implementation**.

For an unvalidated GM SoundFont or unknown Profile, prefer:

```text
phrase + target hold + purposeful bend
```

as the safe baseline.

Only add CC1-based vibrato after that exact renderer/Profile has been listening-validated for electric guitar. If CC1 produces unstable, synthetic or exaggerated high-register behavior, omit it rather than trying to rescue the phrase with more controller data.

Do not hard-code one universal vibrato delay, depth, rate or growth time.

## Stage 5: optional target re-articulation

A held target may be followed by another picked attack on the same pitch before the phrase moves on.

```text
target hold
-> same-pitch re-pick
-> continuation / answer
```

Repeated-pitch re-articulation is optional and phrase-dependent. Do not turn it into a mandatory pattern.

## Expression density

Do not distribute expressive gestures uniformly across the lead line.

A useful hierarchy is:

```text
short connective notes
= primarily motion

important held targets
= stronger candidates for pitch shaping / re-articulation / validated sustained expression
```

This prevents the common failure mode where every note receives a bend, vibrato or slide and the lead becomes articulation noise.

High-register notes deserve particular restraint when the renderer has not been validated there. Do not increase bend or modulation merely because a note is the phrase climax.

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

This Material does not define one implementation for every engine.

A target Profile may realize the same musical intent through:

- MIDI pitch wheel;
- validated CC-based modulation;
- per-note expression;
- sampler articulation;
- keyswitches;
- scripted bend or vibrato controls;
- another engine-specific representation.

Keep musical intent separate from renderer mechanics.

For ordinary channel-wide MIDI pitch bend, avoid applying independent simultaneous bends to polyphonic notes on the same channel unless the target system supports per-note pitch expression.

### Generic GM fallback

When no more specific guitar-expression Profile has been validated, use this conservative fallback:

```text
1. write the phrase and target pitches first
2. keep most notes unmodified
3. select only a few important monophonic targets for bend
4. if bending into a target, start from the lower base pitch
5. use an explicitly known bend range when possible
6. reach and hold the target through note-off
7. reset pitch wheel after note-off
8. omit CC1 vibrato unless that renderer has passed a listening test
```

This fallback is intentionally less expressive than an advanced sampler. Reliability is preferred over synthetic controller theatrics.

## Failure modes

### Target already written, then bent above itself

Symptom: the melodic target sounds correct at attack and then rises into an unintended sharp or alarm-like pitch.

Fix: if the musical intent is `bend into target`, write/realize a lower base pitch and use the bend to reach the target. Only bend above the target when overshoot is deliberate.

### Pitch-wheel reset before note-off

Symptom: a held bent note reaches the target, then audibly falls at the tail for no phrase reason.

Fix: keep the wheel at the target until note-off; reset after the note stops unless the fall is intentional.

### Unvalidated CC1 vibrato

Symptom: long or high notes acquire exaggerated synthetic wobble even though the underlying phrase is sound.

Fix: remove CC1 and return to the bend-only / held-note baseline. Reintroduce modulation only after renderer-specific listening validation.

### Expression sprayed everywhere

Symptom: short passing notes and long arrivals receive similar amounts of expression.

Fix: concentrate expressive development on musically important targets.

### Bend without destination

Symptom: pitch wheel moves because the instrument is a guitar, but the motion has no target-note role.

Fix: make pitch shaping serve arrival, tension or release.

### Fake slide certainty

Symptom: any continuous pitch movement is labelled `slide` despite no string/fret or articulation evidence.

Fix: preserve the neutral concept `continuous pitch approach` until the physical technique is actually supported.

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

## Listening validation: bend-only GM test

A follow-up generated MIDI test used the same phrase layer while isolating expression behavior. The user explicitly preferred the `BEND ONLY` version.

That accepted test used these implementation properties:

- no CC1 modulation;
- only a small number of selected monophonic mid-register targets used bend;
- pitch-bend sensitivity was explicitly set before interpreting wheel values as semitone motion;
- each bend-in target used a base MIDI pitch below the intended target rather than placing the note at the target and bending above it;
- the bend reached the target and stayed there through note-off;
- pitch wheel returned to center only after note-off;
- high-register targets were left free of extra bend in that isolation test.

Promote from this listening test only the **semantic safety rules** above. Do not promote the test's exact number of bends, register cutoff, one-semitone interval or controller curve as universal style rules.

The test validates bend-only realization as a safe current baseline for the repository's generic GM electric-guitar workflow. It does not prove that CC1 is universally wrong for guitar; it means CC1-based vibrato remains renderer-specific and unvalidated for this fallback path.

## Evidence boundaries

The source MIDI supports timing relationships between note attack, pitch-wheel activity and CC1 modulation. The follow-up listening test supports a conservative bend-only realization in the current generic GM workflow.

Do not infer from these alone:

- a universal bend interval;
- a universal pitch-bend sensitivity;
- physical slide versus bend versus whammy technique from pitch wheel alone;
- real finger-vibrato rate or depth from CC1 values;
- a universal delay before vibrato;
- a universal register above which bending should stop;
- a universal percentage of long notes that require expression.

The source's exact melody, harmony, controller curves and song-specific phrase sequence are intentionally omitted.
