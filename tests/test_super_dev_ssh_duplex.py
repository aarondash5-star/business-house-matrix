"""Independent regression tests for the bounded Super Brain/Dev Brain SSH mailbox."""
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "brain" / "dev-operator"))
from super_dev_ssh_duplex import Denied, Mailbox


class DuplexMailboxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.box = Mailbox(Path(self.tmp.name) / "mailbox.sqlite3")
        self.addCleanup(self.box.close)
        self.thread = "andaz-task-001"

    def send(self, mid, sender, kind, reply=None, body=None):
        return self.box.send(
            message_id=mid, thread_id=self.thread, sender=sender,
            kind=kind, in_reply_to=reply,
            body=body or {"text": mid},
        )

    def test_full_duplex_question_and_answer(self):
        first = self.send("super-task-001", "super", "task")
        accepted = self.send("dev-accept-001", "dev", "accepted", "super-task-001")
        question = self.send("dev-question-001", "dev", "question", "super-task-001")
        answer = self.send("super-answer-001", "super", "answer", "dev-question-001")
        result = self.send("dev-result-001", "dev", "result", "super-answer-001")
        self.assertEqual([x["seq"] for x in (first, accepted, question, answer, result)], [1, 2, 3, 4, 5])
        dev_inbox = self.box.poll(recipient="dev")
        super_inbox = self.box.poll(recipient="super")
        self.assertEqual([m["kind"] for m in dev_inbox], ["task", "answer"])
        self.assertEqual([m["kind"] for m in super_inbox], ["accepted", "question", "result"])
        self.assertEqual(len(self.box.poll(recipient="super", after=3)), 1)
        self.assertTrue(self.box.verify_thread(self.thread)["chain_verified"])

    def test_idempotency_conflict(self):
        first = self.send("super-task-001", "super", "task")
        same = self.send("super-task-001", "super", "task")
        self.assertEqual(first["seq"], same["seq"])
        self.assertTrue(same["deduplicated"])
        with self.assertRaisesRegex(Denied, "message_idempotency_conflict"):
            self.send("super-task-001", "super", "task", body={"text": "different"})

    def test_first_message_requires_super_task(self):
        with self.assertRaisesRegex(Denied, "thread_requires_owner_task"):
            self.send("dev-accept-001", "dev", "accepted")
        with self.assertRaisesRegex(Denied, "thread_requires_owner_task"):
            self.send("super-answer-001", "super", "answer")

    def test_role_and_reply_denials(self):
        self.send("super-task-001", "super", "task")
        with self.assertRaisesRegex(Denied, "invalid_actor_or_message_kind"):
            self.send("super-progress-001", "super", "progress", "super-task-001")
        with self.assertRaisesRegex(Denied, "reply_reference_required"):
            self.send("dev-accept-001", "dev", "accepted")
        with self.assertRaisesRegex(Denied, "reply_not_in_thread"):
            self.send("dev-accept-001", "dev", "accepted", "unknown-msg-001")
        with self.assertRaisesRegex(Denied, "reply_must_cross_roles"):
            self.send("super-answer-001", "super", "answer", "super-task-001")
        with self.assertRaisesRegex(Denied, "answer_requires_question"):
            self.send("dev-accept-001", "dev", "accepted", "super-task-001")
            self.send("super-answer-001", "super", "answer", "dev-accept-001")

    def test_terminal_result_closes_thread(self):
        self.send("super-task-001", "super", "task")
        self.send("dev-result-001", "dev", "result", "super-task-001")
        with self.assertRaisesRegex(Denied, "terminal_thread_closed"):
            self.send("super-answer-001", "super", "answer", "dev-result-001")
        with self.assertRaisesRegex(Denied, "terminal_thread_closed"):
            self.send("dev-progress-001", "dev", "progress", "super-task-001")

    def test_bounded_input(self):
        self.send("super-task-001", "super", "task")
        with self.assertRaisesRegex(Denied, "message_size_limit"):
            self.send("dev-progress-001", "dev", "progress", "super-task-001",
                      body={"text": "x" * 17000})
        with self.assertRaisesRegex(Denied, "invalid_message_or_thread_id"):
            self.box.send(message_id="../bad", thread_id=self.thread,
                          sender="dev", kind="progress", body={"text": "bad"},
                          in_reply_to="super-task-001")

    def test_hash_chain_detects_tamper(self):
        self.send("super-task-001", "super", "task")
        self.send("dev-accept-001", "dev", "accepted", "super-task-001")
        self.assertTrue(self.box.verify_thread(self.thread)["chain_verified"])
        self.box.db.execute("UPDATE messages SET body=? WHERE message_id=?",
                            ('{"text":"tampered"}', "dev-accept-001"))
        self.box.db.commit()
        with self.assertRaisesRegex(Denied, "audit_hash_chain_mismatch"):
            self.box.verify_thread(self.thread)

    def test_nonregular_database_path_denied(self):
        path = Path(self.tmp.name) / "directory.sqlite3"
        path.mkdir()
        with self.assertRaisesRegex(Denied, "database_not_regular"):
            Mailbox(path)

    def test_symlink_database_denied(self):
        target = Path(self.tmp.name) / "real.sqlite3"
        link = Path(self.tmp.name) / "link.sqlite3"
        link.symlink_to(target)
        with self.assertRaisesRegex(Denied, "database_symlink_denied"):
            Mailbox(link)


if __name__ == "__main__":
    unittest.main()
