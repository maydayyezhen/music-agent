# Continuous Guitar Strumming

Acoustic Guitar and Electric Rhythm Guitar must distinguish a held chord from continuous
right-hand motion. Do not infer a strumming pattern only from the pitched notes that happen to
sound: the compositional representation must retain down/up travel, including air strokes.

## Two explicit modes

- `sustained_chord_hit`: one intentional attack followed by sustain. Use it as a structural
  plane, entrance, breakdown or ending—not as the automatic Verse/Chorus guitar behavior.
- `continuous_strumming`: persistent eighth- or sixteenth-note hand motion. On a sixteenth
  grid, each bar has 16 potential alternating down/up positions. A position can be
  `full_strum`, `partial_strum`, `single_string_restrike`, `muted_strum`, `ghost_strum`, or
  `air_strum`; sounding attacks are optional. Air strokes remain semantic actions and do not
  create fake pitched notes. The legacy eighth-note action names remain supported.

For a semantic phrase, set `phrase_type: continuous_strumming` and choose
`strumming_pattern` or `strumming_patterns`. Supported shared patterns are defined in
`src/instruments/strumming.py`. For a hand-authored event clip, provide `strumming_grid` with
one item per bar so the physical state remains auditable alongside exact notes.

```json
{
  "bar": 1,
  "subdivision": "eighth",
  "hand_motion": ["down", "up", "down", "up", "down", "up", "down", "up"],
  "actions": ["partial_strum", "air_strum", "muted_strum", "light_upstroke",
              "partial_strum", "air_strum", "accent_strum", "light_upstroke"],
  "last_hand_direction": "up",
  "next_expected_direction": "down",
  "pattern_continues_across_bar": true
}
```

For the stateful sixteenth-note path, use:

```json
{
  "phrase_type": "continuous_strumming",
  "subdivision": "sixteenth",
  "strumming_pattern": "sixteenth_flow",
  "four_bar_variation": true,
  "per_string_sustain": true,
  "foreground_aware": true
}
```

The compiler derives four related variants (A, A', B, B') from the same skeleton. It may make
small changes to attacks, accents, string count, muted strokes and local upstrokes; it must not
replace each bar with an unrelated random pattern.

With `per_string_sustain`, every guitar string owns an independent active-note state. A partial
stroke retriggers only the selected strings. Unselected strings may continue across later
attacks and barlines. At a chord change, only strings whose pitch or fret assignment moves are
closed; the compiler also prevents same-pitch overlap and conflicting note-off ownership.

With `foreground_aware`, the MIDI generator derives activity from Vocal, Main Melody, Lead
Melody, foreground or hook tracks unless explicit activity is supplied. Active foreground
slightly reduces attack density and velocity and favors one-to-three-string partial, light or
muted strokes. Long holds and release spaces can briefly restore fuller strokes. All 16 right-
hand positions remain present even when some become air strokes.

## Composition expectations

- Verse normally exposes 3–6 audible strums per bar while the hand can still move on all eight
  eighth-note positions.
- Chorus normally exposes 5–8 audible strums per bar with stronger downbeat accents and more
  open voicings.
- Vocal activity may reduce velocity, string count or openness; it must not implicitly stop the
  hand. Vocal rests may reveal fuller strokes.
- Chord changes do not reset the down/up state. The previous bar's
  `next_expected_direction` must match the next bar's first hand direction.
- Acoustic and Electric Rhythm Guitar need independent patterns. Acoustic can use open/full and
  high-string partial sweeps; Electric Rhythm normally uses low-string power shapes, palm mute,
  short releases and a different accent map.
- A conscious one-hit bar remains legal when documented as `sustained_chord_hit`. Accidental
  one-hit Verse/Chorus bars are validator failures.

## Verification

Generate the eight-bar A/B proof and inspect its MIDI, WAV, grid and report:

```powershell
.\.venv\Scripts\python.exe scripts\build_strumming_continuity_demo.py
.\.venv\Scripts\python.exe -m unittest tests.test_strumming_continuity -v
```

The demo is `projects/strumming_continuity_demo`: bars 1–2 are the one-hit baseline, bars 3–4
Verse, bars 5–6 Pre-Chorus, and bars 7–8 Chorus. Song-level audits use
`analyze_strumming_flow()` and must report audible density, one-hit/downbeat-only bars, air and
muted strokes, upstroke ratio, cross-bar resets, chord-change interruption and Vocal-active
density.

Generate the focused sixteen-bar regression for the stateful sixteenth-note path:

```powershell
.\.venv\Scripts\python.exe scripts\build_sixteenth_strumming_demo.py
```

The output is `projects/sixteenth_strumming_demo`. Bars 1-4 preserve the fixed eighth-note
baseline; bars 5-8 introduce the sixteenth hand grid and partial attacks; bars 9-12 enable
per-string sustain/retrigger; bars 13-16 add derived foreground-aware thinning. Its comparison
report includes motion/attack counts, voicing-size ratios, retained-string and cross-bar sustain
ratios, downbeat reattack, variant count, velocity/full-strum changes, hand gaps and MIDI note
integrity.
