# Instrument-aware Composition and Performance Architecture

## Research gate and repository baseline

The requested research gate was completed before implementation. The repository has no
root `SKILL.md`, root `resources/`, or root `examples/`; relevant material is instead in
`AGENTS.md`, `README.md`, `references/midi-agent-skill`, `references/ableton-skills`,
existing demo projects, `src/` and `tests/`. Baseline validation passes 15 unit tests plus
the real FluidSynth doctor render.

## Problem statement

The legacy path stores almost-final note/chord/drum events. It can generate useful music,
but after `materialize_clip` every instrument is reduced to `NoteEvent(start, duration,
pitch, velocity)`. There is no persistent phrase intent, physical action, articulation
relation, controller curve, pitch bend or library translation stage.

## Four representations

1. **Musical intent** — section function, energy, harmony, role and interaction targets.
2. **Instrument phrase** — phrase type, register, instrument-specific gestures,
   playability settings, articulation and performance intent.
3. **Neutral performance events** — notes plus grouped attacks, drum gestures, CC curves,
   pitch curves and articulation tokens. Still independent of a sample library.
4. **Rendered MIDI events** — note/program/keyswitch/CC/pitch-bend messages after applying
   a sound-library profile.

Example semantic phrase:

```json
{
  "instrument": "electric_guitar",
  "role": "rhythm",
  "section": "verse",
  "phrase_type": "palm_muted_eighths",
  "harmony": [{"at": "1:1", "duration": 4, "chord": "E5"}],
  "register": "low_mid",
  "energy": 0.55,
  "articulations": ["palm_mute", "accent"],
  "performance_intent": {
    "attack": "tight",
    "release": "controlled",
    "humanization": "subtle",
    "picking": "alternate",
    "seed": 17
  }
}
```

## Compatibility strategy

- Legacy clips with `events` keep the byte-stable old expansion path.
- A clip may instead contain `instrument_phrase`; loader validation preserves its
  semantics and dispatches it to an instrument module.
- The phrase compiler returns ordinary events plus optional `performance_events`, so the
  existing MIDI/render/mix boundary stays intact.
- `semantic_phrases.json` is an inspectable build artifact; composition data remains the
  source of truth.

## Code layout

```text
skills/
  composition/ arrangement/
  instruments/{electric_guitar,electric_bass,drums,keyboards,strings}/
  performance/ validation/ renderers/
src/
  instruments/       # deterministic phrase compilers and playability models
  performance/       # neutral-event and profile compilation
  validation/        # musical diagnostics
profiles/
  general_midi/ sfizz/ shreddage_stratus_free/ custom_soundfonts/
```

Project-local `skills/` contains Agent-facing knowledge/routing notes, not globally
installed Codex skills. Executable Python remains in `src/` to fit the repository.

## Phrase compiler contract

```python
compile_phrase(phrase, context, seed) -> PerformancePhrase
```

The result contains deterministic notes/gestures, articulation tokens, physical metadata
(string/fret or limb assignment when known), warnings and provenance. Random choice is
permitted only among bounded musical alternatives and uses an explicit seed.

## Sound-library profile

Profiles declare capabilities and mappings:

```json
{
  "id": "general_midi",
  "supports": {"keyswitch": false, "cc": [1, 7, 10, 11, 64], "pitch_bend": true},
  "articulations": {
    "palm_mute": {"fallback": {"gate_ratio": 0.42, "velocity_delta": -5}},
    "legato": {"fallback": {"overlap_beats": 0.04}}
  }
}
```

- A profile may map an articulation to keyswitch, CC, program/channel, note shaping or
  `unsupported`.
- Fallback is explicit and reported. No composer contains keyswitch note numbers.
- Pitch-bend range is declared and encoded through RPN 0 only when the profile supports it.

## Validation model

Validators emit `error`, `warning` or `info`, with instrument, section, rule, evidence and
suggestion. Hard errors are limited to invalid schema/MIDI and clearly impossible physical
states. Musical concerns remain contextual warnings.

Initial validators:

- range and guitar string/fret assignment;
- drum limb conflicts and hat state;
- phrase repetition/variation and note-gap analysis;
- velocity pattern and articulation coverage;
- register collision;
- bass-kick alignment/over-copying;
- section density;
- guitar strum simultaneity and articulation/phrase diagnostics.

## Minimum demos and acceptance

Seven 8-16 bar demos prove rhythm guitar mute, open power chorus, expressive lead,
bass-kick relation, verse/chorus drums with fill, keyboard voice leading, and string long
tones with inner movement. Each emits composition JSON, semantic representation, MIDI,
validation report and README. Existing legacy tests must remain green.

## Incremental delivery

1. Research/docs (this document and six instrument documents).
2. Schema + IR + legacy compatibility tests.
3. Instrument compilers and profiles.
4. Validators.
5. Seven demos and real MIDI/render checks.
6. Update Agent workflow. Only then apply the system to a full song.

## Sources

- Project-pinned sources: `references/SOURCES.md` and the specific orchestration, groove,
  cleanup, arrangement and voice-leading files listed in `AGENTS.md`.
- MIDI Association MIDI 1.0 message/CC/RPN reference.
- Ample Sound Guitar/Bass manuals for instrument-specific articulation examples.
- Impact Soundworks Shreddage 3.5 Stratus FREE manual for a separate library mapping.
- Steinberg expression-map documentation for semantic articulation to library trigger
  separation.
- Yamaha keyboard/drum educational material for voice leading, organ/piano differences,
  register cooperation, backbeat and section contrast.
- Spitfire UACC documentation as an example of a CC-based library profile, not a universal
  mapping.

Primary-source links used during research:

- MIDI Association: [MIDI 1.0 messages](https://midi.org/summary-of-midi-1-0-messages) and
  [Control Change messages](https://midi.org/midi-1-0-control-change-messages).
- Ample Sound: [AGPF manual](https://amplesound.net/en/Main_Panel_Manual-AGPF.pdf) and
  [AGL manual](https://amplesound.net/en/Main_Panel_Manual-AGL.pdf).
- Impact Soundworks: [Shreddage 3.5 Stratus FREE manual](https://impactsoundworks.com/manuals/Shreddage%203.5%20Stratus%20FREE%20Manual.pdf).
- Steinberg: [Expression maps](https://www.steinberg.help/r/nuendo/15.0/en/cubase_nuendo/topics/expression_maps/expression_maps_c.html).
- Yamaha: [drum-set configuration](https://hub.yamaha.com/music-educators/instruments/perc/drum-set-configuration/),
  [pop/rock voicings](https://hub.yamaha.com/keyboards/k-how-to/poprock-voicings-part-1/),
  [piano/clav/organ playing](https://hub.yamaha.com/keyboards/k-how-to/how-to-play-electric-piano-clavinet-and-organ-sounds/), and
  [blending keyboard and guitar](https://hub.yamaha.com/keyboards/k-how-to/five-tips-for-blending-keyboard-and-guitar-parts/).
- Spitfire Audio: [UACC overview](https://support.spitfireaudio.com/en/articles/11816123-what-is-uacc-and-how-do-i-use-it).
