---
name: melody-structure-development
description: Compose and revise foreground melodies hierarchically from structural targets and small germs through motif recurrence, phrase development and controlled embellishment before style- or instrument-specific realization.
status: active
---

# Melody Structure and Development

## Purpose

Use this Skill when writing or revising a foreground melody for voice, lead guitar, flute, synth lead, piano melody or another melody-bearing role.

This Skill owns the **generic composition layer**:

```text
structural targets
-> germ / small idea
-> motif identity
-> recurrence and development
-> phrase relation
-> surface embellishment
```

It does **not** own instrument performance technique, renderer behavior, genre instrumentation or a fixed style vocabulary.

For example:

```text
generic melody structure
-> lead-guitar phrase / articulation logic
-> guitar Profile / renderer
```

and:

```text
generic melody structure
+ lyric prosody
-> vocal realization
```

Keep those layers separate.

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

Separate:

```text
structural tone
= important arrival, harmonic anchor, phrase target, climax tone, cadential target or otherwise weighty event

surface tone
= connector, local ornament, anticipation, delayed resolution or other motion that serves the structural line
```

Do not infer structural weight from duration alone. Duration, metrical placement, harmonic relation, phrase position and motif function all matter.

Also keep these concepts separate:

```text
chord tone
!= automatically structural tone

non-chord tone
!= automatically expendable tone
```

A fast chord tone inside a connector run may function as surface motion. A sustained color tone may be a deliberate structural target.

## Germ-first reasoning

Before filling a phrase with many notes, reduce the intended statement to a few important events.

A germ may be only:

- a short scale-line fragment;
- a chord-line fragment;
- a repeated target plus departure;
- a small rise / fall contour;
- another simple, coherent pitch-rhythm idea.

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

Stepwise motion tends to provide local continuity. Repeated pitch is valid melodic material. A larger leap should usually have a reason such as:

- register change;
- target emphasis;
- chord-line implication;
- recurring motif shape;
- sequence;
- expressive contrast;
- style- or instrument-specific gesture.

Do not enforce a universal interval quota or a universal `large leap -> reverse immediately` rule.

The important question is whether the leap has **structural support**, not whether it crosses an arbitrary semitone threshold.

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

Repetition and sequence are not signs that the generator ran out of ideas. They create unity and make variation intelligible.

A locally unusual interval or rhythm may make sense when it clearly belongs to a recurring figure.

Therefore do not judge every event independently.

Use this reasoning order:

```text
surprising event
-> does a motif / sequence / chord-line / phrase role explain it?
-> yes: preserve or soften the local penalty
-> no: inspect as possible random generation
```

A useful general principle is:

> recognizable structure can legitimize local surprise.

## Phrase relation

Do not make every phrase a reboot.

When a phrase follows another phrase, choose an explicit relationship such as:

```text
parallel
lightly varied
sequence-based
partial recurrence
opposite contour
strongly contrasting
```

Think of phrase similarity as a continuum rather than a binary `same / different` switch.

For example:

```text
A
-> A'          familiar, lightly changed
-> A''         more developed
-> B           real contrast
```

The exact phrase length is style- and project-dependent. Four-bar, eight-bar and sixteen-bar textbook forms are useful analytical examples, not universal templates.

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

Connect two different structural tones by filling part or all of the interval.

```text
target A
-> connector motion
-> target B
```

This may be diatonic or, when style and harmony support it, chromatic.

### Neighbor motion

Depart locally from one target and return to it.

```text
target
-> upper/lower neighbor
-> same target
```

### Anticipation

Preview a future structural target before its main arrival.

```text
future target appears early
-> target is re-articulated / established at its structural location
```

### Suspension / delayed arrival

Carry the previous tone into the expected target region, then resolve into the target.

```text
old tone persists
-> tension / delay
-> expected target arrives
```

### Appoggiatura-like approach

Approach an important target through a neighboring tension tone before the principal tone establishes itself.

Do not turn these labels into mandatory classical ornament rules. They are reusable **surface functions**. Their exact accent, duration, chromatic form and frequency must follow style, harmony and instrument context.

## Structural-to-surface workflow

When a melody sounds fragmented, do not immediately add more random notes.

Use this order:

```text
1. identify the intended structural targets
2. verify their contour and phrase direction
3. identify the motif relationship
4. connect selected gaps with passing / neighbor / approach motion
5. preserve real phrase boundaries
6. re-check whether the surface still reveals the underlying idea
```

This is especially useful for the failure mode where a melody sounds like isolated piano dots even though every pitch is individually legal.

## Harmony relationship

Do not generate melody independently of harmony and then merely filter out-of-scale notes.

Important structural targets should have a deliberate relationship to the active harmony.

Moving / surface notes may carry more tension.

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

## Style and tempo boundary

Generic melody grammar must not silently become a style prescription.

Do not promote historical textbook preferences such as:

