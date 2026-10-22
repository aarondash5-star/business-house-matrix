"""Offline-only tests: no Mac SSH, website access or production activity."""
import base64
import datetime as dt
import copy
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import andaz_stageb_fixed_attestation as m

NOW = dt.datetime(2026, 10, 23, 2, 0, tzinfo=dt.timezone.utc)
NONCE = "AQ8w98R_4XbylH8nVcxTT2GBAAA"

class StageBFixedAttestationTests(unittest.TestCase):
    def setUp(self):
        self.private = Ed25519PrivateKey.generate()
        self.pub = base64.b64encode(self.private.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)).decode()
        self.payload = {
            "schema": "bhm.mac.fixed_preflight.v1",
            "host_id": "mac-linux",
            "observed_utc": (NOW - dt.timedelta(seconds=10)).isoformat(),
            "units": {"bhm-marketing-queue-worker.timer": "active"},
            "artifacts": {k:"a"*64 for k in m.REQUIRED_ARTIFACTS},
            "extract_gate_active": False,
            "publish_enabled": False,
            "spend_enabled": False,
            "preflight_nonce": NONCE,
        }
    def sign(self, payload=None):
        p=copy.deepcopy(payload or self.payload)
        return {"payload":p,"signature":base64.b64encode(self.private.sign(m.CONTEXT+m.canonical(p))).decode()}
    def assertRejected(self, payload, message):
        with self.assertRaisesRegex(ValueError, message):
            m.verify(self.sign(payload), self.pub, expected_nonce=NONCE, now=NOW)
    def test_good_signed_preflight_is_never_extraction_approval(self):
        result=m.verify(self.sign(), self.pub, expected_nonce=NONCE, now=NOW)
        self.assertTrue(result["verified_transport_identity"])
        for name in ("stage_b_certified","source_permissions_granted","extract_allowed","publish_allowed"):
            self.assertFalse(result[name])
    def test_tampered_signature(self):
        proof=self.sign()
        proof["payload"]["artifacts"]["searxng_research.py"]="b"*64
        with self.assertRaisesRegex(ValueError,"attestation_signature_invalid"):
            m.verify(proof,self.pub,expected_nonce=NONCE,now=NOW)
    def test_unpinned_key_rejected(self):
        untrusted=Ed25519PrivateKey.generate().public_key()
        other=base64.b64encode(untrusted.public_bytes(Encoding.Raw,PublicFormat.Raw)).decode()
        with self.assertRaisesRegex(ValueError,"attestation_signature_invalid"):
            m.verify(self.sign(),other,expected_nonce=NONCE,now=NOW)
    def test_wrong_host(self):
        p=copy.deepcopy(self.payload);p["host_id"]="dell-linux"
        self.assertRejected(p,"wrong_host_or_schema")
    def test_wrong_nonce(self):
        with self.assertRaisesRegex(ValueError,"nonce_not_bound"):
            m.verify(self.sign(),self.pub,expected_nonce="abcdef012345678901234567",now=NOW)
    def test_stale_attestation(self):
        p=copy.deepcopy(self.payload);p["observed_utc"]=(NOW-dt.timedelta(minutes=6)).isoformat()
        self.assertRejected(p,"expired_or_future_attestation")
    def test_future_attestation(self):
        p=copy.deepcopy(self.payload);p["observed_utc"]=(NOW+dt.timedelta(minutes=1)).isoformat()
        self.assertRejected(p,"expired_or_future_attestation")
    def test_inactive_timer(self):
        p=copy.deepcopy(self.payload);p["units"]["bhm-marketing-queue-worker.timer"]="inactive"
        self.assertRejected(p,"required_unit_not_active")
    def test_shell_and_extra_labels_denied(self):
        p=copy.deepcopy(self.payload);p["artifacts"]["/etc/shadow"]="a"*64
        self.assertRejected(p,"unexpected_artifact_labels")
    def test_secrets_never_part_of_contract(self):
        p=copy.deepcopy(self.payload);p["credentials"]="secret"
        self.assertRejected(p,"bad_attestation_schema")
    def test_extract_active_denied(self):
        p=copy.deepcopy(self.payload);p["extract_gate_active"]=True
        self.assertRejected(p,"extraction_already_active")
    def test_marketing_write_flags_denied(self):
        for key in ("publish_enabled","spend_enabled"):
            p=copy.deepcopy(self.payload);p[key]=True
            self.assertRejected(p,"unsafe_marketing_flags")
    def test_invalid_sha(self):
        p=copy.deepcopy(self.payload);p["artifacts"]["searxng_research.py"]="missing"
        self.assertRejected(p,"invalid_artifact_digest")
    def test_bad_envelope(self):
        with self.assertRaisesRegex(ValueError,"bad_attestation_envelope"):
            m.verify({"payload":self.payload,"signature":"bad","extra":"x"},self.pub,expected_nonce=NONCE,now=NOW)

if __name__ == "__main__": unittest.main()
