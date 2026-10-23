"""Tests of the read-only Dev Brain status responder using a stubbed controller."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "brain" / "dev-operator"))
from super_dev_ssh_duplex import Mailbox
import super_dev_ssh_worker_once as worker


class WorkerOnceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.box = Mailbox(Path(self.tmp.name) / "db.sqlite3")
        self.addCleanup(self.box.close)

    def test_actual_duplex_data_flow(self):
        self.box.send(message_id="super-task-001", thread_id="andaz-task-001",
                      sender="super", kind="task",
                      body={"operation": "controller_status", "nonce": "handshake-001"})
        with patch.object(worker, "controller_status",
                          return_value={"state": "ready", "controller_version": "test-v6"}):
            receipt = worker.respond_once(self.box)
        self.assertTrue(receipt["handled"])
        self.assertEqual(receipt["brain_state"], "ready")
        messages = self.box.poll(recipient="super")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["body"]["nonce"], "handshake-001")
        self.assertEqual(messages[0]["body"]["controller_version"], "test-v6")
        self.assertEqual(messages[0]["in_reply_to"], "super-task-001")
        self.assertEqual(worker.respond_once(self.box)["handled"], False)
        self.assertTrue(self.box.verify_thread("andaz-task-001")["chain_verified"])

    def test_no_arbitrary_operation(self):
        self.box.send(message_id="super-task-002", thread_id="andaz-task-002",
                      sender="super", kind="task",
                      body={"operation": "run_shell", "command": "id"})
        self.assertFalse(worker.respond_once(self.box)["handled"])
        self.assertEqual(self.box.poll(recipient="super"), [])

    def test_backlog_does_not_starve_new_supported_request(self):
        for i in range(105):
            self.box.send(
                message_id=f"super-unsupported-{i:04d}",
                thread_id=f"unsupported-thread-{i:04d}",
                sender="super", kind="task",
                body={"operation": "unrecognized"},
            )
        self.box.send(
            message_id="super-task-late-001",
            thread_id="late-thread-001",
            sender="super", kind="task",
            body={"operation": "controller_status", "nonce": "late"},
        )
        with patch.object(worker, "controller_status", return_value={"state": "ready"}):
            receipt = worker.respond_once(self.box)
        self.assertTrue(receipt["handled"])
        self.assertEqual(receipt["thread_id"], "late-thread-001")
        self.assertEqual(self.box.poll(recipient="super")[0]["body"]["nonce"], "late")


if __name__ == "__main__":
    unittest.main()
