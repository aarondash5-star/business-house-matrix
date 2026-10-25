import ast,sys,unittest
from pathlib import Path
class FoldGuardTests(unittest.TestCase):
 def setUp(self):
  self.text=Path('backend/private_fold_keyframes.py').read_text()
  self.tree=ast.parse(self.text)
 def test_actual_mesh_geometry_not_fake_mask(self):
  for x in ('mesh.from_pydata','bpy.ops.render.render','bpy.ops.wm.save_as_mainfile','distinct_depth_values','front_faces','back_faces'):
   self.assertIn(x,self.text)
  self.assertNotIn('alpha_from_svg(',self.text)
 def test_exact_frozen_svg(self):
  self.assertIn('d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368',self.text)
 def test_five_keyframes(self):
  self.assertIn('01_entry',self.text);self.assertIn('02_first_twist',self.text)
  self.assertIn('03_crossing',self.text);self.assertIn('04_depth_climax',self.text)
  self.assertIn('05_settled_study',self.text)
 def test_no_release(self):
  self.assertIn('"release_authorized":False',self.text)
  self.assertIn('"does_not_claim_exact_logo_equivalence":True',self.text)
 def test_supported_renderer(self):
  self.assertIn('sc.render.engine="BLENDER_EEVEE"',self.text)
 def test_thermal_hold(self):
  self.assertIn('thermal_gate()',self.text)
  self.assertIn('if t is not None and t>73:',self.text)
if __name__=="__main__":unittest.main()
