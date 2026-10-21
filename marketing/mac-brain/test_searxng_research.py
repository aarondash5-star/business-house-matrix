#!/usr/bin/env python3
"""No-network regression checks for LAN-only SearXNG research."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

MODULE=Path(__file__).with_name("searxng_research.py")
class SearchTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="bhm-searxng-")
        spec=importlib.util.spec_from_file_location("searxng_research",MODULE)
        self.r=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.r)
        self.r.DB=Path(self.tmp.name)/"counts.sqlite3"
        self.saved=self.r.router.read_policy
        self.policy={"tool_connections":[{
            "id":"searxng-search","provider":"searxng","type":"search",
            "enabled":True,"self_hosted":True,"open_source_license_reviewed":True,
            "paid_fallback_allowed":False}]}
        self.r.router.read_policy=lambda:self.policy
    def tearDown(self):
        self.r.router.read_policy=self.saved
        self.tmp.cleanup()
    def test_disabled_rejects_without_network(self):
        self.policy["tool_connections"][0]["enabled"]=False
        with self.assertRaisesRegex(RuntimeError,"disabled"):self.r.search("public wellness market")
    def test_private_query_denied(self):
        for value in ["email someone@example.org","+919876543210 location",
                      "password credentials", "guest data tracking"]:
            with self.assertRaises(ValueError):self.r._public_query(value)
    def test_local_endpoint_pinned(self):
        self.r.GATEWAY="http://example.com:18888"
        with self.assertRaisesRegex(RuntimeError,"Nonallowlisted"):self.r.search("wellness research")
    def test_realistic_search_mock_returns_sources(self):
        prev=self.r.urlopen
        calls=[]
        class HTTP:
            def __init__(self):
                self.data=io.BytesIO(json.dumps({"results":[
                    {"title":"Wellness site","url":"https://example.org/wellness",
                     "content":"A sourced description", "engine":"wikipedia"},
                    {"title":"Not public","url":"http://127.0.0.1/admin",
                     "content":"bad"}]}).encode())
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self,*args):return self.data.read(*args)
        def fake(req,timeout):
            calls.append(req.full_url)
            return HTTP()
        self.r.urlopen=fake
        try:answer=self.r.search("sauna wellness research")
        finally:self.r.urlopen=prev
        self.assertEqual(len(calls),1)
        self.assertEqual(answer["provider"],"searxng")
        self.assertEqual(len(answer["results"]),1)
        self.assertTrue(answer["citations_required"])
        self.assertFalse(answer["publish_approval"])
    def test_local_quota(self):
        p=self.r._policy()
        conn=self.r._ledger()
        now=int(__import__("time").time())
        for _ in range(100):
            conn.execute("INSERT INTO attempts(ts,kind,outcome) VALUES(?,?,?)",
                         (now,"search","reserved"))
        conn.close()
        with self.assertRaisesRegex(RuntimeError,"rate limit"):
            self.r.search("marketing research")
    def test_tavily_extract_retired(self):
        with self.assertRaisesRegex(RuntimeError,"deprecated"):
            self.r.extract("https://example.org")

if __name__=="__main__":unittest.main(verbosity=2)
