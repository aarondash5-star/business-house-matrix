import json,unittest,tempfile,sys,hashlib,copy
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from .fixture import create
from visual_yard_v2.metrics import measure
from visual_yard_v2.worker import run
from visual_yard_v2.trace import rasterize
from visual_yard_v2.review import make_review

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.reference=self.root/'reference.png'
        digest=create(self.reference)
        self.assertEqual(digest,'7a02f3a72316378db5201c8fe38e0226ecaad8f1ab389ecd2f37fec6a65781f3')
        freeze={'state':'OWNER_FROZEN','lane1':{'frozen':True},'lane2':{'frozen':True},'allow':{'new_art_jobs':False},'release_authorized':False}
        self.freeze=self.root/'owner_freeze.json';self.freeze.write_text(json.dumps(freeze))

    def test_same_exact_target_no_oracle_passed(self):
        out=self.root/'output'
        report=run(self.reference,out,self.freeze,'opencv')
        self.assertGreater(report['metrics']['weighted_pixel_closeness_pct'],57.2)
        self.assertGreater(report['metrics']['shape_silhouette_iou_pct'],90)
        self.assertGreater(report['metrics']['edge_alignment_f1_pct'],80)
        self.assertFalse(report['creative_certified'])
        self.assertFalse(report['owner_approved'])
        self.assertFalse(report['production_merge_allowed'])
        self.assertEqual(report['qa_outcome'],'VISUAL_REWORK_REQUIRED') # hard foreground gate must be respected
        self.assertTrue((out/'result.svg').read_text().count('<path')>2)
        self.assertNotIn('data:image', (out/'result.svg').read_text())
        make_review(self.reference,out)
        self.assertTrue((out/'index.html').is_file())

    def test_freeze_bad_record_fails_closed(self):
        self.freeze.write_text('{}')
        with self.assertRaises(PermissionError):run(self.reference,self.root/'bad',self.freeze)
        self.assertFalse((self.root/'bad'/'result.png').exists())

    def test_fail_closed_if_renderer_missing(self):
        with patch('visual_yard_v2.worker.vectorize',side_effect=RuntimeError('offline')):
            r=run(self.reference,self.root/'bad',self.freeze,'opencv')
        self.assertEqual(r['qa_outcome'],'FAIL_CLOSED')
        self.assertFalse((self.root/'bad'/'result.png').exists())

    def test_reject_untrusted_svg_content(self):
        p=self.root/'bad.svg';p.write_text('<svg><script>alert(1)</script></svg>')
        with self.assertRaises(ValueError):rasterize(p,self.root/'bad.png',600,400)

    def test_independent_difference_fails_for_incorrect_image(self):
        wrong=self.root/'wrong.png';Image.new('RGB',(600,400),'#fefefe').save(wrong)
        r=measure(self.reference,wrong)
        self.assertLess(r['shape_silhouette_iou_pct'],10)

    def test_no_hidden_approval_in_receipt(self):
        r=run(self.reference,self.root/'ok',self.freeze,'opencv')
        d=json.loads((self.root/'ok'/'qa_receipt.json').read_text())
        self.assertFalse(d['owner_approved'])
        self.assertFalse(d['creative_certified'])
        self.assertTrue(d['art_lanes_frozen'])

if __name__=='__main__':unittest.main(verbosity=2)
