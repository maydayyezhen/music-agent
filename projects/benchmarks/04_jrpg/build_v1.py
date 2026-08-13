import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SECTIONS = [("Frontier Call", 4), ("Pursuit", 12), ("Shadow Pass", 8), ("Heroic Clash", 16), ("Victory Road", 8)]

def note(at, pitch, duration, velocity):
    return {"type": "note", "at": at, "pitch": pitch, "duration": duration, "velocity": velocity}

def chord(at, pitches, duration, velocity):
    return {"type": "chord", "at": at, "pitches": pitches, "duration": duration, "velocity": velocity}

def drum(at, name, velocity, duration=0.10):
    return {"type": "drum", "at": at, "note": name, "duration": duration, "velocity": velocity}

def clip(loop_bars, events):
    return {"loop_bars": loop_bars, "events": events}

def ostinato(chords, velocity=76, high=False):
    events = []
    patterns = {
        "Dm": ["D4", "A4", "F4", "A4", "D5", "A4", "F4", "A4"],
        "Bb": ["Bb3", "F4", "D4", "F4", "Bb4", "F4", "D4", "F4"],
        "Gm": ["G3", "D4", "Bb3", "D4", "G4", "D4", "Bb3", "D4"],
        "A": ["A3", "E4", "C#4", "E4", "A4", "E4", "C#4", "E4"],
        "C": ["C4", "G4", "E4", "G4", "C5", "G4", "E4", "G4"],
        "F": ["F3", "C4", "A3", "C4", "F4", "C4", "A3", "C4"],
    }
    for bar, name in enumerate(chords, 1):
        pitches = patterns[name]
        for step in range(16):
            pitch = pitches[step % 8]
            if high and step in (4, 12):
                pitch = {"D5":"D6", "Bb4":"Bb5", "G4":"G5", "A4":"A5", "C5":"C6", "F4":"F5"}.get(pitch, pitch)
            beat = 1 + step * 0.25
            vel = velocity + (9 if step % 4 == 0 else 0) + (3 if step % 2 == 0 else -4)
            events.append(note(f"{bar}:{beat:g}", pitch, 0.20, vel))
    return events

def motif(bar, start=1, transpose=0, velocity=96, octave=False):
    base = [62, 67, 65, 64, 61, 62]
    durs = [1, .5, .5, 1, .5, .5]
    starts = [start, start+1, start+1.5, start+2, start+3, start+3.5]
    out = []
    for p, d, s in zip(base, durs, starts):
        pitches = [p + transpose]
        if octave: pitches.append(p + transpose + 12)
        for q in pitches:
            out.append(note(f"{bar}:{s:g}", q, d * .82, velocity + (4 if s == start else 0)))
    return out

def bass_pattern(chords, velocity=88, active=True):
    tones = {
        "Dm": ["D2","A2","D3","C3","C#3"], "Bb": ["Bb1","F2","Bb2","A2","A2"],
        "Gm": ["G1","D2","G2","A2","G#2"], "A": ["A1","E2","A2","G2","C#2"],
        "C": ["C2","G2","C3","B2","C#3"], "F": ["F1","C2","F2","E2","F#2"]
    }
    events=[]
    for bar, name in enumerate(chords,1):
        root,fifth,octv,passing,approach=tones[name]
        seq=[(1,root,1),(2,fifth,.5),(2.5,octv,.5),(3,passing,.5),(3.5,fifth,.5),(4,approach,.5),(4.5,fifth,.5)] if active else [(1,root,1.8),(3,fifth,.8),(4,approach,.7)]
        for beat,pitch,dur in seq: events.append(note(f"{bar}:{beat:g}",pitch,dur,velocity+(6 if beat==1 else -3)))
    return events

def piano_broken(chords, velocity=68):
    voicings={
        "Dm": ["D3","A3","F4","A4"], "Bb": ["Bb2","F3","D4","F4"],
        "Gm": ["G2","D3","Bb3","D4"], "A": ["A2","E3","C#4","E4"],
        "C": ["C3","G3","E4","G4"], "F": ["F2","C3","A3","C4"]
    }
    events=[]
    for bar,name in enumerate(chords,1):
        v=voicings[name]
        for i,beat in enumerate([1,1.5,2.5,3,4,4.5]):
            pitch=v[[0,1,2,1,3,2][i]]
            events.append(note(f"{bar}:{beat:g}",pitch,.38,velocity+(7 if beat in (1,3) else 0)))
    return events

def drums_pattern(bars, mode):
    events=[]
    for bar in range(1,bars+1):
        if mode in ("pursuit","clash","victory"):
            kicks=[1,2.5,3,3.75] if bar%2 else [1,1.75,3,4.5]
            for b in kicks: events.append(drum(f"{bar}:{b:g}","kick",108 if b in (1,3) else 91))
            for b in (2,4): events.append(drum(f"{bar}:{b}","snare",104))
            for step in range(8): events.append(drum(f"{bar}:{1+step*.5:g}","closed_hat",78+(10 if step%2==0 else -5),.08))
            if mode=="clash":
                for b in (1.5,2.5,3.5,4.5): events.append(drum(f"{bar}:{b:g}","ride",82,.12))
        elif mode=="shadow":
            for b in (1,3,3.5): events.append(drum(f"{bar}:{b:g}","kick",88))
            for b in (2,4): events.append(drum(f"{bar}:{b}","snare",91))
            for b in (1,2,3,4): events.append(drum(f"{bar}:{b}","closed_hat",65+(5 if b in (1,3) else 0),.08))
        else:
            for b in (1,3): events.append(drum(f"{bar}:{b}","kick",88))
            for b in (2,4): events.append(drum(f"{bar}:{b}","snare",86))
            for b in (1,2,3,4): events.append(drum(f"{bar}:{b}","closed_hat",58+(7 if b==1 else 0),.08))
        if bar==1 and mode in ("pursuit","clash","victory"): events.append(drum(f"{bar}:1","crash",112,.2))
        if bar==bars:
            for b,n,v in [(3,"low_tom",83),(3.5,"mid_tom",90),(4,"high_tom",99),(4.5,"snare",108)]: events.append(drum(f"{bar}:{b:g}",n,v,.12))
    return events

