# Resonances: Music Practice and Style Map

> Source study of Esther M. Morgan-Ellis (ed.), *Resonances: Engaging Music in Its Cultural Context*, University of North Georgia Press.
>
> Source license: CC BY-SA 4.0 for the book's original content, with the book's own note that incorporated third-party material may carry other licenses.
>
> Study purpose: extract a broad navigation model for a Music Agent. This is not a genre encyclopedia and is not composition memory.

## Study mode boundary

This file belongs in `source_library/` and is evidence for explicit `source_study` work only.

Do not load this file during ordinary composition.

Promote only reusable abstractions into `skills_v2/` or validated style vocabulary into `materials_v2/`.

---

## Why this source is useful

The book is intentionally organized by the roles music plays in human life rather than by a single chronological or genre taxonomy. It brings classical, folk, popular and geographically diverse traditions into the same thematic chapters.

The author also explicitly rejects the idea that a definitive comprehensive survey of important music is either possible or desirable. The value of the source is therefore not that it supplies a complete genre tree. Its value is that it provides a **multi-axis way of thinking about music**.

For the Music Agent, the main promotion target is:

```text
not: genre label -> automatic recipe

but:
brief
-> purpose / use
-> style / genre context
-> musical dimensions
-> creation / performance mode
-> instrumentation / timbre / texture
-> form / repetition / variation / contrast
-> relevant specialized knowledge
```

---

# 1. Category warning: genre is useful but incomplete

Source pages: Chapter 2, especially book pp. 32-40.

The source examines the familiar tripartite categories:

```text
classical
popular
folk
```

and shows why each becomes unstable at the boundaries.

Examples from the source include:

- music now called classical could have functioned as commercial popular entertainment in its own time;
- experimental orchestral music may share little with older canonical repertory despite both being called classical;
- popular music can contain experimental work that does not behave like mass-market music;
- music that circulates orally or lacks a named composer is not automatically folk;
- sophisticated non-Western classical traditions cannot be collapsed into folk merely because they use different transmission systems.

### Reusable conclusion

```text
genre is one descriptive axis
!= complete musical identity
```

A genre label may communicate some combination of:

```text
style
instrumentation
historical period
geography
performance venue
audience / community
social meaning
commercial category
```

but different genre labels communicate different subsets of those dimensions.

The source's comparison of `string quartet` and `French reggae` is especially useful:

- `string quartet` gives precise instrumentation and a performance-family expectation but does not determine a unique style, historical era or emotional character;
- `reggae` gives stronger stylistic, historical and cultural information while allowing instrumentation to vary.

### Agent implication

Never expand a genre word into an entire hidden preset.

Do not infer, without additional evidence:

```text
rock = loud
rock = distortion
rock = electric guitar only
classical = orchestra
folk = simple
jazz = random improvisation
world music = non-Western ornament
```

---

# 2. Purpose / use is a first-class musical dimension

Source organization and Chapter 2.

The book groups music by social or practical role, including broad areas such as:

```text
storytelling
entertainment
political expression
spiritual expression
movement / marching / dancing
domestic listening
public concert listening
```

The source explicitly argues that understanding what music is **for** can help explain why musical decisions were made.

### Reusable conclusion

Add purpose/function to the Agent's musical planning model.

A useful navigation field is:

```text
purpose:
  narrative / characterization
  foreground song
  background / underscore
  dance / movement
  ritual / spiritual
  political / communal identity
  concert / attentive listening
  domestic / private listening
  recorded / studio work
  functional / ambient support
  other / mixed
```

These are navigation categories, not exhaustive ontology.

### Important source tendency

Purpose can influence the acceptable balance of repetition, variation and contrast.

The source contrasts dance music with sung theater:

```text
dance-oriented use
-> favors stable tempo / rhythmic character / mood
-> often tolerates or benefits from high repetition

story / character-oriented use
-> can support more contrast and variation
-> contrast can help communicate changing dramatic information
```

Do not convert this into hard rules. Treat it as a purpose-conditioned tendency.

---

# 3. A cross-style musical-dimension map

Source: Chapter 2, *The Elements of Music*.

The book supplies a useful common vocabulary across very different traditions:

```text
rhythm
pitch
volume / dynamics
articulation
timbre
texture
form
```

