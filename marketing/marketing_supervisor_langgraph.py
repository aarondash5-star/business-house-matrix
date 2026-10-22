#!/usr/bin/env python3
"""Marketing Brain Supervisor v2: finite LangGraph research->critique->replan->report.

No unbounded tool use. The existing Brain queue remains the sole scheduler.
Uses only the existing signed Mac-Dell SearXNG adapter and approved hosted OSS
model router (optional); never handles credentials or performs public writes.
"""
import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, TypedDict
from urllib.parse import urlsplit

from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, ConfigDict, Field, field_validator

import marketing_report_orchestrator as basic
import searxng_research

ROOT=Path(__file__).resolve().parent
MAX_ROUNDS=2
MAX_QUERIES=3

class SearchPlan(BaseModel):
    model_config=ConfigDict(extra="forbid")
    queries: list[str] = Field(min_length=1,max_length=2)
    @field_validator("queries")
    @classmethod
    def safe_queries(cls,qs):
        for q in qs:
            if not isinstance(q,str) or not 18<=len(q)<=120 or "\n" in q or "://" in q:
                raise ValueError("unsafe_or_unbounded_query")
            l=q.lower()
            if not any(x in l for x in ("arambol","goa","hostel","wellness","sauna","ice bath")):
                raise ValueError("off_topic_query")
            if any(x in l for x in ("password","credential","token","private","localhost","log in")):
                raise ValueError("not_public_research")
        return qs

class Score(BaseModel):
    model_config=ConfigDict(extra="forbid")
    unique_sources: int = Field(ge=0,le=30)
    non_owner_leads: int = Field(ge=0,le=30)
    distinct_domains: int = Field(ge=0,le=30)
    live_queries: int = Field(ge=0,le=3)
    passed: bool
    finding: str

class State(TypedDict, total=False):
    business:str
    pending_queries:list[str]
    requested:list[str]
    research_groups:list[dict[str,Any]]
    plan_origin:str
    notes:list[str]
    rounds:int
    score:dict[str,Any]
    report:dict[str,Any]
    report_paths:dict[str,str]
    draft_origin:str

def _business(b):
    if b not in basic.BUSINESSES:raise ValueError("business_not_registered")
    return basic.BUSINESSES[b]

def _model(profile,prompt):
    """Reuse the existing policy-constrained no-paid router; never inject external snippets."""
    try:
        import router
        out=router.run(profile,prompt[:3600])
        t=out.get("text","") if isinstance(out,dict) else ""
        return re.sub(r"[\x00-\x08\x0b-\x1f]","",str(t))[:1200].strip()
    except (OSError,RuntimeError,ValueError,KeyError,TimeoutError) as ex:
        return ""

def plan(s:State):
    b=s["business"];c=_business(b)
    fixed=c["queries"][:2]
    src="fixed_open_source_planner"
    # Planner sees vetted, static own-business context, never remote page text.
    prompt=("You are a marketing research planner. Return ONLY compact JSON: "
        '{"queries":["query"]}. One short public English search query to find '
        "independent competing providers/hostels in Arambol Goa. "
        "Never request logins, private data, ads or purchases. "
        "The client is "+c["name"]+". Its sector is "+
        ("hostel accommodation." if b=="andaz_arambol" else "wellness sauna ice bath.")+
        " Query <=120 chars. No commentary.")
    raw=_model("research",prompt)
    if raw:
        try:
            match=re.search(r"\{.*\}",raw,re.S)
            proposed=SearchPlan.model_validate_json(match.group(0)) if match else None
            if proposed:
                candidate=proposed.queries[0]
                if candidate.casefold() not in [x.casefold() for x in fixed]:
                    fixed=[fixed[0],candidate]
                    src="approved_oss_model_planner"
        except (ValueError,TypeError):pass
    return {"pending_queries":fixed,"requested":[],"research_groups":[],
        "plan_origin":src,"notes":[],"rounds":0}

def research(s:State):
    groups=list(s.get("research_groups",[]))
    requested=list(s.get("requested",[]))
    for query in s.get("pending_queries",[]):
        if query in requested or len(requested)>=MAX_QUERIES:continue
        requested.append(query)
        try:
            data=searxng_research.search(query)
            if data.get("device_peer_verified") is not True or data.get("mode")!="self_hosted_encrypted_paired_relay":
                raise RuntimeError("unsigned_or_wrong_peer")
            rows=[x for x in data.get("results",[])[:8] if isinstance(x,dict)]
            groups.append({"query":query,"status":"observed" if rows else "unavailable",
                           "results":rows,"signed_peer_verified":True})
        except (RuntimeError,ValueError,OSError,TimeoutError) as ex:
            groups.append({"query":query,"status":"unavailable","results":[],
                           "reason":type(ex).__name__,"signed_peer_verified":False})
    return {"research_groups":groups,"requested":requested,
            "pending_queries":[],"rounds":int(s.get("rounds",0))+1}

def critic(s:State):
    c=_business(s["business"])
    sources=basic.source_roles(s.get("research_groups",[]),c["owned_terms"])
    leads=[x for x in sources if x["source_type"]!="own_property_listing"]
    domains={urlsplit(x["url"]).hostname for x in sources}
    live=sum(x.get("status")=="observed" for x in s.get("research_groups",[]))
    passed=(len(sources)>=7 and len(leads)>=3 and len(domains)>=2 and live>=2)
    # This measures sufficiency of LEADS, not factual correctness of prices/claims.
    finding=("source_diversity_review_ready" if passed else
             "low_source_diversity_or_missing_evidence")
    grade=Score(unique_sources=len(sources),non_owner_leads=len(leads),
                distinct_domains=len(domains),live_queries=live,
                passed=passed,finding=finding)
    return {"score":grade.model_dump()}

