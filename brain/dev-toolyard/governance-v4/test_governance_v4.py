#!/usr/bin/env python3
"""Synthetic, adversarial v4 Yard regression. stdlib unittest only."""
from __future__ import annotations
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/(name+".py"))
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
gate=module("requirements_gate")
guard=module("adapter_guard")
repair=module("bounded_repair")
def digest(data):return hashlib.sha256(data).hexdigest()

class Fixture(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)
        (self.root/"artifacts").mkdir()
        brief=b"Mandatory: implement visible 3D folding ribbon geometry and independent visual evidence."
        (self.root/"brief.md").write_bytes(brief)
        def evidence(name,data):
            (self.root/"artifacts"/name).write_bytes(data)
            return digest(data)
        probe=evidence("probe.txt",b"Blender geometry renderer version, offline capability probe pass")
        proof=evidence("method.txt",b"Geometry with folding 3D planes, normals, backfaces and occlusion")
        receipt=evidence("receipt.txt",b"Terminal isolated test receipt id: synthetic-check-001 exit=0")
        built=evidence("result.glb",b"non-empty synthetic placeholder artifact")
        test=evidence("test.txt",b"Unit QA: geometry folding test pass (synthetic fixture)")
        independent=evidence("visual.png",b"PNG synthetic visual evidence placeholder")
        reviewer=evidence("review.txt",b"QA reviewer independent from executor, verified the test fixture")
        self.item={
         "schema_version":1,"project":"yard_test_project","task_id":"folding_fixture",
         "source":{"path":"brief.md","sha256":digest(brief)},
         "requirements":[{"id":"fold_geometry","source_quote":"visible 3D folding ribbon geometry","acceptance":"Rendered geometry has measured folds and occluded backfaces", "nonnegotiable":True,
                          "capability_id":"blender_render","forbidden_substitutes":["2D mask","flat SVG"],"evidence_type":"visual"}],
         "capabilities":[{"id":"blender_render","version":"4.3.0","license":"GPL-3.0-or-later",
                          "probe":True,"probe_artifact":"probe.txt","probe_sha256":probe,"approved_operations":["render_geometry"]}],
         "methods":[{"requirement_id":"fold_geometry","capability_id":"blender_render","operation":"render_geometry",
                      "implementation_method":"Geometry normals, actual folding planes and occlusion",
                      "method_proof":"method.txt","method_proof_sha256":proof}],
         "execution":{"state":"completed","exit_code":0,"source_sha256":digest(b"sample source"),
                      "artifacts":[{"path":"result.glb","sha256":built}],"worker_id":"developer_identity",
                      "tests":[{"requirement_id":"fold_geometry","status":"passed","evidence_path":"test.txt","sha256":test}],
                      "receipt_artifact":"receipt.txt","receipt_sha256":receipt},
         "independent_qa":{"reviewer_id":"reviewer_identity","producer_id":"developer_identity",
                    "results":[{"requirement_id":"fold_geometry","status":"passed","observed_artifact":"visual.png","sha256":independent}],
                    "review_receipt":"review.txt","review_sha256":reviewer}
        }
    def result(self):
        return gate.evaluate(self.root,self.item)
    def test_positive_reaches_owner_not_release(self):
        r=self.result()
        self.assertEqual(r["status"],"ready_for_owner_review")
        self.assertTrue(r["independent_qa_verified"])
        self.assertFalse(r["owner_accepted"])
        self.assertFalse(r["release_authorized"])
    def test_missing_requirement(self):
        self.item["requirements"]=[]
        self.assertEqual(self.result()["stage"],"intake")
    def test_weak_critical_requirement(self):
        self.item["requirements"][0]["nonnegotiable"]=False
        self.assertIn("weakened",self.result()["blockers"][0])
    def test_drift_brief_rejected(self):
        (self.root/"brief.md").write_text("Wrong brief")
        self.assertEqual(self.result()["blockers"],["brief_source_hash_drift"])
    def test_unauthorized_2d_shortcut_denied(self):
        self.item["methods"][0]["implementation_method"]="Use 2D mask overlay as folding substitute"
        self.assertIn("forbidden",self.result()["blockers"][0])
    def test_installed_tool_with_no_probe_denied(self):
        self.item["capabilities"][0]["probe"]=False
        self.assertFalse(self.result()["method_fit_verified"])
    def test_wrong_tool_for_requirement(self):
        self.item["methods"][0]["capability_id"]="other_tool"
        self.assertEqual(self.result()["blockers"],["wrong_capability_for_requirement"])
    def test_disallowed_operation(self):
        self.item["methods"][0]["operation"]="unrestricted_shell"
        self.assertEqual(self.result()["blockers"],["unapproved_tool_operation"])
    def test_no_terminal_receipt(self):
        self.item["execution"]["state"]="queued"
        self.assertEqual(self.result()["blockers"],["execution_not_terminal_success"])
    def test_proposal_only_not_execution(self):
        self.item["execution"]={}
        self.assertEqual(self.result()["blockers"],["terminal_execution_receipt_required"])
    def test_no_real_tests(self):
        self.item["execution"]["tests"]=[]
        self.assertEqual(self.result()["blockers"],["real_artifacts_and_tests_required"])
    def test_hashed_artifact_tampering(self):
        (self.root/"artifacts"/"result.glb").write_bytes(b"tamper")
        self.assertEqual(self.result()["blockers"],["source_artifact_drift"])
    def test_independent_role_rejected_same_actor(self):
        self.item["independent_qa"]["reviewer_id"]="developer_identity"
        self.assertEqual(self.result()["blockers"],["self_review_rejected"])
    def test_wrong_producer(self):
        self.item["independent_qa"]["producer_id"]="different"
        self.assertEqual(self.result()["blockers"],["producer_identity_mismatch"])
    def test_visual_qa_rejected(self):
        self.item["independent_qa"]["results"][0]["status"]="failed"
        self.assertEqual(self.result()["blockers"],["independent_semantic_qa_failed"])
    def test_artifact_traversal_denied(self):
        self.item["execution"]["artifacts"][0]["path"]="../bad"
        self.assertEqual(self.result()["blockers"],["receipt_or_artifact_missing"])
    def test_artifact_symlink_denied(self):
        a=self.root/"artifacts"/"result.glb"
        a.unlink();a.symlink_to(self.root/"brief.md")
        self.assertEqual(self.result()["blockers"],["receipt_or_artifact_missing"])
    def test_no_writable_record(self):
        path=self.root/"item.json"
        path.write_text(json.dumps(self.item));path.chmod(0o666)
        with self.assertRaisesRegex(gate.GateDenied,"mutable_record"): gate.load(path)

