---
id: dry-grainy-steel-string-strum
name: Dry Pick-Forward Single Steel-String
instrument: steel_string_acoustic_guitar
status: active
---

# Dry Pick-Forward Single Steel-String

## Identity

A **single-guitar** steel-string texture that is close, dry, compact and pick-forward.

Useful tags:

```text
dry
single-guitar
pick-forward
close
compact
folk-rock
rhythmic
```

This recipe is useful when the goal is to hear one guitar and its attack clearly. It should **not** be treated as the default recipe for a thick layered Britpop-style guitar bed.

The earlier `britpop-adjacent` implication was removed after comparison against a user-provided multi-guitar MIDI arrangement. That comparison showed that a composite guitar texture can come from several complementary guitar tracks rather than from exaggerated pick noise on one track.

## Source requirements

Prefer:

- steel-string acoustic guitar;
- pick-capable source;
- multiple velocity layers;
- round robin or attack variation;
- controllable release;
- close or relatively dry microphone signal.

Avoid relying on processing to rescue a source whose attack is already excessively soft or whose room is baked in.

## Performance prerequisites

The performance should already provide intentional rhythm, chord coverage and note duration.

For ordinary single-note samplers or synthesis, directional onset spread may help down/up strokes read as physical sweeps. For dedicated strum articulations, explicit MIDI staggering may be unnecessary because the sample itself can contain the sweep.

Do not claim that simultaneous MIDI chord tones are inherently wrong for guitar. They are only likely to sound piano-like when the renderer treats every note as an unrelated single-note attack.

## Texture axes

Use these as descriptive targets, not universal plugin values:

```text
dryness:          0.80–0.95
pick definition:  0.65–0.85
wood body:        0.45–0.65
low-end weight:   0.30–0.50
brightness:       0.50–0.72
room amount:      0.04–0.16
stereo width:     0.05–0.25
saturation:       0.08–0.20
```

The pick should belong to the pitched string. If the transient sounds like a separate plastic click, reduce it.

## Intra-stroke timing

When the renderer needs explicit per-string timing, a practical starting range is:

```text
downstroke total spread: 12–35 ms
upstroke total spread:    8–24 ms
```

Use less spread at faster tempos and for narrow partial strokes.

Do not force these values when a strum sample already contains its own timing. Block-like MIDI onsets can be valid input to that kind of source.

## Velocity

This recipe does not prescribe one absolute velocity range.

Choose the velocity region that drives the selected sample source into the intended articulation. A hard-strummed patch may need substantially higher velocities than a soft exposed acoustic part.

When a relevant reference MIDI exists, inspect its velocity distribution for the current project instead of using a generic fixed value.

## Generic processing starting points

### Low end

```text
high-pass: roughly 65–95 Hz when needed
```

Do not remove the entire wooden body.

### Body and mud

Inspect roughly 220–450 Hz. Reduce only when repeated strums become boxy.

### Pick definition

Inspect roughly 2–5 kHz. Use source attack controls or modest EQ rather than extreme boosts.

### Harshness

Inspect roughly 5.5–8.5 kHz when strong strokes become brittle.

### Compression

A useful transparent starting point:

```text
ratio:          2:1–3:1
attack:         15–35 ms
release:        60–140 ms
gain reduction: about 1–4 dB on stronger strokes
```

Avoid very fast attack when preserving pick definition is the goal.

### Saturation

Use subtle tape, console or soft clipping for density and cohesion. Do not turn this single-guitar recipe into obvious distortion.

### Room

Keep the direct guitar in front:

```text
short room / early reflections
wet level: low
```

## Code-synthesis approximation

When no sample library is available:

- use a plucked-string resonator such as Karplus-Strong;
- add a short bright pick transient;
- keep scrape/finger noise quieter than the pitched string;
- vary excitation and damping per string;
- add modest 90–300 Hz body resonances;
- use a short, quiet room;
- keep stereo spread restrained.

The failed direction to avoid is **more pick noise = more rock authenticity**. Too much synthetic transient makes the guitar thin, clicky and detached from the body.

## Pairing with layered production

When the desired result is thick, coarse or wall-like, pair this or another suitable acoustic source with:

```text
materials_v2/production_chains/acoustic_guitar/multi_take_acoustic_stack.md
```

Layering can create density and grain without pushing one guitar's pick transient unnaturally hard.

## Failure modes

### Plastic clicking

Likely causes:

- pick-noise layer too loud;
- excessive 3–7 kHz emphasis;
- transient shape identical on every note;
- insufficient pitched body.

### Smooth but weak

Likely causes:

- source velocity too low for the desired articulation;
- attack too rounded;
- excessive sustain or room;
- insufficient rhythmic retriggering.

### Overly arpeggiated

Likely causes:

- inter-string spread too wide;
- explicit sweep added on top of a sample that already contains a sweep.

### Thin compared with a reference guitar bed

The problem may be arrangement or layering rather than single-guitar timbre. Check whether several guitar parts are contributing before adding more EQ or pick noise.

## Provenance boundary

This recipe comes from the successful single-guitar grain experiment in the current Music Agent work. Its production values are practical starting points, not measurements extracted from a commercial recording or MIDI file.

The user-provided MIDI comparison was used to **limit** the recipe's claims: ordinary MIDI can reveal program choice, velocity, timing, note duration and multi-track arrangement, but it cannot reveal microphone, EQ, compression, saturation or recorded pick-noise level.
