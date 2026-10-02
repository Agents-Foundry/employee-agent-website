"""Character film: original website bot artwork rigged inside a 3D story.

Headless ModernGL rendering; no browser capture, stock footage or image slideshow.
Run narrate.ps1 first, then python video/movie.py [--preview-only].
"""
import json, math, os, sys, wave, subprocess, time
from pathlib import Path
import numpy as np
import moderngl
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'public/assets'; WORK=ROOT/'video/generated'
SPEC=json.loads((ROOT/'video/storyboard.json').read_text(encoding='utf-8'))
W,H,FPS=1920,1080,30
PINK=(.95,.19,.48); BLUE=(.10,.57,.96); GOLD=(1,.57,.10)
VIOLET=(.45,.32,.88); INK=(.045,.065,.13); WHITE=(.94,.95,1)
SKIN=(.78,.48,.30); GREEN=(.18,.75,.57); AMBER=(1,.63,.14)
ctx=moderngl.create_context(standalone=True,require=330)
print('3D renderer:',ctx.info['GL_RENDERER'],flush=True)
ctx.enable(moderngl.DEPTH_TEST)
fbo=ctx.framebuffer(color_attachments=[ctx.renderbuffer((W,H),4,samples=4)],depth_attachment=ctx.depth_renderbuffer((W,H),samples=4))
resolved=ctx.framebuffer(color_attachments=[ctx.texture((W,H),4)])
fbo.use()
program=ctx.program(vertex_shader='''#version 330
in vec3 position; in vec3 normal;
uniform mat4 model, vp; out vec3 n, world;
void main(){vec4 p=model*vec4(position,1);world=p.xyz;n=mat3(transpose(inverse(model)))*normal;gl_Position=vp*p;}
''',fragment_shader='''#version 330
in vec3 n,world; uniform vec3 color,eye; uniform float shine;
out vec4 result;
void main(){vec3 N=normalize(n),L=normalize(vec3(-.6,1,.8)),V=normalize(eye-world);
float diff=max(0,dot(N,L));float rim=pow(1-max(0,dot(N,V)),3);
float spec=pow(max(0,dot(reflect(-L,N),V)),42)*shine;
vec3 c=color*(.46+.60*diff)+vec3(.19,.16,.27)*rim+vec3(.9)*spec;
c=mix(c,vec3(.87,.88,.97),clamp((length(eye-world)-15)*.025,0,.18));
result=vec4(c,1);}
''')

# Use the actual website assets as GPU textures. Art remains unchanged on disk;
# the dense mesh bends at shoulders, neck and feet to animate the original design.
sprite_program=ctx.program(vertex_shader='''#version 330
in vec2 source_uv; out vec2 uv;
uniform mat4 vp, model; uniform float time, walk, wave, reach, floor_uv;
vec2 rotateAround(vec2 p,vec2 pivot,float angle){
    float c=cos(angle),s=sin(angle);return pivot+mat2(c,s,-s,c)*(p-pivot);
}
void main(){
    uv=source_uv;vec2 p=uv;float gait=sin(time*7.5);
    // The original face, curl and ears stay rigid; articulation starts below the neck.
    float left=(1-smoothstep(.278,.318,uv.x))*smoothstep(.50,.54,uv.y)*(1-smoothstep(.65,.69,uv.y));
    float right=smoothstep(.572,.625,uv.x)*(1-smoothstep(.72,.75,uv.x))*smoothstep(.50,.54,uv.y)*(1-smoothstep(.635,.68,uv.y));
    p=mix(p,rotateAround(p,vec2(.31,.53),sin(time*4.0)*(.035+wave*.04)+gait*.035*walk),left);
    p=mix(p,rotateAround(p,vec2(.59,.53),sin(time*4.8)*(.03+wave*.04)-reach*.035),right);
    float feet=smoothstep(.73,.78,uv.y);
    float side=1-smoothstep(.425,.46,uv.x);float stepWave=gait*(side*2-1);
    p.y-=feet*max(0,stepWave)*.027*walk;p.x+=feet*stepWave*.021*walk;
    float tools=smoothstep(.705,.75,uv.x);
    p.y+=tools*sin(time*1.7+uv.y*19)*.010;
    p.x+=tools*cos(time*.9+uv.y*14)*.008;
    vec3 local=vec3((p.x-.455)*3.55,(floor_uv-p.y)*3.55+abs(gait)*.055*walk+sin(time*2)*.012,0);
    gl_Position=vp*model*vec4(local,1);
}
''',fragment_shader='''#version 330
in vec2 uv; uniform sampler2D artwork;out vec4 result;
void main(){result=texture(artwork,uv);if(result.a<.035)discard;}
''')
sprite_vertices=[]
for i in range(70):
    for j in range(70):
        for a,b in [(i,j),(i+1,j),(i+1,j+1),(i,j),(i+1,j+1),(i,j+1)]:sprite_vertices.append((a/70,b/70))
