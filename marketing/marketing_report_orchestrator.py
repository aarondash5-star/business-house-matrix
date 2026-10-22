#!/usr/bin/env python3
"""Marketing Brain research-to-report task owner; uses existing Dell signed search worker.

Autonomy: choose approved searches, gather and classify evidence, synthesize a
source-grounded review draft, QA, preserve failures. No shell actions, model-prompt
execution, publishing, purchases, media writes or private tenant data.
"""
import datetime as dt
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit
import research_quality
import searxng_research

BASE=Path(__file__).resolve().parent
OUTPUT=BASE/"reports"/"private"
BUSINESSES={
 "andaz_arambol":{
   "name":"Andaz Vibe Stay - Arambol, Goa",
   "queries":[
       "Dreamcatcher House Hostel Arambol Goa 2026 property features",
       "Travo Tales Kumbaya 12 Monks Arambol Goa hostel 2026",
       "Andaz Vibe Stay Arambol booking reviews hostel"
   ],
   "owned_terms":("andaz","vibe stay"),
   "segments":["Budget solo backpackers","Groups of friends","Digital nomads / longer stays"],
 },
 "moksha_arambol":{
   "name":"Moksha Wellness, Arambol",
   "queries":["Arambol Goa sauna ice bath competitor pricing booking","North Goa sauna banya ice bath wellness providers"],
   "owned_terms":("moksha",),
   "segments":["Wellness travellers","Active travellers seeking recovery","Wellness retreat visitors"],
 }
}
MIN_RESULTS=4
MAX_SOURCES=18

def source_roles(rows,owned_terms):
    out=[]
    seen=set()
    for query_index,group in enumerate(rows):
        for x in group.get("results",[])[:8]:
            if not isinstance(x,dict):continue
            url=research_quality.clean_url(x.get("url",""))
            if not url or url in seen:continue
            seen.add(url)
            title=re.sub(r"\s+"," ",str(x.get("title",""))).strip()[:150]
            description=str(x.get("snippet",""))[:260]
            domain=urlsplit(url).hostname or ""
            if len(title)<8:continue
            owned=any(word in (title+" "+url).lower() for word in owned_terms)
            source_type="own_property_listing" if owned else (
                "third_party_directory_or_review" if domain.endswith(("booking.com","tripadvisor.com",
                    "agoda.com","hostelworld.com","makemytrip.com","goibibo.com")) else "candidate_public_source"
            )
            out.append({"id":"S"+str(len(out)+1),"title":title,"url":url,"domain":domain,
                        "source_type":source_type,"query_index":query_index,
                        "unverified":True,"excerpt":description[:160]})
            if len(out)>=MAX_SOURCES:return out
    return out

def report_from_evidence(business,groups):
    cfg=BUSINESSES[business]
    sources=source_roles(groups,cfg["owned_terms"])
    independent=[x for x in sources if x["source_type"]!="own_property_listing"]
    complete=sum(x["status"]=="observed" for x in groups)
    status="REVIEW_REQUIRED" if complete and len(independent)>=2 else "INSUFFICIENT_EVIDENCE"
    own=[x for x in sources if x["source_type"]=="own_property_listing"]
    return {
     "schema":"bhm.marketing.research_report.v1","business":business,
     "title":cfg["name"]+" | Market Research — Evidence Review Draft",
     "generated_utc":dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
     "status":status,"research_stage":{"queries":groups,"sources_found":len(sources),
        "independent_source_candidates":len(independent)},
     "executive_summary":(
        f"Public search returned {len(sources)} unique cited source leads across {len(groups)} planned searches. "
        f"{len(own)} appear to describe this business, and {len(independent)} are other public sources "
        "which may include competitors, directories or general guides. None are independently fact-verified."
     ),
     "competitor_landscape":{
       "status":"candidate_leads_needing_review",
       "candidates":[{"name_or_page":x["title"],"source_id":x["id"],"url":x["url"],
                      "price":"unknown","is_competitor_verified":False}
                     for x in independent[:10]]
     },
     "pricing_analysis":{"status":"unknown_not_yet_source_verified","prices":[]},
     "target_audiences":[{"segment":s,"status":"hypothesis_not_proven"}
                            for s in cfg["segments"]],
     "booking_and_reviews":{
       "owner_listing_sources":[{"source_id":x["id"],"url":x["url"]} for x in own],
       "ratings":"unknown_unverified","conversion":"unknown_unverified"
     },
     "seo":{"status":"audit_needed",
       "hypotheses":["Compare category and location terms against independently sourced search impressions",
                     "Check listing name/address and booking calls to action across reviewed directories"]},
     "seasonality":{"status":"not_measured","local_demand_index":"unknown",
                   "research_next":"Obtain real regional time-series evidence before seasonal claims"},
     "recommendations":[
       {"priority":1,"action":"Independently verify local competitors and their official pricing/inclusions",
        "confidence":"process_recommendation"},
       {"priority":2,"action":"Audit first-party listings for consistent brand identity, room types and bookings",
        "confidence":"process_recommendation"},
       {"priority":3,"action":"Develop segment-specific landing copy only after verified guest evidence and reviews",
        "confidence":"process_recommendation"}
     ],
     "sources":sources,
     "quality_gate":{"evidence_count":len(sources),"independent_candidates":len(independent),
        "complete_research_queries":complete,"sources_verified":0,
        "contains_verified_prices":False,"approved_for_customer_facing_use":False,
        "publish_allowed":False,"spend_allowed":False},
     "escalations":(["Need genuine competitor evidence from official current websites",
        "Need independently corroborated price, reviews and current amenities",
        "Need property-linked GSC and reliable Goa seasonality data"] if status=="REVIEW_REQUIRED"
          else ["Search returned insufficient independently relevant evidence; revise query and retry within quota"]),
    }

