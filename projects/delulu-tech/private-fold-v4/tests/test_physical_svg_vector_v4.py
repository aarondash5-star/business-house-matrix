import unittest,ast
from pathlib import Path
class FrozenVectorAnimationTests(unittest.TestCase):
 def setUp(self):
  self.script=Path("backend/physical_svg_vector_v4.py").read_text()
  self.tree=ast.parse(self.script)
 def test_original_svg_is_source(self):
  self.assertIn('bpy.ops.import_curve.svg',self.script)
  self.assertIn('d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368',self.script)
 def test_mesh_and_shape_keys(self):
  for token in ("obj.shape_key_add","sk.keyframe_insert","bpy.ops.object.convert","curve"):
   if token!="curve":self.assertIn(token,self.script)
 def test_actual_motion_range(self):
  self.assertIn("sc.frame_end=49",self.script)
  self.assertIn("sc.render.fps=12",self.script)
  self.assertIn('timeline=[1,13,25,37,49]',self.script)
 def test_keyframes_and_final_original_geometry(self):
  self.assertIn('05_frozen_exact_vector',self.script)
  self.assertIn('original=[',self.script)
  self.assertIn('float((f!=49)',self.script)
 def test_backface_geometry_not_fake_alpha(self):
  self.assertIn('o.data.extrude=.0018',self.script)
  self.assertIn('polygon.normal.z<-.6',self.script)
  self.assertNotIn('alpha_from_svg(',self.script)
  self.assertNotIn('reveal=smooth(',self.script)
 def test_no_self_acceptance_or_publication(self):
  self.assertIn('"owner_approved":False',self.script)
  self.assertIn('"release_authorized":False',self.script)
  self.assertIn('"independent_review":False',self.script)
 def test_thermal_gate(self):
  self.assertIn('if t is not None and t>73:',self.script)
if __name__=="__main__":unittest.main()
