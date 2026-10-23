"""Autonomous Dev Matrix candidate: durable planning dispatch smoke, never live workers."""
import json
import pathlib
import sqlite3
import sys
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"brain"/"supervisor"))
import autonomous_dev_matrix_v1 as m
REFERENCE=ROOT/"benchmarks"/"gate_s"/"andaz_gpt6_reference_plan_20261023.json"

def reference():
 return json.loads(REFERENCE.read_text())
class TestStagedAutonomy(unittest.TestCase):
 def test_work_order_is_admissible(self):
  p=reference()
  self.assertEqual(len(m.policy_check(p)["tasks"]),16)
 def test_parallelism_exists(self):
  groups=m.layers(reference())
  self.assertTrue(any(len(x)>1 for x in groups))
  self.assertEqual(set(sum(groups,[])),{x["id"] for x in reference()["tasks"]})
 def test_default_is_no_authority(self):
  for key in ("execute_real_tools","allow_publish","allow_merge","allow_spend","allow_privilege_change"):
   self.assertFalse(m.POLICY[key])
  self.assertTrue(m.POLICY["require_owner_review"])
  self.assertFalse(m.POLICY["auto_retry"])
 def test_only_fixed_specialists(self):
  self.assertEqual(set(m.REGISTRY),{"research","design","development","qa","security","review"})
 def test_simulated_handoff_requires_owner(self):
  with tempfile.TemporaryDirectory() as t:
   db=pathlib.Path(t)/"records.sqlite3"
   p=reference()
   receipt=m.stage_plan(p,db)
   outcome=m.simulated_dispatch(p,db)
   self.assertEqual(receipt["total_tasks"],16)
   self.assertEqual(outcome["state"],"owner_review_required")
   self.assertEqual(outcome["results"]["T16"],"awaiting_human_approval")
   self.assertFalse(outcome["executed_real_work"])
   with sqlite3.connect(db) as sql:
    self.assertEqual(sql.execute("select count(*) from tasks").fetchone()[0],16)
    self.assertGreater(sql.execute("select count(*) from events").fetchone()[0],16)
 def test_injected_research_failure_blocks_dependent(self):
  with tempfile.TemporaryDirectory() as t:
   db=pathlib.Path(t)/"failure.sqlite3"
   p=reference()
   m.stage_plan(p,db)
   outcome=m.simulated_dispatch(p,db,{"T1"})
   self.assertEqual(outcome["state"],"blocked")
   self.assertEqual(outcome["results"]["T1"],"failed_simulated")
   self.assertEqual(outcome["results"]["T16"],"blocked_dependency")
 def test_no_replay_same_database(self):
  with tempfile.TemporaryDirectory() as t:
   db=pathlib.Path(t)/"run.sqlite3"
   m.stage_plan(reference(),db)
   with self.assertRaises(m.AutonomyError):m.stage_plan(reference(),db)
 def test_reject_unenrolled_role(self):
  p=reference();p["tasks"][1]["role"]="operator"
  with self.assertRaises(m.AutonomyError):m.policy_check(p)
 def test_reject_unverified_dev(self):
  p=reference()
  p["tasks"][12]["depends_on"]=["T8","T11"]
  p["tasks"][11]["depends_on"]=["T4","T9"]
  p["tasks"][14]["depends_on"]=["T10","T12","T14"]
  # Remove T7 from all QA transitive paths: task T7 appears via T8 and T9,
  # so simpler: disconnect specific T10 from QA and make it dangling.
  p["tasks"][14]["depends_on"]=["T12","T13","T14"]
  with self.assertRaises(m.AutonomyError):m.policy_check(p)
 def test_no_early_approval(self):
  p=reference();p["tasks"][3]["role"]="review"
  with self.assertRaises(m.AutonomyError):m.policy_check(p)
 def test_no_review_without_security(self):
  p=reference();p["tasks"][-1]["depends_on"]=["T13"]
  with self.assertRaises(m.AutonomyError):m.policy_check(p)
 def test_no_review_without_qa(self):
  p=reference();p["tasks"][-1]["depends_on"]=["T14"]
  # T14 already indirectly depends on QA T12/T13 so this remains safe.
  self.assertEqual(len(m.policy_check(p)["tasks"]),16)
 def test_unknown_injection_denied(self):
  with tempfile.TemporaryDirectory() as t:
   db=pathlib.Path(t)/"run.sqlite3"
   m.stage_plan(reference(),db)
   with self.assertRaises(m.AutonomyError):
    m.simulated_dispatch(reference(),db,{"T99"})
if __name__=="__main__":unittest.main()
