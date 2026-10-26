"""Fixture-key tests: no real DEV_BETA key or owner approval is created."""
import base64
from copy import deepcopy
from datetime import datetime,timedelta,timezone
import secrets
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from v4_rebased_release_verify import (
    canonical,parse_payload,verify_detached,verified_release,
    RebasedReleaseDenied,HOST,PROJECT,RELEASE,OLD_PINS,NEW_PINS,KEY_ID
)

REVIEWED_TEST_SHA="a"*40

class TestRebasedReleaseVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key=Ed25519PrivateKey.generate()
        cls.public=cls.key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def setUp(self):
        self.now=datetime(2026,10,27,1,0,tzinfo=timezone.utc)
        self.doc={
            "schema":1,"key_id":KEY_ID,"algorithm":"Ed25519",
            "host":HOST,"project":PROJECT,"release":RELEASE,
            "source_commit":REVIEWED_TEST_SHA,
            "old_pins":deepcopy(OLD_PINS),"new_pins":deepcopy(NEW_PINS),
            "release_id":"v4-controller-20261027-"+secrets.token_hex(16),
            "nonce":secrets.token_hex(16),"issued_utc":self.now.isoformat(),
            "expires_utc":(self.now+timedelta(minutes=4)).isoformat(),
            "production":False,"spend":False,"max_activations":1,
            "qa_receipts":["github:40391381715","dell:a0c34b4e-5a12-47bb-a2c9-7ad280a34887"]
        }

    def encoded(self,**updates):
        d=deepcopy(self.doc);d.update(updates);return canonical(d)

    def sign(self,b):
        return base64.b64encode(self.key.sign(b)).decode("ascii")

    def test_valid_fixture_signature_verifies(self):
        b=self.encoded();d=parse_payload(b,REVIEWED_TEST_SHA,self.now)
        self.assertEqual(d["host"],HOST)
        self.assertTrue(verify_detached(b,self.sign(b),self.public))

    def test_no_actual_review_sha_means_denial(self):
        with self.assertRaisesRegex(RebasedReleaseDenied,"independent_review"):
            parse_payload(self.encoded(),None,self.now)

    def test_must_be_canonical_exact(self):
        with self.assertRaisesRegex(RebasedReleaseDenied,"noncanonical"):
            parse_payload(self.encoded().replace(b":",b": "),REVIEWED_TEST_SHA,self.now)

    def test_any_extra_field_denied(self):
        d={**self.doc,"root":True}
        with self.assertRaisesRegex(RebasedReleaseDenied,"noncanonical"):
            parse_payload(canonical(d),REVIEWED_TEST_SHA,self.now)

    def test_wrong_host_and_cross_project_denied(self):
        for field,val in (("host","mac-linux"),("project","pine_engineer_beta"),
                          ("release","unrestricted"),("source_commit","b"*40)):
            with self.subTest(field=field):
                with self.assertRaisesRegex(RebasedReleaseDenied,"release_scope"):
                    parse_payload(self.encoded(**{field:val}),REVIEWED_TEST_SHA,self.now)

    def test_tampering_all_source_pins_denied(self):
        for name in NEW_PINS:
            with self.subTest(name=name):
                modified=deepcopy(NEW_PINS);modified[name]="0"*64
                with self.assertRaisesRegex(RebasedReleaseDenied,"release_scope"):
                    parse_payload(self.encoded(new_pins=modified),REVIEWED_TEST_SHA,self.now)

    def test_old_live_pin_drift_denied(self):
        old=deepcopy(OLD_PINS);old["controller.py"]="0"*64
        with self.assertRaisesRegex(RebasedReleaseDenied,"release_scope"):
            parse_payload(self.encoded(old_pins=old),REVIEWED_TEST_SHA,self.now)

    def test_production_spend_and_bypass_denied(self):
        for field,val in (("production",True),("spend",True),("max_activations",100)):
            with self.subTest(field=field):
                with self.assertRaisesRegex(RebasedReleaseDenied,"release_scope"):
                    parse_payload(self.encoded(**{field:val}),REVIEWED_TEST_SHA,self.now)

    def test_expiry_late_or_unbounded_denied(self):
        for offset in (-1,6):
            with self.subTest(minutes=offset):
                with self.assertRaisesRegex(RebasedReleaseDenied,"release_expired_or_time_unbounded"):
                    parse_payload(self.encoded(expires_utc=(self.now+timedelta(minutes=offset)).isoformat()),
                                  REVIEWED_TEST_SHA,self.now)

    def test_issued_too_old_or_future_denied(self):
        for minutes in (-6,2):
            with self.subTest(minutes=minutes):
                with self.assertRaisesRegex(RebasedReleaseDenied,"release_expired_or_time_unbounded"):
                    parse_payload(self.encoded(issued_utc=(self.now+timedelta(minutes=minutes)).isoformat()),
                                  REVIEWED_TEST_SHA,self.now)

    def test_wrong_private_key_signature_denied(self):
        b=self.encoded()
        wrong=Ed25519PrivateKey.generate()
        bad=base64.b64encode(wrong.sign(b)).decode()
        with self.assertRaisesRegex(RebasedReleaseDenied,"signature_invalid"):
            verify_detached(b,bad,self.public)

    def test_tampered_approval_denied(self):
        b=self.encoded();signature=self.sign(b)
        alter=self.encoded(release_id="v4-controller-20261027-"+"d"*32)
        with self.assertRaisesRegex(RebasedReleaseDenied,"signature_invalid"):
            verify_detached(alter,signature,self.public)

    def test_invalid_signature_length_denied(self):
        with self.assertRaisesRegex(RebasedReleaseDenied,"invalid_signature_length"):
            verify_detached(self.encoded(),base64.b64encode(b"not-signature").decode(),self.public)

    def test_cryptographic_result_never_auto_activates(self):
        b=self.encoded()
        with patch("v4_rebased_release_verify.owner_trust",return_value=self.public):
            result=verified_release(b,self.sign(b),None,REVIEWED_TEST_SHA,self.now)
        self.assertTrue(result["state"].endswith("_VERIFIED"))
        self.assertFalse(result["can_activate"])
        self.assertFalse(result["production"])
        self.assertFalse(result["spend"])

    def test_missing_qa_receipt_denied(self):
        with self.assertRaisesRegex(RebasedReleaseDenied,"qa_receipts"):
            parse_payload(self.encoded(qa_receipts=[]),REVIEWED_TEST_SHA,self.now)

if __name__=="__main__":
    unittest.main()
