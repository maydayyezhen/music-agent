# Music Agent project instructions

Read the root `SKILL.md` and `docs/creative_context_policy.md` before new composition work.

This repository is a local structured-composition and audio-rendering project. References under
`references/` are project reading material, not installed Skills. Do not register them globally,
install their MCP integrations, or introduce Ableton/Suno/cloud dependencies.

## Creative context isolation

The repository contains two very different kinds of material:

1. method documents and reusable implementation primitives;
2. complete proof/demo songs under `projects/`.

Only the first category belongs in the normal composition context.

For a new song or substantial rewrite:

1. Read the user brief.
2. Create `musical-brief.md` and `creative-seed.md` before opening any complete example song.
3. Decide the audible idea, rhythm, harmony behavior, form, texture, silence and instrument roles
   independently.
4. Read only the method documents and primitive libraries needed to realize that idea.
5. Build and render a first draft.
6. Inspect a proof/demo project only after a concrete compiler, profile, validator or renderer
   failure has been identified.
7. When a proof is consulted, read the smallest relevant passage and record only the
   implementation fact used.

Do not use another project's `build_song.py`, `composition*.json`, core motif, exact harmony,
section plan, density curve, register path or MIDI as a starting template.

Changing only key, tempo, programs or a few pitches from a proof song is a failed composition
attempt.

## Preserve the rendering pipeline

Keep the existing boundary intact:

```text
composition.json -> MIDI tracks -> local renderer -> WAV stems -> mix.wav
```

For guitar, bass, drums, keyboard and strings, preserve instrument semantics through:

```text
musical intent -> instrument_phrase -> neutral performance events
-> sound-library profile -> rendered MIDI events
```

New player-like parts should prefer `instrument_phrase`; legacy `events` remain supported and
byte-stable. Never put library-specific keyswitch numbers in composition or instrument modules.
Profiles under `profiles/` own keyswitch, CC, pitch-bend and fallback mapping.

Composition data, instrument mapping, rendering and mixing stay decoupled. Prefer narrow changes:
musical notes in `composition.json`; timbre in `instruments.json`; balance in `render.json`.

## Style is declared by the piece

Validators and schemas may enforce data integrity and physical feasibility. They must not silently
invent the composition's style.

The following are optional strategies, never repository-wide defaults:

- delayed climax or late high note;
- motif sequence followed by thematic return;
- continuous lead activity;
- 4/8/16-bar phrases;
- verse/chorus energy growth;
- one strong cadence per eight bars;
- minor-pentatonic guitar writing;
- open-chord acoustic strumming;
- rich arrangement as the definition of quality.

A project may deliberately be minimal, static, cyclic, asymmetrical, noisy, dissonant,
through-composed, mechanical or unresolved.

## Mandatory workflow for a new song or major rewrite

Execute these stages in order:

1. Read `references/composition-guidelines.md`, `references/music-complexity.md`, and
   `references/accompaniment-textures.md` as decision tools.
2. Analyze the user brief and preserve explicit constraints.
3. Create `projects/<song>/musical-brief.md` with genre, emotional target, key/tonal behavior,
   tempo, length, instrumentation and exclusions.
4. Create `projects/<song>/creative-seed.md` before inspecting complete examples. Record:
   - central audible idea;
   - rhythmic identity;
   - pitch/harmonic identity;
   - formal behavior;
   - instrument roles;
   - planned silence;
   - at least two possible development paths;
   - material or gestures to avoid.
5. Define the song structure from the brief rather than from the nearest demo.
6. Resolve a global complexity profile, section contour and per-section role budget. Complexity is
   a descriptive control, not a demand for more notes.
7. Define an energy or attention map only when useful. A flat, cyclic or discontinuous map is
   valid.
8. Give each instrument a distinct rhythmic/physical identity and plan explicit silence.
9. Plan Point/Line/Plane balance appropriate to the piece.
10. Develop harmony, motif, texture or sound gesture in the order most natural to the brief. A
    melody-first workflow is not mandatory.
11. Write instrument parts as playable/realizable behaviors rather than program-swapped piano
    notes.
12. Apply restrained performance detail after the musical skeleton works.
13. If vocals were explicitly requested, follow the optional vocal workflow; otherwise skip it.
14. Save the initial draft as `composition_v1.json`, copy it to `composition.json`, and render it.
15. Run the relevant critics and interpret warnings in context:

