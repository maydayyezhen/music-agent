# Source Study: Comprehensive Musicianship — A Practical Resource

## Source identity

- Authors: Randall Harlow, Heather Peyton, Jonathan Schwabe, Daniel Swilley
- Title: *Comprehensive Musicianship, A Practical Resource*
- Publication year: 2022
- Institution: University of Northern Iowa / Iowa Regents OER Grant Program
- License: CC BY-NC-SA 4.0
- Study scope for this repository: selected material from Chapters 1, 6, 7, 8 and 11, with emphasis on melody writing, melodic form, cadence, harmonic rhythm and melody harmonization
- Purpose: extract reusable composition reasoning without copying score examples or importing common-practice teaching constraints as universal rules

This study is **source evidence**, not default composition memory.

Do not load it during ordinary composition unless the task explicitly asks to revisit, verify or compare the source.

---

## Evidence discipline

The source mixes several kinds of knowledge:

1. style-neutral structural concepts;
2. useful modern pedagogical organization;
3. classical/common-practice form and voice-leading practice;
4. classroom heuristics and simplifying restrictions.

Therefore promotion follows:

```text
source observation
-> reusable invariant
-> target layer
-> promotion decision
```

The target layers used by this repository are:

```text
melody-structure-development
classical-melody-practice
melody-harmony-coordination
source evidence / deferred heuristic
```

A textbook statement that something is common does not make it a universal validator rule.

---

# 1. Rhythm is compositional syntax

## Source observation

The rhythm chapters explicitly connect rhythm to motive creation and development, texture, meter, transitions, phrase and cadence marking, harmonic change rate and musical energy.

## Reusable invariant

Rhythm is part of melodic identity and structural syntax, not merely note duration metadata.

Useful Agent dimensions include:

```text
rhythmic signature
metrical footprint
rest pattern
subdivision density
duration contrast
```

A motive may preserve rhythm while pitch changes, preserve pitch while rhythm changes, or preserve both.

## Promotion decision

Promote rhythmic identity more explicitly into `melody-structure-development`.

Do not promote fixed energy mappings or fixed rhythmic densities as universal rules.

---

# 2. Range as a compositional plan

## Source observation

Chapter 7.1 treats melodic range as meaningful in relation to performer, singability and musical purpose. Examples contrast narrow, easily sung ranges with wide virtuosic ranges.

## Reusable invariant

Range should be planned, not merely checked after generation.

Useful concepts:

```text
working register
working range
range expansion
range contraction
structural high point
structural low point
exception register
```

Sections may deliberately expose new register over time.

## Promotion decision

Promote `range plan` and `register trajectory` into the generic melody Skill.

## Deferred heuristic

The source observes that mass-singable folk/popular/traditional melodies often use roughly an octave or less. Treat this only as a singability heuristic, never as a universal pitch-range cap.

---

# 3. Interval structure as a profile, not a quota

## Source observation

The source distinguishes conjunct, disjunct and balanced melodic motion according to the relative use of steps and leaps.

## Reusable invariant

An Agent can measure interval behavior across a phrase or section:

```text
step ratio
repeat ratio
small-leap ratio
large-leap ratio
median interval
interval-direction changes
```

These measurements are useful for comparison, diagnosis and planned contrast between sections.

## Promotion decision

Promote the idea of an interval-structure profile.

Do not create a global numerical threshold for what counts as a good melody.

---

# 4. Gesture and structural contour

## Source observation

Chapter 7.1 names large melodic gestures such as:

```text
arch
inverted arch
ascending
descending
stationary
```

The exercises explicitly remove decorative tones in order to perceive the underlying progression of the melodic line.

## Reusable invariant

Gesture is most useful as a description of the **reduced structural contour**, not as a mandatory template for every surface note.

It can help compare phrases, locate directional change and evaluate whether a climax belongs to the whole line rather than appearing as an isolated highest note.

## Promotion decision

Promote structural gesture / contour planning into `melody-structure-development`.

## Historical / expressive boundary

The source associates ascending lines with increased tension, descending lines with release and other shapes with expressive meanings. Preserve these only as possible expressive associations, not universal emotional mappings.

---

# 5. CREATE / VARY / REPEAT

## Source observation

Chapter 7.2 explicitly frames melodic continuation as three choices:

```text
CREATE
VARY
REPEAT
```

`CREATE` introduces new material.

`VARY` changes existing material while keeping it recognizably related, including changes to contour, rhythm, decoration, pickup or ending behavior.

`REPEAT` reuses material directly or primarily preserves it at another pitch level.

