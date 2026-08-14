# Continuous Strum Comparison

## Root cause

The shared guitar path stored only sounding note events. Air strokes, hand direction and cross-bar hand state were absent, while the legacy electric rhythm arrangement used sparse sustained attacks in Verse and Chorus. The Acoustic part in this song was already explicitly authored with healthy motion; its missing piece was auditable right-hand state.

## Before / after

| Track / section | Before audible attacks per bar | After audible strums per bar |
|---|---:|---:|
| Acoustic Verse 1 | 5.00 | 5.00 |
| Acoustic Chorus 1 | 6.17 | 6.17 |
| Electric Rhythm Verse 1 | 0.50 | 5.00 |
| Electric Rhythm Verse 2 | 1.50 | 6.00 |
| Electric Rhythm Chorus 1 | 2.00 | 6.00 |
| Electric Rhythm Chorus 2 | 3.00 | 7.00 |
| Electric Rhythm Final Chorus | 3.43 | 8.00 |

## Flow evidence

- Acoustic Verse/Chorus hand motion: 8/8 eighth-note motions per bar; audible 5.00/6.17.
- Electric Verse/Chorus hand motion: 8/8; audible 5.00/6.00.
- Vocal-active Acoustic/Electric Verse 1 density: 5.00/5.00. Vocal activity changes articulation and dynamics; it does not stop the right hand.
- Cross-bar pattern resets: Acoustic 0; Electric 0. Chord-change interruptions: Acoustic 0; Electric 0.
- Air strokes stay in `strumming_grid`; they are deliberately not rendered as pitched MIDI notes.
- Intentional sustained-hit exceptions: Acoustic Outro bars 5-6; Electric Interlude bars 1-4, Bridge bars 7-8, Outro bars 1-2. These are arrangement planes against active Acoustic material, not accidental Verse/Chorus defaults.
- Remaining unintended one-hit Verse/Chorus bars: 0.

## Scope proof

- Non-target composition tracks byte-equivalent as JSON: True.
- Non-target rendered MIDI SHA-256 unchanged: True.
- Form/section data unchanged: True.
- Acoustic MIDI notes unchanged: True (the fix adds explicit hand-state IR and re-renders the same authored part).
- Electric Rhythm MIDI changed: True.
- Strumming validator warnings: 0.

`acoustic_before_after.mid` and `electric_before_after.mid` play the complete BEFORE version, wait two bars, then play the complete AFTER version.
