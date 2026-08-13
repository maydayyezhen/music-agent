from __future__ import annotations

import re

from g2p_en import G2p

from .score import pitch_to_midi


_G2P = G2p()


def word_to_soulx_phoneme(token: str) -> str:
    override = re.fullmatch(r"(.+)\[([A-Za-z0-9 -]+)\]", token)
    if override:
        phones = override.group(2).upper().split()
    else:
        # A score may mark sung syllables as ``Cof-`` / ``-fee``.  The hyphen
        # describes word joining; it is not part of the text sent to G2P.
        spoken = token.strip("-")
        phones = [phone for phone in _G2P(spoken) if re.fullmatch(r"[A-Z]+[0-2]?", phone)]
    if not phones:
        raise ValueError(f"cannot convert English lyric token to ARPAbet: {token!r}")
    return "en_" + "-".join(phones)


def _joined_syllable_phones(notes: list[dict]) -> list[str]:
    """Resolve hyphen-joined score tokens from the pronunciation of the full word.

    G2P on ``Cof`` and ``fee`` independently duplicates the /f/.  Looking up
    ``coffee`` once and splitting at vowel nuclei produces ``K AO`` / ``F IY``.
    """
    resolved: list[str] = [""] * len(notes)
    index = 0
    while index < len(notes):
        token = str(notes[index]["lyric"])
        if token.endswith("-") and "phoneme" not in notes[index]:
            end = index + 1
            while end < len(notes) and str(notes[end]["lyric"]).startswith("-"):
                last = str(notes[end]["lyric"])
                end += 1
                if not last.endswith("-"):
                    break
            parts = [str(notes[pos]["lyric"]).strip("-") for pos in range(index, end)]
            full_word = "".join(parts)
            phones = [phone for phone in _G2P(full_word) if re.fullmatch(r"[A-Z]+[0-2]?", phone)]
            vowel_positions = [pos for pos, phone in enumerate(phones) if re.search(r"[0-2]$", phone)]
            if len(vowel_positions) >= len(parts):
                boundaries = [0] + [vowel_positions[n] for n in range(1, len(parts))] + [len(phones)]
                for part_index, pos in enumerate(range(index, end)):
                    chunk = phones[boundaries[part_index]:boundaries[part_index + 1]]
                    resolved[pos] = "en_" + "-".join(chunk)
                index = end
                continue
        resolved[index] = str(notes[index].get("phoneme") or word_to_soulx_phoneme(token))
        index += 1
    return resolved


def build_soulx_metadata(phrase: dict, tempo: float, index: int) -> dict:
    seconds_per_beat = 60.0 / tempo
    durations = [0.16]
    text = ["<SP>"]
    phonemes = ["<SP>"]
    pitches = [0]
    types = [1]
    resolved_phonemes = _joined_syllable_phones(phrase["notes"])
    for note, resolved_phoneme in zip(phrase["notes"], resolved_phonemes):
        durations.append(float(note["duration"]) * seconds_per_beat)
        text.append(str(note["lyric"]))
        phonemes.append(resolved_phoneme)
        pitches.append(pitch_to_midi(note["pitch"]))
        types.append(int(note.get("note_type", 2)))
    total = sum(durations)
    return {
        "index": f"english_phrase_{index:03d}",
        "language": "English",
        "time": [0, round(total * 1000)],
        "duration": " ".join(f"{value:.4f}" for value in durations),
        "text": " ".join(text),
        "phoneme": " ".join(phonemes),
        "note_pitch": " ".join(str(value) for value in pitches),
        "note_type": " ".join(str(value) for value in types),
        "f0": "",
    }