## Reusable invariant

Before generating the next phrase or region, an Agent should consciously choose its relationship to prior material.

This is a strong defense against bar-by-bar amnesia.

A useful planning sequence is:

```text
A    = CREATE
A'   = VARY(A)
A''  = VARY(A)
B    = CREATE
A''' = RECALL / VARY(A)
```

## Promotion decision

Promote `CREATE / VARY / REPEAT` as explicit phrase- and region-level decisions in `melody-structure-development`.

---

# 6. Variation needs preserved and changed dimensions

## Source observation

The source repeatedly classifies material as a variation when it changes some dimensions but remains recognizably related.

## Reusable invariant

Variation should not be an opaque label. Track what survives and what changes.

Possible identity dimensions:

```text
pitch shape
interval signature
rhythmic signature
metrical footprint
register
characteristic fragment
ending behavior
```

A useful representation is:

```text
relation: VARY(source)
preserve: [rhythm, first interval]
change: [ending, register, contour tail]
```

## Promotion decision

Promote this reasoning into the motif / phrase development section of the generic Skill.

---

# 7. Motive identity may split into pitch and rhythm

## Source observation

The source discusses motives as short building blocks and explicitly notes that pitch and rhythmic elements can be reused together or independently.

## Reusable invariant

Motif identity should not be represented only as a literal note list.

Useful components:

```text
pitch identity
interval identity
rhythm identity
metrical identity
contour identity
characteristic fragment
```

This supports related material that is audibly connected without being copy-pasted.

## Promotion decision

Promote explicit pitch/rhythm identity separation into `melody-structure-development`.

---

# 8. Sequence taxonomy

## Source observation

Chapter 7.2 distinguishes:

```text
real sequence
= exact interval qualities preserved

tonal sequence
= interval quality may adjust to remain in the active key

modified sequence
= rhythm or contour also changes
```

## Reusable invariant

The existing generic `sequence(unit)` operator can benefit from more explicit intent:

```text
exact-interval sequence
tonal-context sequence
modified sequence
```

## Promotion decision

Promote the taxonomy as optional operator semantics.

## Deferred heuristic

The source mentions a common “rule of 3” in which sequence statements often occur three times before moving on. Keep this as a source heuristic only. It must not become a global generator rule.

---

# 9. Progressive revision distance

## Source observation

Several Chapter 7 exercises use a productive revision procedure:

```text
start with the source melody
-> change only a few notes near the end
-> repeat with more changes
-> eventually improvise a new melodic path using known material
```

Other exercises ask the student to identify short motives and recombine them.

## Reusable invariant

Revision can be parameterized by development distance:

```text
low    -> ending-only change
medium -> tail contour + rhythm change
high   -> recombine known motives into a new phrase
```

## Promotion decision

Promote as a revision workflow, especially when a user says the melody is almost good and wants local improvement rather than full regeneration.

---

# 10. Embellishing-tone vocabulary

## Source observation

Chapter 7.3 expands the non-chord-tone vocabulary and treats these tones as means to decorate, expand, create interest and create motion.

Relevant families include:

```text
passing tone
neighbor tone
double neighbor / enclosure
appoggiatura
incomplete neighbor
escape tone
anticipation
pedal tone
suspension
retardation
```

## Reusable invariant

These labels are useful when treated as **surface functions around structural tones**.

Examples:

```text
passing:
A -> connector -> B

neighbor:
target -> adjacent -> same target

anticipation:
future target arrives early

suspension-like delay:
old pitch survives into new harmonic region

retardation-like delay:
delayed pitch resolves upward
```

## Promotion decision

The generic Skill already owns passing, neighbor, anticipation, suspension-like and appoggiatura-like functions. Add retardation-like delay and enclosure / double-neighbor as optional generic surface functions.

## Classical boundary

Strict accent placement, preparation/resolution formulas and numbered suspension types belong in `classical-melody-practice`.

---

# 11. Structural reduction should be reversible

## Source observation

Chapter 7 exercises encourage removing NCTs to expose the structural line, then comparing the reduced and embellished versions.

## Reusable invariant

A strong melody system should support both directions:

```text
surface melody
-> structural reduction
-> analysis / repair

structural melody
-> controlled embellishment
-> surface melody
```

## Promotion decision

Keep this as a central generic melody architecture principle.

---

# 12. Phrase is interaction, not a bar counter

## Source observation

Chapter 8 describes a phrase as a substantial musical thought shaped through interaction of melody, harmony and rhythm and ending with a cadence. It notes that phrases are often 4, 8 or 16 bars, while also explicitly allowing other lengths.

