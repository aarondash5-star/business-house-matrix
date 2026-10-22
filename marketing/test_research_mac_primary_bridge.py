"""Mac-first bridge contract; synthetic only, never contacts Dell."""
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import research_engine
import research_mac_primary_bridge as bridge


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "evidence.sqlite3"
        research_engine.connect(self.db).close()
        self.db_override = patch.object(bridge, "DB", self.db)
        self.db_override.start()

    def tearDown(self):
        self.db_override.stop()
        self.tmp.cleanup()

    def test_local_andaz_is_primary_without_any_network(self):
        x = bridge.market("andaz_arambol", "searxng")
        self.assertEqual(x["provider"], "bhm_mac_primary_evidence_v1")
        self.assertEqual(x["report"]["primary_host"], "mac-linux")
        self.assertEqual(x["report"]["search_backend"], "andaz_local_evidence_only")
        self.assertFalse(x["report"]["price_claims_approved"])
        self.assertFalse(x["report"]["publish_approval"])

    def test_local_moksha_survives_signed_dell_unavailable(self):
        module = types.ModuleType("research_market_dell_bridge")
        module.market = lambda *_: (_ for _ in ()).throw(OSError("unavailable"))
        with patch.dict(sys.modules, {"research_market_dell_bridge": module}):
            x = bridge.market("moksha_arambol")
        self.assertEqual(x["report"]["search_backend"], "degraded_local_evidence_only")
        self.assertFalse(x["signed_device_pair_verified"])
        self.assertTrue(x["evidence_primary_mac_verified"])

    def test_signed_dell_is_subordinate_and_never_promotes_prices(self):
        module = types.ModuleType("research_market_dell_bridge")
        module.market = lambda *args: {
            "signed_device_pair_verified": True, "request_id": "synthetic-id",
            "report": {
                "schema": "business_house_matrix.marketing_research.v1.3",
                "topic": "moksha_arambol", "publish_approval": False,
                "approved_for_design_claims": False,
                "pricing_table": [{"price": "999999"}],
                "verified_competitors": [{"name": "made up"}],
                "discovery_queries": [{"status": "retrieved", "sources": []}],
            },
        }
        with patch.dict(sys.modules, {"research_market_dell_bridge": module}):
            x = bridge.market("moksha_arambol", "searxng")
        self.assertEqual(x["report"]["search_backend"], "signed_dell_discovery")
        self.assertTrue(x["signed_device_pair_verified"])
        self.assertEqual(x["report"]["pricing_table"], [])
        self.assertEqual(x["report"]["verified_competitors"], [])

    def test_unsafe_or_untrusted_dell_claim_is_rejected(self):
        module = types.ModuleType("research_market_dell_bridge")
        module.market = lambda *_: {"signed_device_pair_verified": False, "report": {"schema": "wrong"}}
        with patch.dict(sys.modules, {"research_market_dell_bridge": module}):
            x = bridge.market("moksha_arambol")
        self.assertEqual(x["report"]["search_backend"], "degraded_local_evidence_only")
        self.assertFalse(x["publish_approval"])

    def test_missing_mac_db_fails_without_dell_fallback(self):
        with patch.object(bridge, "DB", self.db.with_name("missing.db")):
            with self.assertRaisesRegex(ValueError, "snapshot_missing"):
                bridge.market("moksha_arambol")

    def test_unknown_topics_engines_denied(self):
        for topic, engine in [("unapproved", "searxng"), ("moksha_arambol", "arbitrary")]:
            with self.subTest(topic=topic, engine=engine):
                with self.assertRaisesRegex(ValueError, "public_research_scope_not_granted"):
                    bridge.market(topic, engine)

    def test_stage_b_never_certified_from_local_snapshot(self):
        x = bridge.market("andaz_arambol")
        self.assertFalse(x["report"]["stage_b_certified"])
        self.assertEqual(x["report"]["verified_live_checkout_rates"], 0)
        self.assertFalse(x["report"]["ready_for_design_copy"])


if __name__ == "__main__":
    unittest.main()
