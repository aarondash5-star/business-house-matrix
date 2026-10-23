"""Private webhook: Ed25519 cross-language contract and durable idempotency smoke."""
import base64
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"brain"/"automation"))
import private_telegram_sender as sender
import task_events as events

class MockResponse:
 status=200
 def __init__(self,body):self.body=body
 def __enter__(self):return self
 def __exit__(self,*exc):return False
 def read(self,limit=10000):return json.dumps(self.body).encode()

class MockOpener:
 def __init__(self,response=None,err=False):
  self.calls=[]
  self.response=response
  self.err=err
 def open(self,request,timeout=20):
  self.calls.append(request)
  if self.err:raise TimeoutError("interrupted")
  return MockResponse(self.response)

class TestPrivateSender(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  self.db=events.connect(Path(self.temp.name)/"events.sqlite3")
  events.register(self.db,"dev-matrix-run-100","andaz-website","final-qa",now=1000)
  self.payload=events.emit(self.db,"dev-matrix-run-100","approval_required","final-qa",
      "Independent QA receipts are ready for owner review.",
      "https://github.com/karanzing1992/andaz-vibe-stay/pull/2",now=1100)
  self.db.commit()
  self.key=Ed25519PrivateKey.generate()
 def tearDown(self):
  self.db.close();self.temp.cleanup()
 def test_signatures_match_wordpress_canonical(self):
  body=sender.validated_body(self.payload)
  h=sender.sign_request(body,self.payload["event_id"],int(time.time()),self.key)
  canonical=("bhm-private-relay-v1\n"+h["X-Matrix-Timestamp"]+"\n"+
    h["X-Matrix-Event-ID"]+"\n").encode()+body
  self.key.public_key().verify(base64.b64decode(h["X-Matrix-Signature"]),canonical)
  self.assertEqual(len(base64.b64decode(h["X-Matrix-Signature"])),64)
 def test_signature_changes_on_payload_tampering(self):
  from cryptography.exceptions import InvalidSignature
  data=sender.validated_body(self.payload)
  h=sender.sign_request(data,self.payload["event_id"],1234567890,self.key)
  canonical=("bhm-private-relay-v1\n1234567890\n"+self.payload["event_id"]+"\n").encode()
  with self.assertRaises(InvalidSignature):
   self.key.public_key().verify(base64.b64decode(h["X-Matrix-Signature"]),canonical+data+b"x")
 def test_fixed_endpoint_is_not_community(self):
  self.assertEqual(sender.ENDPOINT,
     "https://mokshagoa.com/wp-json/bhm-private-events/v1/notify")
  self.assertNotIn("telegram/publish",sender.ENDPOINT)
 def test_without_activation_no_outbound_request(self):
  client=MockOpener()
  result=sender.dispatch_once(self.db,None,enabled=False,opener=client)
  self.assertEqual(result["status"],"disabled_until_wordpress_relay_active")
  self.assertEqual(len(client.calls),0)
  self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],0)
 def test_valid_delivery_receipt_and_message_id(self):
  client=MockOpener({"ok":True,"status":"delivered",
    "recipient":"verified_private_booking_chat","event_id":self.payload["event_id"],"message_id":12})
  outcome=sender.dispatch_once(self.db,self.key,enabled=True,opener=client)
  self.assertEqual(outcome["status"],"delivered_confirmed")
  self.assertEqual(outcome["telegram_message_id"],12)
  self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],1)
  self.assertEqual(self.db.execute("SELECT count(*) FROM private_notification_receipts").fetchone()[0],1)
  posted=json.loads(client.calls[0].data)
  self.assertNotIn("chat_id",posted)
  self.assertNotIn("telegram_token",posted)
  self.assertEqual(posted["kind"],"approval_required")
 def test_no_resend_after_success(self):
  client=MockOpener({"ok":True,"status":"delivered",
    "recipient":"verified_private_booking_chat","event_id":self.payload["event_id"],"message_id":12})
  sender.dispatch_once(self.db,self.key,enabled=True,opener=client)
  second=sender.dispatch_once(self.db,self.key,enabled=True,opener=client)
  self.assertEqual(second["status"],"no_pending_events")
  self.assertEqual(len(client.calls),1)
 def test_uncertain_timeout_does_not_auto_retry(self):
  client=MockOpener(err=True)
  result=sender.dispatch_once(self.db,self.key,enabled=True,opener=client)
  self.assertEqual(result["status"],"delivery_uncertain_no_retry")
  self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],2)
  self.assertEqual(sender.dispatch_once(self.db,self.key,enabled=True,opener=client)["status"],"no_pending_events")
  self.assertEqual(len(client.calls),1)
 def test_wrong_recipient_receipt_is_not_delivered(self):
  client=MockOpener({"ok":True,"status":"delivered","recipient":"primary_group",
    "event_id":self.payload["event_id"],"message_id":1785})
  result=sender.dispatch_once(self.db,self.key,enabled=True,opener=client)
  self.assertEqual(result["status"],"delivery_uncertain_no_retry")
  self.assertEqual(self.db.execute("SELECT sent FROM events").fetchone()[0],2)
 def test_wrong_event_id_not_delivered(self):
  client=MockOpener({"ok":True,"status":"delivered",
    "recipient":"verified_private_booking_chat","event_id":"a"*64,"message_id":12})
  result=sender.dispatch_once(self.db,self.key,enabled=True,opener=client)
  self.assertEqual(result["status"],"delivery_uncertain_no_retry")
 def test_no_non_events(self):
  for kind in ("publish","charge","remove_security"):
   with self.assertRaises(events.EventError):
    sender.validated_body({"schema":1,"kind":kind,"event_id":"a"*64,"summary":"example"})
 def test_summary_minimum(self):
  with self.assertRaises(events.EventError):
   sender.validated_body({"schema":1,"kind":"blocked","event_id":"a"*64,"summary":"?"})
 def test_key_file_mode(self):
  from cryptography.hazmat.primitives import serialization
  f=Path(self.temp.name)/"private.pem"
  f.write_bytes(self.key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
  f.chmod(0o644)
  with self.assertRaises(events.EventError):sender.private_key(f)
  f.chmod(0o600)
  self.assertIsInstance(sender.private_key(f),Ed25519PrivateKey)
 def test_stalled_and_escalation_event_kinds(self):
  for kind in ("stalled","escalation","completed","failed","blocked","resumed","approval_required"):
   payload={"schema":1,"kind":kind,"event_id":"a"*64,"summary":"Worker state changed"}
   self.assertIn(kind.encode(),sender.validated_body(payload))
if __name__=="__main__":unittest.main()
