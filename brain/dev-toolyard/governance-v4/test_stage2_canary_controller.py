"""Stage2 one-shot V4 controller unit tests; no execution of real worker."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

# The Stage 2 one-shot unit suite is designed for a pinned, isolated Dell
# release workcell. Git source alone deliberately does not contain the
# installed adapter/guard aliases or the private QA standard. Never silently
# substitute a different executable adapter in repository-wide pytest.
import importlib.util
if importlib.util.find_spec("adapter_guard_v4") is None or importlib.util.find_spec("yard_auto_adapter_v1") is None:
    try:
        import pytest
    except ImportError:
        raise RuntimeError("Run these tests only with the pinned V4 installed-workcell fixtures")
    pytest.skip("requires actual installed Stage 2 V4 workcell fixtures; separate verified Dell QA receipt", allow_module_level=True)

import v4_stage2_canary_controller as c


class CanaryUnitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state=Path(self.tmp.name)/"canary"
        self.state.mkdir(mode=0o700)
        self.old=c.STATE
        c.STATE=self.state
        self.addCleanup(lambda: setattr(c,"STATE",self.old))

    def test_literal_owner_scope(self):
        self.assertEqual(c.admission()["project"],"matrix_dev_manager")

    def test_other_project_denied(self):
        with self.assertRaises(c.AdmissionDenied):
            c.admission(project="pine_mcp_chat")

    def test_other_manifest_denied(self):
        with self.assertRaises(c.AdmissionDenied):
            c.admission(manifest="any_other_manifest")

    def test_arbitrary_action_denied(self):
        with self.assertRaises(c.AdmissionDenied):
            c.admission(action="arbitrary_shell")

    def test_other_tool_denied(self):
        with self.assertRaises(c.AdmissionDenied):
            c.admission(tool="git")

    def test_production_denied(self):
        with self.assertRaises(c.AdmissionDenied):
            c.admission(production=True)

    def test_spend_denied(self):
        with self.assertRaises(c.AdmissionDenied):
            c.admission(spend=True)

    def test_first_reservation(self):
        db=c.store()
        try:
            disposition,payload=c.register_once(db)
            self.assertEqual(disposition,"reserved")
            self.assertIsNone(payload)
            row=db.execute("SELECT * FROM jobs WHERE task_id=?",(c.TASK_ID,)).fetchone()
            self.assertEqual(row["attempts"],1)
            self.assertEqual(row["status"],"reserved")
        finally:
            db.close()

    def test_pending_crash_never_replayed(self):
        db=c.store()
        try:
            c.register_once(db)
        finally:
            db.close()
        reopened=c.store()
        try:
            with self.assertRaisesRegex(c.AdmissionDenied,"do_not_replay"):
                c.register_once(reopened)
            self.assertEqual(
                reopened.execute("SELECT COUNT(*) FROM jobs").fetchone()[0],1)
        finally:
            reopened.close()

    def test_completed_deduplicated_without_execution(self):
        db=c.store()
        try:
            c.register_once(db)
            receipt={"status":"completed","task_id":c.TASK_ID,"production":False}
            db.execute("UPDATE jobs SET status='completed',receipt_json=? WHERE task_id=?",
                       (json.dumps(receipt),c.TASK_ID))
            disposition,old=c.register_once(db)
            self.assertEqual(disposition,"deduplicated")
            self.assertEqual(old,receipt)
            self.assertEqual(db.execute("SELECT attempts FROM jobs").fetchone()[0],1)
        finally:
            db.close()

    def test_corrupted_terminal_receipt_denied(self):
        db=c.store()
        try:
            c.register_once(db)
            db.execute("UPDATE jobs SET status='completed',receipt_json=? WHERE task_id=?",
                       (json.dumps({"status":"blocked","task_id":c.TASK_ID}),c.TASK_ID))
            with self.assertRaises(c.AdmissionDenied):
                c.register_once(db)
        finally:
            db.close()

    def test_symlink_state_denied(self):
        db=c.store()
        db.close()
        (self.state/"stage2-canary.sqlite3").unlink()
        (self.state/"stage2-canary.sqlite3").symlink_to(Path(self.tmp.name)/"unused")
        with self.assertRaises(c.AdmissionDenied):
            c.store()

    def test_no_exception_can_replay_reserved(self):
        db=c.store()
        try:
            c.register_once(db)
            db.execute("UPDATE jobs SET status='blocked' WHERE task_id=?",(c.TASK_ID,))
            with self.assertRaises(c.AdmissionDenied):
                c.register_once(db)
        finally:db.close()

    def test_sha256_is_deterministic(self):
        p=self.state/"canary.bin";p.write_bytes(b"canary")
        self.assertEqual(len(c.sha(p)),64)
        self.assertEqual(c.sha(p),c.sha(p))

if __name__=="__main__":
    unittest.main()
