# v1 Critique — *Different Windows*

This critique is based on the actual first instrumental render (`output/v1.wav`), six rendered stems, generated MIDI, and the language-neutral topline score. v1 duration is **153.111 seconds**; no English vocal audio was created because the installed singing backend is Mandarin-only.

## Concrete v1 findings

1. **The final chorus does not exceed the earlier choruses.** Chorus 1 is -24.18 dBFS RMS, Chorus 2 is -24.15 dBFS, and Final Chorus is also -24.15 dBFS. The final 12-bar section has new lyric/harmonic material, but the backing energy is effectively identical rather than reaching the planned 10/10 climax.
   - **Revision:** increase only consequential final-chorus elements: stronger bass/guitar accents, selected string octave reinforcement and a denser last four-bar tag. Preserve vocal space rather than simply stacking foreground notes.

2. **Pre→Chorus payoff is too small.** Pre 1 to Chorus 1 rises only **0.86 dB** (-25.04 to -24.18); Pre 2 to Chorus 2 rises **0.83 dB** (-24.98 to -24.15). Harmony and register change correctly, but the rendered accompaniment does not make arrival large enough.
   - **Revision:** thin the final half-bar of each Pre around the fill, then strengthen chorus downbeats/open-hat language. Contrast will come from both a breath and a larger arrival.

3. **Bridge contrast is numerically modest despite the intended strip-down.** Bridge is -25.95 dBFS, only 1.80 dB below Chorus 2. The first half is sparse, but the full-section statistic shows the rebuild begins too early/heavily.
   - **Revision:** remove bass from Bridge bars 1–2 and hold guitar until bar 7; keep only piano/pad/low string line under the first two bridge lyric phrases, then rebuild decisively in bars 51–52.

4. **One piano same-pitch overlap remains.** The MIDI check reports one piano overlap (all other tracks are zero), while tiny-note count is zero throughout.
   - **Revision:** locate and trim/revoice the colliding piano event, then require zero overlaps on all six tracks.

5. **The instrumental mix is unnecessarily quiet for delivery.** v1 peaks at **-8.08 dBFS** and RMS is -25.48 dBFS. This leaves useful headroom, but the mixer's limiter only attenuates and does not raise a quiet signal.
   - **Revision:** add a coherent 4–5 dB local mix gain while retaining at least 1 dB true PCM headroom for later vocal integration. Target instrumental peak around -3 dBFS, not -1 dBFS, because the future lead vocal will need headroom.

## Vocal-score review

- 31 phrases and 235 note/token events are present.
- Absolute zero-based timing begins at beat 16.5 and ends at beat 266.25, before the 272-beat score end.
- Durations span 0.5–1.75 beats; phrase boundaries validate cleanly with no non-monotonic start times.
- Verse range stays lower; the chorus hook rises; E5 is reserved for the Final Chorus lyric “blue/light.”
- Tokens use one sung syllable per note with hyphen markers for multi-syllable words.
- No `vocals.json`, vocal stem or vocal mix is created in this task. The score is waiting for a compatible licensed English singing backend/schema conversion.

## Checklist summary

- **Melody / lyrics:** strong title hook, concrete imagery, parallel chorus meter, clear bridge perspective shift; no named-artist imitation.
- **Harmony:** functional and section-dependent; Pre dominant withholding and Final Chorus tag are purposeful.
- **Bass:** active roots/fifths/thirds/approaches with 472 notes, MIDI range 33–60, zero overlaps/tiny notes. Bridge density requires reduction.
- **Guitar:** muted Verse offbeats, long Pre power shapes and Chorus eighth-note power drive are distinct from piano.
- **Piano / strings / pad:** vocal-space hierarchy is mostly successful; piano overlap cleanup remains.
- **Drums:** section-specific grooves and boundary fills are present; Pre breath and Final Chorus lift need sharpening.
- **Arrangement:** Intro and Outro contrasts are strong; Final Chorus and Bridge need larger perceptual contrast.
- **Render:** all six intended instrumental stems are present, no clipping, correct duration. v1 is preserved.

## Final verification

- Final instrumental duration is **153.111 seconds** (2:33.111), within the requested 2–3 minute range and the 2:20–2:40 target.
- Overall RMS is **-20.88 dBFS** and peak is **-3.08 dBFS**, leaving useful headroom for later English vocal integration without clipping.
- The section arc now measures Intro -25.59 → Verse 1 -21.95 → Pre 1 -20.55 → Chorus 1 -19.68 dBFS. Verse 2 / Pre 2 / Chorus 2 repeat the rise at -21.99 / -20.50 / -19.65 dBFS.
- Bridge drops to **-21.95 dBFS** after removing early bass/guitar activity; Final Chorus reaches **-19.07 dBFS**, now 0.58–0.61 dB above the earlier choruses and the loudest sustained section. Outro falls decisively to -27.98 dBFS.
- Final MIDI analysis reports **zero same-pitch overlaps** and **zero tiny notes** across all six tracks.
- `vocal-score.json` remains valid: 31 phrases, 235 notes/tokens, beat range 16.5–266.25, durations 0.5–1.75 beats, no phrase-timing or boundary violations.
- No vocal WAV or fake vocal artifact exists; only the instrumental mixes and score are delivered pending a compatible licensed English singing backend.
