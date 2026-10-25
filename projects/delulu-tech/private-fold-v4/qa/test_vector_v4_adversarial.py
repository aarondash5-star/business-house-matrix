import hashlib,ast,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
class VectorVsMaskCertification(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.new=(HERE/"candidate_v4.py").read_text()
  cls.old=(HERE/"rejected_v2.py").read_text()
 def test_actual_source_hash_v4(self):
  self.assertEqual(hashlib.sha256((HERE/"candidate_v4.py").read_bytes()).hexdigest(),"13db2da05467b4b0f93659eeee7feb133114f45b3107b6aa9cb89c28b7277ba3")
 def test_old_source_is_known_bad(self):
  self.assertEqual(hashlib.sha256((HERE/"rejected_v2.py").read_bytes()).hexdigest(),"924f4e29ebc6fbe8f19a3acaf16558c4e3f046181d3d67042b9b73e261c6ab00")
  self.assertIn("alpha_from_svg(",self.old)
 def test_original_svg_is_true_mesh_input(self):
  self.assertIn("bpy.ops.import_curve.svg",self.new)
  self.assertIn("bpy.ops.object.convert",self.new)
 def test_animation_not_static_alpha(self):
  self.assertIn("shape_key_add",self.new)
  self.assertIn("keyframe_insert",self.new)
  self.assertNotIn("alpha_from_svg(",self.new)
 def test_final_shape_key_basis(self):
  self.assertIn("sc.frame_set(49)",self.new)
  self.assertIn("float((f!=49)",self.new)
  self.assertIn("05_frozen_exact_vector",self.new)
 def test_physical_surfaces(self):
  self.assertIn('o.data.extrude=.0018',self.new)
  self.assertIn("polygon.normal.z<-.6",self.new)
 def test_no_release_or_self_qa(self):
  self.assertIn('"owner_approved":False',self.new)
  self.assertIn('"independent_review":False',self.new)
  self.assertIn('"release_authorized":False',self.new)
 def test_original_sha_pinned(self):
  self.assertIn("d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368",self.new)
if __name__=="__main__":unittest.main()

