---
name: bass-line-continuity
description: Write bass parts as supportive musical lines with harmonic anchors, contour, connective motion, motif identity and controlled articulation instead of default root-note reporting.
status: active
---

# Bass Line Continuity

## Purpose

Use this Skill for ordinary electric/synth bass writing, not only for explicitly "smooth" or "melodic" bass requests.

Default posture:

```text
bass foundation
+
small amount of phrase identity
```

Unless the user or style explicitly asks for a mechanical root pulse, drone, pedal, ostinato or deliberately minimal bass part, the bass should usually contain at least a little contour, approach motion, pickup behavior or recurring melodic identity.

This does **not** mean turning the bass into a solo instrument. The amount of melodic information is an arrangement parameter.

The central distinction is:

```text
sounding continuity != motion continuity
```

- **Sounding continuity** comes from note gate, overlap, release, pedal/controller behavior and renderer response.
- **Motion continuity** comes from pitch contour, rhythmic syntax, approach/connecting notes, motif identity and phrase direction.

A bass line can feel very smooth even when adjacent MIDI notes do not overlap. Do not force legato merely because the user asks for a connected bass sound.

## Source evidence

This Skill is currently supported by two user-provided MIDI studies with contrasting articulation.

### Study A: flowing melodic-support bass

Observed in the studied bass channel:

- 516 completed notes;
- GM program 35;
- pitch range MIDI 26-48;
- no CC64 sustain events and no pitch-wheel events on the bass channel;
- median note duration about 0.70 beat;
- median onset spacing 1.0 beat;
- median gap from one note-off to the next note-on about 0.22 beat;
- 0.5-beat and 1.5-beat onset gaps were especially common;
- about 36% of adjacent notes repeated the same pitch;
- about 25% moved by one or two semitones, excluding repeats;
- about 96% of adjacent moves stayed within five semitones.

This supports the idea that a smooth bass line can be built from relatively long anchors, nearby connective motion and rhythmic alternation without MIDI overlap or pitch-bend effects.

### Study B: groove-motif melodic bass

Observed in the second studied bass track:

- 730 completed notes;
- GM program 38;
- pitch range MIDI 24-55;
- no CC64 sustain events and no pitch-wheel events on the bass track;
- median note duration about 0.22 beat;
- median onset spacing 0.5 beat;
- median note-off to next-note-on gap about 0.28 beat;
- 0.5-, 0.25- and 0.75-beat onset gaps dominated;
- about 11% of adjacent notes repeated the same pitch;
- about 49% moved by one or two semitones, excluding repeats;
- about 67% stayed within five semitones;
- octave moves were prominent: 111 adjacent moves were exactly one octave, with more upward than downward octave jumps;
- velocity remained comparatively stable, roughly 98-110 with median about 101.

This supports a different route to continuity: short notes can still form a coherent bass phrase when the rhythm, stepwise contour, recurring motif and purposeful octave displacement are strong.

The exact source melodies, harmony and complete rhythmic sequences remain source-specific and are not promoted here.

## Core model

Think of a bass phrase as three interacting layers.

### 1. Harmonic anchors

Anchors establish the current harmonic floor. They may be roots, chord tones or stable pedal tones.

Anchors should remain easy to hear, but they should not automatically consume every attack in the phrase. A line that only reports the root at every beat is valid when deliberately requested, but should not be the universal default.

### 2. Connective motion

Use nearby motion to lead between anchors:

- repeated pitch with changed rhythm;
- semitone or whole-tone approach;
- neighboring tone;
- small chord-tone movement;
- short pickup into the next anchor;
- descending or ascending contour across several attacks.

For a smooth supportive style, prefer local motion most of the time and make larger jumps structural events rather than routine connectors.

### 3. Phrase identity

The bass should normally retain at least a small recognizable rhythmic or contour idea across a section.

A motif may be defined by:

- onset pattern;
- contour shape;
- anchor/connective relationship;
- characteristic approach movement;
- occasional octave lift or drop.

Phrase identity can be extremely small. A recurring two-note pickup, a characteristic descent, one approach gesture before chord changes, or a repeated rhythmic answer can be enough.

Do not randomize every bar. Variation should preserve enough identity that the bass sounds like one player developing one idea.

## Melodic-information budget

Treat bass melodicism as a continuous control, not an on/off style switch.

A useful conceptual scale is:

```text
0  = pure anchor / pedal / deliberately mechanical pulse
1  = mostly anchors with one recurring pickup or approach gesture
2  = supportive contour with several connective notes
3  = clearly melodic supporting bass with recognizable motif
4  = bass-forward riff or hook
5  = foreground / solo bass
```

For ordinary accompaniment, start around **1-2**, then adjust to the arrangement. This number is a planning aid, not a validator target.

Section examples:

```text
quiet verse       -> 1
normal verse      -> 1-2
open chorus       -> 1-2, possibly stronger contour but not necessarily more notes
instrumental gap  -> 2-3
busy lead section -> keep identity, remove nonessential connectors
breakdown/pedal   -> 0-1 when musically intentional
```

