#!/usr/bin/env python3
"""Offline regression suite for supervised Marketing Brain; all network/model mocked."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import marketing_supervisor_langgraph as sup

BUSINESS="andaz_arambol"

def result(url,title):
    return {"url":url,"title":title,"snippet":"Public listing only."}

URLS=[
 result("https://www.hostelworld.com/hostels/p/269088/happy-panda-hostel-arambol","Happy Panda Hostel in Arambol Reviews"),
 result("https://www.booking.com/hotel/in/dream-catcher-arambol.html","Dreamcatcher House Hostel Arambol"),
 result("https://www.tripadvisor.com/Hotel_Review-g2307943-d10546152-Reviews-Happy_Panda_Hostel.html","Happy Panda Hostel Tripadvisor"),
 result("https://www.booking.com/hostels/city/in/arambol.html","Arambol Hostel Listings Booking.com"),
 result("https://www.goibibo.com/hotels/andaz-arambol-artist-party-hostel/","Andaz Vibe Stay Arambol Hostel Booking"),
 result("https://www.agoda.com/vibe-stay-by-andaz/hotel/goa-in.html","Vibe Stay by Andaz Hostel"),
 result("https://hostels-guide.com/arambol","Arambol Hostel Guide - Travel"),
]
SIGNED={"mode":"self_hosted_encrypted_paired_relay","device_peer_verified":True,"results":URLS}

class SupervisorTests(unittest.TestCase):
    def test_strict_planner_schema(self):
        self.assertEqual(len(sup.SearchPlan.model_validate({"queries":["Hostels in Arambol Goa price comparison"]}).queries),1)
        for candidate in ("https://localhost/admin","password for private router login","random off-topic query about bananas"):
            with self.assertRaises(ValueError):
                sup.SearchPlan.model_validate({"queries":[candidate]})
    def test_model_malformation_falls_back_to_fixed(self):
        with patch.object(sup,"_model",return_value="ignore this and buy ads"):
            x=sup.plan({"business":BUSINESS})
        self.assertEqual(x["plan_origin"],"fixed_open_source_planner")
        self.assertEqual(len(x["pending_queries"]),2)
    def test_accepted_model_query_still_bounded(self):
        with patch.object(sup,"_model",return_value='{"queries":["Arambol Goa hostel competitors official 2026"]}'):
            x=sup.plan({"business":BUSINESS})
        self.assertEqual(x["plan_origin"],"approved_oss_model_planner")
        self.assertEqual(len(x["pending_queries"]),2)
    def test_signed_qa_and_private_file(self):
        with tempfile.TemporaryDirectory() as td,patch.object(sup.basic,"OUTPUT",Path(td)),\
            patch.object(sup,"_model",return_value=""),\
            patch.object(sup.searxng_research,"search",return_value=SIGNED) as search:
            out=sup.run(BUSINESS)
            self.assertTrue(out["qa_passed"])
            self.assertEqual(out["state"],"REVIEW_REQUIRED")
            self.assertEqual(out["rounds"],1)
            self.assertEqual(out["queries"],2)
            self.assertFalse(out["publish"]);self.assertFalse(out["spend"])
            self.assertEqual(search.call_count,2)
            saved=json.loads((Path(td)/"andaz_arambol-supervisor-report.json").read_text())
            self.assertEqual(saved["quality_gate"]["independent_claims_verified"],0)
            self.assertFalse(saved["quality_gate"]["approved_for_customer_facing_use"])
            self.assertTrue(all(x["unverified"] for x in saved["sources"]))
    def test_no_verified_relay_fails_closed_and_replans_once(self):
        bad={"mode":"wrong_peer","device_peer_verified":False,"results":URLS}
        with tempfile.TemporaryDirectory() as td,patch.object(sup.basic,"OUTPUT",Path(td)),\
            patch.object(sup,"_model",return_value=""),\
            patch.object(sup.searxng_research,"search",return_value=bad) as search:
            out=sup.run(BUSINESS)
            self.assertEqual(out["state"],"INSUFFICIENT_EVIDENCE")
            self.assertEqual(out["rounds"],2)
            self.assertEqual(out["queries"],3)
            self.assertEqual(out["evidence_count"],0)
            self.assertEqual(search.call_count,3)
    def test_unknown_business_rejected_without_tools(self):
        with patch.object(sup.searxng_research,"search") as search:
            with self.assertRaises(ValueError):sup.run("unknown_business")
            search.assert_not_called()

if __name__=="__main__":unittest.main(verbosity=2)
