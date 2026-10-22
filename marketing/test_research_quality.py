#!/usr/bin/env python3
"""Offline regression suite: pollution, provenance, research limits and safety."""
import unittest
from unittest.mock import patch
import research_quality as q
import unified_research as u

BAD=[
 {"title":"CHRISTIM DUMBER - World Radio History",
  "url":"https://www.worldradiohistory.com/Archive-All-Music/Billboard/30s/1939/Billboard-1939-12-02.pdf",
  "snippet":"A newspaper from 1939","engine":"duckduckgo"},
 {"title":"5 ways to lighten knee skin naturally",
  "url":"https://www.greenprophet.com/2013/11/5-ways-devoted-muslimahs-can-eco-clean-dirty-prayer-knees/",
  "snippet":"Tips for natural skin.","engine":"duckduckgo"},
 {"title":"Coinkit words.py",
  "url":"https://github.com/shea256/coinkit/blob/master/coinkit/words.py",
  "snippet":"List of words","engine":"duckduckgo"}
]
GOOD=[
 {"title":"Moksha Wellness Goa | Sauna, Ice Bath & Mud Bath in Arambol",
  "url":"https://mokshagoa.com/?utm_source=x",
  "snippet":"Moksha Arambol Goa offers sauna, ice baths and mud wellness rituals",
  "engine":"duckduckgo"},
 {"title":"Sauna and Ice Bath in Arambol Goa",
  "url":"https://wellnesslocal.example.org/sauna-ice-goa",
  "snippet":"A sauna and ice bath experience in North Goa","engine":"duckduckgo"},
 {"title":"Guide to booking experience websites for wellness spas",
  "url":"https://www.uxstudies.org/spa-wellness-booking",
  "snippet":"Mobile website booking usability for wellness spa guests",
  "engine":"bing"}
]

def gsc_rows():
 return {"status":"observed","site":"https://mokshagoa.com/","start":"2026-09-20","end":"2026-10-18",
         "rows":[
             {"query":"sauna and ice bath","clicks":1,"impressions":20,"matched_terms":["and","sauna","bath"]},
             {"query":"old unrelated clothing ads goa","clicks":15,"impressions":500,"matched_terms":["goa"]},
             {"query":"mud bath in goa","clicks":3,"impressions":22,"matched_terms":["bath","goa"]}
         ]}

