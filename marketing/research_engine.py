#!/usr/bin/env python3
"""BHM research evidence engine: guarded public HTTPS, no publishing or spending.
Standalone private CLI on Dell. Intentionally NOT exposed as a model URL tool.
Only validated, granted public domains may be read. All page text is untrusted.
"""
import argparse
import datetime as dt
import hashlib
import http.client
import ipaddress
import json
import os
import re
import socket
import sqlite3
import ssl
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

UA = "BusinessHouseMatrixResearch/1.2 (+public-research; no-auto-publish)"
MAX_BYTES = 512_000
MAX_TEXT = 30_000
TIMEOUT = 8
MAX_REDIRECTS = 3
INTERVAL_SECONDS = 5
STATUS = ("verified", "needs_review", "unavailable")
UTC = dt.timezone.utc

def now():
    return dt.datetime.now(UTC).isoformat()

def allowed_host(host, grants):
    return bool(host and host.lower().rstrip(".") in grants)

def validate_url(raw, grants):
    if not isinstance(raw, str) or len(raw)>1000:
        raise ValueError("invalid_url")
    try:
        u = urlsplit(raw)
        host = (u.hostname or "").rstrip(".").lower().encode("idna").decode("ascii")
        port = u.port
    except (ValueError, UnicodeError):
        raise ValueError("invalid_url") from None
    if (u.scheme.lower() != "https" or not host or port not in (None, 443)
            or u.username or u.password or not allowed_host(host, grants)
            or any(ch in raw for ch in ("\r", "\n", "\t", "\\"))):
        raise ValueError("domain_not_granted_or_non_https")
    try:
        ipaddress.ip_address(host)
        raise ValueError("ip_literal_not_allowed")
    except ValueError as exc:
        if str(exc) == "ip_literal_not_allowed":
            raise
    return urlunsplit(("https", host, u.path or "/", u.query, ""))

def resolve_global(host):
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError:
        raise ValueError("dns_unavailable") from None
    addresses = sorted({i[4][0] for i in infos})
    if not addresses or len(addresses) > 16:
        raise ValueError("dns_unavailable")
    if any(not ipaddress.ip_address(addr).is_global for addr in addresses):
        raise ValueError("ssrf_nonpublic_dns")
    return addresses

class PinnedHTTPS(http.client.HTTPSConnection):
    """TLS SNI/cert match hostname, but TCP connection uses vetted resolved IP."""
    def __init__(self, host, ip):
        super().__init__(host, port=443, timeout=TIMEOUT, context=ssl.create_default_context())
        self.ip = ip
    def connect(self):
        raw = socket.create_connection((self.ip, 443), timeout=TIMEOUT)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except BaseException:
            raw.close()
            raise

def request_once(url, grants, max_bytes=MAX_BYTES):
    safe = validate_url(url, grants)
    u = urlsplit(safe)
    addresses = resolve_global(u.hostname)
    # DNS is resolved once; connection is pinned to vetted IP (rebinding resistant).
    conn = PinnedHTTPS(u.hostname, addresses[0])
    try:
        path = (u.path or "/") + (("?" + u.query) if u.query else "")
        conn.request("GET", path, headers={"Host":u.hostname,"User-Agent":UA,
                     "Accept":"text/html,application/xhtml+xml,text/plain",
                     "Accept-Encoding":"identity","Connection":"close"})
        res = conn.getresponse()
        location = res.getheader("Location")
        content_type = (res.getheader("Content-Type") or "").split(";")[0].strip().lower()
        length = res.getheader("Content-Length")
        if length and length.isdecimal() and int(length) > max_bytes:
            raise ValueError("response_too_large")
        if res.status in (301,302,303,307,308):
            return {"status":res.status,"location":location}
        if res.status != 200:
            return {"status":res.status,"blocked":"http_"+str(res.status)}
        if content_type not in ("text/html","application/xhtml+xml","text/plain"):
            raise ValueError("non_html_response")
        data = res.read(max_bytes+1)
        if len(data)>max_bytes:
            raise ValueError("response_too_large")
        return {"status":200,"url":safe,"body":data,"content_type":content_type}
    finally:
        conn.close()

def follow(url, grants, max_bytes=MAX_BYTES):
    seen = set()
    for _ in range(MAX_REDIRECTS+1):
        safe = validate_url(url,grants)
        if safe in seen:
            raise ValueError("redirect_loop")
        seen.add(safe)
        resp = request_once(safe,grants,max_bytes)
        if resp["status"] not in (301,302,303,307,308):
            return resp
        if not resp.get("location"):
            raise ValueError("redirect_no_location")
        url=urljoin(safe,resp["location"])
        validate_url(url,grants)  # validate every hop before any DNS
    raise ValueError("too_many_redirects")

