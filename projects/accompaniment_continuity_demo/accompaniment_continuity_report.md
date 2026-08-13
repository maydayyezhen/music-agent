# Accompaniment Continuity Report

## Test invariants

The A/B is based on the Galgame standard project `Platform Afterglow`. Both renders keep 92 BPM, D major, 4/4, 28 bars, Intro/A/B/Return/Outro form, instrument programs, and harmonic progression. The selected source piano melody events are preserved exactly: pitch, onset, duration, and velocity.

## Track continuity metrics

Event-weighted averages across active sections. Piano before includes its combined melody/accompaniment source track; piano after reports its newly generated accompaniment where present, while the original melody remains in the render.

| Track | Version | Avg duration | Short-note ratio | Sustain ratio | Legato ratio | Avg positive gap | Overlap | Voice-leading distance | Common-tone retention |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| piano | before | 0.73 beats | 0.71 | 0.03 | 0.39 | 0.23 beats | 0.24 | 3.67 semitones/voice | 0.65 |
| piano | after | 1.09 beats | 0.30 | 0.07 | 0.49 | 0.56 beats | 0.30 | 0.85 semitones/voice | 1.00 |
| bass | before | 0.82 beats | 0.53 | 0.03 | 0.11 | 0.42 beats | 0.00 | 0.00 semitones/voice | 0.00 |
| bass | after | 1.65 beats | 0.09 | 0.41 | 1.00 | 0.00 beats | 0.47 | 0.84 semitones/voice | 1.00 |
| guitar | before | 0.70 beats | 0.97 | 0.03 | 0.00 | 0.86 beats | 0.00 | 1.29 semitones/voice | 0.21 |
| guitar | after | 2.06 beats | 0.28 | 0.22 | 0.51 | 0.70 beats | 0.49 | 0.98 semitones/voice | 1.00 |
| strings | before | 2.81 beats | 0.10 | 0.85 | 0.00 | 0.43 beats | 0.00 | 1.22 semitones/voice | 1.00 |
| strings | after | 3.23 beats | 0.00 | 0.42 | 0.81 | 0.29 beats | 0.42 | 1.00 semitones/voice | 1.00 |
| pad | before | 6.42 beats | 0.00 | 1.00 | 0.31 | 0.16 beats | 0.00 | 1.42 semitones/voice | 0.94 |
| pad | after | 5.93 beats | 0.00 | 1.00 | 0.99 | 0.00 beats | 0.99 | 0.97 semitones/voice | 1.00 |

## Texture distribution and Point/Line/Plane

- Before explicit textures: `{}`; aggregate family counts: `{'point': 11, 'line': 2, 'plane': 10, 'silent': 7}`.
- After explicit textures: `{'sustain': 9, 'counterline': 6, 'broken_chord': 3, 'pulse': 5, 'pedal': 1}`; aggregate family counts: `{'point': 5, 'line': 9, 'plane': 10, 'silent': 6}`.
- In the after A, B, and Return sections, Point, Line, and Plane are all present simultaneously. Drums and selected pulses retain point energy; bass/broken chords/counterline create lines; pad/held harmony/pedal create planes.

## Critic and technical validation

- Before continuity warnings: 3 — the clean guitar is pointillistic/disconnected in A, B, and Return.
- After continuity warnings: 0.
- Before WAV: 75.04s, peak -3.09 dBFS, RMS -19.58 dBFS.
- After WAV: 75.04s, peak -1.93 dBFS, RMS -18.78 dBFS.
- Both full MIDIs: zero same-pitch overlaps, zero tiny notes, zero stuck notes. After contains 611 rendered note-ons.
- Every intended before/after stem is non-silent.

## Listening-oriented assessment from score, MIDI, stems, and rendered-audio analysis

- The event and duration evidence indicates that the repeated ‘ah, ah, ah’ problem is materially reduced. It remains only where Point is intentionally assigned (drums and B-section pulses), rather than being the default behavior of every accompaniment track.
- Guitar changes the most: A uses lightly staggered held clean-guitar chords, B uses offbeat patterned pulses with unequal duration/accent, Return uses a connected broken chord, and Outro returns to a held strum.
- Bass becomes a phrase with held anchors, fifth/chord movement, approaches, anticipations, octave motion, and mixed durations. It no longer reads as uniformly short roots.
- Pad is a voice-led plane. Exact shared MIDI pitches are merged across chord changes, while the Outro uses a real pedal tone across the harmonic spans.
- Piano accompaniment evolves from a sustained Intro plane to an A broken line, B punctuated pulse, Return broken line, and sustained Outro. The source melody is not rewritten.
- Strings remain absent until B. They enter as a counterline, then become smooth sustained inner voices in Return, preserving arrangement growth.
- The result does not overcorrect into constant drones: B still contains active Point gestures, A/Return contain moving Lines, textures enter and leave by section, and sustain/pedal are limited to roles that need harmonic glue.
- No after track remains unintentionally disconnected according to the continuity critic. Codex did not perform human auditory perception; final subjective acceptance should compare the two WAVs on the same speakers/headphones.
