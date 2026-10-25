#!/usr/bin/env python3
"""Delulu V2 private exact-logo MP4 builder executed on Dell Dev Tool Yard.
Uses immutable branded SVG and installed OSS sharp/numpy/Pillow/FFmpeg.
No external calls, publication, geometry changes, or auto approval.
"""
from __future__ import annotations
import argparse,hashlib,io,json,math,os,subprocess,sys,time
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/"brand"/"assets"/"delulu-tech-mobile-white.svg"
OUTPUT=HERE/"assets"
APPROVED_SHA="d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368"
TOOLKIT=Path("/var/lib/generic-linux-automator-exec/matrix-game-toolkit-20261025")
SHARP=TOOLKIT/"node_modules"/"sharp"
INK=np.array([11,13,19],np.float32)
WHITE=np.array([245,246,242],np.float32)
VIOLET=np.array([101,68,234],np.float32)
VOLT=np.array([201,255,61],np.float32)

def smooth(v):
    x=np.clip(v,0,1)
    return x*x*(3-2*x)
def temperature():
    p=Path("/sys/class/thermal/thermal_zone0/temp")
    try:return round(int(p.read_text())/1000,1)
    except Exception:return None
def check_temperature():
    value=temperature()
    if value is not None and value>75:
        raise RuntimeError("Thermal gate triggered: "+str(value)+" C")
    return value
def alpha_from_svg(width):
    script="""const sharp=require(process.argv[1]);const fs=require('fs');
      const file=process.argv[2],width=Number(process.argv[3]);
      sharp(file).resize({width}).ensureAlpha().png().toBuffer()
        .then(data=>process.stdout.write(data)).catch(e=>{console.error(e);process.exit(1)})"""
    p=subprocess.run(["node","-e",script,str(SHARP),str(SOURCE),str(width)],
                     capture_output=True,timeout=35,check=True)
    return np.asarray(Image.open(io.BytesIO(p.stdout)).convert("RGBA"))[:,:,3].copy()
def make_background(w,h):
    yy,xx=np.ogrid[:h,:w]
    xx=xx.astype(np.float32);yy=yy.astype(np.float32)
    distance=((xx-w*.52)/(.83*w))**2+((yy-h*.48)/(.82*h))**2
    light=np.maximum(0,1-distance)**2
    return np.uint8(np.clip(INK[None,None,:]+light[:,:,None]*np.array([5,4,9],np.float32),0,255))
def render(mode):
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=APPROVED_SHA:
        raise RuntimeError("FROZEN SVG HASH MISMATCH")
    if mode=="landscape":w,h=1920,1080
    else:w,h=1080,1920
    check_temperature()
    lw=int((.78*w if mode=="landscape" else .91*w)//2*2)
    alpha=alpha_from_svg(lw)
    lh=alpha.shape[0]
    x0=(w-lw)//2
    y0=(h-lh)//2+(5 if mode=="landscape" else -45)
    assert x0>=0 and y0>=0 and x0+lw<=w and y0+lh<=h
    a=alpha.astype(np.float32)/255.
    ca=np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(7)),dtype=np.float32)/255.
    yy,xx=np.mgrid[:lh,:lw].astype(np.float32)
    base=make_background(w,h)
    name=OUTPUT/("delulu-logo-"+mode+".mp4")
    proc=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-y",
       "-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24",
       "-s",f"{w}x{h}","-r","30","-i","-",
       "-an","-c:v","libx264","-preset","veryfast","-crf","19",
       "-pix_fmt","yuv420p","-movflags","+faststart",str(name)],
       stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    started=time.monotonic();thermal=[]
    for k in range(120):
        if k%15==0: thermal.append(check_temperature())
        t=k/30.
        frame=base.copy()
        roi=frame[y0:y0+lh,x0:x0+lw].astype(np.float32)
        up=smooth((t-.34)/1.36)
        front=-.14*lw+up*1.32*lw
        wave=18*np.sin(yy/lh*7+up*5.4)+12*np.cos(yy/lh*13-up*6.5)
        edge=front+wave
        reveal=smooth((edge-xx+11)/32)
        if t>=1.7:reveal=np.ones_like(reveal)
        if t<.34:reveal*=0
        ridge=np.exp(-((xx-edge)/24)**2)
        fold=np.exp(-((xx-(edge-30))/100)**2)*(1-reveal*.26)
        phase=smooth((t-1.32)/.89)
        vx=(-.28+1.56*phase)*lw+.10*lw*np.sin(yy/lh*3.2+phase*2)
        violet=np.exp(-((xx-vx)/(lw*.078))**2) *(smooth((t-1.30)/.17)*(1-smooth((t-2.18)/.23)))
        gate=smooth((t-2.13)/.12)*(1-smooth((t-2.44)/.14))
        lx=lw*(.31+.4*smooth((t-2.13)/.34))
        lime=np.exp(-((xx-lx)/(lw*.032))**2)*gate
        visible=a*reveal
        aura=(ca*reveal*(.11*violet+.19*lime))[:,:,None]
        roi+=(VIOLET-INK)[None,None,:]*aura*.65
        color=WHITE[None,None,:]+(VIOLET-WHITE)[None,None,:]*np.clip(.45*ridge*up+.83*violet+.10*fold,0,1)[:,:,None]
        color+=(VOLT-WHITE)[None,None,:]*np.clip(.85*lime,0,1)[:,:,None]
        color+=ridge[:,:,None]*15*smooth((t-.35)/.3)
        roi=roi*(1-visible[:,:,None])+np.clip(color,0,255)*visible[:,:,None]
        rim=np.maximum(0,ca-a)*violet*.37
        roi+=(VIOLET-INK)[None,None,:]*rim[:,:,None]
        frame[y0:y0+lh,x0:x0+lw]=np.uint8(np.clip(roi,0,255))
        if k==119:
            Image.fromarray(frame).save(OUTPUT/("delulu-"+mode+"-last-frame.png"),optimize=True)
        try:proc.stdin.write(frame.tobytes())
        except BrokenPipeError:
            raise RuntimeError("Encoder pipe broken")
    proc.stdin.close()
    error=proc.stderr.read()
    if proc.wait(timeout=60):raise RuntimeError("encoder failed: "+error.decode(errors="replace")[-2000:])
    receipt={"mode":mode,"w":w,"h":h,"duration":4,"fps":30,"frames":120,
             "audio":False,"codec":"h264","temperature_samples_c":thermal,
             "svg_sha256":APPROVED_SHA,"output_sha256":hashlib.sha256(name.read_bytes()).hexdigest(),
             "size_bytes":name.stat().st_size,"seconds_elapsed":round(time.monotonic()-started,1),
             "status":"private_review_only"}
    (OUTPUT/("motion-receipt-"+mode+".json")).write_text(json.dumps(receipt,indent=2))
    print(json.dumps(receipt),flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=("landscape","portrait"))
    args=parser.parse_args()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    render(args.mode)
