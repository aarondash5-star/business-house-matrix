"""Verify independent GPT-6 reference contract and semantic planning depth."""
import json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"brain"/"supervisor"))
import gate_s_v2 as s
F=ROOT/"benchmarks"/"gate_s"/"andaz_gpt6_reference_plan_20261023.json"
class ReferenceQuality(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.plan=json.loads(F.read_text())
 def test_contract(self):
  self.assertEqual(len(s.preview(self.plan)["plan"]["tasks"]),16)
 def test_milestones(self):
  self.assertGreaterEqual(len(self.plan["milestones"]),5)
 def test_acceptance_criteria_independently_present(self):
  self.assertTrue(all(t["deliverables"] and t["acceptance"] for t in self.plan["tasks"]))
 def test_specific_unknowns_documented(self):
  self.assertTrue(any("verify" in a.lower() for a in self.plan["assumptions"]))
 def test_booking_integration_task(self):
  self.assertTrue(any("pms" in t["objective"].lower() and t["role"]=="development" for t in self.plan["tasks"]))
 def test_mobile_qa_and_privacy(self):
  roles={t["role"] for t in self.plan["tasks"]}
  self.assertEqual(roles,s.ROLES)
  self.assertTrue(any("mobile" in t["objective"].lower() for t in self.plan["tasks"] if t["role"]=="qa"))
 def test_real_asset_verification(self):
  self.assertTrue(any("photo" in t["objective"].lower() for t in self.plan["tasks"] if t["role"]=="design"))
 def test_no_execution_rights(self):
  p=s.preview(self.plan)
  self.assertFalse(p["execute"])
  self.assertFalse(p["publish"])
  self.assertTrue(p["owner_approval_required"])
if __name__=="__main__":unittest.main()
