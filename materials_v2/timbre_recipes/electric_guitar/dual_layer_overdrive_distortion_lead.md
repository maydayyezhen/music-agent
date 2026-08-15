---
id: dual-layer-overdrive-distortion-lead
name: Dual-Layer Overdrive + Distortion Lead
kind: timbre_recipe
status: active
---

# Dual-Layer Overdrive + Distortion Lead

## Identity

A foreground electric-guitar lead texture built from two closely aligned monophonic layers:

```text
primary overdriven lead
+
quieter distortion reinforcement
```

The two layers share the same musical phrase and pitch identity. Their differences come from source character, velocity / expression hierarchy, a narrow stereo split and very small timing differences.

Useful tags:

```text
lead-guitar
overdrive
distortion
dual-layer
reinforced
wide-but-focused
same-pitch-doubling
expressive
foreground
```

Use this recipe when one generic GM guitar patch sounds too thin, small or synthetic for a singing rock lead, but a full multi-take wall would be too diffuse.

This is a **timbre and realization recipe**, not a melody template. Pair it with `lead-guitar-phrase-design` for phrase writing and `expressive-target-note` for selective bend-arrival behavior.

## Core invariant

Compose and validate one lead-guitar phrase first. Then realize that same semantic phrase on two independent channels.

```text
one phrase design
-> two aligned realizations
-> controlled layer differences
```

Do not independently improvise the reinforcement layer. Random pitch divergence turns the texture into harmony or counterpoint and destroys the focused single-player identity.

## Layer roles

### Primary layer: overdriven lead

The primary layer carries:

- the clearest picked attack;
- the stronger velocity and expression profile;
- the most direct melodic identity;
- the reference timing for note starts, releases and bends.

For a General MIDI fallback, GM Program 29 in zero-based numbering (`Overdriven Guitar`) is a compatible starting point.

### Reinforcement layer: distortion body

The secondary layer carries:

- additional body and sustain density;
- a rougher distorted edge;
- stereo reinforcement around the primary;
- support for held targets without becoming a second foreground melody.

For a General MIDI fallback, GM Program 30 in zero-based numbering (`Distortion Guitar`) is a compatible starting point.

These program numbers are renderer-dependent starting points, not guarantees of identical tone across SoundFonts.

## Alignment behavior

Pitch and phrase structure should normally match exactly between layers.

A practical starting behavior is:

```text
pitch:               identical
primary onset:       phrase reference
secondary onset:     usually identical
secondary delay:     occasional 4–12 ms, not every note
release:             usually aligned
secondary release:   occasionally a few ms earlier
```

Tiny offsets may reduce sterile duplication. They must remain below the point where the attack becomes a flam or slapback echo.

Do not add a fixed delay to every note. The reference texture was mostly synchronous, with only occasional micro-offsets.

## Dynamic hierarchy

The reinforcement layer should usually be clearly quieter at the MIDI-performance layer before any audio processing.

A useful generic relationship is:

```text
primary velocity
>
secondary velocity
```

For the studied source, the most common difference was about 16 MIDI velocity units, while the hardest attacks used a smaller gap. Treat this as calibration evidence, not a universal constant.

Practical adaptation:

- ordinary notes: start with the secondary around 10–18 velocity units lower;
- near-saturated accented targets: reduce the difference when the secondary disappears;
- if the tone becomes fuzzy and masks pitch definition, lower the secondary first;
- if both layers trigger the same sample character, increase the contrast or use a different source.

Do not make both channels numerically identical and expect the program name alone to create depth.

## Stereo and depth

Keep the result wider than a single centered patch but narrower and more focused than rhythm-guitar double tracking.

A useful shape is:

```text
secondary   center   primary
    \          |          /
     narrow stereo opening
```

The studied MIDI placed the two layers on opposite sides of center rather than hard-panning them. Preserve that relative principle.

A General MIDI calibration starting point from the source was:

```text
primary overdrive:
  CC7 volume       72
  CC10 pan         71
  CC11 expression  127
  CC91 reverb      80
  CC93 chorus      0

secondary distortion:
  CC7 volume       72
  CC10 pan         55
  CC11 expression  110
  CC91 reverb      72
  CC93 chorus      0
```

These exact values belong to one MIDI / renderer context. The reusable relationship is:

```text
primary
-> stronger expression
-> one side of center

secondary
-> lower expression
-> opposite side of center
-> similar or slightly drier depth
```

Do not infer EQ, compression, amplifier, cabinet or microphone settings from these MIDI controllers.

## Expression mirroring

Because ordinary MIDI pitch bend is channel-wide, each layer must live on its own channel if both need the same expressive pitch trajectory.

Recommended realization:

```text
primary note + primary bend curve
secondary note + mirrored secondary bend curve
```

Use the same musical destination on both layers. Minor event staggering is acceptable only when it does not create audible pitch beating or a split bend.

For generic GM work, follow `expressive-target-note`:

