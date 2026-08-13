# Optional Vocal Composition and Rendering

This layer is used only when a user explicitly asks for singing, lyrics, a lead vocal, or a vocal demo. Instrumental music remains the normal path and needs no `vocals.json`.

## What the local backends do

Three offline score-controlled backends are installed:

- `zh`: ESPnet OpenCpop VISinger, one Chinese character per note;
- `en`: SoulX-Singer, one English word or sung syllable token per note;
- `ja`: ESPnet Kiritan VISinger, one hiragana/katakana mora per note.

All receive the same musical inputs:

- a lyric token;
- a MIDI pitch such as `F#4`;
- a duration in beats.

The renderer performs language-specific pronunciation conversion, places phrases at absolute `start_beat` offsets, creates `stems/vocal.wav`, and mixes `output/vocal_mix.wav`. English phrases are batched under one model load. Japanese 24 kHz synthesis is automatically resampled into the project's 44.1 kHz mix. Nothing uses a cloud API or spoken TTS.

## Decide whether vocals belong

Create vocals when the user asks for a song with a singer, lyrics, topline, demo vocal, verse/chorus vocal, or a complete pop song. Do not create them for BGM, underscore, soundtrack cues, instrumental studies, karaoke/backing tracks, or ambiguous requests.

Even a vocal project keeps both deliverables:

- `output/mix.wav`: instrumental version;
- `output/vocal_mix.wav`: instrumental plus synthesized lead vocal.

## Write the vocal part

Start from the song form and harmonic rhythm. Draft a melodic topline before finalizing lyrics, then revise melody and words together so important stressed syllables or morae land on musically important beats. Use rests between clauses. Avoid making every syllable the same duration.

Useful starting range for these voices is roughly B3–E5. Treat 2–8 seconds as a practical phrase length; split at breaths and section boundaries. Verify occasional notes outside the central register by listening.

`start_beat` is zero-based absolute beat position from the song start. At 4/4, bar 2 begins at beat 4 and bar 5 begins at beat 16. `duration` is measured in quarter-note beats.

## Schema

Copy `config/vocals.example.json`, `config/vocals.en.example.json`, or `config/vocals.ja.example.json` into the song directory as `vocals.json` and replace the example notes. Mandarin example:

```json
{
  "enabled": true,
  "language": "zh",
  "engine": "espnet_opencpop_visinger",
  "device": "cuda",
  "mix": { "volume_db": -2.0, "pan": 0.0, "mute": false },
  "phrases": [
    {
      "start_beat": 16,
      "notes": [
        { "lyric": "风", "pitch": "E4", "duration": 1.0 },
        { "lyric": "吹", "pitch": "F#4", "duration": 1.0 },
        { "lyric": "过", "pitch": "A4", "duration": 2.0 }
      ]
    }
  ]
}
```

Each lyric must be exactly one Chinese character. When automatic pronunciation is wrong, add an explicit OpenCpop phone list:

```json
{ "lyric": "行", "pitch": "E4", "duration": 1.0, "phonemes": ["x", "ing"] }
```

English uses `"language": "en"` and `"engine": "soulx_singer"`. A multi-note word may be marked with joined tokens such as `"Cof-"`, `"-fee"`; pronunciation is resolved from the complete word. Use `phoneme` with SoulX ARPAbet (for example `"en_L-AY1-T"`) only when the automatic pronunciation needs correction.

Japanese uses `"language": "ja"` and `"engine": "espnet_kiritan_visinger"`. Hiragana and katakana are converted locally; contracted or unusual readings can provide `phonemes`, for example `{ "lyric": "ょ", "pitch": "E4", "duration": 1.0, "phonemes": ["ky", "o"] }`.

## Render and validate

Render everything in one command:

```powershell
.\.venv\Scripts\python.exe scripts\render_song.py <song> --with-vocals
```

Or keep an existing instrumental and render only the vocal layer plus vocal mix:

```powershell
.\.venv\Scripts\python.exe scripts\render_vocals.py <song>
```

Acceptance checks:

- `stems/vocal.wav` is non-silent and 44.1 kHz PCM;
- lyric characters are intelligible enough to identify, especially phrase openings;
- sung pitches follow the intended contour and sit in the harmony;
- phrase starts align with `start_beat` and do not drift across the section;
- breaths and gaps sound intentional;
- `output/vocal_mix.wav` does not clip and the vocal is neither buried nor detached from the accompaniment;
- `output/mix.wav` still exists as the no-vocal version.

Run the automated file, clipping, duration, and pitch-presence checks with:

```powershell
.\.venv\Scripts\python.exe scripts\validate_vocals.py <song>
```

Revise `vocals.json` rather than processing the WAV destructively. Change pitch/duration/phrase segmentation for musical problems and `mix.volume_db` for balance problems.

## Current boundary

The installed backends provide one default local voice path per supported language, not a catalog of real singers. Voice cloning, a named real singer, additional characters, or another language requires another explicitly licensed compatible model. Do not imply that a synthesized voice is a real person. Model attribution and license information are recorded in `licenses/THIRD-PARTY.md`.
