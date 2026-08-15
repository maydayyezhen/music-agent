# Materials V2

`materials_v2/` is the active external musical memory of Music Agent.

It is intentionally allowed to grow large. Harmony, voicing, accompaniment, phrasing and timbre are difficult to invent well from an empty prompt. A broad material library gives the Agent concrete vocabulary to compare, combine and transform.

The Agent may browse `registry.json` by default during composition and load multiple relevant cards.

## What belongs here

Material cards may describe reusable:

- chord voicing families;
- open-string and common-tone strategies;
- harmonic colors and chord-motion tendencies;
- accompaniment pattern families;
- rhythmic texture grids;
- instrument gestures and articulation combinations;
- phrase shapes, pickups, fills, transitions and cadences;
- orchestration and register combinations;
- timbre and production recipes;
- renderer-specific setup advice;
- small synthetic examples and parameterized fragments.

This library is broader than a sound-preset collection. It stores things the Agent can try.

## Suggested structure

```text
materials_v2/
├── registry.json
├── chord_voicings/
├── harmonic_motion/
├── accompaniment_patterns/
├── instrument_gestures/
├── phrase_devices/
├── orchestration/
├── timbre_recipes/
└── production_chains/
```

The directories may grow gradually. Do not create empty ceremony before useful material exists.

## Retrieval policy

For an ordinary multi-instrument composition task, Material retrieval is **not** the first orchestration step.

Use this order:

1. resolve the song's required musical functions;
2. choose an instrument palette and per-section roles;
3. read `registry.json`;
4. search primarily by chosen instrument, role, desired behavior/texture and current problem;
5. use genre as a compatibility/ranking hint, not as an instrument selector;
6. retrieve several cards from different relevant categories;
7. compare compatible and contrasting candidates;
8. combine useful features rather than following one card mechanically;
9. retrieve more material when the first result sounds generic or structurally weak.

There is no rule that only one material may be loaded. Large retrieval is acceptable when it adds useful vocabulary.

### Shortlist diversity

For a broad genre request with no locked instrumentation, inspect the shortlist before treating it as an arrangement.

If most returned cards belong to one instrument family, do not conclude that the genre requires that family. Expand the search to other instruments capable of the required roles.

This matters especially while the library is uneven. A mature acoustic-guitar or electric-guitar section of the library should not crowd keyboard, piano, synth, strings or other valid instrumentation out of the composition simply because those instruments currently have fewer cards.

**Missing Material coverage is not an instrumentation veto.**

## Tag semantics

Keep retrieval dimensions separate.

```text
instruments   = which instruments can reasonably realize the behavior
roles         = what musical function the behavior serves
texture_tags  = articulation / motion / sustain / density / sonic surface
problem_tags  = failure or repair context
genre_tags    = compatible stylistic contexts, not prescriptions
energy        = an arrangement decision; never infer it directly from genre
```

Important consequences:

```text
rock != electric guitar
rock != distortion
rock != high energy
pop-rock != fixed rhythm section
```

A Material tagged `rock` or `pop-rock` means **it can be useful there**, not **that rock should use this Material**.

Do not rank a genre-only match above a strong instrument + role + behavior match.

## Material naming

Prefer behavior-first names for new cards.

Good names describe what the material does, for example a motion, articulation, texture, role relationship or production behavior.

Some existing stable ids contain genre words because they were created from earlier studies. Treat those ids as stable identifiers, not style standards. Do not rename them casually if other files already reference them; instead keep their card text and retrieval policy explicit about the behavior they actually represent.

Avoid creating names that imply:

```text
this genre -> this exact pattern
```

unless the card truly describes a narrowly style-specific behavior and the evidence supports that scope.

## How materials should be used

Materials are starting points and transformation targets.

Useful transformations include:

- transpose;
- revoice;
- invert;
- thin or widen;
- change register;
- alter rhythmic density;
- change meter placement;
- split a pattern between instruments;
- preserve a common tone while changing the surrounding harmony;
- transfer a gesture to another compatible instrument;
- combine the texture of one card with the harmony behavior of another;
- adapt dynamics and articulation to the current section.

The result should fit the active piece rather than behave like a pasted preset.

## Card contents

A useful material card should contain as many of these as apply:

- identity and searchable tags;
- musical role and suitable contexts;
- prerequisites;
- concrete pattern, voicing or processing description;
- small examples;
- controllable variables;
- transformations;
- compatible materials;
- conflicts and failure modes;
- listening or score checks;
- implementation notes;
- provenance and uncertainty.

Cards may overlap. Several cards describing related techniques are valuable because their differences give the Agent choices.

## Boundary

Do not store a complete copyrighted recording, score or MIDI as a default reusable template.

Do not copy a source's complete melody, full chord progression, full form, exact rhythm sequence or detailed automation wholesale into a reusable card.

It is acceptable to store:

- abstracted observations;
- short lawful examples;
- generic or parameterized patterns;
- voicing families;
- transformed exercises;
- texture descriptions;
- implementation guidance;
- source-local research notes kept separate from reusable cards.

When a setting or interpretation was estimated rather than measured, label it as a practical starting point.

## Relationship to Skills

```text
Skills     = how to perform an operation
Materials  = musical vocabulary and sound options worth trying
Projects   = the current piece's actual notes, automation and decisions
Profiles   = mappings from materials to available tools or renderers
```

A Skill may ask the Agent to consult the materials library. A material card does not need to be style-neutral. Accumulation is the point, but genre compatibility must never become a hidden instrumentation template.
