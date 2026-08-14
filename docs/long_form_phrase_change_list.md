# Long-Form Phrase Change List

## Added

- `docs/long_form_phrase_analysis.md`
- `docs/long_form_phrase_schema.md`
- `docs/long_form_phrase_application.md`
- `src/melody/__init__.py`
- `src/melody/long_form.py`
- `src/validation/long_form_phrase_validator.py`
- `scripts/critic_long_form.py`
- `scripts/build_long_form_phrase_demos.py`
- `tests/test_long_form_phrase.py`
- `projects/long_form_phrase_demos/01_singing_lead_8bar/`
- `projects/long_form_phrase_demos/02_developing_solo_16bar/`
- `projects/long_form_phrase_demos/03_legacy_vs_long_form_ab/`

## Modified

- `src/composition/loader.py`: validates both generation modes and the three planning layers.
- `src/instruments/electric_guitar.py`: dispatches long-form Lead Guitar realization while
  preserving the existing rhythm and legacy lead paths.
- `src/instruments/compiler.py` and `src/instruments/__init__.py`: export plans and state traces.
- `src/validation/__init__.py`: exports the dedicated analyzer.
- `scripts/render_song.py`: writes long-form plan and validation artifacts when present.
- root `SKILL.md`, `AGENTS.md`, `README.md`, and composition/guitar/validation skill routing.

The existing complete song and Rhythm Guitar composition data were not rewritten.
