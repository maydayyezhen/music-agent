"use strict";

// Notes get a full three-second visual lead-in. During the countdown the
// timeline runs from -3s to 0s, so a note at song time 0 starts at the top.
const APPROACH_TIME = 3;
const HIT_WINDOWS = { perfect: 0.085, great: 0.145, good: 0.225, miss: 0.26 };
const LANE_COLORS = ["#ffc967", "#63e6df", "#ff6f91", "#a98bff"];
const SECTION_LABELS = {
  intro: "INTRO", verse: "VERSE", chorus: "CHORUS", verse_1: "VERSE I",
  pre_1: "PRE-CHORUS I", chorus_1: "CHORUS I", verse_2: "VERSE II",
  pre_2: "PRE-CHORUS II", chorus_2: "CHORUS II", bridge: "BRIDGE",
  final_chorus: "FINAL CHORUS", theme_a: "MAIN THEME A", theme_b: "MAIN THEME B",
  main_solo: "MAIN GUITAR SOLO", final_theme: "FINAL THEME", outro: "OUTRO"
};

const songs = window.RHYTHM_GAME_SONGS || [];
const canvas = document.querySelector("#gameCanvas");
const ctx = canvas.getContext("2d");
const audio = document.querySelector("#song");
const startButton = document.querySelector("#startButton");
const pauseButton = document.querySelector("#pauseButton");
const soundButton = document.querySelector("#soundButton");
const retryButton = document.querySelector("#retryButton");
const changeSongButton = document.querySelector("#changeSongButton");
const startOverlay = document.querySelector("#startOverlay");
const resultOverlay = document.querySelector("#resultOverlay");
const judgement = document.querySelector("#judgement");
const countdown = document.querySelector("#countdown");
const songPicker = document.querySelector("#songPicker");
const laneButtons = [...document.querySelectorAll("[data-lane]")];

let selectedSong = songs[0] || null;
let chart = [];
let activeNotes = [];
let running = false;
let countingDown = false;
let hitSoundEnabled = true;
let audioContext = null;
let animationId = 0;
let lastPhraseIndex = -2;
let judgementTimer = 0;
let state = freshState();

function freshState() {
  return { score: 0, combo: 0, maxCombo: 0, perfect: 0, great: 0, good: 0, miss: 0, weighted: 0, judged: 0 };
}

function renderSongPicker() {
  songPicker.replaceChildren();
  for (const song of songs) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `song-choice${song.id === selectedSong?.id ? " selected" : ""}`;
    button.style.setProperty("--song-accent", song.accent);
    button.innerHTML = `<strong>${song.title}</strong><small>${song.subtitle} · ${song.bpm} BPM · ${formatTime(song.duration)}</small>`;
    button.addEventListener("click", () => selectSong(song.id));
    songPicker.append(button);
  }
}

function selectSong(songId) {
  if (running) return;
  const song = songs.find(item => item.id === songId);
  if (!song) return;
  selectedSong = song;
  chart = song.notes;
  audio.src = song.audio;
  audio.load();
  document.documentElement.style.setProperty("--gold", song.accent);
  document.querySelector("#headerTitle").textContent = song.title;
  document.querySelector("#headerBpm").textContent = `${song.bpm} BPM`;
  document.querySelector("#headerKey").textContent = song.key.toUpperCase();
  document.querySelector("#startTitle").textContent = song.title;
  document.querySelector("#startMeta").textContent = `${song.subtitle.toUpperCase()} · ${song.bpm} BPM`;
  const songInstructions = {
    "different-windows": "跟随主唱旋律，穿过四条音轨。<br>音符落到判定线时按下 D、F、J、K。",
    "hands-before-notes": "跟随电吉他与鼓组穿过四条音轨。<br>Bridge 段由节奏组接管谱面。",
    "distance-still-burns": "专家难度：完整演奏主音吉他轨。<br>32 小节 Solo 后还有满能量最终主题。"
  };
  document.querySelector(".intro-copy").innerHTML = songInstructions[song.id] || "跟随节奏击打四条音轨。";
  document.querySelector("#loadingText").textContent = `${chart.length} 个音符 · 谱面已就绪`;
  document.querySelector("#timeTotal").textContent = formatTime(song.duration);
  document.querySelector("#currentLyric").textContent = song.intro;
  document.querySelector("#sectionName").textContent = "INTRO";
  startButton.disabled = false;
  renderSongPicker();
  draw(0);
}

