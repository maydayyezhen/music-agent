# Final Validation — Lux in Absidis

- Render chain: structured composition JSON → per-track MIDI → FluidSynth → GeneralUser GS SoundFont → six PCM WAV stems → stereo mix.
- Final file: `output/final.wav`, 44.1 kHz, stereo PCM16, 134.43 seconds.
- Mix peak / RMS: -12.16 / -28.03 dBFS; clipped samples: 0.
- Non-silent stems: 6/6 (`choir_theme`, `choir_inner`, `pipe_organ`, `double_bass`, `slow_strings`, `bell_tower`).
- MIDI notes: 552 total; same-pitch overlaps: 0; stuck notes: 0; tiny notes under 24 ticks: 0.
- Complexity critic: 0 warnings.
- Continuity critic: 0 warnings.
- Point/Line/Plane: Narthex 1/1/1; Invocation 1/2/2; Procession, Sanctus, Great Amen and Benediction 1/3/2.
- Section RMS contour: -32.22, -28.76, -27.95, -27.14, -26.19, -29.64 dBFS (clear ascent to Great Amen and release into Benediction).
- `output/v1.wav` is retained as the auditable pre-revision render; `composition_v1.json` and `analysis_v1.json` preserve its score and metrics.
