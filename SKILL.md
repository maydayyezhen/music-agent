---
name: music-agent-clean-slate
description: Build structured, editable music projects through native artifacts, thin adapters and a newly rebuilt skill library.
---

# Music Agent Clean Slate

Read only:

1. `AGENTS.md`
2. `docs/clean_slate_bootstrap.md`
3. the specific skill selected from `skills_v2/`
4. the active project being edited
5. implementation code or schema needed to execute the current task

The previous knowledge and skill library is inactive. Do not search or read it unless the user
explicitly asks to recover a specific capability.

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
3. Write the smallest editable source that can express the request.
4. Compile, validate and render.
5. Report concrete failures rather than hiding them with randomization.
6. Add a `skills_v2/` skill only when the task reveals reusable knowledge.

Do not begin by loading genre guides, instrument playbooks, proof songs, motif libraries or prior
builders.

## Skill rebuilding rule

A V2 skill must be narrow, testable and style-neutral by default. It should contain capability
facts, contracts, decision procedures, failure modes and validation. Tiny synthetic examples are
allowed. Finished compositions and fixed musical arcs are not.