function resetGame() {
  audio.pause();
  audio.currentTime = 0;
  state = freshState();
  activeNotes = chart.map(note => ({ ...note, judged: false, result: null }));
  lastPhraseIndex = -2;
  updateHud();
  updateStory(0);
  judgement.textContent = "";
}

async function runCountdown() {
  if (countingDown) return false;
  countingDown = true;
  const countdownSeconds = 3;
  const anchorTime = audio.currentTime;
  const startedAt = performance.now();
  let lastValue = "";
  await new Promise(resolve => {
    function countdownFrame(frameTime) {
      const elapsed = Math.min(countdownSeconds, (frameTime - startedAt) / 1000);
      const remaining = countdownSeconds - elapsed;
      const value = elapsed < 1 ? "3" : elapsed < 2 ? "2" : "1";
      if (value !== lastValue) {
        lastValue = value;
        countdown.textContent = value;
        countdown.classList.toggle("go", value === "GO!");
        countdown.classList.remove("show");
        void countdown.offsetWidth;
        countdown.classList.add("show");
        playCountSound(value);
      }
      // Pre-roll the chart while audio stays paused. At the start, notes at
      // anchorTime are at the lane top; at GO they reach the judgement line.
      draw(anchorTime - remaining);
      updateStory(Math.max(0, anchorTime - remaining));
      if (elapsed < countdownSeconds) requestAnimationFrame(countdownFrame);
      else resolve();
    }
    requestAnimationFrame(countdownFrame);
  });
  countdown.textContent = "GO!";
  countdown.classList.add("go");
  countdown.classList.remove("show");
  void countdown.offsetWidth;
  countdown.classList.add("show");
  playCountSound("GO!");
  setTimeout(() => {
    countdown.classList.remove("show", "go");
    countdown.textContent = "";
  }, 480);
  countingDown = false;
  return true;
}

function playCountSound(value) {
  ensureAudioContext();
  const now = audioContext.currentTime;
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  oscillator.type = "sine";
  oscillator.frequency.value = value === "GO!" ? 880 : 440;
  gain.gain.setValueAtTime(.0001, now);
  gain.gain.exponentialRampToValueAtTime(value === "GO!" ? .1 : .065, now + .008);
  gain.gain.exponentialRampToValueAtTime(.0001, now + (value === "GO!" ? .18 : .1));
  oscillator.connect(gain).connect(audioContext.destination);
  oscillator.start(now);
  oscillator.stop(now + .2);
}

async function startGame() {
  if (!selectedSong) return;
  resetGame();
  startOverlay.classList.add("hidden");
  resultOverlay.classList.add("hidden");
  pauseButton.disabled = true;
  running = false;
  ensureAudioContext();
  await runCountdown();
  try {
    await audio.play();
  } catch (error) {
    running = false;
    startOverlay.classList.remove("hidden");
    document.querySelector("#loadingText").textContent = "音频无法播放，请重新点击开始";
    console.error(error);
    return;
  }
  pauseButton.disabled = false;
  running = true;
  cancelAnimationFrame(animationId);
  loop();
}

async function togglePause() {
  if (audio.ended || countingDown || !startOverlay.classList.contains("hidden")) return;
  if (audio.paused) {
    pauseButton.disabled = true;
    document.querySelector("#pauseIcon").textContent = "Ⅱ";
    document.querySelector("#pauseLabel").textContent = "PAUSE";
    await runCountdown();
    await audio.play();
    running = true;
    pauseButton.disabled = false;
    cancelAnimationFrame(animationId);
    loop();
  } else {
    audio.pause();
    running = false;
    document.querySelector("#pauseIcon").textContent = "▶";
    document.querySelector("#pauseLabel").textContent = "RESUME";
  }
}

