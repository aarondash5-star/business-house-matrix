#!/usr/bin/env python3
"""Isolation and fail-closed tests for staged Tavily adapter. No vendor requests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
SRC=ROOT/"research.py"
class ResearchTest(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(prefix="bhm-research-")
        self.temp=Path(self.t.name)
        spec=importlib.util.spec_from_file_location("research_test",SRC)
        self.mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.mod.DB=self.temp/"quota.sqlite3"
        self.mod.SECRET=self.temp/"secrets"/"tavily-search.key"
        self.saved=self.mod.router.read_policy
        self.mod.router.read_policy=lambda:{"tool_connections":[{
            "id":"tavily-search","provider":"tavily","enabled":False,
            "service_terms_reviewed":False,"free_plan_confirmed":False,
            "conservative_monthly_credits":100}]}
    def tearDown(self):
        self.mod.router.read_policy=self.saved
        self.t.cleanup()
    def test_denies_unenrolled_research(self):
        with self.assertRaisesRegex(RuntimeError,"disabled"):
            self.mod.search("reel trends")
    def test_status_reports_private_unenrolled_state(self):
        result=self.mod.state()
        self.assertFalse(result["enabled"])
        self.assertFalse(result["credential_present"])
        self.assertEqual(result["conservative_monthly_cap"],100)
    def test_enroll_fails_before_terms_review(self):
        with self.assertRaisesRegex(RuntimeError,"exception"):
            self.mod.enroll()
        self.assertFalse(self.mod.SECRET.exists())
if __name__=="__main__":unittest.main(verbosity=2)
