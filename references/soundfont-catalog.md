# GeneralUser GS instrument catalog

Use `config/soundfont-catalog.json` as the authoritative, machine-readable list of every installed preset. Program numbers are zero-based. Do not guess a hidden bank or advertise an instrument that is absent from the catalog.

## Selection rules

Melodic track:

```json
{
  "engine": "fluidsynth",
  "bank": 8,
  "program": 25,
  "gm_name": "12-String Guitar"
}
```

Drum track:

```json
{
  "engine": "fluidsynth",
  "channel": 10,
  "bank": 128,
  "program": 40,
  "gm_name": "Brush"
}
```

Per-track SoundFont override:

```json
{
  "engine": "fluidsynth",
  "soundfont": "assets/soundfonts/another-library.sf2",
  "bank": 0,
  "program": 0
}
```

If `soundfont` is absent, the track inherits the global path from `render.json`. This preserves all existing projects.

## Useful installed colors

- `8/25 12-String Guitar`, `8/27 Chorused Clean Gt.`, `8/48 Orchestra Pad`.
- `12/48 Full Orchestra`, `13/48 Woodwind Choir`.
- Drum kits in bank 128 include Standard, Room, Power, Electronic, 808/909, Dance, Jazz, Brush, Orchestral, and SFX.

Choose by musical role and verify the rendered stem. A preset name is not evidence that it will fit the arrangement.

## Naming boundary

Presets containing `Choir`, `Voice`, or `Vox` are ordinary instruments. They may be selected like any other lead, pad, ensemble, or texture when they fit the arrangement; there is no usage prohibition. Their names only describe timbre and do not imply lyric pronunciation. When actual lyric-capable singing is requested, use the AI workflow in `references/vocal-workflow.md`.
