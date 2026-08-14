# Music Agent Project Checkpoint

更新时间：2026-08-14（Asia/Shanghai）  
仓库：`D:\music-agent`  
分支：`codex/accompaniment-continuity`  
基线提交：`bddd354 feat: add accompaniment texture continuity system`  
本文件描述其所在 checkpoint commit 的完整项目状态；渲染二进制仍按 `.gitignore` 排除。

## 1. 当前项目状态

Music Agent 已经是一个可在本机真实运行的结构化作曲、MIDI 生成、乐器语义编译、
SoundFont/SFZ 路由、分轨音频渲染、混音和可选 AI 歌声工程。主链路保持为：

```text
composition.json
  -> composition validation / semantic phrase compilation
  -> standalone track MIDI + full_song.mid
  -> FluidSynth or optional per-track renderer
  -> WAV stems
  -> stereo mix.wav
```

可选人声是与伴奏解耦的并行路径：

```text
vocals.json
  -> zh/en/ja local singing backend
  -> stems/vocal.wav
  -> output/vocal_mix.wav
```

不要求每首音乐都有人声。没有 `vocals.json` 或没有显式 `--with-vocals` 时，普通配乐、
BGM 和纯音乐不会加载歌声模型。

### 本机验证状态

- Python：3.11.9。
- 核心依赖：`mido`、`numpy` 可用。
- FluidSynth：可用，位于 `tools/fluidsynth/bin/fluidsynth.exe`（Git 忽略）。
- 默认 SoundFont：GeneralUser GS，约 30.8 MiB，位于 `assets/soundfonts/`（Git 忽略）。
- ffmpeg：可用。
- 可选歌声环境：CUDA 12.8 PyTorch 2.7.1，NVIDIA GeForce RTX 5060 Laptop GPU 可用。
- `scripts/doctor.py` 的真实 A4 MIDI 渲染、立体声音量/声像混音测试均通过。
- 单元/回归测试：`46/46` 通过。
- 唯一 doctor 警告：可选 SFZ 后端 `sfizz` 尚未安装；不影响 FluidSynth 主链路。

验证命令：

```powershell
.\.venv\Scripts\python.exe scripts\doctor.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 2. 已实现能力

### 2.1 结构化作曲与兼容性

- `composition.json` 定义 metadata、section、track、loop、音符/和弦/鼓事件。
- 支持 `小节:拍` 的位置表达和确定性 MIDI 展开。
- 旧式精确 `events` 路径保持可用；未启用新字段的旧作品不需要迁移。
- 新式 `instrument_phrase` 路径在作曲意图与最终 MIDI 之间保留乐器语义。
- composition、音色配置、渲染配置和混音参数保持解耦。
- schema/physical/MIDI 校验使用 error、warning、info 三级诊断。

### 2.2 Composition Knowledge Layer

- `AGENTS.md`、根 `SKILL.md` 和 `references/composer-checklist.md` 已形成 Agent 作曲流程。
- 新曲工作流覆盖 brief、结构、复杂度、energy map、节奏动机、旋律动机、和声、
  orchestration、真实 V1 渲染、量化 critique、实质 V2/final 修订和交付审计。
- 参考资料只作为项目内教材，不注册为全局 Skill，也不接入 Ableton/Suno/cloud。
- 作品可以纯器乐；只有用户明确要求歌词/演唱时才启用人声工作流。

### 2.3 可控复杂度系统

- 五档复杂度：`minimal`、`simple`、`standard`、`detailed`、`dense`。
- 支持全曲 profile、section contour、section override 和多维 complexity budget。
- 复杂度不只等于音符密度，还覆盖 rhythm、harmony、texture、variation、register 等维度。
- 提供 resolver、critic、demo 和自动化测试。

### 2.4 伴奏 Texture 与连续性

- 可执行 texture：`sustain`、`pulse`、`ostinato`、`broken_chord`、`arpeggio`、
  `riff`、`counterline`、`pad`。
- 支持 Point/Line/Plane 角色平衡、voice leading、common-tone retention、跨和弦轮廓连续。
- continuity critic 检查短音断裂、跳跃、全轨 Point 化、段落衔接与伴奏同质化。
- 旧 composition 在未声明 texture 时保持原路径和兼容性。

### 2.5 Instrument-aware Composition / Performance IR

已实现四层边界：

```text
musical intent
  -> instrument_phrase
  -> neutral performance events
  -> sound-library profile
  -> rendered MIDI events
