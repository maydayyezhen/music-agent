from __future__ import annotations

import json
import shutil
import subprocess
import sys

from _bootstrap import ROOT

PROJECT = ROOT / "projects" / "instrument_aware_full_song"
SECTIONS = [
    ("intro", 8, 0.34), ("verse", 16, 0.48), ("chorus", 16, 0.78),
    ("bridge", 16, 0.58), ("final_chorus", 16, 0.92), ("outro", 8, 0.38),
]
CHORDS = {
    "intro": ["Em", "C", "G", "D", "Em", "C", "D", "D"],
    "verse": ["Em", "C", "G", "D"] * 4,
    "chorus": ["C", "G", "D", "Em"] * 4,
    "bridge": ["Am", "C", "Em", "D"] * 4,
    "final_chorus": ["C", "G", "D", "Em"] * 3 + ["C", "D", "Em", "Em"],
    "outro": ["Em", "C", "G", "D", "Em", "C", "Em", "Em"],
}


def harmony(name: str) -> list[dict[str, object]]:
    return [{"at": f"{index + 1}:1", "duration": 4, "chord": chord} for index, chord in enumerate(CHORDS[name])]


def phrase(instrument: str, role: str, phrase_type: str, energy: float, seed: int, **extra: object) -> dict[str, object]:
    return {"instrument": instrument, "role": role, "phrase_type": phrase_type, "energy": energy,
            "performance_intent": {"attack": "section_shaped", "release": "phrase_shaped",
                                   "humanization": "action_based", "seed": seed}, **extra}


def clip(data: dict[str, object], bars: int) -> dict[str, object]:
    return {"loop_bars": bars, "sound_library_profile": "general_midi", "instrument_phrase": data}


