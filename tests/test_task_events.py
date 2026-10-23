"""Regression tests for event-driven, deduplicated task notifications."""
from pathlib import Path
import os
import sqlite3
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"brain"/"automation"))
import task_events as e

class TestTaskEvents(unittest.TestCase):
    def setUp(self):
        self.dir=tempfile.TemporaryDirectory()
        self.db=e.connect(Path(self.dir.name)/"events.sqlite3")
        e.register(self.db,"andaz-01","andaz-website","build",idle_seconds=300,now=1000)
        self.db.commit()
    def tearDown(self):
        self.db.close()
        self.dir.cleanup()
    def count(self,kind):
        return self.db.execute("SELECT COUNT(*) FROM events WHERE kind=?",(kind,)).fetchone()[0]
    def test_register_duplicate_does_not_reset_heartbeat(self):
        x=e.register(self.db,"andaz-01","andaz-website",now=2000)
        self.assertEqual(x["state"],"existing")
        self.assertEqual(self.db.execute("SELECT last_update FROM runs").fetchone()[0],1000)
    def test_initial_complete_emits_one(self):
        x=e.emit(self.db,"andaz-01","completed","qa","17 tests pass",
                 "https://github.com/karanzing1992/andaz-vibe-stay/pull/2",now=1100)
        self.assertEqual(x["kind"],"completed")
        self.assertEqual(self.count("completed"),1)
        self.assertEqual(e.watchdog(self.db,now=9000),[])
        with self.assertRaises(e.EventError):e.emit(self.db,"andaz-01","completed","qa","duplicate")
    def test_stall_watchdog_fires_only_on_timeout(self):
        self.assertEqual(e.watchdog(self.db,now=1299),[])
        self.assertEqual(len(e.watchdog(self.db,now=1300)),1)
        self.assertEqual(self.count("stalled"),1)
        self.assertEqual(e.watchdog(self.db,now=1400),[])
    def test_repeated_stall_escalates_only_once(self):
        e.watchdog(self.db,now=1300)
        e.watchdog(self.db,now=1600)
        e.watchdog(self.db,now=1800)
        self.assertEqual(self.count("stalled"),1)
        self.assertEqual(self.count("escalation"),1)
    def test_resume_clears_stalled(self):
        e.watchdog(self.db,now=1300)
        self.assertEqual(e.heartbeat(self.db,"andaz-01","qa",now=1400)["status"],"running")
        self.assertEqual(self.count("resumed"),1)
        self.assertEqual(e.watchdog(self.db,now=1600),[])
    def test_terminal_blocks_future_events(self):
        e.emit(self.db,"andaz-01","blocked","booking","No public booking endpoint")
        with self.assertRaises(e.EventError):e.heartbeat(self.db,"andaz-01","code")
    def test_unapproved_event_kind(self):
        with self.assertRaises(e.EventError):
            e.emit(self.db,"andaz-01","publish","qa","model requested")
    def test_unknown_run_fails_closed(self):
        with self.assertRaises(e.EventError):
            e.emit(self.db,"not-enrolled","failed","qa","not working")
    def test_duplicate_event_dedup_digest(self):
        e._write_event(self.db,"andaz-01","andaz-website","escalation","security","owner approval needed",now=1100)
        e._write_event(self.db,"andaz-01","andaz-website","escalation","security","owner approval needed",now=1300)
        self.assertEqual(self.count("escalation"),1)
    def test_no_url_no_external_delivery(self):
        e.emit(self.db,"andaz-01","failed","qa","PHP runtime unavailable")
        r=e.dispatch(self.db,environ={})
        self.assertEqual(r["status"],"queued_no_approved_delivery_endpoint")
        self.assertEqual(r["pending"],1)
        self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],0)
    def test_reject_unsafe_url(self):
        for url in ("http://example.com/","file:///etc/passwd",
                    "https://user:pass@example.com/","https://example.com/page#fragment"):
            with self.subTest(url=url):
                with self.assertRaises(e.EventError):
                    e.safe_link(url)
    def test_webhook_rejects_unpinned_host_and_short_secret(self):
        with self.assertRaises(e.EventError):
            e.approved_endpoint({"MATRIX_TASK_NOTIFY_WEBHOOK":"https://events.example.org/hook",
              "MATRIX_TASK_NOTIFY_HOSTS":"other.example.org","MATRIX_TASK_NOTIFY_SECRET":"x"*40})
        with self.assertRaises(e.EventError):
            e.approved_endpoint({"MATRIX_TASK_NOTIFY_WEBHOOK":"https://events.example.org/hook",
              "MATRIX_TASK_NOTIFY_HOSTS":"events.example.org","MATRIX_TASK_NOTIFY_SECRET":"too-short"})
    def test_threshold_bounds(self):
        with self.assertRaises(e.EventError):
            e.register(self.db,"invalid-02","andaz-website","build",idle_seconds=1)
    def test_bounded_summaries(self):
        with self.assertRaises(e.EventError):
            e.emit(self.db,"andaz-01","failed","qa","x"*2000)
    def test_private_mode_file_permissions(self):
        path=Path(self.dir.name)/"events.sqlite3"
        self.assertEqual(path.stat().st_mode&0o777,0o600)
if __name__=="__main__":unittest.main()
