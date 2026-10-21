#!/usr/bin/env python3
"""Local-only, read-only Search Console evidence store and opt-in API ingestion.

GSC Search Analytics is first-party property performance, NOT trend volume.
Only an explicit verified property and bounded date-window are accepted.
Credentials and observations stay on the Mac; code contains no tokens.
"""
import argparse
import csv
from datetime import date, datetime, timedelta, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
DB = BASE / "data" / "gsc-metrics.sqlite3"
INBOX = BASE / "gsc-inbox"
SECRETS = BASE / "secrets" / "gsc-readonly.json"
MAX_FILE = 1024 * 1024
MAX_ROWS = 2500
PRIVATE = re.compile(r"(?i)(?:[\w.+-]+@[\w.-]+\.[a-z]{2,}|\b(?:password|otp|api.?key|secret|access.?token)\b|\+?\d[\d\s-]{9,}\d)")
TERMS = re.compile(r"[a-z0-9]{3,}", re.I)


def property_id(value):
    if not isinstance(value, str) or len(value) > 240 or not value:
        raise ValueError("Explicit Search Console property required")
    if value.startswith("sc-domain:"):
        host = value[10:]
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9.-]{2,200}", host) or "." not in host:
            raise ValueError("Invalid GSC domain property")
        return value
    u = urlsplit(value)
    if u.scheme != "https" or not u.hostname or u.username or u.password or u.port or u.query or u.fragment:
        raise ValueError("Only exact https:// Search Console URL-prefix property allowed")
    if u.hostname in ("localhost", "127.0.0.1") or "." not in u.hostname:
        raise ValueError("Non-public property rejected")
    return value


def days(start, end):
    try:
        a, b = date.fromisoformat(start), date.fromisoformat(end)
    except (TypeError, ValueError):
        raise ValueError("Dates must be ISO YYYY-MM-DD") from None
    if b < a or (b-a).days > 92 or b > date.today():
        raise ValueError("Search Analytics window must be in the past, at most 93 days")
    return a.isoformat(), b.isoformat()


def db():
    DB.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    c = sqlite3.connect(DB, timeout=15)
    c.execute("PRAGMA busy_timeout=15000")
    c.execute("""CREATE TABLE IF NOT EXISTS batches(
        batch TEXT PRIMARY KEY, site TEXT NOT NULL, start TEXT NOT NULL,
        end TEXT NOT NULL, source TEXT NOT NULL, imported TEXT NOT NULL,
        rows_count INTEGER NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS observations(
        batch TEXT NOT NULL, query TEXT NOT NULL, clicks REAL NOT NULL,
        impressions REAL NOT NULL, ctr REAL NOT NULL, position REAL NOT NULL,
        PRIMARY KEY(batch,query), FOREIGN KEY(batch) REFERENCES batches(batch))""")
    c.commit()
    DB.chmod(0o600)
    return c


def _metric(row):
    q = str(row.get("query", row.get("Query", ""))).strip()[:180]
    if not 3 <= len(q) <= 180 or PRIVATE.search(q):
        return None
    try:
        clicks = float(row.get("clicks", row.get("Clicks", 0)))
        imp = float(row.get("impressions", row.get("Impressions", 0)))
        ctr = str(row.get("ctr", row.get("CTR", "0"))).strip()
        ctr = float(ctr.rstrip("%")) / (100 if ctr.endswith("%") else 1)
        pos = float(row.get("position", row.get("Position", 0)))
    except (TypeError, ValueError):
        return None
    if not all(map(math.isfinite, (clicks, imp, ctr, pos))):
        return None
    if not (0 <= clicks <= imp <= 1e10 and 0 <= ctr <= 1 and 0 <= pos <= 1000):
        return None
    return (q, clicks, imp, ctr, pos)


