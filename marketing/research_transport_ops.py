#!/usr/bin/env python3
"""Audited, exact-page grant for the existing signed Mac↔Dell research relay.
No general URL fetching, secret exchange, arbitrary shell, or publishing.
Source text is never returned beyond a bounded excerpt. No credentials here.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path("/var/lib/generic-linux-automator-exec")
EXTRACTOR=ROOT/"bhm-research-expansion-20261022/research_engine.py"
PYTHON=ROOT/"bhm-research-expansion-20261022/.venv/bin/python"
DATABASE=ROOT/"bhm-research-expansion-20261022/private-evidence.sqlite3"
# Previously audited public pages; all future grants need a reviewed code change.
PAGES=frozenset({
    "https://mokshagoa.com/",
    "https://www.w3.org/WAI/fundamentals/accessibility-intro/"
})
HOST_GRANTS="mokshagoa.com,www.w3.org"

def grant(url):
    if not isinstance(url,str) or url not in PAGES:
        raise ValueError("exact_public_page_not_granted")
    return url

def execute(url):
    grant(url)
    result=subprocess.run([str(PYTHON),str(EXTRACTOR),"--db",str(DATABASE),
                           "--grants",HOST_GRANTS,"extract",url],
                          capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=40)
    if result.returncode!=0 or len(result.stdout)>12000:
        raise RuntimeError("reviewed_extractor_failed")
    d=json.loads(result.stdout)
    if not isinstance(d,dict) or d.get("source_url")!=url:
        raise RuntimeError("source_identity_mismatch")
    if d.get("status") not in ("needs_review","unavailable"):
        raise RuntimeError("untrusted_extraction_status")
    keys=("status","reason","source_url","canonical_url","title","excerpt",
          "sha256","observed_utc","content_bytes","untrusted_external_text","facts_verified")
    page={key:d[key] for key in keys if key in d}
    page["excerpt"]=str(page.get("excerpt",""))[:400]
    if "store" in d:
        page["store"]={k:d["store"].get(k) for k in ("source_id","change","classification","verified")}
    return {"provider":"bhm-exact-page-extractor","node":"dell-linux",
            "page":page,"paid_fallback":False,"publish_approval":False}
