# Music Agent project instructions

This repository is a local structured-composition and audio-rendering project. References under `references/` are project reading material, not installed Skills. Do not register them globally, install their MCP integrations, or introduce Ableton/Suno/cloud dependencies.

## Preserve the rendering pipeline

Keep the existing boundary intact:

```text
composition.json -> MIDI tracks -> local renderer -> WAV stems -> mix.wav
```

Composition data, instrument mapping, rendering, and mixing stay decoupled. Prefer narrow changes: musical notes in the song's `composition.json`; timbre in `config/instruments.json`; balance in `config/render.json`.

Vocals are an optional parallel layer, never a default requirement:

```text
vocals.json -> local zh/en/ja singing backend -> stems/vocal.wav -> output/vocal_mix.wav
```

If the brief asks for instrumental, soundtrack, BGM, underscore, karaoke/backing track, or says nothing about singing, do not create `vocals.json` and do not render vocals. Add vocals only when the user explicitly wants a sung song, lyrics, topline, or vocal demo. The instrumental `output/mix.wav` must remain available even for vocal projects.

## Mandatory workflow for a new song or major rewrite

Before creating a new song or substantially rewriting one, execute these stages in order:

1. Read `references/composition-guidelines.md`, `references/music-complexity.md`, and `references/accompaniment-textures.md`.
2. Analyze the user brief and preserve explicit constraints.
3. Create `projects/<song>/musical-brief.md` with genre, emotional target, key, tempo, length, instrumentation, and exclusions.
4. Define the song structure.
5. Resolve a global complexity profile, section contour, and per-section role budget; record them in the brief and composition.
6. Define an energy map for every section and translate it into entrances/exits, density, register, tension, velocity, and drum intensity.
7. Design a short rhythm motif before choosing pitches, give each instrument a distinct rhythmic identity, and plan explicit silence.
8. Plan a Point/Line/Plane balance for each section. Give accompaniment tracks executable textures and continuity targets; do not let every non-lead track default to short points.
9. Turn the rhythm into a short core melodic motif.
10. Write functional harmony and instrument-appropriate voicings.
11. Test the motif against the harmony before expanding the arrangement.
12. Write section melodies using repetition, variation, contrast, and return.
13. Write bass as a continuous phrase using mixed durations, approaches, fifths, pedals, or anticipation—not roots alone.
14. Write drums with section-specific groove and transitions.
15. Write piano and guitar as distinct playable parts whose texture can evolve by section.
16. Write strings and pad as support, counter-motion, atmosphere, or climax—not chord-block duplicates; preserve common tones where appropriate.
17. Apply restrained MIDI cleanup/humanization: purposeful velocity, duration, articulation, and timing variation while preserving anchors.
18. If vocals were explicitly requested, follow the optional vocal workflow below; otherwise skip it completely.
19. Save the initial draft as `composition_v1.json`, copy it to `composition.json`, and render it.
20. Run `scripts/critic_complexity.py <song> --write` and `scripts/critic_continuity.py <song> --write`, then listen when possible and analyze stems/mix for silence, duration, clipping, section energy, density, contrast, and accompaniment continuity.
21. Complete `references/composer-checklist.md` and write concrete findings to `projects/<song>/critique.md`.
22. Make at least one composition revision. Save it as `composition_v2.json` (and later numbered versions); never erase the only prior version.
23. Copy the selected revision to `composition.json` and render the final candidate.

The following shortcut is prohibited:

```text
user prompt -> immediately generate a complete multi-minute MIDI -> declare done
```

Small local edits (for example, changing one bass phrase) do not require recreating the entire planning package, but must still respect the relevant guidelines and preserve a recoverable prior version when the edit is material.

## Optional vocal workflow

Read `references/vocal-workflow.md` whenever vocals, lyrics, a singer, topline, or a vocal demo are requested. The essential rules are:

1. Write melody and lyrics together. A note carries one Chinese character, one Japanese kana, or one English word/syllable token, plus pitch and duration.
2. Preserve singable prosody: phrase stresses, breaths, vowel length, and comfortable range matter more than filling every beat.
3. Keep phrases short enough to breathe and render independently; `start_beat` is absolute from song start and `duration` is in beats.
4. Never invent a fake vocal stem or substitute speech/TTS. Select the installed backend by language: `zh` OpenCpop VISinger, `en` SoulX-Singer, or `ja` Kiritan VISinger.
5. Render the instrumental first. Then run `scripts/render_vocals.py <song>` or `scripts/render_song.py <song> --with-vocals`.
6. Verify that `stems/vocal.wav` is non-silent, has the intended lyric/pitch contour, and aligns with the instrumental before accepting `output/vocal_mix.wav`.
7. The installed voices are language/model-specific. Do not silently transliterate, clone a real person, promise a named singer, or switch to spoken TTS. Unsupported languages and additional character voices need an explicitly licensed compatible model.

## Progressive disclosure

Default reading before composition:

```text
references/composition-guidelines.md
references/music-complexity.md
references/accompaniment-textures.md
```

Read deeper only when the task needs it:

- Harmony, voicing, or instrument ranges: `references/ableton-skills/skills/chord-pro/SKILL.md` and, when needed, `references/midi-agent-skill/resources/voice-leading.md`.
- Drums, groove, or humanization: `references/ableton-skills/skills/groove-builder/SKILL.md` and `references/ableton-skills/skills/midi-cleanup/SKILL.md`.
- Form, transitions, and section contrast: `references/ableton-skills/skills/arrangement-coach/SKILL.md`.
- Full production planning: `references/ableton-skills/skills/producer-mode/SKILL.md`.
- Hooks, motif, emotional progression, or lyrics/prosody: `references/hermes-songwriting/skills/creative/songwriting-and-ai-music/SKILL.md`. Ignore its Suno/cloud-generation instructions.
- Structured MIDI, GM programs, and local engineering patterns: `references/midi-agent-skill/SKILL.md`, its `resources/`, and relevant helper code. Treat its rigid dissonance/root-bass rules as beginner safeguards, not universal musical law.
- Installed SoundFont presets, hidden GS banks, or alternate drum kits: read `references/soundfont-catalog.md` and query `config/soundfont-catalog.json`. Never guess bank/program values. Every catalog entry—including presets named Choir, Voice, or Vox—is an ordinary instrument and may be used freely in an arrangement. These names do not mean the preset can pronounce lyrics; lyric-capable singing uses the optional AI vocal workflow.
- Genre-specific knowledge: read a matching file under `references/genres/` only if one exists. Do not invent a large genre pack without a task requiring it.

Complexity fields are optional for backward compatibility. If omitted, treat
the target as `standard` without rewriting the file. Never equate a higher
complexity target with random notes or continuous activity on every track.

Do not read all three repositories for every song. The synthesized guideline is the normal entry point.

## Artistic discretion

These rules prevent low-quality accidental AI MIDI; they are not a style grammar. Dissonance, minimalism, noise, asymmetry, repetition, unusual form, or deliberate mechanical timing are allowed when the brief calls for them. A conscious exception should serve the musical idea and be noted in the brief or critique.
