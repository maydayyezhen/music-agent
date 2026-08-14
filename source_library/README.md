# Source Library

`source_library/` is the project's **original-source research library**.

It is deliberately separate from `materials_v2/` and `skills_v2/`.

```text
source_library -> original study/reference sources
materials_v2   -> abstracted reusable musical building blocks
skills_v2      -> reusable decision and performance knowledge
```

## Purpose

Use this library to keep track of user-provided MIDI or other reference sources that may be studied later.

A source may be registered even when no analysis has been performed yet. Registration does **not** imply that its musical details have been promoted into a Skill or Material.

## Retrieval policy

The source library is **not active by default during composition**.

Only open a source when the current task explicitly asks to:

- study that source;
- compare sources;
- verify an existing claim against it;
- extract reusable knowledge from it.

Do not browse finished songs merely to fill creative context. Composition should retrieve from `materials_v2/` instead.

## Promotion boundary

When studying a source:

1. record direct observations separately from interpretation;
2. identify whether the observation is specific to the song or reusable;
3. keep source-specific note sequences, chord progressions and complete patterns in the source study only;
4. promote only abstract reusable ideas into `materials_v2/`;
5. promote only broadly reliable behavior into `skills_v2/`.

A registered source can remain `parked` indefinitely.

## Local binary files

Original MIDI/audio files are local research assets and are not committed to Git.

Recommended local layout:

```text
source_library/midi/<file>.mid
source_library/audio/<file>.wav
```

The registry stores the expected local path and study status. Missing local binaries do not invalidate the repository itself; they only make that source unavailable for local analysis until the user restores it.
