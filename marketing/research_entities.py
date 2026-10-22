#!/usr/bin/env python3
"""Deterministic entity/claim review controls for BHM research. Zero network access."""
import datetime as dt
import re
import unicodedata
from urllib.parse import urlsplit

DIRECTORIES=frozenset(("tripadvisor.com","getyourguide.com","bookmyshow.com","sortmyscene.com",
                       "airbnb.com","viator.com","booking.com","agoda.com","google.com"))
OWN_DOMAINS=frozenset(("mokshagoa.com","www.mokshagoa.com"))
UX_REFERENCE_DOMAINS=frozenset(("w3.org","developer.mozilla.org","web.dev","nngroup.com"))
STALE_DAYS={"displayed_price":7,"opening_hours":14,"service":30,"booking_path":14,"ux_reference":90}

def domain(url):
    try:return (urlsplit(url).hostname or "").lower()
    except ValueError:return ""

def same_or_subdomain(host,root):
    return host==root or host.endswith("."+root)

def normalize_name(name):
    text=unicodedata.normalize("NFKC",str(name)).casefold()
    return " ".join(re.findall(r"[\w]+",text,flags=re.UNICODE))[:140]

def classify(source_url,title,description="",owner_name="Moksha Wellness"):
    host=domain(source_url)
    if not host:return {"role":"unavailable","reason":"missing_host","competitor":False}
    label=normalize_name(title+" "+description)
    own=normalize_name(owner_name)
    is_own=all(part in label.split() for part in own.split())
    if any(same_or_subdomain(host,x) for x in UX_REFERENCE_DOMAINS):
        return {"role":"public_ux_guidance","competitor":False}
    if host in OWN_DOMAINS:
        return {"role":"first_party_own_brand","competitor":False}
    if is_own:
        return {"role":"third_party_own_brand_listing","competitor":False}
    if any(same_or_subdomain(host,x) for x in DIRECTORIES):
        return {"role":"third_party_directory_or_reseller","competitor":False}
    return {"role":"provider_candidate_needs_review","competitor":False}

def claim(kind,value,url,quote,observed_utc,currency="",units="",first_party=False):
    if kind not in STALE_DAYS:
        raise ValueError("unknown_claim_type")
    if not isinstance(url,str) or not url.startswith("https://") or not domain(url):
        raise ValueError("source_url_required")
    if not quote or len(quote.strip())<12:
        raise ValueError("direct_quote_required")
    if kind=="displayed_price":
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?",str(value)):
            raise ValueError("price_must_be_numeric")
        if currency not in ("INR","USD","EUR","GBP","RUB"):
            raise ValueError("currency_required")
    return {"type":kind,"value":str(value)[:180],"currency":currency,"units":units[:40],
            "source_url":url,"quote":quote[:220],"observed_utc":observed_utc,
            "first_party":bool(first_party),"status":"needs_review",
            "corroborated":False,"human_reviewed":False}

def stale(c,at=None):
    age=dt.datetime.fromisoformat(c["observed_utc"])
    if age.tzinfo is None:
        raise ValueError("timestamp_requires_timezone")
    now=at or dt.datetime.now(dt.timezone.utc)
    return (now-age).total_seconds()>STALE_DAYS.get(c.get("type"),7)*86400

def reconcile(claims):
    """Conflict is explicit, never average or silently select latest figure."""
    out=[]
    groups={}
    for c in claims:
        key=(normalize_name(c.get("entity","")),c.get("type"),c.get("units",""))
        groups.setdefault(key,[]).append(c)
    for k,items in groups.items():
        distinct={(x.get("value"),x.get("currency")) for x in items}
        out.append({"entity":k[0],"claim_type":k[1],"sources":[x["source_url"] for x in items],
                    "conflict":len(distinct)>1,"values":[{"value":v,"currency":currency} for v,currency in sorted(distinct)],
                    "status":"needs_review" if len(distinct)>1 else "unverified"})
    return out

def certify_claim(c,corroborating_urls,reviewer,at=None):
    """Require first-party observation, independent origin, human approval and freshness."""
    if not c.get("first_party") or stale(c,at=at):
        raise ValueError("fresh_first_party_evidence_required")
    own=domain(c["source_url"])
    distinct={domain(u) for u in corroborating_urls if str(u).startswith("https://")}
    if not any(host!=own and not same_or_subdomain(host,own) for host in distinct):
        raise ValueError("independent_corroboration_required")
    if not reviewer or len(reviewer.strip())<3:
        raise ValueError("reviewer_required")
    return {**c,"status":"verified","corroborated":True,"human_reviewed":True,
            "reviewer":reviewer[:80],"verification_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
            "corroborating_urls":list(corroborating_urls)[:5]}

def completeness(packet,min_citations=2):
    required=("market_map","verified_competitors","unverified_leads","pricing_table",
              "source_backed_ux_references","gsc_opportunities","unresolved_questions",
              "required_visual_brand_constraints")
    if not isinstance(packet,dict) or any(k not in packet for k in required):
        return {"pass":False,"reason":"missing_required_sections"}
    used=[x for x in packet.get("verified_competitors",[]) + packet.get("pricing_table",[])
          if isinstance(x,dict)]
    if any(not x.get("reviewed") or not x.get("evidence_urls") for x in used):
        return {"pass":False,"reason":"unreviewed_or_uncited_fact"}
    urls={u for x in used for u in x.get("evidence_urls",[]) if str(u).startswith("https://")}
    if used and len(urls)<min_citations:
        return {"pass":False,"reason":"insufficient_source_coverage"}
    if packet.get("truncated") or packet.get("provider_output_chars",1000)<500:
        return {"pass":False,"reason":"incomplete_provider_response"}
    return {"pass":True,"critical_facts":len(used),"source_urls":len(urls),
            "limitations":"No verification implied by empty reviewed claim set"}
