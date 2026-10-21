#!/usr/bin/env python3
"""Private LAN-only SearXNG gateway: authenticated by fixed source IP.

MVP network boundary: 192.168.0.103:18888, only Mac 192.168.0.106.
Port must not be forwarded or exposed to the public internet.
"""
from collections import deque
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
import threading
import time
from urllib.parse import parse_qs,urlsplit,urlencode
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

BIND="192.168.0.103"
MAC_IP="192.168.0.106"
PORT=18888
LOCAL_ENGINE="http://127.0.0.1:18889"
MAX_PER_MINUTE=4
LIMIT_BODY=192000
recent=deque()
lock=threading.Lock()

class Gateway(BaseHTTPRequestHandler):
    server_version="BHM-SearXNG-LANGateway/0.1"
    def log_message(self,fmt,*args):
        # Avoid logging full queries or private data.
        print("gateway",time.strftime("%FT%T%z"),self.client_address[0],args[0] if args else "",flush=True)
    def send(self,code,data):
        body=json.dumps(data,ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.client_address[0] not in ("127.0.0.1",MAC_IP):
            self.send(403,{"error":"forbidden"});return
        u=urlsplit(self.path)
        if u.path=="/health":
            self.send(200,{"ok":True,"engine":"searxng","private":True});return
        if u.path!="/search":
            self.send(404,{"error":"not_found"});return
        args=parse_qs(u.query,keep_blank_values=False)
        if set(args)-{"q","format","language","safesearch","time_range","pageno"}:
            self.send(400,{"error":"unrecognized_search_parameter"});return
        q=args.get("q",[""])[0]
        if not 2<=len(q)<=180 or args.get("format")!=["json"]:
            self.send(400,{"error":"invalid_query"});return
        if args.get("language",["en"])[0] not in ("en","all"):
            self.send(400,{"error":"invalid_language"});return
        with lock:
            now=time.monotonic()
            while recent and recent[0]<now-60: recent.popleft()
            if len(recent)>=MAX_PER_MINUTE:
                self.send(429,{"error":"local_limit"});return
            recent.append(now)
        params={"q":q,"format":"json","language":args.get("language",["en"])[0],
                "safesearch":"1","pageno":"1"}
        if args.get("time_range",[""])[0] in ("day","month","year"):
            params["time_range"]=args["time_range"][0]
        try:
            req=Request(LOCAL_ENGINE+"/search?"+urlencode(params),
                        headers={"Accept":"application/json","User-Agent":"BHM-research-gateway/0.1"})
            with urlopen(req,timeout=28) as r:
                body=r.read(LIMIT_BODY+1)
                if len(body)>LIMIT_BODY:raise ValueError("oversized response")
                data=json.loads(body)
                if not isinstance(data,dict) or not isinstance(data.get("results"),list):
                    raise ValueError("bad search response")
            self.send(200,{"results":data["results"][:12],
                           "number_of_results":data.get("number_of_results",0)})
        except HTTPError as e:
            self.send(502,{"error":"upstream_http","status":e.code})
        except (URLError,TimeoutError,ValueError,OSError):
            self.send(502,{"error":"upstream_unavailable"})

if __name__=="__main__":
    server=ThreadingHTTPServer((BIND,PORT),Gateway)
    print("BHM private SearXNG gateway, local-network only",flush=True)
    server.serve_forever(poll_interval=0.5)