function ensureAudioContext() {
  if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
  if (audioContext.state === "suspended") audioContext.resume();
}

function playHitSound(lane, strength = 1) {
  if (!hitSoundEnabled) return;
  ensureAudioContext();
  const now = audioContext.currentTime;
  const oscillator = audioContext.createOscillator();
  const gain = audioContext.createGain();
  const filter = audioContext.createBiquadFilter();
  const frequencies = [196, 247, 294, 392];
  oscillator.type = lane % 2 ? "triangle" : "sine";
  oscillator.frequency.setValueAtTime(frequencies[lane], now);
  oscillator.frequency.exponentialRampToValueAtTime(frequencies[lane] * 1.45, now + 0.035);
  filter.type = "highpass";
  filter.frequency.value = 150;
  gain.gain.setValueAtTime(0.0001, now);
  gain.gain.exponentialRampToValueAtTime(0.075 * strength, now + 0.004);
  gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.075);
  oscillator.connect(filter).connect(gain).connect(audioContext.destination);
  oscillator.start(now);
  oscillator.stop(now + 0.08);
}

function hitLane(lane) {
  if (!running || countingDown || audio.paused) return;
  flashLane(lane);
  const now = audio.currentTime;
  let closest = null;
  let smallestDelta = Infinity;
  for (const note of activeNotes) {
    if (note.judged || note.lane !== lane) continue;
    const delta = Math.abs(note.time - now);
    if (delta < smallestDelta) { closest = note; smallestDelta = delta; }
    if (note.time > now + HIT_WINDOWS.miss) break;
  }
  if (!closest || smallestDelta > HIT_WINDOWS.miss) {
    playHitSound(lane, .55);
    return;
  }
  playHitSound(lane, 1);
  if (smallestDelta <= HIT_WINDOWS.perfect) applyResult(closest, "perfect");
  else if (smallestDelta <= HIT_WINDOWS.great) applyResult(closest, "great");
  else applyResult(closest, "good");
}

function applyResult(note, result) {
  note.judged = true;
  note.result = result;
  state[result] += 1;
  state.judged += 1;
  if (result === "miss") {
    state.combo = 0;
  } else {
    const weights = { perfect: 1, great: .75, good: .4 };
    const points = { perfect: 1000, great: 700, good: 350 };
    state.combo += 1;
    state.maxCombo = Math.max(state.maxCombo, state.combo);
    state.weighted += weights[result];
    state.score += points[result] + Math.min(state.combo, 100) * 4;
  }
  showJudgement(result);
  updateHud();
}

function markMisses(now) {
  for (const note of activeNotes) {
    if (!note.judged && now - note.time > HIT_WINDOWS.miss) applyResult(note, "miss");
    if (note.time > now) break;
  }
}

function showJudgement(result) {
  const names = { perfect: "Perfect", great: "Great", good: "Good", miss: "Miss" };
  clearTimeout(judgementTimer);
  judgement.classList.remove("show");
  void judgement.offsetWidth;
  judgement.textContent = names[result];
  judgement.style.color = result === "perfect" ? "#ffc967" : result === "great" ? "#63e6df" : result === "good" ? "#a98bff" : "#ff6f91";
  judgement.classList.add("show");
  judgementTimer = setTimeout(() => judgement.classList.remove("show"), 430);
}

function flashLane(lane) {
  const button = laneButtons[lane];
  button.classList.add("active");
  setTimeout(() => button.classList.remove("active"), 90);
}

function accuracy() {
  return state.judged ? state.weighted / state.judged * 100 : 100;
}

