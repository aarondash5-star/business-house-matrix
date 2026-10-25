import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, '/var/lib/generic-linux-automator-exec/matrix-controller')
import controller
import toolyard_qa_standard_v1 as qa

class UniversalToolyardQATests(unittest.TestCase):
    def test_every_controller_tool_mapped(self):
        c=qa.verify_coverage(controller.ALLOWED)
        self.assertTrue(c["complete"],c)
        self.assertEqual(c["mapped_actions"],13)
    def test_all_tool_receipts_are_conservative(self):
        for name in controller.ALLOWED:
            with self.subTest(action=name):
                result=qa.receipt("delulu_tech",name,"test_manifest",{"published":False,"qa_passed":True})
                self.assertFalse(result["universal_quality_standard"]["production_release_authorized"])
                self.assertFalse(result["universal_quality_standard"]["independent_human_accepted"])
                self.assertTrue(result["universal_quality_standard"]["mandatory_checks"])
    def test_unknown_action_denied(self):
        with self.assertRaisesRegex(qa.QualityStandardError,"unknown"):
            qa.receipt("delulu_tech","external_unmediated_tool","test",{})
    def test_fake_approval_denied(self):
        for forged in ({"published":True},{"release_authorized":True},{"design_complete":True}):
            with self.subTest(forged=forged):
                with self.assertRaisesRegex(qa.QualityStandardError,"claim_denied"):
                    qa.receipt("delulu_tech","website_stage","v2",forged)
    def test_frozen_result_copy(self):
        output={"checks":2,"quality_gate":{"status":"evidence_missing"}}
        r=qa.receipt("delulu_tech","website_stage","v2",output)
        self.assertNotIn("universal_quality_standard",output)
        self.assertEqual(r["universal_quality_standard"]["quality_contract_status"],"evidence_missing")
    def test_missing_evidence_is_incomplete(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"evidence.json"
            p.write_text(json.dumps({"project":"delulu_tech","checks":[]}))
            a=qa.inspect_quality_receipt(p,"delulu_tech",("rendered_pixel_visibility","desktop_mobile"))
            self.assertEqual(a["status"],"evidence_incomplete")
            self.assertEqual(len(a["missing"]),2)
            with self.assertRaisesRegex(qa.QualityStandardError,"foreign_project"):
                qa.inspect_quality_receipt(p,"moksha_overhaul",("desktop_mobile",))
    def test_self_report_cannot_approve(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"evidence.json"
            sample=b"independent automation report, NOT a human authorization"
            p.write_text(json.dumps({"project":"delulu_tech","checks":[{"id":"rendered_pixel_visibility","status":"passed","artifact_sha256":hashlib.sha256(sample).hexdigest(),"method":"automated"}]}))
            a=qa.inspect_quality_receipt(p,"delulu_tech",("rendered_pixel_visibility",))
            self.assertEqual(a["status"],"technical_evidence_reported")
            self.assertFalse(a["independent_human_accepted"])
            self.assertFalse(a["release_authorized"])
    def test_sha_cannot_be_fake(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"evidence.json"
            p.write_text(json.dumps({"project":"delulu_tech","checks":[{"id":"scope_binding","status":"passed","artifact_sha256":"not-a-real-sha","method":"automated"}]}))
            a=qa.inspect_quality_receipt(p,"delulu_tech",("scope_binding",))
            self.assertEqual(a["status"],"evidence_incomplete")

if __name__=="__main__":
    unittest.main(verbosity=2)