strings = {
    "Frontier Call": clip(4, ostinato(["Dm","Bb","Gm","A"],64)+motif(1,1,0,85)+motif(3,1,-2,82)),
    "Pursuit": clip(4, ostinato(["Dm","Bb","Gm","A"],74)+motif(1,1,0,96)+motif(3,1,2,92)),
    "Shadow Pass": clip(4, ostinato(["Gm","F","Bb","A"],66)+[note("1:1","G4",1.5,76),note("1:3","A4",.8,79),note("2:1","Bb4",1.5,82),note("2:3","C5",.8,84),note("3:1","D5",1.5,87),note("4:3","C#5",1.7,91)]),
    "Heroic Clash": clip(4, ostinato(["Dm","C","Bb","A"],82,True)+motif(1,1,0,105)+motif(3,1,5,103,True)),
    "Victory Road": clip(4, ostinato(["Bb","F","Gm","A"],72)+motif(1,1,3,96)+motif(3,1,0,94))
}

brass = {
    "Frontier Call": clip(4,[chord("4:1",["A3","E4","C#5"],1.5,88),note("4:3","A4",.8,94)]),
    "Pursuit": clip(4,[chord("1:1",["D3","A3","F4"],.65,91),chord("2:3",["Bb3","F4","D5"],.55,86),chord("4:1",["A3","E4","C#5"],.7,98),note("4:4","A4",.65,101)]),
    "Heroic Clash": clip(4,[chord("1:1",["D3","A3","D4","F4"],.75,106),note("1:2","G4",.45,101),note("1:2.5","F4",.45,99),chord("2:3",["C4","G4","E5"],.6,96),chord("3:1",["Bb3","F4","D5"],.7,102),chord("4:1",["A3","E4","C#5"],.65,110),note("4:4","A4",.7,112)]),
    "Victory Road": clip(4,[chord("1:1",["Bb3","F4","D5"],.8,94),chord("2:1",["A3","C4","F4"],.8,90),chord("4:1",["A3","E4","C#5"],.8,99)])
}

piano = {
    "Frontier Call": clip(4,piano_broken(["Dm","Bb","Gm","A"],63)),
    "Pursuit": clip(4,piano_broken(["Dm","Bb","Gm","A"],69)+[note("2:4","F5",.4,79),note("2:4.5","E5",.4,76),note("4:3.5","C#5",.4,82),note("4:4","E5",.4,80)]),
    "Shadow Pass": clip(4,piano_broken(["Gm","F","Bb","A"],58)),
    "Heroic Clash": clip(4,piano_broken(["Dm","C","Bb","A"],73)+[note("2:2.5","G5",.35,84),note("2:3","E5",.35,81),note("4:3","C#5",.35,88),note("4:3.5","E5",.35,85)]),
    "Victory Road": clip(4,piano_broken(["Bb","F","Gm","A"],67))
}

bass = {
    "Frontier Call": clip(4,bass_pattern(["Dm","Bb","Gm","A"],78,False)),
    "Pursuit": clip(4,bass_pattern(["Dm","Bb","Gm","A"],90,True)),
    "Shadow Pass": clip(4,bass_pattern(["Gm","F","Bb","A"],78,False)),
    "Heroic Clash": clip(4,bass_pattern(["Dm","C","Bb","A"],96,True)),
    "Victory Road": clip(4,bass_pattern(["Bb","F","Gm","A"],86,True))
}

drums = {
    "Frontier Call": clip(4,drums_pattern(4,"intro")),
    "Pursuit": clip(4,drums_pattern(4,"pursuit")),
    "Shadow Pass": clip(4,drums_pattern(4,"shadow")),
    "Heroic Clash": clip(4,drums_pattern(4,"clash")),
    "Victory Road": clip(4,drums_pattern(4,"victory"))
}

composition={
    "metadata":{"title":"Runeblade Pursuit (V1)","tempo":152,"time_signature":"4/4","key":"D minor"},
    "sections":[{"name":n,"bars":b} for n,b in SECTIONS],
    "tracks":{
        "strings":{"role":"motif, counter-line, and rhythmic ostinato","sections":strings},
        "brass":{"role":"structural accents and heroic augmentation","sections":brass},
        "piano":{"role":"broken harmonic support and answers","sections":piano},
        "bass":{"role":"directional low-end line","sections":bass},
        "drums":{"role":"fast battle groove and transitions","sections":drums}
    }
}

text=json.dumps(composition,ensure_ascii=False,indent=2)+"\n"
(ROOT/"composition_v1.json").write_text(text,encoding="utf-8")
(ROOT/"composition.json").write_text(text,encoding="utf-8")
