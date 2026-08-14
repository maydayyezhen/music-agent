---
name: acoustic-guitar-continuous-strumming
description: Write and revise subdivision-based acoustic-guitar strumming with explicit hand motion, stroke coverage, sustain and renderer separation.
status: active
---

# Acoustic Guitar Continuous Strumming

## Purpose

Use this skill for repeated acoustic-guitar strumming built on a regular subdivision grid, especially eighth-note and sixteenth-note accompaniment.

This is a text knowledge and decision skill. It does not require a trained model and it does not define the final guitar timbre. Timbre, layering and production belong in `materials_v2/`.

## Source evidence

### Study 1: dense steel-string subdivision pulse

The first studied MIDI sample should **not** be treated as proof of a continuous-eighth pattern.

Directly observed in its main steel-string guitar track:

- GM program 25 was used for the main dense acoustic-guitar track;
- 2743 note events formed 921 exact onset groups;
- compact chord groups were common, with a median of about three notes per onset;
- the most common adjacent attack gaps were 0.25 and 0.50 quarter-note beats, so both sixteenth- and eighth-spaced attacks were present;
- notes inside the same chord group began on exactly the same MIDI tick;
- therefore the MIDI preserved attack timing, pitch, velocity, duration and overlap, but did not preserve string-by-string sweep order.

This sample supports the idea of a dense subdivision-based chord pulse. It does not justify inferring down/up direction, sweep timing, or an eighth-note-only technique.

### Study 2: warm flowing sixteenth-grid pop strum

A second user-provided MIDI study added a different acoustic-strumming behavior family.

Directly observed in its main acoustic-guitar track:

- GM program 24 was used;
- 2048 note events formed 684 exact onset groups;
- onset groups contained 1-5 notes, with a median of 3;
- 0.25- and 0.50-quarter-note-beat attack gaps dominated;
- most full 4/4 bars contained about 11-12 audible attacks on a sixteenth-note grid rather than sounding all 16 positions;
- quarter/eighth anchor positions were somewhat broader on average than inner-sixteenth connective attacks;
- common note durations were 0.25 and 0.50 quarter-note beats, with a median duration of 0.50 beat;
- adjacent attacks frequently retained only part of the previous pitch set instead of repeating an identical block chord;
- velocity was almost fixed at 100, so this sample was **not** treated as reliable evidence for expressive dynamic shaping;
- notes inside an onset group were simultaneous, so physical down/up direction and string sweep timing remained unknown.

This sample supports several reusable ideas:

- a sixteenth-note hand clock can produce a flowing part with deliberate silent slots;
- accompaniment density and chord width are separate controls;
- inner-sixteenth connective attacks can be narrower than structural anchors;
- repeated strumming can preserve common tones while changing the sounded subset;
- one recurring pattern family can remain stable over many bars without making every bar identical.

The exact source rhythm mask, pitches and harmonic sequence belong to the source library and must not be copied into this Skill.

## General performance knowledge

The following rules are performance conventions, not facts recovered from the studied MIDI samples:

- choose a subdivision grid appropriate to the part, commonly eighths or sixteenths;
- continuous right-hand motion normally alternates down and up across that grid;
- a silent grid position may still contain an air stroke;
- downstrokes often cover more low and middle strings and may carry stronger structural accents;
- upstrokes are often narrower, lighter and biased toward middle or upper strings;
- chord changes do not automatically reset right-hand direction;
- compatible strings or voices may continue ringing through later attacks.

## Core representation

Treat strumming as three separate layers.

### 1. Hand-motion clock

For eighth notes in 4/4:

```text
1 & 2 & 3 & 4 &
D U D U D U D U
```

For sixteenth notes in 4/4:

```text
1 e & a 2 e & a 3 e & a 4 e & a
D U D U D U D U D U D U D U D U
```

The audible pattern is a subset of this physical clock. Do not restart the direction cycle merely because the bar, chord or phrase changed.

For flowing sixteenth-grid accompaniment, do not assume every slot should sound. A useful part may leave several positions as air strokes while retaining continuous hand motion.

### 2. Stroke action

A sounding slot may use:

- `full_strum`
- `low_partial`
- `middle_partial`
- `high_partial`
- `light_upstroke`
- `muted_strum`
- `ghost_strum`
- `single_string_restrike`

A non-sounding slot may use:

- `air_strum`

These are semantic actions, not fixed MIDI note lists.

### 3. Sound realization

The renderer decides:

- which chord tones realize the requested string group;
- whether the source needs explicit string-by-string onset spread;
- velocity and velocity gradient;
- duration and release behavior;
- retrigger and overlap handling;
- sampler articulations or synthesis details.

