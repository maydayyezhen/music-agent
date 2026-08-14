# Strumming Comparison

This test uses an original neutral skeleton. It does not contain a copied reference pattern, melody or chord sequence.

## Sixteen-bar stages

- Bars 1-4 baseline: [8, 8, 8, 8] potential motions; attacks [8, 8, 8, 8].
- Bars 5-8 sixteenth grid: [16, 16, 16, 16] potential motions; attacks [12, 12, 13, 11].
- Bars 9-12 per-string sustain: previous-attack sustain ratio 97.9%; cross-bar sustain 100.0%.
- Bars 13-16 foreground-aware: attacks/bar 12 -> 11, velocity 85.75 -> 76.12, full-strum ratio 12.5% -> 6.8%.

## Acceptance

- Four related variants in each new four-bar phrase: 4.
- First-beat reattack ratio after: 75.0%; one related variant carries strings across an air downbeat.
- Long hand gaps caused by chord changes: 0.
- After MIDI same-pitch overlaps: 0; foreground MIDI same-pitch overlaps: 0.
- Unselected strings retain state; selected strings alone are retriggered. Chord changes close only strings whose pitch/fret assignment moves.
