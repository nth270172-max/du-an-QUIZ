# Bản 4: SHOWREEL gig — cho khách thấy có thể làm gì: 3 dạng quiz, 3 giao diện, đổi thương hiệu, Shorts, thumbnail lô, checklist, CTA
import math, subprocess, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1920,1080,30
FD="/usr/share/fonts/opentype/inter/"
def f(s,w="ExtraBold"): return ImageFont.truetype(FD+f"Inter-{w}.otf",s)
EF=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)
WHITE=(255,255,255)
ease=lambda k: 1-(1-max(0,min(1,k)))**3
def emoji(ch,size):
    im=Image.new("RGBA",(136,136),(0,0,0,0)); ImageDraw.Draw(im).text((4,4),ch,font=EF,embedded_color=True)
    return im.resize((size,size),Image.LANCZOS)
def pixelate(im,block):
    n=max(2,int(im.width/block)); return im.resize((n,n),Image.BILINEAR).resize(im.size,Image.NEAREST)

# ---- bảng màu (3 giao diện) ----
THEMES={
 "animal":dict(top=(14,22,58),bot=(38,22,80),acc=(255,205,70),ok=(64,220,120),card=(38,54,100),dim=(150,165,200),name="GUESS THE ANIMAL"),
 "flag":  dict(top=(8,40,48), bot=(10,70,80), acc=(255,255,255),ok=(255,90,90), card=(18,88,100),dim=(150,200,205),name="GUESS THE FLAG"),
 "trivia":dict(top=(40,12,70), bot=(80,20,110),acc=(90,230,255), ok=(255,210,60),card=(90,40,140),dim=(190,160,220),name="GENERAL KNOWLEDGE"),
 "brandA":dict(top=(120,20,30),bot=(60,10,20),acc=(255,220,80),ok=(80,220,140),card=(150,40,50),dim=(240,180,180),name="YOUR LOGO"),
 "brandB":dict(top=(10,60,40),bot=(5,30,25),acc=(255,255,255),ok=(255,200,60),card=(20,100,70),dim=(160,220,190),name="YOUR LOGO"),
 "brandC":dict(top=(245,245,250),bot=(225,228,240),acc=(20,20,40),ok=(40,180,100),card=(255,255,255),dim=(110,115,140),name="YOUR LOGO",light=True),
}
_BG={}
def bgimg(th):
    if th in _BG: return _BG[th]
    T=THEMES[th]; y=np.linspace(0,1,H)[:,None,None]; top=np.array(T["top"])[None,None,:]; bot=np.array(T["bot"])[None,None,:]
    bg=(top*(1-y)+bot*y)*np.ones((1,W,1)); x=np.linspace(0,1,W)[None,:]
    g=np.exp(-(((x-0.2)**2)/0.08+((np.linspace(0,1,H)[:,None]-0.15)**2)/0.12))[...,None]
    bg=bg+g*(np.array([40,40,40]) if not T.get("light") else np.array([10,10,10]))
    vig=1-(0.5 if not T.get("light") else 0.08)*np.clip(((x-0.5)**2*2.2+(np.linspace(0,1,H)[:,None]-0.5)**2*2.6),0,1)
    im=Image.fromarray(np.clip(bg*vig[...,None],0,255).astype(np.uint8)); d=ImageDraw.Draw(im); random.seed(7)
    if not T.get("light"):
        for _ in range(60): px,py,r=random.randint(0,W),random.randint(0,H),random.randint(1,3); d.ellipse([px,py,px+r,py+r],fill=tuple(min(255,c+70) for c in T["card"]))
    _BG[th]=im; return im
def card(d,box,fill,r=28,outline=None,w=0): d.rounded_rectangle(box,r,fill=fill,outline=outline,width=w)
def ct(d,t,y,fnt,fill,cx=W/2): d.text((cx-d.textlength(t,font=fnt)/2,y),t,font=fnt,fill=fill)
def shadow(img,box,r=40,blur=26,alpha=160):
    x0,y0,x1,y1=box; L=Image.new("RGBA",(x1-x0+160,y1-y0+160),(0,0,0,0)); ImageDraw.Draw(L).rounded_rectangle([80,100,80+x1-x0,100+y1-y0],r,fill=(0,0,0,alpha)); L=L.filter(ImageFilter.GaussianBlur(blur)); img.paste(L,(x0-80,y0-80),L)
