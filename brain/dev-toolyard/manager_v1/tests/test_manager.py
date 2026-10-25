import sys,unittest
sys.path.insert(0,"backend")
from manager import GovernanceError,scope,plan,spec_payload,bmad_roles,review_fold_evidence
H="a"*64
def req():
 return {"requirement_id":"MGR-R01","source_quote_or_pointer":"Verbatim owner brief must be retained",
         "nonnegotiable":True,"measurable_acceptance":"Original owner acceptance is verifiable",
         "evidence_type":"real artifact reference","validator":"independent reviewer"}
class GateTests(unittest.TestCase):
 def test_critical_traceability(self):
  x=scope([req()],H)
  self.assertEqual(x["critical_coverage"],1)
  self.assertFalse(plan(x,"matrix_dev_manager","manager_bmad_langgraph_speckit_v1")["dispatch_authorized"])
  self.assertIn("MGR-R01",spec_payload(x)["spec"])
  self.assertFalse(bmad_roles(x)["agents_may_self_approve"])
 def test_missing_must_have_denied(self):
  r=req();r.pop("measurable_acceptance")
  with self.assertRaises(GovernanceError):scope([r],H)
 def test_silent_substitution_denied(self):
  r=req();r["nonnegotiable"]=False
  with self.assertRaises(GovernanceError):scope([r],H)
 def test_duplicate_denied(self):
  with self.assertRaises(GovernanceError):scope([req(),req()],H)
 def test_cross_project_scope_denied(self):
  with self.assertRaises(GovernanceError):plan(scope([req()],H),"../other","task_v1")
 def test_rejected_delulu_mask_fails(self):
  result=review_fold_evidence({"duration_ok":True,"colors_ok":True,"codec_ok":True,"folds":False})
  self.assertEqual(result["status"],"independent_qa_failed")
  self.assertIn("folds",result["missing"])
 def test_self_signed_reviewer_fails(self):
  x={k:True for k in ("folds","backfaces","self_occlusion","shading","parallax","geometry_normals")}
  x.update({"reviewer_type":"independent_human","reviewer_id":"developer","actual_frames_sha256":H,"geometry_trace_sha256":H})
  self.assertEqual(review_fold_evidence(x)["status"],"independent_qa_failed")
 def test_good_geometry_only_owner_review(self):
  x={k:True for k in ("folds","backfaces","self_occlusion","shading","parallax","geometry_normals")}
  x.update({"reviewer_type":"independent_human","reviewer_id":"external_qa","actual_frames_sha256":H,"geometry_trace_sha256":H})
  self.assertEqual(review_fold_evidence(x)["status"],"owner_review_pending")
  self.assertFalse(review_fold_evidence(x)["release_authorized"])
if __name__=="__main__":unittest.main()
