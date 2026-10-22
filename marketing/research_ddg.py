#!/usr/bin/env python3
"""BHM DuckDuckGo-through-SearXNG controlled public research profile.

The only request target is a fixed Dell loopback SearXNG endpoint. No direct DDG
scraping, CAPTCHA bypass, identity spoofing, paid fallback or hidden provider switch.
Treat every returned title/snippet as untrusted discovery evidence.
"""
import json
import re
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError,URLError

LOCAL="http://127.0.0.1:18889/search"

def check_query(query):
    if (not isinstance(query,str) or not 2<=len(query.strip())<=180
        or any(ord(c)<32 for c in query)
        or re.search(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}",query,re.I)
        or re.search(r"\b(?:api.?key|password|bearer|private.?key|guest.?data)\b",query,re.I)):
        raise ValueError("invalid_or_sensitive_query")
    return query.strip()

def interpret(payload,query):
    if not isinstance(payload,dict) or not isinstance(payload.get("results"),list):
        raise ValueError("invalid_search_response")
    failures=payload.get("unresponsive_engines",[])
    challenge=any("captcha" in str(x).lower() for x in failures)
    results=[]
    for hit in payload["results"][:8]:
        if not isinstance(hit,dict) or str(hit.get("engine","")).lower()!="duckduckgo":continue
        link=str(hit.get("url",""))[:700]
        u=urlsplit(link)
        if u.scheme!="https" or not u.hostname or u.username or u.password:continue
        results.append({"url":link,"title":str(hit.get("title",""))[:150],
                        "snippet":str(hit.get("content",""))[:400],
                        "engine":"duckduckgo","facts_verified":False})
    return {"provider":"duckduckgo_via_local_searxng",
            "status":"observed" if results else "blocked_captcha" if challenge else "unavailable",
            "query":query,"results":results,"blocked_by_source":challenge,
            "fallback_used":False,"untrusted_public_content":True,
            "no_captcha_bypass":True,"publish_approval":False,"spend_approval":False}

def search(query):
    q=check_query(query)
    fixed=LOCAL+"?"+urlencode({"q":q,"format":"json","engines":"duckduckgo",
                               "safesearch":"1","language":"en"})
    try:
        with urlopen(Request(fixed,headers={"Accept":"application/json"}),timeout=20) as response:
            payload=json.loads(response.read(180000))
        return interpret(payload,q)
    except (HTTPError,URLError,TimeoutError,OSError,ValueError) as exc:
        return {"provider":"duckduckgo_via_local_searxng","status":"unavailable",
                "reason":type(exc).__name__,"query":q,"results":[],
                "fallback_used":False,"publish_approval":False,"spend_approval":False}
