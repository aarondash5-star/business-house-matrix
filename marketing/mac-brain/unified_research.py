#!/usr/bin/env python3
"""Evidence-aware read-only Marketing research aggregator.

DO NOT coerce web rankings, national news spikes, or Search Console metrics
into one fabricated search-volume / design preference score.
"""
import argparse
import json
import sys
from datetime import datetime, timezone

import gsc_metrics
import searxng_research
import trends

ALLOWED_GEO = frozenset(("IN", "GB", "RU", "US"))


def collect(topic, geo="IN", site=None, include_web=True):
    # Public-query privacy rules are enforced even when using cached sources.
    topic = searxng_research._public_query(topic)
    if geo not in ALLOWED_GEO:
        raise ValueError("Research geography not approved")
    if type(include_web) is not bool:
        raise ValueError("include_web must be boolean")
    if site is not None:
        site = gsc_metrics.property_id(site)
    web = {"status": "skipped", "results": [], "source": "self_hosted_searxng"}
    if include_web:
        try:
            raw = searxng_research.search(topic)
            web = {
                "status": "observed", "source": "self_hosted_searxng",
                "authenticated_relay": bool(raw.get("device_peer_verified")),
                "results": [
                    {"title": str(x.get("title", ""))[:180],
                     "url": str(x.get("url", ""))[:800],
                     "snippet": str(x.get("snippet", ""))[:700],
                     "engine": str(x.get("engine", ""))[:60]}
                    for x in raw.get("results", [])[:8] if isinstance(x, dict)
                ],
                "citations_required": True,
                "request_id": raw.get("request_id")
            }
            if raw.get("mode") != "self_hosted_encrypted_paired_relay" or not web["authenticated_relay"]:
                raise RuntimeError("Search results lack certified device verification")
        except (RuntimeError, ValueError, OSError) as exc:
            # Fail closed: discard potentially unverified results from response.
            web = {"status": "unavailable", "source": "self_hosted_searxng",
                   "results": [], "reason": type(exc).__name__, "citations_required": True}
    try:
        signal = trends.brief_context(topic, geo, limit=5)
        trend = {
            "status": "observed" if not signal["no_verified_relevance"] else "no_relevant_observation",
            "source": "official_google_trends_rss_and_user_exported_csv",
            "national_news_spikes": signal["rss_signal"],
            "relative_index_groups": signal["historical_comparison_groups"],
            "scope": signal["rss_scope"],
            "relative_index_scope": signal["index_scope"],
            "evidence_limitations": signal["do_not_infer"]
        }
    except (OSError, RuntimeError, ValueError) as exc:
        trend = {"status": "unavailable", "source": "official_google_trends",
                 "national_news_spikes": [], "relative_index_groups": [],
                 "reason": type(exc).__name__}
    gsc = gsc_metrics.relevant(topic, site=site, limit=10)
    status = gsc_metrics.status(site=site)
    return {
        "version": "1.0.0", "type": "evidence_separated_marketing_research",
        "topic": topic, "geo": geo, "captured_utc": datetime.now(timezone.utc).isoformat(),
        "site": site, "web_research": web, "trending_topics": trend,
        "verified_property_performance": gsc,
        "gsc_connection": {
            "oauth_configured": status["oauth_configured"],
            "stored_query_rows": status["stored_query_rows"],
            "last_imported_utc": status["last_imported_utc"],
            "connected_evidence": gsc.get("status") == "observed"
        },
        "research_policy": {
            "cited_sources_required": True,
            "external_content_untrusted": True,
            "gsc_metrics_are_site_specific": True,
            "gsc_no_data_means_unknown": True,
            "trends_not_absolute_search_volume": True,
            "rss_spikes_are_not_local_goa_demand": True,
            "do_not_infer_colors_fonts_or_sales_from_trends": True,
            "paid_fallback": False, "publish_approval": False,
            "requires_human_review_before_campaign_actions": True
        }
    }


def main():
    p = argparse.ArgumentParser(description="Marketing public research + Trends + authorized GSC evidence")
    sub = p.add_subparsers(dest="command", required=True)
    c = sub.add_parser("collect")
    c.add_argument("topic")
    c.add_argument("--geo", choices=sorted(ALLOWED_GEO), default="IN")
    c.add_argument("--site")
    c.add_argument("--skip-web", action="store_true")
    sub.add_parser("status")
    a = p.parse_args()
    try:
        if a.command == "status":
            import searxng_research as s
            data = {"version": "1.0.0", "searxng": s.status(), "trends": trends.status(),
                    "gsc": gsc_metrics.status(), "paid_fallback": False,
                    "publish_approval": False}
        else:
            data = collect(a.topic, geo=a.geo, site=a.site, include_web=not a.skip_web)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except (RuntimeError, ValueError) as exc:
        print("UNIFIED_RESEARCH_ERROR:", str(exc)[:200], file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
