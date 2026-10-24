"""Fail-closed QA regression for project-independent quality governor."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from quality_gate import annotate,evaluate,PROFILES

PROJECT="example_project"
MANIFEST="site_v1"

class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.base=self.root/"quality-inbox"/PROJECT/MANIFEST
        self.base.mkdir(parents=True,mode=0o700)
    def tearDown(self):
        self.tmp.cleanup()
    def write(self,name,data):
        dest=self.base/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(data),encoding="utf-8")
        dest.chmod(0o600)
    def contract(self):
        kinds=sorted(PROFILES["creative_web"])
        criteria=[{"id":"check_"+k,"kind":k,
                   "acceptance":"Owner baseline matched and verifiable with independent evidence",
                   "required":True} for k in kinds]
        data={"schema_version":1,"project":PROJECT,"manifest":MANIFEST,
              "profile":"creative_web","brief_sha256":"a"*64,"criteria":criteria}
        self.write("quality-contract.json",data)
        return data
    def evidence(self,c,reviewer="independent_human"):
        rs=[]
        for n,item in enumerate(c["criteria"]):
            rel="proof%d.txt"%n
            p=self.base/"artifacts"/rel;p.parent.mkdir(exist_ok=True)
            p.write_text("test artifact %d"%n);p.chmod(0o600)
            rs.append({"id":item["id"],"status":"passed",
                       "artifact":rel,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
                       "reviewer_type":reviewer if item["kind"]=="independent_review" else "automated"})
        self.write("evidence.json",{"schema_version":1,"brief_sha256":"a"*64,"results":rs})
    def test_absent_contract_prevents_creative_claim(self):
        g=annotate(PROJECT,MANIFEST,{"qa_passed":True},self.root)
        self.assertEqual(g["quality_gate"]["status"],"requirements_missing")
        self.assertFalse(g["design_complete"])
        self.assertFalse(g["release_approved"])
    def test_missing_evidence_rejected(self):
        self.contract()
        self.assertEqual(evaluate(PROJECT,MANIFEST,self.root)["status"],"evidence_missing")
    def test_incomplete_acceptance_rejected(self):
        c=self.contract();c["criteria"]=c["criteria"][:-1]
        self.write("quality-contract.json",c)
        self.assertEqual(evaluate(PROJECT,MANIFEST,self.root)["status"],"requirements_incomplete")
    def test_all_artifacts_are_not_owner_approval(self):
        c=self.contract();self.evidence(c)
        g=evaluate(PROJECT,MANIFEST,self.root)
        self.assertEqual(g["status"],"evidence_ready_for_owner_review")
        self.assertFalse(g["owner_approved"])
        self.assertFalse(g["release_authorized"])
    def test_ai_cannot_self_sign_independent_review(self):
        c=self.contract();self.evidence(c,reviewer="external_model")
        self.assertEqual(evaluate(PROJECT,MANIFEST,self.root)["status"],"independent_review_missing")
    def test_evidence_tampering_fails_closed(self):
        c=self.contract();self.evidence(c)
        p=self.base/"artifacts/proof0.txt";p.write_text("tampered")
        self.assertEqual(evaluate(PROJECT,MANIFEST,self.root)["status"],"quality_contract_rejected")
    def test_wrong_project_must_not_consume_foreign_evidence(self):
        c=self.contract();self.evidence(c)
        self.assertEqual(evaluate("foreign_project",MANIFEST,self.root)["status"],"requirements_missing")
    def test_deceptive_owner_signoff_rejected(self):
        c=self.contract()
        c["approved"]=True
        self.write("quality-contract.json",c)
        self.assertEqual(evaluate(PROJECT,MANIFEST,self.root)["status"],"quality_contract_rejected")

if __name__=="__main__":
    unittest.main(verbosity=2)
