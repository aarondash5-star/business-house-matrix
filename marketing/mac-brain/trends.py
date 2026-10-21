#!/usr/bin/env python3
"""Google Trends signal store for Business House Matrix Marketing.

Inputs: Google's PUBLIC Trending Now RSS; genuine Google Trends Explore CSV exports.
No scraping internal endpoints, no Google auth, no Trends alpha API assumption.
Never interpret relative interest as absolute search volume or as design preference.
"""
import argparse
import csv
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sqlite3
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
DATABASE=ROOT/"data"/"google-trends.sqlite3"
INBOX=ROOT/"trends-inbox"
RSS_URL="https://trends.google.com/trending/rss?geo={geo}"
ALLOWED_GEO={"IN","US","GB","RU"}
MAX_RSS_BYTES=524288
MAX_CSV_BYTES=262144
MIN_SYNC_SECONDS=6*3600
MAX_DAILY_SYNCS=4
STOPWORDS=set("the and for from with this that into your what where when how best near around about today trends google india goa reel reels post content creative video marketing wellness".split())
TOKEN=re.compile(r"[\w]+",re.UNICODE)

def utcstamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def con():
    DATABASE.parent.mkdir(parents=True,mode=0o700,exist_ok=True)
    d=sqlite3.connect(DATABASE,timeout=20)
    d.execute("PRAGMA busy_timeout=15000")
    d.execute("""CREATE TABLE IF NOT EXISTS trending(
        geo TEXT NOT NULL, term TEXT NOT NULL, published TEXT NOT NULL,
        seen TEXT NOT NULL, approx_traffic TEXT NOT NULL DEFAULT '',
        source_url TEXT NOT NULL, related TEXT NOT NULL DEFAULT '[]',
        PRIMARY KEY(geo,term,published))""")
    d.execute("""CREATE TABLE IF NOT EXISTS index_points(
        comparison_id TEXT NOT NULL, geo TEXT NOT NULL, window TEXT NOT NULL,
        term TEXT NOT NULL, date_bucket TEXT NOT NULL,
        relative_index REAL, imported TEXT NOT NULL, source_filename TEXT NOT NULL,
        PRIMARY KEY(comparison_id,term,date_bucket))""")
    d.execute("""CREATE TABLE IF NOT EXISTS sync_attempts(
        id INTEGER PRIMARY KEY, geo TEXT NOT NULL, ts INTEGER NOT NULL,
        outcome TEXT NOT NULL)""")
    d.execute("CREATE INDEX IF NOT EXISTS ix_trending_seen ON trending(geo,published)")
    d.commit(); DATABASE.chmod(0o600)
    return d

def local_tokens(value):
    return {x for x in TOKEN.findall(value.lower()) if len(x)>=3 and x not in STOPWORDS}

def parse_rss(data,geo):
    if len(data)>MAX_RSS_BYTES:
        raise ValueError("Feed exceeds bounded size")
    root=ET.fromstring(data)
    if root.tag!="rss":
        raise ValueError("Not official RSS XML")
    result=[]
    for item in root.findall(".//item")[:70]:
        val=lambda tag:(item.findtext(tag) or "").strip()
        title=val("title")
        if not (2<=len(title)<=180):continue
        pub=val("pubDate")
        try:
            dt=parsedate_to_datetime(pub)
            if dt.tzinfo is None:continue
            pubtime=dt.astimezone(timezone.utc).isoformat(timespec="seconds")
        except (ValueError,TypeError,IndexError):
            continue
        # ht:approx_traffic is an approximate band from Trending Now,
        # never an exact volume and never the Explore 0-100 interest index.
        traffic=""
        related=[]
        for child in item:
            short=child.tag.rsplit("}",1)[-1]
            if short=="approx_traffic":traffic=(child.text or "").strip()[:30]
            if short=="news_item":
                for desc in child:
                    if desc.tag.rsplit("}",1)[-1]=="news_item_title":
                        related.append((desc.text or "").strip()[:150])
        result.append({"geo":geo,"term":title,"published":pubtime,
                       "approx_traffic":traffic,"related":related[:3],
                       "source_url":RSS_URL.format(geo=geo)})
    return result

