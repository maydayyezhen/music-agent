# Afterglow Current

Original 32-bar instrumental composition with continuous steel-string acoustic accompaniment and an electric-guitar foreground solo.

## Build

```powershell
.\.venv\Scripts\python.exe projects\afterglow_current\build_song.py
```

This writes:

- `composition_v1.json`
- `composition_v2.json`
- `composition.json` selecting V2
- `composition.normalized.json`
- `core_motif.json`
- `manifest.json`

## Validate

```powershell
.\.venv\Scripts\python.exe scripts\critic_instruments.py afterglow_current --write
.\.venv\Scripts\python.exe scripts\critic_complexity.py afterglow_current --write
.\.venv\Scripts\python.exe scripts\critic_continuity.py afterglow_current --write
.\.venv\Scripts\python.exe scripts\critic_long_form.py afterglow_current --write
```

The acoustic part also uses the continuous-strumming path, so run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_strumming_continuity -v
```

## Render through the thin project facade

```powershell
.\.venv\Scripts\python.exe scripts\render_project.py afterglow_current
```

Or call the existing composition renderer directly:

```powershell
.\.venv\Scripts\python.exe scripts\render_song.py afterglow_current
```

Listen at:

```text
projects\afterglow_current\output\mix.wav
```

The project is authored from scratch. It does not import or reconstruct a reference MIDI.
