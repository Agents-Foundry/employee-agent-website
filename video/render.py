"""Render the original narrated explainer. Requires Pillow, numpy and FFmpeg.

Run narrate.ps1 first. FFMPEG_BINARY may point to a local FFmpeg executable;
otherwise imageio-ffmpeg (0.6.0) supplies it. No browser or product API is used.
"""
import json, math, os, subprocess, wave, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public/assets'; WORK=ROOT/'video/generated'
SPEC=json.loads((ROOT/'video/storyboard.json').read_text(encoding='utf-8'))
W,H,FPS=1920,1080,24
BG='#101722'; SURFACE='#1b2535'; LINE='#3c4261'; WHITE='#f4f5fc'; MUTED='#afbcd3'; PURPLE='#b3a3ff'; CYAN='#8bd9e8'
FONT=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
def font(size,bold=False): return ImageFont.truetype(str(FONT/('segoeuib.ttf' if bold else 'segoeui.ttf')),size)
fonts={}; images={}
def f(size,bold=False):
    key=(size,bold)
    if key not in fonts: fonts[key]=font(size,bold)
    return fonts[key]
def wrap(text,size,maxwidth,bold=False):
    lines=[]; line=''
    for word in text.split():
        test=(line+' '+word).strip()
        if f(size,bold).getlength(test)>maxwidth and line: lines.append(line); line=word
        else: line=test
    return lines+[line]
def text(im,value,xy,size=36,color=WHITE,bold=False,width=None,spacing=1.22):
    draw=ImageDraw.Draw(im); x,y=xy
    lines=wrap(value,size,width,bold) if width else value.split('\n')
    for line in lines: draw.text((x,y),line,font=f(size,bold),fill=color); y+=size*spacing
    return y
def roundbox(im,box,fill=SURFACE,radius=26,edge=LINE,depth=0):
    d=ImageDraw.Draw(im); x0,y0,x1,y1=box
    if depth:
        d.rounded_rectangle((x0,y0+depth,x1,y1+depth),radius,fill='#302b4b')
        d.rounded_rectangle((x0+3,y0+depth+7,x1+3,y1+depth+14),radius,fill='#0b111c')
    d.rounded_rectangle(box,radius,fill=fill,outline=edge,width=2)
def pill(im,value,xy,color=PURPLE,fill='#302c50',size=24):
    x,y=xy; width=f(size,True).getlength(value)+36
    roundbox(im,(x,y,x+width,y+size+25),fill,14,fill)
    text(im,value,(x+18,y+8),size,color,True)
def bot(name,width):
    key=(name,width)
    if key not in images:
        images[key]=Image.open(OUT/(name if '.' in name else name+'.avif')).convert('RGBA')
        images[key].thumbnail((width,width),Image.Resampling.LANCZOS)
    return images[key]
def paste(im,asset,xy,opacity=1):
    if opacity<1:
        asset=asset.copy(); asset.putalpha(asset.getchannel('A').point(lambda a:int(a*max(0,opacity))))
    im.alpha_composite(asset,(round(xy[0]),round(xy[1])))
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def show(im,layer,t,delay=0,offset=28):
    progress=ease((t-delay)/.65)
    if progress>0: paste(im,layer,(0,offset*(1-progress)),progress)
def layer(): return Image.new('RGBA',(W,H))

# A fixed branded background with gentle depth and a local font.
yy,xx=np.mgrid[0:H,0:W]; glow=np.exp(-(((xx-1500)/700)**2+((yy-380)/550)**2))
pixels=np.zeros((H,W,3),dtype=np.uint8)
for c,(base,boost) in enumerate(zip([16,23,34],[23,11,38])): pixels[:,:,c]=base+glow*boost
background=Image.fromarray(pixels).convert('RGBA')
grid=layer(); d=ImageDraw.Draw(grid)
for x in range(0,W,96): d.line((x,0,x,H),fill=(145,140,200,10))
for y in range(0,H,96): d.line((0,y,W,y),fill=(145,140,200,10))
background.alpha_composite(grid)
roundbox(background,(80,50,140,110),'#7865dc',18,'#9787ef',5)
text(background,'AF',(93,63),26,WHITE,True)
text(background,'AGENTS FOUNDRY',(160,61),29,WHITE,True)
text(background,'PRODUCT + ONBOARDING EXPLAINER',(1270,65),22,MUTED)

