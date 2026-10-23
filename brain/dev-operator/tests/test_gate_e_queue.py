"""Gate E RC1 durable queue security and recovery tests (all offline)."""
from pathlib import Path
from unittest.mock import patch
import json
import sqlite3
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import gate_e_queue as queue
import gate_e_runtime as gate

class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="gate-e-queue-test-")
        self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)
        self.runs=self.home/"runs"
        self.runs.mkdir()
        self.db=self.home/"queue.sqlite"
        self.mocks=[
            patch.object(queue.operator,"RUNS",self.runs),
            patch.object(queue.operator,"approve_task",side_effect=self.approve)
        ]
        for m in self.mocks:
            m.start()
            self.addCleanup(m.stop)
        self.con=queue.connect(self.db)
        self.addCleanup(self.con.close)

    def approve(self,task):
        if not task.startswith("gate-e-"):
            raise gate.GateError("unapproved_task")
        return {"approved":True}

    def test_single_claim_and_idempotency(self):
        first=queue.enqueue(self.con,"gate-e-synthetic-one","key-unique-1")
        self.assertFalse(first["deduplicated"])
        self.assertTrue(queue.enqueue(self.con,"gate-e-synthetic-one","key-unique-1")["deduplicated"])
        queue.enqueue(self.con,"gate-e-synthetic-two","key-unique-2")
        with self.assertRaises(gate.GateError):
            queue.enqueue(self.con,"gate-e-synthetic-two","key-unique-1")
        task=queue.claim(self.con)
        self.assertEqual(task,"gate-e-synthetic-one")
        with queue.connect(self.db) as peer:
            self.assertIsNone(queue.claim(peer))
        queue.set_status(self.con,task,"verified_local_review","verified_local_review")
        self.assertEqual(queue.claim(self.con),"gate-e-synthetic-two")

    def test_crash_reconciliation_blocks_new_dispatch_without_replay(self):
        queue.enqueue(self.con,"gate-e-synthetic-one","key-unique-1")
        queue.enqueue(self.con,"gate-e-synthetic-two","key-unique-2")
        self.assertEqual(queue.claim(self.con),"gate-e-synthetic-one")
        result=queue.reconcile(self.con)
        self.assertEqual(result["orphaned_for_review"],["gate-e-synthetic-one"])
        self.assertIsNone(queue.claim(self.con))
        self.assertEqual(queue.status(self.con)[0]["status"],"orphaned_needs_review")
        self.assertEqual(queue.dispatch_once(self.con)["status"],"idle_or_blocked")

    def test_existing_completed_task_is_never_requeued(self):
        (self.runs/"gate-e-synthetic-one").mkdir()
        with self.assertRaises(gate.GateError):
            queue.enqueue(self.con,"gate-e-synthetic-one","key-unique-1")
        self.assertEqual(queue.status(self.con),[])

    def test_unapproved_enrollment_and_unsafe_idem_denied(self):
        with self.assertRaises(gate.GateError):
            queue.enqueue(self.con,"private-task","valid-key-111")
        with self.assertRaises(gate.GateError):
            queue.enqueue(self.con,"gate-e-safe","bad/key")
        self.assertEqual(queue.status(self.con),[])

    def test_terminal_verified_receipt_reconciles_to_queue(self):
        task="gate-e-synthetic-one"
        queue.enqueue(self.con,task,"key-unique-1")
        root=self.runs/task
        root.mkdir()
        (root/"receipt.json").write_text(json.dumps(
            {"task":task,"status":"verified_local_review","published":False,"pushed":False}))
        with patch.object(queue.gate,"bounded",return_value={"code":0,"stdout":"{}","stderr":""}) as execute:
            result=queue.dispatch_once(self.con)
        self.assertEqual(result["status"],"verified_local_review")
        self.assertFalse(result["automatically_retried"])
        self.assertEqual(execute.call_count,1)

    def test_missing_terminal_receipt_needs_manual_review(self):
        task="gate-e-synthetic-one"
        queue.enqueue(self.con,task,"key-unique-1")
        with patch.object(queue.gate,"bounded",side_effect=gate.GateError("timeout")):
            result=queue.dispatch_once(self.con)
        self.assertEqual(result["status"],"needs_review")
        self.assertEqual(queue.status(self.con)[0]["status"],"needs_review")

if __name__=="__main__":
    unittest.main()
