# Crash Into Daylight / 撞向天光

Original ~3 minute pop-rock demo for the clean-slate V2 workflow.

- 148 BPM, 4/4, E major
- 112 bars, about 181.6 seconds before render tail
- Flute is the temporary vocal-surrogate lead
- Verse: palm-muted electric-guitar pulse + sparse section-linked bass
- Pre-chorus: denser muted pulse and rising drum energy
- Chorus: continuous overdriven rhythm bed + full bass pulse
- Bridge: half-time first half, rebuild in second half
- Final chorus: fuller drums, pad lift, highest lead register

The arrangement was composed using the active V2 material vocabulary, especially `muted-pop-rock-pulse`, `continuous-overdrive-rhythm-bed`, `section-linked-pop-rock-bass`, `sustained-overdrive-guitar`, and `role-separated-midi-guitar-mix`.

## Build + render in one command

From the repository root on Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe .\projects\crash_into_daylight_pop_rock\build_song.py --render
```

Then listen to:

```text
projects\crash_into_daylight_pop_rock\output\mix.wav
```

`build_song.py` writes the editable `composition.json`, `instruments.json`, and `render.json` before invoking the repository's normal `scripts/render_song.py` pipeline.
