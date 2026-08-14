---
id: warm-rounded-acoustic-strum
name: Warm Rounded Acoustic Strum
kind: timbre_recipe
status: active
---

# Warm Rounded Acoustic Strum

## Identity

A warm, rounded acoustic-guitar texture for flowing pop accompaniment. The attack should remain readable, but the guitar should not feel brittle, clicky or aggressively pick-forward.

Useful tags:

```text
warm
rounded
soft-edge
wood-forward
acoustic-pop
moderate-room
smooth-attack
```

This is a reusable listening target, not a reconstruction of a commercial recording.

## Evidence boundary

This card combines two kinds of evidence:

### User listening judgment

The user identified the studied MIDI render as a useful example of a common warm guitar-strumming character.

### MIDI evidence

The studied guitar track used:

```text
GM program 24: Acoustic Guitar (nylon)
CC7 volume: 117
CC91 reverb send: 79
CC93 chorus send: 0
```

Its velocity was almost fixed at 100, so the MIDI does not provide useful expressive-velocity evidence.

These settings show the MIDI arranger's intended General-MIDI color. They do not prove the real instrument, microphone, EQ, room or processing used in any commercial recording.

## Source choice

Useful starting sources include:

- a nylon-string acoustic with enough definition for strumming;
- a mellow steel-string with softened pick attack;
- an acoustic sample with natural wood body and restrained upper-mid bite.

Avoid sources whose identity is dominated by:

- sharp plastic pick clicks;
- very bright 5-10 kHz fizz;
- huge stereo ambience;
- long cinematic reverb;
- extremely soft attack that erases the rhythm.

## Texture axes

Use these as descriptive targets:

```text
warmth:          0.70-0.90
wood body:       0.60-0.80
pick definition: 0.30-0.55
brightness:      0.35-0.58
low-mid weight:  0.50-0.70
room amount:     0.18-0.38
stereo width:    0.15-0.35
saturation:      0.05-0.15
```

A useful relationship is:

```text
wood body > pick click
```

while still keeping enough attack for the subdivision rhythm to remain clear.

## EQ starting points

### Low end

High-pass only as much as the arrangement needs:

```text
roughly 60-90 Hz
```

Do not over-filter the body.

### Warm body

Inspect roughly:

```text
160-350 Hz
```

A small broad lift can help a thin source, but remove mud rather than adding warmth blindly.

### Definition

Inspect roughly:

```text
1.8-4.0 kHz
```

Keep enough presence for strum timing. Avoid turning this band into hard pick chatter.

### Harshness

Inspect roughly:

```text
5-8 kHz
```

Reduce brittle edges when the source becomes too steel-like or synthetic.

## Compression

Use gentle control rather than aggressive transient emphasis:

```text
ratio:          1.5:1-2.5:1
attack:         20-40 ms
release:        80-180 ms
gain reduction: about 1-3 dB on stronger passages
```

The goal is stable warmth and continuity, not flattened dynamics.

## Room

Use a short or medium-small room that supports the guitar without moving it far away:

```text
decay:     roughly 0.45-1.0 s
pre-delay: 0-20 ms
wet level: low to moderate
```

The room may be more audible than in the dry pick-forward single-guitar recipe, but the rhythmic attacks must remain readable.

## Performance interaction

This timbre works especially well when the accompaniment uses:

- partial chord attacks;
- 2-5 sounded notes per stroke;
- sixteenth-grid motion with deliberate holes;
- common-tone retention;
- slightly narrower connective strokes than structural anchors.

Do not try to obtain warmth by making every note very long. Performance density and timbre should remain separate controls.

## Code-synthesis approximation

When using synthesis instead of samples:

- reduce the level and brightness of the synthetic pick transient;
- increase low-mid body resonance modestly;
- use a slightly softer excitation spectrum;
- allow a little more shared room than the dry single-guitar recipe;
- keep high-frequency decay faster than low-mid decay;
- vary each string enough to avoid glassy identical attacks.

## Failure modes

### Dull blanket

Likely causes:

- too little 2-4 kHz information;
- room too wet;
- attack envelope too slow;
- excessive low-mid buildup.

### Plastic warm preset

Likely causes:

- synthetic pick transient still too detached;
- static identical samples;
- excessive chorus instead of real performance variation.

### Bright steel-string drift

Likely causes:

- too much upper-mid pick definition;
- 5-8 kHz left uncontrolled;
- body carved too aggressively.

## Pairing

A strong pairing is:

```text
warm-pop-sixteenth-strum
+
warm-rounded-acoustic-strum
```

Use multi-take layering only when additional width or density is needed. Warmth itself does not require stacking several guitars.