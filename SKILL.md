---
name: music-agent-clean-slate
description: Build structured, editable music projects through native artifacts, thin adapters and a newly rebuilt skill and materials library.
---

# Music Agent Clean Slate

Read only:

1. `AGENTS.md`
2. `docs/clean_slate_bootstrap.md`
3. the specific skill selected from `skills_v2/`
4. the specific texture recipe selected from `materials_v2/`, only when timbre or production is part of the task
5. the active project being edited
6. implementation code or schema needed to execute the current task

The previous knowledge and skill library is inactive. Do not search or read it unless the user
explicitly asks to recover a specific capability.

`materials_v2/` is opt-in. Do not load its whole registry or browse every recipe during ordinary
composition. Select one recipe by instrument and requested texture.

## Architecture kept during the reset

```text
user intent
-> thin Agent operation layer
-> native/structured project artifacts
-> adapter or compiler
-> MIDI / audio renderer
-> validation and conversion report
```

The project facade indexes artifacts and routes adapters. It must not become a new universal music
format.

Keep these distinctions:

- authoritative source artifacts;
- sidecars that preserve unsupported native data;
- derived MIDI/audio outputs;
- conversion reports that disclose quantization, degradation or loss.

## Default workflow

1. Read the user request.
2. Inspect only the active project's files and required APIs.
3. Select a `skills_v2/` Skill when the task needs reusable musical or technical behavior.
4. Select one `materials_v2/` recipe only when the request includes a timbre, texture or production target.
5. Write the smallest editable source that can express the request.
6. Compile, validate and render.
7. Report concrete failures rather than hiding them with randomization.
8. Add a new Skill or material recipe only when the task reveals reusable knowledge.

Do not begin by loading genre guides, instrument playbooks, proof songs, motif libraries, prior
builders or the entire materials library.

## Skill rebuilding rule

A V2 Skill must be narrow, testable and style-neutral by default. It should contain capability
facts, contracts, decision procedures, failure modes and validation. Tiny synthetic examples are
allowed. Finished compositions and fixed musical arcs are not.

## Material rebuilding rule

A V2 material recipe describes how an instrument or source should sound for a named texture. It may
contain source-selection guidance, processing ranges, renderer mappings, failure modes and listening
checks. It must not contain a finished song's notes, harmony, form or exact performance sequence.

Material recipes provide practical starting ranges, not claims of objective measurement unless a
measurement process actually exists.
