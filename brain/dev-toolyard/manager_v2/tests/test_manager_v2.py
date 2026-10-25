import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,"backend")
from requirements_guard import ScopeDenied,load_frozen,build_rtm_from_frozen,verify_rtm,sha
from method_guard import MethodDenied,inspect_fold_candidate,verify_method_receipt
class GovernanceV2Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.p=Path(self.tmp.name)
  self.brief="\n".join(f"| MGR-R{i:02d} | Owner's exact critical requirement number {i} |" for i in range(1,13))
  self.contract={"schema_version":1,"project":"matrix_dev_manager","manifest":"manager_quality_governance_v2",
   "profile":"automation","brief_sha256":sha(self.brief.encode()),"criteria":[
    {"id":f"mgr_r{i:02d}","acceptance":f"Critical proof must be observed and pinned for {i}",
     "kind":"brief_trace","required":True} for i in range(1,13)]}
  (self.p/"brief.md").write_text(self.brief)
  (self.p/"quality-contract.json").write_text(json.dumps(self.contract))
  self.contract_sha=sha((self.p/"quality-contract.json").read_bytes())
 def tearDown(self):self.tmp.cleanup()
 def test_exact_twelve_succeeds(self):
  r=build_rtm_from_frozen(self.p)
  self.assertEqual(verify_rtm(self.p,r,self.contract_sha)["coverage"],12)
 def test_missing_critical_requirement_denied(self):
  r=build_rtm_from_frozen(self.p)[:-1]
  with self.assertRaises(ScopeDenied):verify_rtm(self.p,r,self.contract_sha)
 def test_unexpected_requirement_denied(self):
  r=build_rtm_from_frozen(self.p);r[1]["requirement_id"]="mgr_r13"
  with self.assertRaises(ScopeDenied):verify_rtm(self.p,r,self.contract_sha)
 def test_duplicate_denied(self):
  r=build_rtm_from_frozen(self.p);r[1]["requirement_id"]="mgr_r01"
  with self.assertRaises(ScopeDenied):verify_rtm(self.p,r,self.contract_sha)
 def test_fake_quote_denied(self):
  r=build_rtm_from_frozen(self.p);r[0]["source_quote"]="my fabricated approval evidence"
  with self.assertRaises(ScopeDenied):verify_rtm(self.p,r,self.contract_sha)
 def test_mutated_critical_acceptance_denied(self):
  r=build_rtm_from_frozen(self.p);r[0]["measurable_acceptance"]="Skip this requirement instead"
  with self.assertRaises(ScopeDenied):verify_rtm(self.p,r,self.contract_sha)
 def test_contract_hash_change_denied(self):
  r=build_rtm_from_frozen(self.p)
  with self.assertRaises(ScopeDenied):verify_rtm(self.p,r,"a"*64)
 def test_brief_drift_denied(self):
  (self.p/"brief.md").write_text(self.brief+"\nchanged")
  with self.assertRaises(ScopeDenied):load_frozen(self.p)
 def test_known_bad_alpha_mask_rejected_with_real_files(self):
  src=self.p/"render.py";video=self.p/"render.mp4"
  src.write_text("alpha_from_svg(100)\na*reveal\nreveal=smooth(42)\nGaussianBlur")
  video.write_bytes(b"media fixture")
  result=inspect_fold_candidate(src,video)
  self.assertEqual(result["status"],"negative_fixture_rejected")
  self.assertFalse(result["geometry_verified"])
 def test_unrecognized_geometry_cannot_autopass(self):
  src=self.p/"render.py";video=self.p/"render.mp4"
  src.write_text("mesh vertex and color");video.write_bytes(b"media")
  self.assertEqual(inspect_fold_candidate(src,video)["status"],"requires_independent_geometry_review")
 def test_method_forged_sha_denied(self):
  file=self.p/"renderer.py";file.write_bytes(b"true")
  good={"method_id":"m1","tool":"bmad","version":"bmad-method@6.12.4",
        "source_sha256":"a"*64,"execution_receipt_sha256":"b"*64,
        "verified_artifact_path":"render.mp4","verified_artifact_sha256":"c"*64,"stage":"private_dev"}
  with self.assertRaises(MethodDenied):verify_method_receipt(good,self.p,file)
 def test_supervisor_source_no_auto_publish(self):
  text=Path("backend/supervisor_v2.py").read_text()
  self.assertIn("interrupt_before=[\"handoff\"]",text)
  self.assertIn("release_authorized",Path("backend/requirements_guard.py").read_text())
  self.assertNotIn("shell=True",text)
if __name__=="__main__":unittest.main()
