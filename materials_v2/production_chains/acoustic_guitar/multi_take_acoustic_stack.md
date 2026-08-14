---
id: multi-take-acoustic-stack
name: Multi-Take Acoustic Guitar Stack
kind: production_chain
status: active
---

# Multi-Take Acoustic Guitar Stack

## Identity

Build a thicker acoustic-guitar texture by combining two or three related guitar performances instead of forcing one track to carry all the density with extra pick noise, EQ or distortion.

Useful tags:

```text
layered
multi-take
double-track
triple-track
thick
coarse
rock
pop
guitar-bed
```

The goal is a composite guitar surface whose grain comes partly from tiny performance differences between layers.

## Two useful layering modes

### 1. Unison multi-take stack

Use two or three performances of essentially the same strumming part.

Each take should differ slightly in:

- stroke timing;
- velocity;
- chord width;
- string emphasis;
- source tone or damping;
- pick attack.

Do not duplicate the same rendered audio three times with fixed delays and call it three takes.

### 2. Complementary guitar bed

Use different but compatible guitar roles:

- one dense main steel-string strum;
- one sparse acoustic support or upper-string figure;
- optionally one clean, nylon or alternate guitar color for selected sections.

This mode creates width and harmonic detail without making every layer attack on every slot.

## Starting layout

For three unison-related takes:

```text
center anchor:  0 ms nominal offset, strongest level
left support:  -3 to -10 ms nominal offset
right support: +3 to +10 ms nominal offset
```

Add small **per-stroke** timing variation of roughly 1–4 ms around those offsets.

Keep the strings inside each stroke coherent. Do not apply independent random jitter to every note, which tears one hand gesture into unrelated events.

## Level and velocity differences

Useful starting relationships:

```text
center take: reference level
side takes:  roughly 3–7 dB below center each
velocity offset between takes: about 3–10 MIDI velocity units when MIDI-driven
```

Do not make all takes hit identical velocity layers. Small differences help the stack avoid sounding cloned.

## Voicing differences

The takes may share the same harmony while varying:

- one omitted bass string;
- one omitted upper string;
- slightly different partial-stroke coverage;
- one shared high common tone;
- one take remaining sparse where the main take is broad.

Avoid changing so many chord tones that the layers stop reading as one harmonic gesture.

## Panning and width

For a coherent guitar bed:

```text
center: near center
left/right support: roughly 20–50% L/R
```

Wider settings can work for a deliberate wall of guitars, but hard panning is not mandatory.

A complementary sparse guitar may be placed farther to one side than the main strum if the arrangement needs separation.

## Tone differences

Small contrasts are more useful than three radically different instruments.

Examples:

- center take: fuller body;
- left take: slightly darker or softer attack;
- right take: slightly brighter or shorter release.

The stack should still read as one family of guitar sounds.

## Bus glue

After the layers are balanced, process the guitar bus rather than over-processing each take independently.

Useful starting points:

```text
compression ratio: 1.5:1–3:1
attack:             10–30 ms
release:            60–150 ms
gain reduction:     about 1–4 dB on stronger passages
saturation:         subtle
```

The bus should glue the takes without erasing their micro-differences.

Short shared ambience can help the layers inhabit one space, but layering itself should provide most of the thickness.

## Why this can create grain

A single close guitar can become artificially clicky when grain is pursued by raising pick noise.

Multiple real or independently synthesized takes create a different kind of grain:

- attacks are nearly aligned but not identical;
- velocity layers differ slightly;
- string decay differs slightly;
- spectral emphasis differs slightly;
- the layers interfere and reinforce dynamically rather than as a static chorus effect.

This produces coarse density without requiring an exaggerated transient on one track.

## Failure modes

### Chorus / comb-filter sound

Likely causes:

- the same audio was copied rather than independently performed;
- delays are static and too small;
- all layers have identical spectrum and envelope.

Fix by using independent takes or independently generated stroke-level variation.

### Blurry rhythm

Likely causes:

- timing offsets too large;
- per-note jitter instead of per-stroke jitter;
- side takes too loud;
- too much shared room.

### Huge but hollow

Likely causes:

- side layers are phasey copies;
- center anchor is too weak;
- low-mid body has been removed from every take.

### Too much pick chatter

Likely causes:

- each layer already has aggressive synthetic pick noise;
- the stack multiplies those transients.

Reduce pick noise per layer first. Let the multi-take differences provide part of the grain.

## Listening checklist

Accept the stack when:

- the guitar feels thicker without obviously hearing three separate clones;
- the center still anchors timing and harmony;
- side layers add motion and texture rather than rhythmic blur;
- strong strokes feel coarse and energetic without plastic clicking;
- reducing the bus level still leaves a readable strumming pulse;
- mono collapse does not destroy the part.

## Provenance boundary

This technique was added after a successful three-layer synthetic A/B experiment in the current Music Agent work.

The user-provided MIDI also contains several guitar-program tracks, including a dense steel-string track plus additional steel-string, nylon-guitar and clean-guitar material in later sections. That supports the general idea that the perceived guitar bed may be composite.

The MIDI does **not** prove how the commercial recording was multitracked, miked, compressed or panned. Those production details must not be claimed from MIDI alone.