```powershell
.\.venv\Scripts\python.exe scripts\critic_instruments.py <song> --write
.\.venv\Scripts\python.exe scripts\critic_complexity.py <song> --write
.\.venv\Scripts\python.exe scripts\critic_continuity.py <song> --write
```

16. Write concrete audible findings to `projects/<song>/critique.md`.
17. Make at least one targeted revision, preserve the prior version, and render again.
18. If a downstream feature fails, then and only then consult a narrow proof/demo passage.
19. Before acceptance, perform the divergence check in `docs/creative_context_policy.md` against
    every complete example that was consulted.

The following shortcut is prohibited:

```text
user prompt
-> open nearest validated project
-> copy its builder/form/motif path
-> replace pitches and title
-> declare a new composition
```

Small local edits do not require recreating the planning package, but must preserve recoverable
prior versions when material.

## Instrument-specific routing

### Electric lead guitar

Read `skills/instruments/electric_guitar/SKILL.md` and
`docs/guitar_native_lead_playbook.md` for physical constraints and optional operations.
Do not inspect a complete guitar proof project during blank-slate writing.

`docs/long_form_phrase_schema.md` contains optional planning fields. Enable stylistic rules only
when the current project declares them. A validator may describe peak timing or phrase resets but
must not fail a piece for omitting a delayed climax unless that rule was enabled.

### Acoustic and electric rhythm guitar

Read `docs/continuous_strumming.md` when continuous right-hand motion matters. Preserve air
strokes, hand direction and per-string state. Strumming pattern names are physical primitives,
not complete arrangement templates. A piece may instead use fingerpicking, isolated attacks,
noise, harmonics, percussion or intentional sustained chords.

### Other instruments

Read the matching method/research document only when needed. Instrument knowledge should describe
range, technique, roles, expression and renderer capabilities without prescribing one finished
part.

## Optional vocal workflow

Vocals are an optional parallel layer, never a default requirement:

```text
vocals.json -> local zh/en/ja singing backend -> stems/vocal.wav -> output/vocal_mix.wav
```

If the brief asks for instrumental, soundtrack, BGM, underscore, karaoke/backing track, or says
nothing about singing, do not create `vocals.json`. Add vocals only when the user explicitly wants
a sung song, lyrics, topline or vocal demo. The instrumental `output/mix.wav` must remain
available even for vocal projects.

Read `references/vocal-workflow.md` whenever vocals are requested. Preserve singable prosody,
breaths and supported language/model constraints. Never invent a fake vocal stem, clone a real
person or silently substitute spoken TTS.

## Progressive disclosure

Default reading before composition:

```text
docs/creative_context_policy.md
references/composition-guidelines.md
references/music-complexity.md
references/accompaniment-textures.md
```

Read deeper only when the task needs it:

- Harmony, voicing or instrument ranges: relevant method/resource documents.
- Drums, groove or humanization: groove and MIDI-cleanup references.
- Form and transitions: arrangement references, treated as option libraries rather than a fixed
  pop form.
- Electric lead guitar: guitar method/research documents, not complete proof songs.
- Acoustic/rhythm guitar motion: `docs/continuous_strumming.md` and compiler primitives.
- Production planning: producer-mode references without cloud-generation instructions.
- Hooks, motif or lyrics/prosody: songwriting method references without copying their examples.
- Structured MIDI, GM programs and local engineering patterns: MIDI skill/resources and helper
  code.
- SoundFont presets: catalog/config files. Preset names such as Choir or Voice remain ordinary
  instruments and do not imply lyric-capable singing.
- Genre-specific knowledge: a matching genre method file when one exists.

Do not read every repository or every example for each song. Finished songs are not a style
knowledge base.

## Reference and material-library design

New reusable materials should be stored as primitives and methods:

- transformation operators;
- playable voicing procedures;
- action vocabularies;
- capability tables;
- groove abstractions;
- articulation mapping;
- validation logic.

Do not promote a complete song's pitch list, chord progression, form, energy curve or exact
statistics into a default Skill. Exact evidence remains project-local.

## Artistic discretion

These rules prevent accidental copying and low-quality mechanical MIDI. They are not a music
grammar. Dissonance, minimalism, noise, asymmetry, repetition, unusual form, deliberate grid
timing and conscious violations are allowed when they serve the brief and are documented.
