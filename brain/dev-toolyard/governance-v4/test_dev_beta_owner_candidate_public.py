"""Canonical public Ed25519 release-candidate evidence only. Does not sign or deploy."""
import base64
import hashlib
from pathlib import Path
import re
import unittest

HERE=Path(__file__).parent
PUBLIC=HERE/"dev_beta_owner_candidate_public.pem"
EXPECTED_SHA256="1eee3d266eb1d362b9c7f36d0301b831a8a527828682505ff286d2738606eec1"
DER_PREFIX=bytes.fromhex("302a300506032b6570032100")

class OwnerCandidatePublicKeyTests(unittest.TestCase):
    def test_owner_provided_pem_hash_exact(self):
        data=PUBLIC.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),EXPECTED_SHA256)

    def test_canonical_lf_terminated_pem(self):
        blob=PUBLIC.read_bytes()
        self.assertFalse(b"\r" in blob)
        self.assertTrue(blob.endswith(b"\n"))
        self.assertRegex(blob.decode("ascii"),
            r"\A-----BEGIN PUBLIC KEY-----\n[A-Za-z0-9+/]{59}=\n-----END PUBLIC KEY-----\n\Z")

    def test_valid_ed25519_spki_encoding(self):
        data=PUBLIC.read_text("ascii")
        der=base64.b64decode(data.splitlines()[1],validate=True)
        self.assertEqual(len(der),44)
        self.assertEqual(der[:12],DER_PREFIX)
        self.assertEqual(len(der[12:]),32)

    def test_not_a_private_key(self):
        self.assertNotIn(b"PRIVATE KEY",PUBLIC.read_bytes())

if __name__=="__main__":
    unittest.main()