sprite_buffer=ctx.buffer(np.array(sprite_vertices,dtype='f4').tobytes())
sprite_mesh=ctx.vertex_array(sprite_program,[(sprite_buffer,'2f','source_uv')])
bot_textures={}
for bot_name in ['testo','fronto','producto']:
    artwork=Image.open(OUT/(bot_name+'.avif')).convert('RGBA')
    texture=ctx.texture(artwork.size,4,artwork.tobytes());texture.build_mipmaps()
    texture.filter=(moderngl.LINEAR_MIPMAP_LINEAR,moderngl.LINEAR);bot_textures[bot_name]=texture
camera_vp=np.eye(4,dtype='f4');camera_eye=np.array((6,5,12),dtype='f4')

def website_bot(pos,color,t,walk,wave,turn,reach,scale):
    name='testo' if color==PINK else 'fronto' if color==BLUE else 'producto'
    delta=camera_eye-np.array(pos);facing=math.atan2(delta[0],delta[2])+turn*.12
    sprite_program['vp'].write(camera_vp.T.astype('f4').tobytes())
    # Keep the boot pixels above the floor shadow, rather than clipping their soles.
    grounded=np.array(pos,dtype='f4')+np.array((0,.10*scale,0),dtype='f4')
    sprite_program['model'].write(matrix(grounded,(scale,scale,scale),yaw(facing)).T.tobytes())
    for key,value in [('time',t),('walk',walk),('wave',wave),('reach',reach),('floor_uv',.883 if name=='producto' else .84)]:sprite_program[key].value=value
    bot_textures[name].use(0);sprite_program['artwork'].value=0
    ctx.enable(moderngl.BLEND);ctx.blend_func=(moderngl.SRC_ALPHA,moderngl.ONE_MINUS_SRC_ALPHA)
    sprite_mesh.render();ctx.disable(moderngl.BLEND)

def unit(v):
    v=np.array(v,dtype='f4'); return v/np.linalg.norm(v)
def matrix(pos=(0,0,0),scale=(1,1,1),rotation=None):
    m=np.eye(4,dtype='f4');m[:3,:3]=(np.eye(3) if rotation is None else rotation)@np.diag(scale);m[:3,3]=pos;return m
def yaw(a):return np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]],dtype='f4')
def view(eye,target):
    forward=unit(np.array(target)-eye);right=unit(np.cross(forward,(0,1,0)));up=np.cross(right,forward)
    m=np.eye(4,dtype='f4');m[:3,:3]=[right,up,-forward];m[:3,3]=-m[:3,:3]@eye;return m
def perspective(fov,aspect,near=.1,far=90):
    a=1/math.tan(fov/2);m=np.zeros((4,4),dtype='f4');m[0,0]=a/aspect;m[1,1]=a;m[2,2]=(far+near)/(near-far);m[2,3]=2*far*near/(near-far);m[3,2]=-1;return m
def mesh(vertices):
    buffer=ctx.buffer(np.array(vertices,dtype='f4').tobytes());return ctx.vertex_array(program,[(buffer,'3f 3f','position','normal')])
