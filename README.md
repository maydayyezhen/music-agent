# Music Agent

一个面向通用 Agent 的结构化音乐工作区。当前知识体系只认 V2。

## Canonical architecture

```text
user intent
-> skills_v2/                 reusable decision procedures
-> instrumentation / roles    choose musical functions before patterns
-> materials_v2/              reusable musical vocabulary for chosen roles
-> projects/<active-project>/ song-specific structured source
-> profiles/                  renderer / instrument capability mapping
-> src + scripts              deterministic execution layer
-> MIDI / audio / reports     derived outputs
```

Original reference sources are separate:

```text
source_library/
-> explicit study only
-> reusable abstraction
-> skills_v2/ or materials_v2/
```

## Agent read order

1. `AGENTS.md`
2. root `SKILL.md`
3. the active project explicitly named by the user
4. `skills_v2/registry.json` and relevant Skills
5. for multi-instrument composition, resolve instrumentation + role + section entry/exit
6. `materials_v2/registry.json` and relevant Materials for those chosen roles
7. the required Profile and implementation code
8. `source_library/registry.json` only for explicit reference study

## Retrieval principle

Do not use genre as a hidden instrument selector.

```text
genre != instrumentation
genre != energy
rock != distortion
rock != electric-guitar-only
```

Genre tags are compatibility hints. Instrument choice comes from the musical functions and the active brief; Material choice comes after instrument/role planning.

A missing Material card does not prove an instrument is unsuitable. It may simply mean that area of the library has not been studied yet.

## Hard boundaries

- `skills_v2/` is the only active Skill library.
- `materials_v2/` is the only active reusable musical-material library.
- Do not use complete projects as style templates or composition memory.
- Do not browse `source_library/` during ordinary composition.
- Do not infer a renderer, plugin or hardware capability that a Profile does not declare.
- Do not recover deleted legacy material from Git history unless the user explicitly asks for legacy recovery.
- Demo, benchmark and full-song builder code may teach schema/API/mechanics only; do not inherit its instrumentation, form, density or arrangement into a new piece.

## Current special extension

8-bit / chiptune work is routed through:

```text
skills_v2/chiptune_8bit/
materials_v2/chiptune/
profiles/chiptune_basic/
projects/_templates/chiptune_8bit/
```

`chiptune_basic` is a scaffold, not a claim of exact NES/Game Boy/C64 hardware behavior.

## Repository roles

```text
skills_v2/       how to work
materials_v2/    what reusable musical ideas are available
source_library/  original evidence, explicit-study only
profiles/        sound/performance capability mappings
projects/        active or archived song-specific work
src/             implementation
scripts/         execution tools and non-authoritative implementation examples
tests/           execution-layer regression tests
docs/            current architecture/policy documentation only
```

The old Skill/reference/playbook system has been removed from the current tree. Git history remains available for explicit recovery, but it is not part of normal Agent context.
