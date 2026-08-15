---
name: classical-melody-practice
description: Layer common-practice and historical melody-writing conventions onto the generic melody structure workflow when the brief explicitly calls for classical tonal practice or historically grounded exercise writing.
status: active
---

# Classical Melody Practice

## Purpose

Use this Skill only when the active brief explicitly calls for a style or exercise context such as:

```text
classical melody
common-practice tonal writing
traditional tonal melody exercise
Goetschius-style melody exercise
antecedent / consequent period practice
traditional cadence-focused melody writing
```

This Skill is a **style-conditioned layer**. It does not replace `melody-structure-development`.

Use the order:

```text
generic melody structure
-> classical/common-practice constraints when requested
-> instrument realization
```

The central rule is:

> historical pedagogy belongs to historical or style-specific practice, not to the global definition of a good melody.

## Why this Skill exists

The Goetschius study contains two kinds of knowledge:

1. structural ideas that remain broadly useful across styles;
2. restrictions and preferences belonging to early-20th-century common-practice pedagogy.

The first category remains in `melody-structure-development`.
The second category is routed here instead of being discarded or treated as universal law.

## Phrase and form practice

When the task explicitly requests traditional exercise form, it is reasonable to use textbook spans such as:

```text
4-bar Phrase
8-bar Period
16-bar Double-period
```

Treat these as **practice frames and stylistic defaults**, not metaphysical laws of melody.

Useful classical-practice reasoning includes:

```text
Antecedent
-> Consequent

parallel relation
-> modified relation
-> more contrasting relation
```

Cadence placement may be used to articulate these phrase functions when the requested style depends on traditional tonal syntax.

Do not force these lengths onto modern pop, rock, game music, modal writing, jazz-derived melody or other styles merely because the generic melody has phrases.

## Cadential and tonal resolution discipline

Common-practice exercise writing may use stronger expectations for:

- clear phrase-ending tonal function;
- conventional cadence placement;
- active scale-degree resolution;
- tonal closure at structurally important endings.

These expectations should be activated only when the project asks for historically grounded tonal practice.

The current source study records the existence of source-specific active-scale-step restrictions but does not preserve the full original resolution tables. Therefore:

```text
do not invent a detailed mandatory resolution table from memory
```

If exact Goetschius exercise compliance is required, reopen the original source in `source_study` mode and verify the relevant rule.

## Leap discipline

The early Goetschius training sequence regulates skips more tightly than the generic Skill.

For a deliberately traditional exercise, a wide leap may be treated more conservatively, including a preference in early training for compensating or reversing direction after the leap.

This is a pedagogical/style tendency, not a universal melodic invariant.

Do not use it to reject a leap that is structurally justified in another style.

## Interval restrictions

The source contains historical restrictions on particular augmented intervals.

For classical exercise writing, interval vocabulary may therefore be filtered more conservatively than in the generic Skill.

The current study note does not preserve a complete interval-by-interval prohibition table, so do not fabricate one. Exact source compliance requires source verification.

## Metric regularity

The historical pedagogy begins from regular metric organization and treats irregular placement more cautiously before allowing broader freedom through recurrence and structural explanation.

In a traditional exercise context:

```text
metrical regularity
clear phrase punctuation
recurring rhythmic design
```

may be given more weight than they would receive in syncopation-heavy modern styles.

Do not convert this into:

```text
syncopation = error
irregular rhythm = bad
```

outside the historical practice context.

## Chromaticism and modulation

The source distinguishes altered scale steps from true modulation and gives priority to common-practice tonal relationships before later expanding to broader chromatic and modulatory procedures.

For traditional tonal practice, useful style-conditioned concerns include:

- clear distinction between local chromatic alteration and key change;
- related-key priority in elementary modulation work;
- common tones, pauses, sequences or cadential context as support for reinterpretation;
- stronger expectations for tonal legibility than in freely chromatic modern writing.

Do not treat `out of scale` as an automatic error even here. Chromatic tones still require functional interpretation.

