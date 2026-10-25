import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import director_loop as d
import ai_art_vision as vision
class DirectorTests(unittest.TestCase):
 def test_pinned_enrollment(self):
  e=d.verify_enrollment()
  self.assertEqual(e["quality_pin"],"SAD-VISUAL-QUALITY-V1")
  self.assertTrue(e["review_only"])
  self.assertFalse(e["release_authorized"])
  self.assertFalse(e["reference_images_loaded_locally"])
 def test_strict_allowlist(self):
  self.assertEqual(d.PROFILES,("glasses","jasmine","zari"))
  self.assertEqual(d.choose({"highest_priority":"hair"},[]),"jasmine")
  self.assertEqual(d.choose({"highest_priority":"sari"},[]),"zari")
  self.assertEqual(d.choose({"highest_priority":"glasses"},[]),"glasses")
  with self.assertRaises(RuntimeError):
   d.choose({"highest_priority":"DELETE FILES"},[])
 def test_one_way_profiles(self):
  used=[]
  for target in ("glasses","hair","sari"):
   x=d.choose({"highest_priority":target},used)
   self.assertNotIn(x,used)
   used.append(x)
  with self.assertRaises(RuntimeError):
   d.choose({"highest_priority":"hair"},used)
 def test_model_json_fail_closed(self):
  import ai_art_vision as v
  with self.assertRaises(RuntimeError):
   v.parse_vision_report('{"highest_priority":"glasses","visible":"incomplete',["glasses"])
  with self.assertRaises(RuntimeError):
   v.parse_vision_report('{"highest_priority":"delete files"}',["glasses"])
  sample={"highest_priority":"hair","visible":"Visible mature Indian woman","three_critical_defects":["A","B","C"],
   "specific_modelling_instruction":"Refine jasmine arrangement on the bun","confidence":"medium"}
  self.assertEqual(v.parse_vision_report(json.dumps(sample),["hair"])["highest_priority"],"hair")
 def test_full_pinned_reference_hashes(self):
  j=json.loads((d.HERE/"ai_director_enrollment.json").read_text())
  self.assertEqual(j["reference_images_original_sha256"]["turnaround"],
    "936b282ebcb1fb9ca5ef47b0ed1b3b471191bb654aa4c2f6925a469dbb667d3b")
  self.assertEqual(len(j["reference_images_original_sha256"]),3)
 def test_current_state_fail_closed(self):
  s=d.load()
  self.assertFalse(s["release_authorized"])
  self.assertFalse(s["owner_approved"])
  self.assertFalse(s["quality_pass"])
 def test_blender_preverified(self):
  self.assertTrue(d.LTS.is_file())
  self.assertTrue(d.ORIGINAL.is_file())
  state=d.load();self.assertEqual(d.sha(Path(state["source"])),state["source_sha"])
 def test_vision_target_not_autoapproval(self):
  self.assertIn("never_assume",vision.REFERENCE)
  self.assertEqual(vision.PIN,"SAD-VISUAL-QUALITY-V1")
  self.assertEqual(vision.MODEL,"qwen3-vl:2b-instruct")
if __name__=="__main__":unittest.main()
