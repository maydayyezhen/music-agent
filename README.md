# Music Agent

纯本地、可由 Agent 长期修改的结构化音乐工程：

```text
composition.json -> standalone MIDI tracks -> FluidSynth/SF2 -> WAV stems -> stereo mix.wav
```

没有 Web、云服务、DAW 或 VST 依赖。作曲、音色映射、渲染和混音相互解耦。

可选的人声层同样完全本地，支持中文、英文、日文：只有歌曲目录明确存在 `vocals.json` 且命令加入 `--with-vocals` 时，才会加载对应歌声模型。普通配乐、BGM 和纯音乐仍走原来的轻量伴奏流程。

## 现在就听 Demo

本机已经建好项目专用 Python 3.11 环境，并下载了渲染资产。在 PowerShell 中运行：

```powershell
cd D:\music-agent
.\.venv\Scripts\python.exe scripts\doctor.py
.\.venv\Scripts\python.exe scripts\render_song.py demo_song
```

完成后播放：

```text
D:\music-agent\projects\demo_song\output\mix.wav
```

Demo 名为 **Aozora Signal**：A major、120 BPM、32 小节、约 66 秒，结构为 Intro / Verse / Pre-Chorus / Chorus。

## 常用 Agent 工作流

只修改某轨的作曲内容后，只重渲该轨，再重新混音：

```powershell
.\.venv\Scripts\python.exe scripts\render_track.py demo_song bass
.\.venv\Scripts\python.exe scripts\mix_song.py demo_song
```

换 Guitar 音色时只修改 `config/instruments.json`，然后用相同的两条命令重渲 `guitar` 和混音。混音音量、声像、静音只改 `config/render.json`，随后只运行 `mix_song.py`。

## 第一次在另一台 Windows 机器安装

```powershell
cd D:\music-agent
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\setup_assets.py
.\.venv\Scripts\python.exe scripts\doctor.py
```

`setup_assets.py` 自动下载：

- FluidSynth 2.5.7 官方 Windows x64 便携版到 `tools/fluidsynth/`。
- GeneralUser GS 2.x 完整 GM/GS SoundFont 到 `assets/soundfonts/`。
- GeneralUser GS 的上游许可证到 `licenses/`。

两份大型二进制默认不提交 Git；在新机器执行一次脚本即可恢复。也可用环境变量 `MUSIC_AGENT_FLUIDSYNTH` 指定已有的 `fluidsynth.exe`。

## 作曲数据

`projects/demo_song/composition.json` 是 Agent 主要编辑入口。每轨按乐段保存短循环，避免复制几十遍：

```json
{
  "type": "note",
  "pitch": "C#4",
  "at": "1:2.5",
  "duration": 0.5,
  "velocity": 84
}
```

- `at` 是 `小节:拍`，从 `1:1` 开始，支持小数拍。
- `duration` 以拍为单位。
- `note` 使用 `pitch`；`chord` 使用 `pitches` 数组。
- `drum` 使用 GM 鼓名（如 `kick`、`snare`、`closed_hat`、`high_tom`）或 MIDI note number。
- `rest` 可用于明确表达留白；没有事件的区域天然也是休止。
- `loop_bars` 表示这一小段在所属 section 内循环多少小节。

例如“把 chorus 的 bass 写得活一点”只需编辑：

```text
tracks.bass.sections.chorus
```

### 可控音乐复杂度

`composition.json` 可选用五档复杂度：`minimal`、`simple`、`standard`、
`rich`、`dense`。旧曲不写该字段时按 `standard` 理解，但原有音符与渲染
不会被改写。

```json
"complexity": {
  "level": "rich",
  "rhythm": 4,
  "harmony": 4,
  "arrangement": 4,
  "melodic_ornamentation": 3,
  "density": 3,
  "variation": 4
},
"complexity_contour": "verse_chorus"
```

每个 section 可以覆盖复杂度，并通过 `complexity_budget` 把注意力分给
lead、drums、bass 等角色。节奏模板可放在顶层 `rhythm_motifs`，clip 用
`rhythm_motif` 与 `rhythm_variation` 标注 A/A'/B 关系。完整规则见
`references/music-complexity.md`。

分析一首曲子的节奏、留白、密度与多轨重叠：

```powershell
.\.venv\Scripts\python.exe scripts\critic_complexity.py <song> --write
```

报告保存为 `projects/<song>/complexity-report.json`。Critic 只提出上下文
相关警告，不会自动把作品写得更密。

## 音色与混音

`config/instruments.json` 使用 MIDI 标准的 **0-based program number**：

| Track | GM program | GeneralUser GS preset |
|---|---:|---|
| piano | 0 | Acoustic Grand Piano |
| bass | 33 | Electric Bass (finger) |
| guitar | 29 | Overdriven Guitar |
| strings | 48 | String Ensemble 1 |
| pad | 89 | Pad 2 (warm) |
| drums | channel 10 | Standard Drum Kit |

