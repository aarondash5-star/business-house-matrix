#!/usr/bin/env python3
"""Evidence-aware Marketing research aggregator with bounded focused queries and QA.
No credential access, paid fallbacks, publication, or source-claim promotion.
"""
import argparse
import json
import sys
from datetime import datetime, timezone

import gsc_metrics
import research_quality
import searxng_research
import trends

ALLOWED_GEO = frozenset(("IN", "GB", "RU", "US"))

def collect(topic, geo="IN", site=None, include_web=True):
    topic = searxng_research._public_query(topic)
    if geo not in ALLOWED_GEO:
        raise ValueError("Research geography not approved")
    if type(include_web) is not bool:
        raise ValueError("include_web must be boolean")
    if site is not None:
        site = gsc_metrics.property_id(site)
    tasks = research_quality.plan(topic)
    web = {"status":"skipped", "results":[], "source":"self_hosted_searxng",
           "authenticated_relay":False, "queries":[]}
    if include_web:
        chunks = []
        requests = []
        verified = False
        errors = 0
        for task in tasks:
            row = {"category":task["category"],"query":task["query"]}
            try:
                # All calls use the pre-existing signed and paired private relay.
                raw = searxng_research.search(task["query"])
                if (raw.get("mode") != "self_hosted_encrypted_paired_relay" or
                    raw.get("device_peer_verified") is not True):
                    raise RuntimeError("Unverified search transport")
                verified = True
                chunks.append({"category":task["category"],"results":
                    [x for x in raw.get("results",[])[:8] if isinstance(x,dict)]})
                row.update({"status":"retrieved","candidate_count":len(chunks[-1]["results"]),
                            "request_id":raw.get("request_id")})
            except (RuntimeError, ValueError, OSError) as exc:
                errors += 1
                row.update({"status":"unavailable","reason":type(exc).__name__})
            requests.append(row)
        quality = research_quality.grade(chunks)
        kept = quality["results"]
        web = {
            "status":("observed" if kept and not errors else "partial" if kept else
                      "insufficient_evidence" if verified else "unavailable"),
            "source":"self_hosted_searxng",
            "authenticated_relay":verified,
            "results":kept,
            "queries":requests,
            "quality_gate":{
                "version":"1.1.0","candidate_count":sum(c.get("candidate_count",0) for c in requests),
                "kept_count":quality["kept_count"],"rejected_count":quality["rejected_count"],
                "category_counts":quality["category_counts"],
                "rejected_sources":quality["rejected"],
                "evidence_limitations":[
                    "Public search relevance is not independent verification.",
                    "Local listings are market leads, not confirmed competitors.",
                    "Generic UX references do not measure local Goa demand.",
                    "Relevance and SEO search rank do not imply conversion or revenue."
                ]
            },
            "citations_required":True,
            "paid_fallback":False
        }
    try:
        # National news RSS must never match a year like 2026 as a research signal.
        signal = trends.brief_context(research_quality.trend_query(topic), geo, limit=5)
        trend = {
            "status":"observed" if not signal["no_verified_relevance"] else "no_relevant_observation",
            "source":"official_google_trends_rss_and_user_exported_csv",
            "national_news_spikes":signal["rss_signal"],
            "relative_index_groups":signal["historical_comparison_groups"],
            "scope":signal["rss_scope"],
            "relative_index_scope":signal["index_scope"],
            "evidence_limitations":signal["do_not_infer"]
        }
    except (OSError, RuntimeError, ValueError) as exc:
        trend = {"status":"unavailable","source":"official_google_trends",
                 "national_news_spikes":[],"relative_index_groups":[],
                 "reason":type(exc).__name__}
    gsc = research_quality.gsc_gate(gsc_metrics.relevant(topic,site=site,limit=25),topic)
    status = gsc_metrics.status(site=site)
    return {
        "version":"1.1.0",
        "type":"evidence_separated_marketing_research",
        "topic":topic,"geo":geo,
        "captured_utc":datetime.now(timezone.utc).isoformat(),
        "site":site, "web_research":web, "trending_topics":trend,
        "verified_property_performance":gsc,
        "gsc_connection":{
            "oauth_configured":status["oauth_configured"],
            "stored_query_rows":status["stored_query_rows"],
            "last_imported_utc":status["last_imported_utc"],
            "connected_evidence":gsc.get("status") in ("observed","no_relevant_queries"),
            "freshness_warning":True
        },
        "research_policy":{
            "cited_sources_required":True,
            "external_content_untrusted":True,
            "gsc_metrics_are_site_specific":True,
            "gsc_no_data_means_unknown":True,
            "trends_not_absolute_search_volume":True,
            "rss_spikes_are_not_local_goa_demand":True,
            "do_not_infer_colors_fonts_or_sales_from_trends":True,
            "source_relevance_is_not_factual_verification":True,
            "paid_fallback":False,"publish_approval":False,
            "requires_human_review_before_campaign_actions":True
        }
    }

def main():
    p=argparse.ArgumentParser(description="Marketing public research + Trends + authorized GSC evidence")
    sub=p.add_subparsers(dest="command",required=True)
    c=sub.add_parser("collect")
    c.add_argument("topic")
    c.add_argument("--geo",choices=sorted(ALLOWED_GEO),default="IN")
    c.add_argument("--site")
    c.add_argument("--skip-web",action="store_true")
    sub.add_parser("status")
    a=p.parse_args()
    try:
        if a.command=="status":
            data={"version":"1.1.0","searxng":searxng_research.status(),
                  "trends":trends.status(),"gsc":gsc_metrics.status(),
                  "paid_fallback":False,"publish_approval":False}
        else:
            data=collect(a.topic,geo=a.geo,site=a.site,include_web=not a.skip_web)
        print(json.dumps(data,ensure_ascii=False,indent=2))
    except (RuntimeError,ValueError) as exc:
        print("UNIFIED_RESEARCH_ERROR:",str(exc)[:200],file=sys.stderr)
        sys.exit(2)

if __name__=="__main__":
    main()