function updateHud() {
  document.querySelector("#score").textContent = String(state.score).padStart(7, "0");
  document.querySelector("#combo strong").textContent = state.combo;
  document.querySelector("#accuracy").textContent = accuracy().toFixed(1);
  document.querySelector("#perfectCount").textContent = state.perfect;
  document.querySelector("#greatCount").textContent = state.great;
  document.querySelector("#goodCount").textContent = state.good;
  document.querySelector("#missCount").textContent = state.miss;
  document.querySelector("#accuracyRing").style.background = `conic-gradient(var(--gold) ${accuracy()}%, rgba(255,255,255,.08) 0)`;
}

function formatTime(value) {
  if (!Number.isFinite(value)) return "0:00";
  return `${Math.floor(value / 60)}:${String(Math.floor(value % 60)).padStart(2, "0")}`;
}

function updateStory(now) {
  const phrases = selectedSong?.phrases || [];
  let index = phrases.findIndex(phrase => now >= phrase.start - .25 && now <= phrase.end + .45);
  if (index < 0) index = phrases.findIndex(phrase => phrase.start > now);
  if (index < 0) index = phrases.length;
  const activeIndex = index < phrases.length && now >= phrases[index].start - .25 ? index : -1;
  const displayIndex = activeIndex >= 0 ? activeIndex : index;
  if (displayIndex === lastPhraseIndex) return;
  lastPhraseIndex = displayIndex;
  const current = activeIndex >= 0 ? phrases[activeIndex] : null;
  document.querySelector("#previousLyric").textContent = displayIndex > 0 ? phrases[displayIndex - 1].text : "";
  document.querySelector("#currentLyric").textContent = current?.text || selectedSong?.intro || "Instrumental";
  document.querySelector("#nextLyric").textContent = displayIndex < phrases.length ? phrases[displayIndex]?.text || "" : "";
  const section = current?.section || selectedSong?.sections.find(item => now >= item.start && now < item.end)?.name || "outro";
  document.querySelector("#sectionName").textContent = SECTION_LABELS[section] || section.replaceAll("_", " ").toUpperCase();
}

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function draw(now) {
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const hitY = height - 92;
  const topY = 48;
  const side = width * .05;
  const laneWidth = (width - side * 2) / 4;
  ctx.clearRect(0, 0, width, height);
  const glow = ctx.createLinearGradient(0, 0, 0, height);
  glow.addColorStop(0, "rgba(55,75,126,.05)");
  glow.addColorStop(1, "rgba(9,13,27,.82)");
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, width, height);
  for (let i = 0; i <= 4; i += 1) {
    const x = side + i * laneWidth;
    ctx.strokeStyle = "rgba(207,219,255,.105)";
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x, topY); ctx.lineTo(x, hitY + 11); ctx.stroke();
  }
  const secondsPerBeat = 60 / (selectedSong?.bpm || 108);
  for (let time = Math.ceil(now / secondsPerBeat) * secondsPerBeat; time < now + APPROACH_TIME; time += secondsPerBeat) {
    const y = hitY - ((time - now) / APPROACH_TIME) * (hitY - topY);
    ctx.strokeStyle = "rgba(255,255,255,.035)";
    ctx.beginPath(); ctx.moveTo(side, y); ctx.lineTo(width - side, y); ctx.stroke();
  }
  ctx.shadowBlur = 16;
  for (const note of activeNotes) {
    if (note.judged) continue;
    const delta = note.time - now;
    if (delta > APPROACH_TIME || delta < -HIT_WINDOWS.miss) continue;
    const y = hitY - (delta / APPROACH_TIME) * (hitY - topY);
    const x = side + note.lane * laneWidth + 7;
    const widthOfNote = laneWidth - 14;
    const color = LANE_COLORS[note.lane];
    ctx.shadowColor = color;
    ctx.fillStyle = color;
    ctx.globalAlpha = Math.max(.32, 1 - Math.max(delta, 0) / APPROACH_TIME * .35);
    ctx.fillRect(x, y - 5, widthOfNote, 10);
    ctx.fillStyle = "rgba(255,255,255,.85)";
    ctx.fillRect(x + 4, y - 3, widthOfNote - 8, 2);
  }
  ctx.globalAlpha = 1;
  ctx.shadowBlur = 0;
  const lineGradient = ctx.createLinearGradient(side, 0, width - side, 0);
  LANE_COLORS.forEach((color, index) => lineGradient.addColorStop(index / 3, color));
  ctx.strokeStyle = lineGradient;
  ctx.lineWidth = 2;
  ctx.shadowBlur = 14;
  ctx.shadowColor = "rgba(255,255,255,.35)";
  ctx.beginPath(); ctx.moveTo(side, hitY); ctx.lineTo(width - side, hitY); ctx.stroke();
  ctx.shadowBlur = 0;
}

