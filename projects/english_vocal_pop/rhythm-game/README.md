# Different Windows Rhythm Game

一个使用三个本地音乐项目资源的四轨下落式音游原型。

- **Different Windows**：人声旋律谱面，235 个音符
- **Hands Before Notes**：以电吉他为主、鼓组重拍为辅；Bridge 由鼓组接管
- **The Distance Still Burns**：专家级完整主音吉他谱；32 小节 Solo，Bridge 由鼓组接管

## 启动

双击 `run-game.bat`，浏览器会自动打开游戏。无需安装、无需启动本地服务。

## 操作

- `D`、`F`、`J`、`K`：击打四条音轨
- `Space`：暂停或继续
- 手机/平板：直接触摸底部四个按键
- 侧栏 `HIT SOUND`：开启或关闭四键击打音效
- 开局及暂停恢复：谱面在 `3、2、1` 时从轨道顶部预落，`GO!` 时抵达判定线并开始播放

歌曲继续使用各自项目中的原始音频，不会复制大体积文件。若源谱有修改，运行 `python build_songs.py` 可重新生成歌曲数据目录。
