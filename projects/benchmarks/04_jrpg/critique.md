# Critique after the real V1 render

V1 was rendered locally from `composition_v1.json` through the repository's MIDI → FluidSynth → stems → mix pipeline. The preserved artifact is `output/v1.wav`.

## Measured render facts

- Duration: **77.79 s** including renderer tail; intended musical body is 75.79 s.
- Full mix: **-12.72 dBFS peak**, **-29.30 dBFS RMS**. No clipping or peak normalization occurred, but the delivered level is unnecessarily conservative.
- All five intended stems are non-silent. MIDI scan found no same-pitch overlaps/stuck notes. Ranges: strings MIDI 53–86, brass 50–76, piano 41–79, bass 29–50, drums 36–51.
- Section RMS: Frontier Call -32.50 dB; Pursuit -28.77 dB; Shadow Pass -32.26 dB; Heroic Clash -27.99 dB; Victory Road -29.25 dB. The broad energy curve exists.

## Concrete V1 problems and revisions

1. **The foreground motif is masked in the driving sections.** In Pursuit, measured stem-power share is strings 8.7%, while bass + drums total 78.3%. In Victory Road, drums alone reach 48.1% while strings are 7.6%. This makes the intended motif development subordinate to the rhythm section. **Revision:** raise strings and piano modestly, lower drums and bass, reduce repeated ride energy, and keep brass behind the string lead.
2. **Shadow Pass changes loudness more than language.** Its RMS drops correctly to -32.26 dB, but the strings still run the same 16th-note ostinato density, so the contrast is largely a fader-like reduction. **Revision:** replace it with a broken eighth-note low-string figure, genuine gaps, a climbing upper counter-line, and a four-bar dominant pedal build.
3. **The harmonic ending contradicts the brief.** The 8-bar Victory Road uses a 4-bar `Bb–F–Gm–A` loop twice, so the actual last bar is A rather than the promised D-minor landing. **Revision:** write all eight bars explicitly as `Bb–F/A–Gm–A | Dm–Bb–A–Dm`, including a final tonic bass and brass/string cadence.
4. **The final mix is too quiet for a finished benchmark.** Peak is -12.72 dBFS even though no clipping is present. **Revision:** rebalance stems first, then use moderate positive per-track mix gain while retaining the repository's -1 dB peak safety normalization.

## Checklist summary

- Motif identity, repetition, transposition and augmentation: pass, but V1 foreground balance needs correction.
- Functional harmony and dominant tension: pass by section; final resolution fails in V1 and is targeted.
- Bass direction: pass; it uses fifths, passing notes and approaches, but its rendered dominance needs lowering.
- Strings: pass for non-block writing; Shadow Pass rhythmic differentiation needs correction.
- Brass restraint and structural use: pass.
- Drums: coherent anchors, velocity-shaped hats and boundary fills; ride layer is excessive in V1.
- Arrangement entrances/exits: brass rests completely in Shadow Pass and sections measure differently; final revision will strengthen the non-loudness contrast.
- MIDI/render integrity: pass; non-silent stems, valid duration, no overlaps/stuck notes, no clipping.