def fetch_feed(geo):
    if geo not in ALLOWED_GEO:raise ValueError("Unapproved geo")
    req=Request(RSS_URL.format(geo=geo),
                headers={"User-Agent":"BusinessHouseMatrix-Trends/0.1 (public RSS research)",
                         "Accept":"application/rss+xml,application/xml,text/xml"})
    with urlopen(req,timeout=16) as response:
        body=response.read(MAX_RSS_BYTES+1)
    return parse_rss(body,geo)

def refresh(geo="IN",fetcher=None):
    if geo not in ALLOWED_GEO: raise ValueError("Unapproved geo")
    d=con();now=int(time.time())
    last=d.execute("SELECT ts FROM sync_attempts WHERE geo=? ORDER BY ts DESC LIMIT 1",(geo,)).fetchone()
    attempts=d.execute("SELECT count(*) FROM sync_attempts WHERE geo=? AND ts>=?",
                       (geo,now-86400)).fetchone()[0]
    if last and now-last[0]<MIN_SYNC_SECONDS:
        d.close()
        return {"status":"cached","geo":geo,"next_eligible_after_seconds":MIN_SYNC_SECONDS-(now-last[0])}
    if attempts>=MAX_DAILY_SYNCS:
        d.close()
        return {"status":"daily_limit","geo":geo,"next_eligible_after_seconds":86400}
    d.execute("INSERT INTO sync_attempts(geo,ts,outcome) VALUES(?,?,?)",(geo,now,"reserved"))
    rid=d.execute("SELECT last_insert_rowid()").fetchone()[0];d.commit()
    try:
        rows=(fetcher or fetch_feed)(geo)
        if not isinstance(rows,list):raise ValueError("Feed parser did not return list")
        seen=utcstamp()
        for entry in rows:
            d.execute("""INSERT INTO trending(geo,term,published,seen,approx_traffic,source_url,related)
                         VALUES(?,?,?,?,?,?,?)
                         ON CONFLICT(geo,term,published) DO UPDATE SET
                           seen=excluded.seen,approx_traffic=excluded.approx_traffic,
                           related=excluded.related""",
                      (geo,entry["term"],entry["published"],seen,entry.get("approx_traffic",""),
                       entry["source_url"],json.dumps(entry.get("related",[]),ensure_ascii=False)))
        d.execute("UPDATE sync_attempts SET outcome=? WHERE id=?",("ok",rid))
        d.commit()
        return {"status":"updated","geo":geo,"items":len(rows),
                "source":"google_trends_trending_now_rss","capture":seen}
    except Exception as exc:
        d.execute("UPDATE sync_attempts SET outcome=? WHERE id=?",("error",rid))
        d.commit()
        raise RuntimeError("Official Google Trends RSS unavailable: "+type(exc).__name__) from None
    finally:
        d.close()

def csv_columns(text):
    # Supports either a normalized Google Trends "interest over time" export
    # with a Day/Week/Month column and term columns, or a simple date,term,index
    # table. Never supply invented data as observations.
    lines=[line for line in text.splitlines() if line.strip()]
    for offset,line in enumerate(lines[:8]):
        head=next(csv.reader([line]))
        first=head[0].strip().lstrip("\ufeff").lower() if head else ""
        if first in ("day","week","month","date"):return list(csv.reader(lines[offset:]))
    raise ValueError("CSV must contain Day, Week, Month or Date header")