## Reusable invariant

Phrase boundaries should be inferred from multiple cues:

```text
melodic punctuation
rest / hold
harmonic closure
rhythmic closure
motif completion
register arrival
```

## Promotion decision

Promote the multi-cue phrase-boundary principle.

## Classical boundary

Common 4/8/16-bar spans remain useful classical practice frames, not universal lengths.

---

# 13. Phrase-relation labels

## Source observation

The source uses simple labels:

```text
aa  = exact repetition
aa' = varied repetition
ab  = contrast
```

## Reusable invariant

This provides a compact reporting vocabulary for larger form while the generic Skill can retain richer relation labels such as parallel, lightly varied, partial recurrence and strongly contrasting.

## Promotion decision

Use `a / a' / b` as optional analysis/report labels, not as the only planning language.

---

# 14. Sentence, Period and larger phrase forms

## Source observation

Chapter 8 presents several form families:

```text
Sentence
Period
Parallel Period
Contrasting Period
Phrase Group
Double Period
```

The Period discussion emphasizes the dependency between an antecedent with a weaker/progressive cadence and a consequent with stronger closure.

The source also allows asymmetrical phrases and periods.

## Reusable invariant

The broadly useful abstraction is hierarchical phrase relationship:

```text
motif
-> phrase
-> phrase pair
-> phrase group
-> section
```

At each level, melodic similarity and closure function are separate dimensions.

For example:

```text
melodic_relation: similar / varied / contrasting
closure_relation: open / dependent / conclusive
```

## Promotion decision

Promote hierarchical phrase relationship and asymmetry tolerance into the generic layer.

Route Sentence, Period and Double Period as named historical/formal families into `classical-melody-practice`.

---

# 15. Phrase elision

## Source observation

Chapter 8.4 describes phrase elision in which the expected ending of one phrase also functions as the beginning of the next phrase, producing overlap, shortening and asymmetry.

## Reusable invariant

A phrase boundary may be intentionally overlapped rather than separated.

Generic abstraction:

```text
phrase-boundary overlap
A end = B beginning
```

This can apply beyond classical music to vocal pickups, hook overlap, game-loop transitions and continuous lead writing.

## Promotion decision

Promote `phrase elision / boundary overlap` into generic phrase-development vocabulary.

---

# 16. Pre- and post-closure extension

## Source observation

Chapter 8.4 distinguishes:

```text
pre-cadential extension
= expected closure is delayed before arrival

post-cadential extension
= closure occurs, then a tag extends the phrase afterward
```

## Reusable invariant

Use style-neutral terms:

```text
delay closure
post-closure tag
```

These are meaningful structural operations, not simply “add two bars.”

## Promotion decision

Promote both into the generic Skill as optional phrase operators.

---

# 17. Cadence as relative closure strength

## Source observation

Chapter 6.2 treats cadences as points of rest, separation and punctuation and explicitly notes different degrees of finality and strength. Strength depends on harmony, inversion, melodic motion and metric placement.

## Reusable invariant

For style-neutral composition, closure is more useful as a graded function than as a yes/no classical cadence label.

Possible representation:

```text
closure role:
continuation
pause
local close
section close
final close

closure strength:
weak <-> strong
```

## Promotion decision

Route the generic concept to `melody-harmony-coordination`.

Keep PAC / IAC / HC / PHC / DC / PC terminology in classical practice.

---

# 18. Harmonic rhythm coordinates melody and harmony

## Source observation

Chapter 6.3 links harmonic rhythm to meter, tempo, cadence approach, phrase similarity and compositional variety. It also notes that slower harmonic rhythm can leave more room for ornate melody.

## Reusable invariant

Melodic density and harmonic rhythm should be co-designed.

Useful reasoning:

```text
slow harmonic rhythm
-> more room for surface ornament

faster harmonic rhythm
-> structural arrivals need clearer coordination
```

This is a tendency, not a fixed formula.

## Promotion decision

Create a dedicated `melody-harmony-coordination` Skill rather than bloating the generic melody Skill.

---

# 19. Chord-tone status depends on context

## Source observation

Chapter 11.5 shows that a soprano note may be treated as a chord tone or as a non-chord tone depending on harmonic rhythm and melodic motion.

## Reusable invariant

```text
note function
!= membership test alone
```

Interpret structural/harmonic role using:

```text
harmonic rhythm
metrical position
duration
approach / departure
phrase role
recurrence
```

## Promotion decision