scenes=[]; rate=None; audio=[]; start=0; cues=[]
for i,scene in enumerate(SPEC['scenes']):
    with wave.open(str(WORK/(scene['id']+'.wav'))) as wav:
        assert wav.getsampwidth()==2 and wav.getnchannels()==1
        if rate is None: rate=wav.getframerate()
        assert rate==wav.getframerate()
        samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').copy()
    # A short breathing space lets viewers read the scene, without speeding up narration.
    lead=.4; duration=len(samples)/rate+1.0
    scene.update(start=start,duration=duration,audio_duration=len(samples)/rate)
    audio.extend([np.zeros(round(rate*lead),dtype='<i2'),samples,np.zeros(round(rate*.6),dtype='<i2')])
    words=scene['narration'].split(); groups=[]
    for n in range(0,len(words),12): groups.append(' '.join(words[n:n+12]))
    cursor=start+lead
    for group in groups:
        length=scene['audio_duration']*len(group.split())/len(words)
        cues.append((cursor,cursor+length,group)); cursor+=length
    title=layer()
    text(title,scene['eyebrow'],(86,206),24,PURPLE,True)
    end=text(title,scene['title'],(80,272),78,WHITE,True,width=760,spacing=1.12)
    text(title,scene['subtitle'],(84,end+30),44,PURPLE,True,width=720,spacing=1.2)
    # Clear provenance and scope, rather than simulated screenshots or speed telemetry.
    if scene['id']=='target':
        text(title,'Configured organization + active employees',(86,690),28,MUTED,width=700)
        pill(title,'Guided QA assignment target',(86,750),size=23)
    elif scene['id']=='outro':
        pill(title,'Explore Agents Foundry',(86,738),size=28)
        text(title,'agents-foundry.github.io/employee-agent-website/',(86,812),24,MUTED,width=760)
    else:
        labels={'intro':'Identity · Scope · Policy · Human ownership','choose':'QA blueprint available locally','configure':'Configuration preferences stay with the assignment','assign':'Separate instances. Separate conversation histories.','verify':'Verified identity before agent selection','govern':'QA planning now · connected execution on the roadmap'}
        text(title,labels[scene['id']],(86,760),25,MUTED,width=700)
    scenes.append((scene,title)); start+=duration

joined=np.concatenate(audio)
with wave.open(str(WORK/'narration.wav'),'wb') as wav:
    wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(rate); wav.writeframes(joined.tobytes())
def stamp(seconds,sep='.'):
    ms=round(seconds*1000); h=ms//3600000; m=ms//60000%60; s=ms//1000%60
    return f'{h:02}:{m:02}:{s:02}{sep}{ms%1000:03}'
(OUT/'agents-foundry-explainer.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(a)} --> {stamp(b)}\n{c}' for a,b,c in cues)+'\n',encoding='utf-8')
(OUT/'agents-foundry-explainer.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a,",")} --> {stamp(b,",")}\n{c}' for i,(a,b,c) in enumerate(cues))+'\n',encoding='utf-8')
(OUT/'agents-foundry-explainer-transcript.txt').write_text('Agents Foundry — product and onboarding explainer\n\nOnboarding target: 5–10 minutes for guided QA assignment after organization setup. Not a measured benchmark. External integration setup is separate.\n\n'+'\n\n'.join(s['eyebrow']+'\n'+s['narration'] for s,_ in scenes)+'\n',encoding='utf-8')