class Registry(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.p=Path(self.tmp.name)/"registry.json"
    def write(self, tools):
        data={"schema":1,"tools":tools}
        self.p.write_text(json.dumps(data,sort_keys=True,indent=2))
        self.p.chmod(0o600)
    def test_registry_over_80k_now_reads(self):
        items={"yard-synthetic-"+str(i):{"state":"accepted_qa_probe_only","operations":["syntax_probe"],
                  "inventory":"direct_script_unreviewed","owner_approved":False,
                  "production_live":False,"filler":"x"*820} for i in range(100)}
        self.write(items)
        self.assertGreater(self.p.stat().st_size,80000)
        self.assertEqual(len(guard.checked_registry(self.p)),100)
    def test_reject_oversize(self):
        self.p.write_bytes(b"x"*(guard.MAX_REGISTRY_BYTES+1))
        with self.assertRaisesRegex(guard.AdapterRegistryDenied,"registry_invalid"):guard.checked_registry(self.p)
    def test_symlink_denied(self):
        other=Path(self.tmp.name)/"source.json";other.write_text("{}")
        self.p.symlink_to(other)
        with self.assertRaises(guard.AdapterRegistryDenied):guard.checked_registry(self.p)
    def test_writable_denied(self):
        self.write({});self.p.chmod(0o666)
        with self.assertRaisesRegex(guard.AdapterRegistryDenied,"mutable"):guard.checked_registry(self.p)
    def test_unknown_shell_operation_denied(self):
        self.write({"python3":{"operations":["arbitrary_shell"],"production_live":False}})
        with self.assertRaisesRegex(guard.AdapterRegistryDenied,"untrusted_operations"):guard.checked_registry(self.p)
    def test_no_privilege_bypass(self):
        self.write({"python3":{"operations":[],"production_live":True}})
        with self.assertRaisesRegex(guard.AdapterRegistryDenied,"privilege_escalation"):guard.checked_registry(self.p)

class BoundedRepair(unittest.TestCase):
    def setUp(self):
        self.entry={"schema_version":1,"project":"test_project","manifest":"test_manifest","task_id":"test_task",
          "task_status":"tests_failed","attempts":0,"source_sha256":"e"*64,
          "failure_code":"python_asyncio_taskgroup_cancel",
          "independent_failure_receipt":True,"owner_intake_signed":True}
    def test_known_recipe_candidate_only(self):
        r=repair.decide(self.entry)
        self.assertEqual(r["status"],"approved_recipe_candidate")
        self.assertFalse(r["executable"])
        self.assertFalse(r["auto_publish"])
    def test_unknown_failure_no_guess(self):
        self.entry["failure_code"]="unknown_problem"
        self.assertIn("unrecognized",repair.decide(self.entry)["reason"])
    def test_expired_no_replay(self):
        self.entry["task_status"]="outcome_unknown"
        self.assertIn("uncertain",repair.decide(self.entry)["reason"])
    def test_max_two_attempts(self):
        self.entry["attempts"]=2
        self.assertEqual(repair.decide(self.entry)["reason"],"bounded_retry_limit_reached")
    def test_owner_gate(self):
        self.entry["owner_intake_signed"]=False
        self.assertIn("owner_scoped",repair.decide(self.entry)["reason"])
    def test_design_change_gate(self):
        self.entry["failure_code"]="ui_design_fidelity"
        self.assertEqual(repair.decide(self.entry)["reason"],"owner_design_change_required")

if __name__=="__main__":unittest.main(verbosity=2)