```

当前乐器模块包括：

- Electric Guitar：rhythm、lead、palm mute、power chord、strum、riff、fret/string assignment。
- Electric Bass：指法/拨片语义、register、kick relation 和物理范围校验。
- Drums：groove、fill、limb assignment、hi-hat 状态与冲突检查。
- Keyboards：piano/organ 角色、voicing 和 voice leading。
- Strings/Pad：长线条、inner movement、register 与层次。

Performance profile 支持 articulation token 到 program、keyswitch、CC、pitch bend、gate/velocity
fallback 的映射；作曲模块不硬编码具体音源 keyswitch。

已存在 profile：

- `general_midi`
- `ample_guitar_v4`
- `shreddage_stratus_free`
- `sfizz`
- `custom_soundfonts`

其中 profile 表示语义映射能力，不等于对应插件宿主或采样库已经在渲染器中完整接通。

### 2.6 SoundFont 与本地渲染

- GeneralUser GS 完整 preset catalog 已建立，包含隐藏 GS bank、Choir/Voice/Vox 音色和鼓组。
- Choir/Voice/Vox 可作为普通乐器音色使用，但不能发音歌词。
- 每条 FluidSynth 轨道可覆盖独立 SoundFont；未覆盖时继续使用全局 SoundFont。
- 支持每轨音量、等功率声像、mute、stem 渲染、峰值保护和尾音裁切。
- `assets/` 与 `tools/` 不进 Git，可通过 setup 脚本恢复。
- 渲染路由已经预留 SFZ engine，但当前本机实际稳定主路径仍是 FluidSynth。

### 2.7 可选本地 AI 歌声

- 中文：OpenCpop VISinger 路径。
- 英文：SoulX-Singer 路径。
- 日文：Kiritan VISinger 路径。
- 独立 `.venv-vocals`，不污染 MIDI/FluidSynth 主环境。
- 支持歌词、逐音音高/时值、独立 vocal stem、伴奏版和 vocal mix 并存。
- 提供 zh/en/ja 示例配置、validator、setup 脚本和许可证说明。
- 不支持真人音色克隆，也不承诺复现某位现实歌手。

### 2.8 Long-Form Phrase Planning

- 保留 Section Arc、Phrase Relationship Graph、Persistent Melodic State 三层实验系统。
- 可分析 8–16 小节的 motif development、peak、cadence、reset、silence、register curve、
  cross-bar continuity。
- 经最小回退修正后，正式作品默认 `legacy_stable`。
- 只有显式 `long_form_experimental` 才启用实验 planner。
- 默认实验 realization 保持单声部，不自动添加 bend/vibrato/重叠 legato；跨小节音必须说明用途。
- MIDI exporter 会在同一 channel 存在其他重叠音时丢弃不安全的 channel-wide pitch bend。

### 2.9 电吉他原生主奏

- 已形成 `docs/guitar_native_lead_playbook.md`。
- 主奏从可演奏指板位置、手型、拨弦、slide、bend、release、sequence 和跨小节动作设计，
  而不是先写人声旋律再替换音色。
- 要求 lick 之间有共享音、slide/release、节奏延续、移位、压缩、扩张或轮廓延续。
- 验证作品 `projects/guitar_native_rock_proof/` 证明连续 guitar-native solo 路径可用。
- General MIDI 仍只是当前试听音色；真实吉他采样插件接入仍属于后续工作。

### 2.10 Acoustic / Electric Rhythm Guitar 持续扫弦

- 明确区分 `sustained_chord_hit` 与 `continuous_strumming`。
- 保留没有发声的 air stroke，不再只用发声音符反推右手动作。
- 旧八分网格继续兼容。
- 新十六分网格每小节保存 16 个交替 Down/Up 潜在动作。
- 动作支持 `full_strum`、`partial_strum`、`single_string_restrike`、`muted_strum`、
  `ghost_strum`、`air_strum`。
- 逐弦管理 active note state；partial stroke 只重新触发被扫到的琴弦。
- 未扫到的旧弦可以继续持续；换和弦只关闭音高/品位确实移动的弦。
- 防止同音 MIDI overlap、冲突 Note Off 和 stuck notes。
- 从一个基础骨架生成 A、A'、B、B' 四小节相关变奏，不逐小节随机换完全无关 pattern。
- 前景感知会在 Vocal/Main Melody/Lead/Hook 活跃时保持右手运动，仅轻降攻击密度与力度，
  减少 4–6 音完整扫弦，改用更薄的 partial/light/muted stroke；长音/换气处可短暂恢复。

十六小节验证结果：

- 潜在动作：旧路径每小节 8，新路径每小节 16。
- 新四小节实际攻击：12 / 12 / 13 / 11。
- 四小节独立相关变体：4。
- 逐弦阶段“上一次攻击仍有弦持续”比例：97.9%。
- 跨小节延音比例：100%。
- 前景活跃时平均攻击：12 -> 11。
- 前景活跃时平均 velocity：85.75 -> 76.12。
- 前景活跃时四音以上完整扫弦：12.5% -> 6.8%。
- 手部动作仍为每小节 16；长时间停手次数为 0。
- same-pitch overlap、unmatched Note Off、stuck notes 均为 0。

## 3. 代表性工程与验证资产

- `projects/instrument_aware_demos/`：七个最小乐器语义 Demo。
- `projects/instrument_aware_full_song/`：instrument-aware 完整作品验证。
- `projects/long_form_phrase_demos/`：Long-Form A/B 实验资产。
- `projects/guitar_native_rock_proof/`：电吉他原生主奏成功证明。
- `projects/strumming_continuity_demo/`：旧八分持续右手与多吉他独立 pattern 验证。
- `projects/sixteenth_strumming_demo/`：十六分、逐弦、四小节变奏、前景退让验证。
- `projects/church_choir_demo/`：Choir/Voice/Organ 作为器乐层的教堂合唱音色作品。
- `projects/electric_guitar_rock_epic/`：第一版长篇电吉他摇滚作品。
- `projects/electric_guitar_rock_long_form/`：Long-Form 实验依赖作品，不作为默认模板。
- `projects/electric_guitar_rock_stable_v2/`：稳定模式长篇电吉他摇滚作品。
- `projects/long_continuous_strum_song/`：长段持续扫弦验证作品。
- `projects/walk_me_to_the_streetlamp/`、`projects/next_stop_unnamed/`：Pop-Rock、歌词与吉他编曲工程。
- `projects/english_vocal_pop/`：英文歌曲、歌词/vocal score 和附属节奏游戏实验。

项目内 `.wav` 和 `.mid` 是可重复生成的渲染产物，默认不进 Git；相应 composition、brief、
critique、debug JSON、validation report 和生成脚本会进入版本控制。

## 4. 未完成问题与已知边界

### P0：远程备份与可恢复性

- 当前没有配置 Git remote，也没有 GitHub 仓库备份。
- 二进制依赖与音源不进 Git；新机器 clone 后必须运行 setup 脚本。
- 尚未在全新空目录执行一次“clone -> setup -> doctor -> tests -> render demo”的冷启动验收。

### P1：真实吉他音源接入

- 本机已有 Ample Guitar/Bass 安装包，但当前主渲染器没有 VST 宿主自动化。
- `ample_guitar_v4` profile 只提供语义映射边界，不代表已把 Ample 插件声音渲染进作品。
- sfizz 未安装，SFZ renderer CLI 的真实版本适配尚未完成。
- 当前 Electric Guitar 的可听结果主要来自 GeneralUser GS，因此演奏结构已进步，但音色真实度仍受限。

### P1：Long-Form 实验系统

- Long-Form planner 已保留但不是正式默认；它仍应被视为实验能力。
- 当前验收重点是稳定单声部 skeleton 和规划层，不是自动堆叠大量 articulation。
- 尚未把实验 planner 与 guitar-native 指板动作系统合并成一个经过完整作品验证的新默认实现。

### P1：持续扫弦推广

- 十六分逐弦引擎已经通过专用 16 小节测试，但现有历史歌曲不会自动迁移。
- 后续应挑一首独立新歌使用新语义重写 rhythm guitar，再做完整 2–3 分钟听感与结构验证。
- 前景识别目前依赖 track name/role 中的 Vocal、Lead Melody、Main Melody、Foreground、Hook 等语义；
  更复杂工程可能需要显式 foreground activity。

### P2：人声产品化

- zh/en/ja 后端可运行，但不同语言的 phoneme coverage、歌词自然度和模型音质仍需逐曲验收。
- 没有通用的自动作词 -> 自动 syllable alignment -> 生产级歌声一键流水线。
- 不支持真人克隆、指定现实歌手或商业云 API 后端。

### P2：工程化边界

- 当前刻意没有 Web UI、DAW 控制、VST 自动化和复杂 mastering。
- GitHub Actions/CI 尚未配置；测试只在本机 Windows 环境验证。
- `projects/` 中保留较多 composition revision 和审计 JSON，适合研究追溯，但后续可区分长期 fixture
  与个人作品档案，降低仓库体积。
- 当前没有稳定版本号、release manifest 或 changelog。

## 5. 下一步计划

1. 创建 GitHub 仓库并推送当前 checkpoint；默认优先使用 private，避免无意公开作品和本机路径信息。
2. 在临时目录做一次完整冷启动复现：clone、`setup_assets.py`、doctor、46 tests、渲染一个 Demo。
3. 为 GitHub 增加 Windows CI，至少执行 composition loader 和不依赖本机音源的单元测试。
4. 选择 Ample 或 sfizz 中一条最小真实吉他路径，先接一轨、一个 articulation、一个离线 render，
   再扩展 profile，不直接引入复杂 DAW 自动化。
5. 用全新 2–3 分钟作品验证十六分逐弦扫弦和 foreground thinning 的长时间听感。
6. 继续保持 `legacy_stable` 为正式 Lead 默认；只有在新的 guitar-native Long-Form A/B 明显胜出后再讨论升级。
7. 为 optional vocals 增加英文/日文各一首可重复的端到端 fixture 与自动 alignment 质量报告。
8. 整理 `projects/`：标记 regression fixtures、benchmark、作品档案和可删除的中间 revision。

## 6. 关键文件位置

### Agent 与项目入口

- `AGENTS.md`：项目最高层 Agent 规则和强制作曲流程。
- `SKILL.md`：项目本地能力路由与渐进阅读入口。
- `README.md`：安装、数据格式、运行、渲染和人声说明。
- `PROJECT_CHECKPOINT.md`：当前恢复点与后续路线。
- `references/composer-checklist.md`：V1 后的作曲/编曲/渲染审查表。

### 配置

- `config/instruments.json`：默认乐器映射。
- `config/render.json`：默认 SoundFont、sample rate、每轨混音配置。
- `config/soundfont-catalog.json`：GeneralUser GS 完整 bank/program/鼓组目录。
- `config/complexity-presets.json`：复杂度预设。
- `config/vocals*.example.json`：中文、英文、日文歌声配置样例。
- `profiles/`：General MIDI、Ample、Shreddage、SFZ、custom SoundFont profile。

### 核心代码

- `src/composition/loader.py`：composition schema 和语义校验。
- `src/midi/generator.py`：事件展开、前景活动推导、独立/全曲 MIDI 输出。
- `src/instruments/`：乐器语义编译器和物理模型。
- `src/instruments/strumming.py`：八分/十六分右手网格、逐弦状态、变奏和 foreground thinning。
- `src/performance/`：neutral performance event 与 sound-library profile 编译。
- `src/accompaniment/`：texture materialization 与 continuity critic。
- `src/complexity/`：复杂度解析与 critic。
- `src/melody/long_form.py`：实验 Long-Form planner/realizer。
- `src/validation/`：乐器、MIDI、Long-Form、扫弦和结构诊断。
- `src/render/`：FluidSynth/SFZ 路由与 WAV 渲染。
- `src/vocals/`：zh/en/ja 歌声 schema、score 和 backend 路由。

### 关键脚本

- `scripts/doctor.py`：本机环境和真实渲染检查。
- `scripts/setup_assets.py`：恢复 FluidSynth/GeneralUser GS 等忽略资产。
- `scripts/setup_vocals.ps1`：恢复可选歌声环境。
- `scripts/render_song.py`：全曲 MIDI、stem、mix 和可选 vocal 入口。
- `scripts/render_vocals.py`、`scripts/validate_vocals.py`：人声渲染与校验。
- `scripts/critic_*.py`：complexity、continuity、instrument、Long-Form critic。
- `scripts/build_instrument_aware_demos.py`：七个乐器语义 Demo。
- `scripts/build_long_form_phrase_demos.py`：Long-Form A/B。
- `scripts/build_strumming_continuity_demo.py`：旧八分持续扫弦验证。
- `scripts/build_sixteenth_strumming_demo.py`：新十六分逐弦/前景退让验证。

### 文档

- `docs/instrument_research/architecture_proposal.md`：instrument-aware 总架构。
- `docs/instrument_research/*.md`：吉他、贝斯、鼓、键盘、弦乐研究说明。
- `docs/guitar_native_lead_playbook.md`：已验证的电吉他原生主奏经验。
- `docs/continuous_strumming.md`：持续扫弦语义与十六分逐弦路径。
- `docs/long_form_phrase_schema.md`：Long-Form 三层 schema 与模式边界。
- `docs/long_form_rollback_audit.md`：Long-Form 最小回退审计。

### 测试

- `tests/test_complexity.py`
- `tests/test_accompaniment.py`
- `tests/test_instrument_aware.py`
- `tests/test_long_form_phrase.py`
- `tests/test_melody_skeleton_v2.py`
- `tests/test_strumming_continuity.py`

## 7. Git 与恢复注意事项

- `.venv/`、`.venv-vocals/`、`assets/`、`tools/`、参考仓库 checkout、WAV、MID、cache 和 IDE
  metadata 不进入版本控制。
- clone 后先阅读 README，执行 `scripts/setup_assets.py`；需要 AI 歌声时再执行
  `scripts/setup_vocals.ps1`。
- 作品的可编辑 source、brief、lyrics、critique、composition revision、debug 和 validation report
  可以进入 Git；最终音频从这些源文件重新渲染。
- 本 checkpoint 不声称 sfizz、VST 或 Ample 实际渲染已经完成。
