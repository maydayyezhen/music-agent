# Renderer routing

Rendering stays downstream of composition. `instruments.json` selects FluidSynth/SFZ and its
sound-library profile; `render.json` controls audio. Profile mappings produce MIDI triggers before
the local renderer. Unsupported articulations must degrade explicitly and remain in the report.

