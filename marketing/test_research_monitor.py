#!/usr/bin/env python3
import datetime as dt
import tempfile
import unittest
from unittest.mock import Mock
import research_engine as e
import research_monitor as m
GRANTS={"example.org"}
def conf(**kw):return {"targets":[{"url":"https://example.org/sauna","role":"confirmed_provider","reviewed_by_owner":True,**kw}]}
class MonitorTests(unittest.TestCase):
    def test_reviewed_plan(self):
        self.assertEqual(m.validate_targets(conf(),GRANTS),["https://example.org/sauna"])
    def test_unreviewed_rejected(self):
        with self.assertRaises(ValueError):m.validate_targets({"targets":[{"url":"https://example.org/","role":"confirmed_provider"}]},GRANTS)
    def test_ungranted_rejected(self):
        with self.assertRaises(ValueError):m.validate_targets({"targets":[{"url":"https://internal.test/","role":"confirmed_provider","reviewed_by_owner":True}]},GRANTS)
    def test_not_provider_rejected(self):
        with self.assertRaises(ValueError):m.validate_targets(conf(role="directory"),GRANTS)
    def test_dedup(self):
        p=conf();p["targets"].append(dict(p["targets"][0]))
        self.assertEqual(len(m.validate_targets(p,GRANTS)),1)
    def test_many_targets(self):
        with self.assertRaises(ValueError):m.validate_targets({"targets":[{"url":f"https://example.org/{i}","role":"confirmed_provider","reviewed_by_owner":True} for i in range(13)]},GRANTS)
    def test_dry_run_never_fetches(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=e.connect(tmp+"/x.sqlite");fetcher=Mock()
            r=m.monitor_once(db,conf(),GRANTS,fetcher=fetcher,dry_run=True)
            fetcher.assert_not_called()
            self.assertFalse(r["automatic_notifications"])
            self.assertFalse(r["publish_approval"])
            db.close()
    def test_failure_is_unavailable_not_notification(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=e.connect(tmp+"/x.sqlite")
            r=m.monitor_once(db,conf(),GRANTS,fetcher=lambda *args:{"status":"unavailable","reason":"robots_denied"},dry_run=False)
            self.assertEqual(r["checked"][0]["status"],"unavailable")
            self.assertFalse(r["automatic_notifications"])
            db.close()
    def test_recent_fetch_defers(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=e.connect(tmp+"/x.sqlite")
            e.record_attempt(db,"https://example.org/sauna","ok")
            fetcher=Mock()
            r=m.monitor_once(db,conf(),GRANTS,fetcher=fetcher,dry_run=False)
            self.assertEqual(r["checked"][0]["status"],"deferred_cooldown")
            fetcher.assert_not_called()
            db.close()
if __name__=="__main__":unittest.main(verbosity=2)