Promote into `melody-harmony-coordination` and reinforce the generic melody principle that chord tone does not automatically mean structural tone.

---

# 20. Harmonization is candidate search

## Source observation

Chapter 11 teaches harmonizing a melody through a staged process:

```text
identify tonal context
identify phrase / cadence structure
plan harmonic rhythm
list chord possibilities
eliminate incompatible choices
choose a progression
inspect bass
complete inner voices
```

The text explicitly recognizes that multiple harmonizations can exist and that the important analytical skill is explaining why one candidate is preferable to another.

## Reusable invariant

Harmony selection should be:

```text
generate candidates
-> evaluate in context
-> explain tradeoffs
-> select
```

Do not harmonize every melody note independently.

Candidate scoring may consider:

```text
phrase support
closure strength
harmonic-rhythm consistency
bass continuity
style compatibility
foreground space
voice-leading / instrument feasibility
```

## Promotion decision

Promote into the new `melody-harmony-coordination` Skill.

---

# 21. Bass is part of harmonization quality

## Source observation

Chapter 11 notes that inversions can create a smoother and more singable bass line.

## Reusable invariant

Harmony selection should hand a bass trajectory to the existing `bass-line-continuity` layer rather than forcing every bass event to be a root.

## Promotion decision

Add an explicit coordination handoff:

```text
melody-harmony-coordination
-> chosen harmonic path / inversion intent
-> bass-line-continuity
```

---

# 22. Classical/common-practice details to preserve conditionally

The source gives detailed traditional material involving:

- Sentence / Period / Double Period families;
- antecedent and consequent cadence dependency;
- PAC / IAC / HC / PHC / DC / PC categories;
- strict NCT distinctions by approach/departure and metric accent;
- suspension preparation, suspension and resolution;
- traditional numbered suspensions such as 9-8, 7-6, 4-3 and bass 2-3;
- retardation as upward resolution;
- tonic/dominant pedal usage in common-practice contexts;
- chord-function priorities, inversions, seventh-chord resolution and four-part voice-leading exercises.

These are useful, but they belong to classical/common-practice layers.

## Promotion decision

Promote the melody/form-facing subset to `classical-melody-practice`.

Do not make a new universal harmony rule set from the Chapter 11 classroom restrictions.

A future `classical-harmony-practice` Skill may own traditional harmonization, inversion, seventh-chord and part-writing rules if that workflow becomes active.

---

# 23. Deferred heuristics and classroom restrictions

Do not promote the following as universal laws:

```text
singable melody must stay within one octave
ascending always means tension
sequence should always occur three times
phrase should be 4 / 8 / 16 bars
one location may contain only one NCT
every melody should begin and end on tonic
avoid iii / vi globally
ii must never move to I in every style
traditional seventh-resolution rules apply to all genres
```

These are either tendencies, style-conditioned practice or pedagogical simplifications.

---

# 24. Promotion summary

## Promote to `melody-structure-development`

- range / register plan;
- interval-structure profile as measurement;
- structural gesture / contour;
- explicit CREATE / VARY / REPEAT decisions;
- motif identity split across pitch, rhythm, contour and meter;
- progressive revision distance;
- enclosure / double-neighbor and retardation-like surface functions;
- multi-cue phrase boundaries;
- hierarchical phrase relations;
- asymmetry tolerance;
- phrase elision / boundary overlap;
- delayed closure and post-closure tag.

## Promote to `classical-melody-practice`

- Sentence / Period / Double Period as named practice families;
- antecedent / consequent closure dependency;
- traditional cadence families;
- traditional NCT distinctions and suspension types;
- classical phrase / cadence exercise practice.

## Create `melody-harmony-coordination`

- closure strength;
- harmonic rhythm planning;
- contextual chord-tone / NCT interpretation;
- harmonization candidate generation and elimination;
- bass-contour handoff.

## Keep as source evidence

- one-octave singability observation;
- fixed expressive meanings for gesture;
- sequence rule-of-three;
- fixed phrase-length frequencies;
- classroom-specific harmonization restrictions.

---

# 25. Recommended empirical follow-up

Use modern MIDI / score sources to validate the newly promoted generic abstractions.

Useful measurements:

```text
range trajectory by section
highest / lowest note placement
interval-structure profile
structural gesture
CREATE / VARY / REPEAT region map
pitch-motif recurrence
rhythm-motif recurrence
phrase lengths and asymmetry
phrase elision frequency
pre-closure delay
post-closure hook tag
harmonic rhythm versus melodic density
closure strength versus section role
```

Promote style-specific Materials only after source comparison or listening validation.
