#!/usr/bin/env python3
"""Recrea el logo Alleanza Academy como PNG transparente (supersampled).
Genera versión a color (fondos claros) y versión wordmark blanco (fondos oscuros)."""
import math
from PIL import Image, ImageDraw, ImageFont

SS = 4
W, H = 1820, 720
NAVY   = (6, 19, 48, 255)
NAVYTX = (10, 20, 46, 255)
PURPLE = (124, 70, 166, 255)
WHITE  = (244, 245, 248, 255)
BASE = "/tmp/claude-0/-home-user-alleanzaacademy/147edd4c-26bd-5fd6-a68b-8407a942b324/scratchpad/"

def bez(p0,p1,p2,n=40):
    out=[]
    for i in range(n+1):
        t=i/n; mt=1-t
        out.append((mt*mt*p0[0]+2*mt*t*p1[0]+t*t*p2[0],
                    mt*mt*p0[1]+2*mt*t*p1[1]+t*t*p2[1]))
    return out

def star_pts(cx,cy,ro,ri,rot=-90):
    p=[]
    for i in range(10):
        a=math.radians(rot+i*36); r=ro if i%2==0 else ri
        p.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    return p

def shield_outline(cx,top,halfw,bottom):
    straight=top+0.42*(bottom-top)
    right=[(cx-halfw,top),(cx+halfw,top),(cx+halfw,straight)]
    right+=bez((cx+halfw,straight),(cx+halfw*0.96,bottom-0.02*(bottom-top)),(cx,bottom))
    left=bez((cx,bottom),(cx-halfw*0.96,bottom-0.02*(bottom-top)),(cx-halfw,straight))
    return right+left

def render(wordmark_color, outfile, mark_only=False):
    img=Image.new("RGBA",(W*SS,H*SS),(0,0,0,0))
    d=ImageDraw.Draw(img)
    def S(v): return int(round(v*SS))
    def poly(pts,c): d.polygon([(S(x),S(y)) for x,y in pts],fill=c)

    cx,top,halfw,bottom,border=235,175,205,690,26
    # stars
    for sx,sy,ro in [(cx,top-92,60),(cx-150,top-44,42),(cx+150,top-44,42)]:
        poly(star_pts(sx,sy,ro,ro*0.42),PURPLE)
    # shield
    poly(shield_outline(cx,top,halfw,bottom),PURPLE)
    poly(shield_outline(cx,top+border,halfw-border,bottom-border*1.6),NAVY)
    # emblem
    ex=cx; apexY=top+92; baseY=bottom-92; bw=158; apex=(ex,apexY)
    right_edge=bez((ex+bw,baseY),(ex+bw*0.78,(apexY+baseY)/2),apex,30)
    left_edge =bez(apex,(ex-bw*0.78,(apexY+baseY)/2),(ex-bw,baseY),30)
    poly([(ex-bw,baseY),(ex+bw,baseY)]+list(reversed(right_edge))+left_edge,WHITE)
    for sgn in (-1,1):
        gx=ex+sgn*bw*0.42; gw=bw*0.075
        top_in=baseY-(baseY-apexY)*0.55; lean=-sgn*bw*0.16
        poly([(gx-gw,baseY),(gx+gw,baseY),(gx+gw*0.25+lean,top_in),(gx-gw*0.25+lean,top_in)],NAVY)
    peakH=baseY-apexY; cwb=bw*0.16
    poly([(ex,apexY+peakH*0.18),(ex+cwb,apexY+peakH*0.52),(ex-cwb,apexY+peakH*0.52)],NAVY)

    if not mark_only:
        fp="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        f_main=ImageFont.truetype(fp,S(150)); f_sub=ImageFont.truetype(fp,S(92))
        def tracked(text,x,y,font,fill,tr):
            cur=x
            for ch in text:
                d.text((S(cur),S(y)),ch,font=font,fill=fill)
                cur+=d.textlength(ch,font=font)/SS+tr
        wx=505
        tracked("ALLEANZA",wx,232,f_main,wordmark_color,6)
        allw=sum(d.textlength(c,font=f_main)/SS for c in "ALLEANZA")+6*7
        acw=sum(d.textlength(c,font=f_sub)/SS for c in "ACADEMY")+34*6
        tracked("ACADEMY",wx+(allw-acw)/2,455,f_sub,PURPLE,34)

    out=img.resize((W,H),Image.LANCZOS)
    if mark_only:
        out=out.crop((0,0,470,H))
    out.save(BASE+outfile)
    return out

render(NAVYTX,"alleanza_logo.png")
render((255,255,255,255),"alleanza_logo_white.png")
render(NAVYTX,"alleanza_mark.png",mark_only=True)

# composite check on navy
w=Image.open(BASE+"alleanza_logo_white.png")
bg=Image.new("RGBA",(W,H),(6,19,48,255)); bg.alpha_composite(w)
bg.convert("RGB").save(BASE+"check_white_on_navy.png")
print("ok")