def decision(s:State):
    if (not s["score"]["passed"] and s.get("rounds",0)<MAX_ROUNDS
       and len(s.get("requested",[]))<MAX_QUERIES):
        return "replan"
    return "compose"

def replan(s:State):
    b=s["business"]
    fallback=("Hostelworld Arambol Goa Happy Panda Dreamcatcher Hostel 2026 official pages"
        if b=="andaz_arambol" else
        "Arambol Morjim Goa sauna ice bath spa independent provider current services")
    # Automatic evidence-gap response; bounded, deterministic, no model decides tools.
    requested=set(q.casefold() for q in s.get("requested",[]))
    if fallback.casefold() in requested:return {"pending_queries":[]}
    return {"pending_queries":[fallback]}

def compose(s:State):
    rep=basic.report_from_evidence(s["business"],s.get("research_groups",[]))
    rep["schema"]="bhm.marketing.supervised_research.v2"
    rep["supervisor"]={
        "framework":"LangGraph MIT","validator":"Pydantic MIT",
        "plan_origin":s.get("plan_origin"),"rounds":s.get("rounds"),
        "queries_ran":len(s.get("requested",[])),
        "critic":s.get("score",{}),
        "full_autonomy_certified":False
    }
    # The model receives no untrusted source text; editorial ideas remain hypotheses.
    prompt=("Give two SHORT practical marketing campaign hypotheses for a "+
         ("budget social hostel in Goa" if s["business"]=="andaz_arambol"
          else "wellness sauna ice bath sanctuary in Goa")+
         ". Do not claim specific competitors, prices, reviews, rankings or demand. "
         "No publishing. Under 80 words. Internal brainstorming only.")
    model_text=_model("creative",prompt)
    rep["model_ideation"]={"text":model_text,"label":"unverified_hypothesis_only",
                           "available":bool(model_text)}
    rep["quality_gate"]["source_lead_sufficiency_pass"]=bool(s["score"]["passed"])
    rep["quality_gate"]["independent_claims_verified"]=0
    rep["quality_gate"]["approved_for_customer_facing_use"]=False
    rep["quality_gate"]["publish_allowed"]=False
    rep["quality_gate"]["spend_allowed"]=False
    rep["status"]="REVIEW_REQUIRED" if s["score"]["passed"] else "INSUFFICIENT_EVIDENCE"
    return {"report":rep,"draft_origin":"existing_no_paid_router" if model_text else "rules_only"}

def qa(s:State):
    r=s["report"]
    req=("executive_summary","competitor_landscape","pricing_analysis",
         "target_audiences","seo","seasonality","recommendations","sources","quality_gate")
    assert all(k in r and r[k] is not None for k in req),"incomplete_report"
    assert r["quality_gate"]["publish_allowed"] is False
    assert r["quality_gate"]["spend_allowed"] is False
    assert r["quality_gate"]["independent_claims_verified"]==0
    assert all(x["unverified"] is True for x in r["sources"])
    return {"notes":s.get("notes",[])+["qa_contract_passed"]}

def store(s:State):
    b=s["business"]
    r=s["report"]
    dest=basic.OUTPUT
    dest.mkdir(parents=True,exist_ok=True,mode=0o700);dest.chmod(0o700)
    paths={}
    for suffix,contents in (
        (".json",json.dumps(r,indent=2,ensure_ascii=False)+"\n"),
        (".md",basic.markdown(r)+
            "\n## Supervisor and QA trace\n"+
            json.dumps(r["supervisor"],ensure_ascii=False,indent=2)+
            "\n\n## Brain-generated campaign ideas — unverified hypotheses\n"+
            (r["model_ideation"]["text"] or "Hosted creative inference unavailable; no invented campaign facts.")+"\n")
    ):
        path=dest/(b+"-supervisor-report"+suffix)
        temp=path.with_suffix(suffix+".tmp")
        # Reject orphaned previous runs instead of overwriting a possibly live file.
        if temp.exists():raise RuntimeError("stale_report_temp_requires_review")
        fd=os.open(temp,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write(contents);f.flush();os.fsync(f.fileno())
        os.replace(temp,path);path.chmod(0o600)
        paths[suffix]=str(path)
    return {"report_paths":paths}

def build():
    graph=StateGraph(State)
    for name,node in (
        ("plan",plan),("research",research),("critic",critic),
        ("replan",replan),("compose",compose),("qa",qa),("store",store)):
        graph.add_node(name,node)
    graph.add_edge(START,"plan")
    graph.add_edge("plan","research")
    graph.add_edge("research","critic")
    graph.add_conditional_edges("critic",decision,{"replan":"replan","compose":"compose"})
    graph.add_edge("replan","research")
    graph.add_edge("compose","qa")
    graph.add_edge("qa","store")
    graph.add_edge("store",END)
    return graph.compile()

def run(business):
    _business(business)
    result=build().invoke({"business":business},config={"recursion_limit":14})
    r=result["report"]
    return {"mode":"brain_owned_langgraph_supervisor_v2",
        "business":business,"state":r["status"],
        "report_path":result["report_paths"][".md"],
        "evidence_count":len(r["sources"]),
        "independent_leads":r["quality_gate"]["independent_candidates"],
        "rounds":r["supervisor"]["rounds"],
        "queries":r["supervisor"]["queries_ran"],
        "model_planner":r["supervisor"]["plan_origin"],
        "model_ideation":r["model_ideation"]["available"],
        "qa_passed":"qa_contract_passed" in result["notes"],
        "human_review_required":True,"publish":False,"spend":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--business",choices=sorted(basic.BUSINESSES),required=True)
    a=p.parse_args()
    print(json.dumps(run(a.business),ensure_ascii=False))

if __name__=="__main__":main()
