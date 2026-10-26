import numpy as np, subprocess
SR=44100; TOTAL=72; ASK,COUNT=1.0,5
mix=np.zeros(int(TOTAL*SR),dtype=np.float32)
def put(sig,t,g=1.0):
    i=int(t*SR); n=max(0,min(len(sig),len(mix)-i))
    if n>0: mix[i:i+n]+=sig[:n]*g
tt=lambda d: np.arange(int(d*SR))/SR
def tone(f,d,env): x=tt(d); return (np.sin(2*np.pi*f*x)*np.exp(-x/env)).astype(np.float32)
tick=tone(1500,0.08,0.02); ding=(tone(880,0.7,0.25)+0.6*tone(1320,0.7,0.2)+0.4*tone(1760,0.7,0.15)).astype(np.float32)
whoosh=(np.random.RandomState(1).randn(int(0.4*SR))*np.exp(-tt(0.4)/0.09)*0.5).astype(np.float32)
pop=tone(600,0.12,0.03)+0.5*tone(1200,0.12,0.02)
riser=(np.sin(2*np.pi*(200+600*tt(1.2)/1.2)*tt(1.2))*np.linspace(0,0.5,int(1.2*SR))).astype(np.float32)
for s in [5,17,29,41,50,58,66]: put(whoosh,s,0.55)
for s in [5,17,29]:
    for k in range(5): put(tick,s+ASK+k,0.45)
    put(ding,s+ASK+COUNT,0.6)
for i in range(6): put(pop,58.2+i*0.35,0.5)
for i in range(3): put(pop,41.3+i*0.25,0.4)
put(riser,64.8,0.6); put(ding,66.8,0.5); put(pop,67.8,0.5)
# nhạc nền (như bản 3)
BPM=112; beat=60/BPM; chords=[[220,261.63,329.63],[174.61,220,261.63],[196,246.94,293.66],[164.81,207.65,246.94]]
music=np.zeros_like(mix)
def pluck(f,d): x=tt(d); return (np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x)+0.2*np.sin(2*np.pi*3*f*x))*np.exp(-x/0.18)
kick=(np.sin(2*np.pi*(55+90*np.exp(-tt(0.3)/0.04))*tt(0.3))*np.exp(-tt(0.3)/0.12)).astype(np.float32)
hat=(np.random.RandomState(2).randn(int(0.05*SR))*np.exp(-tt(0.05)/0.012)).astype(np.float32)
def mput(sig,t,g):
    i=int(t*SR); n=max(0,min(len(sig),len(music)-i))
    if n>0: music[i:i+n]+=sig[:n]*g
for b in range(int(TOTAL/beat)+1):
    t=b*beat; ch=chords[(b//8)%4]
    for k,sub in enumerate([0,0.5]):
        fq=ch[(b*2+k)%3]*(2 if (b+k)%4==3 else 1); mput(pluck(fq,0.45).astype(np.float32),t+sub*beat,0.11)
    if b%2==0: mput(kick,t,0.5); mput((np.sin(2*np.pi*(ch[0]/2)*tt(beat*2))*np.exp(-tt(beat*2)/0.5)).astype(np.float32),t,0.22)
    mput(hat,t+0.5*beat,0.06)
# nhạc to hơn ở hook và CTA, nhỏ ở các cảnh demo
gain=np.ones_like(music)
for a,b,g in [(5,41,0.75),(41,66,0.85)]: gain[int(a*SR):int(b*SR)]=g
mix+=music*gain
fo=int(1.5*SR); mix[-fo:]*=np.linspace(1,0,fo); fi=int(0.5*SR); mix[:fi]*=np.linspace(0,1,fi)
mix=np.clip(mix*1.1,-1,1); mix.tofile("mix4.raw")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","f32le","-ar",str(SR),"-ac","1","-i","mix4.raw","-i","video4.mp4","-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","quiz-gig-showreel.mp4"],check=True)
print("done")