Do not equate section energy with more bass notes. A chorus may stay rhythmically simple while its contour or register becomes slightly more expressive.

## Decision procedure

1. Decide the bass role and melodic-information budget for the current section.
2. Mark the harmonic anchors before writing connective notes.
3. Give the phrase a contour. Ask where it is going over two or more beats, not only which chord is active now.
4. Add a small identity device unless the arrangement intentionally calls for pure anchors: pickup, approach, neighboring motion, characteristic descent/ascent, rhythmic answer or motif fragment.
5. Prefer small interval motion for smooth supportive bass; reserve octave and larger jumps for emphasis, register reset or a deliberate groove gesture.
6. Build a repeatable rhythmic identity. Avoid default quarter-note root pulses unless the arrangement actually calls for them.
7. Allow repeated pitches when rhythm or duration makes them meaningful. Melodic does not mean changing pitch on every attack.
8. Establish phrase logic before adjusting note overlap. Use gate and release to support the line, not to manufacture a line that is compositionally disconnected.
9. Coordinate with kick and accompaniment, but do not copy either track mechanically. Bass may anticipate, answer or bridge between their attacks.
10. In busy arrangements, reduce connector/fill density before removing the bass phrase identity itself.

## Default supporting behavior

For ordinary bass accompaniment, a useful baseline is:

```text
clear harmonic anchors
+ one small recurring contour idea
+ selective nearby connection
+ rhythmic breathing
```

Examples of tiny identity devices:

- descend by one or two nearby notes before a recurring anchor;
- use the same two-note pickup at selected phrase endings;
- approach the next root from a neighboring semitone or whole tone;
- repeat an anchor rhythmically, then answer with one nearby note;
- occasionally lift one structural pitch by an octave, then return.

These are options, not a fixed phrase template.

## Smooth-support starting behavior

When the requested character is connected, rounded and slightly melodic, a useful starting direction is:

```text
stable anchor
+ nearby connective movement
+ occasional pickup into the next harmony
+ mixed long and short durations
+ recognizable contour
```

A useful rhythmic relationship may alternate shorter movement with longer space, for example a half-beat move followed by a longer hold or vice versa. Treat this as a family of gestures, not a fixed mask.

## Groove-motif starting behavior

When the bass should be more active and dance-like:

```text
shorter attacks
+ syncopated onset pattern
+ stepwise motif
+ recurring phrase identity
+ occasional octave displacement
```

Do not import the short-gate behavior into a smooth bass task automatically. Motif identity and octave color can be borrowed independently from articulation density.

## Failure modes

### Root-note autopilot

Symptom: the bass reports the correct root repeatedly because no other behavior was considered.

Fix: keep the anchors and add the smallest useful phrase identity: one pickup, approach, neighboring motion or contour turn. Do not rewrite the whole line.

### Mandatory melodicism

Symptom: the Agent forces passing notes into a section whose musical purpose is pedal-like, minimal or mechanically repetitive.

Fix: set the melodic-information budget to 0-1 intentionally. The rule is "consider phrase identity by default," not "decorate every bar."

### Fake legato

Symptom: all notes overlap, but the pitch sequence still sounds like unrelated chord labels.

Fix: repair contour and approach logic first; then set articulation.

### Bass solo syndrome

Symptom: every gap is filled and the bass competes with the lead.

Fix: keep phrase identity but remove nonessential connective notes, especially under active foreground melody.

### Random walk

Symptom: many different notes but no recognizable contour or motif.

Fix: define a small interval vocabulary and repeat/develop a phrase shape.

### Octave trampoline

Symptom: frequent octave jumps dominate a part that was intended to feel creamy or relaxed.

Fix: reserve octave displacement for occasional lift, register reset or section emphasis.

### Kick photocopy

Symptom: bass attacks exactly duplicate every kick hit and never form their own syntax.

Fix: keep some lock points but allow anticipation, sustain, pickups and independent connective motion.

## Validation

Inspect both note data and phrase structure.

Useful diagnostics include:

- adjacent onset-gap distribution;
- note-duration and note-off-to-next-note-on gap distributions;
- repeated-pitch ratio;
- stepwise-motion ratio;
- large-jump and octave-jump counts;
- contour over two- to four-bar windows;
- motif recurrence or transformed recurrence;
- anchor-note locations relative to harmony;
- bass/kick attack coincidence versus independent bass attacks;
- section-specific density, register and melodic-information budget.

Also perform a simple musical check:

> If the bass is soloed, can at least one small phrase tendency be recognized, while the harmonic floor remains obvious?

For a deliberately minimal/pedal bass part, explicitly allow the answer to be "no" rather than manufacturing decorative motion.

Do not turn the statistics from either source study into universal target percentages. They are contrasting evidence that several different MIDI articulations can produce coherent bass motion.

## Provenance

Promoted from user-provided MIDI studies of two contrasting smooth/groove bass references, plus subsequent listening comparison between fretless and finger-bass renderings. The studies support the separation between line design and timbre; they do not establish one mandatory bass sound. Exact source melodies, harmony and full rhythmic masks are intentionally excluded. Reusable source-specific patterns live in `materials_v2/` rather than in this Skill.
