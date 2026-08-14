---
name: music-agent-clean-slate
description: Build structured, editable music projects through native artifacts, thin adapters and a newly rebuilt skill and materials library.
---

# Music Agent Clean Slate

Read:

1. `AGENTS.md`
2. `docs/clean_slate_bootstrap.md`
3. the relevant skill or skills from `skills_v2/`
4. `materials_v2/registry.json`
5. any material cards that may help with harmony, voicing, accompaniment, phrasing, timbre or production
6. the active project being edited
7. implementation code or schema needed to execute the current task

The previous knowledge and skill library is inactive. Do not search or read it unless the user explicitly asks to recover a specific capability.

`materials_v2/` is an active external memory library. It may be browsed during composition even when the user does not name an exact recipe. Start from the registry, retrieve several plausible cards, compare them, and combine compatible ideas.

Do not treat a large material context as a failure. For harmony, accompaniment and timbre, broad exposure is often more useful than asking the model to invent every detail from first principles.

## Architecture kept during the reset

```text
user intent
-> skills and retrieved material memory
-> thin Agent operation layer
-> native/structured project artifacts
-> adapter or compiler
-> MIDI / audio renderer
-> validation and conversion report
```

The project facade indexes artifacts and routes adapters. It must not become a new universal music format.

Keep these distinctions:

- authoritative source artifacts;
- reusable material cards and reference fragments;
- sidecars that preserve unsupported native data;
- derived MIDI/audio outputs;
- conversion reports that disclose quantization, degradation or loss.

## Default workflow

1. Read the user request.
2. Inspect the active project and required APIs.
3. Select the relevant `skills_v2/` behavior guidance.
4. Read `materials_v2/registry.json` and retrieve a useful set of material cards.
5. Compare and combine material cards instead of forcing a single recipe to solve the whole task.
6. Write the smallest editable source that can express the request.
7. Compile, validate and render.
8. Listen or inspect concrete failures and revise the responsible layer.
9. Add a new Skill or material card when the task reveals reusable knowledge.

The Agent may browse broadly inside `materials_v2/`. It should still avoid copying one finished source wholesale. Recombine, transpose, revoice, vary, thin, expand and adapt materials to the current project.

## Skill rebuilding rule

A V2 Skill should teach a reusable operation, decision procedure, failure mode or validation method. Skills can be narrow and style-neutral, while materials provide concrete musical vocabulary and sound references.

## Material library rule

A V2 material card may describe reusable:

- chord voicings and voicing families;
- harmonic colors and chord-motion tendencies;
- accompaniment patterns and texture grids;
- instrument gestures and phrasing shapes;
- orchestration combinations;
- timbre and production recipes;
- transition, fill, pickup and cadence devices;
- small synthetic examples and parameterized fragments.

Material cards may be stylistic and numerous. Their value comes from accumulation, contrast and recombination.

Do not store a complete copyrighted song as a reusable template. A card may record abstracted observations, short lawful examples, parameterized patterns and implementation advice. Approximate settings must be labeled as practical starting points rather than objective measurements unless they were actually measured.