def check_robots(url,grants):
    u=urlsplit(validate_url(url,grants))
    robots_url="https://"+u.hostname+"/robots.txt"
    resp=follow(robots_url,grants,max_bytes=40_000)
    if resp["status"] in (404,410):
        return True
    if resp["status"]!=200:
        return False  # fail closed on robots outage / denial
    rules=RobotFileParser()
    rules.parse(resp["body"].decode("utf-8","replace").splitlines())
    return rules.can_fetch(UA,url)

class Meta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical=""
        self.title=""
        self.in_title=False
        self.scripts=[]
        self.schema=False
        self.buffer=""
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title":
            self.in_title=True
        if tag=="link" and a.get("rel","").lower()=="canonical":
            self.canonical=a.get("href","")[:1000]
        if tag=="script" and a.get("type","").lower()=="application/ld+json":
            self.schema=True
            self.buffer=""
    def handle_data(self,data):
        if self.in_title and len(self.title)<300:
            self.title+=data
        if self.schema and len(self.buffer)<15000:
            self.buffer+=data[:15000-len(self.buffer)]
    def handle_endtag(self,tag):
        if tag=="title":
            self.in_title=False
        if tag=="script" and self.schema:
            try:
                self.scripts.append(json.loads(self.buffer))
            except (ValueError,TypeError):
                pass
            self.schema=False

def safe_schema(scripts):
    """Store only selected public JSON-LD facts, never arbitrary embedded scripts."""
    out=[]
    def visit(x,depth=0):
        if depth>3 or len(out)>=12:
            return
        if isinstance(x,list):
            for v in x[:12]:
                visit(v,depth+1)
        if isinstance(x,dict):
            if "@graph" in x:
                visit(x["@graph"],depth+1)
            kind=str(x.get("@type",""))[:100]
            if kind:
                d={"type":kind}
                for key in ("name","description","price","priceCurrency","availability","url"):
                    val=x.get(key)
                    if isinstance(val,(str,int,float)):
                        d[key]=str(val)[:260]
                if isinstance(x.get("offers"),(dict,list)):
                    offer=x["offers"]
                    if isinstance(offer,list):offer=offer[0] if offer else {}
                    if isinstance(offer,dict):
                        d["offers"]={k:str(offer[k])[:160] for k in ("price","priceCurrency","url") if isinstance(offer.get(k),(str,int,float))}
                out.append(d)
    visit(scripts)
    return out

def extract_html(body,url,grants):
    try:
        import trafilatura
    except ImportError:
        raise RuntimeError("trafilatura_not_installed") from None
    html=body.decode("utf-8","replace")
    parsed=Meta()
    parsed.feed(html[:MAX_BYTES])
    canonical=url
    if parsed.canonical:
        try:
            canonical=validate_url(urljoin(url,parsed.canonical),grants)
        except ValueError:
            canonical=url
    result=trafilatura.extract(html,output_format="json",with_metadata=True,
                              include_comments=False,include_tables=True)
    data=json.loads(result) if result else {}
    text=(data.get("text") or "").strip()[:MAX_TEXT]
    if len(text)<45:
        return {"status":"unavailable","reason":"insufficient_page_body","source_url":url}
    title=str(data.get("title") or parsed.title or "").strip()[:200]
    return {"status":"needs_review","source_url":url,"canonical_url":canonical,
            "title":title,"text":text,"excerpt":text[:220],
            "sha256":hashlib.sha256(body).hexdigest(),
            "observed_utc":now(),"content_bytes":len(body),
            "schema":safe_schema(parsed.scripts),"untrusted_external_text":True,
            "facts_verified":False}

