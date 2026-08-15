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
-> instrumentation / role plan when arranging multiple instruments
-> relevant materials_v2 per chosen instrument + role
-> profile / project extension
-> compiler / renderer
-> MIDI / audio / report
-> listening feedback
```

For multi-instrument composition, **do not let Material retrieval choose the band lineup**. Resolve a lightweight instrumentation/role plan first, including section entry/exit, then retrieve Materials for those chosen roles.

## Read

1. `AGENTS.md`
2. the active project explicitly named by the user
3. `skills_v2/registry.json` and relevant Skills
4. for multi-instrument composition, use `instrumentation-role-planning` before detailed Material selection
5. `materials_v2/registry.json` and relevant Materials for the chosen instruments/roles
6. required Profile and implementation files

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

## Genre, instrumentation and energy

Treat these as separate dimensions.

```text
genre           -> compatibility / stylistic context
instrumentation -> which instruments are chosen
role            -> what each instrument does
energy          -> density, motion, weight, register and foreground pressure
```

Never assume:

```text
rock = loud
rock = distortion
rock = electric guitar only
pop-rock = one fixed band lineup
```

Genre tags may help rank already-compatible Materials, but they must not choose an instrument by themselves.

If the brief does not specify instrumentation, consider multiple plausible instrument-role palettes before committing. Acoustic guitar, keyboard, piano, synth, strings and other available instruments are not excluded merely because the current Material library has fewer cards for them.

## Legacy boundary

The legacy Skill/reference/playbook architecture is removed from the current tree.
Do not search Git history or reconstruct it during normal work.

Only explicit user-requested legacy recovery may reopen old commits. Recover the smallest useful fact, translate it into V2 terminology, validate it, and promote it only when it still deserves to exist.

## Composition behavior

During composition:

```text
brief
-> choose required musical functions
-> choose instruments and section roles
-> browse materials_v2/registry.json
-> retrieve several behavior candidates per chosen role
-> combine / transform
```

Do not browse unrelated completed projects as creative references.

When a demo, benchmark, reconstruction or build script must be inspected for API/schema/mechanics, extract only that implementation detail. Do not inherit its instrumentation, form, chord progression, section density, mix hierarchy or arrangement constants.

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
