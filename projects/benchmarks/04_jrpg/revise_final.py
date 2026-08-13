import json
from pathlib import Path

root = Path(__file__).resolve().parent
c = json.loads((root / "composition_v1.json").read_text(encoding="utf-8"))
c["metadata"]["title"] = "Runeblade Pursuit"

def n(at, pitch, duration, velocity):
    return {"type":"note", "at":at, "pitch":pitch, "duration":duration, "velocity":velocity}

def ch(at, pitches, duration, velocity):
    return {"type":"chord", "at":at, "pitches":pitches, "duration":duration, "velocity":velocity}

def d(at, name, velocity, duration=.10):
    return {"type":"drum", "at":at, "note":name, "duration":duration, "velocity":velocity}

# Shadow Pass: replace continuous sixteenths with spaced eighth-note gestures and a dominant build.
shadow=[]
harm=[("G3","D4","Bb4"),("F3","C4","A4"),("Bb3","F4","D5"),("A3","E4","C#5")]
for bar,(r,f,t) in enumerate(harm,1):
    for beat,p,v in [(1,r,71),(1.5,f,64),(2.5,t,73),(3,f,65),(4,t,77)]:
        shadow.append(n(f"{bar}:{beat:g}",p,.38,v))
for bar,p1,p2 in [(1,"G4","A4"),(2,"Bb4","C5"),(3,"D5","E5"),(4,"F5","E5")]:
    shadow += [n(f"{bar}:1",p1,1.35,79+bar),n(f"{bar}:3",p2,.75,81+bar)]
for bar in range(5,9):
    top=["A4","Bb4","C5","C#5"][bar-5]
    for beat,p,v in [(1,"A3",72),(2,"E4",68),(3,top,82+bar),(4,"E4",70)]:
        shadow.append(n(f"{bar}:{beat}",p,.7,v))
    if bar>=7:
        shadow += [n(f"{bar}:3.5","A4",.3,88),n(f"{bar}:4.5","C#5",.3,94)]
c["tracks"]["strings"]["sections"]["Shadow Pass"]={"loop_bars":8,"events":shadow}

# Explicit eight-bar resolution: Bb–F/A–Gm–A | Dm–Bb–A–Dm.
voicings=[["Bb3","F4","D5"],["A3","C4","F4"],["G3","D4","Bb4"],["A3","E4","C#5"],["D4","A4","F5"],["Bb3","F4","D5"],["A3","E4","C#5"],["D4","A4","F5"]]
strings=[]
for bar,v in enumerate(voicings,1):
    if bar == 8:
        continue
    seq=[v[0],v[1],v[2],v[1],v[0],v[1],v[2],v[1]]
    for step in range(16):
        strings.append(n(f"{bar}:{1+step*.25:g}",seq[step%8],.20,78+(9 if step%4==0 else -2)))
for bar,pitches in [(1,["F5","Bb5","A5","G5","E5","F5"]),(5,["D5","G5","F5","E5","C#5","D5"])]:
    for p,dur,beat in zip(pitches,[1,.5,.5,1,.5,.5],[1,2,2.5,3,4,4.5]):
        strings.append(n(f"{bar}:{beat:g}",p,dur*.82,103 if bar==5 else 98))
strings += [n("7:3","C#5",.45,101),n("7:3.5","E5",.45,98),n("7:4","A5",.75,106),ch("8:1",["D4","A4","D5","F5"],3.65,105)]
c["tracks"]["strings"]["sections"]["Victory Road"]={"loop_bars":8,"events":strings}

roots=[("Bb1","F2","A2"),("A1","E2","F#2"),("G1","D2","G#2"),("A1","E2","C#2"),("D2","A2","C3"),("Bb1","F2","A2"),("A1","E2","C#2"),("D2","A2","D3")]
bass=[]
for bar,(r,f,a) in enumerate(roots,1):
    seq=[(1,r,1,91),(2,f,.5,84),(2.5,a,.5,82),(3,r,.5,88),(3.5,f,.5,84),(4,a,.7,87)]
    if bar==8:
        seq=[(1,"D2",1.8,101),(3,"A2",.7,91),(4,"D3",.9,96)]
    for beat,p,dur,v in seq:
        bass.append(n(f"{bar}:{beat:g}",p,dur,v))