def save_rows(rows, *, site, start, end, source, digest):
    site = property_id(site)
    start, end = days(start, end)
    if source not in ("gsc_csv_export", "google_gsc_searchanalytics_api"):
        raise ValueError("Unsupported evidence source")
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise ValueError("Bounded rows required")
    clean = [v for r in rows if isinstance(r, dict) if (v := _metric(r)) is not None]
    # GSC's grouped Search Analytics rows include a unique query per source batch.
    clean = list({r[0]: r for r in clean}.values())
    batch = hashlib.sha256((site + "|" + start + "|" + end + "|" + source + "|" + digest).encode()).hexdigest()[:32]
    c = db()
    try:
        c.execute("BEGIN IMMEDIATE")
        c.execute("INSERT OR REPLACE INTO batches VALUES(?,?,?,?,?,?,?)",
                  (batch, site, start, end, source, datetime.now(timezone.utc).isoformat(), len(clean)))
        c.execute("DELETE FROM observations WHERE batch=?", (batch,))
        c.executemany("INSERT INTO observations VALUES(?,?,?,?,?,?)",
                      [(batch, *r) for r in clean])
        c.commit()
    except Exception:
        c.rollback()
        raise
    finally:
        c.close()
    return {"status": "ingested", "batch": batch, "property": site, "start": start,
            "end": end, "rows": len(clean), "source": source, "private_local_only": True}


