#!/usr/bin/env python3
"""Safe offline checks for the PUBLIC Business House Matrix Git repository.

This complements (rather than replaces) full secret scanning and code review.
Does not access cloud accounts, repositories outside this checkout, or networks.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROHIBITED_SUFFIXES = {".pem", ".p12", ".pfx", ".sqlite", ".db", ".key", ".kubeconfig"}
PROHIBITED_NAMES = {"id_rsa", "id_ed25519", "credentials.json", "service-account.json", ".npmrc"}
# Build high-confidence signatures in pieces so the scanner source is not itself a match.
SIGNATURES = [
    ("private key", re.compile("-----BEGIN " + "(?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub access token", re.compile("gh" + "[pousr]_[A-Za-z0-9_]{30,}")),
    ("GitHub fine-grained token", re.compile("github_" + "pat_[A-Za-z0-9_]{20,}")),
    ("AWS access key", re.compile("AK" + "IA[0-9A-Z]{16}")),
    ("Google API key", re.compile("AI" + "za[0-9A-Za-z_\\-]{35}")),
    ("secret service-account JSON", re.compile('"type"\\s*:\\s*"service_' + 'account"')),
]
errors: list[str] = []
listed = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
paths = [p.decode() for p in listed.split(bytes([0])) if p]
for path in paths:
    file = ROOT / path
    name = file.name.lower()
    if name in PROHIBITED_NAMES or file.suffix.lower() in PROHIBITED_SUFFIXES:
        errors.append(f"Potentially private file tracked: {path}")
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        errors.append(f"Actual environment configuration tracked: {path}")
    if not file.is_file():
        errors.append(f"Missing tracked file: {path}")
        continue
    if file.stat().st_size > 5 * 1024 * 1024:
        errors.append(f"Unexpected large tracked file: {path}")
        continue
    if path == "scripts/validate_public_repo.py":
        continue
    try:
        content = file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"Non-text or binary file requires review: {path}")
        continue
    for label, signature in SIGNATURES:
        if signature.search(content):
            errors.append(f"Potential {label} in tracked file: {path}")

compose_file = ROOT / "pilot/docker-compose.yml"
if not compose_file.is_file():
    errors.append("Pilot Compose file missing")
else:
    compose = compose_file.read_text(encoding="utf-8")
    for expected in ['127.0.0.1:3000:8080', 'WEBUI_AUTH: "True"', 'ENABLE_SIGNUP: ${ENABLE_SIGNUP:-False}']:
        if expected not in compose:
            errors.append(f"Pilot safety setting missing: {expected}")

config = ROOT / "matrix/config.py"
if config.is_file():
    tree = ast.parse(config.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "DEPARTMENTS" for t in node.targets):
            values = ast.literal_eval(node.value)
            if len(values) != 9 or values[-1] != "evolution":
                errors.append("Nine-department architecture no longer matches approval")
            break
    else:
        errors.append("DEPARTMENTS definition missing")

if errors:
    for error in errors:
        print(f"BLOCK: {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"PASS: {len(paths)} tracked files checked; no high-confidence secret patterns, public-repo hazards or unsafe pilot defaults found.")
