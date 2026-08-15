---
name: music-agent-v2
description: Route structured music work through the current V2 Skills, Materials, Profiles, project artifacts and deterministic execution layer.
---

# Music Agent V2

## Default route

```text
user request
-> active project
-> relevant skills_v2
-> relevant materials_v2
-> profile / project extension
-> compiler / renderer
-> MIDI / audio / report
-> listening feedback
```

## Read

1. `AGENTS.md`
2. the active project explicitly named by the user
3. `skills_v2/registry.json` and relevant Skills
4. `materials_v2/registry.json` and relevant Materials
5. required Profile and implementation files

Read `source_library/registry.json` only when the user explicitly asks to study, compare, verify or revisit an original source.

## Knowledge authority

```text
Skill       -> how to reason / operate
Material    -> reusable musical vocabulary
Project     -> concrete song decisions
Profile     -> implementation capability mapping
Source      -> original study evidence
Renderer    -> derived execution
```

Keep those layers separate.

## Legacy boundary

The legacy Skill/reference/playbook architecture is removed from the current tree.
Do not search Git history or reconstruct it during normal work.

Only explicit user-requested legacy recovery may reopen old commits. Recover the smallest useful fact, translate it into V2 terminology, validate it, and promote it only when it still deserves to exist.

## Composition behavior

During composition, browse `materials_v2/registry.json`, retrieve several relevant candidates, and combine compatible ideas rather than inventing every detail from zero or copying one complete example project.

Do not browse unrelated completed projects as creative references.

## Source-study behavior

When studying an original source:

```text
source evidence
-> measured / inspectable observation
-> perceptual interpretation
-> reusable invariant
-> Skill or Material when justified
```

Keep exact source melody, full harmony, full rhythmic sequence and complete arrangement source-specific.

## Failure-driven growth

Prefer this loop:

```text
make / render
-> hear or inspect a concrete failure
-> fix the smallest responsible layer
-> validate
-> promote reusable knowledge only after success
```

Do not grow the library with stereotyped or untested rules merely to make it look complete.
