"""Fast no-network tests for promotion policy; not device/runtime QA."""
import copy
import json
import unittest
from pathlib import Path

from release_gate import GateError, validate_production, validate_route

ROOT = Path(__file__).resolve().parents[2]


class SuperGPTPolicyTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads(
            (ROOT / "docs/supergpt/qa/RELEASE_EVIDENCE.json").read_text(encoding="utf-8")
        )

    def test_allowed_dev_to_test(self):
        self.assertFalse(validate_route("pull_request", "super-gpt/test", "super-gpt/dev"))

    def test_allowed_test_to_production(self):
        self.assertTrue(validate_route("pull_request", "super-gpt/production", "super-gpt/test"))

    def test_direct_dev_to_production_denied(self):
        with self.assertRaises(GateError):
            validate_route("pull_request", "super-gpt/production", "super-gpt/dev")

    def test_wrong_source_to_test_denied(self):
        with self.assertRaises(GateError):
            validate_route("pull_request", "super-gpt/test", "main")

    def test_pending_production_evidence_denied(self):
        with self.assertRaises(GateError):
            validate_production(self.evidence, git_ancestry=False, online=False)

    def test_synthetic_valid_evidence_passes_field_checks_only(self):
        e = copy.deepcopy(self.evidence)
        e["candidate"] = "supergpt-rc1"
        e["tested_commit"] = "a" * 40
        e["android_build"].update({
            "source_mode": "project-integrated",
            "apk_sha256": "b" * 64,
            "run_url": "https://github.com/aarondash5-star/business-house-matrix/actions/runs/123456",
        })
        e["android_runtime"].update({
            "device_type": "emulator", "android_api": 30,
            "install": "passed", "cold_start": "passed",
            "crash_scan": "passed", "interaction": "passed",
            "receipt_url": "https://example.org/private-device-receipt",
        })
        e["independent_qa"].update({
            "status": "passed", "reviewer": "independent-test-reviewer",
            "receipt_url": "https://example.org/private-qa-receipt",
        })
        e["owner_acceptance"].update({
            "status": "passed",
            "approval_reference": "https://example.org/owner-acceptance",
        })
        e["known_blockers"] = []
        validate_production(e, git_ancestry=False, online=False)

    def test_upstream_only_source_rejected(self):
        e = copy.deepcopy(self.evidence)
        e["candidate"] = "supergpt-rc1"
        e["android_build"]["source_mode"] = "upstream-prototype"
        with self.assertRaises(GateError):
            validate_production(e, git_ancestry=False, online=False)


if __name__ == "__main__":
    unittest.main()