def graphic(scene,t):
    im=layer(); d=ImageDraw.Draw(im); name=scene['id']; bob=math.sin(t*1.2)*7
    if name=='intro':
        d.ellipse((980,724,1790,850),fill='#352d5d',outline='#6d609b',width=3)
        d.ellipse((980,704,1790,806),fill='#242b42',outline='#5f5d87',width=3)
        paste(im,bot('hero-squad.png',860),(928,145+bob))
        roundbox(im,(1250,810,1810,905),SURFACE,20,LINE,8)
        text(im,'Specialist roles. Shared direction.',(1276,825),26,WHITE,True)
        text(im,'Your people stay in charge.',(1276,863),23,PURPLE)
    elif name=='target':
        d.ellipse((1070,205,1690,825),fill='#252a42',outline='#4e446f',width=3)
        d.arc((1060,195,1700,835),-85,-85+310*ease(t/2),fill=PURPLE,width=12)
        text(im,'5–10',(1115,345),155,WHITE,True)
        text(im,'MINUTES',(1240,525),40,PURPLE,True)
        pill(im,'ONBOARDING TARGET',(1190,610),size=25)
    elif name=='choose':
        roundbox(im,(950,190,1810,325),SURFACE,22,LINE,8)
        text(im,'Your organization',(1192,220),36,WHITE,True)
        text(im,'People + AI employees',(1204,269),25,MUTED)
        d.line((1380,334,1380,380),fill='#706393',width=3)
        for j,label in enumerate(['Engineering','Product','Operations']):
            x=950+j*294; roundbox(im,(x,380,x+272,466),'#302c50' if j==0 else SURFACE,18,PURPLE if j==0 else LINE,6)
            text(im,label,(x+24,403),28,PURPLE if j==0 else MUTED,True)
        d.line((1086,475,1086,520),fill=PURPLE,width=3)
        roundbox(im,(964,520,1764,874),SURFACE,26,PURPLE,10)
        paste(im,bot('testo',320),(966,526+bob))
        text(im,'QA Engineer',(1295,598),43,WHITE,True)
        text(im,'Engineering / QA',(1296,660),28,MUTED)
        pill(im,'Versioned role blueprint',(1296,723),size=22)
    elif name=='configure':
        roundbox(im,(960,190,1810,895),SURFACE,28,LINE,12)
        text(im,'QA Engineer blueprint',(1000,224),38,WHITE,True)
        text(im,'Review the setup before assignment',(1000,284),26,MUTED)
        rows=[('Agent name','Testo'),('Project scope','Release acceptance criteria'),('Working environment','Staging'),('Model preferences','Organization configured'),('Policy boundaries','Enforced capabilities')]
        for j,(label,value) in enumerate(rows):
            row=layer(); y=350+j*95
            roundbox(row,(996,y,1774,y+77),'#222d40',14,LINE)
            text(row,label,(1020,y+20),24,MUTED)
            text(row,value,(1340,y+20),24,WHITE,True)
            show(im,row,t,j*.35+0.2,15)
    elif name=='assign':
        pill(im,'1 setup → up to 25 active employees',(1028,215),size=29)
        for j in range(3):
            card=layer(); x=955+j*288
            roundbox(card,(x,340,x+266,832),SURFACE,24,LINE,12)
            paste(card,bot('testo',232),(x+17,345+math.sin(t*1.3+j)*7))
            text(card,f'Employee {j+1:02}',(x+30,612),29,WHITE,True)
            text(card,'Distinct agent instance',(x+24,670),20,MUTED)
            pill(card,'Signed assignment',(x+22,725),size=19)
            show(im,card,t,j*.4,22)
    elif name=='verify':
        roundbox(im,(956,210,1810,892),SURFACE,26,LINE,12)
        paste(im,bot('testo',260),(975,230+bob))
        text(im,'Your assigned agents',(1260,262),35,WHITE,True)
        text(im,'Testo · QA Engineer',(1260,330),27,MUTED)
        for j,label in enumerate(['Signature verified','Employee ownership checked','Organization checked']):
            row=layer(); y=530+j*87
            d2=ImageDraw.Draw(row); d2.ellipse((1000,y,1040,y+40),fill='#234336')
            d2.line((1010,y+20,1019,y+28,1032,y+12),fill='#92d9b6',width=4)
            text(row,label,(1064,y-1),30,WHITE)
            show(im,row,t,j*.4+.4,15)
        pill(im,'Verify and use agent',(1260,395),size=27)
    elif name=='govern':
        roundbox(im,(950,245,1810,854),SURFACE,26,LINE,12)
        text(im,'Policy travels with the role',(989,277),36,WHITE,True)
        for j,(label,status,color,fill) in enumerate([('Create a test plan','ALLOW','#92d9b6','#244135'),('Browser execution','REVIEW','#e6c37e','#45391e'),('Production deployment','DENY','#f3a4b3','#462b3b')]):
            row=layer(); y=374+j*121
            roundbox(row,(986,y,1774,y+92),'#222d40',17,LINE,4)
            text(row,label,(1010,y+26),29,WHITE)
            pill(row,status,(1560,y+21),color,fill,22)
            show(im,row,t,j*.5+.15,18)
        text(im,'Approval grants permission; execution is a separate step.',(987,771),23,MUTED,width=760)
    elif name=='outro':
        roles=[('fronto','Engineering'),('producto','Product'),('sello','Sales'),('supporto','Support'),('opero','Operations'),('accounto','Finance')]
        for j,(asset,label) in enumerate(roles):
            x=955+(j%3)*286; y=215+(j//3)*286
            card=layer(); roundbox(card,(x,y,x+260,y+259),SURFACE,22,LINE,8)
            paste(card,bot(asset,205),(x+28,y+4+math.sin(t*1.4+j)*5))
            text(card,label,(x+28,y+207),25,WHITE,True)
            show(im,card,t,j*.12,18)
        text(im,'55 role concepts · wider templates planned',(1002,825),27,PURPLE,True)
    return im

graphic_cache={}
def frame(scene,title,index,t,global_time):
    im=background.copy(); content=layer(); show(content,title,t,0,20)
    if t<3: show(content,graphic(scene,t),t,.1,18)
    else:
        if scene['id'] not in graphic_cache: graphic_cache[scene['id']]=graphic(scene,3)
        paste(content,graphic_cache[scene['id']],(0,math.sin((t-3)*1.1)*3))
    opacity=min(1,max(0,t/.35),max(0,(scene['duration']-t)/.35))
    paste(im,content,(0,0),opacity)
    draw=ImageDraw.Draw(im)
    draw.line((80,980,1840,980),fill='#36425b',width=3)
    draw.line((80,980,80+1760*min(1,global_time/start),980),fill=PURPLE,width=4)
    labels=['Vision','5–10 min target','Choose','Configure','Assign','Verify','Govern','Explore']
    for j,label in enumerate(labels):
        x=80+j*221; text(im,f'{j+1:02}  {label}',(x,1000),20,PURPLE if j==index else '#72839e',j==index)
    text(im,'Illustrated workflow · QA assignment available locally',(80,928),20,MUTED)
    return im.convert('RGB')

if '--preview-only' in sys.argv:
    for i,(scene,title) in enumerate(scenes):
        shot=frame(scene,title,i,3,scene['start']+3)
        shot.save(WORK/(scene['id']+'-preview.jpg'),quality=90)
        if i==0: shot.save(OUT/'onboarding-poster.jpg',quality=90)
    print('Saved all eight scene previews',flush=True)
    sys.exit(0)

ffmpeg=os.environ.get('FFMPEG_BINARY')
if not ffmpeg:
    import imageio_ffmpeg
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
target=OUT/'agents-foundry-explainer.mp4'
cmd=[ffmpeg,'-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(WORK/'narration.wav'),'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(target)]
print(f'Rendering {start:.1f}s, {W}x{H}, {FPS}fps',flush=True)
process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
    for i,(scene,title) in enumerate(scenes):
        count=round(scene['duration']*FPS)
        for n in range(count):
            t=n/FPS; shot=frame(scene,title,i,t,scene['start']+t)
            if n==round(2*FPS):
                shot.save(WORK/(scene['id']+'-preview.jpg'),quality=90)
                if i==0: shot.save(OUT/'onboarding-poster.jpg',quality=90)
            process.stdin.write(shot.tobytes())
        print(f'Rendered: {scene["id"]} ({count} frames)',flush=True)
finally:
    process.stdin.close()
if process.wait()!=0: raise RuntimeError('FFmpeg export failed')
(WORK/'render-info.json').write_text(json.dumps({'duration':start,'width':W,'height':H,'fps':FPS,'bytes':target.stat().st_size,'scenes':[{k:s[k] for k in ['id','start','duration']} for s,_ in scenes]},indent=2))
print(f'Exported {target} ({target.stat().st_size/1024/1024:.1f} MB)',flush=True)
