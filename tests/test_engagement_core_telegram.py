"""Private Engagement Core Telegram delivery tests, no external network or messages."""
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"brain"/"automation"))
import task_events as e
import engagement_core_telegram as tg

PRIVATE_ID="123456789"
def bot_status():
    return {"connected":True,"destinations":[
       {"key":"primary","enabled":True,"chat_id":"-1001827799147"},
       {"key":"moksha","enabled":True,"chat_id":"@mokshasauna"},
       {"key":"owner_private","enabled":True,"chat_id":PRIVATE_ID}]}

class TelegramTest(unittest.TestCase):
    def setUp(self):
        self.d=tempfile.TemporaryDirectory()
        self.db=e.connect(Path(self.d.name)/"notify.sqlite3")
        e.register(self.db,"andaz-build-23","andaz-build","qa",now=1000)
        e.emit(self.db,"andaz-build-23","approval_required","qa",
            "Ready for owner review",url="https://github.com/karanzing1992/andaz-vibe-stay/pull/2",now=1100)
        self.db.commit()
    def tearDown(self):
        self.db.close()
        self.d.cleanup()
    def test_target_is_exact_owner_private(self):
        self.assertTrue(tg.allow_target(bot_status(),PRIVATE_ID))
        with self.assertRaises(tg.DeliveryError):
            tg.allow_target(bot_status(),"-1001827799147")
        with self.assertRaises(tg.DeliveryError):
            tg.allow_target(bot_status(),"987654321")
    def test_missing_owner_private_fails_closed(self):
        s=bot_status()
        s["destinations"]=s["destinations"][:2]
        with self.assertRaises(tg.DeliveryError):
            tg.allow_target(s,PRIVATE_ID)
    def test_no_empty_targets_or_levels(self):
        conf={"chat_id":PRIVATE_ID,"key":"FAKE_TEST_KEY_NO_NETWORK"}
        calls=[]
        def mocked(req,opener=None):
            calls.append(req)
            if req.get_method()=="GET":return bot_status()
            request=json.loads(req.data)
            self.assertEqual(request["targets"],["owner_private"])
            self.assertNotIn("levels",request)
            self.assertNotIn("media",request)
            self.assertIn("Andaz",request["text"].replace("andaz","Andaz"))
            return {"ok":True,"sent":[{"key":"owner_private",
                     "chat_id":PRIVATE_ID,"message_ids":[190]}],"failed":[]}
        with mock.patch.object(tg,"_http",side_effect=mocked):
            result=tg.send_once(self.db,conf)
        self.assertEqual(result["status"],"delivered_confirmed")
        self.assertEqual(len(calls),2)
        self.assertIn("X-grec-publish-key".lower(),
            {k.lower() for k in calls[1].headers})
        self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],1)
    def test_no_auto_retry_on_uncertain(self):
        def uncertain(req,opener=None):
            if req.get_method()=="GET":return bot_status()
            raise TimeoutError("uncertain-network-write")
        with mock.patch.object(tg,"_http",side_effect=uncertain):
            result=tg.send_once(self.db,{"chat_id":PRIVATE_ID,"key":"FAKE"})
            self.assertEqual(result["status"],"delivery_uncertain_manual_reconcile")
            self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],2)
            second=tg.send_once(self.db,{"chat_id":PRIVATE_ID,"key":"FAKE"})
            self.assertEqual(second["status"],"no_pending_events")
    def test_wrong_delivery_receipt_stays_uncertain(self):
        def wrong(req,opener=None):
            if req.get_method()=="GET":return bot_status()
            return {"ok":True,"sent":[{"key":"primary","chat_id":"-1001827799147",
                  "message_ids":[200]}],"failed":[]}
        with mock.patch.object(tg,"_http",side_effect=wrong):
            answer=tg.send_once(self.db,{"chat_id":PRIVATE_ID,"key":"FAKE"})
            self.assertEqual(answer["status"],"delivery_uncertain_manual_reconcile")
    def test_no_approved_key_fails_closed(self):
        with self.assertRaises(tg.DeliveryError):
            tg.load_config({})
    def test_approval_message_contains_link(self):
        row=self.db.execute("SELECT payload FROM events").fetchone()
        txt=tg.render(json.loads(row["payload"]))
        self.assertIn("approval",txt.lower())
        self.assertIn("/pull/2",txt)
    def test_sensitive_payload_blocked(self):
        with self.assertRaises(tg.DeliveryError):
            tg.render({"kind":"failed","summary":"api_key=abcd","stage":"qa"})
    def test_negative_group_id_rejected(self):
        with self.assertRaises(tg.DeliveryError):
            tg.load_config({"MATRIX_OWNER_TG_CHAT_ID":"-1001827799147",
               "MATRIX_GREC_KEY_FILE":"/tmp/missing"})
    def test_requires_0600_file(self):
        file=Path(self.d.name)/"key"
        file.write_text("x"*32)
        file.chmod(0o644)
        with self.assertRaises(tg.DeliveryError):
            tg.load_config({"MATRIX_OWNER_TG_CHAT_ID":PRIVATE_ID,
                "MATRIX_GREC_KEY_FILE":str(file)})
    def test_status_only_no_credentials(self):
        self.assertNotIn("bot",tg.PUBLISH_URL)
        self.assertEqual(tg.TARGET,"owner_private")
if __name__=="__main__":unittest.main()
