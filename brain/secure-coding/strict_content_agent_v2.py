#!/usr/bin/env python3
"""Restricted model-content pilot: model selects no paths, tests, commands or tools."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
TASK="pine_content_guarded_v2"
MODEL=Path.home()/".local/bin/matrix-pi-local"
APP="frontend/pine-content-demo-v2.html"
TEST="tests/test_pine_content_demo_v2.py"
TEST_SRC='''import unittest
from pathlib import Path
class PineContentSmoke(unittest.TestCase):
 def test_accessibility(self):
  src=Path("frontend/pine-content-demo-v2.html").read_text().lower()
  self.assertIn("viewport",src)
  self.assertIn("<main",src)
  self.assertIn("pine",src)
  self.assertIn("chat",src)
'''
def port():
 spec=importlib.util.spec_from_file_location("reviewed_pilot",HERE/"scoped_dev_pilot.py")
 module=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(module)
 return module
def extract(raw):
 raw=raw.strip()
 fence=chr(96)*3
 if raw.startswith(fence):raw=raw.partition("\n")[2].rsplit(fence,1)[0]
 try:
  obj=json.loads(raw)
 except json.JSONDecodeError:
  a=raw.find("{");b=raw.rfind("}")
  if a>=0 and b>a:obj=json.loads(raw[a:b+1])
  else:obj={"html":raw}
 if isinstance(obj,dict) and isinstance(obj.get("html"),str):return obj["html"]
 if isinstance(obj,dict) and isinstance(obj.get("files"),list):
  texts=[x.get("content") for x in obj["files"] if isinstance(x,dict) and isinstance(x.get("content"),str) and ("<html" in x.get("content","").lower() or "<main" in x.get("content","").lower())]
  if len(texts)==1:return texts[0]
 raise ValueError("unrecognized_proposal_schema")
def validate(html):
 if not isinstance(html,str) or len(html)<100 or len(html)>8000:raise ValueError("html_size")
 txt=html.lower()
 for term in ("<html","viewport","<main","pine","chat"):
  if term not in txt:raise ValueError("missing_"+term.strip("<"))
 for pat in (r"\bfetch\s*\(",r"XMLHttpRequest",r"WebSocket",r"<script[^>]+src=",r"\bhttps?://",r"\b(?:eval|new Function)\s*\(",r"\b(?:localStorage|sessionStorage)\b"):
  if re.search(pat,html,re.I):raise ValueError("unsafe_content")
 return html
def run():
 p=port()
 state=HERE/"autonomous-code-state"/TASK
 if state.exists():raise RuntimeError("task_already_attempted")
 state.mkdir(parents=True,mode=0o700)
 result={"task":TASK,"project":"pine_mcp_chat","published":False,"status":"blocked"}
 try:
  d=p.isolated("doctor")
  if not d.get("passed"):raise RuntimeError("sandbox_gate_failed")
  prompt='Reply with a compact JSON object with ONE key "html". Its value is a complete self-contained responsive accessible HTML page with title Pine Engineer Chat, viewport meta, main element, and a static synthetic chat demo. No external resources, no scripts, no accounts. Maximum 1800 characters.'
  cmd=[str(MODEL),"--no-tools","--no-mcp","--no-extensions",
       "--no-skills","--no-prompt-templates","--no-context-files",
       "--no-session","--no-approve","--offline","--model","granite4:3b",
       "--thinking","off","--system-prompt","Return only valid compact JSON.",
       "--print",prompt]
  env={"HOME":str(Path.home()),"PATH":"/usr/local/bin:/usr/bin:/bin",
       "PI_TELEMETRY":"0","PI_SKIP_VERSION_CHECK":"1",
       "OLLAMA_HOST":"http://127.0.0.1:11434"}
  model=subprocess.run(cmd,input="",capture_output=True,text=True,timeout=115,env=env)
  if model.returncode:raise RuntimeError("model_failed_"+str(model.returncode))
  html=validate(extract(model.stdout))
  patch={"files":[{"path":APP,"content":html},{"path":TEST,"content":TEST_SRC}]}
  file=state/"validated-patch.json"
  file.write_text(json.dumps(patch))
  change=p.isolated("apply",file)
  qa=p.isolated("test")
  result["qa"]=qa
  if not qa.get("passed") or not qa.get("tests_executed"):raise RuntimeError("qa_failed")
  by_name={f["path"]:f for f in change["written"]}
  if set(by_name)!={APP,TEST}:raise RuntimeError("written_scope_mismatch")
  review=p.local_review(TASK,list(by_name.values()),qa)
  result.update({"status":"verified_local_review","review":review,"sandbox":d["detail"]})
 except Exception as e:result["error"]={"type":type(e).__name__,"message":str(e)[:240]}
 finally:
  result["completed_utc"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
  (state/"receipt.json").write_text(json.dumps(result,indent=2))
 return result
if __name__=="__main__":
 try:
  if len(sys.argv)!=2 or sys.argv[1]!=TASK:raise ValueError("unapproved_task")
  print(json.dumps(run()))
 except Exception as err:
  print(json.dumps({"status":"blocked","type":type(err).__name__,"message":str(err)[:240]}))
  sys.exit(1)