def sphere_mesh():
    vertices=[]
    def p(i,j):
        a=i*math.pi/20;b=j*2*math.pi/28;return (math.sin(a)*math.cos(b),math.cos(a),math.sin(a)*math.sin(b))
    for i in range(20):
        for j in range(28):
            points=[p(i,j),p(i+1,j),p(i+1,j+1),p(i,j+1)]
            for k in [0,1,2,0,2,3]:vertices.append((*points[k],*points[k]))
    return mesh(vertices)
def cube_mesh():
    vertices=[]
    for axis in range(3):
        for sign in [-1,1]:
            other=[x for x in range(3) if x!=axis]
            for i in range(8):
                for j in range(8):
                    points=[]
                    for a,b in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]:
                        p=np.zeros(3);p[axis]=sign;p[other[0]]=-1+a/4;p[other[1]]=-1+b/4
                        q=np.clip(p,-.88,.88);normal=unit(p-q);points.append((q+normal*.12,normal))
                    for k in [0,1,2,0,2,3]:vertices.append((*points[k][0],*points[k][1]))
    return mesh(vertices)
sphere=sphere_mesh();cube=cube_mesh()
def obj(shape,pos,scale,color,rotation=None,shine=.15):
    program['model'].write(matrix(pos,scale,rotation).T.tobytes());program['color'].value=color;program['shine'].value=shine;shape.render()
def ball(pos,scale,color,rotation=None,shine=.15):obj(sphere,pos,scale,color,rotation,shine)
def box(pos,scale,color,rotation=None):obj(cube,pos,scale,color,rotation,.04)
def rod(a,b,r,color):
    a=np.array(a);b=np.array(b);direction=unit(b-a);right=unit(np.cross(direction,(0,0,1) if abs(direction[2])<.9 else (0,1,0)));other=np.cross(direction,right)
    ball((a+b)/2,(r,np.linalg.norm(b-a)/2+r,r),color,np.column_stack((right,direction,other)))
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def path(a,b,t):return np.array(a)*(1-smooth(t))+np.array(b)*smooth(t)
def shadow(x,z,size=1):ball((x,.055,z),(.68*size,.016,.38*size),(.78,.78,.87),shine=0)

