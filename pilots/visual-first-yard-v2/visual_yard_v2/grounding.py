"""OpenCV-based spatial measurement, not a neural object labeler.

Exposes normalized coordinates and a confidence proxy for individual major
colour regions. This catches left-vs-right mistakes, but supplies no semantic
noun labels. Florence-2 remains optional/future.
"""
from pathlib import Path
from PIL import Image
import numpy as np


def extract_regions(image:str|Path, min_fraction:float=.003) -> list[dict]:
    try:import cv2
    except ImportError as e:raise RuntimeError('OpenCV required for region grounding') from e
    rgb=np.asarray(Image.open(image).convert('RGB'))
    h,w=rgb.shape[:2]
    q=Image.fromarray(rgb).quantize(colors=12,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    idx=np.asarray(q)
    pal=q.getpalette()
    detected=[]
    bg=int(idx[0,0])
    for color in np.unique(idx):
        if int(color)==bg:continue
        mask=(idx==color).astype(np.uint8)
        n, labels,stats,cents=cv2.connectedComponentsWithStats(mask,connectivity=8)
        for i in range(1,n):
            x,y,cw,ch,area=(int(v) for v in stats[i]);fraction=area/(h*w)
            if fraction<min_fraction:continue
            r,g,b=(int(v) for v in pal[int(color)*3:int(color)*3+3])
            detected.append({'bbox_xywh_norm':[round(x/w,4),round(y/h,4),round(cw/w,4),round(ch/h,4)],
                             'center_norm':[round(cents[i][0]/w,4),round(cents[i][1]/h,4)],
                             'area_fraction':round(fraction,4),'color':'#%02x%02x%02x'%(r,g,b),
                             'type':'color_component','confidence':'image_segmentation_not_semantic'})
    return sorted(detected,key=lambda item:item['area_fraction'],reverse=True)
