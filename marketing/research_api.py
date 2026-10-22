#!/usr/bin/env python3
"""Business House Matrix research API v1.3: owner-local, read-only public evidence.

Launch: python research_api.py serve --port 18889
        python research_api.py smoke
Never expose on WAN/LAN. No arbitrary URLs, shell, website publishing or spend.
"""
import argparse
import datetime as dt
import http.server
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import urlsplit

import research_engine as engine
import research_entities as entities

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"private-evidence.sqlite3"
SEARCH=Path("/var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py")
SOURCES={
    "owner_home":"https://mokshagoa.com/",
    "hidden_oak":"https://thehiddenoak.space/pricing/",
    "goasian":"https://goasianspa.com/prices-page/",
    "satori":"https://satoriwellness.setmore.com/",
    "accessibility":"https://www.w3.org/WAI/fundamentals/accessibility-intro/",
}
GRANTS={urlsplit(url).hostname for url in SOURCES.values()}
TOPICS={
 "moksha_arambol":(
    "Arambol sauna ice bath wellness provider prices",
    "site:thehiddenoak.space/pricing/ sauna ice bath",
    "site:goasianspa.com/prices-page/ spa prices",
 ),
}
LOCK=threading.Lock()
VERSION="1.3.0"
RESULT_LIMIT=10

def _connection():
    return engine.connect(DATA)

def _public_sources(db):
    rows=db.execute("SELECT id,canonical_url,title,last_seen,status,digest FROM source ORDER BY last_seen DESC LIMIT 40").fetchall()
    approved=set(SOURCES.values())
    out=[]
    for sid,url,title,last,status,digest in rows:
        if url not in approved:continue
        category=entities.classify(url,title or "")
        out.append({"source_id":sid,"url":url,"title":(title or "")[:160],
                    "observed_utc":last,"digest":digest,"status":status,
                    "role":category["role"],"competitor_verified":False})
    return out

def build_packet(topic="moksha_arambol"):
    if topic not in TOPICS:raise ValueError("topic_not_granted")
    db=_connection()
    try:
        sources=_public_sources(db)
        competitor_leads=[s for s in sources if s["role"]=="provider_candidate_needs_review"]
        return {"schema":"business_house_matrix.marketing_research.v1.3",
                "topic":topic,"generated_utc":engine.now(),
                "source_count":len(sources),"market_map":{"own_brand_excluded":True,
                    "provider_candidates":competitor_leads},
                "sources":sources,"verified_competitors":[],
                "unverified_leads":competitor_leads,
                "pricing_table":[],"price_claims_approved":False,
                "source_backed_ux_references":[s for s in sources if s["role"]=="public_ux_guidance"],
                "gsc_opportunities":{"status":"separate_readonly_mac_adapter",
                    "supported_dimensions":["query","page","date"],"country_device":"unknown"},
                "trend_signal":{"rss_scope":"national_news","local_index":"unknown"},
                "unresolved_questions":["Review official page service inclusions and exact prices",
                    "Confirm candidate operating status and independently corroborate critical facts",
                    "Approve exact monitoring URL list before unattended scheduling"],
                "required_visual_brand_constraints":["real Moksha facility images","mobile-first",
                    "ground-floor sauna and ice bath","no active checkout/PMS/retreat writes"],
                "human_review_required":True,"approved_for_design_claims":False,
                "publish_approval":False,"spend_approval":False,"paid_fallback":False}
    finally:db.close()

