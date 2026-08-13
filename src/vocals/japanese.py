from __future__ import annotations

from typing import Any

from .score import PhraseScore, pitch_to_midi


# Phones used by espnet/kiritan_svs_visinger.  This deliberately covers the
# ordinary one-kana-per-note score format; contracted sounds can use the
# per-note ``phonemes`` override.
KANA_PHONES = {
    "あ": ["a"], "い": ["i"], "う": ["u"], "え": ["e"], "お": ["o"],
    "か": ["k", "a"], "き": ["k", "i"], "く": ["k", "u"], "け": ["k", "e"], "こ": ["k", "o"],
    "が": ["g", "a"], "ぎ": ["g", "i"], "ぐ": ["g", "u"], "げ": ["g", "e"], "ご": ["g", "o"],
    "さ": ["s", "a"], "し": ["sh", "i"], "す": ["s", "u"], "せ": ["s", "e"], "そ": ["s", "o"],
    "ざ": ["z", "a"], "じ": ["j", "i"], "ず": ["z", "u"], "ぜ": ["z", "e"], "ぞ": ["z", "o"],
    "た": ["t", "a"], "ち": ["ch", "i"], "つ": ["ts", "u"], "て": ["t", "e"], "と": ["t", "o"],
    "だ": ["d", "a"], "ぢ": ["j", "i"], "づ": ["z", "u"], "で": ["d", "e"], "ど": ["d", "o"],
    "な": ["n", "a"], "に": ["n", "i"], "ぬ": ["n", "u"], "ね": ["n", "e"], "の": ["n", "o"],
    "は": ["h", "a"], "ひ": ["h", "i"], "ふ": ["f", "u"], "へ": ["h", "e"], "ほ": ["h", "o"],
    "ば": ["b", "a"], "び": ["b", "i"], "ぶ": ["b", "u"], "べ": ["b", "e"], "ぼ": ["b", "o"],
    "ぱ": ["p", "a"], "ぴ": ["p", "i"], "ぷ": ["p", "u"], "ぺ": ["p", "e"], "ぽ": ["p", "o"],
    "ま": ["m", "a"], "み": ["m", "i"], "む": ["m", "u"], "め": ["m", "e"], "も": ["m", "o"],
    "や": ["y", "a"], "ゆ": ["y", "u"], "よ": ["y", "o"],
    "ら": ["r", "a"], "り": ["r", "i"], "る": ["r", "u"], "れ": ["r", "e"], "ろ": ["r", "o"],
    "わ": ["w", "a"], "を": ["o"], "ん": ["N"], "っ": ["cl"],
}
VALID_JA_PHONES = {
    "a", "i", "u", "e", "o", "k", "n", "r", "t", "m", "d", "s", "N",
    "sh", "g", "y", "b", "w", "cl", "ts", "z", "ch", "j", "h", "f", "p",
    "ky", "ry", "hy", "py",
}


def _katakana_to_hiragana(text: str) -> str:
    return "".join(chr(ord(ch) - 0x60) if "ァ" <= ch <= "ヶ" else ch for ch in text)


def kana_to_phones(kana: str) -> list[str]:
    normalized = _katakana_to_hiragana(kana)
    if normalized not in KANA_PHONES:
        raise ValueError(
            f"cannot map Japanese lyric {kana!r}; add a phonemes override, "
            "for example ['ky', 'o']"
        )
    return KANA_PHONES[normalized]


def build_japanese_phrase_score(phrase: dict[str, Any], tempo: float) -> PhraseScore:
    seconds_per_beat = 60.0 / tempo
    phone_times: list[tuple[float, float]] = []
    phones: list[str] = []
    notes: list[list[Any]] = []
    cursor = 0.0
    for note in phrase["notes"]:
        written_duration = float(note["duration"]) * seconds_per_beat
        duration = max(0.08, written_duration - min(0.04, written_duration * 0.08))
        start, end = cursor, cursor + duration
        note_phones = note.get("phonemes") or kana_to_phones(str(note["lyric"]))
        if not isinstance(note_phones, list) or not 1 <= len(note_phones) <= 4:
            raise ValueError("Japanese phonemes override must contain 1 to 4 phones")
        unknown = [phone for phone in note_phones if phone not in VALID_JA_PHONES]
        if unknown:
            raise ValueError(f"unsupported Kiritan phones: {unknown}")
        if len(note_phones) == 1:
            boundaries = [start, end]
        else:
            ratios = {2: [0.25, 1.0], 3: [0.10, 0.50, 1.0], 4: [0.05, 0.10, 0.50, 1.0]}[len(note_phones)]
            boundaries = [start] + [start + duration * ratio for ratio in ratios]
        phone_times.extend(zip(boundaries[:-1], boundaries[1:]))
        phones.extend(note_phones)
        notes.append([start, end, str(note["lyric"]), pitch_to_midi(note["pitch"]), "_".join(note_phones)])
        cursor += written_duration
    return PhraseScore(
        offset_seconds=float(phrase["start_beat"]) * seconds_per_beat,
        phone_times=phone_times,
        phones=phones,
        notes=notes,
    )
