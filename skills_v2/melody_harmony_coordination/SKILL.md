---
name: melody-harmony-coordination
description: Coordinate melody structure with harmonic rhythm, relative closure, chord candidates and bass trajectory without forcing every melody note into a chord or importing common-practice harmony rules into every style.
status: active
---

# Melody-Harmony Coordination

## Purpose

Use this Skill when a task requires melody and harmony to be designed, revised or evaluated together.

Typical triggers include:

```text
harmonize a melody
reharmonize melody
choose chords under melody
harmonic rhythm
melody feels disconnected from chords
cadence / closure support
melody target vs chord
bass trajectory after harmony choice
```

This Skill is a **coordination layer**.

It does not replace:

```text
melody-structure-development
style-specific harmony knowledge
classical-melody-practice
bass-line-continuity
instrument realization
```

Use the order:

```text
melody structure
-> melody-harmony coordination
-> style-specific harmony decisions when needed
-> bass-line continuity / arrangement
```

---

## Core principle

Do not harmonize a melody as:

```text
for every melody note:
    choose a chord containing that pitch
```

Prefer:

```text
phrase structure
-> closure plan
-> harmonic rhythm
-> structural melody targets
-> harmony candidates
-> contextual evaluation
-> bass / inversion intent
```

Moving and ornamental melody notes do not require independent chord changes.

---

## Phrase first

Before choosing chords, identify:

```text
phrase boundaries
phrase relationships
important arrivals
open vs closed regions
section-level destination
```

Harmony should support the phrase's direction rather than merely legalize local pitches.

Useful phrase cues include:

```text
melodic punctuation
rests / holds
motif completion
register arrival
rhythmic closure
existing harmonic implications
```

---

## Relative closure strength

Treat closure as a graded structural function.

Useful roles:

```text
continuation
pause
local close
section close
final close
```

Useful reasoning:

```text
weaker closure
-> preserves forward need

stronger closure
-> confirms arrival / section completion
```

In style-neutral work, do not require classical cadence labels.

For explicitly common-practice work, `classical-melody-practice` may add PAC / IAC / HC / other cadence conventions.

---

## Harmonic rhythm

Harmonic rhythm is the rate and placement of chord change.

Plan it independently from melodic note density.

Consider:

```text
chord-change rate
metric placement of changes
section-to-section change in harmonic rhythm
cadence / closure approach
relationship to melodic density
```

Useful tendencies:

```text
slower harmonic rhythm
-> can leave more room for ornate surface melody

faster harmonic rhythm
-> requires clearer coordination of important melodic arrivals
```

These are tendencies, not formulas.

Do not automatically assign one chord per note or one chord per bar.

---

## Structural targets versus surface motion

Coordinate harmony primarily with important melodic events.

A useful order is:

```text
1. identify structural targets
2. identify surface / connector notes
3. plan harmony around structural regions
4. verify that surface notes have plausible melodic functions
```

A note may be:

```text
chord tone but structurally weak
non-chord tone but structurally expressive
```

Chord membership alone does not define melodic importance.

---

## Contextual chord-tone / NCT interpretation

When deciding whether a melody note belongs to the active harmony, inspect context:

```text
harmonic rhythm
metrical position
duration
approach motion
departure motion
phrase role
motif recurrence
```

Example reasoning:

```text
fast connector between two structural targets
-> may remain a non-chord tone
-> no new chord needed
```

versus:

```text
long metrically strong arrival
-> may justify a harmonic reinterpretation or new chord
```

Do not use a simple `pitch in chord` test as the complete decision procedure.

---

## Harmony candidate search

Harmonization usually has multiple plausible answers.

Use candidate generation and comparison:

```text
structural region
-> candidate A
-> candidate B
-> candidate C
-> compare
-> choose
```

Evaluate candidates using relevant dimensions such as:

```text
support for melodic targets
phrase direction
relative closure strength
harmonic-rhythm consistency
bass continuity
style compatibility
voice-leading / instrument feasibility
foreground space
color / tension
```

Do not pretend there is a single mathematically correct chord when the musical context allows alternatives.

---

## Candidate elimination

Eliminate a candidate when it conflicts with the active task, for example:

- it weakens an intended arrival;
- it creates unwanted harmonic churn under surface notes;
- it contradicts the style's harmonic vocabulary;
- it produces a poor bass trajectory;
- it removes needed tension too early;
- it obscures phrase hierarchy;
- it creates instrument-realization problems.

Explain the tradeoff rather than applying hidden textbook rules.

---

## Bass and inversion handoff

After choosing a harmonic path, do not assume the bass must play every chord root.