For Agent navigation, these can be expanded to:

```text
rhythm:
  pulse
  meter / cycle
  subdivision
  syncopation
  rhythmic density
  tempo behavior

pitch:
  melodic material
  register / range
  pitch system / mode / scale / raga / makam / other
  harmony when relevant

dynamics:
  level
  contour
  contrast

articulation:
  attack
  sustain
  release
  connected vs detached behavior

timbre:
  sound source
  performance technique
  processing
  spectral / noise character

texture:
  monophonic
  homophonic
  polyphonic
  heterophonic
  dense / sparse
  foreground / background relations

form:
  repetition
  variation
  contrast
  section ordering
  large-scale timing
```

### Timbre is not decoration

The source explicitly treats timbre as integral to genre and style and notes that traditions develop characteristic timbral expectations.

Agent implication:

```text
style != notes + generic instrument patch
```

Timbre, articulation and performance technique may be part of style identity and should be routed to instrument skills, profiles or style materials where evidence exists.

---

# 4. Repetition, variation and contrast are global organizing operations

Source: Chapter 2, form discussion.

The source describes three basic organizational principles:

```text
repetition
variation
contrast
```

These can operate on:

```text
long melody
short motif
rhythm
harmony
accompaniment
section
texture
```

This strongly aligns with the repository's melody-level:

```text
REPEAT
VARY
CREATE
```

but the source supports a broader interpretation: the same logic can organize entire arrangements and forms, not only melody.

### Promotion decision

Do not duplicate `CREATE / VARY / REPEAT` into every Skill.

Instead, navigation may remind downstream skills to ask:

```text
what is intentionally repeated?
what is varied?
what provides contrast?
which dimension carries the contrast?
```

A new section does not need new material in every dimension simultaneously.

---

# 5. Creation mode: fixed composition and improvisation are a continuum of responsibilities

Source: Chapter 2, *Fixed Composition vs. Improvisation*.

The source distinguishes fixed composition from improvisation but emphasizes that improvisation is not unconstrained randomness.

Improvisers create new material while respecting style- and composition-specific boundaries.

Examples given in the source demonstrate different freedom models:

```text
jazz:
  improvisation constrained by form and harmonic structure

West African balafon practice:
  variation of repeated melodic material supporting singing

Javanese gamelan:
  performers vary a melodic framework in response to ensemble signals

Baroque performance:
  fixed composition with style-conditioned ornamentation freedom
```

### Agent abstraction

Use creation-mode fields such as:

```text
creation_mode:
  fixed_composition
  arranged
  semi_fixed
  improvisatory
  studio_constructed

freedom_scope:
  pitch
  rhythm
  ornament
  phrase
  texture
  instrumentation
  form
```

These fields describe responsibility and flexibility, not quality.

---

# 6. Performance and transmission are part of musical identity

The source repeatedly shows that the same abstract musical material may behave differently depending on how it is transmitted and performed.

Useful dimensions include:

```text
notation-centered
lead-sheet / chart-centered
aural / oral transmission
improvisatory tradition
studio-layered construction
live ensemble interaction
community participation
solo performance
```

This matters because a MIDI Agent otherwise tends to assume:

```text
composition = every final note pre-authored
```

That assumption is valid for some traditions and false for others.

### Agent implication

When emulating a tradition, ask whether MIDI should represent:

```text
a fixed finished performance
an arrangement framework
a repeatable pattern with variation slots
an improvisation scaffold
```

Do not force every tradition into one notation-centered authorship model.

---

# 7. Storytelling and characterization

Source: Chapters 3-6.

The source treats music as a storytelling tool that may:

```text
set mood
characterize a person or place
amplify emotion
shape dramatic contour
support memory of words / events
communicate beyond literal language
```

It distinguishes:

```text
non-diegetic / underscoring
  music for the audience, not heard by characters

diegetic / source music
  music that exists inside the dramatic world
```

This is directly useful for game / film / visual-novel work.

### Storytelling techniques supported by the source

For instrumental storytelling, the source describes:

```text
mimesis
  imitate real-world sound

quotation
  invoke another piece / familiar content

musical topic
  invoke culturally learned style or technique associated with a subject
```

### Cultural-memory caution

A musical topic works because listeners have learned an association. It is not a universal acoustic truth.

