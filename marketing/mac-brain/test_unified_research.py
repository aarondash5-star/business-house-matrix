#!/usr/bin/env python3
"""No-network, no-paid regression suite for evidence-separated research."""
import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import brain
import gsc_metrics
import searxng_research
import trends
import unified_research


class UnifiedResearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="bhm-unified-")
        self.root = Path(self.tmp.name)
        self.patches = [
            patch.object(gsc_metrics, "DB", self.root / "gsc.sqlite3"),
            patch.object(gsc_metrics, "INBOX", self.root / "gsc-inbox"),
            patch.object(gsc_metrics, "SECRETS", self.root / "no-credentials.json"),
            patch.object(trends, "DATABASE", self.root / "trends.sqlite3"),
        ]
        for p in self.patches:
            p.start()
        gsc_metrics.INBOX.mkdir(mode=0o700)
        self.site = "sc-domain:example.org"

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.tmp.cleanup()

    def web(self, query):
        return {"provider": "searxng", "mode": "self_hosted_encrypted_paired_relay",
                "device_peer_verified": True, "request_id": "signed-probe",
                "results": [{"title": "Sauna destination", "url": "https://example.org/sauna",
                             "snippet": "Untrusted content", "engine": "brave"}],
                "citations_required": True}

    def test_no_gsc_is_explicit_missing_not_zero_demand(self):
        with patch.object(searxng_research, "search", side_effect=self.web):
            report = unified_research.collect("sauna wellness Goa")
        self.assertEqual(report["web_research"]["status"], "observed")
        self.assertEqual(report["verified_property_performance"]["status"], "property_not_selected")
        self.assertFalse(report["gsc_connection"]["connected_evidence"])
        self.assertTrue(report["research_policy"]["gsc_no_data_means_unknown"])
        self.assertTrue(report["research_policy"]["external_content_untrusted"])
        self.assertFalse(report["research_policy"]["paid_fallback"])

    def test_web_failure_never_invents_search_results(self):
        with patch.object(searxng_research, "search", side_effect=RuntimeError("secret-should-not-leak")):
            report = unified_research.collect("sauna wellness Goa")
        self.assertEqual(report["web_research"]["status"], "unavailable")
        self.assertEqual(report["web_research"]["results"], [])
        self.assertNotIn("secret-should-not-leak", json.dumps(report))

    def test_unverified_signature_discards_results(self):
        def fake(query):
            obj = self.web(query)
            obj["device_peer_verified"] = False
            return obj
        with patch.object(searxng_research, "search", side_effect=fake):
            report = unified_research.collect("sauna wellness Goa")
        self.assertEqual(report["web_research"]["status"], "unavailable")
        self.assertEqual(report["web_research"]["results"], [])

    def test_gsc_csv_is_property_scoped_and_private(self):
        csv_name = gsc_metrics.INBOX / "performance.csv"
        with csv_name.open("w") as f:
            w = csv.writer(f); w.writerow(["Query","Clicks","Impressions","CTR","Position"])
            w.writerow(["wood fired sauna Goa", 12, 400, "3%", "8.5"])
            w.writerow(["sauna booking someone@example.org", 20, 100, "20%", "3"])
            w.writerow(["irrelevant unrelated keyword", 5, 200, "2.5%", "20"])
        result = gsc_metrics.import_csv("performance.csv", self.site, "2026-09-01", "2026-09-28")
        self.assertEqual(result["rows"], 2)
        with patch.object(searxng_research, "search", side_effect=self.web):
            report = unified_research.collect("sauna Goa", site=self.site)
        data = report["verified_property_performance"]
        self.assertEqual(data["status"], "observed")
        self.assertEqual(len(data["rows"]), 1)
        self.assertEqual(data["rows"][0]["impressions"], 400)
        self.assertAlmostEqual(data["rows"][0]["ctr"], 0.03)
        self.assertTrue(report["gsc_connection"]["connected_evidence"])
        self.assertNotIn("someone@example.org", json.dumps(report))
        self.assertEqual(gsc_metrics.relevant("sauna",site="sc-domain:another.org")["status"],"no_property_data")

    def test_source_confidence_is_separate(self):
        with patch.object(searxng_research, "search", side_effect=self.web):
            r = unified_research.collect("sauna Goa")
        self.assertIn("national news", r["trending_topics"]["scope"])
        self.assertTrue(r["research_policy"]["trends_not_absolute_search_volume"])
        self.assertTrue(r["research_policy"]["do_not_infer_colors_fonts_or_sales_from_trends"])

    def test_skipping_live_search_is_no_external_query(self):
        with patch.object(searxng_research, "search", side_effect=AssertionError("unexpected internet use")):
            r = unified_research.collect("sauna Goa", include_web=False)
        self.assertEqual(r["web_research"]["status"], "skipped")

    def test_bad_property_and_private_query_rejected(self):
        for site in ("http://example.org/", "https://localhost/", "https://example.org:444/"):
            with self.assertRaises(ValueError):
                gsc_metrics.property_id(site)
        with self.assertRaises(ValueError):
            unified_research.collect("please research password credentials", include_web=False)
        with self.assertRaises(ValueError):
            unified_research.collect("sauna research", geo="ZZ", include_web=False)

    def test_no_credentials_cannot_fetch_or_make_fake_data(self):
        with self.assertRaises(RuntimeError):
            gsc_metrics.fetch_api("2026-09-01", "2026-09-28")
        self.assertEqual(gsc_metrics.status()["stored_query_rows"], 0)

    def test_brain_task_allowlist_contract(self):
        payload = {"topic": "wellness Goa research", "geo": "IN",
                   "site": "sc-domain:example.org"}
        self.assertEqual(brain.safe_payload("research_brief", payload), payload)
        for data in ({"topic": "x"}, {"topic": "sauna", "geo": "XX"},
                     {"topic": "sauna", "include_web": "yes"},
                     {"topic": "sauna", "site": "file:///etc/passwd"}):
            with self.assertRaises(ValueError):
                brain.safe_payload("research_brief", data)


    def test_verified_wordpress_bridge_real_metrics_import_and_relevance(self):
        report = {
            "property": "https://example.org/", "start_date": "2026-09-20",
            "end_date": "2026-10-18", "dimensions": ["query"],
            "source": "google-search-console-direct",
            "rows": [
                {"keys": ["mud bath goa"], "clicks": 5, "impressions": 97,
                 "ctr": 5/97, "position": 1.48},
                {"keys": ["contact someone@example.org"], "clicks": 2,
                 "impressions": 3, "ctr": 2/3, "position": 4.5}
            ]
        }
        result = gsc_metrics.import_engagement_core(report, "https://example.org/")
        self.assertEqual(result["rows"], 1)
        self.assertEqual(result["source"], "engagement_core_gsc_readonly_bridge")
        saved = gsc_metrics.relevant("mud bath", site="https://example.org/")
        self.assertEqual(saved["status"], "observed")
        self.assertEqual(saved["rows"][0]["impressions"], 97)
        self.assertNotIn("someone@example.org", json.dumps(saved))
        self.assertFalse(gsc_metrics.status()["oauth_configured"])

    def test_bridge_fails_closed_for_foreign_property_or_wrong_source(self):
        sample = {"property":"https://example.org/","start_date":"2026-09-20",
                  "end_date":"2026-10-18","dimensions":["query"],
                  "source":"google-search-console-direct","rows":[
                    {"keys":["sauna goa"],"clicks":1,"impressions":2,"ctr":0.5,"position":2.0}]}
        with self.assertRaises(ValueError):
            gsc_metrics.import_engagement_core(sample,"https://another.org/")
        with self.assertRaises(ValueError):
            gsc_metrics.import_engagement_core({**sample,"source":"unknown"},"https://example.org/")
        with self.assertRaises(ValueError):
            gsc_metrics.import_engagement_core({**sample,"dimensions":["page"]},"https://example.org/")
        with self.assertRaises(ValueError):
            gsc_metrics.import_engagement_core({**sample,"private_token":"never"},"https://example.org/")
        with self.assertRaises(ValueError):
            gsc_metrics.import_engagement_core({**sample,"rows":[]},"https://example.org/")
        self.assertEqual(gsc_metrics.status()["stored_query_rows"], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
