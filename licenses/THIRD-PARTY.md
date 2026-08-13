# Third-party assets and tools

## FluidSynth

- Upstream: https://github.com/FluidSynth/fluidsynth
- Installed build: 2.5.7, official Windows x64 cpp11 release archive
- License: GNU Lesser General Public License (LGPL); see the upstream distribution in `tools/fluidsynth/`.
- The binary is downloaded by `scripts/setup_assets.py` and excluded from this project's Git history.

## GeneralUser GS

- Upstream: https://github.com/mrbumpy409/GeneralUser-GS
- Purpose: General MIDI / GS SoundFont used by FluidSynth
- License copy: `licenses/GeneralUser-GS-LICENSE.txt`
- The SoundFont permits use in music creation and software projects under its included license. Review that license before redistribution.
- The `.sf2` is downloaded from upstream by `scripts/setup_assets.py` and excluded from this project's Git history.

## ESPnet OpenCpop VISinger (optional vocal backend)

- Model: `espnet/opencpop_visinger` on Hugging Face.
- Purpose: optional local Mandarin singing-voice synthesis from lyrics, pitch, and duration.
- Model card license: Creative Commons Attribution 4.0 (`CC BY 4.0`).
- Required attribution/source: https://huggingface.co/espnet/opencpop_visinger
- ESPnet source code is Apache License 2.0: https://github.com/espnet/espnet
- The checkpoint is stored under `assets/vocals/` and excluded from Git because it is about 411 MiB.
- Generated vocals are optional; instrumental projects do not load this model or its Python environment.

## SoulX-Singer (optional English vocal backend)

- Upstream: https://github.com/Soul-AILab/SoulX-Singer
- Model: https://huggingface.co/Soul-AILab/SoulX-Singer
- Purpose: optional local English score-controlled singing synthesis.
- Source revision copied into `tools/soulx-singer/`: `81aeb3ae772c70093c3de74dc23c92d983801ae4`.
- Upstream repository and model card declare Apache License 2.0 for code and model weights.
- The 2.8 GB checkpoint is stored under `assets/vocals/soulx-singer/` and excluded from Git.
- The included anonymous English prompt in the upstream example is used as the default timbre prompt; this project does not clone a named real person.

## ESPnet Kiritan VISinger (optional Japanese vocal backend)

- Model: `espnet/kiritan_svs_visinger` on Hugging Face.
- Purpose: optional local Japanese singing synthesis from kana, pitch, and duration.
- Model card license: Creative Commons Attribution 4.0 (`CC BY 4.0`).
- Required attribution/source: https://huggingface.co/espnet/kiritan_svs_visinger
- ESPnet source code is Apache License 2.0: https://github.com/espnet/espnet
- The selected VISinger checkpoint is stored under `assets/vocals/` and excluded from Git.
