---
name: local-instrument-aware-music-agent
description: Compose structured local music with instrument-specific phrase logic, semantic articulations, deterministic performance, validation, MIDI, stems and WAV renders.
---

# Local Instrument-aware Music Agent

Read `AGENTS.md` first. For a new composition or material rewrite, also read:

1. `references/composition-guidelines.md`
2. `references/music-complexity.md`
3. `references/accompaniment-textures.md`
4. `docs/instrument_research/architecture_proposal.md`
5. the matching instrument research files under `docs/instrument_research/`

For Acoustic Guitar or Electric Rhythm Guitar strumming, also read
`docs/continuous_strumming.md`. Use explicit `sustained_chord_hit` versus
`continuous_strumming`; preserve air strokes and cross-bar hand direction in the IR, and run
the strumming validator/demo before accepting a Verse or Chorus rhythm part.

Prefer `instrument_phrase` for guitar, bass, drums, keyboard and strings when the requested
part should model a player's decisions. Keep legacy `events` for migration and small exact-note
edits. Never mix both inside one clip.

The required boundary remains:

```text
musical intent -> instrument phrase -> neutral performance -> profile-mapped MIDI
-> local renderer -> WAV stem -> mix
```

Sound-library triggers belong in `profiles/`, never in instrument composers. Run:

```powershell
.\.venv\Scripts\python.exe scripts\critic_instruments.py <song> --write
.\.venv\Scripts\python.exe scripts\critic_complexity.py <song> --write
.\.venv\Scripts\python.exe scripts\critic_continuity.py <song> --write
```

Use an explicit seed in every semantic phrase. Humanization follows physical actions and
phrase function; random note timing/velocity is not a substitute for instrument writing.

For a substantial Electric Lead Guitar theme or solo, read
`docs/guitar_native_lead_playbook.md` before note realization. Start from a playable motif,
plan continuous fretboard/hand movement, and render before changing the system. The proven
reference project is `projects/guitar_native_rock_proof/`; reuse its method and audits, not
its exact notes or form.

For 8–16 bar lead melodies, read `docs/long_form_phrase_analysis.md` and
`docs/long_form_phrase_schema.md`. Formal work defaults to `legacy_stable`; use the experimental
planner only through the explicit `phrase_generation_mode: long_form_experimental`, then run
`scripts/critic_long_form.py <song> --write`.
