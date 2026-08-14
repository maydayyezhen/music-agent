---
id: role-separated-midi-guitar-mix
name: Role-Separated MIDI Guitar Mix
kind: production_chain
status: active
---

# Role-Separated MIDI Guitar Mix

## Identity

A reusable MIDI-level mix-balancing strategy for arrangements with several electric-guitar roles. The central idea is to separate **foreground**, **rhythm bed**, and **support texture** with controller balance and spatial placement instead of making every guitar equally loud and equally close.

This material is intentionally limited to what a reference MIDI can support. It covers MIDI controller balance, pan, reverb/chorus sends and role hierarchy. It does **not** claim source-derived EQ, compression, amplifier, microphone or mastering settings.

Useful tags:

```text
midi-mix
electric-guitar
role-hierarchy
foreground-vs-bed
cc7
pan
reverb-send
chorus-send
section-balance
```

## Core principle

Do not mix several guitar roles as peers.

First classify each active part:

```text
foreground / melodic guitar
rhythm bed
muted support
clean / chorused bed
```

Then give each role a distinct mix position.

A useful hierarchy is:

```text
foreground melodic guitar
→ more audible direct presence
→ less send-based distance

continuous rhythm guitar bed
→ lower direct level
→ more ambience / distance
→ off-center placement

support guitar
→ level and space chosen to avoid masking the current foreground
```

The exact numeric values must be adapted to the current sound source and arrangement.

## Same-program foreground versus bed

A particularly useful source observation came from two separate GM Program 29 Overdriven Guitar tracks that served different roles.

The sustained melodic track used:

```text
CC7 volume: 95
CC10 pan:   74
CC91 reverb send: 64
CC93 chorus send: 64
```

The continuous rhythm Overdrive track used:

```text
CC7 volume: 80
CC10 pan:   94
CC91 reverb send: 127
CC93 chorus send: 64
```

Because the two tracks use the same GM program, this supports a robust relative principle:

```text
melodic / foreground Overdrive
→ higher direct level
→ lower reverb send
→ closer to center

rhythm Overdrive bed
→ lower direct level
→ much wetter
→ farther to one side
```

Do not universalize the absolute CC values. Preserve the role relationship.

## Why level alone is not enough

Reducing a rhythm guitar only with CC7 can make it disappear. Instead, let it remain active while changing its perceived distance and placement.

Useful controls are:

```text
CC7  -> direct MIDI channel level
CC10 -> stereo placement
CC91 -> reverb send / apparent distance when the renderer supports it
CC93 -> chorus send / modulation width when appropriate
```

A background rhythm layer may remain continuously active while reading as background because it is lower, wetter and spatially separated from the foreground guitar.

## Clean / chorused bed evidence

A separate chorused clean-guitar track in the same source used:

```text
CC7 volume: 127
CC10 pan:   34
CC91 reverb send: 90
CC93 chorus send: 95, later 127
```

This supports another reusable principle:

```text
wide / chorused clean bed
→ may be strong in level
→ can occupy a clearly different side of the stereo field
→ chorus send can define width and identity rather than simple loudness
```

Do not infer that clean guitar should always be louder than every distorted guitar. The source only demonstrates one successful role separation.

## Muted-guitar evidence and boundary

The source muted-guitar track used:

```text
CC7 volume: 75
CC91 reverb send: 120
CC93 chorus send: 64
```

No explicit pan controller was present on that track.

This is useful evidence that a muted part does not need maximum direct level to remain functional. However, the source does not establish that this exact balance remains correct when muted guitar overlaps a different arrangement or when the listener wants it as the foreground rhythm detail.

When adapting the material, prioritize the intended role over copying the source number.

## Section transitions: preserve energy by default

Do **not** use CC7 fade-outs as the default way to end an interior section.

For ordinary verse / build / chorus / bridge handoffs, prefer:

```text
role handoff
+ deliberate note ending
+ phrase gap
+ density change
+ new layer entry / old layer exit
```

The next section should normally arrive with intentional energy, not feel as if the channel fader is being pulled down underneath it.

A fade is reserved for cases where the musical form explicitly calls for it, especially:

```text
intro fade-in
outro fade-out
explicit atmospheric dissolve
special transition whose purpose is loss of energy
```

Even when a reference MIDI contains interior CC7 fades, treat those as source-specific arrangement choices rather than a reusable default.

## Adaptation rule

When applying this material to a new project:

1. Preserve foreground-versus-bed ordering before copying any exact value.
2. Compensate for attack density. A denser rhythm part may need lower direct level even when it remains clearly audible.
3. Compensate for the renderer. CC91 and CC93 behavior varies between SoundFonts, synths and plugins.
4. Rebalance when several guitar families overlap that were not simultaneously active in the reference.
5. Prefer reducing a masking bed before endlessly boosting the foreground.
6. Keep interior-section energy stable unless the composition explicitly asks for a fade.

## Failure modes

Revise when:

- every guitar is assigned nearly the same level and center position;
- the rhythm bed masks a melodic guitar even though both parts are musically correct;
- a background guitar is made quieter but still occupies the same pan and apparent distance as the foreground;
- an interior section loses momentum because a routine CC7 fade pulls the guitar bed away;
- a phrase tail is confused with a channel-level fade-out;
- absolute CC values from one MIDI are treated as universal decibel targets;
- EQ, compression, amp or microphone claims are attributed to MIDI evidence that cannot support them.

## Study provenance

This material was abstracted from the controller and role structure of a user-provided pop-rock MIDI with several dedicated guitar tracks.

Observed source facts used here:

- chorused clean guitar: CC7 127, pan 34, reverb send 90, chorus send 95 then 127;
- sustained melodic GM Program 29 Overdrive: initial CC7 95, pan 74, reverb send 64, chorus send 64;
- continuous rhythm GM Program 29 Overdrive: initial CC7 80, pan 94, reverb send 127, chorus send 64;
- muted guitar: CC7 75, reverb send 120, chorus send 64, with no explicit pan event;
- the source also contained extensive CC7 automation, including fades, but listening tests in the current project showed that promoting interior fade-outs as a general rule caused unwanted loss of section energy;
- therefore those fades remain source-specific evidence and are not a default production behavior.

The source does not reveal commercial-recording EQ, compression, amplifier, cabinet, microphone, bus processing or mastering.