Therefore:

```text
recognized association
-> possible narrative shorthand
!= universal emotion mapping
```

Do not create a global rule such as:

```text
flute = pastoral
minor = sad
march rhythm = military in every culture/context
```

without relevant style/context evidence.

---

# 8. Song and narrative

Source: Chapter 5.

The book calls song one of the most familiar and widespread forms of musical storytelling and stresses that songs can serve many other functions as well, including worship, scene description and dancing.

It also distinguishes related large-form concepts:

```text
song cycle
concept album
```

Both can create a cohesive larger experience from multiple songs, but their production/performance contexts differ.

### Agent implication

For a multi-song or multi-cue project, large-scale coherence can exist above individual tracks through:

```text
shared narrative
shared sound world
recurring motifs
ordered emotional trajectory
production continuity
```

Do not assume an album or soundtrack is merely a bag of independent tracks.

---

# 9. Recording medium can become part of composition

Source: Chapter 8, especially the discussion of *Sgt. Pepper's Lonely Hearts Club Band*.

The source describes a shift from songs as live-reproducible performances toward studio works deliberately designed as recordings.

Key observations:

- the album can be conceived as an extended unified work;
- studio production can enable music that cannot be reproduced live in the same way;
- multitrack recording allows separately recorded material to become one composed sound object;
- recording technology, editing, overdubbing and ambient sound can become compositional resources;
- the studio can function as a musical instrument.

### Agent implication

Keep these separate:

```text
composition
arrangement
performance realization
studio / renderer construction
```

But recognize that some styles intentionally make production part of the authored musical result.

For MIDI-first work, this means the structured score may need explicit production intent in a later realization layer rather than pretending the note data alone contains the full style.

---

# 10. Evidence examples: style is behavior, not merely instrumentation

The following examples are preserved as source evidence, not universal templates.

## Ragtime

Source: Chapter 3.

Observed traits in the source include:

```text
steady left-hand pulse
alternation of low/high accompaniment register
complex right-hand syncopation
dance connection
repeated strain-based form
```

Promotion decision:

Do not create a generic `ragtime = piano` rule. If ragtime becomes a supported style, study it separately and validate with additional sources/examples.

## Swing

Source: Chapter 12.

The source emphasizes:

```text
dance function
swung rhythmic behavior
arranged sectional writing
call and response
repeated passes through known song material
increasing rearrangement / improvisation across passes
strong rhythm-section drive
```

Useful broader abstraction:

```text
repetition can remain recognizable while orchestration, countermelody and improvisation progressively transform the surface
```

## Disco

Source: Chapter 12.

Observed traits include:

```text
fast tempo
four-on-the-floor pulse
dense texture
rhythmic guitar / percussion layers
syncopated electric bass
instrument layers entering and leaving
extended duration for dancers / DJs
```

Broader abstraction:

```text
repetitive groove does not require static arrangement
```

Variation may come from layer entry/exit and timbral change rather than constant harmonic or melodic novelty.

## Psychedelic rock / Hendrix case

Source: Chapter 7.

The source emphasizes electric guitar not only as a pitch instrument but as a sound-sculpting system through:

```text
distortion
feedback
wah
vibrato / whammy-bar effects
noise / timbral exploration
riff-centered songwriting
live improvisatory expansion
```

Broader abstraction:

```text
instrument technique + processing can be compositionally central
```

Do not reduce rock lead writing to note choice alone.

## Studio rock / Beatles case

Source: Chapter 8.

The source demonstrates:

```text
recording as composition
concept-album coherence
style mixing
meter / key / instrumentation contrast between sections
large timbral transitions
studio-only layering
```

Broader abstraction:

```text
production medium can define what a musical work is capable of being
```

---

# 11. Evidence examples: non-Western traditions resist Western default assumptions

These examples are especially important as anti-bias evidence.

## North Indian raga

Source: Chapter 6, Raga Madhuvanti.

The source shows that a raga is much richer than a Western scale label. It may specify or imply:

```text
ascending / descending pitch behavior
pitch hierarchy
microtonal tuning
approach / ornament behavior
resting points
typical identifying phrases
extramusical associations
```

Performance may include:

```text
free-rhythm opening exploration
progressive register expansion
gradual introduction of pulse
rhythmic cycle / tala
fixed gat material
improvisation using fragments under raga rules
increasing rhythmic complexity
```

