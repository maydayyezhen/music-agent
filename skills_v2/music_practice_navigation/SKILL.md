---
name: music-practice-navigation
description: Interpret broad music style, genre and functional briefs by separating purpose, style, instrumentation, texture, creation mode and performance context before routing to specialized Skills and Materials.
status: active
---

# Music Practice Navigation

## Purpose

Use this Skill when a brief names or implies a broad musical domain, genre, style, cultural practice or functional use and the Agent needs to decide **what kind of musical knowledge should be active next**.

Examples:

```text
rock
pop
jazz
folk
classical
film music
game music
BGM
dance music
spiritual music
storytelling music
soundtrack
background music
studio-produced song
```

This Skill is a **thin navigation layer**.

It does not contain full genre recipes.
It does not replace style-specific Materials.
It does not select instruments by stereotype.

Use it to avoid collapsing a broad label into an automatic arrangement.

---

## Core rule

Do not reason as:

```text
genre
-> automatic instrument preset
-> automatic energy
-> automatic texture
-> automatic harmony
```

Prefer:

```text
brief
-> purpose / function
-> style / genre context
-> musical dimensions that matter
-> creation / performance mode
-> instrumentation + roles
-> relevant specialized Skill / Material
-> realization
```

A genre label is useful evidence, but it is not a complete specification.

---

## Keep the axes separate

Before making detailed musical choices, distinguish the dimensions that are actually present in the brief.

```text
purpose
  what the music is for

genre / style
  stylistic family or compatibility

instrumentation
  chosen sound sources

role
  musical function of each part

energy
  density / motion / register / weight / foreground pressure

texture
  layer interaction / sustain / rhythmic surface / articulation

timbre
  sound quality / technique / processing

creation mode
  fixed / arranged / improvisatory / studio-constructed

performance context
  live / recorded / dance / dramatic / intimate / interactive
```

Never silently derive all later fields from the genre field.

---

## Purpose first when purpose is explicit

If the user tells you what the music is **for**, treat that as first-class compositional context.

Useful broad categories include:

```text
storytelling / characterization
foreground song
background / underscore
dance / movement
ritual / spiritual
political / communal identity
concert / attentive listening
domestic / intimate listening
recorded / studio work
interactive / game context
mixed purpose
```

These categories are navigation aids, not an exhaustive ontology.

### Purpose-conditioned tendencies

Purpose may influence the balance of repetition, variation, contrast, density and clarity.

For example:

```text
dance-oriented task
-> stable pulse / groove and sustained motion may matter more

storytelling task
-> larger changes in texture, register, timbre or thematic material may be useful

background / underscore task
-> foreground pressure and narrative interference may need restraint

studio-constructed task
-> production layers may be part of the intended composition
```

Treat these as questions and tendencies, not hidden validators.

---

## Cross-style musical dimensions

When comparing or planning unfamiliar styles, inspect relevant dimensions instead of guessing from a label.

```text
rhythm
  pulse
  meter / cycle
  subdivision
  syncopation
  rhythmic density
  tempo behavior

pitch / melody
  pitch organization
  range / register
  motif behavior
  phrase behavior

harmony
  only where the tradition or task makes harmony a useful organizing concept

dynamics
  level / contour / contrast

articulation
  attack / sustain / release

timbre
  sound source / technique / processing

texture
  foreground-background relation
  monophonic / homophonic / polyphonic / heterophonic when useful
  sparse / dense

form
  repetition / variation / contrast
  section ordering
  large-scale timing
```

Do not assume every musical tradition is best described by Western harmony terminology.

---

## Repetition, variation and contrast

At arrangement and form scale, ask:

```text
what should remain recognizable?
what should vary?
what should provide contrast?
which musical dimension carries that contrast?
```

Repetition, variation and contrast may operate independently in:

```text
melody
rhythm
harmony
bass
texture
instrumentation
timbre
register
form
```

Do not make every new section new in every dimension.

For melody-specific `CREATE / VARY / REPEAT` reasoning, use `melody-structure-development`.

---

## Creation mode

Identify how fixed the intended musical object is.

Useful descriptions include:

```text
fixed_composition
arranged
semi_fixed
improvisatory
studio_constructed
```

When improvisation is relevant, also ask what is actually free:

```text
pitch
rhythm
ornament
phrase
texture
instrumentation
form
```

Improvisation means constrained creation inside a style or performance framework, not arbitrary note generation.

Do not simulate an improvisatory tradition by simply increasing randomness.

---

## Performance and transmission

When relevant, distinguish:

```text
notation-centered
aural / oral
lead-sheet / chart
live ensemble interaction
community participation
studio layering
performer-led realization
producer-led realization
```

A structured MIDI output may represent different things in different tasks:

```text
finished fixed performance
arrangement framework
repeatable pattern with variation slots
improvisation scaffold
```

Choose the representation that best matches the requested practice while preserving project editability.

---

## Timbre can carry style identity

Do not treat timbre as a cosmetic final step.

Depending on the style, identity may depend strongly on:

```text
instrument choice
playing technique
articulation
register
amplification
processing
noise component
envelope / sustain behavior
```

Route detailed behavior to the relevant instrument Skill, Material and Profile.

Do not claim a style has been reproduced merely because the pitch/rhythm data is plausible.

---

## Storytelling and dramatic context

For film, game, visual-novel, theater or other narrative work, determine whether music is functioning as:

```text
underscore / non-diegetic support
source / diegetic music
character / place association
scene transition
emotional contour
foreground musical event
```

Recognizable stylistic references can carry learned associations, but those associations are contextual.

Do not universalize a local musical topic into a global emotional rule.

Example of the correct reasoning shape:

```text
requested narrative association
-> identify relevant cultural / stylistic evidence
-> choose musical behavior that supports it
```

not:

```text
instrument X = emotion Y
mode X = emotion Y
```

---

## Cultural and regional styles

When the user requests a culturally specific or regional tradition:

1. identify whether validated Skill / Material evidence exists;
2. use that evidence if available;
3. if it does not exist, do not invent a detailed style grammar from stereotypes;
4. for serious stylistic imitation, switch to explicit source study or request/use appropriate reference material;
5. keep exact cultural claims separate from generic musical reasoning.

A broad genre or regional name may encode history, community, performance practice and social meaning as well as sound.

Do not imply that one musical practice represents every member of a nation or culture.

---

## Interaction with instrumentation-role-planning

For multi-instrument composition, this Skill may clarify the musical context first, then hand off to:

```text
instrumentation-role-planning
```

Correct order:

```text
brief
-> purpose / style context
-> required musical functions
-> instrument palette
-> roles / section entry / exit
-> Material retrieval
```

Do not reverse this into:

```text
genre
-> familiar instrument Material
-> force the composition around it
```

---

## Interaction with style Materials

This Skill does not contain production-ready recipes for:

```text
ragtime
swing
disco
reggae
psychedelic rock
North Indian raga
Javanese gamelan
or any other specific tradition
```

Detailed behavior should come from dedicated evidence-backed Skills or Materials.

If no such knowledge exists, stay conservative about stylistic claims.

---

## Decision procedure

1. Read the brief and identify whether purpose/function is explicit.
2. Record the requested genre/style without expanding it into stereotypes.
3. Separate instrumentation, role, energy, texture and timbre requirements already stated by the user.
4. Identify which musical dimensions are likely to carry the requested identity.
5. Determine whether the target is fixed, arranged, improvisatory or studio-constructed when relevant.
6. Determine the performance/consumption context when it changes musical decisions.
7. Retrieve only specialized Skills/Materials that match the chosen dimensions.
8. For multi-instrument writing, run `instrumentation-role-planning` before detailed Material selection.
9. If cultural/style specificity exceeds available evidence, do not fabricate precision.
10. Keep source-library evidence closed during ordinary composition.

---

## Validation questions

### Context separation

- Did the Agent keep genre, instrumentation, energy and texture distinct?
- Did it infer a hidden stereotype that the user never requested?

### Purpose

- Does the musical plan support what the music is for?
- Is repetition/contrast appropriate to the intended use rather than a house default?

### Style evidence

- Which style-defining behaviors are actually supported by active Skills/Materials?
- Is the Agent making claims beyond its evidence?

### Timbre / realization

- Is important style identity dependent on technique or timbre that the current profile cannot express?
- If so, was that limitation acknowledged rather than hidden?

### Creation mode

- Is the Agent treating improvisation as bounded musical freedom rather than randomness?
- Is a studio-constructed work being forced into a live-performance mental model?

---

## Failure modes

### Genre preset collapse

Symptom:

```text
rock -> loud distorted electric guitars
```

without support from the brief.

Fix: separate genre, instrumentation, energy and texture.

### Style encyclopedia bloat

Symptom: this Skill grows into hundreds of mini genre recipes.

Fix: move detailed style behavior to specialized Skills/Materials and keep this file navigational.

### Cultural stereotype synthesis

Symptom: a regional label causes the Agent to invent instrumentation, scales or ornaments from vague familiarity.

Fix: require explicit evidence or source study.

### Harmony universalism

Symptom: every style is analyzed as melody + chord progression even when another organizing model is more appropriate.

Fix: use the cross-style musical dimensions and apply harmony only when useful to the active practice.

### Random improvisation

Symptom: `improvised` means arbitrary pitches and rhythms.

Fix: identify the fixed framework and the actual freedom scope.

### Timbre-last thinking

Symptom: the notes are style-aware but all realization uses generic interchangeable patches.

Fix: route style-bearing timbre and articulation to instrument Materials / Profiles.

---

## Provenance

This Skill is distilled from:

```text
source_library/studies/resonances_music_practice_map.md
```

which studies Esther M. Morgan-Ellis (ed.), *Resonances: Engaging Music in Its Cultural Context*.

Only broad reusable navigation principles were promoted here. Detailed historical narratives, cultural claims and individual genre examples remain in the source study rather than ordinary composition context.