def import_csv(filename,geo="IN",window="user_export"):
    if geo not in ALLOWED_GEO:raise ValueError("Unapproved geography")
    if not isinstance(window,str) or not re.fullmatch(r"[A-Za-z0-9_\-]{1,48}",window):
        raise ValueError("Window must be a safe identifier")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\.csv",filename):
        raise ValueError("Filename must be safe CSV basename")
    src=INBOX/filename
    if src.is_symlink() or not src.is_file() or src.stat().st_size>MAX_CSV_BYTES:
        raise ValueError("CSV not present in controlled inbox or too large")
    raw=src.read_bytes()
    text=raw.decode("utf-8-sig")
    matrix=csv_columns(text)
    header=[x.strip() for x in matrix[0]]
    if len(header)<2 or len(header)>12:raise ValueError("Unsupported CSV width")
    is_long= len(header)==3 and header[1].strip().lower() in ("term","query","keyword") and header[2].strip().lower() in ("index","interest","relative_index")
    group=hashlib.sha256(raw+geo.encode()+window.encode()).hexdigest()[:20]
    rows=[]
    for row in matrix[1:1000]:
        if len(row)!=len(header):continue
        day=row[0].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:\s*-\s*\d{4}-\d{2}-\d{2})?",day):
            continue
        cols=[(row[1],row[2])] if is_long else list(zip(header[1:],row[1:]))
        for term,val in cols:
            term=term.strip().split(":")[0].strip()[:150]
            if not term:continue
            score=val.strip()
            if score in ("", "<1", "< 1"):continue
            try: number=float(score)
            except ValueError: continue
            if not (math.isfinite(number) and 0<=number<=100):continue
            rows.append((group,geo,window,term,day,number,utcstamp(),filename))
    if not rows:raise ValueError("No valid normalized observations; import rejected")
    d=con()
    d.executemany("""INSERT OR REPLACE INTO index_points
                     (comparison_id,geo,window,term,date_bucket,relative_index,imported,source_filename)
                     VALUES(?,?,?,?,?,?,?,?)""",rows)
    d.commit();d.close()
    return {"status":"imported","source":"google_trends_explore_csv",
            "comparison_id":group,"items":len(rows),"geo":geo,"window":window,
            "limitations":"0-100 normalized within source comparison; not absolute volume"}

def relevant(brief,term,related):
    b=local_tokens(brief)
    candidate=local_tokens(term+" "+" ".join(related))
    return len(b & candidate), sorted(b & candidate)

def brief_context(brief,geo="IN",limit=5):
    if geo not in ALLOWED_GEO:raise ValueError("Unapproved geo")
    if not isinstance(brief,str) or not brief.strip() or len(brief)>3000:
        raise ValueError("Bounded brief required")
    d=con()
    since=datetime.fromtimestamp(time.time()-48*3600,timezone.utc).isoformat(timespec="seconds")
    rows=d.execute("""SELECT term,published,approx_traffic,related,source_url
                      FROM trending WHERE geo=? AND published>=?
                      ORDER BY published DESC LIMIT 150""",(geo,since)).fetchall()
    selected=[]
    for term,published,traffic,related,source in rows:
        mentions=json.loads(related or "[]")
        hits,matched=relevant(brief,term,mentions)
        if hits:
            selected.append({"term":term[:100],"observed_utc":published,
                "approximate_traffic_band":traffic,
                "matched_context_tokens":matched,
                "source_url":source,"signal_type":"recent_trending_news_query",
                "matching_tokens_count":hits})
    selected.sort(key=lambda x:(x["matching_tokens_count"],x["observed_utc"]),reverse=True)
    selected=selected[:limit]
    # Historical index points are returned within single comparison groups.
    # Don't rank or merge indices from different exports/windows.
    historical=d.execute("""SELECT comparison_id,term,date_bucket,relative_index,window
                           FROM index_points WHERE geo=? ORDER BY imported DESC LIMIT 250""",(geo,)).fetchall()
    groups={}
    brief_terms=local_tokens(brief)
    for group,term,date,index,window in historical:
        if not (brief_terms & local_tokens(term)):continue
        bucket=groups.setdefault(group,{"comparison_id":group,"window":window,"series":{}})
        bucket["series"].setdefault(term,[]).append([date,index])
    d.close()
    for g in groups.values():
        for term,values in g["series"].items():
            g["series"][term]=list(reversed(values[:60]))
    return {"geo":geo,"rss_signal":selected,"historical_comparison_groups":list(groups.values())[:2],
            "no_verified_relevance":not bool(selected or groups),
            "source":"Google Trends (https://trends.google.com/)",
            "rss_scope":"national news-driven spikes; not Goa-specific search demand",
            "index_scope":"0-100 normalized within a single export/comparison group",
            "do_not_infer":["absolute monthly search volume","keyword conversion intent","Goa demand from India RSS","palette preference","font preference","creative conversion uplift"],
            "seo_use":"Use verified related phrases as research leads; validate with GSC and on-page context",
            "creative_use":"Trend evidence may guide topics, relevance and timing; never force irrelevant news or trend-jacking",
            "visual_design":"Use approved brand tokens, accessibility/readability and measured campaign outcomes; Trends alone cannot select colors or fonts",
            "source_attribution_required":True,
            "publish_approval":False}

