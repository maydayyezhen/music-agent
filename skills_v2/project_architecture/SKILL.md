---
name: project-artifact-architecture
description: Create, inspect and route structured music projects through a thin manifest, native artifacts, adapters and derived outputs.
status: active
---

# Project Artifact Architecture

## Trigger

Use this skill when the task involves:

- creating or indexing a music project;
- deciding which file is authoritative;
- importing or exporting MIDI/PMT/other native artifacts;
- preserving unsupported events in a sidecar;
- routing a project to a renderer;
- reporting conversion loss or quantization.

Do not use this skill to decide melody, harmony, form, genre or arrangement.

## Capability boundary

This skill can:

- define a thin `manifest.json`;
- register native and derived artifacts;
- resolve artifact paths safely;
- choose an available adapter;
- preserve unsupported source data in a sidecar;
- generate conversion and validation reports.

This skill cannot:

- make one schema express every music concept;
- infer that a successful conversion sounds good;
- invent support in a renderer that does not exist;
- silently drop unsupported data.

## Core model

```text
manifest
├── authoritative native artifacts
├── authoritative project extensions
├── sidecars preserving unmapped source data
├── derived execution artifacts
└── derived audio and reports
```

The manifest is an index and routing surface. It does not duplicate notes, controllers,
automation, plugin state or other rich artifact content.

## Artifact authority

Use one of:

- `authoritative`: edited source of truth;
- `derived`: reproducible output generated from authoritative artifacts;
- `cache`: disposable acceleration data.

A derived artifact should record or be traceable to the source revision and adapter version when
that information is available.

## Adapter procedure

1. Identify the source artifact and its declared standard.
2. Verify that an adapter is registered for the source/target pair.
3. Preserve source-native fields whenever the target can represent them.
4. Put unsupported but recoverable data in a sidecar.
5. Mark deterministic quantization explicitly.
6. Mark degradation and dropped data explicitly.
7. Generate the target artifact.
8. Run a round-trip or invariant check where possible.
9. Write a conversion report.

## Conversion statuses

Use these report values:

- `lossless`
- `quantized`
- `preserved_in_sidecar`
- `degraded`
- `dropped`
- `not_present`

Never use `lossless` when timing, velocity or controller resolution changed.

## Minimal manifest example

```json
{
  "schema": "music-agent-project-facade",
  "schema_version": 1,
  "project": {"title": "Untitled"},
  "artifacts": {
    "performance": {
      "standard": "PMT performance-timed tokens",
      "path": "performance.pmt",
      "authority": "authoritative"
    },
    "midi_sidecar": {
      "standard": "MIDI 1.0 preserved events",
      "path": "performance.midi-sidecar.json",
      "authority": "authoritative"
    },
    "execution_midi": {
      "standard": "MIDI 1.0 Standard MIDI File",
      "path": "output/full_song.mid",
      "authority": "derived"
    }
  },
  "conversion_reports": ["reports/import.json"]
}
```

This example is structural and contains no musical template.

## Failure modes

- manifest path escapes the project directory;
- an authoritative artifact is missing;
- no adapter is registered;
- adapter version cannot read the declared schema;
- source contains unsupported events and no sidecar policy exists;
- derived artifact is stale relative to its source;
- round-trip exceeds declared tolerances;
- renderer capability is weaker than the requested expression.

## Validation

At minimum verify:

- manifest schema and safe relative paths;
- existence of required authoritative artifacts;
- adapter availability;
- event/note counts where meaningful;
- deterministic timing and velocity tolerances;
- preservation counts for sidecar events;
- explicit accounting of unsupported messages.

A validation pass means only that these invariants held.

## Provenance

This skill is based on the clean-slate project facade already implemented in the repository and on
standard adapter/sidecar design principles. It deliberately contains no composition knowledge or
complete musical example.
