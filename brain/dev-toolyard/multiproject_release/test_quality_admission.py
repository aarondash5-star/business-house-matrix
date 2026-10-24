"""Prove mandatory Tool Yard quality admission and release fail closed."""
import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from quality_admission import AdmissionDenied,intake_check,release_check
from quality_gate import PROFILES,evaluate

P="sample_project";M="sample_v1"
class EnforcementTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.base=self.root/"quality-inbox"/P/M
        self.base.mkdir(parents=True)
        self.write(self.root/"owner-intake-approvals-v1.json",{"schema_version":1,"approvals":[]})
        self.write(self.root/"owner-release-approvals-v1.json",{"schema_version":1,"approvals":[]})
    def tearDown(self):self.tmp.cleanup()
    def write(self,path,obj):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(obj),encoding="utf-8")
        path.chmod(0o600)
    def make_contract(self):
        brief="Owner-approved exact requirements and scope, revision 1. All criteria mandatory.\n"
        p=self.base/"brief.md";p.write_text(brief);p.chmod(0o600)
        brief_sha=hashlib.sha256(p.read_bytes()).hexdigest()
        criteria=[{"id":"check_"+v,"kind":v,"required":True,"acceptance":"A real owner-approved measurable visual or functional acceptance criterion"} for v in sorted(PROFILES["creative_web"])]
        c={"schema_version":1,"project":P,"manifest":M,"profile":"creative_web","brief_sha256":brief_sha,"criteria":criteria}
        self.write(self.base/"quality-contract.json",c)
        return c,hashlib.sha256((self.base/"quality-contract.json").read_bytes()).hexdigest()
    def intake_approval(self,c,sha):
        return {"project":P,"manifest":M,"profile":"creative_web","brief_sha256":c["brief_sha256"],"contract_sha256":sha,
                "approval_ref":"https://github.com/owner/private/issues/123","approved_by":"owner"}
    def admit(self):
        c,sha=self.make_contract()
        self.write(self.root/"owner-intake-approvals-v1.json",{"schema_version":1,"approvals":[self.intake_approval(c,sha)]})
        return c,sha
    def make_evidence(self,c):
        results=[]
        for i,item in enumerate(c["criteria"]):
            file=self.base/"artifacts"/("frame-"+str(i)+".txt")
            file.parent.mkdir(parents=True,exist_ok=True)
            file.write_text("Independent real review evidence "+str(i));file.chmod(0o600)
            results.append({"id":item["id"],"status":"passed","artifact":file.name,
                            "sha256":hashlib.sha256(file.read_bytes()).hexdigest(),
                            "reviewer_type":"independent_human"})
        self.write(self.base/"evidence.json",{"schema_version":1,"brief_sha256":c["brief_sha256"],"results":results})
    def test_denies_missing_contract(self):
        with self.assertRaises(AdmissionDenied):intake_check(P,"website_stage",M,self.root)
    def test_denies_unapproved_contract(self):
        self.make_contract()
        with self.assertRaisesRegex(AdmissionDenied,"owner_intake_approval_missing"):intake_check(P,"website_stage",M,self.root)
    def test_owner_pinned_contract_admitted_but_not_released(self):
        self.admit()
        result=intake_check(P,"dev_project_build",M,self.root)
        self.assertEqual(result["status"],"approved_intake")
        self.assertFalse(result["release_authorized"])
    def test_tampered_brief_denied(self):
        self.admit()
        (self.base/"brief.md").write_text("CHANGED WITHOUT OWNER APPROVAL")
        with self.assertRaises(AdmissionDenied):intake_check(P,"website_stage",M,self.root)
    def test_tampered_contract_denied(self):
        c,_=self.admit();c["criteria"][0]["acceptance"]="Very different requirement"
        self.write(self.base/"quality-contract.json",c)
        with self.assertRaises(AdmissionDenied):intake_check(P,"website_stage",M,self.root)
    def test_other_project_not_admitted(self):
        self.admit()
        with self.assertRaises(AdmissionDenied):intake_check("wrong_project","website_stage",M,self.root)
    def test_no_release_without_evidence(self):
        self.admit()
        with self.assertRaisesRegex(AdmissionDenied,"independent_quality_evidence"):release_check(P,M,"vercel","preview","b"*64,self.root)
    def test_no_release_without_distinct_owner_approval(self):
        c,_=self.admit();self.make_evidence(c)
        self.assertEqual(evaluate(P,M,self.root)["status"],"evidence_ready_for_owner_review")
        with self.assertRaisesRegex(AdmissionDenied,"explicit_owner_release_approval_missing"):release_check(P,M,"vercel","preview","b"*64,self.root)
    def test_release_protected_by_exact_artifact_and_target(self):
        from datetime import datetime,timedelta,timezone
        c,sha=self.admit();self.make_evidence(c)
        record={"project":P,"manifest":M,"contract_sha256":sha,
                "evidence_sha256":hashlib.sha256((self.base/"evidence.json").read_bytes()).hexdigest(),
                "artifact_sha256":"b"*64,"platform":"vercel","environment":"preview",
                "expires_utc":(datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),
                "approval_ref":"https://github.com/owner/private/issues/456","approved_by":"owner"}
        self.write(self.root/"owner-release-approvals-v1.json",{"schema_version":1,"approvals":[record]})
        self.assertEqual(release_check(P,M,"vercel","preview","b"*64,self.root)["status"],"preflight_authorized")
        for platform,env,digest in [("cloudflare","preview","b"*64),("vercel","production","b"*64),("vercel","preview","a"*64)]:
            with self.assertRaises(AdmissionDenied):release_check(P,M,platform,env,digest,self.root)
        record["expires_utc"]="2020-01-01T00:00:00+00:00"
        self.write(self.root/"owner-release-approvals-v1.json",{"schema_version":1,"approvals":[record]})
        with self.assertRaisesRegex(AdmissionDenied,"expired"):release_check(P,M,"vercel","preview","b"*64,self.root)
    def test_read_only_exempt(self):
        self.assertFalse(intake_check(P,"research_search",M,self.root)["required"])
if __name__=="__main__":unittest.main(verbosity=2)
