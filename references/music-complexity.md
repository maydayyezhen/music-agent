# Music Complexity System

This layer controls **how much musical information is active and where it is
placed**. Complexity is not a synonym for note count, randomness, or making
every track busy.

## Agent entry point

For every new song or major rewrite:

1. Translate the brief into a global complexity profile.
2. Choose a contour across sections.
3. Design one or more rhythm motifs before assigning pitches.
4. Give each instrument a rhythmic identity and explicit silence.
5. Allocate a section budget so not every role spends complexity at once.
6. Compose pitch/harmony, then add restrained performance variation.
7. Run `scripts/critic_complexity.py <song> --write`; interpret warnings in
   context. Never respond to a warning by blindly adding notes.

## Five levels

| Level | Musical intention |
|---|---|
| `minimal` | Few layers, long phrases, high rest ratio, repetition is welcome |
| `simple` | Clear groove and theme, limited counterpoint and fills |
| `standard` | Balanced pop/game-BGM default with sectional contrast |
| `rich` | More dialogue, harmonic color, register movement, and varied returns |
| `dense` | High information and fast role exchange, still with hierarchy and gaps |

Six independent dimensions use integers from 1 to 5:

- `rhythm`: syncopation, duration vocabulary, groove variation.
- `harmony`: chord color, inversions, secondary function, voice leading.
- `arrangement`: number of roles and the sophistication of entrances/exits.
- `melodic_ornamentation`: pickups, passing notes, turns, octave displacement.
- `density`: simultaneous and temporal event density.
- `variation`: transformation between repetitions and sections.

`level` selects a preset; individual dimensions may override it. The presets
live in `config/complexity-presets.json`. Missing complexity means `standard`,
so old projects retain their exact notes and rendering behavior.

```json
{
  "complexity": {
    "level": "rich",
    "rhythm": 4,
    "harmony": 4,
    "arrangement": 4,
    "melodic_ornamentation": 3,
    "density": 3,
    "variation": 4
  },
  "complexity_contour": "verse_chorus"
}
```

Supported contours are `flat`, `gradual_build`, `verse_chorus`, `wave`,
`sparse_to_climax`, and `custom`. A section override has higher priority than
the contour and global profile:

```json
{
  "name": "breakdown",
  "bars": 8,
  "complexity": {"level": "simple", "harmony": 4, "density": 1},
  "complexity_budget": {"lead": 4, "drums": 2, "bass": 1, "texture": 1}
}
```

Budget points describe **where attention lives**, not a note quota. A standard
section guide is 11 points; the example above spends the section mostly on the
lead while keeping the texture quiet. Section target guides are minimal 5,
simple 8, standard 11, rich 15, and dense 19.

## Rhythm before pitch

`rhythm_motifs` store reusable onset and duration shapes. Clips may annotate
which motif/variation they realize; their actual note events remain explicit,
auditable MIDI data.

```json
{
  "rhythm_motifs": {
    "signal_A": [
      {"offset": 0, "duration": 1},
      {"offset": 1.5, "duration": 0.5},
      {"offset": 2, "duration": 1},
      {"offset": 3, "duration": 1}
    ]
  },
  "tracks": {
    "lead": {"sections": {"verse": {
      "loop_bars": 2,
      "rhythm_motif": "signal_A",
      "rhythm_variation": "A'",
      "events": []
    }}}
  }
}
```

The helper `vary_rhythm_motif()` provides deterministic A, A', B, B', and C
shapes without choosing pitches. It is optional; hand-written stylistic
variations are valid.

## Rhythmic identities and silence

Define identities in the brief or `instrument_notes.md`, for example:

- lead: long-short cells, phrases end before bar 4;
- bass: downbeat anchors plus two approach notes per four bars;
- chords: offbeat answers, never duplicate the lead rhythm for a full phrase;
- drums: steady subdivision with fills only at real boundaries;
- texture: long entries and planned exits.

Silence is first-class structure. Prefer call-and-response, foreground versus
background, and entrances/exits. A dense passage can be complex because roles
trade rapidly; it does not require six continuous tracks.

## Performance complexity

Performance variation comes last. Vary velocity by role and phrase, shorten
percussive articulation, lengthen selected legato notes, and add only small
timing offsets where the style permits. Preserve kick/snare anchors and motif
recognition. Humanization must not conceal weak rhythm design.

## Natural-language mapping

`parse_complexity_request()` maps common brief phrases deterministically:

- “极简、很空” -> `minimal`
- “丰富一点但不要很吵” -> rich arrangement/harmony with density capped at 2
- “节奏更有意思” -> rhythm at least 4
- “和声漂亮、旋律少装饰” -> harmony at least 4, ornamentation at most 2

Agents should record the interpreted profile in `musical-brief.md` and in
`composition.json`; do not hide it in reasoning.

## Critic metrics

The critic reports, by track and section:

- `note_density`, `rest_ratio`, `duration_entropy`, `same_grid_ratio`
- `velocity_variance`, `pattern_repetition`, `event_count`
- `section_density`, `active_tracks`, `track_overlap_ratio`
- `onset_overlap_ratio`, target and declared complexity budgets

Warnings look for melody without breath, equal-duration grid lock, tracks that
speak together, continuous all-track activity, profile mismatch, and duplicated
busyness. Repetition is not itself a defect—especially in minimal music—and a
warning can be consciously rejected in `critique.md`.

