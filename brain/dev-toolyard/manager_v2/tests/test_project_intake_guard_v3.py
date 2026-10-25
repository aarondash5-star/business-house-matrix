import sys,tempfile,json,hashlib,unittest
from pathlib import Path
sys.path.insert(0,"backend")
from project_intake_guard_v3 import ProjectScopeDenied,read_project_contract,require_actual_folds,propose_only
class ProjectRouterTests(unittest.TestCase):
 def fixture(self,updated):
  self.tmp=tempfile.TemporaryDirectory()
  r=Path(self.tmp.name);p=r/"quality-inbox/delulu_tech/delulu_fold_review_v1";p.mkdir(parents=True)
  phrases=("actual 3d mesh","front and back surfaces","self-occlusion","five review keyframes","frozen svg sha")
  brief="\n".join(phrases) + "\nno production publish\n"
  criteria=[{"id":f"x{i}","acceptance":x if updated else "generic reveal colors only"} for i,x in enumerate(phrases)]
  c={"project":"delulu_tech","manifest":"delulu_fold_review_v1","brief_sha256":hashlib.sha256(brief.encode()).hexdigest(),"criteria":criteria}
  (p/"brief.md").write_text(brief)
  (p/"quality-contract.json").write_text(json.dumps(c))
  self.addCleanup(self.tmp.cleanup)
  return r
 def test_full_project_approved_intent(self):
  item=read_project_contract("delulu_tech","delulu_fold_review_v1",root=self.fixture(True))
  res=require_actual_folds(item,"https://github.com/aarondash5-star/business-house-matrix/pull/27")
  self.assertEqual(res["status"],"project_scope_verified")
  self.assertFalse(res["release_authorized"])
 def test_outdated_v2_reveal_does_not_meet_geometry(self):
  item=read_project_contract("delulu_tech","delulu_fold_review_v1",root=self.fixture(False))
  with self.assertRaises(ProjectScopeDenied):require_actual_folds(item,"https://github.com/aarondash5-star/business-house-matrix/pull/27")
 def test_project_swap_denied(self):
  with self.assertRaises(ProjectScopeDenied):read_project_contract("matrix_dev_manager","delulu_fold_review_v1",root=self.fixture(True))
 def test_no_owner_change_ref_denied(self):
  item=read_project_contract("delulu_tech","delulu_fold_review_v1",root=self.fixture(True))
  with self.assertRaises(ProjectScopeDenied):require_actual_folds(item,"approval-by-model")
 def test_stale_contract_sha_denied(self):
  root=self.fixture(True)
  p=root/"quality-inbox/delulu_tech/delulu_fold_review_v1/brief.md"
  p.write_text("changed material")
  with self.assertRaises(ProjectScopeDenied):read_project_contract("delulu_tech","delulu_fold_review_v1",root=root)
 def test_has_no_auto_release(self):
  item=read_project_contract("delulu_tech","delulu_fold_review_v1",root=self.fixture(True))
  self.assertIs(propose_only(item)["auto_release"],False)
if __name__=="__main__":unittest.main()
