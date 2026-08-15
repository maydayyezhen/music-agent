# Music Agent V2 Instructions

This file is the coding/composition Agent entry point for the current repository.

## Canonical context

Use only these knowledge surfaces by default:

```text
skills_v2/       reusable procedures and decision rules
materials_v2/    reusable musical vocabulary
profiles/        declared sound/performance capabilities
projects/        only the project explicitly being edited
source_library/  only when explicit source study is requested
```

Implementation may be inspected under `src/`, `scripts/`, `config/` and `tests/` when required to execute or debug a task.

## Required read order

1. root `SKILL.md`
2. the user's request and active project
3. `skills_v2/registry.json`
4. relevant Skill files only
5. for multi-instrument composition, resolve instrumentation + role + section entry/exit before Material retrieval
6. `materials_v2/registry.json`
7. relevant Material cards for the chosen instruments/roles
8. required Profile and implementation files

Do not browse unrelated projects for creative inspiration.

## Arrangement routing rule

For multi-instrument composition, use the thin `instrumentation-role-planning` Skill before selecting detailed Materials.

The order is:

```text
brief
-> required musical functions
-> instrument palette
-> per-section roles / entry / exit
-> Material retrieval by instrument + role + behavior
```

Do **not** reverse this into `genre -> Material -> instrument`.

Keep these dimensions separate:

```text
genre           stylistic compatibility
instrumentation chosen sound sources
role            musical function
energy          density / motion / register / weight / foreground pressure
texture         articulation / sustain / rhythmic surface / timbre
```

Never use shortcuts such as `rock = loud`, `rock = distortion`, or `rock = electric guitar only`.

A sparse Material library for one instrument is not evidence that the instrument should be excluded. If the arrangement needs that role and the implementation supports it, write the part project-specifically and promote reusable knowledge only after validation.

## Hard no-legacy rule

The former `skills/`, `references/`, old instrument research, long-form playbooks and legacy proof projects are not part of the current architecture.

Do not:

- search Git history for them during normal work;
- reconstruct them because an old filename is mentioned in stale code comments;
- treat old project statistics as quality targets;
- recover old composition rules because the V2 library seems sparse.

Legacy recovery is allowed only when the user explicitly asks to recover a named old capability. In that case, recover the smallest relevant fact, rewrite it into V2 form, validate it, and keep the old artifact out of default context.

## Skill policy

Create or revise a Skill only for a reusable operation, decision procedure, capability boundary, failure mode or validation method.

Do not put complete songs, fixed chord progressions, signature riffs or renderer presets into a Skill.

## Material policy

Materials may be numerous and stylistic. They should contain reusable musical vocabulary learned from a reference study or controlled experiment.

Genre words in a Material id or tag describe provenance or compatible context, not a claim that the Material is the standard answer for that genre.

Prefer:

```text
observed failure or source evidence
-> reusable invariant
-> narrow Material
-> project validation
-> registry activation
```

Do not promote exact source melody, full rhythm sequence, full harmony or complete arrangement.

## Project policy

A project is song-specific state, not reusable knowledge.

- Open only the active project named by the user.
- `_templates/` is structural scaffolding only.
- Archived/completed projects remain closed unless explicitly reopened.
- Never load all projects to "learn the house style".
- Benchmark, reconstruction, demo and finished-song code may be inspected only for a concrete schema/API/conversion/mechanical question; never inherit its instrumentation, form, density, harmony, melody or mix hierarchy into a new composition.

## Script / implementation-example boundary

Some files under `scripts/` have names such as `build_*demo.py` or `build_*full_song.py`. Their presence does not make them active creative guidance.

When such a file is required to understand an API or execution path:

```text
keep: schema, function calls, file layout, compiler/renderer mechanics
ignore: instrument lineup, chord loop, section form, density, melody, dynamics, mix choices
```

Prefer generic execution entry points over old demo builders for new work.

## Source-library policy

`source_library/` contains original evidence. It is not composition memory.

Open it only for requests such as study, compare, verify, analyze or revisit an original source. Promote only the abstract reusable result to V2.

## Profile policy

Profiles declare available implementation capabilities. Never invent unsupported keyswitches, CC mappings, chip modes, plugin behavior or hardware limits.

For chiptune, `chiptune_basic` is only a generic scaffold until validated platform profiles and renderers exist.

## Execution honesty

A successful compile means the pipeline accepted the data. It does not prove the music sounds good.
A validator proves only its declared invariants.
Listening feedback may override a technically valid but musically poor result, and successful fixes should be abstracted only when they generalize.
