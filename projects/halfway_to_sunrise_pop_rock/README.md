# Halfway to Sunrise

一首按当前 V2 架构写的原创英文流行摇滚歌曲工程。

- **Tempo:** 128 BPM
- **Meter:** 4/4
- **Key center:** D major / B minor
- **Score length:** 96 bars = 180.00 s
- **Rendered length:** 约 183 s（含 3 s tail）
- **Complexity:** rich，自定义 section contour
- **Lead vocal:** English / SoulX-Singer

## Form

```text
Intro          4 bars
Verse 1       12 bars
Pre 1          8 bars
Chorus 1      12 bars
Verse 2       12 bars
Pre 2          8 bars
Chorus 2      12 bars
Bridge         8 bars
Final Chorus  16 bars
Outro          4 bars
```

## Instrument / role plan

这次先定角色，再检索 Material，没有从 `pop-rock` 标签反推乐器阵容。

- **Lead vocal**: 主叙事与副歌 hook。Intro / Outro 不唱，Final Chorus 最后四小节也故意留给吉他回答。
- **Steel-string acoustic guitar**: 全曲连续的手部运动骨架。Verse 用 selective sixteenth flow；Pre 与 Final Chorus 提高为 dense continuous sixteenth。有人声时启用 foreground-aware thinning，而不是粗暴停掉整轨。
- **Muted electric guitar**: Verse / Pre 的干、短、前推节奏；Bridge 前半继续承担压缩能量的角色。
- **Overdrive rhythm guitar**: Chorus 的持续中频床；Bridge 后半从 muted guitar 手里接棒；Outro 只保留前半后退出。
- **Lead electric guitar**: Intro hook、Verse/Chorus 句尾回答、Bridge 独奏、Final Chorus 最后四小节 instrumental tag。
- **Finger electric bass**: 保留根音地基，但带 fifth / octave / approach motion；Bridge 与 Final Chorus 切到更连接的行为。
- **Drum kit**: Verse 与 Chorus 使用不同密度，段尾 fill 负责连接，不靠单纯提高 velocity 制造所有 lift。
- **Piano**: Intro、Pre、第二次 Chorus、Bridge、Final Chorus 与 Outro 的 voice-led harmonic color，不与吉他抢主要节奏功能。

## V2 material choices

角色规划完成以后才使用这些当前 Material：

- `materials_v2/accompaniment_patterns/acoustic_guitar/warm_pop_sixteenth_strum.md`
- `materials_v2/accompaniment_patterns/electric_guitar/muted_pop_rock_pulse.md`
- `materials_v2/accompaniment_patterns/electric_guitar/continuous_overdrive_rhythm_bed.md`
- `materials_v2/instrument_gestures/electric_guitar/sustained_overdrive_guitar.md`
- `materials_v2/accompaniment_patterns/bass/section_linked_pop_rock_bass.md`
- `materials_v2/production_chains/electric_guitar/role_separated_midi_guitar_mix.md`

Renderer 选择 `general_midi`。`shreddage_stratus_free` 当前 Profile 明确只是 capability placeholder，缺少已验证的具体 trigger，所以本工程不虚构其 keyswitch / renderer 行为。

## Build

在仓库根目录：

```powershell
python .\projects\halfway_to_sunrise_pop_rock\build_song.py
```

这会生成/刷新：

```text
composition.json
vocals.json
instruments.json
render.json
manifest.json
lyrics.md
```

`build_song.py` 是 manifest 登记的 authoritative song source；上述 JSON / lyrics 是可检查的结构化派生物。若直接编辑派生 JSON，之后再次运行 builder 会覆盖它们。

## Render instrumental

```powershell
python .\projects\halfway_to_sunrise_pop_rock\build_song.py --render --audit
```

主要输出：

```text
projects/halfway_to_sunrise_pop_rock/output/full_song.mid
projects/halfway_to_sunrise_pop_rock/output/mix.wav
```

同时会写 semantic phrase / instrument validation 等报告。

## Render with English vocal

如果本机还没配置过 vocal 环境，先按仓库现有脚本安装：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_vocals.ps1
```

然后：

```powershell
python .\projects\halfway_to_sunrise_pop_rock\build_song.py --with-vocals --audit
```

最终带人声版本：

```text
projects/halfway_to_sunrise_pop_rock/output/vocal_mix.wav
```

## Musical intent

不是“大失真墙从第一秒砸到最后”。Verse 里木吉他的 16 分运动和 muted guitar 各自承担不同颗粒度；Pre 通过密度、钢琴和节奏重心逐层抬升；Chorus 再让 overdrive bed、完整鼓组和更开的 vocal register 进入。Bridge 前四小节收紧，后四小节换成 overdrive + lead guitar，把能量重新打开。Final Chorus 的最后四小节停止主唱，让 Intro guitar hook 以更高能量回来，形成真正的回收与结尾。
