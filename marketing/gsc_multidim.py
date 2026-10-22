#!/usr/bin/env python3
"""Strict GSC dimension importer for APPROVED read-only engagement-core reports.
No OAuth, network, global volume claims, or changes to the active gsc_metrics adapter.
"""
import datetime as dt
import hashlib
import json
import sqlite3
from pathlib import Path
from zoneinfo import ZoneInfo

DIMENSIONS=["query","page","country","device","date"]
PACIFIC=ZoneInfo("America/Los_Angeles")
UTC=dt.timezone.utc

def validate(report,approved_property):
    if not isinstance(report,dict) or report.get("site")!=approved_property:
        raise ValueError("unapproved_site")
    if report.get("dimensions")!=DIMENSIONS:
        raise ValueError("required_five_dimensions")
    if report.get("source")!="engagement_core_read_only":
        raise ValueError("unapproved_source")
    start=dt.date.fromisoformat(report["start_date"])
    end=dt.date.fromisoformat(report["end_date"])
    if end<start or end>dt.datetime.now(PACIFIC).date():
        raise ValueError("bad_date_window")
    page_size=int(report.get("row_limit",25000))
    start_row=int(report.get("start_row",0))
    if not (1<=page_size<=25000 and 0<=start_row<=1000000):
        raise ValueError("pagination_out_of_bounds")
    rows=report.get("rows")
    if not isinstance(rows,list) or len(rows)>page_size:
        raise ValueError("invalid_rows")
    for r in rows:
        keys=r.get("keys")
        if not isinstance(keys,list) or len(keys)!=5:
            raise ValueError("wrong_dimension_tuple")
        if not isinstance(keys[0],str) or not str(keys[1]).startswith("https://"):
            raise ValueError("invalid_query_or_page")
        day=dt.date.fromisoformat(keys[4])
        if not start<=day<=end:
            raise ValueError("row_outside_window")
        if keys[3] not in ("DESKTOP","MOBILE","TABLET"):
            raise ValueError("invalid_device")
        for m in ("clicks","impressions","ctr","position"):
            n=r.get(m)
            if not isinstance(n,(int,float)) or isinstance(n,bool) or n<0:
                raise ValueError("invalid_metric")
        if r["clicks"]>r["impressions"] or not 0<=r["ctr"]<=1:
            raise ValueError("metric_invariant")
    return {"valid":True,"rows":len(rows),"complete_page":len(rows)<page_size,
            "next_start_row":start_row+len(rows),
            "settled":end<=dt.datetime.now(PACIFIC).date()-dt.timedelta(days=3),
            "date_timezone":"America/Los_Angeles"}

def db_open(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    c=sqlite3.connect(str(p))
    c.executescript("""
       CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY,applied_utc TEXT);
       INSERT OR IGNORE INTO schema_migrations VALUES(1,datetime('now'));
       CREATE TABLE IF NOT EXISTS import_batch(id INTEGER PRIMARY KEY,site TEXT,source_digest TEXT UNIQUE,
         start_date TEXT,end_date TEXT,start_row INTEGER,row_count INTEGER,imported_utc TEXT);
       CREATE TABLE IF NOT EXISTS gsc_observation(site TEXT,query TEXT,page TEXT,country TEXT,device TEXT,
         event_date_pacific TEXT,clicks REAL,impressions REAL,ctr REAL,position REAL,
         batch_id INTEGER,PRIMARY KEY(site,query,page,country,device,event_date_pacific,batch_id));
    """)
    return c

def import_report(conn,report,site):
    summary=validate(report,site)
    encoded=json.dumps(report,sort_keys=True,ensure_ascii=False).encode()
    digest=hashlib.sha256(encoded).hexdigest()
    if conn.execute("SELECT 1 FROM import_batch WHERE source_digest=?",(digest,)).fetchone():
        return {**summary,"status":"duplicate","inserted":0}
    stamp=dt.datetime.now(UTC).isoformat()
    with conn:
        cursor=conn.execute("""INSERT INTO import_batch(site,source_digest,start_date,end_date,start_row,
           row_count,imported_utc) VALUES(?,?,?,?,?,?,?)""",
           (site,digest,report["start_date"],report["end_date"],report.get("start_row",0),len(report["rows"]),stamp))
        n=cursor.lastrowid
        for r in report["rows"]:
            q,page,country,device,day=r["keys"]
            conn.execute("""INSERT INTO gsc_observation VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
               (site,q,page,country,device,day,r["clicks"],r["impressions"],r["ctr"],r["position"],n))
    return {**summary,"status":"imported","inserted":len(report["rows"]),
            "site_only":True,"not_global_search_volume":True,
            "capture_utc":stamp}

def compare(conn,site,day_a,day_b,limit=10):
    if not 1<=limit<=10:raise ValueError("max_limit_10")
    sql="""SELECT query,page,country,device,event_date_pacific,clicks,impressions
             FROM gsc_observation WHERE site=? AND event_date_pacific IN (?,?)
             ORDER BY batch_id DESC LIMIT 10000"""
    latest={}
    for q,page,country,device,day,clicks,imp in conn.execute(sql,(site,day_a,day_b)):
        latest.setdefault((q,page,country,device,day),(clicks,imp))
    buckets={}
    for (q,page,country,device,day),val in latest.items():
        buckets.setdefault((q,page,country,device),{})[day]=val
    out=[]
    for key,v in buckets.items():
        if day_a not in v or day_b not in v:continue
        out.append({"query":key[0],"page":key[1],"country":key[2],"device":key[3],
                    "click_delta":v[day_b][0]-v[day_a][0],
                    "impression_delta":v[day_b][1]-v[day_a][1]})
    return {"site_only":True,"timezone":"America/Los_Angeles",
            "deltas":sorted(out,key=lambda x:abs(x["impression_delta"]),reverse=True)[:limit],
            "unknown_if_missing":True}
