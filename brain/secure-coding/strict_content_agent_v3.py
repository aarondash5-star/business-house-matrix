#!/usr/bin/env python3
"""Narrow offline model→validated content→Bubblewrap QA→local-review pilot.

Models produce *content only*, never paths, code tools, commands or test programs.
The existing reviewed_patch_runner and source_governor independently enforce scope.
No credential access, network, remote Git push, daemon edit or private Pine source.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
TASK = "pine_chat_b1_synthetic_review_v1"
PROJECT = "pine_mcp_chat"
MODEL = Path.home() / ".local/bin/matrix-pi-local"
STATE = HERE / "autonomous-code-state" / TASK
APP = "frontend/pine-chat-a11y.html"
TEST = "tests/test_pine_chat_a11y.py"
MAX_ATTEMPTS = 2
TEST_SOURCE = '''import unittest
from pathlib import Path
class PineChatIndependent(unittest.TestCase):
 def test_semantics(self):
  s=Path("frontend/pine-chat-a11y.html").read_text(encoding="utf-8").lower()
  for x in ('<html lang="en"','name="viewport"','<main','pine','chat'):
   self.assertIn(x,s)
 def test_offline(self):
  s=Path("frontend/pine-chat-a11y.html").read_text(encoding="utf-8").lower()
  for x in ("<script","<iframe","http://","https://","fetch(","websocket"):
   self.assertNotIn(x,s)
'''

def load_source(name):
    p=HERE/name
    spec=importlib.util.spec_from_file_location("reviewed_"+name.replace(".","_"),p)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def unpack(raw):
    """Prefer one-key structured model output; never allow model-selected paths."""
    raw=raw.strip()
    if len(raw)>12000: raise ValueError("model_output_too_large")
    mark=chr(96)*3
    if raw.startswith(mark): raw=raw.partition("\n")[2].rsplit(mark,1)[0].strip()
    try: obj=json.loads(raw)
    except (json.JSONDecodeError,ValueError):
        a=raw.find("{");z=raw.rfind("}")
        if a<0 or z<=a: raise ValueError("proposal_not_json")
        obj=json.loads(raw[a:z+1])
    if not isinstance(obj,dict) or set(obj)!={"html"} or not isinstance(obj["html"],str):
        raise ValueError("proposal_schema_denied")
    return obj["html"]

def repair_known_markup(raw):
    """One deterministic *markup-only* correction. Reject active content first."""
    if not isinstance(raw,str) or not 120<=len(raw.encode("utf-8"))<=5800:
        raise ValueError("markup_size_denied")
    lower=raw.lower()
    blocked=(r"<\s*(?:script|iframe|object|embed|form|base|link)\b",
             r"\b(?:https?://|fetch\s*\(|websocket|xmlhttprequest|localstorage|sessionstorage)\b",
             r"\b(?:password|api[_-]?key|service_role|private.?key|bearer)\b",
             r"\bon\w+\s*=",r"javascript\s*:",r"<\s*meta\b[^>]*http-equiv")
    if any(re.search(p,raw,re.I) for p in blocked):
        raise ValueError("active_or_secret_content_denied")
    if not re.search(r"<!doctype\s+html",raw,re.I) or not re.search(r"<html\b",raw,re.I):
        raise ValueError("html_document_required")
    # The v2 pilot failed on a missing main landmark. Exact bounded repair only.
    if not re.search(r"<main(?:\s|>)",raw,re.I):
        opening=re.search(r"<body(?:\s[^>]*)?>",raw,re.I)
        closing=re.search(r"</body\s*>",raw,re.I)
        if not opening or not closing or closing.start()<=opening.end():
            raise ValueError("missing_main_nonrepairable")
        raw=raw[:opening.end()]+"<main>"+raw[opening.end():closing.start()]+"</main>"+raw[closing.start():]
    if not re.search(r'<html\s+lang="en"',raw,re.I):
        raw=re.sub(r"<html\s*>",'<html lang="en">',raw,count=1,flags=re.I)
    if 'name="viewport"' not in raw.lower():
        raw=re.sub(r"<head(?:\s[^>]*)?>",lambda m:m.group(0)+'<meta name="viewport" content="width=device-width,initial-scale=1">',raw,count=1,flags=re.I)
    if not re.search(r"<main(?:\s|>)",raw,re.I):
        raise ValueError("missing_main")
    return raw

def payload(html):
    gate=load_source("source_governor.py")
    envelope={
        "project":gate.PROJECT,"manifest":gate.MANIFEST,
        "work_id":gate.WORK_ID,"repository":gate.REPOSITORY,
        "base_branch":gate.BASE_BRANCH,
        "files":[{"path":APP,"content":repair_known_markup(html)},
                 {"path":TEST,"content":TEST_SOURCE}],
    }
    output=gate.inspect(envelope)
    if output["status"]!="needs_independent_review" or output["approved"] or output["executed"]:
        raise RuntimeError("proposal_governance_failed")
    return output

def model_only(prompt):
    if not MODEL.is_file():raise RuntimeError("local_model_not_installed")
    cmd=[str(MODEL),"--no-tools","--no-mcp","--no-extensions",
         "--no-skills","--no-prompt-templates","--no-context-files",
         "--no-session","--no-approve","--offline","--model","granite4:3b",
         "--thinking","off","--system-prompt","Return only valid JSON with exactly one key html.",
         "--print",prompt]
    env={"HOME":str(Path.home()),"PATH":"/usr/local/bin:/usr/bin:/bin",
         "PI_TELEMETRY":"0","PI_SKIP_VERSION_CHECK":"1",
         "OLLAMA_HOST":"http://127.0.0.1:11434"}
    response=subprocess.run(cmd,capture_output=True,text=True,input="",
                            env=env,timeout=110)
    if response.returncode:raise RuntimeError("offline_model_nonzero")
    return unpack(response.stdout)

def run():
    if STATE.exists():raise RuntimeError("one_attempt_per_manifest_no_replay")
    STATE.mkdir(parents=True,mode=0o700)
    result={"task":TASK,"project":PROJECT,"status":"blocked","published":False,
            "private_pine_access":False,"spend":False,"model_tool_calls":False,
            "attempts":[]}
    try:
        runner=load_source("scoped_dev_pilot.py")
        probe=runner.isolated("doctor")
        if probe.get("passed") is not True:raise RuntimeError("sandbox_isolation_denied")
        inventory=runner.isolated("inventory").get("files",[])
        if any(item["path"] in (APP,TEST) for item in inventory):
            raise RuntimeError("existing_target_denied")
        template=(
          'Generate a small original HTML5 synthetic Pine Engineer Chat landing page. '
          'Reply ONLY JSON with one key "html", a string containing the COMPLETE '
          '<!doctype html><html lang="en"><head><meta name="viewport" '
          'content="width=device-width,initial-scale=1"><title>Pine Chat</title>'
          '</head><body><main> ... </main></body></html> document. '
          'A mobile-friendly accessible static chat sample with a heading, 2 example '
          'messages and inline CSS; no JavaScript, external links, APIs, trades, forms, '
          'network calls or secrets. Plain text examples only. Keep under 1600 characters.'
        )
        approved=None
        for attempt in range(1,MAX_ATTEMPTS+1):
            try:
                html=model_only(template)
                approved=payload(html)
                result["attempts"].append({"iteration":attempt,"validation":"passed",
                                           "review_sha256":approved["review_sha256"]})
                break
            except (ValueError,RuntimeError) as err:
                # Never log untrusted output or secrets.
                reason=type(err).__name__ if isinstance(err,RuntimeError) else str(err)[:70]
                result["attempts"].append({"iteration":attempt,"validation":"blocked",
                                           "reason":reason})
        if approved is None:raise RuntimeError("bounded_model_validation_exhausted")
        patch=STATE/"governed-patch.json"
        # File stays in private 0700 directory; exact paths and expected SHA validated.
        patch.write_text(json.dumps(approved["payload"],separators=(",",":")),encoding="utf-8")
        patch.chmod(0o600)
        applied=runner.isolated("apply",patch)
        written=applied.get("written",[])
        if set(x.get("path") for x in written)!={APP,TEST}:
            raise RuntimeError("scope_mismatch_after_apply")
        qa=runner.isolated("test")
        result["qa"]=qa
        if qa.get("passed") is not True or qa.get("tests_executed") is not True:
            raise RuntimeError("isolated_unit_tests_failed")
        review=runner.local_review(TASK,written,qa)
        if review.get("published") is not False or set(review.get("files",[]))!={APP,TEST}:
            raise RuntimeError("local_review_contract_failed")
        result.update(status="verified_local_review",review=review,sandbox=probe["detail"],
                      source_governor_sha256=approved["review_sha256"])
    except Exception as err:
        result["error"]={"type":type(err).__name__,"reason":str(err)[:120]}
    result["finished_utc"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    (STATE/"receipt.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    return result

if __name__=="__main__":
    try:
        if sys.argv!=[sys.argv[0],TASK]: raise ValueError("work_id_not_enrolled")
        receipt=run()
        print(json.dumps({k:v for k,v in receipt.items() if k not in ("source","payload")}))
        sys.exit(0 if receipt["status"]=="verified_local_review" else 2)
    except Exception as err:
        print(json.dumps({"status":"blocked","reason":type(err).__name__}))
        sys.exit(2)
