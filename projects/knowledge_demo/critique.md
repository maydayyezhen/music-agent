# Knowledge Demo — Composition Critique

## Candidate reviewed

- Composition: `composition_v1.json`
- Render: `output/mix_v1.wav`
- Stems: `stems_v1/`
- Duration: 66.00 seconds (64-second score + 2-second tail)
- Render status: all six intended stems are non-silent; no clipping or overlong FluidSynth tail.

This critique was completed after the first full render. It uses `references/composer-checklist.md`, MIDI event inspection, and section/stem RMS analysis. It evaluates audible/encoded decisions rather than treating a successful WAV as completion.

## What already works

- The core short–short–long motif is explicit and appears as a restrained Piano idea before Guitar owns the full Chorus hook. It returns with an altered A′ answer and a single C#6 climax rather than generating unrelated scale material.
- The form has measurable growth: mix RMS rises from Intro `-35.70 dBFS` to Verse `-34.04`, Pre-Chorus `-30.71`, and Chorus `-29.38`.
- Bass is not root-only. It uses roots, fifths, thirds/sevenths, passing notes, approach notes, anticipations, and rests; its MIDI contains 24 distinct velocities.
- Guitar is not Piano duplication: it is absent in Intro, enters with muted off-beat power shapes only in Verse bars 5–8, sustains through Pre, then carries a single-note hook with sparse chord punctuation.
- Strings use delayed answers, one inner Verse voice, an ascending Pre swell, and a separate Chorus counter-line instead of copied Piano chord blocks.
- Pad remains quiet, broadly voiced, and intentionally drops out in the last Pre-Chorus bar to create width on return.
- Drum velocity is shaped rather than uniform (53 distinct values), and fills/open hats/crashes are attached to section boundaries.

## Problems requiring revision

1. **The main snare backbeat is wrong for the target style.** Verse, Pre, and Chorus place their principal snare on beat 3 only, producing a half-time center. At 120 BPM this weakens the intended anime-rock forward motion. Revision: move the main backbeat to beats 2 and 4; keep only low-velocity ghost/side-stick notes around secondary positions.

2. **Pre → Chorus payoff is too small.** The mix gains only about `1.33 dB` RMS from Pre (`-30.71`) to Chorus (`-29.38`). The Pre has already accumulated dense hats, kick activity, guitar sustain, and strong strings, leaving too little new impact. Revision: thin Pre bars 1–2, reserve open hats/denser kicks for bars 3–4, preserve the bar-4 breath, then add full 2/4 backbeat and stronger chorus support.

3. **Strings peak too early and then retreat.** String RMS falls from Pre `-34.58` to Chorus `-37.90 dBFS`, contradicting the energy plan. The Chorus counter-line also speaks every beat for nearly all 16 bars, risking competition with the guitar hook. Revision: reduce Pre sustain level, reshape Chorus into two-beat/held answers with strategic rests, and raise only the A′ counter-line/climax.

4. **Piano Chorus drive is underweighted.** Piano RMS drops from Verse `-34.42` to Chorus `-34.66 dBFS`; the broken-chord pattern is present but does not contribute enough perceived lift. Revision: raise chorus velocities modestly, add accents at beats 1/3, and slightly lengthen select upper notes without copying the guitar melody.

5. **Too many tracks technically contain every named section.** Guitar appropriately exits Intro, but all other tracks have events in all four sections. Their density varies, yet the checklist asks for clearer entrances/exits. Revision: remove Strings from Intro bars 1–2 already achieved at event level; further make the first Verse bar strings-rest and preserve Pad's final Pre bar rest. No wholesale muting is needed because the brief calls for a compact opening, but rests must be structurally audible.

6. **Final crash is placed on the final bar arrival rather than allowed to mark the ending tail.** This is acceptable but can blur the last hook response. Revision: keep the final crash but reduce it slightly and let the final A landing and cymbal tail speak without an extra busy fill after the last downbeat.

## Revision plan for v2

- Rewrite Verse/Pre/Chorus drum backbeats to beats 2 and 4; retain restrained humanized hats and section fills.
- Make Pre bars 1–2 sparser and bars 3–4 the actual build.
- Reshape Strings Chorus from constant quarter-note commentary into shorter answers; lift A′ velocity and preserve one climax.
- Increase Piano Chorus accents/velocity while keeping its pitch role separate from Guitar.
- Remove the first Verse bar's String event and reduce the final crash/fill density.
- Re-render, re-run section/stem analysis, and confirm the Pre → Chorus contrast improves without clipping.

No key, tempo, form, core motif, or instrument mapping change is needed; revision should strengthen the existing concept rather than replace it.

## Post-v2 verification and final polish

The v2 render confirmed the intended structural changes:

- Verse/Pre/Chorus principal snares now land on beats 2 and 4.
- Strings were reduced from 95 to 58 events and Chorus writing fell from 68 to 32 MIDI notes, leaving more space for the Guitar hook.
- Piano Chorus RMS rose from `-34.66` to `-33.31 dBFS`.
- Strings no longer fall from Pre to Chorus; both measured `-36.50 dBFS`, with the higher A′ climax reserved for the second half.
- Pre → Chorus mix contrast improved from `1.33` to `1.59 dB`, but remained smaller than the energy map intended.

The verification also found a duplicate Pre bar-4 snare at beat 4: the preserved transition fill collided with the newly added backbeat. A small v3 polish is therefore required rather than accepting a known MIDI-cleanup failure. v3 will deduplicate identical drum events, lower Pre bars 1–2 backbeat/support velocities, and add a modest Piano Chorus accent. It will not replace the motif, harmony, form, or instrument roles.
