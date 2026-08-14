# Chiptune / 8-bit Project Template

Copy this template when starting a new chip-oriented composition project.

## Expected files

```text
manifest.json
composition.json
chip-performance.json
output/
reports/
```

The template files are examples, not a finished song.

## Start procedure

1. Choose `constraint_mode`: `8bit_aesthetic`, `hardware_inspired`, or `strict_platform`.
2. Select a compatible profile.
3. Replace template project metadata.
4. Write musical structure into the chosen authoritative composition artifact.
5. Put chip-specific performance state in `chip-performance.json` only when it is not already represented safely elsewhere.
6. Derive MIDI/audio through an explicit adapter/renderer when available.
7. Record degradation or unsupported controls in reports instead of silently dropping them.

For `strict_platform`, replace the generic profile with a validated platform profile before claiming hardware accuracy.