def character(pos,color,t,walk=0,wave=0,turn=0,human=False,reach=0,scale=1):
    """Hierarchical rig: torso/head/eyes, antenna, shoulders, elbows, hips, knees, feet."""
    if not human:
        shadow(pos[0],pos[2],scale)
        website_bot(pos,color,t,walk,wave,turn,reach,scale)
        return
    root=np.array(pos,dtype='f4');rot=yaw(turn);phase=t*7.5;bounce=abs(math.sin(phase))*.085*walk
    def world(p):return root+rot@(np.array(p)*scale)
    def B(p,s,c,shine=.15):ball(world(p),np.array(s)*scale,c,rot,shine)
    def C(p,s,c):box(world(p),np.array(s)*scale,c,rot)
    def R(a,b,r,c):rod(world(a),world(b),r*scale,c)
    shadow(root[0],root[2],scale)
    y=bounce
    bodycolor=color
    # Feet and legs counter-swing continuously when walking.
    for side in [-1,1]:
        swing=math.sin(phase+(0 if side==1 else math.pi))*.38*walk
        hip=(side*.22,.9+y,0);knee=(side*.23,.52+y,-swing*.40);foot=(side*.23,.19+max(0,swing)*.32,swing)
        R(hip,knee,.12,bodycolor);R(knee,foot,.105,bodycolor);B(foot,(.20,.16,.29),(.07,.09,.17) if human else bodycolor,.3)
    B((0,1.18+y,0),(.48,.53,.31),bodycolor,.27)
    if not human:
        B((0,1.22+y,.275),(.335,.34,.075),INK,.1)
        for k in range(3):C((-.16+k*.15,1.35+y,.345),(.048,.035,.018),[BLUE,GREEN,GOLD][k])
        C((0,1.15+y,.352),(.21,.023,.015),(.58,.83,1));C((-.07,1.03+y,.352),(.14,.016,.015),VIOLET)
    # A waving forearm, reaching gesture and gait use real joint transforms.
    for side in [-1,1]:
        shoulder=np.array((side*.47,1.51+y,0));elbow=np.array((side*.66,1.10+y,math.sin(phase+side)*.22*walk));hand=np.array((side*.67,.85+y,-math.sin(phase+side)*.29*walk))
        if side==-1 and wave:
            elbow=path(elbow,(side*.76,1.78+y,.03),wave);hand=path(hand,(side*(.72+.10*math.sin(t*8)),2.16+y,.12),wave)
        if side==1 and reach:
            elbow=path(elbow,(.52,1.38+y,.35),reach);hand=path(hand,(.44,1.52+y,.80),reach)
        R(shoulder,elbow,.105,bodycolor);B(elbow,(.125,.125,.125),bodycolor);R(elbow,hand,.09,bodycolor);B(hand,(.14,.15,.12),SKIN if human else bodycolor,.3)
    B((0,1.82+y,0),(.17,.15,.17),SKIN if human else color)
    B((0,2.20+y,0),(.51,.48,.38),SKIN if human else color,.3)
    if human:B((0,2.48+y,-.08),(.53,.24,.36),(.12,.08,.13))
    else:
        B((0,2.18+y,.30),(.415,.34,.13),(.99,.86,.69),.08)
        for side in [-1,1]:B((side*.52,2.20+y,0),(.10,.22,.21),color,.35)
        R((0,2.59+y,0),(.12,2.85+y,0),.055,color);B((.16,2.88+y,0),(.105,.105,.105),(.30,.86,1),.6)
    blink=max(.08,1-smooth((math.sin(t*1.7+turn)-.986)/.013))
    for side in [-1,1]:
        B((side*.18,2.23+y,.405),(.115,.145*blink,.055),WHITE,.3)
        B((side*.18+.015*math.sin(t*.6),2.23+y,.455),(.063,.087*blink,.031),INK,.25)
        B((side*.18-.025,2.27+y,.482),(.018,.023*blink,.01),WHITE,.2)
        B((side*.31,2.08+y,.415),(.071,.03,.018),(.99,.58,.54),0)
    # Curved smile built as smooth connected pieces, rather than a flat facial image.
    for i in range(6):
        x=-.13+i*.052;xx=x+.052
        R((x,2.02+y+.10*(x/.13)**2,.428),(xx,2.02+y+.10*(xx/.13)**2,.428),.014,INK)

def desk(x,z,color=VIOLET):
    box((x,.96,z),(.94,.09,.54),WHITE)
    for dx in [-.72,.72]:box((x+dx,.48,z),(.055,.46,.34),(.73,.74,.85))
    box((x,1.38,z-.28),(.48,.29,.045),INK);box((x,1.39,z-.228),(.425,.235,.012),color)
    box((x,1.08,z+.22),(.35,.025,.13),(.67,.68,.79));rod((x,1.04,z-.28),(x,1.29,z-.28),.04,INK)
def plant(x,z):
    ball((x,.3,z),(.28,.32,.28),(.66,.61,.86));rod((x,.38,z),(x,1.4,z),.045,(.25,.47,.37))
    for i in range(5):
        a=i*2.2;ball((x+math.cos(a)*.16,.65+i*.16,z+math.sin(a)*.16),(.25,.09,.13),(.24,.62,.43),yaw(a))
def room(t):
    box((0,-.25,0),(6,.25,3.5),(.86,.86,.96))
    box((0,-.005,0),(5.96,.035,3.46),WHITE)
    # Architectural archway, offset walls, a skyline and plants give the cast a place to act.
    box((-5,1.5,-2.9),(.10,1.5,.2),(.67,.63,.90));box((5,1.5,-2.9),(.1,1.5,.2),(.67,.63,.90))
    box((0,3.0,-2.9),(5.1,.10,.2),(.67,.63,.90))
    for x in [-3.4,-1.1,1.2,3.5]:
        box((x,1.64,-3.05),(.84,1.02,.06),(.78,.84,.98))
        box((x,1.64,-2.97),(.027,1.02,.03),WHITE)
        box((x,1.55,-2.97),(.84,.025,.03),WHITE)
    plant(-5.05,1.75);plant(5.05,-1.5)
    for j in range(5):
        a=t*.25+j*1.25;ball((math.cos(a)*5.6,3.5+.15*math.sin(t+j),math.sin(a)*2.7),(.07,.07,.07),[VIOLET,BLUE,GOLD][j%3],shine=.4)
