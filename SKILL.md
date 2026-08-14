---
name: local-instrument-aware-music-agent
description: Compose structured local music with instrument-specific phrase logic, semantic articulations, deterministic performance, validation, MIDI, stems and WAV renders.
---

# Local Instrument-aware Music Agent

Read `AGENTS.md` and `docs/creative_context_policy.md` first.

For a new composition or material rewrite, create `musical-brief.md` and
`creative-seed.md` before inspecting any complete song, demo, proof project, MIDI, core motif or
project-local build script.

Normal composition context may include:

1. `references/composition-guidelines.md`
2. `references/music-complexity.md`
3. `references/accompaniment-textures.md`
4. `docs/instrument_research/architecture_proposal.md`
5. matching method/research files under `docs/instrument_research/`
6. primitive libraries that describe operations rather than finished songs

Files under `projects/` are executable evidence, not default creative references. Do not read a
proof/demo project's `composition*.json`, `build_song.py`, exact motif, harmony, form, density
curve or MIDI before writing the new piece. Consult the smallest relevant proof passage only
after a concrete compiler, profile, validator or renderer failure exists.

For Acoustic Guitar or Electric Rhythm Guitar strumming, read
`docs/continuous_strumming.md`. Use explicit `sustained_chord_hit` versus
`continuous_strumming`; preserve air strokes and cross-bar hand direction in the IR. The
available strumming patterns are physical primitives, not instructions to reproduce an existing
song's groove or form.

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
.\.venv\Scripts\python.exe scripts\critic_reference_similarity.py <song> --write
```

The similarity critic is a template-reuse heuristic, not a copyright or quality judgment. A high
score requires musical inspection; do not respond by randomly changing notes.

Use an explicit seed in every semantic phrase. Humanization follows physical actions and
phrase function; random note timing/velocity is not a substitute for instrument writing.

For substantial Electric Lead Guitar work, read `docs/guitar_native_lead_playbook.md` as a
capability and physical-playability guide. Its development strategies are optional choices, not
a canonical song arc. Do not automatically require a delayed high point, thematic return,
continuous density or the workflow of any existing proof song.

For 8–16 bar lead melodies, `docs/long_form_phrase_schema.md` describes optional planning fields.
Only enable rules that the current piece declares. Formal work defaults to `legacy_stable`; use
`phrase_generation_mode: long_form_experimental` only for an explicit planning experiment, then
run `scripts/critic_long_form.py <song> --write`.

Before accepting a new composition, perform the divergence check in
`docs/creative_context_policy.md`. Changing only key, tempo, program number or a few pitches from
a consulted example is a failed composition attempt.
