#!/usr/bin/env python3
"""Tavily research connector prepared for the Matrix Marketing Brain.

Search is OFF pending OSI/vendor terms review and Free-plan enrollment.
No shared-model router modifications, no arbitrary URL execution or scraping.
"""
import argparse
import getpass
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
import urllib.error
import urllib.request

import router

ROOT=Path(__file__).resolve().parent
DB=ROOT/"research-quota.sqlite3"
SECRET=ROOT/"secrets"/"tavily-search.key"
SEARCH_URL="https://api.tavily.com/search"
MAX_MONTHLY=100 # 10% of Tavily advertised 1000/month free tier; local guard
MAX_MINUTE=2
MAX_RESULTS=5

def policy():
    p=router.read_policy()
    rows=[t for t in p.get("tool_connections",[]) if t.get("id")=="tavily-search"]
    if len(rows)!=1:raise RuntimeError("Tavily connector unconfigured")
    return rows[0]

def ledger():
    db=sqlite3.connect(DB,timeout=15,isolation_level=None)
    db.execute("PRAGMA busy_timeout=15000")
    db.execute("CREATE TABLE IF NOT EXISTS requests(id INTEGER PRIMARY KEY, ts INTEGER, month TEXT, outcome TEXT)")
    DB.chmod(0o600)
    return db

def state():
    s=policy()
    cred=SECRET.is_file() and not (SECRET.stat().st_mode & 0o077)
    d=ledger()
    now=time.gmtime()
    month=f"{now.tm_year:04}-{now.tm_mon:02}"
    used=d.execute("SELECT count(*) FROM requests WHERE month=?",(month,)).fetchone()[0]
    d.close()
    return {"id":"tavily-search","enabled":bool(s.get("enabled",False)),
            "license_review_required":not bool(s.get("service_terms_reviewed",False)),
            "free_plan_confirmed":bool(s.get("free_plan_confirmed",False)),
            "credential_present":cred,"used_this_month":used,
            "conservative_monthly_cap":min(MAX_MONTHLY,int(s.get("conservative_monthly_credits",MAX_MONTHLY))),
            "paid_fallback_allowed":False}

def enroll():
    # Do not request/collect secrets until the legal and open-source gate is cleared.
    s=policy()
    if not (s.get("service_terms_reviewed") and s.get("free_plan_confirmed")):
        raise RuntimeError("Tavily terms/open-source-policy review and Free plan confirmation required")
    if not sys.stdin.isatty():raise RuntimeError("interactive hidden prompt required")
    if SECRET.exists():raise RuntimeError("credential already present, rotate explicitly")
    val=getpass.getpass("Tavily Researcher Free key (hidden): ").strip()
    if len(val)<12:raise RuntimeError("credential too short")
    SECRET.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    fd=os.open(SECRET,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,"w") as f:f.write(val+"\n")
    return {"enrolled":True,"enabled":False}

def search(query):
    s=policy()
    if not (s.get("enabled") and s.get("service_terms_reviewed") and
            s.get("free_plan_confirmed")):
        raise RuntimeError("Tavily search disabled pending Free plan and service policy review")
    if not SECRET.is_file() or SECRET.stat().st_mode & 0o077:
        raise RuntimeError("No protected Tavily credential")
    if not isinstance(query,str) or not query.strip() or len(query)>220:
        raise ValueError("Bounded text query required")
    d=ledger()
    ts=int(time.time())
    now=time.gmtime(ts)
    month=f"{now.tm_year:04}-{now.tm_mon:02}"
    d.execute("BEGIN IMMEDIATE")
    try:
        total=d.execute("SELECT count(*) FROM requests WHERE month=?",(month,)).fetchone()[0]
        recent=d.execute("SELECT count(*) FROM requests WHERE ts>=?",(ts-60,)).fetchone()[0]
        if total>=min(MAX_MONTHLY,int(s.get("conservative_monthly_credits",MAX_MONTHLY))) or recent>=MAX_MINUTE:
            raise RuntimeError("Conservative research credit limit reached")
        d.execute("INSERT INTO requests(ts,month,outcome) VALUES(?,?,?)",(ts,month,"reserved"))
        rid=d.execute("SELECT last_insert_rowid()").fetchone()[0]
        d.commit()
    except:
        d.rollback()
        raise
    body={"query":query,"search_depth":"basic","max_results":MAX_RESULTS,
          "include_answer":False,"include_raw_content":False,"include_images":False}
    req=urllib.request.Request(SEARCH_URL,data=json.dumps(body).encode(),
      headers={"Authorization":"Bearer "+SECRET.read_text().strip(),
               "Content-Type":"application/json"},
      method="POST")
    try:
        with urllib.request.urlopen(req,timeout=18) as response:
            data=json.load(response)
        urls=[]
        for x in data.get("results",[])[:MAX_RESULTS]:
            if isinstance(x,dict) and str(x.get("url","")).startswith(("https://","http://")):
                urls.append({"title":str(x.get("title",""))[:180],
                             "url":str(x["url"])[:600],
                             "snippet":str(x.get("content",""))[:650]})
        d.execute("UPDATE requests SET outcome='ok' WHERE id=?",(rid,))
        return {"provider":"tavily","results":urls,"requires_source_verification":True,
                "may_be_untrusted_web_content":True,"paid_fallback":False}
    except urllib.error.HTTPError as exc:
        d.execute("UPDATE requests SET outcome=? WHERE id=?",("HTTP_"+str(exc.code),rid))
        raise RuntimeError("Tavily HTTP "+str(exc.code)) from None
    except (ValueError,OSError):
        d.execute("UPDATE requests SET outcome='failed' WHERE id=?",(rid,))
        raise RuntimeError("Tavily request failed") from None

def main():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="cmd",required=True)
    sp.add_parser("status");sp.add_parser("enroll")
    s=sp.add_parser("search");s.add_argument("query")
    a=p.parse_args()
    if a.cmd=="status":print(json.dumps(state(),indent=2))
    elif a.cmd=="enroll":print(json.dumps(enroll()))
    else:print(json.dumps(search(a.query),indent=2))
if __name__=="__main__":
    try: main()
    except (RuntimeError,ValueError,sqlite3.Error) as e:
        print("RESEARCH_ERROR:",str(e),file=sys.stderr);sys.exit(2)