def parcel(pos,color=GOLD,turn=0):
    box(pos,(.22,.22,.22),color,yaw(turn));p=np.array(pos);box(p+(0,.225,0),(.23,.015,.04),WHITE,yaw(turn))
def gate(x,z,color,open_amount):
    for side in [-1,1]:box((x+side*.72,1.40,z),(.07,1.40,.11),color)
    box((x,2.78,z),(.79,.07,.11),color)
    width=.65*(1-open_amount)
    if width>.025:
        for side in [-1,1]:box((x+side*(.72-width),1.39,z),(width,1.27,.025),(.72,.78,.92))

fonts={}; fontdir=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
def font(size,bold=False):
    key=(size,bold)
    if key not in fonts:fonts[key]=ImageFont.truetype(str(fontdir/('segoeuib.ttf' if bold else 'segoeui.ttf')),size)
    return fonts[key]
def label(im,value,pos,vp,size=27,accent=False):
    p=vp@np.array([*pos,1]);xy=((p[0]/p[3]+1)*W/2,(1-p[1]/p[3])*H/2)
    d=ImageDraw.Draw(im);width=font(size,True).getlength(value);x,y=xy
    d.rounded_rectangle((x-width/2-20,y-12,x+width/2+20,y+size+12),16,fill=(255,255,255,235),outline=(220,214,245,255),width=2)
    d.text((x-width/2,y),value,font=font(size,True),fill='#6449cf' if accent else '#232238')

