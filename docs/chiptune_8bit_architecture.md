# Chiptune / 8-bit Architecture Scaffold

This document defines where future chiptune work belongs. It intentionally does not define a finished musical style or a specific console implementation.

## Layers

```text
skills_v2/chiptune_8bit/
  decision process and composition constraints

materials_v2/**/chiptune/
  reusable musical vocabulary promoted from evidence

profiles/chiptune_basic/
  generic voice budget and implementation surface

projects/<project>/chip-performance.json
  song-specific chip performance parameters

output MIDI/audio
  derived execution/listening artifacts
```

## Authority model

For a chip-oriented project, keep ordinary musical content and chip-specific performance data separate.

Suggested project artifacts:

```text
manifest.json
composition.json
chip-performance.json
output/full_song.mid
output/full_song.wav
reports/render.json
```

Recommended authority:

```text
composition.json      authoritative musical structure
chip-performance.json authoritative chip-specific performance extension
full_song.mid         derived exchange/execution artifact
full_song.wav         derived listening artifact
```

A project may use another authoritative music representation when appropriate. The key rule is that plain MIDI must not silently become the only source of truth when important chip controls cannot round-trip through it.

## Minimal chip-performance shape

```json
{
  "schema": "music-agent-chip-performance",
  "schema_version": 1,
  "profile": "chiptune_basic",
  "constraint_mode": "hardware_inspired",
  "voice_assignments": [],
  "events": [],
  "renderer_overrides": {}
}
```

Future agents may extend this structure, but should preserve explicit versioning and avoid embedding complete duplicate note data when the authoritative composition already owns the notes.

## Suggested event responsibilities

`chip-performance.json` may carry information that MIDI cannot represent cleanly, such as:

```text
voice slot assignment
waveform family or exact waveform id
pulse/duty mode
noise mode
chip envelope state
chip modulation state
pitch-effect state
renderer-specific chip parameters
```

Do not store ordinary note/harmony data twice unless a platform-specific performance representation truly requires it.

## Strict-platform rule

A strict platform profile must be evidence-backed.

Do not infer real hardware limits from `chiptune_basic`. That profile is a project scaffold only.

## Growth workflow

```text
reference / experiment
→ analysis
→ reusable Material or validated Profile change
→ project proof
→ registry activation
```

This keeps 8-bit knowledge evidence-driven instead of stereotype-driven.