```text
phrase must be 4 bars
period must be 8 bars
melody must close on tonic
specific active scale degree must always resolve one way
augmented interval is universally bad
irregular rhythm is inherently wrong
modulation should stay in related keys
```

into universal rules.

Instead treat style as a later prior learned from suitable Materials, source studies and project validation.

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

but modern vocal styles may intentionally displace stress. Treat this as a style-conditioned relationship, not a hard law.

## Instrument boundary

After the generic melody works, route it into the relevant role / instrument Skill and Profile.

For lead guitar, `lead-guitar-phrase-design` remains responsible for guitar-oriented foreground phrasing boundaries and validated downstream expression routing. Guitar bends, slides, vibrato, string choice and picking behavior are **not** invented by this Skill.

The same generic melody may therefore be realized very differently by voice, guitar, flute or synth.

## Decision procedure

1. Identify the melody-bearing role and section intent: hook, verse statement, chorus lift, answer, solo phrase, transition, climax or another explicit function.
2. Inspect the tonal / harmonic context and expected section boundaries.
3. Mark a small number of important structural targets before filling subdivisions.
4. Reduce the intended phrase to a simple germ or contour that is coherent without ornament.
5. Give the germ a rhythmic and metric identity.
6. Extend the idea primarily through recurrence and transformation rather than unrelated regeneration.
7. Choose the relationship between adjacent phrases explicitly.
8. Check phrase punctuation, rests, register trajectory and climax placement.
9. Add only enough passing / neighbor / anticipation / delaying / approach motion to make the surface natural and style-compatible.
10. Re-check the structural reduction after embellishment. The underlying idea should still be recoverable.
11. Apply genre, vocal or instrument-specific realization only after the generic phrase works.
12. Validate by listening or source comparison before promoting new style-specific rules or Materials.

## Validation

Before accepting a melody, inspect at several levels.

### Structural

- Can the phrase be reduced to a comprehensible line of important targets?
- Do those targets have a deliberate harmonic and registral relationship?
- Is the climax or principal arrival distinct enough to matter?

### Motif

- Is there recognizable material to recur?
- Do repeated or derived figures remain identifiable after variation?
- Does each new bar really need new material?

### Phrase

- Do phrase boundaries read as syntax rather than arbitrary gaps?
- Does the next phrase answer, continue, sequence, vary or contrast the previous one intentionally?
- Are rests placed for phrase reasons rather than by periodic mask?

### Surface

- Do connector notes serve structural targets?
- Is embellishment clarifying the line rather than burying it?
- Are too many notes being treated as equally important?

### Context

- Does the melody fit the backing arrangement's available foreground space?
- Is style-specific behavior coming from relevant Materials / evidence instead of this generic Skill?
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

Fix: remove the decoration and prove the structural melody first.

### Chord-tone prison

Symptom: every note is forced into the current chord and melodic tension disappears.

Fix: distinguish structural arrivals from moving / surface tones.

### Clone-loop motif

Symptom: exact repetition continues long after identity is established and no development occurs.

Fix: preserve recognizability while varying rhythm, interval, fragment, register or phrase destination.

### Fake complexity

Symptom: note density rises but the germ, phrase relation and climax remain unchanged.

Fix: develop structure before adding surface density.

### Historical-rule lock

Symptom: a modern pop, rock, modal, blues or game melody is rejected because it violates an early common-practice exercise rule.

Fix: retain the structural principle and discard the style-specific prohibition unless the active style actually needs it.

### Instrument leakage

Symptom: generic melody generation sprays bends, slides, vocal breaths or renderer controllers into the composition layer.

Fix: finish the abstract melody first, then route to the relevant instrument / role Skill and Profile.

## Study provenance

This Skill was distilled from a complete three-batch study of Percy Goetschius, *Exercises in Melody-Writing* (1903), with the main text reviewed through its conclusion.

Promoted here are the broad structural ideas that remain useful to a style-neutral Music Agent:

- coherence, unity and controlled variety;
- scale-like, repeated and chord-like motion as basic melodic resources;
- contextual support for leaps and irregularities;
- recurrence and sequence as syntax;
- modified / partial recurrence;
- phrase relationships ranging from parallel to contrasting;
- structural versus embellishing tones;
- passing, neighboring, anticipatory and delaying surface functions;
- development of larger melodic surfaces from simple germs;
- separation of technical invention from later style / expression.

Not promoted as universal rules are the book's common-practice-era restrictions on exact phrase lengths, cadence formulas, active-scale-step resolution, particular augmented intervals, related-key modulation or stylistic characterizations of modes and meters.

The detailed research note is kept outside default composition context under:

```text
source_library/studies/goetschius_exercises_in_melody_writing.md
```

The book study is theory evidence, not proof that every operator is already validated across modern genres. New style-specific Materials should still follow the repository's normal failure-driven / source-validation loop.
