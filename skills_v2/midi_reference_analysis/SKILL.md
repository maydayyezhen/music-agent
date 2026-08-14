---
name: midi-reference-articulation-analysis
description: Analyze reference MIDI articulation using notes, controllers, overlap and section context before promoting reusable knowledge.
status: active
---

# MIDI Reference Articulation Analysis

Use this Skill whenever a reference MIDI is studied for instrument behavior.

## Core rule

```text
raw note gate != audible duration
```

Do not infer staccato, legato, continuity or silence from Note On / Note Off alone.

## Required checks

For each studied track:

1. Identify track, channel, program, pitch range and musical role.
2. Measure onset spacing and onset-group width.
3. Measure raw note-on to note-off duration, but label it `nominal MIDI gate`.
4. Inspect CC64 sustain before interpreting any short gate as an audible gap.
5. Inspect CC7 and CC11 when automation may shape phrase tails or section level.
6. Check note overlap, same-pitch retrigger, held lower tones and near-contiguous note changes.
7. Consider renderer or sampler release behavior when available.
8. Determine section-level activation: always-on layer, section bed, fill, transition or sparse phrase.
9. Only then describe the perceptual articulation and promote a Material.

## Effective sounding behavior

Prefer descriptions such as:

```text
genuinely clipped pulse
continuous bed with re-articulation
nearly connected note chain
long phrase tail
phrase-level silence
```

When CC64 is active, reconstruct pedal-down intervals and compare them with note gates. A 0.4-beat gate inside an 8-beat sustain block is not evidence for a 0.4-beat audible stab.

## Same-program tracks

Do not merge tracks just because they use the same GM program. Two overdriven-guitar tracks may have completely different roles, such as continuous rhythm bed versus sparse sustained melody.

## Promotion rule

Preserve the musical invariant rather than one MIDI implementation.

For example, a continuous rhythm bed created in the source with CC64 may be generated with CC64, note overlap, longer release, or an amp/sampler envelope, provided the audible result stays connected.

## Failure modes

Revise the analysis when raw gate length is treated as audible length, CC64 is ignored, same-program tracks are conflated, or a section-only layer is generalized into an always-on part.

## Working maxim

```text
Reconstruct what is heard first.
Abstract the role second.
Teach the Agent third.
```
