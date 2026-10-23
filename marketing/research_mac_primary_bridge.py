#!/usr/bin/env python3
"""Mac-first Marketing research evidence, with existing signed Dell discovery only.

Deploy as research_market_bridge.py only after isolated QA and a verified private
SQLite snapshot. Does not perform extraction, accept URLs, enable schedules,
publish, spend, promote factual claims or change the signed relay protocol.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import research_mac_local

TOPICS = frozenset(("moksha_arambol", "andaz_arambol"))
ENGINES = frozenset(("searxng", "duckduckgo"))
DB = Path.home() / ".local" / "share" / "bhm-research" / "evidence.sqlite3"
QUERIES = {
    "moksha_arambol": "Arambol Goa wellness sauna ice bath service providers",
    "andaz_arambol": "Arambol Goa hostel dorm private rooms traveler accommodation",
}


def local_report(topic: str) -> dict:
    evidence = research_mac_local.packet(topic, path=DB)
    with research_mac_local._readonly_connection(DB) as db:
        total = db.execute("SELECT COUNT(*) FROM source").fetchone()[0]
    return {
        "schema": "business_house_matrix.marketing_research.v1.3",
        "topic": topic,
        "primary_host": "mac-linux",
        "local_evidence_snapshot": True,
        "source_count": total,
        "market_map": evidence["market_map"],
        "sources": evidence["unverified_leads"],
        "verified_competitors": [],
        "unverified_leads": evidence["unverified_leads"],
        "pricing_table": [],
        "price_claims_approved": False,
        "source_backed_ux_references": evidence.get("source_backed_ux_references", []),
        "gsc_opportunities": evidence["gsc_opportunities"],
        "trend_signal": evidence["trends"],
        "discovery_queries": [],
        "human_review_required": True,
        "approved_for_design_claims": False,
        "ready_for_design_copy": False,
        "publish_approval": False,
        "spend_approval": False,
        "paid_fallback": False,
        "stage_b_certified": False,
        "verified_live_checkout_rates": 0,
        "local_evidence_confidence": "unverified",
    }


def market(topic="moksha_arambol", source_engine="duckduckgo") -> dict:
    if topic not in TOPICS or source_engine not in ENGINES:
        raise ValueError("public_research_scope_not_granted")
    # A bad/missing Mac DB must fail closed rather than silently declaring Dell
    # the primary or inventing a new evidence store.
    report = local_report(topic)
    signed = False
    delegated = "not_requested"
    request_id = None
    if topic == "moksha_arambol":
        # Existing approved signed Mac->Dell public research operation is now a
        # subordinate discovery worker; it is NOT the evidence primary.
        try:
            import research_market_dell_bridge
            previous = research_market_dell_bridge.market(topic, source_engine)
            incoming = previous["report"]
            if (previous.get("signed_device_pair_verified") is not True
                or incoming.get("schema") != report["schema"]
                or incoming.get("topic") != topic
                or incoming.get("publish_approval") is not False
                or incoming.get("approved_for_design_claims") is not False):
                raise ValueError("untrusted_delegated_research")
            signed = True
            delegated = "signed_dell_discovery"
            request_id = previous.get("request_id")
            report["discovery_queries"] = incoming.get("discovery_queries", [])
            report["source_backed_ux_references"] = report["source_backed_ux_references"]
            report["delegated_research_status"] = "unverified_public_leads_only"
        except (OSError, ValueError, RuntimeError, ImportError, KeyError, TypeError):
            delegated = "degraded_local_evidence_only"
    else:
        # Andaz local database available; live signed discovery is handled by
        # the existing research_brief/unified_research pipeline, not this path.
        delegated = "andaz_local_evidence_only"
    report["requested_engine"] = source_engine
    report["search_backend"] = delegated
    report["publish_approval"] = False
    report["approved_for_design_claims"] = False
    report["ready_for_design_copy"] = False
    report["price_claims_approved"] = False
    report["pricing_table"] = []
    return {
        "provider": "bhm_mac_primary_evidence_v1",
        "primary_host": "mac-linux",
        "evidence_primary_mac_verified": True,
        "signed_device_pair_verified": signed,
        "request_id": request_id,
        "source_engine": source_engine,
        "report": report,
        "paid_fallback": False,
        "publish_approval": False,
    }
