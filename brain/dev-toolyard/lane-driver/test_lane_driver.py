"""Independent deterministic lane-driver unit and negative gates; synthetic only."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from lane_driver import Ledger, DriverDenied


SHA = "a" * 64
EVIDENCE = "b" * 64


def spec(task="fixture_task_a", host="dell-linux", lane="development"):
    return {
        "schema": 1,
        "task_id": task,
        "project_id": "matrix_dev_manager",
        "host_id": host,
        "lane": lane,
        "brief_sha256": SHA,
        "stages": [
            {"id": "implementation", "action": "dev_project_build",
             "manifest": "driver_fixture_v1", "return_to": None},
            {"id": "independent_qa", "action": "sandbox_qa",
             "manifest": "driver_qa_fixture_v1", "return_to": "implementation"},
            {"id": "review", "action": "sandbox_qa",
             "manifest": "driver_review_fixture_v1", "return_to": "implementation"},
        ],
        "max_corrections": 2,
        "release_allowed": False,
        "spend_allowed": False,
    }


def receipt(task="fixture_task_a", host="dell-linux", lane="development",
            state="completed", gate="pass", code=0, ident="synthetic-rcpt-001"):
    return {
        "receipt_id": ident, "task_id": task, "host_id": host, "lane": lane,
        "state": state, "exit_code": code, "gate": gate,
        "source_sha256": SHA, "evidence_sha256": EVIDENCE,
    }


def admit(owner, stage):
    return owner["project_id"] == "matrix_dev_manager" and stage["action"] in {"dev_project_build", "sandbox_qa"}


def verify(owner, stage, evidence):
    return evidence["task_id"] == owner["task_id"] and evidence["evidence_sha256"] == EVIDENCE


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "lane" / "driver.sqlite3"
        self.ledger = Ledger(self.file)
        self.addCleanup(self.ledger.close)

    def enrolled(self, task="fixture_task_a", host="dell-linux", lane="development"):
        item = spec(task, host, lane)
        self.ledger.enroll(item, lambda x: True)
        return item

    def run_stage(self, number, task="fixture_task_a", gate="pass", state="completed", code=0):
        current = self.ledger.get(task)
        self.assertEqual(current["stage_idx"], number)
        reservation = self.ledger.reserve(task, current["version"], admit)
        current = self.ledger.get(task)
        return self.ledger.observe(
            task, current["version"], reservation["lease"],
            receipt(task, state=state, gate=gate, code=code, ident=f"synthetic-rcpt-{current['version']:03}"),
            verify)

    def test_happy_path(self):
        self.enrolled()
        self.assertEqual(self.run_stage(0)["state"], "ready")
        self.assertEqual(self.run_stage(1)["state"], "ready")
        self.assertEqual(self.run_stage(2)["state"], "complete")
        self.assertTrue(self.ledger.verify_chain("fixture_task_a")["valid"])

    def test_success_no_automatic_release(self):
        self.enrolled()
        for index in range(3):
            self.run_stage(index)
        self.assertFalse(json.loads(self.ledger.get("fixture_task_a")["spec"])["release_allowed"])

    def test_qa_return_to_previous(self):
        self.enrolled()
        self.run_stage(0)
        outcome = self.run_stage(1, gate="correctable_fail", state="failed", code=2)
        self.assertEqual((outcome["stage_idx"], outcome["corrections"], outcome["state"]), (0, 1, "ready"))
        self.run_stage(0)
        self.run_stage(1)
        self.run_stage(2)
        self.assertEqual(self.ledger.get("fixture_task_a")["state"], "complete")

    def test_retry_exhaustion(self):
        self.enrolled()
        for attempt in range(3):
            self.run_stage(0)
            outcome = self.run_stage(1, gate="correctable_fail", state="failed", code=3)
        self.assertEqual((outcome["state"], outcome["reason"]), ("blocked", "retry_limit_exhausted"))
        with self.assertRaises(DriverDenied):
            self.ledger.reserve("fixture_task_a", self.ledger.get("fixture_task_a")["version"], admit)

    def test_unknown_terminal_quarantine(self):
        self.enrolled()
        outcome = self.run_stage(0, gate="uncertain", state="outcome_unknown", code=None)
        self.assertEqual(outcome["reason"], "uncertain_no_replay")
        with self.assertRaises(DriverDenied):
            self.ledger.reserve("fixture_task_a", self.ledger.get("fixture_task_a")["version"], admit)

    def test_no_identity_cross_host(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 1, p["lease"],
                                receipt(host="mac-linux"), verify)

    def test_unauthorized_gate_verifier(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 1, p["lease"], receipt(), lambda *_: False)
        self.assertEqual(self.ledger.get("fixture_task_a")["state"], "reserved")

    def test_missing_gate_verifier(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 1, p["lease"], receipt(), None)

    def test_exact_replay_deduplicates_reservation(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        replay = self.ledger.reserve("fixture_task_a", 1, admit)
        self.assertEqual(p["lease"], replay["lease"])
        self.assertTrue(replay["deduplicated"])

    def test_unknown_stage_admission_denied(self):
        self.enrolled()
        with self.assertRaises(DriverDenied):
            self.ledger.reserve("fixture_task_a", 0, lambda *_: False)

    def test_stale_version_denied(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 0, p["lease"], receipt(), verify)

    def test_stale_receipt_replay_denied(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        self.ledger.observe("fixture_task_a", 1, p["lease"], receipt(), verify)
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 1, p["lease"], receipt(), verify)

    def test_duplicate_enrollment_dedup(self):
        item = self.enrolled()
        self.assertEqual(self.ledger.enroll(item, lambda _: True)["task_id"], item["task_id"])
        item["brief_sha256"] = "c" * 64
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(item, lambda _: True)

    def test_owner_approval_required(self):
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(spec(), lambda _: False)

    def test_forbidden_releases(self):
        item = spec()
        item["release_allowed"] = True
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(item, lambda _: True)

    def test_forbidden_paid_usage(self):
        item = spec()
        item["spend_allowed"] = True
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(item, lambda _: True)

    def test_unknown_envelope_fields_rejected(self):
        item = spec()
        item["command"] = "sh -c evil"
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(item, lambda _: True)

    def test_forward_retry_edge_rejected(self):
        item = spec()
        item["stages"][0]["return_to"] = "review"
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(item, lambda _: True)

    def test_invalid_lane_rejected(self):
        with self.assertRaises(DriverDenied):
            self.ledger.enroll(spec(lane="unknown"), lambda _: True)

    def test_works_with_six_isolated_driver_identifiers(self):
        for index, host in enumerate(("dell-linux", "mac-linux")):
            for j, lane in enumerate(("control", "operations", "development")):
                task = f"fixture_task_{index}_{j}"
                self.enrolled(task=task, host=host, lane=lane)
                self.assertEqual((self.ledger.get(task)["host"], self.ledger.get(task)["lane"]), (host, lane))

    def test_symlink_db_denied(self):
        target = Path(self.tmp.name) / "target"
        target.write_text("canary")
        pointer = Path(self.tmp.name) / "pointer"
        pointer.symlink_to(target)
        with self.assertRaises(DriverDenied):
            Ledger(pointer)

    def test_evidence_source_sha_rejected(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        e = receipt()
        e["source_sha256"] = "d" * 64
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 1, p["lease"], e, verify)

    def test_event_hash_tamper_detected(self):
        self.enrolled()
        self.ledger.db.execute("UPDATE events SET kind='altered' WHERE task_id='fixture_task_a'")
        with self.assertRaises(DriverDenied):
            self.ledger.verify_chain("fixture_task_a")

    def test_crash_reopen_reservation_not_replayed(self):
        self.enrolled()
        first = self.ledger.reserve("fixture_task_a", 0, admit)
        self.ledger.close()
        self.ledger = Ledger(self.file)
        replay = self.ledger.reserve("fixture_task_a", 1, admit)
        self.assertTrue(replay["deduplicated"])
        self.assertEqual(first["lease"], replay["lease"])

    def test_bad_final_qa_does_not_advance(self):
        self.enrolled()
        outcome = self.run_stage(0, gate="block", state="completed", code=0)
        self.assertEqual(outcome["state"], "blocked")

    def test_missing_receipt_fields_denied(self):
        self.enrolled()
        p = self.ledger.reserve("fixture_task_a", 0, admit)
        bad = receipt()
        del bad["evidence_sha256"]
        with self.assertRaises(DriverDenied):
            self.ledger.observe("fixture_task_a", 1, p["lease"], bad, verify)


if __name__ == "__main__":
    unittest.main()