def connect(dbpath):
    p=Path(dbpath)
    p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    db=sqlite3.connect(str(p),timeout=10)
    db.execute("PRAGMA busy_timeout=5000")
    db.executescript("""
      CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY, applied_utc TEXT NOT NULL);
      INSERT OR IGNORE INTO schema_migrations VALUES(1,datetime('now'));
      CREATE TABLE IF NOT EXISTS research_run(id INTEGER PRIMARY KEY, topic TEXT, started_utc TEXT, status TEXT);
      CREATE TABLE IF NOT EXISTS source(id INTEGER PRIMARY KEY, canonical_url TEXT UNIQUE, source_url TEXT,
        title TEXT, first_seen TEXT, last_seen TEXT, digest TEXT, status TEXT);
      CREATE TABLE IF NOT EXISTS business_entity(id INTEGER PRIMARY KEY, canonical_domain TEXT UNIQUE,
        name TEXT, role TEXT, reviewed INTEGER DEFAULT 0);
      CREATE TABLE IF NOT EXISTS source_entity_link(source_id INTEGER,entity_id INTEGER,
        PRIMARY KEY(source_id,entity_id));
      CREATE TABLE IF NOT EXISTS claim(id INTEGER PRIMARY KEY,source_id INTEGER,entity_id INTEGER,
        kind TEXT,value TEXT,currency TEXT,unit TEXT,observed_utc TEXT,
        status TEXT,quote TEXT,UNIQUE(source_id,kind,value));
      CREATE TABLE IF NOT EXISTS observation_history(id INTEGER PRIMARY KEY,source_id INTEGER,
        observed_utc TEXT,digest TEXT,change_type TEXT);
      CREATE TABLE IF NOT EXISTS review_queue(id INTEGER PRIMARY KEY,claim_id INTEGER,
        reason TEXT,status TEXT DEFAULT 'pending');
      CREATE TABLE IF NOT EXISTS crawl_attempt(id INTEGER PRIMARY KEY,url TEXT,host TEXT,
        observed_utc TEXT,outcome TEXT);
      CREATE VIRTUAL TABLE IF NOT EXISTS source_search USING fts5(title,url,excerpt,
        tokenize='unicode61');
    """)
    return db

def last_crawl(db,host):
    row=db.execute("SELECT observed_utc FROM crawl_attempt WHERE host=? ORDER BY id DESC LIMIT 1",(host,)).fetchone()
    if not row:return None
    try:return dt.datetime.fromisoformat(row[0])
    except ValueError:return None

def record_attempt(db,url,outcome):
    db.execute("INSERT INTO crawl_attempt(url,host,observed_utc,outcome) VALUES(?,?,?,?)",
               (url,urlsplit(url).hostname,now(),outcome))
    db.commit()

def fetch_extract(url,grants,db):
    safe=validate_url(url,grants)
    host=urlsplit(safe).hostname
    previous=last_crawl(db,host)
    if previous and (dt.datetime.now(UTC)-previous).total_seconds()<INTERVAL_SECONDS:
        return {"status":"unavailable","reason":"domain_rate_limit","source_url":safe}
    # Book a domain slot before network; robots is fetched without infinite recursion.
    record_attempt(db,safe,"started")
    try:
        if not check_robots(safe,grants):
            record_attempt(db,safe,"robots_denied")
            return {"status":"unavailable","reason":"robots_denied","source_url":safe}
        resp=follow(safe,grants)
        if resp["status"]!=200:
            record_attempt(db,safe,"http_"+str(resp["status"]))
            return {"status":"unavailable","reason":"http_"+str(resp["status"]),"source_url":safe}
        result=extract_html(resp["body"],resp["url"],grants)
        record_attempt(db,safe,result["status"])
        return result
    except (OSError,TimeoutError,ssl.SSLError,ValueError,RuntimeError,http.client.HTTPException) as exc:
        reason=str(exc)[:80] if isinstance(exc,(ValueError,RuntimeError)) else type(exc).__name__
        record_attempt(db,safe,"unavailable:"+reason)
        return {"status":"unavailable","source_url":safe,"reason":reason}

def save_evidence(db,item):
    if item.get("status")!="needs_review":
        return {"stored":False,"reason":"no_page_evidence"}
    url=item["canonical_url"]
    prior=db.execute("SELECT id,digest FROM source WHERE canonical_url=?",(url,)).fetchone()
    change="first_seen" if not prior else "unchanged" if prior[1]==item["sha256"] else "content_changed_unverified"
    db.execute("""INSERT INTO source(canonical_url,source_url,title,first_seen,last_seen,digest,status)
      VALUES(?,?,?,?,?,?,?) ON CONFLICT(canonical_url) DO UPDATE SET source_url=excluded.source_url,
      title=excluded.title,last_seen=excluded.last_seen,digest=excluded.digest,status=excluded.status""",
      (url,item["source_url"],item["title"],item["observed_utc"],item["observed_utc"],item["sha256"],"needs_review"))
    sid=db.execute("SELECT id FROM source WHERE canonical_url=?",(url,)).fetchone()[0]
    db.execute("INSERT INTO observation_history(source_id,observed_utc,digest,change_type) VALUES(?,?,?,?)",
               (sid,item["observed_utc"],item["sha256"],change))
    db.execute("DELETE FROM source_search WHERE rowid=?",(sid,))
    db.execute("INSERT INTO source_search(rowid,title,url,excerpt) VALUES(?,?,?,?)",
               (sid,item["title"],url,item["excerpt"]))
    # Schema offers are leads only; no price is automatically verified.
    for row in item["schema"]:
        offer=row.get("offers",{})
        if not offer or not offer.get("price"):
            continue
        price=str(offer["price"])[:70]
        cur=str(offer.get("priceCurrency",""))[:12]
        db.execute("""INSERT OR IGNORE INTO claim(source_id,kind,value,currency,unit,observed_utc,status,quote)
          VALUES(?,?,?,?,?,?,?,?)""",(sid,"displayed_price",price,cur,"unspecified",
          item["observed_utc"],"needs_review",item["excerpt"][:180]))
    db.commit()
    return {"stored":True,"source_id":sid,"change":change,
            "verified":False,"requires_review":True}