`config/render.json` 保存 sample rate、SoundFont 路径，以及每轨的 `volume_db`、`pan`（-1 左至 +1 右）和 `mute`。

完整的 GeneralUser GS 预设（包含隐藏 GS bank 和鼓组）记录在 `config/soundfont-catalog.json`，使用说明见 `references/soundfont-catalog.md`。除了全局默认值，每条 FluidSynth 轨道也可以覆盖自己的 SoundFont：

```json
"choir": {
  "engine": "fluidsynth",
  "soundfont": "assets/soundfonts/special-choir.sf2",
  "bank": 0,
  "program": 0
}
```

未填写 `soundfont` 时仍使用 `render.json` 的全局 SoundFont，因此旧项目不需要迁移。鼓组用 `channel: 10`、bank 128（或 120）和目录中列出的 program 选择；例如 program 40 是 Brush Kit。

一首歌如果需要不同轨道名或独立音色/混音，可在该歌曲目录放置自己的 `instruments.json` 和 `render.json`。渲染脚本会优先读取歌曲本地配置，没有时才使用 `config/` 下的共享默认值。

## 输出结构

```text
projects/demo_song/
├─ composition.json
├─ tracks/
│  ├─ piano.mid ... drums.mid
├─ stems/
│  ├─ piano.wav ... drums.wav
└─ output/
   ├─ full_song.mid
   └─ mix.wav
```

## SFZ 升级接口

渲染入口已经按 `engine` 路由。未来可以把单个映射改为：

```json
{
  "guitar": {
    "engine": "sfizz",
    "sfz": "assets/sfz/guitar/distortion_guitar.sfz"
  }
}
```

`doctor.py` 会探测 `sfizz_render` / `sfizz-render`。当前第一阶段未安装 sfizz，FluidSynth 全链路不受影响；实际启用 SFZ 前需要按所安装 sfizz 版本完成 CLI 适配。最值得优先替换的是 **Overdriven Guitar**，其次是强调真实演奏法时的 Strings。

## 模块边界

- `src/composition/`：加载与校验 Agent 友好数据。
- `src/midi/`：事件展开、音高解析、standalone/full MIDI 生成。
- `src/render/`：FluidSynth 封装、SFZ 路由、WAV 尾音裁切。
- `src/mixer/`：稳定的 16-bit PCM stem 读取、音量、等功率声像、峰值保护。
- `scripts/`：供人和 Agent 调用的窄命令入口。

工程刻意不包含 Web UI、DAW 控制、VST 自动化和复杂 mastering。

## 可选中文歌声

本机已经安装独立的 `.venv-vocals`、CUDA 12.8 PyTorch，以及中文 OpenCpop VISinger、英文 SoulX-Singer、日文 Kiritan VISinger。人声环境与 MIDI/FluidSynth 主环境隔离，不会改变纯音乐渲染。

要给一首歌加人声，将中文、英文或日文示例（`config/vocals.example.json`、`config/vocals.en.example.json`、`config/vocals.ja.example.json`）复制为 `projects/<song>/vocals.json`，写入歌词、音高和时值，然后运行：

```powershell
.\.venv\Scripts\python.exe scripts\render_song.py <song> --with-vocals
```

已有伴奏时只生成人声和人声版混音：

```powershell
.\.venv\Scripts\python.exe scripts\render_vocals.py <song>
.\.venv\Scripts\python.exe scripts\validate_vocals.py <song>
```

输出同时保留：

```text
output/mix.wav        # 纯伴奏
stems/vocal.wav       # 独立干声
output/vocal_mix.wav  # 人声 + 伴奏
```

当前支持 `zh`、`en`、`ja` 三种本地歌声路径，但不提供真人克隆或指定现实歌手。详细写法、发音覆盖和验收项见 `references/vocal-workflow.md`；各模型归属和许可证见 `licenses/THIRD-PARTY.md`。在另一台兼容 NVIDIA GPU 的 Windows 机器可运行 `powershell -ExecutionPolicy Bypass -File scripts/setup_vocals.ps1` 恢复可选人声环境。

## Composition Knowledge Layer

项目级作曲工作流由 `AGENTS.md` 约束。新曲或大规模重写前先读：

```text
references/composition-guidelines.md
```

首次完整渲染后必须使用 `references/composer-checklist.md` 自查，把问题写进歌曲目录的 `critique.md`，保留 `composition_v1.json`，至少生成并渲染一个后续版本。三个上游参考仓库原样保存在 `references/`，来源与固定 revision 见 `references/SOURCES.md`；它们只是项目内教材，不是已安装 Skill。

当前 A/B：

```text
projects/old_demo/output/mix.wav
projects/knowledge_demo/output/mix.wav
```

详细决策对比见 `projects/knowledge_demo/ab-comparison.md`。
