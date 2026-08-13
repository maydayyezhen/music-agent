from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pypinyin import Style, pinyin


NOTE_NAMES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
VALID_PHONES = {
    "SP", "AP", "i", "e", "y", "d", "w", "sh", "ai", "n", "x", "j", "ian",
    "u", "l", "h", "b", "o", "zh", "an", "ou", "m", "q", "z", "en", "g", "ing",
    "ei", "ao", "ang", "uo", "eng", "t", "a", "ong", "ui", "k", "f", "r", "iang",
    "ch", "v", "in", "iao", "ie", "iu", "c", "s", "van", "p", "ve", "uan", "uang",
    "ia", "ua", "uai", "un", "er", "vn", "iong",
}


@dataclass(frozen=True)
class PhraseScore:
    offset_seconds: float
    phone_times: list[tuple[float, float]]
    phones: list[str]
    notes: list[list[Any]]

    @property
    def duration_seconds(self) -> float:
        return self.notes[-1][1]


def pitch_to_midi(value: str | int) -> int:
    if isinstance(value, int):
        midi = value
    else:
        text = value.strip().upper()
        if len(text) < 2 or text[0] not in NOTE_NAMES:
            raise ValueError(f"invalid pitch: {value}")
        accidental = 0
        index = 1
        if text[index:index + 1] in ("#", "B"):
            accidental = 1 if text[index] == "#" else -1
            index += 1
        try:
            octave = int(text[index:])
        except ValueError as error:
            raise ValueError(f"invalid pitch: {value}") from error
        midi = (octave + 1) * 12 + NOTE_NAMES[text[0]] + accidental
    if not 0 <= midi <= 127:
        raise ValueError(f"MIDI pitch out of range: {value}")
    return midi


def hanzi_to_phones(character: str) -> list[str]:
    initial = pinyin(character, style=Style.INITIALS, strict=False)[0][0]
    final = pinyin(character, style=Style.FINALS, strict=False)[0][0]
    normal = pinyin(character, style=Style.NORMAL, strict=False)[0][0]
    # pypinyin writes y/w as pseudo-initials; OpenCpop models them as real phones.
    if not initial and normal in VALID_PHONES:
        phones = [normal]
    else:
        phones = [part for part in (initial, final) if part]
    aliases = {"ue": "ve"}
    phones = [aliases.get(phone, phone) for phone in phones]
    unknown = [phone for phone in phones if phone not in VALID_PHONES]
    if not phones or unknown:
        raise ValueError(
            f"cannot map lyric {character!r} to installed OpenCpop phones: {phones}; "
            "add a phonemes override such as ['sh', 'i']"
        )
    return phones


def build_phrase_score(phrase: dict[str, Any], tempo: float) -> PhraseScore:
    seconds_per_beat = 60.0 / tempo
    phone_times: list[tuple[float, float]] = []
    phones: list[str] = []
    notes: list[list[Any]] = []
    cursor = 0.0
    for note in phrase["notes"]:
        # A short gap keeps consonants intelligible and prevents phrase-internal
        # note boundaries from being glued into one continuous vowel.
        written_duration = float(note["duration"]) * seconds_per_beat
        duration = max(0.08, written_duration - min(0.04, written_duration * 0.08))
        start = cursor
        end = cursor + duration
        note_phones = note.get("phonemes") or hanzi_to_phones(str(note["lyric"]))
        if not isinstance(note_phones, list) or not 1 <= len(note_phones) <= 4:
            raise ValueError("phonemes override must contain 1 to 4 OpenCpop phones")
        if any(phone not in VALID_PHONES for phone in note_phones):
            raise ValueError(f"unsupported OpenCpop phones: {note_phones}")
        if len(note_phones) == 1:
            boundaries = [start, end]
        else:
            # OpenCpop's ruled segmentation leaves most time to the syllable final.
            ratios = {2: [0.25, 1.0], 3: [0.10, 0.50, 1.0], 4: [0.05, 0.10, 0.50, 1.0]}[len(note_phones)]
            boundaries = [start] + [start + duration * ratio for ratio in ratios]
        phone_times.extend(zip(boundaries[:-1], boundaries[1:]))
        phones.extend(note_phones)
        joined = "_".join(note_phones)
        notes.append([start, end, str(note["lyric"]), pitch_to_midi(note["pitch"]), joined])
        cursor += written_duration
    return PhraseScore(
        offset_seconds=float(phrase["start_beat"]) * seconds_per_beat,
        phone_times=phone_times,
        phones=phones,
        notes=notes,
    )
