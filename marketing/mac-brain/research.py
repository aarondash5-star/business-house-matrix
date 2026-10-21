#!/usr/bin/env python3
"""Public-only Tavily keyless Search/Extract for Business House Matrix Marketing.

Tavily is a proprietary HOSTED research service, not an open-source component.
No key required; no token or automatic paid fallback; no sensitive data permitted.
Reference: https://docs.tavily.com/documentation/keyless
"""
import argparse
import getpass
import ipaddress
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import router

ROOT=Path(__file__).resolve().parent
DB=ROOT/"research-quota.sqlite3"
SECRET=ROOT/"secrets"/"tavily-search.key"
ROOT_URL="https://api.tavily.com"
MAX_MONTHLY=100    # self-imposed request cap; NOT an advertised keyless allowance
MAX_DAY=15
MAX_MINUTE=2
MAX_RESULTS=3

def policy():
    p=router.read_policy()
    rows=[t for t in p.get("tool_connections",[]) if t.get("id")=="tavily-search"]
    if len(rows)!=1: raise RuntimeError("Tavily connector unconfigured")
    return rows[0]

def ledger():
    db=sqlite3.connect(DB,timeout=15,isolation_level=None)
    db.execute("PRAGMA busy_timeout=15000")
    db.execute("CREATE TABLE IF NOT EXISTS requests(id INTEGER PRIMARY KEY, ts INTEGER, month TEXT, outcome TEXT, endpoint TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS cooldowns(provider TEXT PRIMARY KEY, until_epoch INTEGER, reason TEXT)")
    cols={x[1] for x in db.execute("PRAGMA table_info(requests)")}
    if "endpoint" not in cols:
        db.execute("ALTER TABLE requests ADD COLUMN endpoint TEXT")
    DB.chmod(0o600)
    return db

