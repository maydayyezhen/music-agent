# v1 Critique — *Parallax Bloom*

This critique uses the actual first render (`output/v1.wav`), seven rendered stems and generated MIDI. v1 is **147.714 seconds**, non-silent and unclipped; the full-mix peak is **-9.73 dBFS**.

## Concrete v1 problems

1. **One lead overlap compromises the featured theme track.** The MIDI scan found one same-pitch overlap on Doctor Solo, MIDI note 89 at absolute bar 59.75. All other tracks have zero overlaps/tiny/stuck notes.
   - **Revision:** remove the duplicated final Apogee F6 collision by shortening/replacing the pre-existing answer note before the added extended landing. Re-scan until the featured lead is clean.

2. **Wormhole does not rebuild strongly enough after Zero Gravity.** Zero Gravity correctly drops to -30.86 dBFS RMS, but Wormhole returns only to -26.64 dBFS, which is **0.38 dB below Orbital Garden** (-26.26) despite denser thematic compression and its intended 6→9 arc.
   - **Revision:** turn Wormhole bars 9–12 from the initial broken groove into full drive, strengthen Acid Bass accents and raise the motoric Synth Chime slightly. This should create a clear internal rebuild rather than one uniform 12-bar block.

3. **Prism Build is too close to the final climax.** Prism is -25.44 dBFS while Apogee is -25.02, only **0.42 dB** apart. The high-register lead is distinguishable in Apogee, but the energy reserve is too small.
   - **Revision:** thin Prism's first four bars and reserve its strongest drum density for bars 25–28; increase Apogee pad/lead support selectively. Target at least ~1 dB sustained difference while retaining the build's directional rise.

4. **Several texture stems are technically audible but under-contribute.** Bell Piano is -37.16 dBFS RMS, Chime -38.62, Solar Pad -38.75 and Night Pad -39.36. Their peaks prove they render, but at these averages the two pad roles can disappear behind drums (-26.94) and Acid Bass (-28.34), especially outside Zero Gravity.
   - **Revision:** raise texture mix levels by 2–3 dB, with Night Vision most audible in Zero Gravity and Solar Wind broader at Apogee. Keep Doctor Solo foreground and avoid turning every texture into a co-lead.

5. **Overall delivery level is unnecessarily low.** v1 peak is -9.73 dBFS and RMS -27.05 dBFS. No vocal headroom is needed in this instrumental project.
   - **Revision:** raise local track mix gains coherently, targeting a peak around -2 to -3 dBFS without clipping or limiter normalization.

## What already works

- The section arc is measurable: Launch -31.67 → Orbital -26.26 → Prism -25.44 → Zero Gravity -30.86 → Wormhole -26.64 → Apogee -25.02 → Re-entry -29.54 dBFS.
- Zero Gravity is a strong contrast and the score exceeds two minutes.
- Doctor Solo clearly owns the theme: 217 lead notes, range MIDI 57–93 in v1, with fragment/full/sequence/augmentation/compression/octave/reduction treatments.
- Acid Bass uses 404 notes across MIDI 31–51 with approaches and pedal behavior, not root transcription.
- Seven intended stems are non-silent; no vocals or `vocals.json` exist.
- Drum fills correspond to structural boundaries and drums fully exit in the beatless portion.

## Final verification

- Final duration remains **147.714 seconds** (>120 s), overall RMS is **-20.64 dBFS**, and peak is **-2.90 dBFS** with no clipping or normalization attenuation.
- The revised energy arc is Launch -25.47 → Orbital Garden -20.19 → Prism Build -19.74 → Zero Gravity -24.64 → Wormhole -20.00 → Apogee Bloom -18.06 → Re-entry -23.40 dBFS.
- Wormhole now exceeds Orbital Garden by 0.19 dB and contains a stronger bars 9–12 drive; Apogee is the loudest sustained section, **1.68 dB above Prism**.
- All seven necessary stems are non-silent. The quiet texture stems retain lower all-song averages because they are deliberately sparse/slow, but their peaks range from -22.14 to -16.26 dBFS before mix gain and their section roles remain audible.
- The final MIDI scan reports **zero overlaps, zero tiny notes and zero stuck notes** across all tracks. Doctor Solo spans MIDI 57–93 and remains the sole featured melody instrument.
- No `vocals.json`, vocal stem or vocal mix exists; Choir/Voice/Vox catalog presets remain valid ordinary synth colors under project rules but were not selected for this arrangement.
