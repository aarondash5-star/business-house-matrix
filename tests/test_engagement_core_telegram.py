"""Fail-closed regression after an unauthorized Primary-group routing assumption."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"brain"/"automation"))
import task_events as events
import engagement_core_telegram as tg

class TestUnenrolledDestination(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.db=events.connect(Path(self.tmp.name)/"events.sqlite3")
  events.register(self.db,"andaz-run-1","andaz-dev","qa",now=1000)
  events.emit(self.db,"andaz-run-1","approval_required","qa",
              "Andaz requires final owner review",
              "https://github.com/karanzing1992/andaz-vibe-stay/pull/2",now=1100)
  self.db.commit()
 def tearDown(self):
  self.db.close()
  self.tmp.cleanup()
 def test_wrong_group_never_selected(self):
  self.assertNotEqual(tg.TARGET,"primary")
  self.assertNotEqual(tg.TARGET,"moksha")
  self.assertNotEqual(tg.TARGET,"andaz")
  self.assertNotEqual(tg.TARGET,"exclusiv")
  self.assertIn("primary",tg.BLOCKED_KEYS)
  self.assertIn("-1001827799147",tg.BLOCKED_CHAT_IDS)
 def test_disabled_until_owner_confirms_group(self):
  with self.assertRaisesRegex(tg.DeliveryError,"DESTINATION_NOT_VERIFIED_BY_OWNER"):
   tg.load_config({"MATRIX_OWNER_TG_GROUP_ID":"-1001827799147",
       "MATRIX_GREC_KEY_FILE":"/tmp/should-not-be-accessed"})
 def test_cannot_preflight_wrong_group(self):
  with self.assertRaisesRegex(tg.DeliveryError,"DESTINATION_NOT_VERIFIED_BY_OWNER"):
   tg.allow_target({"connected":True,"destinations":[
    {"key":"primary","chat_id":"-1001827799147","enabled":True}]},
    "-1001827799147")
 def test_no_http_request_until_destination_verified(self):
  with patch.object(tg,"_http") as network:
   with self.assertRaises(tg.DeliveryError):
    tg.send_once(self.db,{"chat_id":"-1001827799147","key":"test"})
   network.assert_not_called()
  self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],0)
 def test_render_preserves_evidence(self):
  payload=json.loads(self.db.execute("SELECT payload FROM events").fetchone()[0])
  txt=tg.render(payload)
  self.assertIn("Andaz",txt)
  self.assertIn("/pull/2",txt)
 def test_render_sensitive_token_blocked(self):
  with self.assertRaises(tg.DeliveryError):
   tg.render({"kind":"failed","summary":"api_key=abc"})
 def test_delivery_ack_requires_exact_target(self):
  self.assertFalse(tg.accepted_delivery({"ok":True,"sent":[
   {"key":"primary","chat_id":"-1001827799147","message_ids":[1785]}],"failed":[]},
   "-1001827799147"))
 def test_outbox_stays_private(self):
  self.assertEqual((Path(self.tmp.name)/"events.sqlite3").stat().st_mode&0o777,0o600)

if __name__=="__main__":unittest.main()
