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

This skill targets one technique:

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

The target technique must not be treated as learned unless the source MIDI contains measurable within-stroke onset order. A quantized block-chord track can teach attack rhythm, relative velocity, voicing coverage, duration and overlap, but it cannot teach down/up direction or sweep timing.

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
4. Measure direction observability before assigning any hand motion:
   - count multi-note strokes;
   - measure within-stroke onset spread;
   - count strokes with enough non-zero spread to support an ordering estimate;
   - mark fully quantized sources as `unobservable_quantized_onsets`.
5. Estimate direction only for observable strokes:
   - low pitch to high pitch over time: `down`;
   - high pitch to low pitch over time: `up`;
   - insufficient spread or weak correlation: `unknown`.
6. Quantize the candidate onset to an eighth-note slot while retaining grid deviation.
7. Classify the sounding string group from note count, pitch span and relative register.
8. Normalize velocity within the local bar.
9. Aggregate multiple bars into slot probabilities and dominant behavior.
10. Store uncertainty and limitations explicitly.
11. Generate a directional synthetic demo only when direction is observable, or when the caller explicitly requests an alternate-hand hypothesis.

## Direction observability states

- `observable`: enough chordal strokes preserve within-stroke onset order.
- `weak_partial_evidence`: a small minority of strokes preserve order; do not generalize aggressively.
- `unobservable_quantized_onsets`: chord attacks exist, but every string/voice starts together.
- `no_chordal_strokes`: the selected track does not provide usable stroke groups.

For an unobservable source, set direction fields to `unknown`. Do not manufacture a D/U label from slot parity or stylistic expectations.

An optional demo may impose `D U D U` through `--assume-alternate-demo` or `--assume-alternate`. That is a rendering hypothesis, not learned evidence, and it must not be written back into the study model.

## Evidence versus inference

Direct MIDI evidence:

- note onset;
- note duration;
- velocity;
- pitch;
- track/channel/program;
- note overlap;
- onset order inside a cluster, when non-zero onset differences exist.

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

The analysis package also contains `observability.direction`, including multi-note stroke count, measurable direction count, zero-spread ratio, and median/maximum spread.

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

Generate a deliberately hypothetical D/U demo from an unobservable model:

```powershell
.\.venv\Scripts\python.exe scripts\study_acoustic_strumming.py generate `
  studies\first_eighth_strumming\model.json `
  studies\first_eighth_strumming\hypothesis_demo.mid `
  --assume-alternate
```

## Acceptance criteria

The first technique is considered learned only when:

1. at least one real MIDI sample contains measurable within-stroke direction evidence;
2. a real sample produces a plausible stroke study;
3. the source-specific absolute data is absent from the fingerprint;
4. transposition, tempo, program and uniform velocity transformations preserve the fingerprint;
5. the synthetic demo is valid MIDI and uses unrelated chord voicings;
6. uncertainty is retained instead of converted into invented technique labels.

A source with `unobservable_quantized_onsets` contributes attack-grid, voicing, velocity and sustain knowledge, but does not complete the D/U technique.