def glow_arc(img,cx,cy,r,frac,color):
    L=Image.new("RGBA",(2*r+120,2*r+120),(0,0,0,0)); o=60; ImageDraw.Draw(L).arc([o,o,o+2*r,o+2*r],-90,-90+360*frac,fill=color+(255,),width=22)
    B=L.filter(ImageFilter.GaussianBlur(14)); img.paste(B,(cx-r-60,cy-r-60),B); img.paste(L,(cx-r-60,cy-r-60),L)
random.seed(3); CONF=[(random.random(),random.random()*1.3,random.choice([(255,205,70),(64,220,120),(255,90,120),(90,170,255),WHITE]),random.randint(10,22),random.random()*6) for _ in range(110)]
def confetti(d,rl):
    for (px,py,c,sz,rot) in CONF:
        yy=(py+rl*0.55)%1.3-0.15; xx=px+0.03*math.sin(rl*4+rot); X,Y=int(xx*W),int(yy*H); d.rounded_rectangle([X,Y,X+sz,Y+sz*0.6],3,fill=c)

ASK,COUNT,REVEAL=1.0,5,3; QDUR=ASK+COUNT+REVEAL
def header(img,d,T,label,q=1,n=5):
    tx=T["acc"] if not T.get("light") else (20,20,40)
    card(d,[60,46,60+40+int(d.textlength(label,font=f(28,"SemiBold")))+40,106],T["card"],30); d.text((88,60),label,font=f(28,"SemiBold"),fill=T["dim"])
    for i in range(n):
        x=W/2-n*34/2+i*34+6; d.rounded_rectangle([x,66,x+22,86],6,fill=T["acc"] if i<q else T["card"])
    d.text((1740,58),f"{q} / {n}",font=f(34,"Bold"),fill=tx)
def progress(d,T,lt):
    d.rounded_rectangle([60,1020,1860,1034],7,fill=T["card"]); d.rounded_rectangle([60,1020,60+int(1800*min(1,lt/QDUR)),1034],7,fill=T["acc"])
