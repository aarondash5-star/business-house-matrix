"""Offline Mac-native research staging regression tests; no host/network access."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import research_engine
import research_mac_local as adapter


class MacLocalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "evidence.sqlite3"

    def tearDown(self):
        self.temp.cleanup()

    def fixture_db(self):
        db = research_engine.connect(self.path)
        db.close()

    def test_missing_private_evidence_does_not_create_database(self):
        result = adapter.describe(self.path, code_dir=Path(__file__).parent)
        self.assertFalse(result["private_evidence_snapshot_present"])
        self.assertFalse(self.path.exists())
        self.assertFalse(result["release_ready"])

    def test_missing_db_rejected_for_packet(self):
        with self.assertRaisesRegex(ValueError, "snapshot_missing"):
            adapter.packet("moksha_arambol", path=self.path)

    def test_zero_size_db_is_rejected(self):
        self.path.touch()
        with self.assertRaisesRegex(ValueError, "empty_snapshot"):
            adapter.packet("moksha_arambol", path=self.path)

    def test_symlink_database_rejected(self):
        self.fixture_db()
        alias = Path(self.temp.name) / "evidence-link.sqlite3"
        alias.symlink_to(self.path)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            adapter.packet("moksha_arambol", path=alias)

    def test_packet_uses_local_sqlite_but_does_not_fetch(self):
        self.fixture_db()
        original_hash = hashlib.sha256(self.path.read_bytes()).hexdigest()
        with patch.object(research_engine, "fetch_extract", side_effect=AssertionError("network")):
            result = adapter.packet("moksha_arambol", path=self.path)
        self.assertEqual(result["compute_target"], "mac-linux")
        self.assertFalse(result["facts_verified"])
        self.assertFalse(result["publish_approval"])
        self.assertFalse(result["spend_approval"])
        self.assertFalse(result["approved_for_design_claims"])
        self.assertFalse(result["stage_b_certified"])
        self.assertEqual(result["source_grants"], [])
        self.assertEqual(original_hash, hashlib.sha256(self.path.read_bytes()).hexdigest())

    def test_andaz_packet_uses_real_brand_constraints_not_moksha(self):
        self.fixture_db()
        result = adapter.packet("andaz_arambol", path=self.path)
        self.assertIn("real Andaz Vibe Stay imagery", result["required_visual_brand_constraints"])
        self.assertNotIn("real Moksha site photography", result["required_visual_brand_constraints"])
        self.assertFalse(result["price_claims_approved"])

    def test_unknown_topic_denied(self):
        with self.assertRaisesRegex(ValueError, "topic_not_granted"):
            adapter.packet("http://example.org/", path=self.path)

    def test_describe_only_fixed_required_modules_and_snapshot_hash(self):
        self.fixture_db()
        result = adapter.describe(self.path, code_dir=Path(__file__).parent)
        self.assertTrue(result["private_evidence_snapshot_present"])
        self.assertEqual(result["snapshot_sha256"], hashlib.sha256(self.path.read_bytes()).hexdigest())
        self.assertEqual(set(result["required_modules_present"]), set(adapter.MODULES))

    def test_policy_does_not_activate_network_or_production(self):
        policy = adapter.describe(self.path)["policy"]
        self.assertFalse(policy["mac_primary_active"])
        self.assertFalse(policy["automated_extraction"])
        self.assertFalse(policy["automated_monitoring"])
        self.assertFalse(policy["publication"])
        self.assertFalse(policy["spending"])
        self.assertEqual(policy["network_source_grants"], [])

    def test_no_arbitrary_path_or_url_arguments_in_cli(self):
        with patch("sys.argv", ["research_mac_local.py", "status", "--url", "https://example.org"]):
            with self.assertRaises(SystemExit) as error:
                adapter.main()
            self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
