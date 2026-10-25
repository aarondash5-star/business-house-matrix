"""Delulu real-task certification, rootless independent QA; detected blockers are expected test observations."""
import hashlib,pathlib,re,tempfile,unittest,json
from method_guard import inspect_fold_candidate
from requirements_guard import verify_rtm,ScopeDenied
SRC=pathlib.Path(__file__).resolve().parent
class DeluluChallenge(unittest.TestCase):
 def test_renderer_is_exact_known_bad_source(self):
  s=(SRC/"render_motion.py").read_bytes()
  self.assertEqual(hashlib.sha256(s).hexdigest(),"924f4e29ebc6fbe8f19a3acaf16558c4e3f046181d3d67042b9b73e261c6ab00")
 def test_real_renderer_is_mask_not_geometry(self):
  s=(SRC/"render_motion.py").read_text()
  for token in ("alpha_from_svg(","reveal=smooth(","GaussianBlur", "a*reveal"):self.assertIn(token,s)
  for token in ("bpy.data.meshes.new","mesh.vertices", "bpy.ops.object.modifier_add"):self.assertNotIn(token,s)
  self.assertIn("fold=np.exp",s)
  print("CONFIRMED_NEGATIVE: renderer Gaussian fold label is a 2D color effect",flush=True)
 def test_known_bad_method_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   f=pathlib.Path(td)/"sample.mp4";f.write_bytes(b"test only; real MP4 hash externally verified")
   v=inspect_fold_candidate(SRC/"render_motion.py",f)
   self.assertEqual(v["status"],"negative_fixture_rejected")
   self.assertFalse(v["geometry_verified"])
 def test_unrelated_geometry_never_autoapproved(self):
  with tempfile.TemporaryDirectory() as td:
   f=pathlib.Path(td)/"renderer.py";f.write_text("vertex mesh")
   m=pathlib.Path(td)/"frame.mp4";m.write_bytes(b"synthetic")
   x=inspect_fold_candidate(f,m)
   self.assertEqual(x["status"],"requires_independent_geometry_review")
   self.assertFalse(x["geometry_verified"])
 def test_foreign_project_handoff_denied(self):
  s=(SRC/"supervisor_v2.py").read_text()
  self.assertIn('if project!=PROJECT:raise StageError("foreign_project_denied")',s)
  self.assertIn('"submitted":False',s)
 def test_missing_early_cross_project_scope_is_blocker(self):
  s=(SRC/"supervisor_v2.py").read_text()
  block=s.split("def scope_stage(state):",1)[1].split("def method_stage(state):",1)[0]
  self.assertNotIn('state["project"]',block)
  self.assertIn('build_rtm_from_frozen(state["base"])',block)
  print("CERTIFICATION_BLOCKER: scope node does not bind Delulu project to original brief",flush=True)
 def test_no_operational_bmad_role_execution(self):
  s=(SRC/"supervisor_v2.py").read_text().lower()
  self.assertNotIn("bmad-agent-",s)
  print("CERTIFICATION_BLOCKER: BMad role invocation not present",flush=True)
 def test_no_operational_spec_kit_flow(self):
  s=(SRC/"supervisor_v2.py").read_text().lower()
  self.assertNotIn("specify ",s)
  print("CERTIFICATION_BLOCKER: Spec Kit plan/task execution not present",flush=True)
 def test_independent_reviewer_must_be_external(self):
  s=(SRC/"evidence_guard.py").read_text()
  self.assertIn('TRUST_FILE=Path("/etc/business-house-matrix/independent-qa-trust-v1.json")',s)
  self.assertIn("p.stat().st_uid!=0",s)
  self.assertIn("key.verify(",s)
 def test_critical_coverage_is_exact_contract_bound(self):
  s=(SRC/"requirements_guard.py").read_text()
  self.assertIn('len(records)!=12',s)
  self.assertIn("critical_requirement_mutated",s)
 def test_no_trusted_positive_delulu_fixture(self):
  s=(SRC/"method_guard.py").read_text()
  self.assertIn('"requires_independent_geometry_review"',s)
  self.assertIn('"geometry_verified":False',s)
  print("CERTIFICATION_BLOCKER: no positive proof accepted without actual independent geometry review",flush=True)
if __name__=="__main__":unittest.main()
