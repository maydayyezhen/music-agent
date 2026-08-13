# Accompaniment Texture and Continuity

Read this before writing or substantially regenerating accompaniment. The main
idea is simple:

```text
Accompaniment is not just a sequence of note events.
```

Every section needs an intentional balance of:

- **Point**: stab, hit, short accent, drum attack.
- **Line**: bass phrase, broken chord, arpeggio, ostinato, counterline.
- **Plane**: sustained chord, held guitar, pad, pedal, harmonic bed.

Unless the style explicitly calls for pointillism, the lead must not be the
only line while all accompaniment becomes short disconnected points.

## Schema and compatibility

`texture`, `continuity`, `harmony_spans`, and `texture_pattern` are optional.
Old clips containing only `events` render through the unchanged path. New
texture generation activates only when a clip has `harmony_spans`.

```json
{
  "role": "harmonic atmosphere",
  "texture": "sustain",
  "continuity": {
    "sustain_ratio": 0.9,
    "legato_ratio": 0.8,
    "overlap": 0.08,
    "common_tone_retention": 0.9,
    "voice_leading_strength": 0.9
  },
  "sections": {
    "verse": {
      "loop_bars": 4,
      "harmony_spans": [
        {"at": "1:1", "duration": 4, "pitches": ["C3", "E3", "G3"]},
        {"at": "2:1", "duration": 4, "pitches": ["A2", "C3", "E3"]}
      ],
      "texture_pattern": {"register": [55, 76], "voices": 4, "velocity": 42},
      "events": []
    }
  }
}
```

Track settings provide defaults; clip settings override them. This lets one
instrument evolve by section.

## Executable textures

| Texture | Family | Generation behavior |
|---|---|---|
| `sustain` | Plane | Long voiced harmony; shared MIDI pitches merge across chord changes |
| `pulse` | Point | Explicit offsets, unequal durations/accents, phrase-end rest |
| `broken_chord` | Line | Named voice-index pattern; cursor continues across chords |
| `arpeggio` | Line | Directional contour; nearest legal tone at chord changes; no root reset |
| `ostinato` | Line | Recognizable index/offset/accent motif with small phrase variation |
| `counterline` | Line | Start-development-arrival-release contour with a phrase breath |
| `stab` | Point | Short accents with planned omissions; never a universal default |
| `pedal` | Plane | One pitch held across several harmony spans |

`harmony_spans.pitches` list chord identity; the generator chooses a legal
register voicing. `texture_pattern` controls register, voice count, velocity,
and texture-specific values such as pulse offsets or broken-chord indices.

## Continuity parameters

All values are guides from 0 to 1:

- `sustain_ratio`: preference for long durations;
- `legato_ratio`: preference for adjacent notes meeting at their boundaries;
- `overlap`: small beat overlap for suitable lines and planes;
- `common_tone_retention`: value placed on keeping shared pitches sounding;
- `voice_leading_strength`: value placed on small ordered voice movements.

Typical sustain-ratio intent:

- sustain 0.7–1.0;
- broken chord 0.2–0.5;
- arpeggio 0.3–0.6;
- counterline 0.4–0.8;
- stab 0.0–0.2.

These are generation tendencies, not validator hard limits. Different pitches
may overlap for legato. Same-pitch duplicates are always trimmed; when authored
melody meets generated accompaniment, the authored event wins.

## Smooth voice leading

The voicing planner minimizes an inspectable cost:

```text
ordered voice movement
+ large-leap penalty
+ register/spacing penalty
- exact common-tone bonus
```

It treats each voice as a line. Chord identity changing does not imply every
voice must reattack. For example C–Am should normally retain C and E when the
instrument/register permits it.

## Instrument behavior

### Bass

Use a line, not repeated roots or random chord tones. Mix held roots, fifths,
approaches, anticipation, octave movement, and releases. Durations should
include whole/dotted/half/short pickup values. Set
`texture_pattern.bass_line: true` to activate the bass-specific generator.

### Piano

Separate the main melody from accompaniment intent. Useful section strategies
are sustain, broken chord, arpeggio, sparse pulse, or inner motion. Do not use a
uniform one-note-per-beat pattern as the default.

### Guitar

Use guitar-shaped roles: a sustained chord may use `strum_spread` to stagger
its voices; other sections can use offbeat pulse, broken chord, muted point, or
single-note response. Do not copy piano accompaniment events and only change
the program.

### Pad and strings

Pad normally favors sustain/pedal, slow change, common-tone retention, and
small overlap. Strings may alternate a connected counterline and sustained
inner voices. Do not retrigger a rhythmic pad every beat unless explicitly
requested.

## Complexity interaction

Complexity changes motion and interaction, not the right to sustain:

- minimal: sustain, pedal, sparse line;
- simple: sustain, simple broken chord, connected bass;
- standard: broken chord, fragmentary counterline, arpeggio, patterned pulse;
- rich/dense: more sectional texture changes and dialogue.

Even dense music needs planes and hierarchy. Never convert every plane into
points merely to raise event count.

## Critic

Run:

```powershell
.\.venv\Scripts\python.exe scripts\critic_continuity.py <song> --write
```

The report contains average note duration, short-note ratio, sustain ratio,
legato ratio, average positive gap, overlap ratio, duration entropy,
voice-leading distance, common-tone retention, texture distribution, and
point/line/plane balance. It warns about disconnected pointillism, missing
planes/lines, texture mismatch, poor voice leading, and excessive stabs. A
warning is contextual evidence, not an instruction to make everything longer.
