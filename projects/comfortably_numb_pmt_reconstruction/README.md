# Comfortably Numb PMT Reconstruction

This project is the first audible vertical slice of the `agent/pmt-gesture-ir`
branch.

It does not ask the composition generator to invent a similar solo. It takes the
user-supplied reference MIDI performance, serializes it through PMT, decodes that
PMT back into MIDI, and renders the result with the repository's existing audio
backends.

The purpose of this milestone is narrow:

1. preserve both source tracks;
2. preserve pitch and instrument identity exactly;
3. keep onset and duration within the 10 ms PMT grid;
4. keep velocity within the 32-bin PMT representation;
5. avoid truncating notes longer than 2 seconds;
6. emit a guitar gesture sidecar for later gesture-aware renderers.

## Build the PMT project

```powershell
.\.venv\Scripts\python.exe `
  projects\comfortably_numb_pmt_reconstruction\build_pmt_project.py
```

Generated files:

```text
performance.pmt
performance.meta.json
performance.gestures.json
roundtrip-report.json
```

## Verify the reference survived PMT

```powershell
.\.venv\Scripts\python.exe `
  projects\comfortably_numb_pmt_reconstruction\verify_pmt_reconstruction.py
```

The expected tolerances are:

```text
pitch / track / program: exact
onset: <= 5 ms
duration: <= 5 ms
velocity: <= 2 MIDI units
```

## Render

```powershell
.\.venv\Scripts\python.exe `
  scripts\render_pmt_project.py comfortably_numb_pmt_reconstruction
```

Listen to:

```text
projects\comfortably_numb_pmt_reconstruction\output\mix.wav
```

## Important boundary

The current WAV is rendered from the PMT note performance. The gesture sidecar is
preserved but is not yet interpreted by FluidSynth. That is the next A/B step,
after the new PMT path proves it can reproduce the supplied piece without losing
the performance data.
