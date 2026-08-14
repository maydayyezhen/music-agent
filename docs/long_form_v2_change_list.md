# Long-Form v2 Minimal-Fix Change List

## Modified

- `SKILL.md`, `AGENTS.md`, `README.md` and the composition/guitar/validation skill routing:
  stable default and explicit experimental opt-in.
- `src/composition/loader.py`: mode aliases, stable default, and semantic cross-bar reasons.
- `src/instruments/electric_guitar.py`: explicit experimental gate.
- `src/instruments/compiler.py`: experimental-plan export gate.
- `src/melody/long_form.py`: safe monophonic default, effect opt-ins, reasoned bar crossings,
  no automatic phrase-ending vibrato or random duration growth.
- `src/midi/generator.py`: channel-overlap Pitch Bend safety and gradual bend curves.
- `profiles/general_midi/profile.json`: no synthetic overlap-legato gate extension.
- `src/validation/__init__.py`: skeleton validator export.
- `scripts/build_long_form_phrase_demos.py` and `tests/test_long_form_phrase.py`: migrated
  explicit experimental mode and safe-realization assertions.
- `docs/long_form_phrase_schema.md`: stable/experimental mode contract.

## Added

- `docs/long_form_rollback_audit.md`
- `docs/long_form_v2_change_list.md`
- `src/validation/melody_skeleton.py`
- `scripts/build_melody_skeleton_v2.py`
- `tests/test_melody_skeleton_v2.py`
- `tests/fixtures/lead_guitar_long_form_v2/melody_skeleton_v2.json`
- `tests/fixtures/lead_guitar_long_form_v2/melody_skeleton_v2.mid`
- `tests/fixtures/lead_guitar_long_form_v2/melody_skeleton_v2_report.md`
- `tests/fixtures/lead_guitar_long_form_v2/legacy_fragmented_test.mid`
- `tests/fixtures/lead_guitar_long_form_v2/ab_report.json`

No guitarized `guitar_realization_v2.mid` was generated. The plain skeleton is the acceptance
target for this iteration.
