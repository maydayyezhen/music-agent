# Applying Long-Form Mode to a Full Song

The minimum tests are complete. The existing full song has deliberately not been rewritten.

To migrate one Lead Guitar section safely:

1. Keep the existing clip as a recoverable `composition_vN.json` version.
2. Set `phrase_generation_mode` to `long_form` only on the selected Lead Guitar clip.
3. Make `loop_bars` equal the complete 8–16 bar planning window. Do not feed the planner a
   repeated four-bar clip.
4. Add the complete section harmony, `section_arc`, `phrase_relationships`, `motif_seed` and
   `long_form_phrase_rules` described in `docs/long_form_phrase_schema.md`.
5. Place the planned peak and delayed target in the later half. Allow only the final relationship
   to use `resolution: strong`; connect earlier relationships with `continuation_from` and
   `continuation_to`.
6. Use motif operations to describe development. A breath may be marked after a motif event,
   but it does not reset melodic state.
7. Render and inspect the generated `long-form-plans.json`, `long-form-validation.json`, MIDI,
   stem and mix:

```powershell
.\.venv\Scripts\python.exe scripts\render_song.py <song>
.\.venv\Scripts\python.exe scripts\critic_long_form.py <song> --write
```

8. Compare against the preserved legacy MIDI before selecting the new composition version.

`projects/long_form_phrase_demos/02_developing_solo_16bar/composition.json` is the canonical
sixteen-bar example. The rhythm-guitar clips need no migration and remain on their existing
instrument-aware compiler.
