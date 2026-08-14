---
name: replace-with-skill-name
description: State the narrow reusable task this skill supports.
status: draft
---

# Skill title

## Trigger

Use this skill only when:

- the task contains ...;
- the current project needs ...

Do not load it for unrelated composition work.

## Capability boundary

This skill can:

- ...

This skill cannot:

- ...

## Inputs

- required artifact or user intent;
- relevant project paths;
- renderer/compiler capability assumptions.

## Outputs

- files or structured fields written;
- generated validation report;
- derived MIDI/audio artifacts when applicable.

## Decision procedure

1. Inspect the user brief and active project only.
2. Validate required capabilities.
3. Choose among the documented options.
4. Author the smallest sufficient structured representation.
5. Compile/render.
6. Inspect concrete failures.
7. Revise only the failing layer.

## Failure modes

- unsupported renderer capability;
- invalid or missing source artifact;
- information loss during conversion;
- physical or protocol constraint violation.

## Validation

Provide at least one of:

- automated test;
- validator command;
- deterministic round-trip check;
- inspectable MIDI/controller invariant;
- audio/stem measurement.

## Tiny synthetic example

Examples must demonstrate one capability using minimal invented material. Do not include a full
song, signature progression, reusable melodic phrase or project-specific arrangement.

## Provenance

Record standards, source documents or legacy implementation facts used. Rewrite recovered legacy
knowledge in style-neutral terms and do not import its finished musical material.