class ResearchQualityTests(unittest.TestCase):
 def test_topic_planning_replaces_keyword_dump(self):
  p=q.plan("Goa wellness retreats sauna ice bath mud aloe therapies mobile booking UX website SEO design customer journey")
  self.assertLessEqual(len(p),3)
  self.assertEqual([x["category"] for x in p],["local_services","local_pricing","website_ux_reference"])
  self.assertTrue(all(len(x["query"])<=90 for x in p))
  self.assertFalse(any("customer journey" in x["query"] for x in p))
 def test_irrelevant_documents_rejected(self):
  result=q.grade([{"category":"local_services","results":BAD+GOOD[:1]}])
  self.assertEqual(len(result["results"]),1)
  self.assertEqual(result["rejected_count"],3)
  self.assertIn("mokshagoa.com",result["results"][0]["url"])
 def test_own_brand_not_marked_competitor(self):
  res,_=q.judge(GOOD[0],"local_services")
  self.assertEqual(res["evidence_class"],"own_brand_or_third_party_listing_not_competitor")
  self.assertNotIn("utm_source",res["url"])
 def test_general_ux_reference_separate(self):
  result=q.grade([{"category":"website_ux_reference","results":GOOD[2:3]}])
  self.assertEqual(result["kept_count"],1)
  self.assertEqual(result["results"][0]["evidence_class"],"general_ux_reference_not_local_demand")
 def test_irrelevant_generic_result_not_ux(self):
  result=q.grade([{"category":"website_ux_reference","results":BAD}])
  self.assertEqual(result["kept_count"],0)
 def test_canonical_dedup(self):
  dup={**GOOD[0],"url":"https://mokshagoa.com/?fbclid=123"}
  res=q.grade([{"category":"local_services","results":[GOOD[0],dup]}])
  self.assertEqual(res["kept_count"],1)
  self.assertEqual(res["rejected"][0]["reason"],"duplicate_url")
 def test_block_ssrf_scheme_credentials(self):
  for url in ["http://mokshagoa.com/","https://127.0.0.1/home","https://localhost/x",
              "https://user:pass@mokshagoa.com/","file:///etc/passwd"]:
   self.assertEqual(q.clean_url(url),"")
 def test_trends_ignore_year(self):
  self.assertNotIn("2026",q.trend_query("Goa wellness sauna retreat website 2026"))
  self.assertIn("sauna",q.trend_query("Goa wellness sauna retreat website 2026"))
 def test_gsc_drop_generic_and_keep_service(self):
  out=q.gsc_gate(gsc_rows(),"Goa sauna ice bath mud wellness website UX")
  self.assertEqual(len(out["rows"]),2)
  self.assertNotIn("old unrelated",str(out))
  self.assertNotIn("and",out["rows"][0]["matched_terms"])
 def test_gsc_no_relevant_not_fabricated(self):
  out=q.gsc_gate(gsc_rows(),"news seo marketing ux customer")
  self.assertEqual(out["status"],"no_relevant_queries")
  self.assertEqual(out["rows"],[])
 def test_collect_no_results_insufficient_evidence(self):
  fake={"mode":"self_hosted_encrypted_paired_relay","device_peer_verified":True,
        "results":BAD,"request_id":"mock-only"}
  tr={"no_verified_relevance":True,"rss_signal":[],"historical_comparison_groups":[],
      "rss_scope":"test","index_scope":"test","do_not_infer":[]}
  gsc=gsc_rows()
  status={"oauth_configured":False,"stored_query_rows":3,"last_imported_utc":"2026-10-21"}
  with patch.object(u.searxng_research,"search",return_value=fake) as search,\
       patch.object(u.trends,"brief_context",return_value=tr),\
       patch.object(u.gsc_metrics,"relevant",return_value=gsc),\
       patch.object(u.gsc_metrics,"status",return_value=status),\
       patch.object(u.gsc_metrics,"property_id",return_value="https://mokshagoa.com/"):
   out=u.collect("Goa wellness sauna ice bath website UX",site="https://mokshagoa.com/")
   self.assertEqual(out["web_research"]["status"],"insufficient_evidence")
   self.assertFalse(out["web_research"]["results"])
   self.assertGreater(out["web_research"]["quality_gate"]["rejected_count"],0)
   self.assertTrue(all("1939" not in str(x) for x in out["web_research"]["results"]))
   self.assertEqual(search.call_count,3)
 def test_forged_peer_rejected(self):
  fake={"mode":"self_hosted_encrypted_paired_relay","device_peer_verified":False,"results":GOOD}
  tr={"no_verified_relevance":True,"rss_signal":[],"historical_comparison_groups":[],
      "rss_scope":"test","index_scope":"test","do_not_infer":[]}
  status={"oauth_configured":False,"stored_query_rows":0,"last_imported_utc":None}
  with patch.object(u.searxng_research,"search",return_value=fake),\
       patch.object(u.trends,"brief_context",return_value=tr),\
       patch.object(u.gsc_metrics,"relevant",return_value={"status":"no_property_data","rows":[]}),\
       patch.object(u.gsc_metrics,"status",return_value=status):
   out=u.collect("Goa sauna ice wellness")
   self.assertEqual(out["web_research"]["status"],"unavailable")
   self.assertFalse(out["web_research"]["results"])
 def test_actual_gsc_limit_contract(self):
  tr={"no_verified_relevance":True,"rss_signal":[],"historical_comparison_groups":[],
      "rss_scope":"test","index_scope":"test","do_not_infer":[]}
  status={"oauth_configured":False,"stored_query_rows":3,"last_imported_utc":"2026-10-21"}
  def bounded(*args,**kw):
   if kw.get("limit",0)>10:raise ValueError("Bounded GSC result limit required")
   return gsc_rows()
  with patch.object(u.trends,"brief_context",return_value=tr),\
       patch.object(u.gsc_metrics,"relevant",side_effect=bounded),\
       patch.object(u.gsc_metrics,"status",return_value=status):
   result=u.collect("Goa sauna mud wellness",include_web=False)
   self.assertEqual(result["version"],"1.1.0")
   self.assertEqual(result["web_research"]["status"],"skipped")
   self.assertEqual(result["verified_property_performance"]["status"],"observed")
 def test_privacy_validation_before_network(self):
  with patch.object(u.searxng_research,"search") as search:
   with self.assertRaises(ValueError):u.collect("Send jane@example.com sauna research")
   search.assert_not_called()
if __name__=="__main__":
 unittest.main(verbosity=2)
