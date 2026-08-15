---
name: lead-guitar-phrase-design
description: Write lead-guitar melodies as connected phrases with target-note arrivals, local motion, purposeful repetition and phrase-level space before adding renderer-specific articulation.
status: active
---

# Lead Guitar Phrase Design

## Purpose

Use this Skill when writing or revising a lead-guitar melody, solo, melodic fill, answering phrase or other foreground single-note guitar part.

Its first job is **phrase design**, not effects or guitar-sampler decoration.

Keep these layers separate:

```text
phrase design
= rhythm + contour + target-note logic + repetition + phrase boundaries

articulation
= picked attack + legato + bend + slide + vibrato + release behavior

timbre / realization
= clean / crunch / overdrive source + amp / renderer / keyswitch capability
```

A convincing lead part should already read as a musical sentence before bend, slide or vibrato is added.

## Core principle

Do not treat lead guitar as a continuous stream of unrelated melody notes.

Prefer phrase shapes such as:

```text
short pickup / burst
-> held target
-> repeated target or small local answer
-> connective motion
-> cadence / phrase rest
```

This is a grammar, not a fixed rhythm template. A phrase may omit, reorder or stretch these functions.

The reusable invariant is:

> create direction toward important arrivals, then let the arrival and phrase boundary have enough time to matter.

## Two kinds of continuity

Lead-guitar continuity has two different scales.

### Micro continuity

Inside an active phrase, adjacent notes may connect closely in time. Short notes can feed directly into the next note instead of becoming detached dots.

Useful behavior:

```text
active phrase
████████████████
```

This does **not** mean every note must overlap or use legato articulation.

### Phrase-level space

Between phrases, real rests are useful punctuation.

```text
phrase A        phrase B
████████        ██████████
```

Do not convert this into a mechanical `play-play-rest` pattern repeated every bar. Phrase space should follow musical syntax and arrangement support.

## Target-note logic

Separate moving notes from arrival notes.

Moving notes may include:

- scale motion;
- neighbor tones;
- approach tones;
- passing tones;
- repeated pickups;
- short register transitions.

Arrival notes may be held longer, re-articulated, emphasized by rhythm, or given more registral weight.

Do not enforce `every note must be a chord tone`.

A better rule is:

```text
movement may carry tension
+
important arrivals should have a deliberate harmonic relationship
```

Stable chord tones are one strong arrival option, but a sustained color tone or tension may also be intentional. Judge the target by phrase function and harmony, not by a binary chord-tone checker.

## Repeated-pitch permission

Repeated pitch is valid melodic development.

Do not assume:

```text
melody development = constant pitch change
```

A repeated target can develop through:

- different duration;
- different onset placement;
- re-articulation;
- accent change;
- later articulation such as vibrato or bend when supported;
- a changed answer after the repetition.

Repeated notes can make a guitar line feel anchored and vocal rather than algorithmically restless.

## Interval behavior

For a lyrical or singing lead-guitar line, local motion should usually dominate over constant large jumps.

Useful default reasoning:

```text
nearby motion = sentence continuity
larger jump = register change / new gesture / emphasis
```

Do not turn this into a universal interval quota. Fast rock, fusion, metal, country, tapping or sequence-based phrases may use different interval vocabularies.

The important distinction is **purposeful register motion versus random MIDI jumping**.

## Duration contrast

Lead guitar benefits from strong contrast between short connective activity and notes that are allowed to arrive and stay.

A useful phrase may contain both:

```text
very short pickup notes
+
medium connective notes
+
one or more held arrivals
```

Do not fill every available beat just because the lead track is foreground.

A held note is musical content. It is not an empty placeholder waiting for more pitches.

## Arrangement dependency

Phrase density depends on what the backing arrangement is doing.

If the rhythm section or accompaniment bed is stable and active, the lead can leave larger phrase-level gaps without making the whole arrangement collapse.

If the backing is sparse, the lead may need more continuity, longer sustain or different handoff behavior.

Therefore do not define lead density from the lead track alone.

## Decision procedure

1. Identify the lead role for the current section: hook, lyrical solo, answer phrase, fill, transition, climax, or other explicit function.
2. Mark one or more important arrival zones before filling every subdivision.
3. Write a short contour or pickup that has direction toward an arrival.
4. Let important target notes last long enough to be perceived as arrivals when the phrase needs that effect.
5. Permit repeated-pitch re-articulation when it reinforces the target or motif.
6. Use nearby connective motion by default in lyrical phrases; reserve larger jumps for a clear registral or structural reason.
7. End the phrase deliberately. Decide whether it resolves, hangs, repeats, descends, lifts register or leaves a rest.
8. Check the backing arrangement before deciding how much phrase-level space is safe.
9. Only after the phrase works as notes and rhythm, add articulation supported by the chosen Profile, active Material or source evidence.
10. For an expressive held target, `expressive-target-note` is the current validated Material for conservative bend-arrival behavior.
11. Do not invent slide, vibrato, hammer-on or pull-off merely to make the MIDI look more guitar-like. Do not assume CC1 is a safe guitar-vibrato fallback without renderer-specific listening validation.

