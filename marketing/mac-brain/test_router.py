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

    def test_all_providers_disabled(self):
        out = self.r.status()
        self.assertEqual(len(out["connections"]), 4)
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
