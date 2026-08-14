---
id: warm-pop-sixteenth-strum
name: Warm Pop Sixteenth Strum Family
kind: accompaniment_pattern
status: active
---

# Warm Pop Sixteenth Strum Family

## Identity

A flowing acoustic-guitar accompaniment built on a sixteenth-note hand-motion grid while leaving deliberate silent positions. The result should feel continuous and warm rather than frantic or percussive.

Useful tags:

```text
warm
pop
acoustic
sixteenth-grid
flowing
partial-strum
connected
```

This card is an abstracted accompaniment family. It does not store a finished song's exact bar pattern, chord progression, pitches or section order.

## Core behavior

Use a 4/4 sixteenth-note motion clock:

```text
1 e & a 2 e & a 3 e & a 4 e & a
```

The hand may move through all sixteen positions, but only a subset should sound.

A useful active-density range is roughly:

```text
9-13 audible attacks per bar
```

For a typical flowing pop version, 10-12 attacks per bar is a strong starting region.

Do not fill all sixteen positions merely because the grid exists.

## Attack hierarchy

Separate structural anchors from connective sixteenths.

### Structural anchors

Quarter-note and eighth-note positions can carry broader chord coverage:

```text
3-5 sounded chord tones
```

They establish harmony and meter.

### Connective sixteenths

Inner sixteenth positions are often narrower:

```text
2-3 sounded chord tones
```

They keep the right hand moving without making every attack a full chord.

This creates the useful relationship:

```text
broad anchors + narrow connective strokes
```

rather than:

```text
full chord x every attack
```

## Pattern construction

Build each bar from three ingredients:

1. stable anchor attacks on important beats or eighth-note positions;
2. one or more short clusters of adjacent sixteenth-note attacks;
3. deliberate holes that prevent the bar from becoming a solid machine-gun texture.

A cluster may contain two to four nearby sounding slots. Move or remove one connective stroke to make A/A' variants instead of replacing the whole rhythm.

Do not copy one reference bar verbatim. Generate a related pattern family from these constraints.

## Chord coverage and common tones

Repeated attacks should not always use the same pitch set.

Useful transformations include:

- broad chord -> middle partial;
- broad chord -> high partial;
- partial -> slightly broader answer;
- retain one or two common tones while changing another voice;
- omit a bass string on a connective stroke;
- refresh upper voices while lower compatible tones continue ringing.

A convincing connected texture often preserves part of the previous voicing while changing the sounded subset.

## Duration and connection

Gate length should follow the subdivision and the desired amount of ringing.

Useful starting behavior:

```text
sixteenth connective hit: around 70-100% of a sixteenth interval
longer anchor: around 70-100% of an eighth interval when the next retrigger permits
```

Do not interpret this as a requirement to cut every non-retriggered string. Compatible tones may continue ringing under later partial strokes.

## Dynamics

This material does not prescribe fixed absolute MIDI velocities.

Start from meter and phrase role:

- anchors stronger;
- inner connective strokes slightly lighter;
- occasional late-bar pickup may rise toward the next downbeat;
- reduce width before reducing every velocity when a vocal or lead needs room.

If a study MIDI uses nearly fixed velocities, do not promote that encoding shortcut into a reusable performance rule.

## Variation family

Create related bars by changing only a small number of dimensions:

- move one inner-sixteenth attack;
- turn one connective hit into an air stroke;
- thin one cluster from three notes to two;
- broaden one arrival stroke;
- extend or shorten one ringing common tone;
- reduce one cluster under a foreground phrase;
- restore density during a vocal rest or section lift.

The listener should recognize one accompaniment identity across several bars.

## Pairing

Works well with:

- warm or rounded acoustic timbres;
- suspended or open-string voicings;
- common-tone chord changes;
- light bass and vocal-led pop arrangements;
- multi-take layering at restrained levels when more width is needed.

Can also be adapted to steel-string sources by increasing attack definition while keeping the same broad-anchor / narrow-connective logic.

## Failure modes

### Too busy

Likely causes:

- all sixteen positions sounding;
- every connective hit using a broad chord;
- no intentional holes;
- excessive high-frequency attack.

### Too static

Likely causes:

- exactly the same pitch set on every attack;
- no change in chord width;
- no A/A' rhythmic variation;
- every bar using the same audible-slot mask.

### Too choppy

Likely causes:

- every note cut at each new attack;
- no common-tone retention;
- gates much shorter than the subdivision without a deliberate mute effect.

## Study provenance

This card was abstracted from a user-provided MIDI study of a warm pop acoustic-strumming arrangement.

Observed in the studied main acoustic-guitar track:

- 2048 note events formed 684 exact onset groups;
- onset groups contained 1-5 notes, with a median of 3;
- 0.25- and 0.50-quarter-note-beat attack gaps dominated;
- most full 4/4 bars used about 11-12 audible attacks on a sixteenth-note grid;
- inner-sixteenth attacks were somewhat narrower on average than quarter/eighth anchors;
- common note durations were 0.25 and 0.50 quarter-note beats;
- adjacent pitch sets frequently retained part of the previous voicing;
- the MIDI used nearly fixed velocity, so it was not treated as reliable evidence for expressive dynamics;
- simultaneous note onsets did not reveal physical down/up direction or string sweep timing.

The source's exact rhythmic mask, chord sequence and pitches are intentionally omitted.