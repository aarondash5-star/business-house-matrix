"""Unseen flat illustrations: no semantic metadata passed to workers."""
import json,unittest,tempfile
from pathlib import Path
from PIL import Image,ImageDraw
from visual_yard_v2.worker import run

class UnseenDrawings(unittest.TestCase):
 def test_two_unseen_layouts(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);freeze=folder/'f.json'
   freeze.write_text(json.dumps({'state':'OWNER_FROZEN','lane1':{'frozen':True},'lane2':{'frozen':True},'allow':{'new_art_jobs':False},'release_authorized':False}))
   for idx in range(2):
    im=Image.new('RGB',(480,320),'#faf8f0');p=ImageDraw.Draw(im)
    shift=idx*58
    p.rectangle((65+shift,122,252+shift,284),fill='#7dc8bf',outline='#173a54',width=5)
    p.polygon([(52+shift,124),(158+shift,43),(271+shift,124)],fill='#e99569')
    p.ellipse((84+shift,154,129+shift,199),fill='#f3c872',outline='#173a54',width=4)
    p.rectangle((173+shift,213,211+shift,283),fill='#b57c59',outline='#173a54',width=4)
    p.ellipse((343-shift,50,391-shift,98),fill='#e8c252')
    target=folder/f'unseen{idx}.png';im.save(target)
    receipt=run(target,folder/f'out{idx}',freeze,'opencv')
    assert receipt['metrics']['shape_silhouette_iou_pct']>=80,receipt
    assert receipt['metrics']['edge_alignment_f1_pct']>=65,receipt
    assert receipt['owner_approved'] is False
if __name__=='__main__':unittest.main(verbosity=2)