## Failure modes

### Distorted piano

Symptom: the line is a sequence of equally weighted MIDI notes with no clear arrivals, phrase boundaries or duration contrast.

Fix: design sentences first; use short motion to approach held or emphasized targets.

### Pitch-change compulsion

Symptom: nearly every note changes pitch because repetition is treated as a defect.

Fix: allow repeated target notes and develop rhythm, duration or articulation instead.

### Random register hopping

Symptom: large jumps occur frequently without a phrase or register reason.

Fix: restore local contour; use big moves as structural events.

### Chord-tone prison

Symptom: every lead note is forced into the current chord, flattening melodic tension.

Fix: distinguish moving tones from arrival tones and judge harmonic intent at important targets.

### Endless noodle

Symptom: the lead plays continuously because silence is treated as missing content.

Fix: add phrase punctuation where the backing can carry the motion.

### Mechanical breathing

Symptom: the same fixed rest pattern appears every bar.

Fix: place rests according to phrase endings, motif syntax and arrangement handoff rather than a periodic gap mask.

### Articulation cosplay

Symptom: bends, slides and vibrato are sprayed onto notes without source evidence, instrument capability or phrase reason.

Fix: keep phrase design and articulation separate; only realize gestures that the Profile can support and the musical context motivates.

### Target overshoot masquerading as bend

Symptom: the written note is already the intended target, then pitch bend pushes it above the destination and the lead sounds sharp or alarm-like.

Fix: route the chosen held target through `expressive-target-note`; a bend-in gesture must distinguish the lower base pitch from the intended target pitch.

## Validation

Before accepting a lead-guitar part, inspect:

- phrase boundaries and phrase lengths;
- note-on / previous-note-off gaps inside phrases versus between phrases;
- duration distribution, especially whether any important targets are allowed to hold;
- repeated-pitch usage and whether repetition has a musical function;
- interval distribution and the placement of larger register jumps;
- contour over multi-note phrases rather than note-by-note randomness;
- relationship of longer or emphasized targets to the active harmony;
- whether rests line up with phrase syntax rather than a mechanical periodic mask;
- whether lead density makes sense against the backing arrangement;
- whether articulation claims are actually present in the source or supported by the target Profile / active Material;
- for bend-in targets, whether the realized destination equals the intended musical target instead of overshooting it;
- whether pitch-wheel reset changes the audible note tail before note-off;
- whether any CC-based modulation has been validated for the actual renderer.

Do not convert one source's percentages into universal quality targets.

## Study provenance: user-provided Comfortably Numb solo MIDI

A user-provided MIDI study supplied the first direct evidence for this Skill's phrase layer.

Observed in the dedicated lead track:

- 82 completed notes were present over MIDI pitch range 50-79;
- 24 notes were very short at `<= 0.125` quarter-note beats;
- 11 notes lasted `>= 1.0` quarter-note beat;
- the median note duration was about `0.333` beat;
- 65 of 81 adjacent note transitions, about 80.2%, had the previous note-off exactly at the next note-on, supporting strong within-phrase temporal connection without requiring note overlap;
- 22 of 81 adjacent transitions, about 27.2%, repeated the same pitch;
- 74 of 81 adjacent pitch transitions, about 91.4%, stayed within five semitones, supporting predominantly local motion with occasional larger register moves;
- against the simultaneously active pitch classes in the backing-guitar track, 45 of 82 lead onsets, about 54.9%, were chord-member matches;
- among the 11 lead notes lasting at least one beat, 8, about 72.7%, matched the active backing pitch classes at onset, supporting the distinction between freer moving tones and more deliberately related long arrivals;
- velocity carried little expressive information: 78 notes used velocity 80 and four used velocity 72;
- the lead track contained no pitch-wheel events and no control-change events, so this source does **not** establish reusable bend, vibrato, slide, sustain-pedal or modulation rules.

These measurements are evidence about this source, not style-wide targets.

The source's exact melody, note sequence, harmony, phrase transcription and song form are intentionally omitted from reusable knowledge.

## Current boundary

This Skill still teaches the **phrase layer only**. It now routes expressive held targets to the separate active Material `expressive-target-note` after the phrase itself works.

Current validated downstream knowledge includes a conservative bend-arrival semantic pattern:

```text
lower base pitch
-> bend reaches intended target
-> hold target through note-off
-> reset pitch wheel after note-off
```

That downstream Material also records a listening-validated bend-only baseline for the current generic GM workflow.

This Skill does not itself claim a general validated grammar for:

- physical slide technique;
- vibrato rate or depth;
- CC1 as a universal vibrato implementation;
- hammer-ons / pull-offs;
- pick-direction logic;
- string / fret choice;
- feedback or amp interaction.

Those should be promoted only after separate inspectable evidence and, where realization is renderer-dependent, listening validation on the target Profile.
