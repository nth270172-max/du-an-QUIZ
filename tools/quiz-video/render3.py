# Bản 3: emoji con vật vỡ điểm ảnh rõ dần theo đếm ngược, lộ đáp án nét + bật + pháo giấy
import math, subprocess, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import render2 as R
W,H,FPS=R.W,R.H,R.FPS
f=R.f; WHITE,YEL,GRN,DIM,CARD,CARD2=R.WHITE,R.YEL,R.GRN,R.DIM,R.CARD,R.CARD2
ease=R.ease; ctext=R.ctext; card=R.card; glow_arc=R.glow_arc

INTRO,OUTRO=5,5; ASK,COUNT,REVEAL=1.5,5,3; PERQ=ASK+COUNT+REVEAL
Q=[("🐱","Cat",["Snake","Cat","Fox","Lizard"],1,(255,170,60)),
   ("🐯","Tiger",["Zebra","Lion","Tiger","Leopard"],2,(255,120,40)),
   ("🐐","Goat",["Horse","Goat","Deer","Camel"],1,(190,140,90)),
   ("🦉","Owl",["Eagle","Parrot","Hawk","Owl"],3,(170,120,255)),
   ("🐘","Elephant",["Rhino","Hippo","Whale","Elephant"],3,(120,170,255))]
TOTAL=INTRO+PERQ*len(Q)+OUTRO

EF=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)
def emoji(ch,size):
    im=Image.new("RGBA",(136,136),(0,0,0,0)); ImageDraw.Draw(im).text((4,4),ch,font=EF,embedded_color=True)
    return im.resize((size,size),Image.LANCZOS)
ESZ=470
CRISP=[emoji(q[0],ESZ) for q in Q]
def pixelated(im,block):
    n=max(2,int(ESZ/block)); return im.resize((n,n),Image.BILINEAR).resize((ESZ,ESZ),Image.NEAREST)

IW,IH=980,600
def panel(color,t):
    # thẻ trái: nền tối + quầng màu con vật + hạt
    y=np.linspace(-1,1,IH)[:,None]; x=np.linspace(-1,1,IW)[None,:]
    g=np.exp(-((x*0.75)**2+(y*1.1)**2)*1.6)[...,None]
    base=np.array([18,24,52])[None,None,:]*(1-g*0.3)+np.array(color)[None,None,:]*g*0.45
    im=Image.fromarray(np.clip(base,0,255).astype(np.uint8)).convert("RGBA")
    d=ImageDraw.Draw(im); random.seed(11)
    for i in range(26):
        px=(random.random()+0.05*math.sin(t*0.7+i))%1*IW; py=(random.random()-t*0.02*(i%3+1))%1*IH; r=random.randint(2,5)
        d.ellipse([px,py,px+r,py+r],fill=color+(90,))
    return im
MASK=Image.new("L",(IW,IH),0); ImageDraw.Draw(MASK).rounded_rectangle([0,0,IW,IH],40,fill=255)
SHADOW=R.SHADOW; CONF=R.CONF

def header(img,d,q=None):
    card(img,[60,46,440,106],30,CARD); d.text((88,60),"GUESS THE ANIMAL",font=f(28,"SemiBold"),fill=DIM)
    for i in range(5):
        x=W/2-5*34/2+i*34+6; col=YEL if (q is not None and i<=q) else (60,75,120); d.rounded_rectangle([x,66,x+22,86],6,fill=col)
    if q is not None: d.text((1740,58),f"{q+1} / 5",font=f(34,"Bold"),fill=WHITE)

def place_emoji(img,im,cx,cy,scale=1.0):
    s=int(ESZ*scale); e=im.resize((s,s),Image.LANCZOS) if scale!=1 else im
    img.paste(e,(int(cx-s/2),int(cy-s/2)),e)

