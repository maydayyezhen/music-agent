# Connected Lead Reference Demo

This is an original 16-bar rock-guitar study. It does not copy the supplied reference melody.

It tests:

- explicit D-major tonality with borrowed C natural;
- repeated-note propulsion;
- triplet-like short bursts inside a longer sentence;
- cross-bar slide continuity;
- late, rare register peak;
- long-form vibrato metadata reaching MIDI realization.

From the repository root:

```powershell
git pull
.\.venv\Scripts\python.exe -m unittest tests.test_long_form_tonality -v
.\.venv\Scripts\python.exe scripts\critic_instruments.py connected_lead_reference_demo --write
.\.venv\Scripts\python.exe scripts\critic_complexity.py connected_lead_reference_demo --write
.\.venv\Scripts\python.exe scripts\critic_continuity.py connected_lead_reference_demo --write
.\.venv\Scripts\python.exe scripts\render_song.py connected_lead_reference_demo
```

Listen to:

```text
projects\connected_lead_reference_demo\output\mix.wav
```

Also listen to the isolated lead stem before judging the full mix.
