---
id: sustained-overdrive-guitar
name: Sustained Overdrive Guitar
kind: instrument_gesture
status: active
---

# Sustained Overdrive Guitar

## Identity

A long-note overdriven electric-guitar role built from sparse single notes and compact dyads that ring for roughly one to several beats. Its job is to add sustained electric-guitar body, melodic weight and phrase tails without becoming a repeated per-beat rhythm pulse.

Useful tags:

```text
overdriven-guitar
sustained
long-note
melodic-support
phrase-tail
single-note
fifth-dyad
pedal-tone
```

This is deliberately different from a short muted rhythm layer. Do not use it as a quarter-note chug generator.

## Core principle

Prefer fewer attacks with longer occupancy:

```text
attack
──────── sustain ────────

        next attack
        ───── sustain ────
```

The part should feel like it stays in the room after the pick attack.

A useful default is:

```text
1-2 beat onset spacing
+
roughly 1-2 beat note lengths
+
selected longer phrase-ending holds
```

Do not cut every note to a short gate merely because the sound source is overdriven.

## Phrase behavior

Build phrases from sparse melodic attacks rather than constant chord repetition.

Useful behavior:

- many attacks begin on whole-beat positions;
- one-beat and two-beat gaps are common;
- a phrase may use several connected single notes, then finish on a much longer held tone;
- large section-level rests are allowed;
- later or stronger passages may use more dyads without turning into a dense rhythm-guitar pulse.

The important contrast is:

```text
short rhythm guitar
→ repeated attack is the identity

sustained overdrive guitar
→ held note and phrase shape are the identity
```

## Single-note mode

Use single notes for a clear melodic phrase or hook-support line.

A practical articulation family is:

```text
ordinary phrase note: about 0.9-1.2 beats
longer answer note: about 1.7-2.2 beats
phrase-ending hold: several beats when the arrangement has space
```

Do not force every note into those exact lengths. Preserve the larger behavior: ordinary notes nearly fill their rhythmic slot, and selected notes deliberately outlive the local pulse.

## Dyad mode

Later or stronger passages may thicken the gesture with compact two-note shapes.

Perfect-fifth-related dyads are a strong option, but the role is still sustained and melodic rather than a repeated power-chord rhythm pattern.

Useful transformations include:

- single note -> fifth-doubled answer;
- single note -> sustained dyad on an arrival;
- held lower note + moving upper note;
- held support tone + occasional re-articulation above it.

Do not treat every dyad as a new chord attack.

## Pedal sustain

A particularly useful gesture is to let one lower guitar tone continue ringing while the upper voice changes:

```text
lower tone:  ━━━━━━━━━━━━━━━━━
upper voice: x── x─── x─ x────
```

This creates electric-guitar mass without adding constant new attacks.

Use this selectively in climactic or extended passages. The held tone must remain harmonically compatible with the moving line.

## Gate and continuity

Most ordinary notes should occupy nearly all of the time until the next melodic event.

Prefer:

```text
note ends near next onset
```

rather than:

```text
short note + large dead gap + short note
```

Small gaps are fine when articulation needs separation. Long silence should usually be phrase-level space, not an automatic gate after every attack.

## Phrase tails without routine fader fades

For normal interior phrases and section boundaries, preserve the tail primarily through the **note itself** and the renderer's natural release.

Prefer:

```text
longer final note
+ natural release
+ intentional next-section handoff
```

Do not automatically add CC7 / expression fade-outs to sustained phrases. In energetic pop-rock arrangements this can make the next section feel as if the power suddenly disappears.

Channel-level fades are reserved for deliberate form-level effects such as an intro fade-in, an outro fade-out, or an explicitly atmospheric dissolve.

## Arrangement role

Useful roles include:

- melodic fill over a simpler rhythm section;
- sustained answer after a vocal phrase;
- long-note electric layer that fills space above muted guitar and bass;
- section ending or transition tail carried by note duration and natural release;
- later-section thickening through fifth-doubled notes or pedal sustain.

The role may be foreground or supporting depending on register and level.

## Failure modes

Revise when:

- every overdrive note is cut to a short 0.3-0.5 beat gate;
- the part becomes a mechanical one-hit-per-beat power-chord pulse;
- every beat receives a new attack even when a previous note could continue ringing;
- every note is doubled into a dyad from the beginning;
- long notes are added randomly without phrase meaning;
- a pedal tone clashes with the changing harmony;
- an interior phrase loses energy because a routine CC7 fade is used instead of note length and natural release.

## Study provenance

This material was abstracted from the long-note GM program 29 Overdriven Guitar track in a user-provided pop-rock MIDI.

Observed in the studied track:

- 157 note attacks formed 103 exact onset groups;
- 49 onset groups were single-note attacks and 54 were two-note attacks;
- 40 of the 54 dyads were separated by seven semitones, supporting frequent fifth-related thickening;
- the dominant onset gaps were 1 beat (56 occurrences) and 2 beats (30 occurrences), with much less dense activity than a subdivision-based rhythm-guitar part;
- median onset-group duration was about 1.49 beats;
- 99 of 103 onset groups lasted at least about 0.9 beat, 51 lasted at least about 1.5 beats, and 23 lasted at least about 2 beats;
- the first two recurring phrases were entirely single-note and mixed roughly one-beat notes with selected two-beat notes, ending in a very long held tail;
- later passages used many more dyads and occasionally held a lower support tone for many beats while upper notes continued to move;
- the source also contained extensive CC7 automation, but that controller behavior is not promoted as the default way to shape interior phrase tails.

These observations support a sustained overdrive gesture family centered on long occupancy, sparse melodic attacks, optional fifth doubling and pedal sustain. The source's exact melody, pitches, harmony, full phrase sequence and arrangement are intentionally omitted.