function loop() {
  if (!running) return;
  const now = audio.currentTime;
  markMisses(now);
  updateStory(now);
  draw(now);
  document.querySelector("#timeNow").textContent = formatTime(now);
  document.querySelector("#timeTotal").textContent = formatTime(audio.duration || selectedSong.duration);
  document.querySelector("#songProgress").style.width = `${Math.min(100, now / (audio.duration || selectedSong.duration) * 100)}%`;
  animationId = requestAnimationFrame(loop);
}

function finishGame() {
  running = false;
  cancelAnimationFrame(animationId);
  const acc = accuracy();
  const grade = acc >= 98 ? "S" : acc >= 90 ? "A" : acc >= 80 ? "B" : acc >= 70 ? "C" : "D";
  document.querySelector("#resultGrade").textContent = grade;
  document.querySelector("#resultScore").textContent = String(state.score).padStart(7, "0");
  document.querySelector("#resultSummary").textContent = `${selectedSong.title} · Accuracy ${acc.toFixed(1)}% · Max Combo ${state.maxCombo}`;
  resultOverlay.classList.remove("hidden");
  pauseButton.disabled = true;
}

function showSongSelection() {
  audio.pause();
  running = false;
  countingDown = false;
  countdown.classList.remove("show", "go");
  countdown.textContent = "";
  resultOverlay.classList.add("hidden");
  startOverlay.classList.remove("hidden");
  renderSongPicker();
}

const KEY_TO_LANE = { KeyD: 0, KeyF: 1, KeyJ: 2, KeyK: 3 };
window.addEventListener("keydown", event => {
  if (event.code === "Space") { event.preventDefault(); if (!event.repeat) togglePause(); return; }
  const lane = KEY_TO_LANE[event.code];
  if (lane !== undefined && !event.repeat) { event.preventDefault(); hitLane(lane); }
});
laneButtons.forEach(button => {
  const lane = Number(button.dataset.lane);
  button.addEventListener("pointerdown", event => { event.preventDefault(); hitLane(lane); });
});
startButton.addEventListener("click", startGame);
retryButton.addEventListener("click", startGame);
changeSongButton.addEventListener("click", showSongSelection);
pauseButton.addEventListener("click", togglePause);
soundButton.addEventListener("click", () => {
  hitSoundEnabled = !hitSoundEnabled;
  soundButton.setAttribute("aria-pressed", String(hitSoundEnabled));
  soundButton.textContent = `♪ HIT SOUND · ${hitSoundEnabled ? "ON" : "OFF"}`;
  if (hitSoundEnabled) playHitSound(1, .7);
});
audio.addEventListener("ended", finishGame);
audio.addEventListener("loadedmetadata", () => document.querySelector("#timeTotal").textContent = formatTime(audio.duration));
window.addEventListener("resize", () => { resizeCanvas(); draw(audio.currentTime || 0); });

startButton.disabled = true;
resizeCanvas();
if (selectedSong) selectSong(selectedSong.id);
else document.querySelector("#loadingText").textContent = "没有找到歌曲数据";
