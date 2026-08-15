---
name: melody-structure-development
description: Compose and revise foreground melodies hierarchically from structural targets and small germs through motif recurrence, phrase development and controlled embellishment before style- or instrument-specific realization.
status: active
---

# Melody Structure and Development

## Purpose

Use this Skill when writing or revising a foreground melody for voice, lead guitar, flute, synth lead, piano melody or another melody-bearing role.

This Skill owns the **style-neutral structural layer**:

```text
structural targets
-> germ / small idea
-> motif identity
-> recurrence and development
-> phrase relation
-> surface embellishment
```

It does not own:

```text
historical style rules
instrument performance technique
renderer behavior
genre instrumentation
fixed phrase lengths
fixed cadence formulas
```

Those belong to later style, instrument or implementation layers.

## Core principle

Do not compose a melody as a flat stream of equally important MIDI notes.

Prefer a hierarchy:

```text
harmonic / tonal context
        ↓
important structural targets
        ↓
small germ or motif seed
        ↓
recognizable motif
        ↓
repeat / vary / answer / contrast
        ↓
phrase and section shape
        ↓
passing / neighboring / anticipatory / delaying surface motion
        ↓
style and instrument realization
```

The finished surface may contain many notes while the underlying structural line remains simple.

## Structural tones versus surface tones

Not every note has equal structural weight.

```text
structural tone
= important arrival, harmonic anchor, phrase target, climax tone,
  cadential target or otherwise weighty event

surface tone
= connector, local ornament, anticipation, delayed resolution
  or other motion serving the structural line
```

Do not infer structural weight from duration alone. Duration, metrical placement, harmonic relation, phrase position and motif function all matter.

Keep these separate:

```text
chord tone != automatically structural tone
non-chord tone != automatically expendable tone
```

A fast chord tone inside a connector run may be surface motion. A sustained color tone may be a deliberate structural target.

## Germ-first reasoning

Before filling a phrase with many notes, reduce the intended statement to a few important events.

A germ may be only:

- a short scale-line fragment;
- a chord-line fragment;
- a repeated target plus departure;
- a small rise / fall contour;
- another simple coherent pitch-rhythm idea.

The germ does not need to be spectacular. Its job is to provide a stable identity that can survive development.

Prefer:

```text
simple germ
+ strong manipulation
```

rather than:

```text
new unrelated pitch idea on every beat
```

## Basic motion vocabulary

Useful abstract motion types include:

```text
STEP
REPEAT
LEAP
TURN
ARRIVE
RESOLVE
```

Stepwise motion often provides local continuity. Repeated pitch is valid melodic material.

A larger leap should have a structural reason such as:

- register change;
- target emphasis;
- chord-line implication;
- recurring motif shape;
- sequence;
- expressive contrast;
- style- or instrument-specific gesture.

Do not enforce a universal interval quota. The important question is whether the leap has structural support.

## Motif identity

A motif is useful only if later material can still be heard as related to it.

Track identity through some combination of:

- contour;
- interval pattern;
- rhythm;
- metrical footprint;
- repeated target;
- characteristic fragment.

Do not require every dimension to remain unchanged.

A useful development principle is:

> change enough to create motion, but preserve enough for recognition.

## Development operators

When extending a successful germ or motif, prefer transformations over full regeneration.

Useful operations include:

```text
repeat(unit)
sequence(unit)
partial_recurrence(unit)
fragment(unit)
modify_intervals(unit)
expand_or_contract_contour(unit)
rhythm_variation(unit)
augment_or_diminish_rhythm(unit)
invert_contour(unit)
add_connector_notes(unit)
omit_surface_notes(unit)
```

These names describe musical operations, not mandatory implementation APIs.

Apply transformations at more than one scale when useful:

```text
motif
subphrase
phrase region
whole phrase
```

## Recurrence before randomness

Repetition and sequence create unity and make variation intelligible.

Do not judge every event independently.

Use this reasoning order:

