# Composer Checklist

## Complexity and rhythm architecture

- [ ] Global level and six dimensions are explicit (or intentionally inherit `standard`).
- [ ] Section contour and overrides match the emotional/energy contour.
- [ ] A rhythm motif was designed before pitch expansion.
- [ ] Each active instrument has its own rhythmic identity.
- [ ] Section role budgets distribute attention instead of duplicating busyness.
- [ ] Lead phrases contain deliberate breathing space.
- [ ] At least one long section avoids continuous all-track activity.
- [ ] `scripts/critic_complexity.py <song> --write` was reviewed contextually.

Complete this after the first full render and before declaring a song finished. Record concrete failures and planned fixes in `projects/<song>/critique.md`. “Intentional because …” is a valid answer when it serves the brief.

## Accompaniment texture and continuity

- [ ] Does each section intentionally combine Point, Line, and Plane where the style permits?
- [ ] Do accompaniment tracks declare executable textures or contain equally clear explicit-event behavior?
- [ ] Are `sustain`/`pedal` parts actually sustained instead of retriggered every beat?
- [ ] Do broken chords, arpeggios, ostinatos, and counterlines read as continuous phrases rather than random chord tones?
- [ ] Does the bass mix long anchors, movement, approaches, and useful rests?
- [ ] Does guitar writing resemble strum/held chord/broken chord/offbeat comping rather than piano MIDI with another program?
- [ ] Do pad and strings retain common tones and use smooth inner-voice motion where appropriate?
- [ ] Is any long passage accidentally dominated by short equal notes and regular small gaps?
- [ ] Did `scripts/critic_continuity.py <song> --write` pass or were its warnings addressed in critique?
- [ ] Did the fix preserve Point activity instead of turning all accompaniment into an undifferentiated long drone?

## Melody

- [ ] Is there a clear motif with a recognizable rhythmic identity?
- [ ] Does the motif repeat enough to register?
- [ ] Is there meaningful variation rather than unrelated replacement?
- [ ] Does the chorus have a specific hook and landing point?
- [ ] Do verse and chorus differ in register, contour, density, or rhythm?
- [ ] Are question/answer phrases and useful rests audible?
- [ ] Is the climax placed deliberately?
- [ ] Is any passage merely scale-safe random wandering?

## Harmony

- [ ] Does the progression support each section's emotional function?
- [ ] Do tension and release have clear destinations?
- [ ] Is upper-voice leading smooth where it should be?
- [ ] Are large leaps, inversions, slash chords, and extensions purposeful?
- [ ] Do low voicings avoid mud and masking?
- [ ] Does the harmony develop established material instead of changing randomly every four bars?

## Bass

- [ ] Does the line use more than chord roots?
- [ ] Do fifths, chord tones, approaches, passing tones, or rests have clear roles?
- [ ] Does it connect naturally into the next chord?
- [ ] Does it cooperate with the kick without copying it exactly?
- [ ] Is it supportive rather than constantly overplaying?

## Guitar

- [ ] Is the guitar rhythm/pitch content distinct from the piano?
- [ ] Does it resemble a playable guitar role or shape?
- [ ] Does its articulation change by section (mute, strum, power chord, arpeggio, riff, lead response)?
- [ ] For continuous Acoustic/Electric Rhythm strumming, does the IR preserve down/up hand motion and air strokes rather than storing sounding notes only?
- [ ] Do Verse and Chorus meet their intended audible strum density without accidental one-hit/downbeat-only bars?
- [ ] Does hand direction continue across barlines and chord changes without a hidden pattern reset?
- [ ] On a sixteenth grid, are all 16 alternating hand positions represented even when some are air strokes?
- [ ] Do partial strokes retrigger only selected strings while safe unselected strings can keep sustaining?
- [ ] Does each four-bar unit use related variations of one skeleton instead of unrelated per-bar random patterns?
- [ ] Does Vocal activity change velocity, openness or string count rather than stopping the strumming hand?
- [ ] Are any `sustained_chord_hit` bars conscious arrangement planes and documented as exceptions?
- [ ] Does it leave space for the main hook?
- [ ] For a substantial Lead Guitar part, was `docs/guitar_native_lead_playbook.md` followed?
- [ ] Does the lead grow from a playable fretboard motif and connected position movement rather than vocal-style short phrases?
- [ ] Can every adjacent solo pattern explain its connection through shared pitch, slide/release, retained picking rhythm, sequence, compression, extension, or continued contour?
- [ ] Is the climax deliberately delayed, followed by continued development or thematic recovery rather than immediate shutdown?
- [ ] Did the real MIDI preserve any intentional `planned_string` / `planned_fret` and channel-safe bend/slide gestures without different-pitch overlap?

## Piano

- [ ] Are left/right-hand or bass/upper-register roles clear?
- [ ] Are voicings and density appropriate to the section?
- [ ] Are low chords free of unnecessary mud?
- [ ] Is the piano doing more than firing uniform chord blocks?

## Strings and pad

- [ ] Are strings more than copied chord notes?
- [ ] Do they provide counter-line, inner movement, swell, octave support, or a meaningful climax?
- [ ] Do string entrances/exits contribute to the energy map?
- [ ] Does the pad add atmosphere/glue without competing with melody or bass?
- [ ] Would removing either part reveal a real arrangement function?

## Drums and groove

- [ ] Are kick and snare roles coherent?
- [ ] Do verse, pre-chorus, and chorus differ audibly?
- [ ] Do hats have accents/variation rather than identical repeated velocity?
- [ ] Are fills and crashes tied to transitions?
- [ ] Are ghost notes and extra kicks controlled rather than cluttered?
- [ ] Is timing humanization appropriate to the genre and instrument?

## Arrangement

- [ ] Do instruments enter and leave, or does everything play continuously?
- [ ] Does the measured and perceived density follow the energy map?
- [ ] Is the Verse → Pre → Chorus rise unmistakable?
- [ ] Is the chorus a payoff rather than merely a louder copy?
- [ ] If present, does the bridge/breakdown create enough contrast?
- [ ] Are transitions legible without relying on excessive effects?
- [ ] Is foreground/background hierarchy clear in every section?

## MIDI and render

- [ ] Are velocities shaped by accents and phrases rather than all equal?
- [ ] Are durations/articulations varied for musical reasons?
- [ ] Are timing offsets restrained and anchors preserved?
- [ ] Are there duplicate, stuck, tiny, overlapping, or out-of-range notes?
- [ ] Are all intended stems non-silent and the final duration correct?
- [ ] Is the mix free of clipping, severe masking, and an overlong/sudden tail?
- [ ] Has the initial render been critiqued and at least one revision rendered?