The original study records source-specific altered-scale-step tables and common-practice modulation procedures, but not their complete detailed contents. Verify the original source before claiming exact rule compliance.

## Embellishing tones in classical practice

The generic Skill already defines passing, neighboring, anticipatory, delaying and appoggiatura-like functions.

In a classical/common-practice task, these functions may be realized with stricter harmonic and metric placement according to the requested historical idiom.

Relevant families include:

```text
passing motion
neighbor motion
suspension
anticipation
appoggiatura-family approach
```

Do not invent a universal accent, duration or chromatic placement rule from this Skill. The source study intentionally promoted those devices only at the functional level.

When exact historical placement matters, verify the original source or another explicit classical reference.

## Style-character claims

The source contains period-specific characterizations of major/minor, meter and tempo.

These may be useful as evidence about historical pedagogy or for recreating that pedagogical mindset, but they are not reliable universal mappings from musical parameter to emotion.

Therefore:

```text
historical characterization
-> optional style evidence
!= universal emotional truth
```

## Vocal setting

For historically oriented text setting, lexical stress and semantic importance may be aligned more strongly with musical prominence.

Possible correspondences include stronger metric placement, duration or registral emphasis, but the exact mapping remains style-conditioned.

Modern vocal writing may intentionally violate these tendencies.

## Decision procedure

1. Run `melody-structure-development` first to establish structural targets, germ, motif identity, phrase relation and surface hierarchy.
2. Confirm that the brief actually requests classical/common-practice practice before activating this Skill.
3. Decide whether the task is free classical-style composition or a stricter pedagogical exercise.
4. For an exercise, choose an explicit phrase frame such as Phrase, Period or Double-period when appropriate.
5. Plan antecedent/consequent relation and cadential function before surface decoration.
6. Apply more conservative leap, interval, metric and tonal-resolution discipline only to the extent supported by the requested historical style.
7. Distinguish chromatic color from modulation and keep tonal reinterpretation legible.
8. Apply embellishing tones with awareness of their harmonic and metric role.
9. Do not invent exact historical tables or prohibitions that are absent from the active evidence.
10. If exact source compliance matters, switch to `source_study`, verify the original rule, then return to the composition task.

## Failure modes

### Historical rules leaking into modern composition

Symptom: a pop, rock, game, jazz-derived or modal melody is rejected for violating a traditional exercise convention.

Fix: remove this Skill from the active style stack and keep only the generic structural layer.

### Fake historical precision

Symptom: the Agent claims an exact scale-degree, interval or ornament rule that is not recorded in the active source evidence.

Fix: verify the original source instead of reconstructing a table from memory.

### Classical as fixed bar counts

Symptom: every classical-style melody is forced into 4+4 bars regardless of musical intent.

Fix: treat Phrase/Period/Double-period lengths as practice frames and common examples, not the complete space of classical form.

### Rule compliance without musical syntax

Symptom: every local interval is legal but the melody lacks motif identity, phrase direction or structural hierarchy.

Fix: return to `melody-structure-development`; this Skill is a style layer, not a substitute for composition.

## Provenance

This Skill reorganizes the common-practice-era material explicitly marked as historical or not universal in the repository study of Percy Goetschius, *Exercises in Melody-Writing* (1903).

The source study supports the presence of historical constraints or preferences involving:

- early leap regulation;
- regular versus irregular metric hierarchy;
- four-bar Phrase, eight-bar Period and sixteen-bar Double-period practice frames;
- traditional cadence placement and tonal closure;
- active-scale-degree resolution rules;
- restrictions on particular augmented intervals;
- related-key priority and common-practice modulation procedures;
- stricter historical realization of embellishing tones;
- period-specific characterizations of mode, meter and tempo;
- stronger lexical-stress-to-musical-prominence tendencies in vocal setting.

Where the study note does not preserve the source's detailed tables or exact formulations, this Skill deliberately records the boundary instead of inventing specifics.
