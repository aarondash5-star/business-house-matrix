"""Independent pixel/geometry scores. Never declares an owner or artistic approval."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def _mask(img: np.ndarray) -> np.ndarray:
    # Compare to the upper-left corner; flat illustration background convention.
    return np.max(np.abs(img-img[0,0]),axis=2)>24


def _edges(img: np.ndarray) -> np.ndarray:
    dx=np.zeros(img.shape[:2], dtype=np.float32)
    dy=dx.copy()
    dx[:,1:]=np.abs(img[:,1:]-img[:,:-1]).mean(axis=2)
    dy[1:,:]=np.abs(img[1:,:]-img[:-1,:]).mean(axis=2)
    return np.maximum(dx,dy)>30


def _dilate(mask: np.ndarray) -> np.ndarray:
    return np.array(Image.fromarray((mask.astype('uint8')*255)).filter(ImageFilter.MaxFilter(7)))>0


def measure(reference: str | Path, candidate: str | Path) -> dict:
    a=np.asarray(Image.open(reference).convert('RGB'),dtype=np.float32)
    b=np.asarray(Image.open(candidate).convert('RGB'),dtype=np.float32)
    if a.shape!=b.shape or a.ndim!=3 or a.shape[2]!=3:
        raise ValueError('image_dimension_mismatch')
    mae=np.abs(a-b).mean(axis=2)
    rgb_similarity=max(0.,1-mae.mean()/255.)
    ma=_mask(a); mb=_mask(b)
    union=(ma|mb); overlap=(ma&mb)
    silhouette=overlap.sum()/max(1,union.sum())
    foreground=max(0.,1-mae[union].mean()/255) if union.any() else 0.
    ea=_edges(a);eb=_edges(b)
    precision=(eb & _dilate(ea)).sum()/max(1,eb.sum())
    recall=(ea & _dilate(eb)).sum()/max(1,ea.sum())
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.
    weighted=0.2*rgb_similarity+0.4*foreground+0.25*silhouette+0.15*f1
    metrics={'global_rgb_similarity_pct':round(100*rgb_similarity,1),
             'foreground_rgb_similarity_pct':round(100*foreground,1),
             'shape_silhouette_iou_pct':round(100*silhouette,1),
             'edge_alignment_f1_pct':round(100*f1,1),
             'weighted_pixel_closeness_pct':round(100*weighted,1)}
    return {k:round(float(v),1) for k,v in metrics.items()}


def difference(reference: str | Path,candidate: str | Path,out: str | Path) -> None:
    a=np.asarray(Image.open(reference).convert('RGB'),dtype=np.int16)
    b=np.asarray(Image.open(candidate).convert('RGB'),dtype=np.int16)
    e=np.abs(a-b).mean(axis=2)
    red=np.stack([np.minimum(255,e*2),np.minimum(160,e*.4),np.minimum(120,e*.3)],axis=2).astype('uint8')
    red[e<12]=[19,34,43]
    Image.fromarray(red).save(out)