Do not hard-code sample-library keyswitches into the musical phrase.

## Decision procedure

1. Choose the subdivision from the musical task instead of assuming eighth notes.
2. Build the continuous D/U hand-motion clock.
3. Mark which grid positions sound and which are air strokes.
4. Assign stroke width and register coverage per sounding slot.
5. Treat structural anchors and connective attacks as different roles; connective sixteenths may be narrower.
6. Establish meter-aware dynamics before adding any humanization.
7. Preserve compatible ringing voices rather than cutting every chord at every attack.
8. At chord changes, release conflicting voices without resetting the hand clock.
9. Thin the guitar when a lead or vocal needs space.
10. Keep repeated bars related. Variation should transform a recognizable pattern rather than randomize every bar.

## Dynamics

Do not use one fixed velocity recipe for every style.

Useful relationships:

- structural downstrokes are often stronger than connective attacks;
- upstrokes are often lighter than nearby downstrokes;
- ghost or muted contacts are substantially lower;
- section energy, accompaniment role and the target instrument source determine the absolute velocity range.

When a reference MIDI is available, its velocity distribution may guide the current project only when that distribution contains meaningful variation. A nearly fixed-velocity export is evidence about encoding, not expressive performance.

Do not promote one song's exact velocities into a universal Skill default.

## Voicing and sustain

Continuous strumming should not be repeated copies of one full block chord.

Useful contrasts include:

- broad downstroke with bass support;
- narrow upper-string upstroke;
- low or middle partial connective stroke;
- ghost contact;
- single-tone refresh;
- longer compatible ringing voices under thinner re-attacks.

A partial stroke should retrigger only the selected voices when the renderer allows it. Shared tones may ring across chord changes when musically compatible.

A useful flowing-pop relationship is:

```text
broader structural anchors
+
narrower connective sixteenths
+
partial common-tone retention
```

Do not hard-code one source's exact chord-width sequence. Generate a related family from the current harmony and phrase role.

## MIDI realization

A fully quantized block chord can be a valid MIDI representation.

Do **not** assume that guitar realism always requires visible inter-string MIDI staggering. A sampler may contain a recorded strum inside one articulation, and some reference MIDIs intentionally quantize chord tones to the same tick.

When ordinary single-note samples or synthesis require explicit sweep motion:

- downstroke: use a small low-to-high onset spread;
- upstroke: use a small high-to-low onset spread;
- scale the spread with tempo and stroke width;
- keep it short enough that the result remains a strum rather than an arpeggio.

When the source evidence has simultaneous chord onsets, label direction and sweep timing as unknown unless another source supplies them.

## Common failure modes

Revise the part when:

- the subdivision was guessed incorrectly from a reference;
- a sixteenth grid is treated as a requirement to sound all sixteen positions;
- every attack uses the same full voicing;
- connective sixteenths are as broad and heavy as every structural anchor without a style reason;
- the right hand restarts at every bar or chord;
- up/down labels are invented from fully simultaneous MIDI blocks;
- all notes are cut mechanically at every new attack;
- accidental same-pitch overlap creates doubled notes or stuck notes;
- humanization is random rather than tied to stroke role and meter;
- visible MIDI staggering is forced even when the sampler already supplies a strum articulation;
- the guitar continuously duplicates a foreground melody or vocal rhythm.

## Validation checklist

Before accepting a generated part, verify:

- the declared subdivision matches the intended pattern;
- the D/U hand clock is internally continuous;
- sounding and silent slots are intentional;
- a sixteenth-grid part has deliberate holes when the style calls for flow rather than maximum density;
- stroke width varies meaningfully;
- structural and connective attacks have sensible width relationships;
- dynamics form a readable meter and phrase;
- partial strokes actually use fewer voices;
- note duration creates the intended amount of connection;
- chord changes do not leave incompatible sustained tones;
- renderer-specific sweep behavior is not confused with source MIDI evidence;
- repeated bars are related but not mechanically identical.

## Current status

This skill documents reusable acoustic-guitar strumming behavior across regular eighth- and sixteenth-note subdivision grids.

The first MIDI study contributed evidence for dense chord-pulse attacks, compact chord groups, strong velocity variation and note overlap.

The second strumming study added evidence for warm flowing sixteenth-grid accompaniment with deliberate holes, variable 1-5-note attack width, narrower connective sixteenths, common-tone retention and stable multi-bar pattern families.

Neither studied MIDI provided recoverable physical down/up direction or string-by-string sweep timing.