def lead_motif(name: str, energy: float) -> list[dict[str, object]]:
    bars = dict((section, count) for section, count, _ in SECTIONS)[name]
    base = ["E4", "G4", "B4", "A4", "G4", "D5", "B4", "E5"]
    if name in {"chorus", "final_chorus"}:
        base = ["G4", "B4", "E5", "D5", "B4", "D5", "E5", "G5"]
    if name == "outro":
        base = ["E4", "G4", "B4", "E5"]
    result = []
    phrase_starts = list(range(1, bars + 1, 4))
    for phrase_index, bar in enumerate(phrase_starts):
        pitches = base if phrase_index % 2 == 0 else base[2:] + base[:2]
        count = 6 if phrase_index % 3 != 2 else 5
        for note_index, pitch in enumerate(pitches[:count]):
            local = note_index * (0.5 if phrase_index % 2 == 0 else 0.75)
            at_bar = bar + int(local // 4)
            beat = local % 4 + 1
            if at_bar > bars:
                break
            arts = ["sustain"]
            if note_index == 1:
                arts = ["hammer_on", "legato"]
            elif note_index == 3:
                arts = ["slide", "legato"]
            elif note_index == 5:
                arts = ["bend", "vibrato"] if name in {"chorus", "final_chorus"} else ["sustain", "vibrato"]
            item = {"at": f"{at_bar}:{beat:g}", "pitch": pitch, "duration": 0.42 if note_index < 5 else 1.3,
                    "articulations": arts}
            if "bend" in arts:
                item["bend_semitones"] = 2
            result.append(item)
    return result


def build() -> dict[str, object]:
    sections = [{"name": name, "bars": bars, "complexity": "rich" if energy > 0.7 else "standard",
                 "complexity_budget": {"lead": 2, "drums": 2, "bass": 2, "chords": 2}}
                for name, bars, energy in SECTIONS]
    tracks: dict[str, object] = {
        "rhythm_guitar": {"role": "electric rhythm guitar", "sections": {}},
        "lead_guitar": {"role": "electric lead guitar main melody", "sections": {}},
        "bass": {"role": "electric bass", "sections": {}},
        "drums": {"role": "drum kit", "sections": {}},
        "organ": {"role": "organ harmonic line", "sections": {}},
        "strings": {"role": "string ensemble plane", "sections": {}},
    }
    for section_index, (name, bars, energy) in enumerate(SECTIONS):
        guitar_type = "open_power_chords" if name in {"intro", "chorus", "final_chorus", "outro"} else "palm_muted_eighths"
        tracks["rhythm_guitar"]["sections"][name] = clip(phrase(
            "electric_rhythm_guitar", "rhythm", guitar_type, energy, 200 + section_index,
            harmony=harmony(name), subdivision=1.0 if guitar_type == "open_power_chords" else 0.5,
            gate=0.8 if guitar_type == "open_power_chords" else 0.42,
            strum_spread=0.07 if guitar_type == "open_power_chords" else 0.045,
            rest_steps=[index for index in range(bars * (4 if guitar_type == "open_power_chords" else 8))
                        if index % (4 if guitar_type == "open_power_chords" else 8) == 3],
            articulations=["sustain", "accent"] if guitar_type == "open_power_chords" else ["palm_mute"]), bars)
        if name != "bridge":
            tracks["lead_guitar"]["sections"][name] = clip(phrase(
                "electric_lead_guitar", "lead", "melodic_lead", energy, 220 + section_index,
                motif=lead_motif(name, energy)), bars)
        tracks["bass"]["sections"][name] = clip(phrase(
            "electric_bass", "bass", "kick_locked_line", min(1, energy + 0.05), 240 + section_index,
            harmony=harmony(name), kick_offsets=[0, 2], articulations=["finger"]), bars)
        tracks["drums"]["sections"][name] = clip(phrase(
            "drum_kit", "drums", "chorus_with_fill" if name in {"chorus", "final_chorus"} else "rock_verse",
            energy, 260 + section_index, bars=bars, transition_fill=name not in {"intro", "outro"}), bars)
        tracks["organ"]["sections"][name] = clip(phrase(
            "organ", "harmony", "organ_voice_led_chords", max(0.25, energy - 0.12), 280 + section_index,
            harmony=harmony(name), register_midi=[57, 79], voices=3, pedal=False,
            articulations=["legato"]), bars)
        if name in {"chorus", "bridge", "final_chorus", "outro"}:
            tracks["strings"]["sections"][name] = clip(phrase(
                "strings", "plane", "long_tones_inner_movement", max(0.3, energy - 0.08), 300 + section_index,
                harmony=harmony(name), register_midi=[60, 84], voices=3,
                articulations=["sustain", "legato"]), bars)
    return {"metadata": {"title": "Hands Before Notes", "tempo": 104, "time_signature": "4/4", "key": "E minor"},
            "complexity": "rich", "complexity_contour": "custom", "sections": sections, "tracks": tracks}


def main() -> int:
    PROJECT.mkdir(parents=True, exist_ok=True)
    composition = build()
    (PROJECT / "composition.json").write_text(json.dumps(composition, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    instruments = {
        "rhythm_guitar": {"engine": "fluidsynth", "bank": 0, "program": 29},
        "lead_guitar": {"engine": "fluidsynth", "bank": 0, "program": 30},
        "bass": {"engine": "fluidsynth", "bank": 0, "program": 33},
        "drums": {"engine": "fluidsynth", "channel": 10, "bank": 128, "program": 16},
        "organ": {"engine": "fluidsynth", "bank": 0, "program": 18},
        "strings": {"engine": "fluidsynth", "bank": 8, "program": 48},
    }
    render = {"sample_rate": 44100, "soundfont": "assets/soundfonts/GeneralUser-GS.sf2", "fluidsynth_gain": 0.75,
              "tail_seconds": 3, "master_peak_db": -1,
              "mix": {
                  "rhythm_guitar": {"volume_db": -5, "pan": -0.38, "mute": False},
                  "lead_guitar": {"volume_db": -3, "pan": 0.18, "mute": False},
                  "bass": {"volume_db": -4, "pan": 0, "mute": False},
                  "drums": {"volume_db": -8, "pan": 0, "mute": False},
                  "organ": {"volume_db": -8, "pan": 0.32, "mute": False},
                  "strings": {"volume_db": -10, "pan": 0.08, "mute": False},
              }}
    (PROJECT / "instruments.json").write_text(json.dumps(instruments, indent=2) + "\n", encoding="utf-8")
    (PROJECT / "render.json").write_text(json.dumps(render, indent=2) + "\n", encoding="utf-8")
    (PROJECT / "README.md").write_text(
        "# Hands Before Notes\n\nA complete 80-bar integration song in which all six tracks are compiled from instrument-aware semantic phrases. The bridge deliberately removes lead guitar so bass, rhythm guitar, organ, strings and drums carry the transition.\n",
        encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "render_song.py"), "instrument_aware_full_song"], cwd=ROOT)
    if result.returncode:
        return result.returncode
    shutil.copy2(PROJECT / "output" / "mix.wav", PROJECT / "output" / "final.wav")
    for script in ("critic_instruments.py", "critic_complexity.py", "critic_continuity.py"):
        completed = subprocess.run([sys.executable, str(ROOT / "scripts" / script), "instrument_aware_full_song", "--write"], cwd=ROOT)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
