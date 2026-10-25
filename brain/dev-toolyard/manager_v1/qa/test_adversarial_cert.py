"""Adversarial QA for BHM Dev Yard Manager v1. Detection tests are NOT acceptance tests.
Run in Tool Yard sandbox_qa rootless offline Python worker with a copied immutable candidate.
Each DETECTED_UNSAFE state denotes a product blocker, even if unittest itself passes.
"""
import ast, hashlib, pathlib, sys, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import candidate as c
H="a"*64
def req(n=1):
    return {"requirement_id":f"MGR-R{n:02}","source_quote_or_pointer":"Exact owner wording from the frozen brief",
            "nonnegotiable":True,"measurable_acceptance":"Demonstrable actual behavior with evidence",
            "evidence_type":"Source-linked real artifact proof","validator":"Independent assessor identity"}
def declared_geometry():
    d={key:True for key in c.GEOMETRY}
    d.update({"reviewer_type":"independent_human","reviewer_id":"made_up_external_reviewer",
              "actual_frames_sha256":H,"geometry_trace_sha256":H})
    return d
class AdversarialGovernance(unittest.TestCase):
    def test_good_rejects_missing_critical_field(self):
        x=req();x.pop("measurable_acceptance")
        with self.assertRaises(c.GovernanceError):c.scope([x],H)
    def test_good_rejects_no_folds_even_if_codec_valid(self):
        x={"duration_ok":True,"codec_ok":True,"colors_ok":True,"folds":False}
        self.assertEqual(c.review_fold_evidence(x)["status"],"independent_qa_failed")
    def test_good_release_is_blocked_in_plan(self):
        x=c.plan(c.scope([req()],H),"matrix_dev_manager","manager_bmad_langgraph_speckit_v1")
        self.assertFalse(x["release_authorized"]);self.assertFalse(x["dispatch_authorized"])
    def test_detect_critical_omission_false_full_coverage(self):
        x=c.scope([req(1)],H)
        self.assertEqual(x["critical_coverage"],1.0)
        self.assertEqual(len(x["requirements"]),1)
        print("DETECTED_UNSAFE MGR-R02: 1/12 criteria still reports 100% coverage",flush=True)
    def test_detect_source_fingerprint_not_matched_to_brief(self):
        x=c.scope([req()],H)
        self.assertEqual(x["source_sha256"],H)
        print("DETECTED_UNSAFE MGR-R01: arbitrary 64-character digest accepted without reading source",flush=True)
    def test_detect_fake_geometry_review_accepted(self):
        result=c.review_fold_evidence(declared_geometry())
        self.assertEqual(result["status"],"owner_review_pending")
        print("DETECTED_UNSAFE MGR-R08: fabricated flags and fake frame hashes advance to review",flush=True)
    def test_detect_reviewer_identity_can_be_claimed(self):
        x=declared_geometry()
        self.assertEqual(c.review_fold_evidence(x,developer="developer")["status"],"owner_review_pending")
        print("DETECTED_UNSAFE MGR-R07: unverified reviewer identifier accepted as independent",flush=True)
    def test_detect_missing_capability_fit(self):
        p=c.plan(c.scope([req()],H),"matrix_dev_manager","manager_bmad_langgraph_speckit_v1")
        self.assertNotIn("method",p)
        self.assertNotIn("runtime_versions",p)
        self.assertNotIn("capability_smoke_receipt",p)
        print("DETECTED_UNSAFE MGR-R03: no algorithm/method-capability enforcement in plan",flush=True)
    def test_detect_spec_kit_not_actually_executed(self):
        spec=c.spec_payload(c.scope([req()],H))
        self.assertEqual(spec["state"],"draft_pending_review")
        self.assertNotIn("spec_kit_receipt",spec)
        print("DETECTED_UNSAFE MGR-R05: plain text spec payload is not Spec Kit execution receipt",flush=True)
    def test_detect_no_durable_checkpoint(self):
        source=pathlib.Path(c.__file__).read_text()
        tree=ast.parse(source)
        fn=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=="manager_graph")
        has_checkpoint=any(n for n in ast.walk(fn) if isinstance(n,ast.Name) and "checkpointer" in n.id.lower())
        self.assertFalse(has_checkpoint)
        print("DETECTED_UNSAFE MGR-R04: graph compiles without persistent checkpointer",flush=True)
    def test_detect_no_toolyard_controller_handoff(self):
        source=pathlib.Path(c.__file__).read_text()
        self.assertNotIn("intake_check(",source)
        self.assertNotIn("controller.submit(",source)
        print("DETECTED_UNSAFE MGR-R06: no verified dispatch handoff to approved controller",flush=True)
    def test_detect_role_workflow_only_labels(self):
        roles=c.bmad_roles(c.scope([req()],H))
        self.assertIn("architect",roles["roles"])
        self.assertNotIn("execution_receipt",roles)
        print("DETECTED_UNSAFE MGR-R03: BMad role labels are not actual agent invocation",flush=True)
if __name__=="__main__":unittest.main(verbosity=2)
