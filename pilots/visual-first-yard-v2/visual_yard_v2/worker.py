"""Bounded visual worker, evidence receipts and independent QA. No production side effects."""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,os,tempfile,time,traceback
from PIL import Image,ImageDraw
from .trace import vectorize,rasterize
from .metrics import measure,difference
from .review import make_review

THRESHOLDS={'shape_silhouette_iou_pct':90.,'edge_alignment_f1_pct':80.,'foreground_rgb_similarity_pct':90.}


def _sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _atomic(p:Path,data:dict)->None:
    p.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(dir=str(p.parent),prefix='.receipt-')
    try:
        with os.fdopen(fd,'w') as f:
            json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def _freeze_record(freeze:Path|None)->dict:
    if freeze is None:
        # No release authority without an actual owner freeze record.
        return {'state':'UNVERIFIED','release_authorized':False,'owner_art_unfreeze':False}
    o=json.loads(freeze.read_text())
    ok=o.get('state')=='OWNER_FROZEN' and o.get('lane1',{}).get('frozen') is True and o.get('lane2',{}).get('frozen') is True and o.get('allow',{}).get('new_art_jobs') is False and o.get('release_authorized') is False
    if not ok:raise PermissionError('owner_freeze_missing_or_invalid')
    return {'state':'OWNER_FROZEN','release_authorized':False,'owner_art_unfreeze':False}


def _montage(target:Path,result:Path,diff:Path,out:Path) -> None:
    a=Image.open(target).convert('RGB');b=Image.open(result).convert('RGB');c=Image.open(diff).convert('RGB')
    w,h=a.size;board=Image.new('RGB',(3*w+40,h+65),'#101922');d=ImageDraw.Draw(board)
    for i,(name,im) in enumerate([('REFERENCE',a),('GENERATED VECTOR',b),('PIXEL DIFFERENCE',c)]):
        x=i*(w+15)+10;d.text((x,14),name,fill='white');board.paste(im,(x,44))
    board.save(out)


def run(reference:str|Path,output:str|Path,freeze:str|Path|None=None,engine:str='auto',max_attempts:int=2)->dict:
    ref=Path(reference);dest=Path(output);freeze_file=Path(freeze) if freeze else None
    if not ref.is_file() or ref.stat().st_size>16*1024*1024:raise ValueError('invalid_reference')
    with Image.open(ref) as input_image:
        w,h=input_image.size
    if w*h>16_000_000:raise ValueError('reference_too_large')
    _freeze_record(freeze_file)
    dest.mkdir(parents=True,exist_ok=True)
    receipt=dest/'qa_receipt.json';started=time.monotonic()
    target_digest=_sha(ref)
    result={'project':'shaadi_aunty_dodge','mode':'ISOLATED_VECTOR_TRACE','source':'reference_pixels_only',
      'input_sha256':target_digest,'art_lanes_frozen':bool(freeze_file),'owner_approved':False,
      'creative_certified':False,'production_merge_allowed':False,'qa_outcome':'PENDING',
      'evaluated_at_utc':datetime.now(timezone.utc).isoformat(),'attempts':[],
      'thresholds':THRESHOLDS,'trace_not_freehand_recreation':True}
    _atomic(receipt,result)
    try:
        if max_attempts<1 or max_attempts>2:raise ValueError('attempt_bounds_1_or_2')
        engines=([engine] if engine!='auto' else ['vtracer','opencv'])[:max_attempts]
        for attempt,e in enumerate(engines,1):
            _freeze_record(freeze_file)
            sv=dest/f'candidate_{attempt}.svg';png=dest/f'candidate_{attempt}.png'
            try:
                r=vectorize(ref,sv,e)
                rasterize(sv,png,w,h)
                m=measure(ref,png)
                meta={'attempt':attempt,'engine':r['engine'],'render_sha256':_sha(png),
                      'svg_sha256':_sha(sv),'metrics':m,'editable_paths':r['editable_paths'],'status':'EVALUATED'}
                result['attempts'].append(meta)
            except Exception as exc:
                result['attempts'].append({'attempt':attempt,'engine':e,'status':'FAILED','error':type(exc).__name__+': '+str(exc)[:180]})
            _atomic(receipt,result)
        evaluated=[a for a in result['attempts'] if a['status']=='EVALUATED']
        if not evaluated:raise RuntimeError('no_valid_vector_output')
        best=max(evaluated,key=lambda a:a['metrics']['weighted_pixel_closeness_pct'])
        index=best['attempt'];chosen=dest/f'candidate_{index}.png'
        (dest/'result.png').write_bytes(chosen.read_bytes())
        (dest/'result.svg').write_bytes((dest/f'candidate_{index}.svg').read_bytes())
        difference(ref,chosen,dest/'difference.png')
        _montage(ref,chosen,dest/'difference.png',dest/'side_by_side.png')
        passed=all(best['metrics'][name]>=minimum for name,minimum in THRESHOLDS.items())
        result.update({'best_engine':best['engine'],'metrics':best['metrics'],
          'best_attempt':index,'render_sha256':_sha(dest/'result.png'),
          'vector_sha256':_sha(dest/'result.svg'),'visual_gate':('PASSED_AUTOMATED_THRESHOLDS' if passed else 'REWORK_REQUIRED'),
          'qa_outcome':'OWNER_VISUAL_REVIEW_REQUIRED' if passed else 'VISUAL_REWORK_REQUIRED',
          'duration_seconds':round(time.monotonic()-started,2)})
        make_review(ref,dest)
        _freeze_record(freeze_file)
    except Exception as exc:
        result.update({'qa_outcome':'FAIL_CLOSED','error':type(exc).__name__+': '+str(exc)[:240],
                       'duration_seconds':round(time.monotonic()-started,2)})
    _atomic(receipt,result)
    return result
