---
name: instrumentation-role-planning
description: Choose a song's instrument palette, assign musical roles, and plan section entry/exit before selecting instrument-specific Materials.
status: active
---

# Instrumentation Role Planning

## Purpose

Use this Skill before Material retrieval when composing or arranging a multi-instrument piece.

Its job is deliberately thin:

```text
brief
-> instrumentation palette
-> role assignment
-> section entry / exit plan
-> Material queries per role
```

It does **not** prescribe genre templates, fixed band lineups, chord progressions, section forms, or instrument-specific performance patterns.

## Core separation

Keep these dimensions independent:

```text
genre          = stylistic context / compatibility
instrumentation = which sound-producing roles are present
role           = what each instrument is doing
energy         = how much motion, density, weight and foreground pressure a section carries
texture        = articulation, register, sustain, rhythmic surface and timbral character
```

Do not collapse them into shortcuts.

In particular:

```text
rock != loud
rock != distortion
rock != electric guitar only
pop-rock != fixed band lineup
acoustic guitar != low energy by definition
synth / keyboard != electronic genre only
```

A genre label may narrow compatible vocabulary, but it must not automatically choose the instrumentation or energy level.

## Decision procedure

1. Read explicit user constraints first. If the user names or excludes an instrument, honor that before any genre association.
2. Identify the musical functions the arrangement needs: foreground melody, harmonic/rhythmic bed, bass foundation, pulse, counterline, sustained support, transition color, percussion, texture, or other task-specific roles.
3. Choose the smallest useful instrument palette that can cover those functions.
4. When the brief leaves instrumentation open, consider more than one plausible palette before committing. Do not treat the most common genre stereotype as the default answer.
5. Assign one primary role to each instrument for each section. Secondary roles are allowed, but avoid making every instrument perform the same function.
6. Plan section entry, exit, thinning and handoff before choosing detailed accompaniment patterns.
7. Decide how section energy changes. Use density, register, articulation, dynamics, rhythmic activity, sustain, layer count and role handoff as independent controls. Distortion or adding electric guitar is only one possible choice.
8. After the palette and roles are clear, query `materials_v2` by the chosen instrument + role + desired behavior/texture. Use genre tags as compatibility hints, not as the first selector.
9. If no validated Material exists for a chosen instrument/role, do not delete that instrument from the arrangement. Write the behavior project-specifically using available implementation capability, then promote new reusable knowledge only after evidence or successful validation.
10. Revisit instrumentation only when listening feedback reveals a role conflict, missing function, masking problem or unnecessary layer.

## Section plan

A useful lightweight plan may look like:

```text
instrument: acoustic_guitar
primary_role: rhythmic_bed
sections:
  verse: active, thin
  pre_chorus: active, slightly denser
  chorus: active, wider or layered
  bridge: optional / reduced

instrument: keyboard
primary_role: harmonic_support
sections:
  verse: sparse or absent
  pre_chorus: enter as sustain/color
  chorus: support upper harmony
  bridge: may temporarily become the main harmonic bed
```

This is a role plan, not a genre template. Replace instruments and section behaviors according to the actual brief.

## Material retrieval handoff

Material selection should happen **after** role planning.

Prefer queries shaped like:

```text
chosen instrument
+ current role
+ desired texture / motion
+ current section energy
+ current problem
+ compatible genre context
```

Avoid queries shaped like:

```text
genre
-> first matching Material
-> infer instrument from that Material
```

For broad genre requests, inspect shortlist diversity. If nearly every result belongs to one instrument family while the brief did not request that family, expand the search to other instruments that can perform the required roles.

## Failure modes

### Genre-to-instrument shortcut

Symptom: a rock request immediately becomes distorted electric guitar + bass + drums before roles are considered.

Fix: return to the required functions and compare plausible palettes.

### Material-first orchestration

Symptom: the Agent finds a strong Material card and adds its instrument simply because the card exists.

Fix: decide whether that musical role is needed first; Material availability does not define the arrangement.

### Energy-to-distortion shortcut

Symptom: every section lift is implemented by distortion, louder velocity or another guitar layer.

Fix: consider density, register, rhythm, sustain, layer entry/exit and role handoff independently.

### Missing-library veto

Symptom: keyboard, acoustic guitar or another suitable instrument is omitted because the Material library currently has fewer cards for it.

Fix: keep the instrumentation decision; use project-specific writing until validated reusable knowledge exists.

### Example inheritance

Symptom: reading a demo or implementation example silently imports its instrumentation, form, section density or mix hierarchy.

Fix: extract only the API/schema/mechanical detail needed for the task. Creative decisions must come from the active brief and V2 knowledge surfaces.

## Boundary

This Skill should remain small. Do not expand it into "how to arrange rock", "how to arrange pop", or fixed instrumentation recipes.

Its reusable invariant is only:

> choose musical functions and instruments first, then retrieve behavior Materials for those chosen roles.
