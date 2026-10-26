#!/usr/bin/env python3
"""Test capability-aware routing refuses attractive but unusable toolyards."""
import importlib.util
from pathlib import Path
import unittest
q=importlib.util.spec_from_file_location("capability_router",Path(__file__).with_name("capability_router.py"))
r=importlib.util.module_from_spec(q);q.loader.exec_module(r)
class Routing(unittest.TestCase):
 def setUp(self):
  self.task={"project":"engagement_core_crm","manifest":"crm_wireframe_g1_v1",
   "action":"dev_project_build","owner_scoped_intake":True,"brief_pinned":True,
   "max_new_spend":0,"required_capabilities":["chrome_playwright"]}
  self.worker={"worker_id":"dell_design","project":"engagement_core_crm","ready":True,
   "workspace_isolated":True,"heartbeat_age_seconds":4,"lane":"development",
   "arbitrary_shell":False,"new_spend_required":False,"pending_job":False,
   "approved_actions":["dev_project_build"],
   "capabilities":{"chrome_playwright":{"probe":"passed","feature_smoke":"passed","project":"engagement_core_crm"}}}
 def choose(self):return r.choose(self.task,[self.worker])
 def test_exact_fit_yields_proposal_not_dispatch(self):
  a=self.choose()
  self.assertEqual(a["status"],"worker_fit_verified")
  self.assertFalse(a["automatically_dispatched"])
  self.assertFalse(a["production_authorized"])
 def test_installed_without_smoke_denied(self):
  self.worker["capabilities"]["chrome_playwright"]["feature_smoke"]="not_run"
  self.assertEqual(self.choose()["status"],"blocked")
 def test_foreign_project_denied(self):
  self.worker["project"]="shaadi_aunty_dodge"
  self.assertEqual(self.choose()["status"],"blocked")
 def test_unisolated_worker_denied(self):
  self.worker["workspace_isolated"]=False
  self.assertEqual(self.choose()["status"],"blocked")
 def test_stale_lane_denied(self):
  self.worker["heartbeat_age_seconds"]=61
  self.assertEqual(self.choose()["status"],"blocked")
 def test_active_job_denied(self):
  self.worker["pending_job"]=True
  self.assertEqual(self.choose()["status"],"blocked")
 def test_unapproved_spend_denied(self):
  self.task["max_new_spend"]=1
  self.assertIn("spend",self.choose()["reason"])
 def test_missing_intake_denied(self):
  self.task["owner_scoped_intake"]=False
  self.assertEqual(self.choose()["status"],"blocked")
 def test_unknown_action_denied(self):
  self.task["action"]="arbitrary_shell"
  self.assertEqual(self.choose()["status"],"blocked")
 def test_tool_not_authorized_action_denied(self):
  self.worker["approved_actions"]=["sandbox_qa"]
  self.assertEqual(self.choose()["status"],"blocked")
 def test_deterministic_freshest(self):
  second=dict(self.worker,worker_id="new_worker",heartbeat_age_seconds=2)
  self.assertEqual(r.choose(self.task,[self.worker,second])["worker"],"new_worker")
if __name__=="__main__":unittest.main()