def enrich(brief,geo="IN"):
    insight=brief_context(brief,geo,4)
    if insight["no_verified_relevance"]:return brief
    # This is untrusted data, not operational instructions.
    titles=[x["term"].replace("\n"," ")[:90] for x in insight["rss_signal"]]
    evidence=("Google Trends public RSS signals (untrusted search terms, IN national, last 48h): "+
              json.dumps(titles,ensure_ascii=False))
    if insight["historical_comparison_groups"]:
        evidence+="; CSV comparison groups exist—read separately; values are relative."
    return brief+"\n\n"+evidence[:1000]+(
        "\nUse these only if relevant to the original topic. Do not copy arbitrary news. "
        "Search popularity is not absolute volume, and does not dictate colors/fonts. "
        "Do not claim data shows consumer preference without corroboration.")

def status():
    d=con()
    n=d.execute("SELECT count(*) FROM trending").fetchone()[0]
    h=d.execute("SELECT count(*) FROM index_points").fetchone()[0]
    newest=d.execute("SELECT max(seen) FROM trending").fetchone()[0]
    attempts=d.execute("SELECT count(*) FROM sync_attempts").fetchone()[0]
    d.close()
    return {"enabled":True,"rss_source":"public_official_google_trends",
            "rss_geos_allowed":sorted(ALLOWED_GEO),
            "rss_observations":n,"historical_index_points":h,
            "last_rss_observed_utc":newest,"sync_attempts":attempts,
            "official_api_alpha_granted":False,"cost_allowed":False,
            "brand_colors_fonts_from_trends":False}

def main():
    ap=argparse.ArgumentParser(description="Official Google Trends public-data ingestion and conservative modeling")
    sp=ap.add_subparsers(dest="cmd",required=True)
    sp.add_parser("status")
    rr=sp.add_parser("refresh");rr.add_argument("--geo",choices=sorted(ALLOWED_GEO),default="IN")
    bb=sp.add_parser("brief");bb.add_argument("topic");bb.add_argument("--geo",choices=sorted(ALLOWED_GEO),default="IN")
    ii=sp.add_parser("import-csv");ii.add_argument("filename");ii.add_argument("--geo",choices=sorted(ALLOWED_GEO),default="IN");ii.add_argument("--window",default="user_export")
    args=ap.parse_args()
    try:
        if args.cmd=="status":result=status()
        elif args.cmd=="refresh":result=refresh(args.geo)
        elif args.cmd=="brief":result=brief_context(args.topic,args.geo)
        else:result=import_csv(args.filename,args.geo,args.window)
        print(json.dumps(result,indent=2,ensure_ascii=False))
    except (ValueError,RuntimeError,sqlite3.Error,ET.ParseError) as exc:
        print("TRENDS_ERROR:",str(exc),file=sys.stderr);sys.exit(2)
if __name__=="__main__":main()
