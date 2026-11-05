"""Exact pixel-level reproduction of prior benchmark reference for regression testing ONLY."""
from PIL import Image,ImageDraw
from pathlib import Path
import hashlib

def create(out):
    W,H=600,400
    # This is the earlier trusted fixture renderer. Test oracle is never passed to the worker.
    HEX=lambda x:x
    def numbers(v):return [round(float(x)*2) for x in v]
    shapes=[
 {'type':'ellipse','bbox':[64,55,128,119],'fill':'#F5CA5F'},
 {'type':'line','bbox':[94,43,94,31],'stroke':'#F5CA5F','stroke_width':5},
 {'type':'line','bbox':[56,86,42,86],'stroke':'#F5CA5F','stroke_width':5},
 {'type':'line','bbox':[138,86,152,86],'stroke':'#F5CA5F','stroke_width':5},
 {'type':'line','bbox':[71,58,61,48],'stroke':'#F5CA5F','stroke_width':5},
 {'type':'line','bbox':[117,58,127,48],'stroke':'#F5CA5F','stroke_width':5},
 {'type':'line','bbox':[67,330,544,330],'stroke':'#5D9F78','stroke_width':6},
 {'type':'rectangle','bbox':[466,233,490,328],'fill':'#B87750','stroke':'#203A4E','stroke_width':4},
 {'type':'ellipse','bbox':[424,158,528,262],'fill':'#54A578','stroke':'#203A4E','stroke_width':5},
 {'type':'ellipse','bbox':[447,132,513,207],'fill':'#54A578','stroke':'#203A4E','stroke_width':4},
 {'type':'rectangle','bbox':[188,167,387,331],'fill':'#73C8C4','stroke':'#203A4E','stroke_width':6},
 {'type':'polygon','points':[[168,173],[289,91],[407,173]],'fill':'#ED975C','stroke':'#203A4E','stroke_width':7},
 {'type':'rectangle','bbox':[270,248,316,329],'fill':'#E5A56D','stroke':'#203A4E','stroke_width':5},
 {'type':'ellipse','bbox':[228,202,263,237],'fill':'#FFF8DA','stroke':'#203A4E','stroke_width':5},
 {'type':'ellipse','bbox':[325,202,360,237],'fill':'#FFF8DA','stroke':'#203A4E','stroke_width':5},
 {'type':'ellipse','bbox':[302,287,309,294],'fill':'#203A4E'}]
    im=Image.new('RGB',(W*2,H*2),'#FCF8EF'); d=ImageDraw.Draw(im)
    for it in shapes:
        k=it['type'];fill=it.get('fill');stroke=it.get('stroke');sw=int(it.get('stroke_width',0)*2)
        if k in ('ellipse','rectangle','line'):
            bbox=numbers(it['bbox'])
            if k=='ellipse':d.ellipse(bbox,fill=fill,outline=stroke,width=sw)
            elif k=='rectangle':d.rectangle(bbox,fill=fill,outline=stroke,width=sw)
            else:d.line(bbox,fill=stroke or fill or '#203B4D',width=max(2,sw),joint='curve')
        else:
            pts=[tuple(numbers(p)) for p in it['points']]
            d.polygon(pts,fill=fill)
            if stroke and sw:d.line(pts+[pts[0]],fill=stroke,width=sw,joint='curve')
    im.resize((W,H),Image.Resampling.LANCZOS).save(out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()
if __name__=='__main__':
    from sys import argv
    print(create(argv[1]))
