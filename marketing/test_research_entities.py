#!/usr/bin/env python3
import datetime as dt
import unittest
import research_entities as e
NOW=dt.datetime(2026,10,22,12,0,tzinfo=dt.timezone.utc)
Q="The official provider lists an ice bath at this price on its public service page."
def c(**kw):
    return e.claim("displayed_price","700","https://provider.example/pricing",Q,NOW.isoformat(),
                   currency="INR",units="per session",first_party=True,**kw)
class EntityTests(unittest.TestCase):
    def test_moksha_official_not_competitor(self):
        self.assertEqual(e.classify("https://mokshagoa.com/","Moksha Wellness Goa")["role"],"first_party_own_brand")
    def test_reseller_not_competitor(self):
        x=e.classify("https://getyourguide.com/arambol/moksha","Moksha Wellness Goa - Fire & Ice")
        self.assertEqual(x["role"],"third_party_own_brand_listing")
        self.assertFalse(x["competitor"])
    def test_directory_is_not_verified_competitor(self):
        x=e.classify("https://www.tripadvisor.com/Attractions-Goa","Sauna listings")
        self.assertEqual(x["role"],"third_party_directory_or_reseller")
        self.assertFalse(x["competitor"])
    def test_own_name_with_punctuation(self):
        self.assertEqual(e.normalize_name("MÓKSHA  WELLNESS").split(),["móksha","wellness"])
    def test_provider_candidate_unverified(self):
        self.assertEqual(e.classify("https://provider.example/","Goa sauna")["role"],"provider_candidate_needs_review")
    def test_direct_quote_required(self):
        with self.assertRaises(ValueError):e.claim("service","sauna","https://example.org/x","",NOW.isoformat())
    def test_price_currency_required(self):
        with self.assertRaises(ValueError):e.claim("displayed_price","700","https://example.org/x",Q,NOW.isoformat())
    def test_non_numeric_price_rejected(self):
        with self.assertRaises(ValueError):e.claim("displayed_price","as low as 700","https://example.org/x",Q,NOW.isoformat(),currency="INR")
    def test_typed_claim_is_unverified(self):
        x=c()
        self.assertEqual(x["status"],"needs_review")
        self.assertEqual(x["currency"],"INR")
        self.assertFalse(x["human_reviewed"])
    def test_price_stale(self):
        x=c()
        later=NOW+dt.timedelta(days=8)
        self.assertTrue(e.stale(x,at=later))
    def test_price_fresh(self):
        self.assertFalse(e.stale(c(),at=NOW+dt.timedelta(days=1)))
    def test_price_conflict_explicit(self):
        x=c(); y={**x,"value":"900","source_url":"https://other.example/listing"}
        rows=e.reconcile([{**x,"entity":"Sauna Spa"},{**y,"entity":"sauna SPA"}])
        self.assertEqual(len(rows),1)
        self.assertTrue(rows[0]["conflict"])
    def test_identical_prices_no_false_conflict(self):
        x=c();y={**x,"source_url":"https://other.example"}
        self.assertFalse(e.reconcile([{**x,"entity":"X"},{**y,"entity":"X"}])[0]["conflict"])
    def test_no_auto_approval_without_independent_source(self):
        with self.assertRaisesRegex(ValueError,"independent"):e.certify_claim(c(),["https://provider.example/other"],"Reviewer",at=NOW)
    def test_no_auto_approval_without_reviewer(self):
        with self.assertRaisesRegex(ValueError,"reviewer"):e.certify_claim(c(),["https://independent.example/fact"],"",at=NOW)
    def test_no_auto_approval_when_stale(self):
        with self.assertRaisesRegex(ValueError,"fresh"):e.certify_claim(c(),["https://independent.example/fact"],"Reviewer",at=NOW+dt.timedelta(days=8))
    def test_valid_manual_certification_contract(self):
        row=e.certify_claim(c(),["https://independent.example/fact"],"Reviewer",at=NOW)
        self.assertEqual(row["status"],"verified")
        self.assertTrue(row["human_reviewed"])
    def test_incomplete_output_rejected(self):
        self.assertEqual(e.completeness({"market_map":{}})["reason"],"missing_required_sections")
    def test_empty_packet_not_fabricated(self):
        pkt={k:[] for k in ("market_map","verified_competitors","unverified_leads","pricing_table",
            "source_backed_ux_references","gsc_opportunities","unresolved_questions","required_visual_brand_constraints")}
        self.assertTrue(e.completeness(pkt)["pass"])
    def test_truncated_output_rejected(self):
        pkt={k:[] for k in ("market_map","verified_competitors","unverified_leads","pricing_table",
            "source_backed_ux_references","gsc_opportunities","unresolved_questions","required_visual_brand_constraints")}
        pkt["provider_output_chars"]=433
        self.assertFalse(e.completeness(pkt)["pass"])
if __name__=="__main__":unittest.main(verbosity=2)
