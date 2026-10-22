#!/usr/bin/env python3
"""Moksha marketing research guard: scoped queries, relevance, provenance, no claims.
Research leads are never treated as verified businesses, sales or search volume.
No network use and no credentials in this module.
"""
import re
from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit

SERVICE = frozenset("sauna ice bath mud aloe wellness spa banya ritual therapy retreat retreats yoga recovery treatment treatments".split())
STRONG_SERVICE = frozenset("sauna ice mud aloe banya therapy retreat retreats yoga".split())
LOCATION = frozenset("goa arambol mandrem pernem ashvem morjim north".split())
UX = frozenset("booking website mobile ux conversion checkout reservation design navigation accessibility wcag speed performance".split())
FILLER = frozenset("the and with this that from into about where when best near for 2026 2025 2024 2023 marketing creative how seo people intent comparisons pricing website design mobile customer journey".split())
VALID_ENGINE = frozenset(("duckduckgo","google","bing","brave","startpage","qwant","mojeek","yahoo",""))
T = re.compile(r"[a-z][a-z0-9-]{1,}", re.I)
MAX_QUERIES = 3

def words(s):
    return {x.lower() for x in T.findall(str(s).lower()) if x.lower() not in FILLER}

def plan(topic):
    t = words(topic)
    local = bool(t & LOCATION) and bool(t & SERVICE)
    if local:
        tasks = [
            {"category":"local_services", "query":"Arambol Goa sauna ice bath wellness services"},
            {"category":"local_pricing", "query":"Goa sauna ice bath mud bath wellness booking prices"}
        ]
        if t & UX:
            tasks.append({"category":"website_ux_reference","query":"spa wellness mobile booking website user experience"})
        return tasks[:MAX_QUERIES]
    meaningful = [x for x in T.findall(topic) if x.lower() not in FILLER and not x.isdigit()]
    bounded = " ".join(meaningful[:9])[:160]
    return [{"category":"general_research","query":bounded or topic[:160]}]

def clean_url(raw):
    from ipaddress import ip_address
    u=urlsplit(str(raw).strip())
    if u.scheme!="https" or not u.hostname or u.username or u.password or u.port not in (None,443):
        return ""
    host=u.hostname.lower()
    if host=="localhost" or host.endswith((".local",".internal",".example")):
        return ""
    try:
        ip_address(host)
        return ""
    except ValueError:
        pass
    safe_params=[(k,v) for k,v in parse_qsl(u.query,keep_blank_values=False)
                 if not (k.lower().startswith("utm_") or k.lower() in ("fbclid","gclid","mc_cid","mc_eid","ref"))]
    result=urlunsplit(("https",host+("" if not u.port else ":443"),u.path.rstrip("/") or "/",urlencode(safe_params),""))
    return result[:800]

def judge(item,category):
    if not isinstance(item,dict):
        return None,"not_object"
    url=clean_url(item.get("url",""))
    if not url:
        return None,"invalid_url"
    title=str(item.get("title","")).strip()[:180]
    desc=str(item.get("snippet","")).strip()[:650]
    if len(title)<6 or not (desc or len(title)>20):
        return None,"missing_text"
    engine=str(item.get("engine","")).strip().lower()[:60]
    if engine and engine not in VALID_ENGINE:
        return None,"unknown_engine"
    text=(title+" "+desc+" "+urlsplit(url).path.replace("-"," ")+" "+urlsplit(url).hostname.replace("-"," ")).lower()
    terms=words(text)
    service=terms & SERVICE
    geography=terms & LOCATION
    evidence=""
    if category.startswith("local"):
        if not geography:
            return None,"not_goa_or_arambol"
        if not service:
            return None,"not_wellness_service"
        if not (service & STRONG_SERVICE) and not (len(service)>=2 or "book" in terms or "booking" in terms):
            return None,"generic_wellness_only"
        evidence="local_market_lead_not_verified_competitor"
    elif category=="website_ux_reference":
        if not (terms & UX) or not (terms & SERVICE):
            return None,"not_wellness_booking_ux"
        evidence="general_ux_reference_not_local_demand"
    else:
        evidence="unverified_public_research_lead"
    if urlsplit(url).hostname in ("mokshagoa.com","www.mokshagoa.com") or "moksha wellness" in text:
        evidence="own_brand_or_third_party_listing_not_competitor"
    return {"title":title,"url":url,"snippet":desc,"engine":engine,"category":category,
            "evidence_class":evidence,"verified_facts":False},None

def grade(plan_results):
    seen=set()
    kept=[];rejected=[];breakdown={}
    for chunk in plan_results:
        category=chunk["category"]
        for item in chunk.get("results",[]):
            scored,reason=judge(item,category)
            if reason:
                rejected.append({"category":category,"reason":reason,"title":str(item.get("title",""))[:100] if isinstance(item,dict) else ""})
                continue
            key=(urlsplit(scored["url"]).hostname,urlsplit(scored["url"]).path.rstrip("/").lower())
            if key in seen:
                rejected.append({"category":category,"reason":"duplicate_url","title":scored["title"][:100]})
                continue
            seen.add(key);kept.append(scored)
            breakdown[category]=breakdown.get(category,0)+1
    return {"results":kept[:15],"rejected":rejected[:30],
            "kept_count":len(kept),"rejected_count":len(rejected),
            "category_counts":breakdown, "policy":"Geo/service/UX topical evidence gate; relevance alone never verifies a factual claim"}

def trend_query(topic):
    # Drop years and uninformative website-build terms before matching news RSS.
    tokens=words(re.sub(r"\b(?:19|20)\d{2}\b"," ",topic))
    meaningful=[x for x in tokens if x in SERVICE or x in ("moksha","arambol","sauna","goa")]
    return " ".join(sorted(meaningful)) or "no matching subject"

def gsc_gate(data,topic):
    if not isinstance(data,dict) or data.get("status")!="observed":
        return data
    topic_terms=words(topic)
    allowed=SERVICE | frozenset(("moksha","arambol","goa","north"))
    high=STRONG_SERVICE | frozenset(("moksha","arambol","wellness"))
    selected=[]
    for row in data.get("rows",[]):
        query_terms=words(row.get("query",""))
        hits=topic_terms & query_terms & allowed
        if not hits or not hits & high:
            continue
        clean={**row,"matched_terms":sorted(hits)}
        selected.append(clean)
    out={**data,"rows":selected,"relevance_gate":"Brand/service-specific query matches only; not site totals or search volume",
         "filtered_total":len(data.get("rows",[]))-len(selected)}
    if not selected:
        out["status"]="no_relevant_queries"
    return out
