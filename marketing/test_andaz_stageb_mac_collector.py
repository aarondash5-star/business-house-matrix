"""Synthetic tests for fixed read-only Mac attestation collection."""
import base64
import datetime as dt
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import andaz_stageb_mac_collector as m
import andaz_stageb_fixed_attestation as v

NOW = dt.datetime(2026, 10, 23, 2, 0, tzinfo=dt.timezone.utc)
NONCE = "AQ8w98R_4XbylH8nVcxTT2GBAAA"

class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.files = {label:Path(self.tmp.name) / str(i) for i,label in enumerate(m.ARTIFACTS)}
        for f in self.files.values(): f.write_text("safe-source-fixture")
        self.pk = Ed25519PrivateKey.generate()
        self.pub = base64.b64encode(self.pk.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)).decode()
        self.paths = patch.object(m, "ARTIFACTS", self.files)
        self.exec = patch.object(m, "_fixed_exec", side_effect=["active", '{"publish_enabled":false,"spend_enabled":false}'])
        self.paths.start()
        self.mock_exec = self.exec.start()
    def tearDown(self):
        self.exec.stop()
        self.paths.stop()
        self.tmp.cleanup()
    def make(self):
        return m.collect_fixed_attestation(NONCE, self.pk.sign, clock=lambda:NOW)
    def test_full_signature_roundtrip_existing_verifier(self):
        r=v.verify(self.make(), self.pub, expected_nonce=NONCE, now=NOW)
        self.assertEqual(r["status"],"preflight_evidence_only")
        self.assertFalse(r["extract_allowed"])
        self.assertEqual(self.mock_exec.call_count,2)
        self.assertEqual(self.mock_exec.call_args_list[0].args[0], ["systemctl", "--user", "is-active", m.TIMER])
    def test_wrong_nonce(self):
        with self.assertRaisesRegex(ValueError,"invalid_nonce"):
            m.collect_fixed_attestation("short",self.pk.sign)
        self.mock_exec.assert_not_called()
    def test_shell_metacharacters_are_not_allowed_as_nonce(self):
        with self.assertRaisesRegex(ValueError,"invalid_nonce"):
            m.collect_fixed_attestation("A" * 24 + ";echo forbidden", self.pk.sign)
        self.mock_exec.assert_not_called()
    def test_requires_authenticated_signer(self):
        with self.assertRaisesRegex(ValueError,"authenticated_signer_required"):
            m.collect_fixed_attestation(NONCE,None)
    def test_inactive_unit(self):
        self.mock_exec.side_effect=["inactive", "{}"]
        with self.assertRaisesRegex(ValueError,"brain_timer_not_active"):self.make()
    def test_brain_flags_missing(self):
        self.mock_exec.side_effect=["active", "{}"]
        with self.assertRaisesRegex(ValueError,"brain_flags_missing"):self.make()
    def test_spend_true(self):
        self.mock_exec.side_effect=["active", '{"publish_enabled":false,"spend_enabled":true}']
        with self.assertRaisesRegex(ValueError,"unsafe_brain_flags"):self.make()
    def test_nonboolean_flag_rejected(self):
        self.mock_exec.side_effect=["active", '{"publish_enabled":"false","spend_enabled":false}']
        with self.assertRaisesRegex(ValueError,"invalid_brain_flag_type"):self.make()
    def test_extra_activated_transport_marker(self):
        self.files["matrix-research-transport/transport.py"].write_bytes(m.GATE_MARKER)
        with self.assertRaisesRegex(ValueError,"extraction_gate_already_active"):self.make()
    def test_symlink_source_rejected(self):
        self.files["searxng_research.py"].unlink()
        self.files["searxng_research.py"].symlink_to(self.files["marketing_report_orchestrator.py"])
        with self.assertRaises(OSError):self.make()
    def test_missing_source_rejected(self):
        self.files["searxng_research.py"].unlink()
        with self.assertRaises(FileNotFoundError):self.make()
    def test_signer_must_return_signature_bytes(self):
        with self.assertRaisesRegex(ValueError,"invalid_signer_signature"):
            m.collect_fixed_attestation(NONCE,lambda _: b"bad",clock=lambda:NOW)
    def test_unbound_signer_fails_verification(self):
        bogus = Ed25519PrivateKey.generate()
        proof = m.collect_fixed_attestation(NONCE,bogus.sign,clock=lambda:NOW)
        with self.assertRaisesRegex(ValueError,"attestation_signature_invalid"):
            v.verify(proof,self.pub,expected_nonce=NONCE,now=NOW)
    def test_missing_timezone(self):
        with self.assertRaisesRegex(ValueError,"timezone_required"):
            m.collect_fixed_attestation(NONCE,self.pk.sign,clock=lambda:NOW.replace(tzinfo=None))

if __name__ == "__main__": unittest.main()
