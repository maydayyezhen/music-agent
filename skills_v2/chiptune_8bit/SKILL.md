---
name: chiptune-8bit-composition
summary: Route 8-bit/chiptune composition tasks through explicit style constraints, voice budgets, Materials, profiles and chip-performance extensions without inventing hardware behavior.
status: active
---

# Chiptune / 8-bit Composition

## Purpose

Use this skill when a task asks for 8-bit, chiptune, chip-music, pulse-wave, limited-voice game music, or a chip-inspired arrangement.

This skill defines **how to reason and route the project**. It does not contain a library of fixed riffs, arpeggios, basslines or platform-specific register tables.

## First decision: constraint mode

Before composing, choose one mode:

```text
8bit_aesthetic
hardware_inspired
strict_platform
```

### `8bit_aesthetic`

The result should sound chip-like, but it may use a flexible voice count and non-hardware-specific synthesis.

### `hardware_inspired`

Use an explicit limited voice budget from a selected profile, but do not claim cycle-accurate or platform-exact behavior.

### `strict_platform`

Use only a validated platform profile and platform references. If the required hardware facts are not present in the repository or verified source material, do not invent them.

## Separation of concerns

Keep these layers distinct:

```text
Skill
→ how to compose and make decisions

Material
→ reusable musical vocabulary learned from references or experiments

Profile
→ available chip voices, synthesis controls and renderer mapping

Project extension
→ song-specific chip-performance data that MIDI cannot preserve cleanly

Derived MIDI / audio
→ execution and listening outputs
```

Do not put renderer parameters into a composition Material. Do not put a finished song pattern into this Skill.

## Composition procedure

1. Resolve the constraint mode.
2. Select a compatible profile.
3. Read the profile's voice budget and capabilities.
4. Retrieve only relevant active chiptune Materials from `materials_v2/registry.json`.
5. Assign musical roles to available voices before writing notes.
6. Compose within the current voice budget rather than arranging a normal band first and replacing instruments with square waves afterward.
7. Store chip-specific performance parameters outside plain MIDI when MIDI cannot represent them faithfully.
8. Derive MIDI only for information that maps cleanly enough to MIDI.
9. Render with an explicit profile/backend when one exists.
10. Validate voice-count, overlap and unsupported-parameter handling.

## Voice-budget principle

A limited chip arrangement should treat polyphony as a resource.

The agent should ask:

```text
Which voice carries the foreground?
Which voice implies harmony?
Which voice owns the low register?
Which transient/noise role is needed?
When must one role yield to another?
```

Do not solve every harmonic problem by adding more simultaneous notes.

## Material policy

Concrete chiptune vocabulary belongs in Materials, for example future families such as:

- rapid harmony implication;
- pulse counter-lines;
- chip bass motion;
- limited-voice percussion gestures;
- pitch ornaments;
- register-sharing recipes.

These examples are **category hints only**. Do not create or activate a Material until a reference study or controlled experiment supports it.

## Profile policy

Waveform, duty cycle, noise mode, envelope implementation, pitch range, polyphony and renderer behavior belong in `profiles/`.

A generic chiptune profile must not be presented as a specific real console.

A strict-platform profile must record provenance for hardware-specific constraints.

## Chip-performance project extension

Use a project-local `chip-performance.json` when needed for data such as:

- voice-slot assignment;
- waveform selection;
- pulse/duty mode;
- noise mode;
- chip-specific envelope or modulation state;
- chip-specific pitch effects;
- renderer-only parameters.

Plain MIDI may remain a useful derived artifact, but it is not automatically authoritative for chip-specific performance.

## Failure modes

Revise when:

- a normal band arrangement is merely reassigned to square-wave patches;
- voice count exceeds the chosen profile without an explicit degradation report;
- a specific console is claimed without a validated platform profile;
- exact arpeggio patterns or melodies are embedded in this Skill;
- synthesis implementation details leak into musical Materials;
- MIDI silently drops chip-specific parameters;
- every 8-bit task loads every chiptune Material regardless of relevance.

## Current scaffold boundary

This skill intentionally starts with architecture and decision rules only. It does not yet claim a mature 8-bit musical vocabulary.

Future agents should grow the system through this loop:

```text
study reference / run experiment
→ identify reusable invariant
→ promote to Material or Profile
→ validate in a project
→ only then broaden the Skill when the rule is truly general
```