c["tracks"]["bass"]["sections"]["Victory Road"]={"loop_bars":8,"events":bass}

piano=[]
pvs=[["Bb2","F3","D4","F4"],["A2","F3","C4","F4"],["G2","D3","Bb3","D4"],["A2","E3","C#4","E4"],["D3","A3","F4","A4"],["Bb2","F3","D4","F4"],["A2","E3","C#4","E4"],["D3","A3","F4","D5"]]
for bar,v in enumerate(pvs,1):
    if bar==8:
        piano.append(ch("8:1",v,3.4,78))
    else:
        for i,beat in enumerate([1,1.5,2.5,3,4,4.5]):
            piano.append(n(f"{bar}:{beat:g}",v[[0,1,2,1,3,2][i]],.38,71+(7 if beat in (1,3) else 0)))
c["tracks"]["piano"]["sections"]["Victory Road"]={"loop_bars":8,"events":piano}

brass=[ch("1:1",["Bb3","F4","D5"],.8,94),ch("4:1",["A3","E4","C#5"],.8,101),ch("5:1",["D3","A3","D4","F4"],.9,106),ch("7:1",["A3","E4","C#5"],.9,105),ch("8:1",["D3","A3","D4","F4"],2.8,108)]
c["tracks"]["brass"]["sections"]["Victory Road"]={"loop_bars":8,"events":brass}

drums=[]
for bar in range(1,9):
    kicks=[1,2.5,3,3.75] if bar<7 else ([1,3] if bar==7 else [1])
    for beat in kicks:
        drums.append(d(f"{bar}:{beat:g}","kick",108 if beat in (1,3) else 90))
    if bar<8:
        for beat in (2,4):
            drums.append(d(f"{bar}:{beat}","snare",101 if bar<7 else 94))
    if bar<7:
        for step in range(8):
            drums.append(d(f"{bar}:{1+step*.5:g}","closed_hat",76+(8 if step%2==0 else -5),.08))
    if bar in (1,5,8):
        drums.append(d(f"{bar}:1","crash",110 if bar<8 else 102,.2))
    if bar==7:
        for beat,name,v in [(3,"low_tom",82),(3.5,"mid_tom",89),(4,"high_tom",98),(4.5,"snare",106)]:
            drums.append(d(f"{bar}:{beat:g}",name,v,.12))
c["tracks"]["drums"]["sections"]["Victory Road"]={"loop_bars":8,"events":drums}

# Prefer the foreground line wherever an identical string pitch would retrigger underneath it.
def pitch_number(value):
    if isinstance(value,int):
        return value
    letter=value[0].upper()
    accidental=1 if "#" in value else (-1 if "b" in value else 0)
    octave=int(value[2:] if accidental else value[1:])
    return (octave+1)*12+{"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}[letter]+accidental

for clip in c["tracks"]["strings"]["sections"].values():
    notes=[e for e in clip["events"] if e["type"]=="note"]
    other=[e for e in clip["events"] if e["type"]!="note"]
    kept=[]
    occupied={}
    for event in sorted(notes,key=lambda e:e["velocity"],reverse=True):
        bar,beat=event["at"].split(":")
        start=(int(bar)-1)*4+float(beat)-1
        end=start+float(event["duration"])
        spans=occupied.setdefault(pitch_number(event["pitch"]),[])
        if any(start < old_end and old_start < end for old_start,old_end in spans):
            continue
        spans.append((start,end))
        kept.append(event)
    clip["events"]=kept+other

text=json.dumps(c,ensure_ascii=False,indent=2)+"\n"
(root/"composition_final.json").write_text(text,encoding="utf-8")
(root/"composition.json").write_text(text,encoding="utf-8")
