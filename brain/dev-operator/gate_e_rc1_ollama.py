#!/usr/bin/env python3
"""Fixed-loopback Ollama JSON proposer for RC1 non-sensitive public tasks.

No proxy, redirect, external host, model-selected command or filesystem access.
The enclosing gate_e_runtime.bounded() enforces cancellation and wall time.
"""
import json
import sys
import urllib.request

URL="http://127.0.0.1:11434/api/generate"
MODEL="qwen3:4b-instruct"
MAX_PROMPT=22000
MAX_RESPONSE=60000

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def request_payload(prompt):
    if not isinstance(prompt,str) or len(prompt.encode("utf-8"))>MAX_PROMPT:
        raise ValueError("model_prompt_size")
    schema={"type":"object","properties":{
        "summary":{"type":"string"},
        "files":{"type":"array","maxItems":8,"items":{"type":"object","properties":{
            "path":{"type":"string"},"content":{"type":"string"}},
            "required":["path","content"],"additionalProperties":False}}},
        "required":["summary","files"],"additionalProperties":False}
    return {"model":MODEL,"stream":False,"format":schema,
            "system":"Return ONLY correct JSON. You are a bounded offline coding proposer. Never write tests, shell commands or credentials.",
            "prompt":prompt,
            "options":{"temperature":0.1,"num_ctx":4096,"num_predict":2100,
                       "num_thread":2,"seed":2319},
            "keep_alive":"0"}

def propose(prompt, opener=None):
    data=json.dumps(request_payload(prompt),separators=(",",":")).encode()
    req=urllib.request.Request(URL,data=data,headers={
        "Content-Type":"application/json","Accept":"application/json"},
        method="POST")
    if opener is None:
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    with opener.open(req,timeout=95) as response:
        if response.status!=200:
            raise ValueError("local_model_status")
        raw=response.read(MAX_RESPONSE+1)
        if len(raw)>MAX_RESPONSE:
            raise ValueError("local_model_response_too_large")
    envelope=json.loads(raw)
    if not isinstance(envelope,dict) or envelope.get("model") not in (
           MODEL,MODEL+":latest"):
        raise ValueError("model_identity_mismatch")
    generated=envelope.get("response")
    if not isinstance(generated,str) or len(generated.encode())>34000:
        raise ValueError("model_output_size")
    proposal=json.loads(generated)
    if not isinstance(proposal,dict) or set(proposal)!={"summary","files"}:
        raise ValueError("model_json_schema")
    # The outer independently enforced enrollment policy still validates
    # every path, content limit and trusted immutable test source.
    return proposal

if __name__=="__main__":
    try:
        prompt=sys.stdin.read(MAX_PROMPT+1)
        print(json.dumps(propose(prompt),separators=(",",":")))
    except Exception as exc:
        print(json.dumps({"error":type(exc).__name__}),file=sys.stderr)
        sys.exit(2)