def scene_draw(name,t,duration):
    global camera_vp,camera_eye
    labels=[];u=t/duration
    # A slow orbit and dolly replace the static camera of a slide deck.
    orbit=.12*math.sin(u*math.pi-.6)
    eye=np.array([6.7+orbit*7,5.5+.2*math.sin(u*math.pi),13.0-1.4*u],dtype='f4')
    target=np.array([0,1.12,0],dtype='f4')
    if name in ['intro','target','configure','verify']:eye*=.83;target=np.array([-.35 if name=='intro' else 0,1.40,.45],dtype='f4')
    if name=='govern':eye=np.array([3.2+orbit*4,5.2,13.6-u],dtype='f4');target=np.array([0,1.22,.15],dtype='f4')
    if name=='outro':eye*=.9;target=np.array([0,1.40,.55],dtype='f4')
    vp=perspective(math.radians(39),W/H)@view(eye,target)
    camera_vp=vp;camera_eye=eye
    program['vp'].write(vp.T.astype('f4').tobytes());program['eye'].value=tuple(eye)
    room(t)
    if name=='intro':
        desk(-2.65,-.4);character((-2.9,0,1.15),VIOLET,t,human=True,reach=.6,turn=.3)
        enter=smooth((t-.6)/4);p=path((4.6,0,1.7),(.7,0,1.2),enter)
        character(p,PINK,t,walk=1-smooth((t-4)/1.2),wave=smooth((t-4)/1),turn=-.15)
        for j in range(4):parcel((-2.15+j*.42,1.12+.45*smooth((t-j*.4)/1),-.08),GOLD,t*.25+j)
        labels=[('Meet Testo',(.7,3.3,1.2),True)]
    elif name=='target':
        gate(0,-.5,VIOLET,smooth((t-2)/2))
        p=path((0,0,-2),(0,0,1.5),(t-1)/5)
        character(p,PINK,t,walk=1-smooth((t-5.7)/1),wave=.35*smooth((t-6)/1),turn=.15)
        character((-2.5,0,1.6),VIOLET,t,human=True,wave=.65,turn=.5)
        for j in range(14):
            a=j*2*math.pi/14+t*.28;ball((math.cos(a)*2.0,3.2+math.sin(a)*.05,-.5+math.sin(a)*.3),(.075,.075,.075),VIOLET)
        labels=[('5–10 MIN TARGET',(0,3.9,-.5),True),('Organization already configured',(-.3,.55,2.7),False)]
    elif name=='choose':
        for j,(x,col) in enumerate([(-3.2,BLUE),(0,PINK),(3.2,GOLD)]):
            box((x,.22,-.25),(.85,.22,.70),(.72,.71,.86))
            character((x,.42,-.25),col,t,scale=.80,wave=.75 if j==1 else .15,turn=.12*math.sin(t*.6+j))
        character((-1.7,0,1.9),VIOLET,t,human=True,reach=smooth(t/2),turn=-.4)
        for k in range(12):
            a=k*math.pi/6+t*.7;ball((math.cos(a)*1.0,.55,-.25+math.sin(a)*.8),(.055,.055,.055),PINK)
        labels=[('QA ENGINEER',(0,3.1,-.25),True),('Wider role vision',(-3.2,2.95,-.25),False),('Wider role vision',(3.2,2.95,-.25),False)]
    elif name=='configure':
        desk(-2.5,-.6);character((-2.65,0,.55),VIOLET,t,human=True,reach=.9,turn=.6)
        character((.95,0,.3),PINK,t,reach=.6,wave=.25,turn=-.2)
        # Orbiting tokens travel into the assignment; a physical ring outlines the scope.
        for j in range(4):
            progress=smooth((t-j*.6)/3);a=t*.7+j*math.pi/2
            p=path((math.cos(a)*2.1+.95,2.0+math.sin(t+j)*.3,math.sin(a)*1.4+.3),(.95,1.26,.75),progress*.80)
            parcel(p,[BLUE,GOLD,GREEN,VIOLET][j],t*.7+j)
        for j in range(30):
            a=j*2*math.pi/30;ball((.95+math.cos(a)*1.25,.13+smooth(t/3)*.07,.3+math.sin(a)*1.25),(.09,.035,.09),VIOLET)
        labels=[('NAME  ·  SCOPE  ·  POLICY',(.95,3.4,.3),True)]
    elif name=='assign':
        for j,x in enumerate([-3.6,0,3.6]):
            desk(x,-1.05,[BLUE,VIOLET,GREEN][j]);arrive=smooth((t-j*.9-.4)/3)
            p=path((x,2.1,-.1),(x,0,.1),arrive);scale=max(.05,arrive)
            character(p,PINK,t+j,scale=scale,wave=.7*smooth((t-j*.9-3)/1))
            character((x-.58,0,1.85),VIOLET,t+j,human=True,scale=.7,turn=.2)
            if arrive<1:
                for k in range(8):
                    a=k*math.pi/4+t*2;ball((x+math.cos(a)*.58,1.7-arrive*1.3,-.1+math.sin(a)*.58),(.05,.1,.05),PINK)
        labels=[('Distinct signed instances',(0,3.3,-1.05),True),('Employee 01',(-3.6,.7,2.8),False),('Employee 02',(0,.7,2.8),False),('Employee 03',(3.6,.7,2.8),False)]
    elif name=='verify':
        gate(-.65,.2,GREEN,smooth((t-2)/2));desk(3,-1)
        p=path((-2.4,0,.35),(1.0,0,.8),(t-.5)/5)
        character(p,PINK,t,walk=1-smooth((t-5)/1),wave=.8*smooth((t-5)/1),turn=.2)
        character((2.4,0,.85),VIOLET,t,human=True,wave=.8*smooth((t-5)/1),turn=-.3)
        for j in range(3):
            if t>j*.8+1:
                ball((-.65,2.97+j*.12,.2),(.16,.16,.16),GREEN)
        labels=[('VERIFIED',(-.65,3.45,.2),True),('Signature + owner + organization',(.3,.4,2.5),False)]
    elif name=='govern':
        character((-3.4,0,1.0),PINK,t,reach=.9,turn=.3)
        character((.2,0,1.3),VIOLET,t,human=True,reach=.7,turn=-.3)
        for j,(x,col,word) in enumerate([(-2.7,GREEN,'PLAN / ALLOW'),(0,AMBER,'BROWSER / REVIEW'),(2.7,PINK,'PRODUCTION / DENY')]):
            box((x,.45,-.65),(.30,.055,1.0),(.76,.76,.87));gate(x,-1.2,col,1 if j==0 else 0)
            progress=(t*.15+j*.25)%1
            z=.5-min(progress,.66 if j else 1)*2.1
            parcel((x,.76,z),col,t*.3)
            labels.append((word,(x,3.2,-1.2),j==0))
    else:
        for j,(x,col) in enumerate([(-2.5,BLUE),(0,PINK),(2.5,GOLD)]):
            advance=smooth(t/3);p=path((x,0,-.6),(x,0,1.0),advance)
            character(p,col,t+j,walk=1-smooth((t-2)/1),wave=.7*smooth((t-3)/1),turn=.14*math.sin(t*.5+j))
        character((-4.2,0,.6),VIOLET,t,human=True,wave=.7,turn=.4)
        for j in range(24):
            a=j*2.4;age=(t*.38+j*.13)%1
            box((math.cos(a)*4.8,4.7-age*2.6,math.sin(a)*2.0),(.035,.065,.025),[VIOLET,PINK,BLUE,GOLD][j%4],yaw(t+j))
        labels=[('SPECIALISTS. SHARED DIRECTION.',(0,3.65,.1),True)]
    return vp,labels