- phrase design comes first;
- select only important held targets for bend;
- set a known pitch-bend range;
- when bending into a target, start from a lower base pitch;
- hold the reached bend through note-off;
- reset after note-off;
- omit CC1 vibrato unless the exact renderer has passed listening validation.

Do not spray bend or modulation across every passing note merely because two expressive channels are available.

## Renderer adaptation

### General MIDI / SoundFont

Start with Overdriven Guitar + Distortion Guitar on separate channels. Copy the same semantic note stream, then apply the layer hierarchy above.

If the SoundFont makes the distortion layer buzzy or nasal:

1. lower its expression or velocity;
2. narrow its register contribution if needed;
3. try a compatible crunch / distortion source;
4. keep the same role relationship instead of protecting the exact GM program number.

### Dedicated guitar sampler

Do not assume two duplicated sampler instances automatically sound like two physical takes. Round-robin behavior, fretboard allocation, humanization, pick direction and amp chains may require renderer-specific control.

If one sampler can already produce a layered amp or dual-source lead internally, use that implementation when it preserves the same audible invariant.

### Audio amp chain

A single DI performance split into two amp paths may realize the same concept:

```text
clearer overdrive path
+
quieter heavier distortion path
```

That is a valid adaptation, but this Material does not prescribe amp, cabinet, microphone, EQ or compression settings because the MIDI evidence cannot establish them.

## Failure modes

### Two equally loud plastic guitars

Symptom: the tone becomes louder but not deeper, and attacks feel synthetic.

Fix: restore a clear primary / reinforcement hierarchy. Lower the distortion layer before boosting the lead bus.

### Flam doubling

Symptom: every note has a repeated pick attack.

Fix: remove fixed delay. Keep most onsets aligned and use only occasional micro-offsets.

### Wide rhythm-guitar smear

Symptom: the melodic center becomes vague because the layers are hard-panned.

Fix: move both parts closer to center. This recipe is a focused lead, not a rhythm wall.

### Split bends

Symptom: one layer reaches the target before the other, producing beating or two apparent pitches.

Fix: mirror bend destinations and timing across the independent channels.

### Distortion masks note identity

Symptom: held targets become fuzzy and pitch movement is difficult to hear.

Fix: reduce secondary expression / velocity or choose a less saturated reinforcement source.

### Program-number superstition

Symptom: the recipe is declared successful because Program 29 and 30 were selected, even though the actual SoundFont sounds wrong.

Fix: judge the audible roles. Preserve clear-overdrive primary plus quieter-distortion reinforcement, not the patch labels.

### Melody copied into reusable knowledge

Symptom: a source lick, exact rhythm sequence or full phrase appears in the Material.

Fix: keep source melody project-specific. Promote only layering, controller relationships and realization behavior.

## Validation

Before accepting the texture, check:

- both layers use the same intended pitches and phrase boundaries;
- the primary remains intelligible when both channels play;
- the secondary is audible as body, not as a competing melody;
- onset offsets do not create flams;
- pan creates width without losing the melodic center;
- mirrored bends reach the same destination;
- pitch-wheel resets occur after note-off unless a fall is intentional;
- CC1 or other modulation is present only after renderer-specific listening validation;
- the result is compared with each layer soloed and with the full pair;
- the recipe still works when the musical phrase changes.

A compile success proves only that the MIDI is valid. Listening remains authoritative.

## Study provenance

This Material was abstracted from the user-provided Type-0 MIDI file `01_OPENING_GUITAR_EXACT_trimmed(1).mid`.

Measured source facts:

- 384 ticks per quarter note;
- approximately 54.99 BPM;
- one GM Program 29 Overdriven Guitar channel and one GM Program 30 Distortion Guitar channel;
- 38 note attacks on each layer;
- identical pitch sequence and pitch range 60–76 on both layers;
- 33 of 38 attacks were exactly simultaneous;
- five secondary attacks were delayed by 4 ticks, about 11 ms at the source tempo;
- most releases aligned, with three secondary releases 4 ticks earlier;
- the primary layer was louder in velocity on every paired note;
- the common primary-minus-secondary velocity difference was 16, with smaller differences on several saturated accents;
- both layers contained 104 pitch-wheel events;
- the primary contained 101 CC1 events and the secondary contained 100;
- no sustain-pedal behavior was used;
- initial controller values were the calibration values listed in the stereo and depth section;
- the file also contained Roland GS SysEx initialization, which remains renderer-specific and is not required by this Material.

The original melody, exact note sequence and complete expression curves remain source-specific and are not encoded here.

## Promotion boundary

Promote only this invariant:

```text
focused singing lead
=
clearer stronger overdrive layer
+
quieter distortion reinforcement
+
mostly aligned same-pitch performance
+
small stereo and dynamic differences
+
mirrored, selective expression
```

Do not promote one SoundFont, exact commercial tone, fixed controller values or the studied melody as universal knowledge.
