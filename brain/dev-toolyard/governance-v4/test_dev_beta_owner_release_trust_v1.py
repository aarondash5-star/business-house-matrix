"""Fail-closed source policy validation for DEV_BETA Dell/Mac trust (no signer invocation).

This fixture confirms owner-intent is documented without manufacturing a signature.
The private signing key must never appear in this repository, CI, or Dev workers.
"""
import json
from pathlib import Path
import unittest

POLICY = Path(__file__).with_name("dev_beta_owner_release_trust_v1.json")


class DevBetaTrustPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY.read_text("utf-8"))

    def test_owner_identity_is_dev_beta_not_pine_beta(self):
        self.assertEqual(self.policy["key_identifier"], "DEV_BETA_ED25519_PRIVATE_PKCS8_B64")
        self.assertNotEqual(self.policy["key_identifier"], "PINE_BETA_ED25519_PRIVATE_PKCS8_B64")

    def test_no_placeholder_attestation_can_sign(self):
        p = self.policy
        self.assertFalse(p["enabled"])
        self.assertFalse(p["issue_signatures"])
        self.assertFalse(p["allow_host_activation"])
        self.assertFalse(p["signing_endpoint_verified"])
        self.assertFalse(p["signature_test_passed"])
        self.assertFalse(p["host_public_key_trust_installed"])
        self.assertFalse(p["otp_or_link_owner_verified"])

    def test_unknown_public_material_cannot_be_pinned(self):
        p = self.policy
        self.assertIsNone(p["public_key_pem"])
        self.assertIsNone(p["public_key_sha256"])

    def test_exact_hosts_without_expansion(self):
        p = self.policy
        self.assertEqual({h["host_id"] for h in p["hosts"]}, {"dell-linux", "mac-linux"})
        self.assertEqual(len(p["hosts"]), 2)
        for h in p["hosts"]:
            self.assertEqual(h["allowed_project"], "matrix_dev_manager")
            self.assertFalse(h["production"])
            self.assertTrue(h["authenticated_approval_required"])
            self.assertTrue(h["requires_independent_rollback"])

    def test_no_cross_project_authorization(self):
        deny = set(self.policy["forbidden_projects"])
        self.assertTrue({"pine_engineer_beta", "staycore", "ashwakaal_support_channels"} <= deny)

    def test_limited_time_and_one_time_replay(self):
        p = self.policy
        self.assertLessEqual(p["expires_after_minutes"], 5)
        self.assertIn("one_time", p["replay_policy"])

    def test_secret_never_stored_in_policy(self):
        p = self.policy
        self.assertTrue(p["private_key_must_remain_server_side"])
        self.assertEqual(p["key_storage"], "supabase_edge_secret_owner_controlled")
        self.assertNotIn("private_key", p)
        self.assertNotIn("secret_value", p)

    def test_mac_is_not_inferred_running_dell_controller(self):
        hosts = {h["host_id"]: h for h in self.policy["hosts"]}
        self.assertNotEqual(hosts["mac-linux"]["release"], hosts["dell-linux"]["release"])
        self.assertIn("separately_manifested", hosts["mac-linux"]["release"])


if __name__ == "__main__":
    unittest.main()
