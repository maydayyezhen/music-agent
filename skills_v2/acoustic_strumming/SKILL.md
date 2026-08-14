---
name: acoustic-guitar-continuous-eighth-strumming
description: Extract, validate and generate a generalized continuous eighth-note acoustic-guitar strumming model from MIDI evidence.
status: active
---

# Acoustic Guitar Continuous Eighth Strumming

## Trigger

Use this skill when the task is specifically about:

- detecting common eighth-note acoustic-guitar strumming in MIDI;
- separating right-hand motion from the source song's key, chords, tempo and program;
- generating a new strumming performance from a generalized model;
- testing whether extracted behavior survives transposition, tempo changes and timbre changes.

Do not use this skill for fingerpicking, sixteenth-note funk, isolated chord hits, electric-guitar palm muting or complete song composition.

## Capability boundary

This skill models one technique:

```text
continuous eighth-note alternate hand motion
D U D U D U D U
```

A grid position may produce:

- `full`
- `low_partial`
- `middle_partial`
- `high_partial`
- `double_stop`
- `single_string`
- `air_candidate`

`air_candidate` is an inference from a missing MIDI attack. Ordinary MIDI does not encode a literal empty hand stroke.

## Required invariants

The extracted technique fingerprint should remain stable when the same performance is:

- transposed;
- assigned another MIDI program;
- played under another tempo map;
- given a uniform velocity offset;
- moved to another absolute register while retaining relative voicing shape.

The fingerprint intentionally excludes:

- song title;
- key;
- absolute pitches;
- chord names;
- absolute BPM;
- absolute MIDI program;
- source form and section names;
- exact source velocity values.

## Extraction procedure

1. Select one MIDI track/channel.
2. Pair note-on and note-off events.
3. Group near-simultaneous note attacks into stroke candidates using a beat-relative window.
4. Estimate direction:
   - low pitch to high pitch over time: `down`;
   - high pitch to low pitch over time: `up`;
   - insufficient spread or weak correlation: `unknown`.
5. Quantize the candidate onset to an eighth-note slot while retaining grid deviation.
6. Classify the sounding string group from note count, pitch span and relative register.
7. Normalize velocity within the local bar.
8. Aggregate multiple bars into slot probabilities and dominant behavior.
9. Store uncertainty and limitations explicitly.
10. Generate a synthetic demo on unrelated chord voicings.

## Evidence versus inference

Direct MIDI evidence:

- note onset;
- note duration;
- velocity;
- pitch;
- track/channel/program;
- note overlap;
- onset order inside a cluster.

Inferred behavior:

- down/up direction;
- full versus partial stroke;
- continuous alternate hand motion;
- missing-slot air stroke;
- strings ringing through a later stroke.

Unknown without stronger data:

- literal guitar-string identity;
- pick angle;
- fretting fingering;
- hand pressure;
- body/percussive noise;
- whether a silent grid position was physically performed.

Never report an inference as a directly encoded MIDI fact.

## Model contract

The generalized model contains:

- `technique`
- `subdivision`
- `slots_per_bar`
- `motion`
- `slot_profiles`
- `attack_mask`
- `sustain_observations`
- `evidence`
- `invariance_fingerprint`
- `limitations`

The model is an extracted behavior summary, not a transcription of a source song.

## Commands

List candidate track/channels:

```powershell
.\.venv\Scripts\python.exe scripts\study_acoustic_strumming.py list "<file.mid>"
```

Analyze one candidate:

```powershell
.\.venv\Scripts\python.exe scripts\study_acoustic_strumming.py analyze `
  "<file.mid>" `
  first_eighth_strumming `
  --track 4 `
  --channel 0
```

Generate from an existing model:

```powershell
.\.venv\Scripts\python.exe scripts\study_acoustic_strumming.py generate `
  studies\first_eighth_strumming\model.json `
  studies\first_eighth_strumming\new_demo.mid
```

## Acceptance criteria

The first technique is considered learned only when:

1. a real MIDI sample produces a plausible stroke study;
2. the source-specific absolute data is absent from the fingerprint;
3. transposition, tempo, program and uniform velocity transformations preserve the fingerprint;
4. the synthetic demo is valid MIDI and uses unrelated chord voicings;
5. uncertainty is retained instead of converted into invented technique labels.
