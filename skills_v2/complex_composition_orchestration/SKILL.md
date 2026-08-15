---
name: complex-composition-orchestration
description: Let a capable host coding agent decompose long, multi-section, multi-instrument music work into focused subagent responsibilities while preserving one coherent song and one structured project.
status: active
---

# Complex Composition Orchestration

## Purpose

Use this Skill when the host environment already supports subagents, parallel workers, delegated tasks, or equivalent isolated contexts, and the music task is large enough that one context is likely to lose detail.

This repository does **not** implement its own multi-agent framework.

```text
host agent = orchestrator
music-agent repo = shared musical workspace + contracts + knowledge
subagents = temporary focused workers created by the host when useful
```

For a short cue, a small arrangement, or a narrow edit, work directly. Do not delegate for the sake of delegation.

## Complexity signals

Consider orchestration when several of these are present:

- long duration;
- many sections with distinct development jobs;
- several meaningful instrument roles;
- foreground melody plus a full rhythm section;
- multiple guitars, counterlines, keys, orchestral colors, or other interacting layers;
- instrument-specific performance realization;
- detailed arrangement requested rather than a sketch;
- one pass would require the same context to remember too many independent musical states.

These are signals, not validator thresholds.

## Core rule: more duration must buy more musical development

Do not satisfy a long requested duration primarily by literal duplication, static accompaniment, or low-information filler.

Long-form repetition may be musically correct, but it should have a reason: identity, groove, return, anticipation, contrast, or another explicit function.

When scope grows, distribute the work across some combination of:

- motif recurrence and development;
- section-level contrast and return;
- role evolution;
- density and register change;
- rhythmic development;
- harmonic movement;
- instrumentation entry, exit, and handoff;
- instrument-specific performance detail;
- deliberate breathing space.

Do not force novelty every few bars merely to avoid repetition. The goal is intentional development, not constant mutation.

## Parent-agent responsibility

The parent host agent owns the final piece.

It must:

1. understand the user brief;
2. choose whether delegation is useful;
3. establish the shared global plan before detailed track writing;
4. choose the smallest useful set of subagent responsibilities;
5. give each subagent a narrow, clean context;
6. integrate all returned work;
7. resolve cross-track conflicts and unnecessary density;
8. apply performance realization and renderer constraints at the correct layer;
9. build, validate, render, inspect, and patch the active project;
10. remain accountable for musical coherence even when every child task reports success.

Subagent completion is not acceptance.

## Global blueprint before delegation

Before spawning detailed music writers, create or update a compact shared blueprint in the active project.

It should contain only project-specific decisions needed to keep workers coherent, such as:

```text
brief / constraints
section map and approximate lengths
global tempo / meter decisions
tonal or harmonic framework when already decided
foreground identity / motif plan when already decided
instrument palette and per-section role plan
energy / density arc
important arrivals, transitions, rests, and climax locations
development contract: what changes, returns, or hands off across sections
```

Do not turn the blueprint into a complete song encoded twice. Detailed notes remain in their authoritative track or composition artifacts.

If harmony or motif design itself is delegated, the parent may leave that field unresolved in the first blueprint, then publish the accepted result before dependent workers continue.

## Prefer responsibility ownership over arbitrary time slicing

Default to longitudinal musical ownership.

Good responsibility boundaries include:

```text
foreground melody / hook development
harmony / harmonic rhythm
bass + drums as a coordinated rhythm section
guitar arrangement
keys / pads / color layers
instrument-specific performance realization
arrangement integration / critique
```

A worker that owns a musical identity should usually see its responsibility across the whole piece, so it can remember what it introduced and how it develops.

Avoid this default pattern:

```text
worker A = first minute
worker B = second minute
worker C = third minute
```

Arbitrary time slicing often produces locally competent sections with weak global identity.

Time-based delegation is acceptable only when the sections are intentionally self-contained or when the parent supplies strong shared identity constraints and performs explicit integration afterward.

## Minimal delegation principle

Use as few workers as needed.

Examples of useful grouping:

- one melody worker for all foreground melody;
- one rhythm-section worker for bass + drums when their interaction matters;
- one guitar-arrangement worker for multiple guitar roles;
- one performance worker after guitar notes are accepted;
- one integration critic after parallel writing.

Do not create one worker per instrument automatically. Do not create a specialist for a layer that is intentionally simple or absent.

## Clean-context contract

Give each worker only what it needs from the allowed composition surfaces.

Typical worker input:

```text
user brief
accepted shared blueprint
accepted harmonic / motif / role artifacts relevant to the task
active-project artifacts needed for dependencies
relevant skills_v2
relevant materials_v2
required profiles / Agent API contract
```

