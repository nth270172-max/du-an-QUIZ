# Dựng video quiz mẫu 60s 16:9 — khung hình bằng Pillow, pipe sang ffmpeg
import math, subprocess, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1920,1080,30
BG=(11,27,58); WHITE=(255,255,255); TIMER=(255,196,61); GREEN=(76,217,100); DIM=(120,135,170)
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s): return ImageFont.truetype(F,s)

QUESTIONS=[("Whose eye is this?","CAT"),("Whose stripes are these?","TIGER"),
           ("Who stands on hooves like these?","MOUNTAIN GOAT"),("Whose eye is watching you?","OWL"),
           ("Whose skin is this?","ELEPHANT")]
INTRO,PERQ,OUTRO=5,11.5,5
ASK,COUNT,REVEAL=3.5,5,3
TOTAL=INTRO+PERQ*len(QUESTIONS)+OUTRO

# ---- ảnh gợi ý thay thế (procedural placeholder, sẽ thay bằng ảnh Flow) ----
IW,IH=1000,620
def clue_img(i):
    random.seed(i); img=Image.new("RGB",(IW,IH)); d=ImageDraw.Draw(img)
    if i==0:   # mắt mèo
        d.rectangle([0,0,IW,IH],fill=(40,60,30))
        d.ellipse([150,110,850,510],fill=(120,190,60)); d.ellipse([460,120,540,500],fill=(10,10,10))
        d.ellipse([600,170,680,250],fill=(230,255,220))
    elif i==1: # vằn hổ
        d.rectangle([0,0,IW,IH],fill=(225,120,30))
        for x in range(-200,IW,140): d.polygon([(x,0),(x+60,0),(x+180,IH),(x+90,IH)],fill=(20,15,10))
    elif i==2: # móng guốc trên đá
        d.rectangle([0,0,IW,IH],fill=(70,75,85))
        for _ in range(40): x,y=random.randint(0,IW),random.randint(200,IH); d.ellipse([x,y,x+random.randint(80,300),y+random.randint(40,120)],fill=(random.randint(80,120),)*3)
        d.polygon([(400,140),(600,140),(640,420),(360,420)],fill=(235,235,230)); d.rectangle([495,140,505,420],fill=(60,60,60))
    elif i==3: # mắt cú
        d.rectangle([0,0,IW,IH],fill=(60,45,30))
        d.ellipse([250,60,750,560],fill=(245,170,40)); d.ellipse([400,210,600,410],fill=(10,10,10)); d.ellipse([440,240,500,300],fill=WHITE)
    else:      # da voi
        a=np.random.RandomState(5).randint(95,135,(IH,IW)).astype(np.uint8); img=Image.fromarray(np.stack([a,a,a],2)).filter(ImageFilter.GaussianBlur(2)); d=ImageDraw.Draw(img)
        for _ in range(60): x1,y1=random.randint(0,IW),random.randint(0,IH); d.line([(x1,y1),(x1+random.randint(-200,200),y1+random.randint(-80,80))],fill=(60,60,65),width=random.randint(3,8))
        d.polygon([(700,IH),(820,IH),(980,300),(930,280)],fill=(240,235,220))
    return img
CLUES=[clue_img(i) for i in range(5)]

def rounded(d,box,r,fill,outline=None,w=0): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=w)
def center_text(d,txt,y,f,fill):
    w=d.textlength(txt,font=f); d.text(((W-w)/2,y),txt,font=f,fill=fill)

def base():
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    # bokeh nhẹ
    random.seed(1)
    for _ in range(18): x,y,r=random.randint(0,W),random.randint(0,H),random.randint(40,160); d.ellipse([x,y,x+r,y+r],fill=(20,45,95))
    img=img.filter(ImageFilter.GaussianBlur(30)); d=ImageDraw.Draw(img)
    d.text((60,40),"GUESS THE ANIMAL",font=font(36),fill=DIM)
    return img

def frame(t):
    img=base(); d=ImageDraw.Draw(img)
    if t<INTRO:
        k=min(1,t/0.6)
        center_text(d,"CAN YOU GUESS",250,font(int(110*k)+1),WHITE)
        center_text(d,"THE ANIMAL?",390,font(int(110*k)+1),TIMER)
        if t>1.2: center_text(d,"5 QUESTIONS  ·  5 SECONDS EACH",620,font(56),DIM)
        return img
    if t>=TOTAL-OUTRO:
        center_text(d,"HOW MANY DID YOU GET?",180,font(96),WHITE)
        for i in range(6):
            x=260+i*240; rounded(d,[x,420,x+180,600],28,(25,50,100),TIMER if i==5 else None,6)
            d.text((x+90-d.textlength(str(i),font=font(90))/2,445),str(i),font=font(90),fill=WHITE)
        d.text((W/2-d.textlength("/5",font=font(48))/2,630),"/5",font=font(48),fill=DIM)
        center_text(d,"SUBSCRIBE FOR MORE QUIZZES",820,font(64),GREEN)
        return img
    q=int((t-INTRO)//PERQ); lt=(t-INTRO)-q*PERQ; ask,ans=QUESTIONS[q]
    # thẻ câu hỏi
    rounded(d,[60,110,520,190],24,(25,50,100)); d.text((90,122),f"QUESTION {q+1} / 5",font=font(44),fill=TIMER)
    # ảnh gợi ý với zoom chậm
    z=1+0.05*min(lt,ASK+COUNT)/(ASK+COUNT); im=CLUES[q]
    cw,ch=int(IW*z),int(IH*z); im2=im.resize((cw,ch)).crop(((cw-IW)//2,(ch-IH)//2,(cw-IW)//2+IW,(ch-IH)//2+IH))
    mask=Image.new("L",(IW,IH),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,IW,IH],36,fill=255)
    img.paste(im2,(60,220),mask); d=ImageDraw.Draw(img)
    # câu hỏi
    y=260
    for line in ([ask] if d.textlength(ask,font=font(66))<760 else ask.split(" like ")):
        d.text((1120,y),line,font=font(66),fill=WHITE); y+=85
    if lt<ASK+COUNT:
        # timer vòng tròn
        rem=max(0,ASK+COUNT-lt); cx,cy,r=1500,720,180
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(30,55,110),width=26)
        frac=rem/COUNT if lt>=ASK else 1
        d.arc([cx-r,cy-r,cx+r,cy+r],-90,-90+360*frac,fill=TIMER,width=26)
        n=str(math.ceil(rem)) if lt>=ASK else "5"
        d.text((cx-d.textlength(n,font=font(170))/2,cy-105),n,font=font(170),fill=WHITE)
    else:
        rl=lt-ASK-COUNT; k=min(1,rl/0.35)
        rounded(d,[1120,560,1120+int(740*k),700],30,GREEN)
        if k>=1:
            f=font(84 if len(ans)<10 else 60); d.text((1120+370-d.textlength(ans,font=f)/2,580 if len(ans)<10 else 595),ans,font=f,fill=(10,30,20))
        d.text((1120,740),"✓" if False else "ANSWER",font=font(44),fill=DIM)
    return img

if __name__=="__main__":
    out=sys.argv[1] if len(sys.argv)>1 else "video.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","fast","-crf","20","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
    for n in range(int(TOTAL*FPS)):
        p.stdin.write(frame(n/FPS).tobytes())
    p.stdin.close(); p.wait(); print("video ok",TOTAL,"s")