Pass the harmonic intention to:

```text
bass-line-continuity
```

with enough information to choose or realize:

```text
root / inversion intent
bass contour
approach notes
register
section energy
```

A smoother or more melodic bass trajectory may justify inversion or alternate voicing when the active style allows it.

---

## Interaction with generic melody revision

If harmony exposes a melodic problem, repair the smallest responsible layer.

Examples:

```text
structural target fights intended harmony
-> reconsider target or harmony candidate

surface note sounds wrong
-> inspect its passing / neighbor / anticipation role

phrase ending feels weak
-> inspect closure plan before adding more notes
```

Do not regenerate the entire melody when a local coordination issue is enough to explain the failure.

---

## Interaction with classical practice

When the active brief explicitly requests classical/common-practice writing, layer:

```text
skills_v2/classical_melody_practice/SKILL.md
```

That layer may add:

```text
traditional cadence families
antecedent / consequent closure dependency
traditional NCT classifications
stricter tonal-resolution expectations
```

Detailed four-part voice-leading, doubling, seventh-chord resolution and inversion rules should remain a separate classical-harmony concern rather than becoming universal coordination rules here.

---

## Interaction with modern styles

For pop, rock, game music, modal writing, jazz-derived harmony or other modern styles:

```text
coordination logic
+
validated style-specific harmony knowledge
```

should determine the result.

This Skill must not silently impose:

```text
begin/end on tonic
fixed dominant-tonic cadence
one chord per melody note
related-key-only movement
traditional seventh-resolution rules
```

unless the active style layer requires them.

---

## Decision procedure

1. Load or establish the melody's structural reduction.
2. Identify phrase boundaries and section destination.
3. Mark important melodic arrivals and distinguish surface motion.
4. Assign relative closure roles to phrase and section endings.
5. Plan harmonic rhythm before selecting detailed chords.
6. Generate several plausible harmonic paths where ambiguity exists.
7. Evaluate candidates by melodic support, closure, harmonic rhythm, style and bass trajectory.
8. Preserve surface notes as non-chord tones when their motion makes sense; do not create unnecessary chord changes.
9. Choose or suggest inversion / bass intent and hand it to `bass-line-continuity` when needed.
10. Re-check the melody after harmony selection.
11. If a local conflict remains, revise the smallest responsible melody or harmony region.
12. Apply classical or other style-specific harmony constraints only from the appropriate style layer.

---

## Validation

### Phrase

- Does harmony support the intended phrase direction?
- Are weaker and stronger closures differentiated where needed?
- Does the harmonic path clarify rather than flatten section structure?

### Harmonic rhythm

- Are chord changes intentional rather than mechanically attached to notes?
- Does the rate of harmonic change fit the melodic density and tempo?
- Does harmonic rhythm vary when the section needs contrast?

### Melody relation

- Do important targets have deliberate harmonic relationships?
- Are surface notes allowed to move freely where their function is clear?
- Are too many melody notes forcing unnecessary re-harmonization?

### Bass

- Does the chosen harmony permit a coherent bass trajectory?
- Should inversion or alternate voicing be considered before accepting a poor root-jumping bass line?

### Style

- Are style-specific harmonic rules coming from evidence relevant to the requested style?
- Has common-practice pedagogy leaked into unrelated music?

---

## Failure modes

### One-note-one-chord harmonization

Symptom: every melody note triggers a chord change.

Fix: identify structural targets and plan harmonic rhythm first.

### Chord-tone prison

Symptom: melody is rewritten so every note belongs to the active chord.

Fix: allow functional surface notes and coordinate deliberate arrivals instead.

### Flat closure hierarchy

Symptom: every phrase ending feels equally final.

Fix: plan relative closure strength across the section.

### Harmonic churn

Symptom: accompaniment changes so rapidly that the foreground melody loses continuity.

Fix: simplify harmonic rhythm and let surface motion live above a more stable harmonic region.

### Root-bass lock

Symptom: chosen chords are acceptable but bass leaps mechanically between roots.

Fix: hand inversion and contour options to `bass-line-continuity`.

### Style leakage

Symptom: a modern melody is rejected for violating a classical harmonization rule.

Fix: remove the unrelated style constraint and keep only coordination logic.

---

## Provenance

This Skill was created from the repository study of:

```text
source_library/studies/comprehensive_musicianship_practical_resource.md
```

The source supports the importance of phrase structure, cadence / closure, harmonic rhythm, multiple harmonization possibilities, contextual NCT interpretation and bass-aware harmonization.

The generic abstractions here intentionally exclude classroom-specific common-practice chord restrictions unless a classical style layer is active.
