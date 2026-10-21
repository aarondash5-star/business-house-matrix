#!/usr/bin/env python3
"""Self-hosted SearXNG source discovery for Matrix Marketing.

Only talks to the trusted Dell LAN gateway. No Tavily calls, no paid route,
no arbitrary search endpoint. Result content is untrusted external text.
"""
import argparse
import ipaddress
import json
from pathlib import Path
import re
import sqlite3
import sys
import time
from urllib.error import HTTPError,URLError
from urllib.parse import urlencode,urlsplit
from urllib.request import Request,urlopen
import router

ROOT=Path(__file__).resolve().parent
DB=ROOT/"searxng-quota.sqlite3"
GATEWAY="http://192.168.0.103:18888"
MAX_DAY=100
MAX_MINUTE=3
MAX_RESULTS=6

def _policy():
    data=router.read_policy()
    entries=[x for x in data.get("tool_connections",[]) if x.get("id")=="searxng-search"]
    if len(entries)!=1: raise RuntimeError("Self-hosted SearXNG policy is not installed")
    return entries[0]

def _ledger():
    conn=sqlite3.connect(DB,timeout=15,isolation_level=None)
    conn.execute("PRAGMA busy_timeout=15000")
    conn.execute("CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,ts INTEGER,kind TEXT,outcome TEXT)")
    DB.chmod(0o600)
    return conn

def _public_query(query):
    if not isinstance(query,str) or not 2 <= len(query.strip()) <= 180:
        raise ValueError("Public query must be between 2 and 180 characters")
    if any(ord(c)<32 for c in query):
        raise ValueError("Control characters not allowed")
    if (re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",query) or
        re.search(r"\b(?:\+?\d[\s\-]?){10,}\b",query) or
        re.search(r"\b(api.?key|private.?key|password|bearer.?token|guest.?data)\b",query,re.I)):
        raise ValueError("Possible secrets or personal data in research query")
    return query.strip()

def _local_response():
    if GATEWAY!="http://192.168.0.103:18888":
        raise RuntimeError("Nonallowlisted SearXNG gateway")
    u=urlsplit(GATEWAY)
    if not (u.scheme=="http" and u.hostname=="192.168.0.103" and u.port==18888):
        raise RuntimeError("SearXNG must use fixed Dell LAN-only endpoint")

def status():
    p=_policy();d=_ledger();now=int(time.time())
    day=d.execute("SELECT count(*) FROM attempts WHERE ts>=?",(now//86400*86400,)).fetchone()[0]
    latest=d.execute("SELECT outcome,ts FROM attempts ORDER BY ts DESC LIMIT 1").fetchone()
    d.close()
    return {"provider":"searxng","endpoint":"Dell LAN private gateway",
            "enabled":p.get("enabled",False),"self_hosted":True,
            "paid_fallback":False,"used_today":day,"local_daily_cap":MAX_DAY,
            "last_outcome":latest[0] if latest else None,
            "last_attempt_ts":latest[1] if latest else None}

def search(query,language="en",time_range=None):
    p=_policy()
    if not (p.get("enabled") is True and p.get("self_hosted") is True
            and p.get("open_source_license_reviewed") is True and p.get("paid_fallback_allowed") is False):
        raise RuntimeError("Self-hosted research disabled or license gate missing")
    _local_response()
    q=_public_query(query)
    if language not in ("en","all"):raise ValueError("Unsupported language")
    if time_range not in (None,"day","month","year"):raise ValueError("Unsupported period")
    now=int(time.time())
    d=_ledger();d.execute("BEGIN IMMEDIATE")
    try:
        day=d.execute("SELECT count(*) FROM attempts WHERE ts>=?",(now//86400*86400,)).fetchone()[0]
        minute=d.execute("SELECT count(*) FROM attempts WHERE ts>=?",(now-60,)).fetchone()[0]
        if day>=MAX_DAY or minute>=MAX_MINUTE:raise RuntimeError("Local search rate limit")
        d.execute("INSERT INTO attempts(ts,kind,outcome) VALUES(?,?,?)",(now,"search","reserved"))
        ident=d.execute("SELECT last_insert_rowid()").fetchone()[0]
        d.commit()
    except Exception:
        d.rollback();d.close();raise
    params={"q":q,"format":"json","language":language,"safesearch":"1"}
    if time_range:params["time_range"]=time_range
    url=GATEWAY+"/search?"+urlencode(params)
    try:
        req=Request(url,headers={"Accept":"application/json","User-Agent":"BusinessHouseMatrix-Marketing/1.0"})
        with urlopen(req,timeout=24) as response:
            data=json.loads(response.read(192000))
        if not isinstance(data,dict) or not isinstance(data.get("results"),list):
            raise ValueError("SearXNG result schema mismatch")
        results=[]
        for item in data["results"][:MAX_RESULTS]:
            if not isinstance(item,dict):continue
            target=str(item.get("url",""))[:700]
            u=urlsplit(target)
            if u.scheme!="https" or not u.hostname:continue
            try: ipaddress.ip_address(u.hostname);continue
            except ValueError:pass
            results.append({"title":str(item.get("title",""))[:180],
                            "url":target,"snippet":str(item.get("content",""))[:700],
                            "engine":str(item.get("engine",""))[:60]})
        d.execute("UPDATE attempts SET outcome=? WHERE id=?",("ok",ident))
        return {"provider":"searxng","mode":"self_hosted","query":q,"results":results,
                "citations_required":True,"untrusted_external_content":True,
                "retrieval_is_not_independent_fact_verification":True,
                "paid_fallback":False,"publish_approval":False}
    except (HTTPError,URLError,TimeoutError,ValueError) as exc:
        d.execute("UPDATE attempts SET outcome=? WHERE id=?",("failed",ident))
        raise RuntimeError("SearXNG search unavailable: "+type(exc).__name__) from None
    finally:
        d.close()

def extract(url):
    raise RuntimeError("Tavily Extract deprecated. No arbitrary URL fetching. Add a reviewed local Trafilatura extractor later.")

def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("status")
    s=sub.add_parser("search");s.add_argument("query");s.add_argument("--language",default="en")
    args=parser.parse_args()
    try:
        data=status() if args.command=="status" else search(args.query,args.language)
        print(json.dumps(data,indent=2,ensure_ascii=False))
    except (RuntimeError,ValueError) as err:
        print("SEARXNG_ERROR:",str(err),file=sys.stderr);sys.exit(2)
if __name__=="__main__": main()
