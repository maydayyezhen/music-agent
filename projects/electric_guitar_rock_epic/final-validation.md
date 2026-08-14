# Final Validation — After the Last Thunder

- Composition files: `composition.json` and `composition_final.json` SHA-256 are identical (`8F1155E1...A908281`).
- Audio revisions differ: V1 SHA-256 `2D85A622...74CD4AB`; final SHA-256 `D77BB321...DC9012B`.
- Duration: 232.00 s at 44.1 kHz stereo (score 230 s + 2 s configured tail), exceeding the 180 s minimum.
- Mix: peak -8.44 dBFS, RMS -26.86 dBFS, clipped samples 0.
- Non-silent stem RMS: lead guitar -27.65, rhythm guitar -28.02, bass -28.47, organ -27.38, strings -31.13, drums -23.58 dBFS.
- MIDI integrity on every track: same-pitch overlaps 0; unmatched note-offs 0; stuck notes 0; tiny notes under 0.05 beat 0.
- Critic result: complexity 0 warnings; accompaniment continuity 0 warnings.
- Energy proof (section RMS dBFS): Verse I -29.81; Chorus I -25.53; Verse II -29.86; Chorus II -25.42; Build A -29.01; Bridge Build -26.00; Final Chorus -24.92; Outro -29.86.
- Lead absence: global bars 57–72 (score time 140–180 s) contain zero `lead_guitar` MIDI notes or overlaps into the segment.
- Development within that lead-free segment: rhythm guitar 136, bass 76, organ 40, strings 24, drums 98 notes. Build A vs Bridge Build event-set symmetric differences are respectively 68/76/40/8/98 for those tracks.
- Repeated chorus variation: Chorus I vs Chorus II lead events 50 vs 52, symmetric difference 102; rhythm-guitar and bass event sets each differ by 10. Chorus II vs extended Final Chorus lead events 52 vs 78, rhythm guitar 50 vs 70, bass 50 vs 70, organ 20 vs 28, strings 10 vs 14, drums 145 vs 201.
- No `vocals.json` exists; no vocal renderer was invoked.
