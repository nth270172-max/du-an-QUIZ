import numpy as np, subprocess
SR=44100
INTRO,PERQ,OUTRO=5,11.5,5; ASK,COUNT=3.5,5; TOTAL=INTRO+PERQ*5+OUTRO
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","voice.mp3","-ac","1","-ar",str(SR),"-f","f32le","voice.raw"],check=True)
v=np.fromfile("voice.raw",dtype=np.float32)
# 12 đoạn (giây) từ silencedetect, ngưỡng nghỉ >=0.8s
segs=[(0,6.13),(7.05,10.03),(11.18,11.74),(13.02,16.18),(17.23,17.93),(19.12,22.87),(23.92,24.91),(26.17,29.55),(30.39,31.13),(32.19,35.16),(36.06,36.87),(38.05,42.76)]
place=[0.3]
for q in range(5):
    s=INTRO+q*PERQ; place+= [s+0.1, s+ASK+COUNT+0.15]
place.append(TOTAL-OUTRO+0.2)
mix=np.zeros(int(TOTAL*SR),dtype=np.float32)
def put(sig,t,g=1.0):
    i=int(t*SR); n=min(len(sig),len(mix)-i); mix[i:i+n]+=sig[:n]*g
for (a,b),t in zip(segs,place): put(v[int(a*SR):int(b*SR)],t)
tt=lambda d: np.arange(int(d*SR))/SR
def tone(f,d,env=0.004): x=tt(d); return (np.sin(2*np.pi*f*x)*np.exp(-x/env)).astype(np.float32)
tick=tone(1500,0.08,0.02)
ding=(tone(880,0.6,0.25)+tone(1320,0.6,0.2)*0.6).astype(np.float32)
for q in range(5):
    s=INTRO+q*PERQ+ASK
    for k in range(5): put(tick,s+k,0.5)
    put(ding,s+COUNT,0.6)
# nhạc nền pad nhẹ: vòng hợp âm, mỗi hợp âm 2s
chords=[(220,277.18,329.63),(174.61,220,261.63),(196,246.94,293.66),(164.81,207.65,246.94)]
music=np.zeros_like(mix); x=tt(2.0); env=np.minimum(1,np.minimum(x/0.3,(2.0-x)/0.3))
for i in range(int(TOTAL//2)+1):
    c=chords[i%4]; s=sum(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*2*f*x) for f in c)*env
    put(s.astype(np.float32),i*2.0,0.045)
mix+=music
mix=np.clip(mix,-1,1); mix.tofile("mix.raw")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","f32le","-ar",str(SR),"-ac","1","-i","mix.raw","-i","video2.mp4","-map","1:v","-map","0:a","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","quiz-mau-v2.mp4"],check=True)
print("done",TOTAL)