Do not give a child unrelated completed projects, tests, implementation source, source-study evidence, or every other worker's scratch reasoning.

The normal creative-context firewall still applies to every child.

## Child-agent contract

Each delegated task should state:

- exact musical responsibility;
- authoritative inputs it may read;
- files or logical regions it may write;
- global decisions it must preserve;
- decisions it is allowed to make locally;
- dependencies it must not silently redefine;
- what report or artifact it must return.

A child should not redesign form, tempo, global harmony, instrumentation, or another worker's role unless the parent explicitly delegated that authority.

Prefer structured project artifacts or precise patches over prose-only output.

## Suggested orchestration waves

Use dependencies rather than spawning everything at once.

```text
Wave 0: parent
brief -> complexity judgment -> shared blueprint

Wave 1: foundation when needed
harmony / harmonic rhythm
motif or foreground identity
rhythm / groove architecture

Wave 2: role writers
melody
rhythm section
guitar arrangement
keys / color / counterline
other task-specific roles

Wave 3: performance realization
instrument-specific performance Skills / Profiles

Wave 4: integration and critique
cross-track inspection -> local patches -> build / render / listen
```

This is a dependency model, not a mandatory fixed pipeline. Collapse waves when the task is simpler.

## Composition versus performance

Keep `what to play` separate from `how to play` when the instrument warrants it.

For example:

```text
guitar composition / arrangement
-> accepted pitches, rhythm, phrase roles
-> guitar-performance-model
-> renderer/profile mapping
```

Do not let a performance worker silently rewrite the accepted melody, harmony, or section identity merely to expose more articulations.

## Integration pass

Before rendering, the parent should inspect the combined arrangement for at least:

- foreground ownership: who is actually carrying attention now;
- redundant doubling without purpose;
- register and rhythmic collisions;
- bass versus kick interaction;
- melody versus accompaniment competition;
- every worker making its own part too busy;
- section entries/exits and role handoffs;
- whether later sections genuinely develop earlier material;
- whether returns preserve enough identity;
- whether long duration came from meaningful form or copied filler;
- whether empty space is being preserved where useful;
- whether instrument-performance detail changes musical content that should remain authored.

The parent has deletion authority. Removing a competent but unnecessary layer is a successful integration decision.

## Revision policy

Prefer local revision loops.

```text
critic identifies a concrete problem
-> identify responsible artifact / bars / role
-> send a narrow repair task or patch directly
-> rebuild / inspect
```

Do not restart the whole composition because one track, section, transition, or performance layer failed.

Critics should report problems and evidence. They should not automatically replace the entire song.

## Parallelism rules

Parallelize work that is genuinely independent after shared constraints are accepted.

Good parallel candidates:

- guitar arrangement and keys/color writing after harmony + role plan are stable;
- drum detail and bass detail when a shared groove contract already exists;
- independent performance realization for accepted tracks.

Keep dependent work sequential or staged when necessary.

Do not trade coherence for maximum worker count.

## Active-project artifact guidance

The exact filenames are project-specific, but a complex project may benefit from lightweight coordination artifacts such as:

```text
blueprint / section plan
harmonic map
motif or foreground identity plan
instrument role plan
development contract
track-level authoritative composition artifacts
performance sidecars
integration / validation reports
```

Reuse the project's existing artifact architecture. Do not invent duplicate authoritative representations of the same notes.

## Failure modes

### Delegation theater

Symptom: many workers are spawned for a task one agent could do well.

Fix: collapse to the minimum useful set of responsibilities.

### Musical corpse stitching

Symptom: different workers write arbitrary time ranges and the result sounds like unrelated songs concatenated together.

Fix: use longitudinal ownership, shared motifs, shared harmony, and parent integration.

### Everyone is the protagonist

Symptom: every specialist fills every available space to demonstrate quality.

Fix: enforce per-section roles and let the parent delete, thin, mute, or hand off parts.

### Blueprint becomes a second composition

Symptom: note-level content is duplicated in coordination files and track files.

Fix: keep the blueprint thin; authoritative notes live in one place.

### Child silently changes global decisions

Symptom: one worker changes tempo, harmony, form, or instrumentation to make its own part easier.

Fix: narrow the child contract and require explicit parent approval for global changes.

### Long-song filler

Symptom: duration target is met with copied loops and negligible role or motif development.

Fix: revisit the development contract and assign the missing long-range work explicitly.

### Parallel race on shared files

Symptom: workers overwrite the same authoritative artifact.

Fix: give each worker non-overlapping write ownership or collect proposals and let the parent perform the final write.

## Success criterion

The orchestration succeeded when the final work feels like one composition whose parts remember and develop shared decisions, while the host used smaller contexts to preserve detail.

The number of subagents is not a quality metric.
