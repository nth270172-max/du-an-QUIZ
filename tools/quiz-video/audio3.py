import numpy as np, subprocess
SR=44100
INTRO,OUTRO=5,5; ASK,COUNT,REVEAL=1.5,5,3; PERQ=ASK+COUNT+REVEAL; TOTAL=INTRO+PERQ*5+OUTRO
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","voice.mp3","-ac","1","-ar",str(SR),"-f","f32le","voice.raw"],check=True)
v=np.fromfile("voice.raw",dtype=np.float32)
A=(0,6.13); C=(38.05,42.76); REV=[(11.18,11.74),(17.23,17.93),(23.92,24.91),(30.39,31.13),(36.06,36.87)]
mix=np.zeros(int(TOTAL*SR),dtype=np.float32)
def put(sig,t,g=1.0):
    i=int(t*SR); n=min(len(sig),len(mix)-i)
    if n>0: mix[i:i+n]+=sig[:n]*g
seg=lambda a,b: v[int(a*SR):int(b*SR)]
put(seg(*A),0.3)
for q in range(5): put(seg(*REV[q]),INTRO+q*PERQ+ASK+COUNT+0.2)
put(seg(*C),TOTAL-OUTRO+0.2)
tt=lambda d: np.arange(int(d*SR))/SR
def tone(f,d,env): x=tt(d); return (np.sin(2*np.pi*f*x)*np.exp(-x/env)).astype(np.float32)
tick=tone(1500,0.08,0.02); ding=(tone(880,0.7,0.25)+0.6*tone(1320,0.7,0.2)+0.4*tone(1760,0.7,0.15)).astype(np.float32)
whoosh=(np.random.RandomState(1).randn(int(0.35*SR))*np.exp(-tt(0.35)/0.08)*0.5).astype(np.float32)
for q in range(5):
    s=INTRO+q*PERQ; put(whoosh,s,0.5)
    for k in range(5): put(tick,s+ASK+k,0.45)
    put(ding,s+ASK+COUNT,0.6)
# nhạc nền: 112 BPM, 4 hợp âm, arpeggio + bass + kick mềm + hi-hat nhẹ
BPM=112; beat=60/BPM; chords=[[220,261.63,329.63],[174.61,220,261.63],[196,246.94,293.66],[164.81,207.65,246.94]]
music=np.zeros_like(mix)
def pluck(f,d): x=tt(d); return (np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x)+0.2*np.sin(2*np.pi*3*f*x))*np.exp(-x/0.18)
kick=(np.sin(2*np.pi*(55+90*np.exp(-tt(0.3)/0.04))*tt(0.3))*np.exp(-tt(0.3)/0.12)).astype(np.float32)
hat=(np.random.RandomState(2).randn(int(0.05*SR))*np.exp(-tt(0.05)/0.012)).astype(np.float32)
nb=int(TOTAL/beat)+2
for b in range(nb):
    t=b*beat; ch=chords[(b//8)%4]
    i=int(t*SR); 
    for k,sub in enumerate([0,0.5]):
        f=ch[(b*2+k)%3]*(2 if (b+k)%4==3 else 1); s=pluck(f,0.45).astype(np.float32); j=int((t+sub*beat)*SR); n=min(len(s),len(music)-j)
        if n>0: music[j:j+n]+=s[:n]*0.11
    if i>=len(music): break
    if b%2==0:
        n=min(len(kick),len(music)-i); music[i:i+n]+=kick[:n]*0.5
    j=int((t+0.5*beat)*SR); n=min(len(hat),len(music)-j)
    if n>0: music[j:j+n]+=hat[:n]*0.06
    bass=(np.sin(2*np.pi*(ch[0]/2)*tt(beat*2))*np.exp(-tt(beat*2)/0.5)).astype(np.float32)
    if b%2==0:
        n=max(0,min(len(bass),len(music)-i)); music[i:i+n]+=bass[:n]*0.22
# nén nhẹ nhạc khi có giọng (ducking)
env=np.convolve(np.abs(mix),np.ones(int(0.08*SR))/int(0.08*SR),mode="same")
duck=1-0.6*np.clip(env/0.05,0,1)
mix+=music*duck*0.9
# fade cuối
fo=int(1.2*SR); mix[-fo:]*=np.linspace(1,0,fo)
mix=np.clip(mix*1.1,-1,1); mix.tofile("mix3.raw")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","f32le","-ar",str(SR),"-ac","1","-i","mix3.raw","-i","video3.mp4","-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","quiz-mau-v3.mp4"],check=True)
print("done",TOTAL)