```text
surprising event
-> does motif / sequence / chord-line / phrase role explain it?
-> yes: preserve or soften local penalty
-> no: inspect as possible random generation
```

A useful general principle is:

> recognizable structure can legitimize local surprise.

## Phrase relation

Do not make every phrase a reboot.

Choose an explicit relationship between adjacent phrases, for example:

```text
parallel
lightly varied
sequence-based
partial recurrence
opposite contour
strongly contrasting
```

Think of phrase similarity as a continuum:

```text
A
-> A'          familiar, lightly changed
-> A''         more developed
-> B           real contrast
```

Phrase length is style- and project-dependent.

## Phrase punctuation and rests

Rests are structural events.

Use silence to:

- reveal motif boundaries;
- separate statement and answer;
- emphasize an arrival;
- create breath;
- expose arrangement handoff;
- prepare a new phrase.

Do not insert a fixed rest mask every bar.

A rest is good when it clarifies syntax without destroying continuity.

## Embellishment layer

Only embellish after the structural line and phrase relationship work.

Useful generic surface functions include:

### Passing motion

```text
target A
-> connector motion
-> target B
```

### Neighbor motion

```text
target
-> upper/lower neighbor
-> same target
```

### Anticipation

```text
future target appears early
-> target is established at its structural location
```

### Suspension / delayed arrival

```text
old tone persists
-> tension / delay
-> expected target arrives
```

### Appoggiatura-like approach

```text
local tension near target
-> important target establishes itself
```

These are reusable **surface functions**. Their exact accent, duration, chromatic form and frequency belong to style and harmony.

## Structural-to-surface workflow

When a melody sounds fragmented, do not immediately add random notes.

Use this order:

```text
1. identify intended structural targets
2. verify contour and phrase direction
3. identify motif relationship
4. connect selected gaps with passing / neighbor / approach motion
5. preserve real phrase boundaries
6. re-check whether the surface still reveals the underlying idea
```

This directly addresses the failure mode where a melody sounds like isolated note dots even though every pitch is individually legal.

## Harmony relationship

Do not generate melody independently of harmony and then merely filter out-of-scale notes.

Important structural targets should have a deliberate relationship to the active harmony.
Moving and surface notes may carry more tension.

Prefer:

```text
freer motion
+
deliberate arrivals
```

rather than:

```text
every note forced into the current chord
```

Chromatic tones may serve local color, connection, tension, tonicization or modulation. Do not classify every out-of-scale pitch as an error.

## Style handoff

Generic melody grammar must not silently become a style prescription.

After the structural melody works, layer style-specific knowledge only when the active brief calls for it.

For explicitly classical/common-practice work, load:

```text
skills_v2/classical_melody_practice/SKILL.md
```

That Skill owns historical practice frames and common-practice constraints that should not leak into modern pop, rock, game, modal, jazz-derived or other melody writing.

Other styles should gain their own validated Materials or Skills rather than modifying this generic layer.

Tempo may also change viable note density, ornament density, sustain and gesture length. Do not merely time-stretch one melody recipe across all BPM values.

## Vocal boundary

For vocal melody, add a prosody layer after or alongside structural planning.

Consider:

- syllable count;
- lexical / syllabic stress;
- important words;
- punctuation and phrase boundaries;
- breath;
- melisma versus syllabic delivery;
- emotional emphasis.

A useful default relationship is:

```text
linguistic prominence
<->
musical prominence
```

The exact mapping is style-conditioned.

## Instrument boundary

After the generic melody works, route it into the relevant role / instrument Skill and Profile.

For lead guitar, `lead-guitar-phrase-design` owns guitar-oriented foreground phrasing and validated downstream expression routing.

Guitar bends, slides, vibrato, string choice and picking behavior are not invented by this Skill.

The same generic melody may therefore be realized very differently by voice, guitar, flute or synth.

## Decision procedure

