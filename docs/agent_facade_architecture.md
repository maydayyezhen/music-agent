# Thin Agent Facade over existing music standards

This experiment deliberately avoids defining a universal music format.

The project directory may carry several native representations at once:

```text
project/
├── manifest.json
├── performance.pmt
├── performance.meta.json
├── performance.midi-sidecar.json
├── instruments.json
├── render.json
├── reports/
│   └── midi-import.json
└── output/
    ├── full_song.mid
    └── mix.wav
```

## Responsibilities

### Existing standards

- PMT stores note performance tokens.
- MIDI 1.0 SMF stores executable note and controller events.
- WAVE stores rendered audio.
- Future adapters may add native MusicXML or DAWproject files without changing
  the PMT vocabulary.

### Adaptation

`performance.meta.json` and `performance.midi-sidecar.json` are adapter data used
for round trips where PMT does not carry the complete MIDI project state.

### Extension

`instruments.json` and `render.json` are current music-agent renderer extensions.
They are not presented as PMT, MIDI, MusicXML, DAWproject, VST3, or CLAP fields.

## What manifest.json does

The manifest is intentionally thin. It records only:

- the project title and source fingerprint
- artifact paths
- the real standard used by each artifact
- whether an artifact is authoritative or derived
- conversion-report paths
- the existing RFC 6901 / RFC 6902 edit protocols

It does not contain notes, chords, mixer automation, plugin parameters, or score
semantics. Those remain in native artifacts.

## Adapter policy

Every conversion report uses these result labels:

- `lossless`
- `quantized`
- `preserved_in_sidecar`
- `dropped`
- `not_present`

An adapter must not silently discard unsupported data.

## Current route

```text
MIDI 1.0 SMF
├── notes -> PMT
├── tempo / meter / key / CC / program / SysEx -> MIDI sidecar
└── conversion facts -> reports/midi-import.json

manifest.json indexes those artifacts

PMT + MIDI sidecar
└── rebuilt MIDI 1.0 SMF
    └── existing FluidSynth renderer
```

## Future route

MusicXML and DAWproject should be added as native files through adapters. The
manifest gains new artifact entries; it does not grow a second copy of their
musical data.

Plugin formats follow the same rule. VST3 or CLAP state should remain native
plugin state referenced by a DAWproject/device artifact, with a fallback only
when the project explicitly declares one.