The source compares different performances of the same raga that sound very different while remaining recognizably within the same tradition.

### Agent implication

```text
scale name != complete style grammar
```

Do not emulate raga by choosing a seven-note pitch collection and adding generic ornaments.

Exact raga composition requires dedicated source study and performance-aware support.

## Javanese gamelan

Source: Chapter 4.

The source describes:

```text
cyclic structure marked by characteristic gong timbres
ensemble-specific tuning
heterophonic realizations of a shared melody
ornate / spare / syncopated versions across instruments
improvised melodic lines related to the main contour
ensemble coordination and dramatic shaping
```

### Agent implication

A texture can be organized around **multiple idiomatic realizations of one melodic identity**, rather than Western melody-plus-chord accompaniment.

Do not map gamelan to generic General MIDI bells and call the style complete.

## West African jali / Sunjata

Source: Chapter 5.

The source presents epic recitation as a living, variable practice in which:

```text
story wording may vary
story events may vary
melody may vary
instrumentation may vary
kumbengo accompaniment may vary
listeners may participate
performance context matters
```

### Agent implication

A tradition may preserve identity through social function, story, formulas and performance practice rather than a fixed canonical score.

## Chinese pipa repertoire

Source: Chapter 6.

The source notes a strong aural tradition even where historical notation exists. Notation can serve preservation/reference without being the primary way unfamiliar music is learned or performed.

### Agent implication

Do not equate:

```text
written notation
=
complete musical knowledge
```

Instrument technique and oral transmission may carry information that a MIDI event list does not capture.

---

# 12. Function can constrain form, rhythm and density

The strongest cross-source pattern is:

```text
musical purpose
-> changes what counts as useful repetition, contrast, clarity and complexity
```

Examples preserved by the source:

### Marching

Music supporting coordinated movement prioritizes a clear regular pulse and movement-compatible meter/tempo.

### Dance

Dance traditions commonly prioritize pulse, groove, repetition and sustained motion. Arrangement variation may be preferable to disruptive formal contrast.

### Dramatic storytelling

Dramatic music may use larger changes in texture, register, meter, harmony, timbre or thematic material to communicate scene and character changes.

### Domestic / intimate listening

Performance space and listener proximity can encourage smaller forces and detail-oriented writing.

### Studio listening

Recording removes the requirement that every audible result be reproducible in one live take and can make editing/layering a compositional dimension.

### Promotion boundary

These are purpose-conditioned tendencies.

Never promote them to unconditional style validators.

---

# 13. Context and culture are not optional metadata

The source repeatedly shows that musical meaning depends on learned cultural associations, social practice, historical circumstances and audience expectations.

This matters for Agent design in two directions.

## Do not essentialize cultures

Avoid claims such as:

```text
nation X sounds like instrument Y
culture X always uses rhythm Z
style X represents all members of community Y
```

The source explicitly warns that claims of national representation can exclude members who do not fit the claimed musical identity.

## Do not erase context either

The opposite mistake is to treat every style as only a technical parameter bundle.

For some traditions, history, community, ritual, performance setting or identity is central to what the music means and how it is made.

### Agent policy

```text
technical style description
+
context boundary
```

When context is not needed for the user's creative task, it need not dominate the prompt. But the Agent should not invent culturally specific behavior from stereotypes.

---

# 14. Proposed Music Practice Map

This is the main reusable abstraction from the source.

```text
Music Practice Map

1. PURPOSE / FUNCTION
   storytelling / characterization
   song / foreground communication
   dance / movement
   ritual / spiritual
   political / identity
   concert / attentive listening
   domestic / private listening
   background / functional support
   recorded / studio object

2. GENRE / STYLE CONTEXT
   genre family
   subgenre
   historical period
   region / tradition
   hybrid influences

3. MUSICAL DIMENSIONS
   rhythm / meter / cycle
   melody / pitch organization
   harmony when relevant
   dynamics
   articulation
   timbre
   texture
   form

4. CREATION MODE
   fixed composition
   arrangement
   semi-fixed performance
   improvisation
   studio construction

5. TRANSMISSION / AUTHORSHIP
   notation
   lead sheet / chart
   oral / aural
   communal / participatory
   composer-led
   performer-led
   producer-led

6. PERFORMANCE / CONSUMPTION CONTEXT
   live public
   intimate / domestic
   dance floor
   ritual
   dramatic scene
   headphones / recording
   interactive game / adaptive context

7. IMPLEMENTATION HANDOFF
   instrumentation-role-planning
   style-specific Skill / Material
   instrument Skill / Material
   profile / renderer capability
```