def import_csv(filename, site, start, end):
    if not isinstance(filename, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\.csv", filename):
        raise ValueError("Only a CSV basename in controlled inbox allowed")
    src = INBOX / filename
    if src.is_symlink() or not src.is_file() or src.stat().st_size > MAX_FILE:
        raise ValueError("CSV unavailable, symlinked or oversized")
    raw = src.read_bytes()
    records = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if len(records) > MAX_ROWS:
        raise ValueError("GSC export exceeds 2500 rows")
    return save_rows(records, site=site, start=start, end=end,
                     source="gsc_csv_export", digest=hashlib.sha256(raw).hexdigest())


def fetch_api(start, end):
    """Opt-in, read-only live Search Analytics. No Google credentials exist by default.

    The private file must include explicit site_url, client_id, client_secret,
    refresh_token and scope=...webmasters.readonly; never print these.
    """
    if SECRETS.is_symlink() or not SECRETS.is_file() or SECRETS.stat().st_mode & 0o077:
        raise RuntimeError("Read-only GSC OAuth not configured in owner-only secret file")
    c = json.loads(SECRETS.read_text())
    if c.get("scope") != "https://www.googleapis.com/auth/webmasters.readonly":
        raise RuntimeError("Read-only OAuth scope assertion is required")
    site = property_id(c.get("site_url"))
    start, end = days(start, end)
    for field in ("client_id", "client_secret", "refresh_token"):
        if not isinstance(c.get(field), str) or not c[field].strip():
            raise RuntimeError("Incomplete read-only GSC OAuth enrollment")
    post = urlencode({k: c[k] for k in ("client_id", "client_secret", "refresh_token")}).encode() + b"&grant_type=refresh_token"
    req = Request("https://oauth2.googleapis.com/token", data=post,
                  headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    with urlopen(req, timeout=15) as res:
        result = json.load(io.BytesIO(res.read(16384)))
    if "https://www.googleapis.com/auth/webmasters.readonly" not in str(result.get("scope", c["scope"])).split():
        raise RuntimeError("Google token lacks read-only scope")
    access = result.get("access_token")
    if not isinstance(access, str) or not access:
        raise RuntimeError("Read-only Google OAuth token refresh unavailable")
    endpoint = "https://www.googleapis.com/webmasters/v3/sites/" + quote(site, safe="") + "/searchAnalytics/query"
    body = json.dumps({"startDate": start, "endDate": end, "dimensions": ["query"],
                       "rowLimit": 250, "dataState": "final"}).encode()
    req = Request(endpoint, data=body,
                  headers={"Authorization": "Bearer " + access, "Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=20) as res:
        response = json.load(io.BytesIO(res.read(MAX_FILE + 1)))
    rows = [{**r, "query": r.get("keys", [""])[0]} for r in response.get("rows", [])[:250]
            if isinstance(r, dict) and isinstance(r.get("keys"), list) and len(r["keys"]) == 1]
    return save_rows(rows, site=site, start=start, end=end, source="google_gsc_searchanalytics_api",
                     digest=hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest())


def status(site=None):
    if site is not None:
        site = property_id(site)
    conn = db()
    if site:
        batches = conn.execute("SELECT count(*),sum(rows_count),max(imported) FROM batches WHERE site=?", (site,)).fetchone()
    else:
        batches = conn.execute("SELECT count(*),sum(rows_count),max(imported) FROM batches").fetchone()
    conn.close()
    oauth = (SECRETS.exists() and not SECRETS.is_symlink() and not SECRETS.stat().st_mode & 0o077)
    return {"source": "google_search_console", "site": site, "oauth_configured": bool(oauth),
            "ingested_batches": batches[0], "stored_query_rows": batches[1] or 0,
            "last_imported_utc": batches[2], "read_only": True,
            "private_local_store": True, "paid_api": False}


def relevant(brief, *, site=None, limit=10):
    if site is not None:
        site = property_id(site)
    if not isinstance(brief, str) or not 2 <= len(brief.strip()) <= 3000:
        raise ValueError("Bounded research topic required")
    if not 1 <= limit <= 20:
        raise ValueError("Bounded GSC result limit required")
    if not site:
        return {"status": "property_not_selected", "site": None, "rows": [],
                "note": "Choose a verified property; no cross-property aggregation or hidden default."}
    c = db()
    batch = c.execute("SELECT batch,start,end,source,rows_count FROM batches WHERE site=? "
                      "ORDER BY imported DESC,batch DESC LIMIT 1", (site,)).fetchone()
    if batch is None:
        c.close()
        return {"status": "no_property_data", "site": site, "rows": [],
                "note": "No genuine Search Analytics observations in local store."}
    rows = c.execute("SELECT query,clicks,impressions,ctr,position FROM observations WHERE batch=?",
                     (batch[0],)).fetchall()
    c.close()
    tokens = set(TERMS.findall(brief.lower()))
    out = []
    for query, clicks, impressions, ctr, position in rows:
        hit = sorted(set(TERMS.findall(query.lower())) & tokens)
        if not hit:
            continue
        out.append({"query": query, "clicks": clicks, "impressions": impressions,
                    "ctr": ctr, "avg_position": position, "matched_terms": hit,
                    "source": "Google Search Console: Search Analytics"})
    out.sort(key=lambda x: (len(x["matched_terms"]), x["impressions"]), reverse=True)
    return {"status": "observed", "site": site, "start": batch[1], "end": batch[2],
            "source": batch[3], "batch": batch[0], "rows": out[:limit],
            "time_basis": "Search Console Pacific Time; settled data",
            "note": "Per-query real property metrics, not global search volume. Rows are top-limited; no summation to site totals."}


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("status"); s.add_argument("--site")
    x = sub.add_parser("brief"); x.add_argument("topic"); x.add_argument("--site")
    x = sub.add_parser("import-csv"); x.add_argument("filename"); x.add_argument("--site", required=True); x.add_argument("--start", required=True); x.add_argument("--end", required=True)
    x = sub.add_parser("fetch-api"); x.add_argument("--start", required=True); x.add_argument("--end", required=True)
    a = p.parse_args()
    try:
        if a.command == "status": ans = status(a.site)
        elif a.command == "brief": ans = relevant(a.topic, site=a.site)
        elif a.command == "import-csv": ans = import_csv(a.filename, a.site, a.start, a.end)
        else: ans = fetch_api(a.start, a.end)
        print(json.dumps(ans, ensure_ascii=False, indent=2))
    except (ValueError, RuntimeError, OSError, sqlite3.Error) as e:
        print("GSC_ERROR:", str(e)[:220], file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
