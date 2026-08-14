# Concrete V1 critique and targeted revision

## What already worked and therefore was not rewritten

- Global bars 49-80 form one 32-bar Solo island, with all bars active and only 0.09 beat maximum internal gap.
- The Solo peak is delayed until global bar 74 / Solo bar 26.
- Theme and Solo have 0 different-pitch overlap; bend messages are channel-safe.
- Rhythm guitar, bass, drums and organ already provide a coherent rock hierarchy and continuity critic has 0 warnings.

## Actual failure 1

- Problem: authored guitar position changes are not preserved.
- Concrete bars: global bars 13, 17, 21, 25, 29, 33, 37, 57, 65, 73, 77, 81, 87, 93.
- Root cause: `src/instruments/electric_guitar.py::_lead()` always calls the generic nearest-fret allocator and discards `planned_string` / `planned_fret`.
- Modified file: `src/instruments/electric_guitar.py`.
- Logic: when the song supplies a string/fret pair, verify its bounds and pitch, then use it; keep automatic allocation as the compatibility fallback.
- Expected sound: position shifts belong to the planned continuous hand path instead of collapsing to a convenient but musically different string choice.
- Verification: materialized global bar 57 G4 is now string 3/fret 12, not string 5/fret 3; impossible pairs raise a test-covered error.

## Actual failure 2

- Problem: declared slide gestures are silent in V1.
- Concrete bars: the same 14 position-change bars above; V1 contains 0 recognized slide-in pitch-wheel gestures.
- Root cause: `slide_from_semitones` is not copied by the Lead compiler and the GM profile/MIDI generator have no neutral slide curve path.
- Modified files: `src/instruments/electric_guitar.py`, `src/performance/profiles.py`, `src/midi/generator.py`.
- Logic: preserve the semantic interval, declare bend range through the profile, then create a six-point monotonic approach from the lower pitch to center during the first 62% of the target note.
- Expected sound: audible connection into a new fretboard position, without changing pitches, rhythm, velocity or phrase structure.
- Verification: V2 contains 14 recognized slide-in gestures at the exact authored bars, 0 unsafe pitch-wheel messages, and 0 different-pitch overlaps.

## Warnings intentionally not “fixed”

The critic's `melody_no_breath` warning would push the Solo toward the prohibited vocal model. The repeated-bar warning detects motif sequence and repeated-note drive, while the independent four-bar-window audit finds no exact repeated lick window. Thresholds and validators were left unchanged; the critique records the artistic exception instead.