The map is not a requirement to fill every field.

Use only the dimensions that materially affect the task.

---

# 15. Promotion decisions

## Promote to active navigation Skill

Promote only these reusable procedures:

1. genre is not a complete recipe;
2. separate purpose, style, instrumentation, role, energy, texture and performance context;
3. use musical dimensions as a cross-style comparison language;
4. ask what is repeated, varied and contrasted;
5. identify whether the tradition is fixed, arranged, improvisatory or studio-constructed;
6. treat timbre / articulation / technique as possible style-bearing information;
7. route detailed stylistic behavior to specialized evidence rather than inventing it;
8. avoid cultural essentialism and false precision.

## Keep in source study

Do not place these detailed examples into default context:

```text
ragtime recipe
swing recipe
disco recipe
Hendrix rig / exact effects
Beatles album details
Raga Madhuvanti rules
gamelan tuning / instrument details
Sunjata performance details
pipa repertoire details
historical political / religious narratives
```

They are evidence and future study leads.

## Do not create style Materials yet

A single broad textbook is not enough evidence to declare a production-ready Material for a genre.

For an actual supported style, prefer:

```text
broad map
+
dedicated style source
+
real score / MIDI / recording analysis when available
+
controlled generation / listening test
-> reusable Material
```

---

# 16. Recommended future specialization path

The source helps identify branches worth deeper study but should not be treated as final authority on them.

High-value future branches for this repository include:

```text
pop / rock songwriting and arrangement
J-pop / anime song writing
Britpop / alternative rock
JRPG / visual-novel / game BGM
film / game underscore and musical topics
blues / rock lead-guitar phrasing
jazz / swing improvisation and arranging
dance / funk / disco groove design
chiptune / limited-voice arranging
regional traditions only when the project explicitly wants them
```

For each branch, the desired evidence should answer:

```text
what musical behavior must remain stable?
what dimensions commonly vary?
what carries style identity?
what is performer-dependent?
what is production-dependent?
what should never become a universal rule?
```

---

# 17. Compact reusable lessons

```text
1. A genre label is a hint, not a full specification.

2. Ask what the music is for before deciding how it should behave.

3. Compare styles across rhythm, pitch, dynamics, articulation, timbre, texture and form.

4. Repetition, variation and contrast operate at many musical levels.

5. Timbre and performance technique can carry as much style identity as pitch/harmony.

6. Improvisation is constrained creation, not randomness.

7. Some traditions preserve identity through performance rules, cycles, formulas, timbre or social practice rather than fixed notes.

8. Recording technology can itself become part of composition.

9. Musical meaning often depends on learned cultural context; avoid universalizing local associations.

10. Detailed genre behavior belongs in specialized, evidence-backed Skills or Materials, not in the global map.
```

---

## Source coverage used in this study

Primary source regions reviewed:

```text
How to Use This Book / Our Vision
Chapter 2: The Elements of Music
Chapter 3: Music and Characterization
Chapter 4: Sung and Danced Drama
Chapter 5: Song
Chapter 6: Stories without Words
Chapter 7: Listening at Public Concerts
Chapter 8: Listening at Home and at Court
Chapter 9: National Identity
Chapter 11: Music for Spiritual Expression
Chapter 12: Music for Moving
Chapter 13: What is Good Music?
```

Representative examples reviewed for navigation purposes include:

```text
ragtime / Dixieland context
Stravinsky, The Rite of Spring
film underscoring / source music
Javanese gamelan / wayang wong
West African Sunjata / jali practice
Chinese pipa repertoire
North Indian Raga Madhuvanti
Jimi Hendrix
The Beatles, Sgt. Pepper's Lonely Hearts Club Band
Appalachian fiddle / banjo dance practice
swing arranging
disco
```

This study intentionally does not reproduce the source's full historical narratives, listening guides, score excerpts or exact work analyses.