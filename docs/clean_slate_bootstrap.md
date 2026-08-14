# Clean-Slate Skill Bootstrap

This document defines the temporary reset used while the Music Agent knowledge system is rebuilt.

## What stays active

- project facade and manifest routing;
- native artifacts such as PMT, MIDI and sidecars;
- existing compilers, renderers, validators and tests as callable implementation tools;
- project-local source files explicitly named by the user;
- the new `skills_v2/` directory.

## What is inactive by default

The following are cold storage and must not be read, searched, summarized or used as creative
references unless the user explicitly names a file or asks to recover knowledge from the legacy
library:

- `references/`;
- `skills/`;
- `docs/instrument_research/`;
- old style/playbook documents outside `skills_v2/`;
- complete projects under `projects/` other than the project currently being edited;
- prior motifs, harmony plans, build scripts and validation statistics from example songs.

Inactive means unavailable to default reasoning, not deleted from Git history.

## Minimal active workflow

For a new task:

1. Read the user brief.
2. Inspect only schemas, APIs and code paths required to make the requested artifact run.
3. Create a project-local brief with explicit assumptions.
4. Author the smallest structured source that expresses the request.
5. Compile, validate and render.
6. Record concrete failures.
7. Add or revise a `skills_v2/` skill only when the failure reveals reusable knowledge.

No legacy document may be consulted merely because it is nearby or shares an instrument name.

## Rebuilding skills

A new skill must begin from an observed task and contain only reusable decisions.

Each skill should separate:

- capability facts;
- input/output contract;
- decision procedure;
- failure modes;
- validation checks;
- optional examples.

Examples must be tiny and synthetic. Complete songs, exact forms, signature chord loops and full
melodic phrases do not belong in default skill context.

## Promotion rule

New knowledge is promoted into `skills_v2/` only when all are true:

1. it solved or prevented a concrete failure;
2. it applies to more than one project;
3. it can be expressed without copying a finished work;
4. it has a test, validator or inspectable success criterion;
5. it does not silently prescribe style.

## Legacy recovery

When the user explicitly requests legacy recovery:

1. identify the exact question;
2. open the smallest relevant legacy file;
3. extract the implementation fact;
4. rewrite it into style-neutral language;
5. add a test or validation criterion;
6. place the cleaned result in `skills_v2/`;
7. record provenance in the new skill without importing the old example material.
