#!/usr/bin/env python3
"""Offline tests for the owner-reviewed, narrow SearXNG tool activation."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest import TestCase, main, mock
import router


class ResearchActivationTest(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="bhm-research-activation-")
        self.old_policy, self.old_config = router.POLICY, router.BRAIN_CONFIG
        root = Path(self.temp.name)
        router.POLICY = root / "provider-policy.json"
        router.BRAIN_CONFIG = root / "config.json"
        self.policy = {
            "version": 1, "paid_inference_allowed": False, "connections": [],
            "tool_connections": [{
                "id": "searxng-search", "provider": "searxng", "type": "search",
                "enabled": False, "self_hosted": True,
                "open_source_license_reviewed": True,
                "paid_fallback_allowed": False, "conservative_daily_requests": 100,
                "endpoint": "old disabled LAN gateway"
            }]
        }
        router.POLICY.write_text(json.dumps(self.policy))
        router.BRAIN_CONFIG.write_text(json.dumps({
            "publish_enabled": False, "spend_enabled": False,
            "local_inference_enabled": False
        }))

    def tearDown(self):
        router.POLICY, router.BRAIN_CONFIG = self.old_policy, self.old_config
        self.temp.cleanup()

    @staticmethod
    def check(argv, **_):
        action = argv[-1]
        values = {
            "identity": {"host_id": "mac-linux",
                         "fingerprint": "a14b45012cbc7d39b52b6a68",
                         "trusted_peer": "fb011d3c5f91d65b50c7184c"},
            "selftest": {"passed": True},
            "health": {"service": "bhm-research-v1", "healthy": True,
                       "authenticated_jobs_only": True, "public_search_port": False}
        }
        return SimpleNamespace(returncode=0, stdout=json.dumps(values[action]))

    def test_enables_only_approved_tool_and_backups(self):
        with mock.patch("pathlib.Path.is_file", return_value=True), mock.patch("subprocess.run", side_effect=self.check):
            first = router.activate_research_relay()
            second = router.activate_research_relay()
        self.assertTrue(first["enabled"])
        self.assertTrue(second["already_active"])
        updated = json.loads(router.POLICY.read_text())
        self.assertEqual(updated["tool_connections"][0]["transport"], "encrypted_signed_relay_v1")
        self.assertTrue(updated["tool_connections"][0]["enabled"])
        self.assertFalse(updated["paid_inference_allowed"])
        backup = router.POLICY.with_name("provider-policy.json.pre-bhm-research-20261021")
        self.assertFalse(json.loads(backup.read_text())["tool_connections"][0]["enabled"])

    def test_mismatched_fingerprint_is_rejected_and_policy_untouched(self):
        def wrong(argv, **kwargs):
            r = self.check(argv, **kwargs)
            if argv[-1] == "identity":
                r.stdout = json.dumps({"host_id": "mac-linux", "fingerprint": "impostor"})
            return r
        before = router.POLICY.read_text()
        with mock.patch("pathlib.Path.is_file", return_value=True), mock.patch("subprocess.run", side_effect=wrong):
            with self.assertRaisesRegex(RuntimeError, "identity"):
                router.activate_research_relay()
        self.assertEqual(before, router.POLICY.read_text())

    def test_publication_permission_denies_activation(self):
        router.BRAIN_CONFIG.write_text(json.dumps({
            "publish_enabled": True, "spend_enabled": False,
            "local_inference_enabled": False
        }))
        with mock.patch("pathlib.Path.is_file", return_value=True):
            with self.assertRaisesRegex(RuntimeError, "Publishing"):
                router.activate_research_relay()
        self.assertFalse(router.read_policy()["tool_connections"][0]["enabled"])


if __name__ == "__main__":
    main()