def markdown(p):
    rows=[f"# {p['title']}","",f"**Status:** {p['status']} — internal review draft; not approved for publication.",
       "","## Executive summary",p["executive_summary"],"","## Competitor source leads",
       "All leads are unverified; listing in this table does not establish an actual competitor.",
       "","| Source | Candidate page | Price |","|---|---|---|"]
    for x in p["competitor_landscape"]["candidates"]:
        title=x["name_or_page"].replace("|","/").replace("[","").replace("]","")
        rows.append(f"| {x['source_id']} | [{title}]({x['url']}) | Not verified |")
    rows+=["","## Pricing and positioning","No trustworthy current competitor price table yet.",
            "","## Guest segments — hypotheses only"]
    rows.extend("- "+x["segment"]+" (unverified)" for x in p["target_audiences"])
    rows+=["","## SEO and booking-platform review"]
    rows.extend("- "+x for x in p["seo"]["hypotheses"])
    rows+=["","## Seasonality","No region-specific time series verified.",
            "","## Recommended next research actions"]
    rows.extend("- "+x["action"] for x in p["recommendations"])
    rows+=["","## Open blockers"]
    rows.extend("- "+x for x in p["escalations"])
    rows+=["","## Source registry"]
    rows.extend(f"- [{x['id']}] {x['title']} — {x['url']} ({x['source_type']}; unverified)" for x in p["sources"])
    rows+=["","No data, rates, reviews or sales values were invented. No publishing or spend was performed."]
    return "\n".join(rows)+"\n"

def run(business):
    if business not in BUSINESSES:raise ValueError("business_not_registered")
    groups=[]
    for query in BUSINESSES[business]["queries"]:
        try:
            res=searxng_research.search(query)
            if res.get("device_peer_verified") is not True or res.get("mode")!="self_hosted_encrypted_paired_relay":
                raise RuntimeError("missing_signed_research_transport")
            groups.append({"query":query,"status":"observed" if res.get("results") else "unavailable",
                           "results":res.get("results",[])[:8]})
        except (RuntimeError,ValueError,OSError) as exc:
            groups.append({"query":query,"status":"unavailable","reason":type(exc).__name__,"results":[]})
    report=report_from_evidence(business,groups)
    OUTPUT.mkdir(parents=True,exist_ok=True,mode=0o700);OUTPUT.chmod(0o700)
    target=OUTPUT/(business+"-research-report.json")
    tmp=target.with_suffix(".json.tmp")
    with tmp.open("x") as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
        f.flush();os.fsync(f.fileno())
    os.chmod(tmp,0o600);os.replace(tmp,target)
    md=target.with_suffix(".md");tmpmd=md.with_suffix(".md.tmp")
    with tmpmd.open("x") as f:
        f.write(markdown(report));f.flush();os.fsync(f.fileno())
    os.chmod(tmpmd,0o600);os.replace(tmpmd,md)
    return {"mission":"research_report","business":business,"state":report["status"],
            "report_path":str(md),"source_count":len(report["sources"]),
            "independent_candidates":report["quality_gate"]["independent_candidates"],
            "research_queries":len(groups),"full_report_generated":True,
            "human_review_required":True,"publish":False,"spend":False,
            "escalations":report["escalations"][:3]}


# BHM_LANGGRAPH_SUPERVISOR_V2_20261022
# The original v1 report builder remains available as _legacy_report_run
# for independent rollback; Brain sends only allowlisted business slugs.
_legacy_report_run = run
def run(business):
    import json
    import subprocess
    from pathlib import Path
    if business not in BUSINESSES:
        raise ValueError("business_not_registered")
    py = BASE / ".venv-supervisor" / "bin" / "python"
    script = BASE / "marketing_supervisor_langgraph.py"
    if not py.is_file() or not script.is_file():
        raise RuntimeError("reviewed_supervisor_runtime_unavailable")
    result = subprocess.run([str(py), str(script), "--business", business],
        capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=135,
        check=True, cwd=str(BASE))
    if len(result.stdout)>12000:
        raise RuntimeError("oversized_supervisor_receipt")
    data = json.loads(result.stdout.strip())
    if (data.get("mode")!="brain_owned_langgraph_supervisor_v2"
        or data.get("business")!=business
        or data.get("state") not in ("REVIEW_REQUIRED","INSUFFICIENT_EVIDENCE")
        or data.get("qa_passed") is not True
        or data.get("publish") is not False or data.get("spend") is not False):
        raise RuntimeError("unsafe_supervisor_receipt")
    expected = (OUTPUT / (business+"-supervisor-report.md")).resolve()
    if str(expected)!=str(Path(data.get("report_path","")).resolve()) or not expected.is_file():
        raise RuntimeError("invalid_supervisor_report_path")
    return data
