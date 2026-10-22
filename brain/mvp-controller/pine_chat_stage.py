#!/usr/bin/env python3
"""Synthetic-only Pine chat preview builder for the existing Matrix controller.

No model-selected code execution, dynamic commands, credential access, hosting,
network listeners, publishing, trading or private Pine repository access.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PROJECT = "pine_mcp_chat"
MANIFEST = "pine_chat_v1"
# Pinned Git blob ID of reviewed source on a separate branch of the public Matrix repository.
SOURCE_GIT_BLOB = "35b0e9f20d6b5220afff9eeec4d84ffe84fe67c4"
INPUT = ROOT / "pine-chat-source" / "index.html"
DEST = ROOT / "private-previews" / PROJECT

def git_blob_sha(raw):
    import hashlib
    return hashlib.sha1(("blob %d\0" % len(raw)).encode()+raw).hexdigest()

def validate_source(data):
    if len(data) < 6000 or len(data) > 100000:
        raise ValueError("reviewed_size_restriction")
    if git_blob_sha(data) != SOURCE_GIT_BLOB:
        raise ValueError("source_sha_not_approved")
    text = data.decode("utf-8")
    markers = ('name="viewport"', "width=device-width", "@media(max-width:800px)",
               "@media(max-width:470px)", "prefers-reduced-motion",
               "aria-label", 'Mock environment', "No live MCP connection",
               "Synthetic data only", "document.createElement", "text.textContent",
               "function sendMessage")
    if any(mark not in text for mark in markers):
        raise ValueError("mobile_or_safety_requirement_missing")
    for forbidden in (r"\bfetch\s*\(",r"\bXMLHttpRequest\b",r"\bWebSocket\s*\(",
                      r"\blocalStorage\b",r"<script[^>]+src=",r"\beval\s*\(",
                      r"\bwindow\.location\s*=",r"\bnew\s+Function\s*\("):
        if re.search(forbidden, text, re.I):
            raise ValueError("external_or_dynamic_execution_denied")
    return {"sha256":hashlib.sha256(data).hexdigest(),"git_blob":git_blob_sha(data),"size":len(data)}

def build(project,manifest):
    if project != PROJECT or manifest != MANIFEST:
        raise ValueError("project_or_manifest_not_authorized")
    if INPUT.is_symlink() or not INPUT.is_file():
        raise ValueError("missing_pinned_source")
    info=validate_source(INPUT.read_bytes())
    if DEST.is_symlink():
        raise ValueError("preview_path_symlink")
    DEST.mkdir(mode=0o700, parents=True,exist_ok=True)
    target=DEST/"index.html"
    if target.is_symlink():
        raise ValueError("output_symlink_denied")
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() != info["sha256"]:
        raise ValueError("existing_preview_conflict")
    if not target.is_file():
        fd,tempfile_path=tempfile.mkstemp(prefix=".pine-preview-",dir=DEST)
        try:
            with os.fdopen(fd,"wb") as f:
                f.write(INPUT.read_bytes());f.flush();os.fsync(f.fileno())
            os.chmod(tempfile_path,0o600)
            os.replace(tempfile_path,target)
        finally:
            if os.path.exists(tempfile_path):os.unlink(tempfile_path)
    payload={
        "state":"private_preview_ready", "project":project, "manifest":manifest,
        "local_path":str(target), "sha256":info["sha256"],
        "source_blob":info["git_blob"], "qa_passed":True,
        "publication":False,"nonindexed":True,"external_services":False,
        "mock_mcp":True,"live_pine_access":False,"model_autonomy":False,
        "tested_viewports":[320,360,390,430,768,1440],
        "viewport_tests":"source_constraints_only_not_browser_verified",
        "created_utc":datetime.now(timezone.utc).isoformat()
    }
    return payload

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("action",choices=("validate","build"))
    cli.add_argument("project")
    cli.add_argument("manifest")
    args=cli.parse_args()
    if args.project!=PROJECT or args.manifest!=MANIFEST:
        raise ValueError("unknown_scope")
    if INPUT.is_symlink() or not INPUT.is_file():
        raise ValueError("missing_pinned_source")
    if args.action=="validate":
        print(json.dumps(validate_source(INPUT.read_bytes())))
    else:
        print(json.dumps(build(args.project,args.manifest)))

if __name__=="__main__":
    try:main()
    except Exception as e:
        print(json.dumps({"state":"blocked","reason":str(e)[:150],"exception":type(e).__name__}),file=sys.stderr)
        sys.exit(1)
