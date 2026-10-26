"""Fixed-purpose independent owner trust: non-root/incorrect-key negative QA."""
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from owner_native_public_trust_enroll import (
    validate_public_pem,enroll_from_verified_stdin,TrustEnrollmentDenied,
    EXPECTED_PEM_SHA256, TRUST_PATH
)

PEM=(b"-----BEGIN PUBLIC KEY-----\n"
     b"MCowBQYDK2VwAyEAqKeblk/QLUfkDouPOhJSNV1InnH06lYY8esP8JYDMTE=\n"
     b"-----END PUBLIC KEY-----\n")

class TestNativeOwnerPublicTrust(unittest.TestCase):
    def test_exact_public_key_and_fingerprint(self):
        self.assertEqual(validate_public_pem(PEM),EXPECTED_PEM_SHA256)
        self.assertEqual(hashlib.sha256(PEM).hexdigest(),EXPECTED_PEM_SHA256)

    def test_public_key_only_not_private_key(self):
        self.assertNotIn(b"PRIVATE "+b"KEY",PEM)

    def test_invalid_public_rejected(self):
        variants=[
            b"",PEM[:-1],PEM.replace(b"\n",b"\r\n"),
            PEM.replace(b"InnH",b"lnnH"),PEM+b"more",
            b"-----BEGIN "+b"PRIVATE "+b"KEY-----\\n"+PEM,
            b"x"*513
        ]
        for altered in variants:
            with self.subTest(altered=altered[:30]):
                with self.assertRaises(TrustEnrollmentDenied):
                    validate_public_pem(altered)

    def test_non_root_cannot_install_to_system(self):
        with patch("owner_native_public_trust_enroll.os.geteuid",return_value=1001):
            with self.assertRaisesRegex(TrustEnrollmentDenied,"independent_admin_root_required"):
                enroll_from_verified_stdin(PEM)

    def test_any_path_override_is_denied(self):
        with patch("owner_native_public_trust_enroll.os.geteuid",return_value=0):
            with self.assertRaisesRegex(TrustEnrollmentDenied,"target_override_denied"):
                enroll_from_verified_stdin(PEM,Path("/tmp/untrusted.pem"))

    def test_native_root_path_exact(self):
        self.assertEqual(str(TRUST_PATH),"/etc/matrix-internal-release/dev_beta_owner_public.pem")

    def test_no_shell_or_restart_api(self):
        s=Path(__file__).with_name("owner_native_public_trust_enroll.py").read_text()
        for unsafe in ("subprocess", "systemctl", "ssh ", "sudo ", "os.system(",
                       "password", "privateKey"):
            self.assertNotIn(unsafe,s)
        
if __name__=="__main__":
    unittest.main()
