# Final validation — Hands Before Notes

- Form: 80 bars at 104 BPM, 187.615 seconds.
- Semantic phrases: 33 across six instrument-aware tracks.
- Bridge: no lead-guitar phrase; rhythm guitar, bass, drums, organ and strings carry it.
- Instrument critic: 0 errors, 0 warnings, 1 informational register observation.
- Complexity critic: 0 warnings.
- Accompaniment continuity critic: 0 warnings.
- Semantic same-pitch overlaps: 0.
- Exported MIDI: 0 same-pitch overlaps, 0 stuck notes and 0 unmatched note-offs on all six tracks.
- Audio: 44.1 kHz stereo, peak -10.90 dBFS, RMS -28.83 dBFS, 0 clipped samples.
- Stems: all six are non-silent.
- Regression suite: 23 tests passed.
- `composition.json` and `composition_final.json` are identical.
- V1 and final WAV SHA-256 hashes differ.

The one informational observation is a lead-guitar/strings register intersection in the outro.
It is retained as intentional orchestration rather than treated as an error.
