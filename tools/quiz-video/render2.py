# Bản 2: bố cục chuẩn kênh quiz — 4 đáp án, trượt vào, timer phát sáng, pháo giấy, thanh tiến độ
import math, subprocess, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from render import clue_img  # dùng lại ảnh tạm; sẽ thay bằng ảnh Flow

W,H,FPS=1920,1080,30
FD="/usr/share/fonts/opentype/inter/"
def f(s,w="ExtraBold"): return ImageFont.truetype(FD+f"Inter-{w}.otf",s)
WHITE=(255,255,255); YEL=(255,205,70); GRN=(64,220,120); DIM=(150,165,200); CARD=(28,40,78); CARD2=(38,54,100)

Q=[("Whose eye is this?",["Snake","Cat","Crocodile","Lizard"],1),
   ("Whose stripes are these?",["Zebra","Bee","Tiger","Leopard"],2),
   ("Who stands on hooves like these?",["Horse","Mountain Goat","Deer","Camel"],1),
   ("Whose eye is watching you?",["Eagle","Frog","Cat","Owl"],3),
   ("Whose skin is this?",["Rhino","Hippo","Whale","Elephant"],3)]
INTRO,PERQ,OUTRO=5,11.5,5; ASK,COUNT,REVEAL=3.5,5,3
TOTAL=INTRO+PERQ*5+OUTRO
ease=lambda k: 1-(1-max(0,min(1,k)))**3

# ---- nền: gradient + quầng sáng + viền tối (tính một lần) ----
y=np.linspace(0,1,H)[:,None]; x=np.linspace(0,1,W)[None,:]
top=np.array([14,22,58]); bot=np.array([38,22,80])
bg=(top[None,None,:]*(1-y)[...,None]+bot[None,None,:]*y[...,None])*np.ones((1,W,1))
glow=np.exp(-(((x-0.18)**2)/0.08+((y-0.15)**2)/0.12))[...,None]*np.array([30,60,140])
vig=1-0.55*np.clip(((x-0.5)**2*2.2+(y-0.5)**2*2.6),0,1)
BASE=Image.fromarray(np.clip((bg+glow)*vig[...,None],0,255).astype(np.uint8))
# hạt sáng nhỏ
d=ImageDraw.Draw(BASE); random.seed(7)
for _ in range(60):
    px,py,r=random.randint(0,W),random.randint(0,H),random.randint(1,3); d.ellipse([px,py,px+r,py+r],fill=(90,110,170))

IW,IH=980,600
CLUES=[clue_img(i).resize((IW,IH)) for i in range(5)]
MASK=Image.new("L",(IW,IH),0); ImageDraw.Draw(MASK).rounded_rectangle([0,0,IW,IH],40,fill=255)
SHADOW=Image.new("RGBA",(IW+160,IH+160),(0,0,0,0)); ImageDraw.Draw(SHADOW).rounded_rectangle([80,100,80+IW,100+IH],40,fill=(0,0,0,170)); SHADOW=SHADOW.filter(ImageFilter.GaussianBlur(28))
random.seed(3); CONF=[(random.random(),random.random()*1.3,random.choice([YEL,GRN,(255,90,120),(90,170,255),WHITE]),random.randint(10,22),random.random()*6) for _ in range(140)]

def ctext(d,txt,cy,fnt,fill,cx=W/2):
    w=d.textlength(txt,font=fnt); d.text((cx-w/2,cy),txt,font=fnt,fill=fill)

def card(img,box,a,b=28,outline=None,w=0):
    fill,r=(a,b) if isinstance(a,tuple) else (b,a)
    ImageDraw.Draw(img).rounded_rectangle(box,r,fill=fill,outline=outline,width=w)

def glow_arc(img,cx,cy,r,frac,color):
    L=Image.new("RGBA",(2*r+120,2*r+120),(0,0,0,0)); g=ImageDraw.Draw(L); o=60
    g.arc([o,o,o+2*r,o+2*r],-90,-90+360*frac,fill=color+(255,),width=22)
    img.paste(L.filter(ImageFilter.GaussianBlur(14)),(cx-r-60,cy-r-60),L.filter(ImageFilter.GaussianBlur(14)))
    img.paste(L,(cx-r-60,cy-r-60),L)

def header(img,d,q=None):
    card(img,[60,46,440,106],30,CARD); d.text((88,60),"🐾 GUESS THE ANIMAL".replace("🐾 ",""),font=f(28,"SemiBold"),fill=DIM)
    for i in range(5):
        x=W/2-5*34/2+i*34+6
        col=YEL if (q is not None and i<=q) else (60,75,120)
        d.rounded_rectangle([x,66,x+22,86],6,fill=col)
    if q is not None: d.text((1740,58),f"{q+1} / 5",font=f(34,"Bold"),fill=WHITE)

