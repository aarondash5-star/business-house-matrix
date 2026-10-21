#!/usr/bin/env python3
"""Read-only SearXNG CLI on Dell, callable via authorized Generic Linux SSH.

This is a *local* researcher and NOT a cross-host Marketing Brain connection.
Keeps URLs/summaries bounded, outputs audit-ready source citations.
"""
import argparse
from urllib.parse import urlencode,urlsplit
from urllib.request import Request,urlopen
import ipaddress
import json
import re
import sys

SOURCE="http://127.0.0.1:18889/search"
def search(query,limit=6):
    if not isinstance(query,str) or not 2<=len(query.strip())<=180 or any(ord(c)<32 for c in query):
        raise ValueError("Bad bounded public search query")
    if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",query):
        raise ValueError("Possible private email in query")
    if not 1<=limit<=10:raise ValueError("Bad result limit")
    url=SOURCE+"?"+urlencode({"q":query.strip(),"format":"json","safesearch":"1","language":"en"})
    req=Request(url,headers={"Accept":"application/json"})
    with urlopen(req,timeout=30) as response:
        data=json.loads(response.read(300000))
    if not isinstance(data.get("results"),list):raise RuntimeError("Unexpected SearXNG response")
    rows=[]
    for result in data["results"]:
        if len(rows)>=limit:break
        src=str(result.get("url",""))
        p=urlsplit(src)
        if p.scheme!="https" or not p.hostname:continue
        try:ipaddress.ip_address(p.hostname);continue
        except ValueError:pass
        rows.append({"title":str(result.get("title",""))[:160],
                     "url":src[:700],
                     "snippet":str(result.get("content",""))[:550],
                     "engine":str(result.get("engine",""))[:40]})
    return {"provider":"self-hosted-searxng","node":"dell-linux",
            "results":rows,"result_count":len(rows),
            "source_attribution_required":True,"untrusted_external_content":True,
            "automatic_publication":False}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--limit",type=int,default=6)
    x=p.parse_args()
    try:print(json.dumps(search(x.query,x.limit),ensure_ascii=False,indent=2))
    except Exception as e:
        print("SEARXNG_LOCAL_ERROR",type(e).__name__,str(e)[:150],file=sys.stderr)
        sys.exit(2)
