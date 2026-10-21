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
        self.assertEqual(result["conservative_monthly_request_cap"],100)
    def test_public_query_dlp(self):
        for q in ("help alice@example.com", "find phone +919876543210",
                  "private customer list", "api key leaked"):
            with self.assertRaises(ValueError):
                self.mod.check_public_query(q)

    def test_private_extract_urls_denied(self):
        for url in ("http://example.com", "https://localhost/xyz",
                    "https://10.0.0.2/path", "https://example.com/?token=abc",
                    "https://username:pass@example.com/"):
            with self.assertRaises(ValueError):
                self.mod.check_public_url(url)

    def test_keyless_search_no_credential_header(self):
        self.mod.router.read_policy=lambda:{"tool_connections":[{
            "id":"tavily-search","provider":"tavily","enabled":True,
            "keyless_mode":True,"public_only":True,
            "external_search_service_disclosed":True,
            "conservative_monthly_credits":100}]}
        original=self.mod.urllib.request.urlopen
        captured=[]
        import io
        class FakeHTTP:
            def __init__(self):self.input=io.BytesIO(json.dumps({
               "results":[{"title":"example","url":"https://example.org/a",
                           "content":"Public article"}]}).encode())
            def __enter__(self):return self
            def __exit__(self,*x):return False
            def read(self,*args):return self.input.read(*args)
        def fake_request(request,timeout=None):
            captured.append(request)
            return FakeHTTP()
        self.mod.urllib.request.urlopen=fake_request
        try:
            result=self.mod.search("open source marketing research")
        finally:
            self.mod.urllib.request.urlopen=original
        self.assertEqual(result["mode"],"keyless")
        self.assertEqual(len(result["results"]),1)
        headers={k.lower():v for k,v in captured[0].header_items()}
        self.assertEqual(headers.get("x-tavily-access-mode"),"keyless")
        self.assertNotIn("authorization",headers)
        self.assertFalse(self.mod.SECRET.exists())

    def test_keyless_429_creates_cooldown_without_retry(self):
        self.mod.router.read_policy=lambda:{"tool_connections":[{
            "id":"tavily-search","provider":"tavily","enabled":True,
            "keyless_mode":True,"public_only":True,
            "external_search_service_disclosed":True,
            "conservative_monthly_credits":100}]}
        import urllib.error
        orig=self.mod.urllib.request.urlopen
        calls=[]
        def response(request, timeout=None):
            calls.append(1)
            raise urllib.error.HTTPError("https://api.tavily.com/search",429,
                "rate limited",{"Retry-After":"600"},None)
        self.mod.urllib.request.urlopen=response
        try:
            with self.assertRaisesRegex(RuntimeError,"cooldown 600"):
                self.mod.search("public travel industry research")
            self.assertGreaterEqual(self.mod.state()["keyless_cooldown_seconds_remaining"],590)
            with self.assertRaisesRegex(RuntimeError,"temporarily rate-limited"):
                self.mod.search("public wellness travel insights")
            self.assertEqual(len(calls),1)
        finally:
            self.mod.urllib.request.urlopen=orig

    def test_keyless_budget_enforced(self):
        self.mod.router.read_policy=lambda:{"tool_connections":[{
            "id":"tavily-search","provider":"tavily","enabled":True,
            "keyless_mode":True,"public_only":True,
            "external_search_service_disclosed":True,
            "conservative_monthly_credits":1}]}
        self.mod.reserve("search",self.mod.policy())[0].close()
        with self.assertRaisesRegex(RuntimeError,"limit reached"):
            self.mod.reserve("search",self.mod.policy())
if __name__=="__main__":unittest.main(verbosity=2)