def options(img,d,T,opts,ai,lt,reveal,ox,oy,bw,bh,gap,cols=2,fs=34):
    tx=WHITE if not T.get("light") else (20,20,40)
    for i,o in enumerate(opts):
        ki=ease((lt-0.2-i*0.08)/0.35); bx=ox+(i%cols)*(bw+gap); by=oy+(i//cols)*(bh+gap)+int(30*(1-ki))
        if reveal and i==ai: fill,txt,bd=T["ok"],(8,30,18),None
        elif reveal: fill,txt,bd=tuple(int(c*0.6) for c in T["card"]),T["dim"],None
        else: fill,txt,bd=T["card"],tx,tuple(min(255,c+40) for c in T["card"])
        card(d,[bx,by,bx+bw,by+bh],fill,24,bd,2)
        d.ellipse([bx+16,by+bh//2-24,bx+64,by+bh//2+24],fill=tuple(min(255,c+25) for c in T["card"]) if not(reveal and i==ai) else (8,30,18))
        d.text((bx+40-d.textlength("ABCD"[i],font=f(28,"Black"))/2,by+bh//2-18),"ABCD"[i],font=f(28,"Black"),fill=txt if not(reveal and i==ai) else T["ok"])
        d.text((bx+84,by+bh//2-fs//2-3),o,font=f(fs,"Bold"),fill=txt)
def timer(img,d,T,cx,cy,r,lt):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=T["card"],width=22); rem=ASK+COUNT-lt; frac=min(1,rem/COUNT)
    glow_arc(img,cx,cy,r,frac,T["acc"] if rem>2 else (255,90,90)); d=ImageDraw.Draw(img)
    n=str(math.ceil(rem)) if lt>=ASK else "5"; tx=WHITE if not T.get("light") else (20,20,40)
    d.text((cx-d.textlength(n,font=f(int(r*1.05),"Black"))/2,cy-int(r*0.63)),n,font=f(int(r*1.05),"Black"),fill=tx); return d

# ---- Dạng 1: động vật (thẻ trái, đáp án phải) ----
CAT=emoji("🐱",470); TIGER=emoji("🐯",470)
def quiz_animal(th,lt,q=1,em=CAT,ans="Cat",opts=("Snake","Cat","Fox","Lizard"),ai=1,logo=None):
    T=THEMES[th]; img=bgimg(th).copy(); d=ImageDraw.Draw(img); reveal=lt>=ASK+COUNT; rl=lt-ASK-COUNT
    if reveal: confetti(d,rl)
    header(img,d,T,T["name"] if not logo else logo,q)
    k=ease(lt/0.45); x0=int(70-500*(1-k)); IW,IH=980,600; shadow(img,[x0,250,x0+IW,250+IH]); d=ImageDraw.Draw(img)
    card(d,[x0,250,x0+IW,250+IH],tuple(int(c*0.8) for c in T["card"]) if not T.get("light") else (255,255,255),40,(255,255,255) if not T.get("light") else (215,218,230),3)
    cx,cy=x0+IW//2,250+IH//2
    if not reveal:
        prog=max(0,lt-ASK)/COUNT; e=pixelate(em,int(64-54*prog)); img.paste(e,(cx-235,cy-235),e); d=ImageDraw.Draw(img)
        card(d,[x0+IW-130,274,x0+IW-24,380],WHITE,53); d.text((x0+IW-77-d.textlength("?",font=f(70,"Black"))/2,286),"?",font=f(70,"Black"),fill=(20,30,70))
    else:
        sc=1+0.22*math.sin(min(1,rl/0.5)*math.pi); s=int(470*sc); e=em.resize((s,s),Image.LANCZOS)
        L=Image.new("RGBA",(700,700),(0,0,0,0)); ImageDraw.Draw(L).ellipse([80,80,620,620],outline=T["acc"]+(255,),width=18); L=L.filter(ImageFilter.GaussianBlur(22)); img.paste(L,(cx-350,cy-350),L)
        img.paste(e,(cx-s//2,cy-s//2),e); d=ImageDraw.Draw(img)
    tx=WHITE if not T.get("light") else (20,20,40)
    d.text((1110,240),"Which animal is this?",font=f(58,"ExtraBold"),fill=tx)
    options(img,d,T,opts,ai,lt,reveal,1110,400,360,96,18)
    if not reveal: d=timer(img,d,T,1500,790,105,lt)
    else:
        kr=ease(rl/0.4); card(d,[1110,720,1110+int(740*kr),860],T["ok"],28)
        if kr>=1: ct(d,"IT'S A "+ans.upper()+"!",762,f(46,"Black"),(8,30,18),1480)
    progress(d,T,lt); return img

# ---- Dạng 2: quốc kỳ (cờ giữa trên, 4 đáp án hàng ngang) ----
FLAG=emoji("🇧🇷",420)
def quiz_flag(th,lt):
    T=THEMES[th]; img=bgimg(th).copy(); d=ImageDraw.Draw(img); reveal=lt>=ASK+COUNT; rl=lt-ASK-COUNT
    if reveal: confetti(d,rl)
    header(img,d,T,T["name"],3,10)
    ct(d,"Which country does this flag belong to?",150,f(56,"ExtraBold"),WHITE)
    k=ease(lt/0.5); cx,cy=W//2,520; s=int(420*(0.7+0.3*k))
    shadow(img,[cx-300,cy-190,cx+300,cy+190],36,24); d=ImageDraw.Draw(img)
    card(d,[cx-300,cy-190,cx+300,cy+190],T["card"],36,(255,255,255),3)
    e=FLAG.resize((s,s),Image.LANCZOS) if not reveal else FLAG.resize((int(420*(1+0.1*math.sin(min(1,rl/0.5)*math.pi))),)*2,Image.LANCZOS)
    if not reveal and lt<ASK+COUNT: e=pixelate(e,int(40-34*max(0,lt-ASK)/COUNT)) if lt<ASK+COUNT*0.85 else e
    img.paste(e,(cx-e.width//2,cy-e.height//2),e); d=ImageDraw.Draw(img)
    options(img,d,T,["Argentina","Brazil","Portugal","Mexico"],1,lt,reveal,140,780,390,100,22,cols=4,fs=32)
    if not reveal: d=timer(img,d,T,1660,520,95,lt)
    else:
        kr=ease(rl/0.4); card(d,[W//2-200,920,W//2-200+int(400*kr),990],T["ok"],22)
        if kr>=1: ct(d,"BRAZIL",934,f(38,"Black"),(30,10,10))
    progress(d,T,lt); return img

# ---- Dạng 3: kiến thức chung (câu hỏi chữ lớn, đáp án 2x2 toàn khung) ----
def quiz_trivia(th,lt):
    T=THEMES[th]; img=bgimg(th).copy(); d=ImageDraw.Draw(img); reveal=lt>=ASK+COUNT; rl=lt-ASK-COUNT
    if reveal: confetti(d,rl)
    header(img,d,T,T["name"],7,10)
    k=ease(lt/0.5); shadow(img,[160,200,1760,440],36,24); d=ImageDraw.Draw(img); card(d,[160,200,1760,440],T["card"],36)
    d.text((200,235),"QUESTION 7",font=f(28,"SemiBold"),fill=T["dim"])
    ct(d,"Which planet has the most moons?",300,f(62,"ExtraBold"),WHITE)
    options(img,d,T,["Jupiter","Saturn","Neptune","Uranus"],1,lt,reveal,160,520,780,130,40,cols=2,fs=40)
    if not reveal: d=timer(img,d,T,W//2,900,80,lt)
    else:
        kr=ease(rl/0.4); card(d,[W//2-330,840,W//2-330+int(660*kr),960],T["ok"],28)
        if kr>=1: ct(d,"SATURN — 146 MOONS",872,f(44,"Black"),(30,20,10))
    progress(d,T,lt); return img

# ---- Shorts dọc (1080x1920) ----
def shorts_frame(lt):
    T=THEMES["animal"]; img=Image.new("RGB",(1080,1920)); bg=bgimg("animal").resize((1080,608)); 
    y=np.linspace(0,1,1920)[:,None,None]; arr=(np.array(T["top"])[None,None,:]*(1-y)+np.array(T["bot"])[None,None,:]*y)*np.ones((1,1080,1)); img=Image.fromarray(arr.astype(np.uint8)); d=ImageDraw.Draw(img)
    reveal=lt>=ASK+COUNT; rl=lt-ASK-COUNT
    card(d,[60,80,560,150],T["card"],35); d.text((95,97),"GUESS THE ANIMAL",font=f(32,"SemiBold"),fill=T["dim"])
    ct(d,"Which animal is this?",260,f(72,"ExtraBold"),WHITE,540)
    card(d,[90,400,990,1120],tuple(int(c*0.8) for c in T["card"]),48,WHITE,4)
    em=CAT.resize((600,600),Image.LANCZOS)
    e=pixelate(em,int(80-68*max(0,lt-ASK)/COUNT)) if not reveal else em.resize((int(600*(1+0.15*math.sin(min(1,rl/0.5)*math.pi))),)*2,Image.LANCZOS)
    img.paste(e,(540-e.width//2,760-e.height//2),e); d=ImageDraw.Draw(img)
    for i,o in enumerate(["Snake","Cat","Fox","Lizard"]):
        bx=90+(i%2)*460; by=1200+(i//2)*150
        fill=T["ok"] if (reveal and i==1) else T["card"]; card(d,[bx,by,bx+440,by+120],fill,30)
        d.text((bx+40,by+38),"ABCD"[i]+"   "+o,font=f(40,"Bold"),fill=WHITE if not(reveal and i==1) else (8,30,18))
    if not reveal:
        cx,cy,r=540,1660,110; d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=T["card"],width=24); rem=ASK+COUNT-lt
        d.arc([cx-r,cy-r,cx+r,cy+r],-90,-90+360*min(1,rem/COUNT),fill=T["acc"],width=24); n=str(math.ceil(rem)); d.text((cx-d.textlength(n,font=f(120,"Black"))/2,cy-78),n,font=f(120,"Black"),fill=WHITE)
    else: card(d,[140,1600,940,1720],T["ok"],30); ct(d,"IT'S A CAT!",1630,f(56,"Black"),(8,30,18),540)
    return img

def thumb(label,em,num,th):
    T=THEMES[th]; im=bgimg(th).resize((480,270)); d=ImageDraw.Draw(im)
    e=emoji(em,200); im.paste(e,(270,50),e); d=ImageDraw.Draw(im)
    d.text((24,30),label,font=f(44,"Black"),fill=T["acc"]); d.text((24,90),"QUIZ",font=f(60,"Black"),fill=WHITE)
    card(d,[24,200,150,250],T["ok"],14); d.text((44,210),f"#{num}",font=f(30,"Black"),fill=(10,20,10))
    d.rounded_rectangle([0,0,479,269],18,outline=WHITE,width=3); return im

def label_chip(img,d,text,sub,t):
    k=ease(t/0.5); x=int(60-400*(1-k))
    shadow(img,[x,120,x+700,235],28,18,120); d=ImageDraw.Draw(img); card(d,[x,120,x+700,235],(255,255,255),28)
    d.text((x+30,135),text,font=f(26,"Bold"),fill=(90,100,130)); d.text((x+30,168),sub,font=f(40,"Black"),fill=(20,24,50)); return d

# ---- Lịch cảnh ----
S=[("hook",0,5),("animal",5,17),("flag",17,29),("trivia",29,41),("brand",41,50),("shorts",50,58),("get",58,66),("cta",66,72)]
TOTAL=72
def fade_in(img,k):
    if k>=1: return img
    return Image.blend(Image.new("RGB",img.size,(8,10,24)),img,max(0,k))

def frame(t):
    for name,a,b in S:
        if a<=t<b: lt=t-a; break
    if name=="hook":
        img=bgimg("animal").copy(); d=ImageDraw.Draw(img)
        k1=ease(lt/0.6); k2=ease((lt-0.5)/0.6); k3=ease((lt-1.3)/0.6)
        ct(d,"YOUR QUIZ CHANNEL,",300-50*(1-k1),f(116,"Black"),WHITE)
        if lt>0.5: ct(d,"ON AUTOPILOT.",440-50*(1-k2),f(116,"Black"),(255,205,70))
        if lt>1.3: ct(d,"Ready-to-upload quiz videos  •  delivered in 24–48h",640,f(42,"SemiBold"),(150,165,200))
        if lt>2.0:
            for i,e in enumerate(["🐱","🇧🇷","🧠","🎵","🏆"]):
                ki=ease((lt-2.0-i*0.1)/0.4); im=emoji(e,int(150*ki)+1); img.paste(im,(int(W/2-5*190/2+i*190+95-im.width/2),int(820-im.height/2)),im)
        return fade_in(img,lt/0.4)
    if name=="animal":
        img=quiz_animal("animal",min(lt,QDUR-0.01) if lt<QDUR else QDUR-0.01); d=ImageDraw.Draw(img)
        if lt<3.5: label_chip(img,d,"FORMAT 01","Guess the Animal",lt)
        return fade_in(img,lt/0.3)
    if name=="flag":
        img=quiz_flag("flag",min(lt,QDUR-0.01)); d=ImageDraw.Draw(img)
        if lt<3.5: label_chip(img,d,"FORMAT 02","Guess the Flag",lt)
        return fade_in(img,lt/0.3)
    if name=="trivia":
        img=quiz_trivia("trivia",min(lt,QDUR-0.01)); d=ImageDraw.Draw(img)
        if lt<3.5: label_chip(img,d,"FORMAT 03","General Knowledge Trivia",lt)
        return fade_in(img,lt/0.3)
    if name=="brand":
        img=bgimg("animal").copy(); d=ImageDraw.Draw(img)
        ct(d,"YOUR BRAND. YOUR COLORS. YOUR LOGO.",90,f(64,"Black"),WHITE); ct(d,"Same template, restyled to match your channel",175,f(34,"SemiBold"),(150,165,200))
        for i,th in enumerate(["brandA","brandB","brandC"]):
            ki=ease((lt-0.3-i*0.25)/0.5)
            if ki<=0: continue
            sub=quiz_animal(th,(lt*1.6)%QDUR,logo="YOUR LOGO").resize((560,315),Image.LANCZOS)
            x=int(100+i*600); y=int(330+40*(1-ki)); shadow(img,[x,y,x+560,y+315],20,18,140); img.paste(sub,(x,y)); d=ImageDraw.Draw(img); d.rounded_rectangle([x,y,x+560,y+315],20,outline=WHITE,width=3)
            ct(d,["Red & Gold","Forest Green","Clean Light"][i],680,f(30,"Bold"),WHITE,x+280)
        if lt>1.5: ct(d,"Logo on every frame  •  colors matched to your thumbnails  •  consistent across the whole series",820,f(30,"SemiBold"),(150,165,200))
        return fade_in(img,lt/0.3)
    if name=="shorts":
        img=bgimg("trivia").copy(); d=ImageDraw.Draw(img)
        ct(d,"LANDSCAPE + VERTICAL SHORTS",80,f(64,"Black"),WHITE); ct(d,"Every quiz can ship as a 9:16 version for Shorts, Reels and TikTok",165,f(32,"SemiBold"),(190,160,220))
        k=ease(lt/0.6)
        land=quiz_animal("animal",(lt*1.4)%QDUR).resize((900,506),Image.LANCZOS); x=int(140-300*(1-k)); shadow(img,[x,330,x+900,836],24,20,150); img.paste(land,(x,330)); d=ImageDraw.Draw(img); d.rounded_rectangle([x,330,x+900,836],24,outline=WHITE,width=3)
        ph=shorts_frame((lt*1.4)%QDUR).resize((360,640),Image.LANCZOS); px=int(1300+300*(1-k)); shadow(img,[px,250,px+360,890],44,20,150); d=ImageDraw.Draw(img)
        card(d,[px-14,236,px+374,904],(20,20,30),52,(80,80,100),3); m=Image.new("L",(360,640),0); ImageDraw.Draw(m).rounded_rectangle([0,0,359,639],40,fill=255); img.paste(ph,(px,250),m); d=ImageDraw.Draw(img)
        card(d,[px+120,262,px+240,282],(20,20,30),10)
        ct(d,"16:9  •  1080p / 4K",900,f(28,"Bold"),WHITE,x+450); ct(d,"9:16  •  Shorts",940,f(28,"Bold"),WHITE,px+180)
        return fade_in(img,lt/0.3)
    if name=="get":
        img=bgimg("animal").copy(); d=ImageDraw.Draw(img)
        ct(d,"WHAT YOU GET IN EVERY ORDER",80,f(64,"Black"),(255,205,70))
        items=[("✓","Original, fact-checked questions (or use yours)"),("✓","Countdown timer, reveal animation, score screen"),("✓","AI voiceover + royalty-free music"),("✓","Your logo and colors on every frame"),("✓","Thumbnails, titles and descriptions (Batch of 10)"),("✓","MP4 1080p/4K + question sheet, delivered in 24–48h")]
        for i,(c,txt) in enumerate(items):
            ki=ease((lt-0.2-i*0.35)/0.4)
            if ki<=0: continue
            y=int(210+i*125+30*(1-ki)); card(d,[260,y,1660,y+100],(38,54,100),24); d.ellipse([290,y+22,346,y+78],fill=(64,220,120)); d.text((306,y+30),"✓",font=f(36,"Black"),fill=(8,30,18)); d.text((380,y+28),txt,font=f(38,"Bold"),fill=WHITE)
        return fade_in(img,lt/0.3)
    if name=="cta":
        img=bgimg("animal").copy(); d=ImageDraw.Draw(img)
        for i,(lab,em,th) in enumerate([("ANIMAL","🐱","animal"),("FLAG","🇯🇵","flag"),("TRIVIA","🧠","trivia"),("ANIMAL","🦉","animal")]):
            ki=ease((lt-0.1-i*0.12)/0.4); x=int(110+i*440); y=int(120+40*(1-ki)); tb=thumb(lab,em,12+i,th); shadow(img,[x,y,x+480,y+270],18,16,140); img.paste(tb,(x,y)); d=ImageDraw.Draw(img)
        ct(d,"BATCH OF 10  •  SAME LOOK, SAME VOICE, SAME PACING",430,f(34,"Bold"),(150,165,200))
        k=ease((lt-0.8)/0.6)
        ct(d,"SEND YOUR CHANNEL LINK",560-30*(1-k),f(96,"Black"),WHITE)
        if lt>1.2: ct(d,"GET A FREE SAMPLE IN 24H",690,f(72,"Black"),(255,205,70))
        if lt>1.8:
            p=1+0.04*math.sin(lt*6); bw,bh=int(700*p),int(110*p); card(d,[W/2-bw/2,880-bh/2,W/2+bw/2,880+bh/2],(64,220,120),34); ct(d,"ORDER NOW ON FIVERR",880-28,f(50,"Black"),(8,30,18))
        k2=1 if lt<TOTAL-66-0.8 else max(0,(72-t)/0.8)
        return fade_in(img,min(lt/0.3,k2))

if __name__=="__main__":
    out=sys.argv[1] if len(sys.argv)>1 else "video4.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
    for n in range(int(TOTAL*FPS)): p.stdin.write(frame(n/FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("ok",TOTAL)
