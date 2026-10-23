#!/usr/bin/env python3
"""Private-only GSC query+page+Pacific date importer from connected read-only WP Manager.
Explicitly NOT a five-dimensional query/page/country/device/date report.
No OAuth, publishing, or API calls; separate from active gsc_metrics.py.
"""
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit

PROPERTY="https://mokshagoa.com/"
DIMENSIONS=["query","page","date"]
PRIVATE=re.compile(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}",re.I)

def validate(payload):
    if not isinstance(payload,dict) or payload.get("source")!="google-search-console-direct":
        raise ValueError("unapproved_gsc_source")
    if payload.get("property")!=PROPERTY or payload.get("dimensions")!=DIMENSIONS:
        raise ValueError("unapproved_property_or_dimensions")
    start=dt.date.fromisoformat(payload["start_date"])
    end=dt.date.fromisoformat(payload["end_date"])
    if end<start or (end-start).days>90:
        raise ValueError("invalid_date_window")
    rows=payload.get("rows")
    if not isinstance(rows,list) or len(rows)>250 or not rows:
        raise ValueError("invalid_rows")
    clean=[]
    for row in rows:
        keys=row.get("keys")
        if not isinstance(keys,list) or len(keys)!=3:
            raise ValueError("invalid_dimensions")
        query,page,date=keys
        if not isinstance(query,str) or len(query)>180 or PRIVATE.search(query):
            raise ValueError("pii_or_unbounded_query")
        u=urlsplit(page)
        if u.scheme!="https" or u.netloc not in ("mokshagoa.com","www.mokshagoa.com"):
            raise ValueError("unapproved_landing_page")
        event_date=dt.date.fromisoformat(date)
        if not start<=event_date<=end:raise ValueError("row_outside_range")
        values=[row.get(k) for k in ("clicks","impressions","ctr","position")]
        if any(type(v) not in (int,float) or v<0 for v in values):
            raise ValueError("invalid_metrics")
        clicks,impressions,ctr,position=values
        if clicks>impressions or ctr>1:raise ValueError("invalid_ctr")
        clean.append((query,page,date,*values))
    return clean

def import_report(payload,path):
    rows=validate(payload)
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    digest=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    db=sqlite3.connect(p)
    os.chmod(p,0o600)
    try:
        db.executescript("""CREATE TABLE IF NOT EXISTS batches(digest TEXT PRIMARY KEY, imported_utc TEXT,
            start_date TEXT,end_date TEXT,row_count INTEGER);
        CREATE TABLE IF NOT EXISTS observations(digest TEXT,query TEXT,page TEXT,pacific_date TEXT,
           clicks REAL,impressions REAL,ctr REAL,position REAL,
           PRIMARY KEY(digest,query,page,pacific_date));""")
        if db.execute("SELECT 1 FROM batches WHERE digest=?",(digest,)).fetchone():
            return {"status":"duplicate","rows":0,"dimension_coverage":"query,page,date only"}
        with db:
            db.execute("INSERT INTO batches VALUES(?,?,?,?,?)",(digest,
                dt.datetime.now(dt.timezone.utc).isoformat(),
                payload["start_date"],payload["end_date"],len(rows)))
            db.executemany("INSERT INTO observations VALUES(?,?,?,?,?,?,?,?)",
                [(digest,*x) for x in rows])
        return {"status":"imported","rows":len(rows),"read_only":True,
                "source":"connected_engagement_core_read_only",
                "date_basis":"Search Console Pacific calendar dates",
                "dimension_coverage":"query,page,date only",
                "country":"unknown","device":"unknown",
                "does_not_measure_global_search_volume":True}
    finally:
        db.close()