def run(topic="moksha_arambol",refresh=False):
    if topic not in TOPICS or type(refresh) is not bool:raise ValueError("invalid_run_request")
    if not LOCK.acquire(blocking=False):return {"status":"busy","retry_later":True}
    try:
        scans=[]
        if refresh:
            db=_connection()
            try:
                for name,url in SOURCES.items():
                    result=engine.fetch_extract(url,GRANTS,db)
                    row={"name":name,"url":url,"status":result.get("status","unavailable")}
                    if result.get("status")=="needs_review":
                        ev=engine.save_evidence(db,result)
                        row.update({"change":ev.get("change"),"source_id":ev.get("source_id")})
                    else:row["reason"]=str(result.get("reason","unknown"))[:80]
                    scans.append(row)
            finally:db.close()
        searches=[]
        for q in TOPICS[topic]:
            if not SEARCH.is_file():break
            try:
                p=subprocess.run([sys.executable,str(SEARCH),q,"--limit","5"],capture_output=True,
                                 text=True,stdin=subprocess.DEVNULL,timeout=18)
                if p.returncode:raise RuntimeError("search_nonzero")
                response=json.loads(p.stdout[:55000])
                results=[]
                for item in response.get("results",[])[:5]:
                    url=str(item.get("url",""))[:500]
                    if not url.startswith("https://"):continue
                    role=entities.classify(url,str(item.get("title","")))
                    results.append({"url":url,"title":str(item.get("title",""))[:140],
                                    "role":role["role"],"verified":False})
                searches.append({"query":q,"status":"retrieved","sources":results})
            except (OSError,RuntimeError,ValueError,subprocess.TimeoutExpired) as exc:
                searches.append({"query":q,"status":"unavailable","reason":type(exc).__name__})
        packet=build_packet(topic)
        packet["discovery_queries"]=searches
        packet["crawl_results"]=scans
        packet["quality_gate"]={"historical_or_unrelated_source_promoted":False,
            "all_critical_facts_verified":False,"release_status":"research_only",
            "missing_live_5d_gsc":True}
        packet["ready_for_design_copy"]=False
        return packet
    finally:LOCK.release()

class Handler(http.server.BaseHTTPRequestHandler):
    server_version="BHMResearch/1.3"
    def log_message(self,*args):pass
    def _reply(self,status,payload):
        body=json.dumps(payload,ensure_ascii=False,separators=(",",":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path=="/health":
            self._reply(200,{"version":VERSION,"status":"ready","bind":"loopback",
                             "no_external_publish":True,"manual_review_required":True})
        elif self.path=="/v1/packet/moksha_arambol":
            self._reply(200,build_packet())
        else:self._reply(404,{"error":"not_found"})
    def do_POST(self):
        if self.path!="/v1/run":
            self._reply(404,{"error":"not_found"});return
        if self.headers.get("Origin") is not None:
            self._reply(403,{"error":"browser_origin_denied"});return
        if self.headers.get("Content-Type")!="application/json":
            self._reply(415,{"error":"json_required"});return
        rawsize=self.headers.get("Content-Length","")
        if not rawsize.isdecimal() or int(rawsize)>1024:
            self._reply(413,{"error":"bounded_body_required"});return
        try:
            value=json.loads(self.rfile.read(int(rawsize)))
            if not isinstance(value,dict) or set(value)-{"topic","refresh"}:
                raise ValueError("request_schema")
            response=run(value.get("topic","moksha_arambol"),value.get("refresh",False))
            self._reply(200,response)
        except (ValueError,TypeError,KeyError) as exc:
            self._reply(400,{"error":str(exc)[:80]})
        except (sqlite3.Error,OSError) as exc:
            self._reply(503,{"error":type(exc).__name__})

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="action",required=True)
    s=sub.add_parser("serve");s.add_argument("--port",type=int,default=18889)
    sub.add_parser("smoke");sub.add_parser("packet")
    a=p.parse_args()
    if a.action=="smoke":
        packet=run()
        print(json.dumps({"status":"pass" if packet["source_count"]>=2 else "partial",
              "sources":packet["source_count"],
              "providers":len(packet["unverified_leads"]),
              "queries":len(packet["discovery_queries"]),
              "verified_competitors":len(packet["verified_competitors"]),
              "design_approved":packet["ready_for_design_copy"],
              "paid_fallback":packet["paid_fallback"]},indent=2))
        if packet["source_count"]<2:sys.exit(2)
    elif a.action=="packet":
        print(json.dumps(build_packet(),ensure_ascii=False,indent=2))
    else:
        if not 1024<=a.port<=65535:raise ValueError("port_out_of_range")
        server=http.server.ThreadingHTTPServer(("127.0.0.1",a.port),Handler)
        server.daemon_threads=True
        server.serve_forever(poll_interval=0.5)
if __name__=="__main__":main()
