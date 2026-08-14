---
id: dry-grainy-steel-string-strum
name: Dry Grainy Steel-String Strum
instrument: steel_string_acoustic_guitar
status: active
---

# Dry Grainy Steel-String Strum

## Identity

A close, dry steel-string acoustic-guitar texture with audible pick contact and separate string attacks.

The desired impression is:

- clear right-hand motion;
- short, tactile pick grain;
- compact wooden body rather than glossy cinematic bloom;
- controlled low end;
- enough upper-mid presence to hear individual attacks;
- minimal room smear;
- one coherent guitar, not a wide chorus cloud.

Useful texture tags:

```text
dry
grainy
pick-forward
close-miked
compact
folk-rock
britpop-adjacent
rhythmic
```

This recipe describes a reusable texture. It does not store a source song's notes, chords, form or exact rhythm.

## Best instrument source

Prefer:

- steel-string acoustic guitar;
- pick-played or pick-capable sample source;
- multiple velocity layers;
- round robin or attack variation;
- separate or naturally present pick/string noise;
- short, controllable release;
- close microphone position or dry direct signal.

Avoid as the primary source:

- nylon guitar;
- soft fingerstyle-only samples;
- heavily reverberant baked samples;
- pre-processed stereo pads labeled as acoustic guitar;
- sources whose attack is already rounded off;
- sources with long fixed release that cannot handle repeated eighth-note attacks.

## Performance prerequisites

Processing cannot create convincing grain if the performance is a row of identical block chords.

The MIDI or performance should already provide:

- low-to-high onset order for downstrokes;
- high-to-low onset order for upstrokes;
- narrower and usually lighter upstrokes;
- variation between full and partial chord coverage;
- non-random metric accents;
- intentional note overlap and release;
- occasional air, ghost or muted actions when appropriate;
- no accidental same-pitch stacking.

For continuous eighth-note strumming, use the active acoustic-strumming Skill for the musical behavior. This material recipe only shapes the resulting sound.

## Texture axes

Use these normalized values as descriptive targets, not plugin parameters:

```text
dryness:          0.80–0.95
grain:            0.65–0.85
pick definition:  0.70–0.90
wood body:        0.45–0.65
low-end weight:   0.30–0.50
brightness:       0.55–0.75
room amount:      0.05–0.18
stereo width:     0.10–0.30
saturation:       0.10–0.25
```

The most important relationship is:

```text
pick definition > room amount
```

If the room tail becomes more obvious than the string attacks, the texture has drifted away from this recipe.

## Performance-to-render starting ranges

These are practical starting ranges derived from the desired texture and the successful grainier preview. They are not measurements from a commercial recording.

### Intra-stroke spread

```text
downstroke total spread: 18–45 ms
upstroke total spread:    10–30 ms
```

Scale with tempo and chord width.

- Wider downstrokes may use the upper part of the range.
- Two- or three-note upstrokes should remain near the lower part.
- At fast tempos, reduce both ranges so the stroke does not become an arpeggio.

### Attack relationship

```text
downstroke velocity reference: 1.00
upstroke velocity reference:   0.68–0.85
ghost contact reference:       0.35–0.55
```

Use meter and phrase function before adding randomness.

### Duration

```text
full stroke gate:       65–95% of the next eighth-note interval
partial stroke gate:    50–80%
ghost or muted contact: 15–35%
```

Compatible voices may ring across later attacks. Do not shorten every note merely to create more attack noise.

## Source and sampler controls

Start here when the instrument provides matching controls:

- choose a medium or firm pick articulation;
- increase pick or attack noise modestly;
- keep release noise present but below the initial pick transient;
- reduce room microphone level;
- favor close mic over ambient mic;
- reduce built-in stereo width;
- disable lush chorus or doubling;
- keep round robin enabled;
- avoid maxing attack-noise controls, which turns grain into plastic clicking.

A useful balance is that the pick should be audible at normal listening level but should not sound detached from the pitched string.

## Generic processing chain

### 1. High-pass and low-end control

Start with:

```text
high-pass: 65–90 Hz
slope:     12 or 18 dB/octave
```

Use the lower end for solo guitar and the higher end when bass and kick are present.

Do not remove all body below 180 Hz. The texture should be dry, not skeletal.

### 2. Mud control

Typical inspection area:

```text
220–450 Hz
```

Apply a broad reduction of roughly 1–4 dB only when repeated strums accumulate cardboard or boxiness.

Do not automatically carve this region. Some sources need the body.

### 3. Pick and string definition

Typical inspection area:

```text
2.2–4.8 kHz
```