def packet(db,topic):
    rows=db.execute("""SELECT s.id,s.canonical_url,s.title,s.last_seen,s.status
      FROM source_search f JOIN source s ON s.id=f.rowid
      WHERE source_search MATCH ? LIMIT 12""",(topic.replace('"',"").split()[0] if topic.strip() else "wellness",)).fetchall()
    leads=[{"source_id":a,"url":b,"title":c,"last_seen":d,"status":e} for a,b,c,d,e in rows]
    return {"type":"bhm_research_packet","version":"1.2-dev","topic":topic,
            "created_utc":now(),"market_map":{"status":"needs_review","leads":leads},
            "verified_competitors":[],"unverified_leads":leads,
            "source_backed_ux_references":[],"pricing_table":[],
            "gsc_opportunities":{"status":"adapter_unchanged_read_only","site_data_only":True},
            "trends":{"local_time_series":"unknown","rss_news_not_search_volume":True},
            "unresolved_questions":["Verify service/provider identity and exact pricing using official pages",
                                    "Review citations before Design uses any market claim"],
            "evidence_confidence":"unverified","required_visual_brand_constraints":
             ["real Moksha site photography","mobile-first layout","no production booking edits"],
            "approved_for_design_claims":False,"publish_approval":False,"spend_approval":False}

def validate_draft(draft):
    required=("market_map","verified_competitors","unverified_leads","source_backed_ux_references",
              "pricing_table","gsc_opportunities","unresolved_questions",
              "required_visual_brand_constraints")
    missing=[x for x in required if x not in draft]
    if missing:return {"valid":False,"reason":"missing_sections","sections":missing}
    if draft.get("verified_competitors") and any(
       not x.get("evidence_urls") or not x.get("reviewed") for x in draft["verified_competitors"]):
        return {"valid":False,"reason":"uncited_or_unreviewed_competitor"}
    if draft.get("approved_for_design_claims") and not draft.get("reviewer"):
        return {"valid":False,"reason":"reviewer_required"}
    return {"valid":True,"facts_promoted":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",default=str(Path.home()/".local/share/bhm-research/evidence.sqlite3"))
    p.add_argument("--grants",default="mokshagoa.com,www.mokshagoa.com,example.org,www.w3.org")
    sub=p.add_subparsers(dest="cmd",required=True)
    e=sub.add_parser("extract");e.add_argument("url")
    v=sub.add_parser("inspect");v.add_argument("url")
    s=sub.add_parser("search");s.add_argument("query")
    k=sub.add_parser("packet");k.add_argument("topic")
    args=p.parse_args()
    grants={x.strip().lower() for x in args.grants.split(",") if x.strip()}
    if args.cmd=="inspect":
        print(json.dumps({"url":validate_url(args.url,grants),"ip_addresses":resolve_global(urlsplit(args.url).hostname)},indent=2))
        return
    db=connect(args.db)
    try:
        if args.cmd=="extract":
            result=fetch_extract(args.url,grants,db)
            if result["status"]=="needs_review":
                result["store"]=save_evidence(db,result)
                result.pop("text",None)  # CLI receipt contains only bounded excerpt/metadata
        elif args.cmd=="search":
            rows=db.execute("""SELECT s.canonical_url,s.title,s.status,s.last_seen
               FROM source_search f JOIN source s ON s.id=f.rowid WHERE source_search MATCH ? LIMIT 15""",
               (args.query,)).fetchall()
            result={"results":[dict(zip(("url","title","status","last_seen"),r)) for r in rows],
                    "read_only":True}
        else:
            result=packet(db,args.topic)
            result["completeness"]=validate_draft(result)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    finally:
        db.close()

if __name__=="__main__":
    main()