def state():
    s=policy()
    cred=SECRET.is_file() and not (SECRET.stat().st_mode & 0o077)
    db=ledger()
    now=time.gmtime()
    month=f"{now.tm_year:04}-{now.tm_mon:02}"
    used=db.execute("SELECT count(*) FROM requests WHERE month=?",(month,)).fetchone()[0]
    today=db.execute("SELECT count(*) FROM requests WHERE ts>=?",(int(time.time())//86400*86400,)).fetchone()[0]
    cooldown=db.execute("SELECT until_epoch FROM cooldowns WHERE provider='tavily-keyless'").fetchone()
    remaining=max(0,cooldown[0]-int(time.time())) if cooldown else 0
    db.close()
    return {"id":"tavily-search","enabled":bool(s.get("enabled",False)),
            "keyless_cooldown_seconds_remaining":remaining,
            "access_mode":"keyless" if s.get("keyless_mode",False) else "keyed",
            "public_only":bool(s.get("public_only",False)),
            "external_proprietary_service":True,
            "credential_present":cred,"used_this_month":used,"used_today":today,
            "conservative_monthly_request_cap":min(MAX_MONTHLY,int(s.get("conservative_monthly_credits",MAX_MONTHLY))),
            "conservative_daily_request_cap":MAX_DAY,
            "paid_fallback_allowed":False}

def check_public_query(query):
    if not isinstance(query,str) or not (2<=len(query.strip())<=220):
        raise ValueError("Search requires a public text query of 2 to 220 characters")
    if any(ord(c)<32 for c in query):
        raise ValueError("Invalid control character")
    # Conservative tripwires, not a complete DLP solution. Never forward
    # unreleased company plans, guest material or internal documents.
    if (re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",query) or
        re.search(r"\b(?:\+?\d[\s-]?){10,}\b",query) or
        re.search(r"\b(?:api.?key|password|private.?key|secret.?token|customer.?list|guest.?data)\b",query,re.I)):
        raise ValueError("Query may contain private or sensitive data")
    return query.strip()

def check_public_url(url):
    if not isinstance(url,str) or len(url)>800:
        raise ValueError("Extract requires a bounded public HTTPS URL")
    p=urllib.parse.urlsplit(url)
    host=(p.hostname or "").lower().rstrip(".")
    if p.scheme!="https" or not host or p.username or p.password or p.port not in (None,443):
        raise ValueError("Only public HTTPS URLs supported")
    if host in {"localhost","localhost.localdomain"} or host.endswith((".local",".internal",".localhost",".test",".invalid")) or "." not in host:
        raise ValueError("Non-public host not permitted")
    try: ipaddress.ip_address(host);raise ValueError("IP literals not permitted")
    except ValueError as e:
        if str(e)=="IP literals not permitted": raise
    if re.search(r"\b(token|password|apikey|secret|auth)=?",p.query,re.I):
        raise ValueError("URL contains credential-like query parameter")
    if any(ord(c)<32 for c in url):
        raise ValueError("Invalid URL")
    return url

def reserve(endpoint,s):
    db=ledger()
    ts=int(time.time())
    month=time.strftime("%Y-%m",time.gmtime(ts))
    db.execute("BEGIN IMMEDIATE")
    try:
        cooldown=db.execute("SELECT until_epoch FROM cooldowns WHERE provider='tavily-keyless'").fetchone()
        if cooldown and cooldown[0]>ts:
            raise RuntimeError("Tavily keyless temporarily rate-limited; retry after "+str(cooldown[0]-ts)+" seconds")
        total=db.execute("SELECT count(*) FROM requests WHERE month=?",(month,)).fetchone()[0]
        day=db.execute("SELECT count(*) FROM requests WHERE ts>=?",(ts//86400*86400,)).fetchone()[0]
        recent=db.execute("SELECT count(*) FROM requests WHERE ts>=?",(ts-60,)).fetchone()[0]
        if (total>=min(MAX_MONTHLY,int(s.get("conservative_monthly_credits",MAX_MONTHLY)))
            or day>=MAX_DAY or recent>=MAX_MINUTE):
            raise RuntimeError("Conservative Tavily keyless request limit reached")
        db.execute("INSERT INTO requests(ts,month,outcome,endpoint) VALUES(?,?,?,?)",(ts,month,"reserved",endpoint))
        id_=db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.commit()
        return db,id_
    except Exception:
        db.rollback()
        db.close()
        raise

def execute(endpoint,value):
    s=policy()
    if not s.get("enabled",False):
        raise RuntimeError("Tavily research disabled")
    keyless=s.get("keyless_mode") is True
    if keyless:
        if not (s.get("public_only") is True and s.get("external_search_service_disclosed") is True):
            raise RuntimeError("Tavily keyless must be public-only and disclosed")
        headers={"Content-Type":"application/json",
                 "X-Tavily-Access-Mode":"keyless",
                 "User-Agent":"BusinessHouseMatrixMarketing-Keyless/0.3"}
    else:
        if not (s.get("free_plan_confirmed") and s.get("service_terms_reviewed")
                and s.get("open_source_policy_exception_approved")):
            raise RuntimeError("Keyed Tavily plan and service review required")
        if not SECRET.is_file() or SECRET.stat().st_mode & 0o077:
            raise RuntimeError("Protected Tavily key required")
        headers={"Authorization":"Bearer "+SECRET.read_text().strip(),
                 "Content-Type":"application/json",
                 "User-Agent":"BusinessHouseMatrixMarketing/0.3"}
    if endpoint=="search":
        body={"query":check_public_query(value),"search_depth":"basic",
              "max_results":MAX_RESULTS,"include_answer":False,
              "include_raw_content":False,"include_images":False}
    elif endpoint=="extract":
        body={"urls":[check_public_url(value)],"extract_depth":"basic"}
    else:
        raise RuntimeError("Unsupported Tavily keyless endpoint")
    db,rid=reserve(endpoint,s)
    req=urllib.request.Request(ROOT_URL+"/"+endpoint,
          data=json.dumps(body).encode("utf-8"),headers=headers,method="POST")
    try:
        with urllib.request.urlopen(req,timeout=18) as response:
            data=json.load(response)
        if data.get("error"):
            err=data["error"]
            code=err.get("code","limit_or_provider_error") if isinstance(err,dict) else "error"
            raise RuntimeError("Tavily keyless response error: "+str(code)[:80])
        if endpoint=="search":
            rows=[]
            for item in data.get("results",[])[:MAX_RESULTS]:
                if isinstance(item,dict) and str(item.get("url","")).startswith("https://"):
                    rows.append({"title":str(item.get("title",""))[:180],
                                 "url":str(item["url"])[:700],
                                 "snippet":str(item.get("content",""))[:700]})
            result={"results":rows}
        else:
            rows=[]
            for item in data.get("results",[])[:1]:
                if isinstance(item,dict):
                    rows.append({"url":str(item.get("url",""))[:700],
                                 "content":str(item.get("raw_content",item.get("content","")))[:6000]})
            result={"extracted":rows}
        db.execute("UPDATE requests SET outcome='ok' WHERE id=?",(rid,))
        return {"provider":"tavily","mode":"keyless" if keyless else "free_keyed",
                "operation":endpoint,**result,"public_only":keyless,
                "source_verification_required":True,
                "untrusted_external_content":True,"paid_fallback":False}
    except urllib.error.HTTPError as exc:
        db.execute("UPDATE requests SET outcome=? WHERE id=?",("HTTP_"+str(exc.code),rid))
        if exc.code==429:
            retry=3600
            try:
                retry=max(300,min(3600,int(exc.headers.get("Retry-After","3600"))))
            except (ValueError,TypeError,AttributeError):
                pass
            db.execute("INSERT OR REPLACE INTO cooldowns(provider,until_epoch,reason) VALUES(?,?,?)",
                       ("tavily-keyless",int(time.time())+retry,"429"))
            raise RuntimeError("Tavily keyless HTTP 429; cooldown "+str(retry)+" seconds") from None
        raise RuntimeError("Tavily HTTP "+str(exc.code)) from None
    except (OSError,ValueError,RuntimeError) as exc:
        db.execute("UPDATE requests SET outcome='failed' WHERE id=?",(rid,))
        raise RuntimeError("Tavily request failed: "+str(exc)[:110]) from None
    finally:
        db.close()

def search(query):return execute("search",query)
def extract(url):return execute("extract",url)

def main():
    p=argparse.ArgumentParser()
    s=p.add_subparsers(dest="cmd",required=True)
    s.add_parser("status")
    a=s.add_parser("search");a.add_argument("query")
    e=s.add_parser("extract");e.add_argument("url")
    args=p.parse_args()
    try:
        if args.cmd=="status":res=state()
        elif args.cmd=="search":res=search(args.query)
        else:res=extract(args.url)
        print(json.dumps(res,indent=2))
    except (RuntimeError,ValueError,sqlite3.Error) as exc:
        print("RESEARCH_ERROR:",str(exc),file=sys.stderr)
        sys.exit(2)
if __name__=="__main__":main()
