#!/usr/bin/env python3
"""Research API contract, scope and deny-by-default regression suite."""
import json
import tempfile
import unittest
from unittest import mock
import research_api as api

class ApiContract(unittest.TestCase):
    def test_exact_sources_are_https(self):
        self.assertEqual(len(api.SOURCES),5)
        self.assertTrue(all(url.startswith("https://") for url in api.SOURCES.values()))
    def test_approved_host_grants_only(self):
        self.assertEqual(api.GRANTS, {"mokshagoa.com","thehiddenoak.space",
                                       "goasianspa.com","satoriwellness.setmore.com","www.w3.org"})
    def test_strict_topics(self):
        with self.assertRaises(ValueError):api.build_packet("file:///etc/passwd")
        with self.assertRaises(ValueError):api.run("not_granted")
    def test_payload_invalid_refresh(self):
        with self.assertRaises(ValueError):api.run("moksha_arambol",refresh="yes")
    def test_packet_never_promotes_facts(self):
        item=api.build_packet()
        self.assertFalse(item["approved_for_design_claims"])
        self.assertFalse(item["publish_approval"])
        self.assertFalse(item["spend_approval"])
        self.assertFalse(item["paid_fallback"])
        self.assertEqual(item["verified_competitors"],[])
        self.assertEqual(item["pricing_table"],[])
    def test_real_source_roles(self):
        x=api.build_packet()
        urls=[z["url"] for z in x["market_map"]["provider_candidates"]]
        self.assertIn("https://thehiddenoak.space/pricing/",urls)
        self.assertNotIn("https://mokshagoa.com/",urls)
    def test_run_no_open_fetch_without_refresh(self):
        with mock.patch.object(api.engine,"fetch_extract",side_effect=AssertionError):
            packet=api.run(refresh=False)
        self.assertGreater(len(packet["discovery_queries"]),0)
    def test_review_flag_present_on_search(self):
        packet=api.run(refresh=False)
        self.assertFalse(packet["ready_for_design_copy"])
        for query in packet["discovery_queries"]:
            for source in query.get("sources",[]):
                self.assertFalse(source["verified"])
    def test_no_api_key_or_credential_in_sources(self):
        for url in api.SOURCES.values():
            self.assertNotIn("@",url)
            self.assertNotIn("?",url)

if __name__=="__main__":unittest.main()