scenes=[];audio=[];cues=[];cursor=0;rate=22050
for scene in SPEC['scenes']:
    with wave.open(str(WORK/(scene['id']+'.wav'))) as wav:
        assert wav.getnchannels()==1 and wav.getsampwidth()==2 and wav.getframerate()==rate
        samples=np.frombuffer(wav.readframes(wav.getnframes()),dtype='<i2').copy()
    duration=len(samples)/rate+1.2;scene.update(start=cursor,duration=duration)
    audio.extend([np.zeros(round(rate*.45),dtype='<i2'),samples,np.zeros(round(rate*.75),dtype='<i2')])
    words=scene['narration'].split();c=cursor+.45
    for i in range(0,len(words),10):
        group=words[i:i+10];end=c+len(samples)/rate*len(group)/len(words);cues.append((c,end,' '.join(group)));c=end
    scenes.append(scene);cursor+=duration

def stamp(s,sep='.'):
    ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{sep}{ms%1000:03}'
def export_audio():
    sound=np.concatenate(audio).astype('f4')/32768;music=np.zeros(len(sound),dtype='f4');times=np.arange(len(sound))/rate
    # Original, quiet synthesised score: a warm four-chord pulse and scene chimes.
    for j in range(4):
        frequencies=[[130.81,164.81,196],[110,130.81,164.81],[87.31,110,130.81],[98,123.47,146.83]][j]
        mask=((times//4)%4==j);envelope=np.sin(np.pi*(times%4)/4)**.5
        for hz in frequencies:music+=np.sin(2*np.pi*hz*times)*.008*envelope*mask
    for scene in scenes:
        local=times-scene['start']-.15;env=np.exp(-np.maximum(local,0)*4)*(local>=0)*(local<1.2)
        music+=(np.sin(2*np.pi*660*local)+np.sin(2*np.pi*990*local))*.013*env
    # Duck the score under speech and fade the film edges.
    duck=1-np.minimum(1,np.abs(sound)*8)*.45;fade=np.minimum(1,times/1.1)*np.minimum(1,(cursor-times)/1.4)
    mixed=np.clip(sound+music*duck*fade,-.98,.98)
    with wave.open(str(WORK/'movie-audio.wav'),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes((mixed*32767).astype('<i2').tobytes())
    stem='agents-foundry-movie-v3'
    (OUT/(stem+'.vtt')).write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(a)} --> {stamp(b)} line:14%\n{c}' for a,b,c in cues)+'\n',encoding='utf8')
    (OUT/(stem+'.srt')).write_text('\n\n'.join(f'{i+1}\n{stamp(a,",")} --> {stamp(b,",")}\n{c}' for i,(a,b,c) in enumerate(cues))+'\n',encoding='utf8')
    (OUT/(stem+'-transcript.txt')).write_text(SPEC['title']+'\n\n'+SPEC['targetContext']+'\n\n'+'\n\n'.join(s['eyebrow']+'\n'+s['narration'] for s in scenes),encoding='utf8')

def frame(scene,t):
    fbo.clear(.875,.88,.97,1,depth=1)
    vp,labels=scene_draw(scene['id'],t,scene['duration'])
    ctx.copy_framebuffer(resolved,fbo)
    im=Image.frombytes('RGB',(W,H),resolved.read(components=3)).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert('RGBA')
    overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
    for text,pos,accent in labels:label(overlay,text,pos,vp,25,accent)
    d.rounded_rectangle((65,42,126,103),18,fill='#674bda');d.text((77,54),'AF',font=font(27,True),fill='white')
    d.text((145,58),'AGENTS FOUNDRY',font=font(26,True),fill='#27203c')
    chapter=scene['eyebrow'];width=font(23,True).getlength(chapter);d.text((W-65-width,61),chapter,font=font(23,True),fill='#67528f')
    # Small film lower third; the characters and world occupy the frame.
    d.rounded_rectangle((55,905,W-55,1042),26,fill=(255,255,255,234))
    d.text((88,924),scene['title'],font=font(43,True),fill='#251e3e')
    d.text((90,986),scene['subtitle'],font=font(26),fill='#67528f')
    progress=(scene['start']+t)/cursor;d.rectangle((65,1063,65+(W-130)*progress,1068),fill='#785bdf')
    if scene['id']=='outro' and t>3:
        d.text((1075,984),'agents-foundry.github.io',font=font(25,True),fill='#674bda')
    im.alpha_composite(overlay)
    # Short dip to pastel between locations preserves continuous character motion inside each shot.
    fade=min(1,t/.25,(scene['duration']-t)/.3)
    if fade<1:im=Image.blend(Image.new('RGBA',(W,H),(225,225,246,255)),im,max(0,fade))
    return im.convert('RGB')

export_audio()
if '--preview-only' in sys.argv:
    for scene in scenes:
        frame(scene,min(5,scene['duration']*.65)).save(WORK/(scene['id']+'-3d.jpg'),quality=92)
    frame(scenes[0],5).save(OUT/'onboarding-movie-v3-poster.jpg',quality=92)
    print('Saved eight 3D scene previews',flush=True);sys.exit(0)
import imageio_ffmpeg
target=OUT/'agents-foundry-movie-v3.mp4'
cmd=[os.environ.get('FFMPEG_BINARY') or imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(WORK/'movie-audio.wav'),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(target)]
process=subprocess.Popen(cmd,stdin=subprocess.PIPE);started=time.monotonic()
try:
    for scene in scenes:
        for n in range(round(scene['duration']*FPS)):
            im=frame(scene,n/FPS)
            if n==150:
                im.save(WORK/(scene['id']+'-3d.jpg'),quality=92)
                if scene['id']=='intro':im.save(OUT/'onboarding-movie-v3-poster.jpg',quality=92)
            process.stdin.write(im.tobytes())
        print(f'Rendered {scene["id"]}, elapsed {time.monotonic()-started:.1f}s',flush=True)
finally:process.stdin.close()
if process.wait()!=0:raise RuntimeError('Movie export failed')
(WORK/'movie-info.json').write_text(json.dumps({'duration':cursor,'width':W,'height':H,'fps':FPS,'bytes':target.stat().st_size,'renderer':ctx.info['GL_RENDERER'],'scenes':scenes},indent=2),encoding='utf8')
print(f'Exported {cursor:.1f}s 3D film, {target.stat().st_size/1048576:.1f} MB',flush=True)