def frame(t):
    img=R.BASE.copy(); d=ImageDraw.Draw(img)
    if t<INTRO:
        header(img,d); k=ease(t/0.7)
        ctext(d,"CAN YOU GUESS",200-40*(1-k),f(120,"Black"),WHITE); ctext(d,"THE ANIMAL?",330,f(120,"Black"),YEL)
        if t>0.9: ctext(d,"5 QUESTIONS  •  5 SECONDS EACH",500,f(48,"SemiBold"),DIM)
        for i in range(5):
            ki=ease((t-1.3-i*0.12)/0.4)
            if ki<=0: continue
            blk=max(6,int(60*(1-min(1,(t-2.2)/2.3))))
            e=pixelated(CRISP[i],blk).resize((int(220*ki),int(220*ki)),Image.NEAREST); x=int(W/2-5*260/2+i*260+130-e.width/2); y=int(760-e.height/2)
            img.paste(e,(x,y),e)
        return img
    if t>=TOTAL-OUTRO:
        header(img,d,4); ctext(d,"HOW MANY DID YOU GET?",120,f(96,"Black"),WHITE)
        for i in range(5):
            e=CRISP[i].resize((130,130),Image.LANCZOS); img.paste(e,(int(W/2-5*160/2+i*160+15),250),e)
        for i in range(6):
            x=240+i*250; k=ease((t-(TOTAL-OUTRO)-i*0.08)/0.4); yy=int(440+30*(1-k))
            card(img,[x,yy,x+200,yy+170],CARD2 if i<5 else (70,55,20),30,YEL if i==5 else None,5)
            d.text((x+100-d.textlength(str(i),font=f(90,"Black"))/2,yy+30),str(i),font=f(90,"Black"),fill=WHITE if i<5 else YEL)
        ctext(d,"out of 5 — tell me in the comments",650,f(38,"SemiBold"),DIM)
        p=1+0.04*math.sin(t*6); bw,bh=int(620*p),int(110*p)
        card(img,[W/2-bw/2,850-bh/2,W/2+bw/2,850+bh/2],(230,40,60),34); ctext(d,"SUBSCRIBE",850-28,f(56,"Black"),WHITE)
        return img
    q=int((t-INTRO)//PERQ); lt=(t-INTRO)-q*PERQ; ch,ans,opts,ai,col=Q[q]; header(img,d,q)
    k=ease(lt/0.45); reveal=lt>=ASK+COUNT; rl=lt-ASK-COUNT
    if reveal:
        for (px,py,c,sz,rot) in CONF:
            yy=(py+rl*0.55)%1.3-0.15; xx=px+0.03*math.sin(rl*4+rot); X,Y=int(xx*W),int(yy*H); d.rounded_rectangle([X,Y,X+sz,Y+sz*0.6],3,fill=c)
    x0=int(70-500*(1-k)); img.paste(SHADOW,(x0-80,250-100),SHADOW)
    pn=panel(col,t); img.paste(pn,(x0,250),MASK)
    cx,cy=x0+IW//2,250+IH//2
    if not reveal:
        prog=max(0,(lt-ASK))/COUNT              # 0→1 theo đếm ngược
        blk=int(64-(64-10)*prog)                # 64px → 10px
        e=pixelated(CRISP[q],blk); place_emoji(img,e,cx,cy,1.0)
        d=ImageDraw.Draw(img)
        # huy hiệu ?
        card(img,[x0+IW-130,250+24,x0+IW-24,250+130],(255,255,255),53); d.text((x0+IW-77-d.textlength("?",font=f(70,"Black"))/2,250+36),"?",font=f(70,"Black"),fill=(20,30,70))
    else:
        kr=ease(rl/0.5); sc=1+0.22*math.sin(min(1,rl/0.5)*math.pi)
        # vòng sáng
        L=Image.new("RGBA",(700,700),(0,0,0,0)); ImageDraw.Draw(L).ellipse([80,80,620,620],outline=col+(255,),width=18); L=L.filter(ImageFilter.GaussianBlur(22))
        img.paste(L,(cx-350,cy-350),L)
        place_emoji(img,CRISP[q],cx,cy,sc); d=ImageDraw.Draw(img)
    d.rounded_rectangle([x0,250,x0+IW,250+IH],40,outline=(255,255,255),width=3)
    # câu hỏi + đáp án
    d.text((1110,240),"Which animal is this?",font=f(58,"ExtraBold"),fill=WHITE)
    ox,oy,bw,bh,gap=1110,400,360,96,18
    for i,o in enumerate(opts):
        ki=ease((lt-0.2-i*0.08)/0.35); bx=ox+(i%2)*(bw+gap); by=oy+(i//2)*(bh+gap)+int(30*(1-ki))
        if reveal and i==ai: fill,txt,bd=GRN,(8,30,18),None
        elif reveal: fill,txt,bd=(26,34,62),(90,100,130),None
        else: fill,txt,bd=CARD2,WHITE,(70,90,150)
        card(img,[bx,by,bx+bw,by+bh],fill,24,bd,2)
        d.ellipse([bx+16,by+24,bx+64,by+72],fill=(60,78,130) if not(reveal and i==ai) else (8,30,18))
        d.text((bx+40-d.textlength("ABCD"[i],font=f(28,"Black"))/2,by+34),"ABCD"[i],font=f(28,"Black"),fill=WHITE if not(reveal and i==ai) else GRN)
        d.text((bx+84,by+30),o,font=f(34,"Bold"),fill=txt)
    tx,ty,r=1500,790,105
    if not reveal:
        d.ellipse([tx-r,ty-r,tx+r,ty+r],outline=(40,55,100),width=22)
        rem=ASK+COUNT-lt; frac=min(1,rem/COUNT); glow_arc(img,tx,ty,r,frac,YEL if rem>2 else (255,90,90)); d=ImageDraw.Draw(img)
        n=str(math.ceil(rem)) if lt>=ASK else "5"; d.text((tx-d.textlength(n,font=f(110,"Black"))/2,ty-66),n,font=f(110,"Black"),fill=WHITE)
        d.text((tx-d.textlength("SECONDS",font=f(22,"SemiBold"))/2,ty+r+16),"SECONDS",font=f(22,"SemiBold"),fill=DIM)
    else:
        kr=ease(rl/0.4); card(img,[1110,720,1110+int(740*kr),860],GRN,28)
        if kr>=1: ctext(d,"IT'S A "+ans.upper()+"!" if ans!="Elephant" and ans!="Owl" else "IT'S AN "+ans.upper()+"!",762,f(46,"Black"),(8,30,18),1480)
    d.rounded_rectangle([60,1020,1860,1034],7,fill=(35,48,90)); d.rounded_rectangle([60,1020,60+int(1800*min(1,lt/PERQ)),1034],7,fill=YEL)
    return img

if __name__=="__main__":
    out=sys.argv[1] if len(sys.argv)>1 else "video3.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",out],stdin=subprocess.PIPE)
    for n in range(int(TOTAL*FPS)): p.stdin.write(frame(n/FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("ok",TOTAL)
