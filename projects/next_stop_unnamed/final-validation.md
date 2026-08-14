# Final Validation — 《下一站还没有名字》

- Form: 96 bars; 112 BPM; 4/4; D major / B minor.
- Duration: 207.714 seconds (3:27.714), including the two-second render tail.
- Audio: peak -4.39 dBFS; RMS -22.04 dBFS; 0 clipped samples.
- Section arc: Verse 1 -23.61 dBFS; Chorus 1 -20.75; Verse 2 -23.31; Chorus 2 -20.75; Final Chorus -20.47 (highest section); Outro -24.42.
- Lyrics: 42 phrases, 420 Chinese character-note mappings, 0.422-beat minimum explicit breath, 10 notes crossing an internal phrase barline.
- Vocal proxy: GeneralUser GS bank 8 / program 80 Sine Wave; B3-E5; strict monophony; no actual vocals, `vocals.json`, TTS, or samples.
- Guitar 1: 898 note-ons; Guitar 2: 350 note-ons. Both have explicit string/fret, attack group, strum direction, and right-hand intent.
- MIDI integrity, every musical track: 0 same-pitch overlaps, 0 stuck notes, 0 unmatched note-offs, 0 tiny notes.
- Guitar attack integrity: 0 perfectly simultaneous multi-note attacks; chord tones are physically staggered.
- Stems: all six stems are non-silent.
- Critics after final revision: Complexity 0 warnings; Continuity 0 warnings; Instrument-aware 0 errors / 0 warnings.
- Revision proof: V1 SHA-256 `8a50842c1afe18006c1bb287eb73b68c92dea782097cba47d7c4e7a57dfb20fc`; final SHA-256 `23d5496698985bcaccdef830e7494f2ca07fb572d678be17a14983689ed4e1e9`.

The remaining seven instrument-aware diagnostics are informational register-proximity notices. The guitar-only and no-vocal-proxy comparison renders verify that neither guitar doubles the Clean Synth Lead line.
