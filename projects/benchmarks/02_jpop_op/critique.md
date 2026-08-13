# v1 Critique — *Hikari no Compass*

This critique follows the repository checklist and uses the actual `output/v1.wav`, rendered stems and generated MIDI from 2026-08-13. v1 duration is **79.838 s**; the mix peak is **-10.42 dBFS**, so there is no clipping.

## Concrete v1 problems

1. **Intro and Verse are almost the same measured energy.** Intro is -29.12 dBFS RMS and Verse is -28.98 dBFS—only **0.14 dB** apart. The intended “intro opens, then walking groove settles in” contrast is weaker than the energy map. The intro begins drums and a full eighth-note bass too early, so the motif has insufficient exposed space.
   - **Revision:** delay bass/drum entry in Intro and simplify their first two bars; preserve bar-4 fill into Verse. This makes the opening hook more legible and gives Verse arrival perceptual weight without changing the form.

2. **Outro does not decrescendo enough.** The entire Outro measures -27.56 dBFS, only 1.33 dB below Chorus (-26.23 dBFS), and the guitar stem remains at -27.56 dBFS through the section because v1's 8-bar guitar clip is looped into bars 9–12. That contradicts the planned final-four-bar guitar exit and keeps the ending feeling like another chorus loop.
   - **Revision:** rewrite Outro guitar as a true 12-bar clip that only contains bars 1–8; reduce outro drum activity and let the last four bars contain no drums/guitar. Thin piano attacks in the cadence and reduce bass density in bars 9–12.

3. **MIDI has same-pitch overlaps that can retrigger/cut sustained voices.** Analysis found **7 piano overlaps** and **8 strings overlaps**. The string overlaps happen every pre-chorus bar because the explicit top-line note duplicates a pitch already held in the sustained chord (for example MIDI 67 at bar 13.5). Piano overlaps include A3 during the intro arpeggiation and melody/chord collisions later.
   - **Revision:** remove duplicated top pitches from the relevant string sustain voicings and remove/revoice piano arpeggio notes that collide with held chord tones. Re-run the MIDI check and require zero same-pitch overlaps.

4. **The mix has excessive unused headroom.** v1 peaks at -10.42 dBFS even though the configured ceiling is -1 dBFS; the mixer's peak protection does not boost quiet material. This makes the deliverable unnecessarily quiet despite healthy stem dynamics.
   - **Revision:** raise local track gains coherently (not by compressing individual stems) while preserving balance, targeting a final peak around -3 to -1 dBFS with no clipping.

5. **Chorus payoff is real but the Pre→Chorus jump can be clearer.** RMS rises from -27.47 dBFS in Pre to -26.23 dBFS in Chorus (**+1.24 dB**) and the chorus has the correct higher hook/register; however, the Pre strings are already relatively loud (-28.80 dBFS), so the last two bars can aim more strongly at the dominant before impact.
   - **Revision:** make the second-half Pre ascent more selective and ensure the final dominant/fill breath leaves room for the chorus crash. Keep the harmonic progression; improve hierarchy rather than add more tracks.

## Checklist summary

- **Melody / hook:** pass. The chorus has a repeated rising `A–B–D–E–F#` hook and clear D landing; Verse is lower and sparser.
- **Harmony:** pass with revision needed for Pre hierarchy. Functional D-major motion is consistent; low piano/pad mud is avoided.
- **Bass:** pass. 384 notes span MIDI 31–54, using fifths, thirds, passing and approach tones with zero overlaps/tiny notes. It is audibly active, but the intro/outro need density control.
- **Guitar:** musical role passes—muted Verse pulse, sustained Pre power shapes and Chorus eighth-note power drive are distinct from piano. Outro exit fails in v1 because of loop behavior and will be fixed.
- **Piano / strings:** voicing roles pass, MIDI overlap cleanup fails and must be fixed.
- **Drums / groove:** section-specific groove and transition fills are present. Intro/outro restraint needs revision.
- **Arrangement:** Verse→Pre→Chorus rise is measurable and audible in the render, but Intro→Verse and Chorus→final cadence contrast are too small.
- **Render:** all six intended stems are non-silent where scheduled; Strings are correctly silent in Intro/Verse (about -90 dBFS residual floor). No clipping; duration is correct. v1 is preserved at `output/v1.wav`.

## Final revision targets

- Zero MIDI same-pitch overlaps and zero tiny notes.
- Intro→Verse difference becomes structurally obvious through withheld entry.
- Last four bars remove drums and guitar as promised.
- Preserve the chorus hook, moving bass, power-chord guitar role and boundary fills.
- Final peak near the configured ceiling without clipping.

## Final verification

All revision targets were re-rendered and checked against `output/final.wav`:

- Final duration remains **79.838 s**; peak is **-2.92 dBFS** and RMS is **-20.10 dBFS**, with no clipping or normalization limiting.
- Intro is now **-23.35 dBFS RMS** and Verse is **-21.47 dBFS**, a clear **+1.88 dB** arrival rather than v1's +0.14 dB.
- Energy continues upward: Pre **-20.01 dBFS**, Chorus **-18.73 dBFS**. Chorus remains the loudest and highest-register section.
- Outro falls to **-20.34 dBFS**; more importantly, drums and guitar have no new events in bars 45–48, while bass changes to sparse half notes and the Dadd9 cadence remains.
- The final MIDI scan reports **zero same-pitch overlaps** and **zero tiny notes** on all six tracks. Piano overlaps went 7→0 and Strings 8→0.
- Every intended stem is present. Strings remain intentionally absent from Intro/Verse; the rest of their entrance/exit behavior matches the energy map.