A broad 1–3 dB lift can reveal pick grain when the source is dull.

When the source is already sharp, use a transient shaper or source-level attack control instead of a large EQ boost.

### 4. Harshness control

Inspect:

```text
5.5–8.5 kHz
```

Use a narrow or dynamic reduction when strong downstrokes become brittle or fizzy.

The goal is audible grain without a spray-can top end.

### 5. Compression

Starting range:

```text
ratio:          2:1–3:1
attack:         15–35 ms
release:        60–140 ms
gain reduction: 1–4 dB on stronger strokes
```

A slower attack preserves the pick transient. Too-fast attack erases the very grain this recipe is meant to keep.

Do not flatten every upstroke to the same level as every downstroke.

### 6. Saturation

Use subtle tape, console or soft-clipping saturation:

```text
harmonic drive: low
perceived effect: slight density and edge binding
```

The target is a small amount of roughness and cohesion, not obvious distortion.

When using a wet/dry control, a starting range around 3–12% processed signal is often enough.

### 7. Room

Use a short room or early-reflection treatment:

```text
decay:     0.25–0.65 s
pre-delay: 0–15 ms
wet level: 4–12%
```

Keep the dry pick attack in front.

Avoid long halls, glossy plates and obvious stereo tails for this texture.

### 8. Stereo image

Keep the guitar itself fairly compact:

```text
dry width:  mostly mono to modest stereo
room width: slightly wider than dry
```

For one guitar, avoid hard-splitting low strings left and high strings right. Small pitch- or string-dependent movement is acceptable, but it should still read as one instrument.

## Code-synthesis approximation

When no sample library is available, approximate the texture with:

- Karplus-Strong or another plucked-string resonator;
- a 6–12 ms high-passed noise transient for pick contact;
- a 10–25 ms low-level scrape component;
- slightly different excitation and damping per string;
- faster high-frequency decay than low-frequency decay;
- quiet body resonances around roughly 90–300 Hz;
- a short, low-level room response;
- restrained stereo spread.

Important relationships:

```text
pick transient is short and bright
string body is longer and pitched
scrape is quieter than both
room is quieter than the direct signal
```

Do not use identical oscillator envelopes for every chord tone. That produces smooth glass rather than grainy wood and string.

## Arrangement interaction

When a lead or vocal is present:

- reduce chord width before aggressively reducing brightness;
- lower upstroke velocity;
- use more partial strokes;
- reduce low-mid body slightly if masking occurs;
- keep enough pick definition that the rhythm remains audible at lower level.

When the guitar is exposed:

- allow a little more body;
- retain release and finger-change noise at a low level;
- avoid making the transient unnaturally sharp merely because there is more space.

## Failure modes

### Smooth wash with no individual attacks

Likely causes:

- attack too soft;
- too much room or release;
- insufficient intra-stroke onset spread;
- excessive compression with a fast attack;
- too little 2–5 kHz information;
- every string synthesized with the same envelope.

### Plastic clicking detached from the guitar

Likely causes:

- pick-noise control too high;
- transient layer too loud;
- noise transient too short and identical on every attack;
- not enough pitched string body;
- excessive 3–7 kHz boost.

### Cardboard boxiness

Likely causes:

- too much 250–450 Hz buildup;
- long overlapping full voicings;
- excessive body-mic level;
- compression release too slow.

### Brittle spray-can top end

Likely causes:

- too much 6–10 kHz;
- saturation after a large high-frequency boost;
- identical bright attack on every string;
- upstrokes rendered as loudly and broadly as downstrokes.

### Piano-like repeated chords

Likely causes:

- all chord tones begin at the same time;
- every stroke uses the full voicing;
- all notes are cut at every new attack;
- no difference between downstroke and upstroke coverage;
- velocity is copied uniformly across the chord.

Fix the performance layer before adding more effects.

## Listening checklist

Accept the texture when:

- individual string attacks are perceptible without sounding like a slow arpeggio;
- the pick contact belongs to the string rather than floating above it;
- downstrokes feel broader than upstrokes;
- the guitar remains compact and near the listener;
- the room is sensed more than heard;
- repeated eighth notes retain rhythmic definition;
- the low end supports the wood body without obscuring bass or kick;
- strong strokes have edge but do not become brittle;
- the texture still works at reduced volume.

## Provenance boundary

This recipe was created from the shared listening goal and the contrast between a smooth synthetic preview and a grain-enhanced synthetic preview.

Its parameter ranges are reusable production starting points and informed approximations. They were not objectively extracted from the referenced MIDI, because ordinary MIDI does not contain microphone, sample, EQ, compression, saturation or room settings.