def frame(t):
    img=BASE.copy(); d=ImageDraw.Draw(img)
    if t<INTRO:
        header(img,d); k=ease(t/0.7)
        ctext(d,"CAN YOU GUESS",250-40*(1-k),f(120,"Black"),WHITE); ctext(d,"THE ANIMAL?",380,f(120,"Black"),YEL)
        if t>0.9:
            k2=ease((t-0.9)/0.5); ctext(d,"5 QUESTIONS  •  5 SECONDS EACH",560,f(48,"SemiBold"),DIM)
            for i in range(5):
                ki=ease((t-1.3-i*0.12)/0.4); tw,th=300,184; x=int(W/2-5*320/2+i*320+10); yy=int(680+40*(1-ki))
                th_img=CLUES[i].resize((tw,th)); m=Image.new("L",(tw,th),0); ImageDraw.Draw(m).rounded_rectangle([0,0,tw,th],22,fill=int(255*ki)); img.paste(th_img,(x,yy),m)
        return img
    if t>=TOTAL-OUTRO:
        header(img,d,4); ctext(d,"HOW MANY DID YOU GET?",150,f(96,"Black"),WHITE)
        for i in range(6):
            x=240+i*250; k=ease((t-(TOTAL-OUTRO)-i*0.08)/0.4); yy=int(380+30*(1-k))
            card(img,[x,yy,x+200,yy+200],CARD2 if i<5 else (70,55,20),30,YEL if i==5 else None,5)
            d.text((x+100-d.textlength(str(i),font=f(96,"Black"))/2,yy+40),str(i),font=f(96,"Black"),fill=WHITE if i<5 else YEL)
        ctext(d,"out of 5 — tell me in the comments",640,f(40,"SemiBold"),DIM)
        p=1+0.04*math.sin(t*6); bw,bh=int(620*p),int(110*p)
        card(img,[W/2-bw/2,850-bh/2,W/2+bw/2,850+bh/2],(230,40,60),34); ctext(d,"SUBSCRIBE",850-28,f(56,"Black"),WHITE)
        return img
    q=int((t-INTRO)//PERQ); lt=(t-INTRO)-q*PERQ; ask,opts,ans=Q[q]; header(img,d,q)
    k=ease(lt/0.45); reveal=lt>=ASK+COUNT; rl=lt-ASK-COUNT
    if reveal:
        for (px,py,col,sz,rot) in CONF:
            yy=(py+rl*0.55)%1.3-0.15; xx=px+0.03*math.sin(rl*4+rot); X,Y=int(xx*W),int(yy*H)
            d.rounded_rectangle([X,Y,X+sz,Y+sz*0.6],3,fill=col)
    # thẻ ảnh trượt vào từ trái
    x0=int(70-500*(1-k)); img.paste(SHADOW,(x0-80,250-100),SHADOW)
    z=1+0.06*min(lt,ASK+COUNT)/(ASK+COUNT); cw,ch=int(IW*z),int(IH*z)
    im=CLUES[q].resize((cw,ch)).crop(((cw-IW)//2,(ch-IH)//2,(cw-IW)//2+IW,(ch-IH)//2+IH)); img.paste(im,(x0,250),MASK)
    d=ImageDraw.Draw(img); d.rounded_rectangle([x0,250,x0+IW,250+IH],40,outline=(255,255,255,60),width=3)
    # câu hỏi
    fq=f(58,"ExtraBold"); lines=[ask] if d.textlength(ask,font=fq)<760 else [" ".join(ask.split()[:3])," ".join(ask.split()[3:])]
    yy=240
    for ln in lines: d.text((1110,yy),ln,font=fq,fill=WHITE); yy+=72
    # 4 đáp án 2x2
    ox,oy,bw,bh,gap=1110,400,360,96,18
    for i,o in enumerate(opts):
        ki=ease((lt-0.25-i*0.08)/0.35); bx=ox+(i%2)*(bw+gap); by=oy+(i//2)*(bh+gap)+int(30*(1-ki))
        if reveal and i==ans: fill,txt,bd=GRN,(8,30,18),None
        elif reveal: fill,txt,bd=(26,34,62),(90,100,130),None
        else: fill,txt,bd=CARD2,WHITE,(70,90,150)
        card(img,[bx,by,bx+bw,by+bh],fill,24,bd,2)
        d.ellipse([bx+16,by+24,bx+64,by+72],fill=(60,78,130) if not(reveal and i==ans) else (8,30,18)); d.text((bx+40-d.textlength("ABCD"[i],font=f(28,"Black"))/2,by+34),"ABCD"[i],font=f(28,"Black"),fill=WHITE if not(reveal and i==ans) else GRN)
        d.text((bx+84,by+30),o,font=f(34 if len(o)<12 else 28,"Bold"),fill=txt)
    # timer / lộ đáp án
    cx,cy,r=1500,790,105
    if not reveal:
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(40,55,100),width=22)
        rem=ASK+COUNT-lt; frac=min(1,rem/COUNT); glow_arc(img,cx,cy,r,frac,YEL if rem>2 else (255,90,90)); d=ImageDraw.Draw(img)
        n=str(math.ceil(rem)) if lt>=ASK else "5"; d.text((cx-d.textlength(n,font=f(110,"Black"))/2,cy-66),n,font=f(110,"Black"),fill=WHITE)
        d.text((cx-d.textlength("SECONDS",font=f(22,"SemiBold"))/2,cy+r+16),"SECONDS",font=f(22,"SemiBold"),fill=DIM)
    else:
        kr=ease(rl/0.4); card(img,[1110,720,1110+int(740*kr),860],GRN,28)
        if kr>=1: ctext(d,"✓ CORRECT: "+opts[ans].upper() if False else "CORRECT: "+opts[ans].upper(),762,f(46,"Black"),(8,30,18),1480)
    # thanh tiến độ thời gian câu
    d.rounded_rectangle([60,1020,1860,1034],7,fill=(35,48,90)); d.rounded_rectangle([60,1020,60+int(1800*min(1,lt/PERQ)),1034],7,fill=YEL)
    return img

if __name__=="__main__":
    out=sys.argv[1] if len(sys.argv)>1 else "video2.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
    for n in range(int(TOTAL*FPS)): p.stdin.write(frame(n/FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("ok")
