from __future__ import annotations

from pathlib import Path
from typing import Any

from src.render.fluidsynth import render_midi as render_fluidsynth
from src.render.sfizz import render_midi_with_sfizz
from src.utils.paths import project_root


def render_midi(
    midi_path: Path,
    instrument: dict[str, Any],
    render_config: dict[str, Any],
    output_wav: Path,
) -> None:
    engine = instrument.get("engine", "fluidsynth")
    if engine == "fluidsynth":
        # A track may opt into a dedicated SoundFont. Existing projects keep
        # using render.json's global default when this field is absent.
        soundfont = (
            project_root() / instrument.get("soundfont", render_config["soundfont"])
        ).resolve()
        render_fluidsynth(
            midi_path,
            soundfont,
            output_wav,
            sample_rate=int(render_config.get("sample_rate", 44100)),
            gain=float(render_config.get("fluidsynth_gain", 0.7)),
        )
        return
    if engine == "sfizz":
        sfz_path = (project_root() / instrument["sfz"]).resolve()
        render_midi_with_sfizz(midi_path, sfz_path, output_wav, render_config)
        return
    raise ValueError(f"unknown rendering engine: {engine!r}")


def render_track(
    track_name: str,
    midi_path: Path,
    instruments: dict[str, Any],
    render_config: dict[str, Any],
    output_wav: Path,
) -> None:
    if track_name not in instruments:
        raise KeyError(f"instrument mapping is missing track '{track_name}'")
    render_midi(midi_path, instruments[track_name], render_config, output_wav)