1. Identify the melody-bearing role and section intent.
2. Inspect tonal / harmonic context and section boundaries.
3. Mark a small number of important structural targets before filling subdivisions.
4. Reduce the intended phrase to a coherent simple germ or contour.
5. Give the germ rhythmic and metric identity.
6. Extend primarily through recurrence and transformation rather than unrelated regeneration.
7. Choose the relationship between adjacent phrases explicitly.
8. Check phrase punctuation, rests, register trajectory and climax placement.
9. Add only enough passing / neighbor / anticipation / delaying / approach motion to make the surface natural.
10. Re-check the structural reduction after embellishment.
11. Apply style-specific and instrument-specific realization only after the generic phrase works.
12. Validate by listening or source comparison before promoting new reusable style knowledge.

## Validation

### Structural

- Can the phrase be reduced to a comprehensible line of important targets?
- Do those targets have a deliberate harmonic and registral relationship?
- Is the principal arrival distinct enough to matter?

### Motif

- Is there recognizable material to recur?
- Do derived figures remain identifiable after variation?
- Does each new bar really need new material?

### Phrase

- Do phrase boundaries read as syntax rather than arbitrary gaps?
- Does the next phrase answer, continue, vary or contrast intentionally?
- Are rests placed for phrase reasons rather than by periodic mask?

### Surface

- Do connector notes serve structural targets?
- Is embellishment clarifying the line rather than burying it?
- Are too many notes being treated as equally important?

### Context

- Does the melody fit the arrangement's available foreground space?
- Is style-specific behavior coming from the proper style layer?
- Is instrument-specific behavior routed to the correct downstream Skill / Profile?

## Failure modes

### Note soup

Symptom: many legal notes but no recoverable structural line.

Fix: strip the phrase to a few targets, repair the contour, then rebuild the surface.

### Bar-by-bar amnesia

Symptom: each bar introduces unrelated pitch and rhythm material.

Fix: assign motif identity and derive later material through repetition, sequence, fragmentation or controlled variation.

### Ornament-first composition

Symptom: runs, chromatic notes and decorative turns exist before there is a convincing phrase.

Fix: remove decoration and prove the structural melody first.

### Chord-tone prison

Symptom: every note is forced into the current chord and melodic tension disappears.

Fix: distinguish structural arrivals from moving and surface tones.

### Clone-loop motif

Symptom: exact repetition continues long after identity is established and no development occurs.

Fix: preserve recognizability while varying rhythm, interval, fragment, register or phrase destination.

### Fake complexity

Symptom: note density rises but germ, phrase relation and climax remain unchanged.

Fix: develop structure before adding surface density.

### Style leakage

Symptom: a style-specific convention is treated as a universal melody law.

Fix: return this Skill to structural invariants and route the convention into the appropriate style Skill or Material.

### Instrument leakage

Symptom: generic melody generation sprays bends, slides, vocal breaths or renderer controllers into the composition layer.

Fix: finish the abstract melody first, then route to the relevant instrument / role Skill and Profile.

## Study provenance

This Skill was initially distilled from a complete three-batch study of Percy Goetschius, *Exercises in Melody-Writing* (1903), with the main text reviewed through its conclusion.

Promoted here are the broad structural ideas that remain useful to a style-neutral Music Agent:

- coherence, unity and controlled variety;
- scale-like, repeated and chord-like motion as melodic resources;
- contextual support for leaps and irregularities;
- recurrence and sequence as syntax;
- modified and partial recurrence;
- phrase relationships ranging from parallel to contrasting;
- structural versus embellishing tones;
- passing, neighboring, anticipatory and delaying surface functions;
- development of larger melodic surfaces from simple germs;
- separation of technical invention from later style and expression.

Historical common-practice restrictions from that source are no longer duplicated here. They are routed to:

```text
skills_v2/classical_melody_practice/SKILL.md
```

The detailed research note remains outside default composition context under:

```text
source_library/studies/goetschius_exercises_in_melody_writing.md
```

The book study is theory evidence, not proof that every operator is already validated across modern genres. New style-specific Materials should still follow the repository's failure-driven and source-validation loop.
