#!/usr/bin/env python3
"""Network-free tests for Dell-compatible hosted Marketing router."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).with_name("router.py")
TEMPLATE = Path(__file__).with_name("provider-policy.template.json")

class MarketingRouterTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bhm-router-test-")
        self.root = Path(self.temp.name)
        spec = importlib.util.spec_from_file_location("marketing_router", SOURCE)
        self.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.r)
        self.r.BASE = self.root
        self.r.POLICY = self.root / "provider-policy.json"
        self.r.VAULT = self.root / "secrets"
        self.r.LEDGER = self.root / "provider-quota.sqlite3"
        self.r.BRAIN_CONFIG = self.root / "config.json"
        self.r.POLICY.write_text(TEMPLATE.read_text())
        self.r.BRAIN_CONFIG.write_text('{"online_enabled":false}')
        self.r.db().close()

    def tearDown(self):
        self.temp.cleanup()

    def test_zero_paid_validation(self):
        self.assertFalse(self.r.read_policy()["paid_inference_allowed"])
        p = self.r.read_policy()
        p["connections"][0]["model"] = "paid/unapproved-model"
        self.r.POLICY.write_text(json.dumps(p))
        with self.assertRaisesRegex(RuntimeError, "allowlisted"):
            self.r.read_policy()

    def test_gemini_proprietary_guard_and_openrouter_key_gate(self):
        p=self.r.read_policy()
        slot=next(s for s in p["connections"] if s["provider"]=="gemini")
        self.assertEqual(self.r.eligibility(slot)[1],"disabled")
        forced={**slot,"enabled":True,"free_plan_confirmed":True}
        self.assertEqual(self.r.eligibility(forced)[1],"license_review")
        with self.assertRaisesRegex(RuntimeError,"proprietary-model exception"):
            self.r.call_api(forced,"Synthetic content. Do not send to a vendor.")
        router_slot=next(s for s in p["connections"] if s["provider"]=="openrouter")
        with self.assertRaisesRegex(RuntimeError,"no securely enrolled"):
            self.r.verify_provider(router_slot["id"])

    def test_candidate_vendor_slots_blocked(self):
        p = self.r.read_policy()
        self.assertEqual(len(p["connections"]), 5)
        gemini = next(x for x in p["connections"] if x["id"]=="gemini-flash-candidate")
        self.assertFalse(gemini["enabled"])
        self.assertFalse(gemini["model_license_approved"])
        self.assertEqual(p["tool_connections"][0]["id"], "searxng-search")
        self.assertEqual(p["tool_connections"][0]["provider"], "searxng")
        self.assertFalse(p["tool_connections"][0]["enabled"])
        p["tool_connections"][0]["enabled"] = True
        p["tool_connections"][0]["self_hosted"] = False
        self.r.POLICY.write_text(json.dumps(p))
        with self.assertRaisesRegex(RuntimeError, "SearXNG requires"):
            self.r.read_policy()

    def test_all_providers_disabled(self):
        out = self.r.status()
        self.assertEqual(len(out["connections"]), 5)
        self.assertTrue(all(not s["eligible"] for s in out["connections"]))
        self.assertTrue(all(not s["credentials_present"] for s in out["connections"]))
        self.assertEqual(out["paid_inference_allowed"], False)

    def test_run_fails_without_network(self):
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            self.r.run("creative", "Create three headlines")

    def test_enroll_requires_tty(self):
        with self.assertRaisesRegex(RuntimeError, "interactive"):
            self.r.enroll("groq-creative-oss120", free_confirmed=True)
        self.assertFalse(self.r.VAULT.exists())

    def test_synthetic_429_falls_back_without_network(self):
        p = self.r.read_policy()
        self.r.VAULT.mkdir(mode=0o700)
        key = self.r.VAULT / "groq-creative-oss120.key"
        key.write_text("synthetic-key-never-used")
        key.chmod(0o600)
        for s in p["connections"][:2]:
            s["enabled"] = True
            s["free_plan_confirmed"] = True
        p["connections"][1]["credential_ref"] = "groq-creative-oss120"
        self.r.POLICY.write_text(json.dumps(p))
        self.r.BRAIN_CONFIG.write_text('{"online_enabled":true}')
        attempted = []
        original_call = self.r.call_api
        def mock_call(s, prompt, **kwargs):
            attempted.append(s["id"])
            if s["id"] == "groq-creative-oss120":
                raise self.r.ProviderFailure(429)
            return "Sample creative concept"
        self.r.call_api = mock_call
        try:
            result = self.r.run("creative", "Propose a concept")
        finally:
            self.r.call_api = original_call
        self.assertEqual(result["slot"], "groq-copy-qwen")
        self.assertEqual(len(attempted), 2)
        db = self.r.db()
        outcomes = db.execute("SELECT outcome FROM events ORDER BY id").fetchall()
        self.assertEqual([x[0] for x in outcomes], ["failed", "ok"])
        self.assertIsNotNone(db.execute("SELECT until_epoch FROM cooldowns WHERE slot='groq-creative-oss120'").fetchone())
        db.close()

    def test_quota_group_sharing_and_cooldown(self):
        p = self.r.read_policy()
        self.r.VAULT.mkdir(mode=0o700)
        key = self.r.VAULT / "groq-creative-oss120.key"
        key.write_text("synthetic-key-never-used")
        key.chmod(0o600)
        s = p["connections"][0]
        s["enabled"] = True
        s["free_plan_confirmed"] = True
        self.r.POLICY.write_text(json.dumps(p))
        con = self.r.db()
        selected = [r for r in self.r.candidates("creative", p, con) if r[0]["id"] == s["id"]][0]
        self.assertTrue(selected[1])
        for i in range(40):
            con.execute("INSERT INTO events(slot,ts,outcome) VALUES(?,?,?)",
                        ("groq-copy-qwen", self.r.epoch(), "reserved"))
        self.assertEqual([r for r in self.r.candidates("creative", p, con)
                          if r[0]["id"] == s["id"]][0][2], "daily_quota")
        con.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
