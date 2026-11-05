"""Colour vectorization, preserving geometry without leaking oracle coordinates.

Select VTracer first when installed (dual MIT/Apache-2.0); OpenCV contours are the
fallback. Neither mode calls a language model or copies hidden source geometry.
"""
from __future__ import annotations
import html
from pathlib import Path
from PIL import Image
import numpy as np


def _hex(rgb:tuple[int,int,int]) -> str:
    return '#%02x%02x%02x'%rgb


def _contour_svg(png:Path,out:Path,colors:int=22) -> dict:
    try:import cv2
    except ImportError as exc:raise RuntimeError('OpenCV is required for the contour fallback; install opencv-python-headless') from exc
    rgb=Image.open(png).convert('RGB')
    w,h=rgb.size
    if not(32<=w<=4096 and 32<=h<=4096):raise ValueError('unsupported_image_dimensions')
    # No dithering: regions remain contiguous/editable. Use a colour palette, not
    # decoded prompt/source coordinates. Interpolate only at vector-render stage.
    q=rgb.quantize(colors=colors,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    idx=np.asarray(q,dtype=np.uint8)
    pal=q.getpalette()
    uniq, counts=np.unique(idx,return_counts=True)
    # Background is first, followed by lowest-to-highest coverage regions.
    bg=int(idx[0,0]);order=[bg]+[int(x) for x in uniq[np.argsort(-counts)] if int(x)!=bg]
    fragments=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    parts=0
    for ci in order:
        color=tuple(int(x) for x in pal[ci*3:ci*3+3]);mask=np.where(idx==ci,255,0).astype('uint8')
        # Border via cv2 contours. RETR_CCOMP + evenodd works for holes.
        contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        ps=[]
        for ctr in contours:
            # Trace each color cluster, preserving tiny but meaningful islands.
            if len(ctr)<2:
                x,y=ctr[0][0];ps.append(f'M{x} {y}h1v1h-1z');continue
            poly=cv2.approxPolyDP(ctr,epsilon=.35,closed=True)
            pts=poly[:,0,:]
            if len(pts)<3:continue
            path='M'+' '.join(f'{int(pt[0])} {int(pt[1])}' if i==0 else f'L{int(pt[0])} {int(pt[1])}' for i,pt in enumerate(pts))+'Z'
            ps.append(path)
        if not ps:continue
        fragments.append(f'<path fill="{_hex(color)}" fill-rule="evenodd" d="{" ".join(ps)}"/>')
        parts+=1
    fragments.append('</svg>')
    out.write_text('\n'.join(fragments),encoding='utf-8')
    return {'engine':'opencv-quantized-contours','palette_colors':len(order),'editable_paths':parts,'width':w,'height':h}


def vectorize(input_path:str|Path,svg_path:str|Path,engine:str='auto') -> dict:
    p=Path(input_path);out=Path(svg_path)
    if p.suffix.lower() not in ('.png','.jpg','.jpeg','.webp') or not p.is_file():raise ValueError('unsupported_input')
    out.parent.mkdir(parents=True,exist_ok=True)
    if engine in ('auto','vtracer'):
        try:
            import vtracer
            vtracer.convert_image_to_svg_py(str(p),str(out),colormode='color',hierarchical='stacked',
                mode='spline',filter_speckle=3,color_precision=8,layer_difference=12,
                corner_threshold=60,length_threshold=4.0,max_iterations=10,
                splice_threshold=45,path_precision=3)
            text=out.read_text()
            if '<svg' not in text or '<path' not in text:raise ValueError('invalid_vtracer_svg')
            return {'engine':'vtracer','editable_paths':text.count('<path')}
        except ImportError:
            if engine=='vtracer':raise RuntimeError('VTracer is not installed')
    if engine not in ('auto','opencv'):raise ValueError('unknown_engine')
    return _contour_svg(p,out)


def rasterize(svg_path:str|Path,png_path:str|Path,width:int,height:int) -> None:
    # SVG comes only from the known vectorizer, never from an untrusted API.
    # Reject embedded images, scripts, URLs and entity references before conversion.
    s=Path(svg_path).read_text()
    lower=s.lower()
    if any(k in lower for k in ('<script','<image','<!entity','<!doctype','foreignobject','javascript:','xlink:href','href=','url(')):
        raise ValueError('unsafe_svg_source')
    try:import cairosvg
    except ImportError as exc:raise RuntimeError('CairoSVG required to rasterize vectors') from exc
    cairosvg.svg2png(bytestring=s.encode(),write_to=str(png_path),output_width=width,output_height=height)
