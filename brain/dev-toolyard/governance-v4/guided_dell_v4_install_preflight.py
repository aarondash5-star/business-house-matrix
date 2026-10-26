#!/usr/bin/env python3
"""Read-only Dell V4 guided-install preflight. NOT a privileged installer.

A readiness report for the independent owner terminal. This tool NEVER asks
for a password, changes sudo rights, generates signed approvals, mutates the
controller, starts services, or downloads/evaluates scripts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
from typing import Callable, Any

HOST = "dell-linux"
PROJECT = "matrix_dev_manager"
SERVICE = "bhm-autonomy-controller.service"
EXPECTED_NAMES = {
    "controller.py": "e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836",
    "yard_auto_adapter_v1.py": "adad20add5e247c515c48d8e2d0c61f2b91e2238d489ed8b4c2e674c845d1abe",
    "yard_execution_guard_v13.py": "7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e",
    "yard_exec_bindings_v13.json": "9c084832984c1471a22079cc606daccd0a49b78c942ddfee0800a800176c43a9",
}
# Exact values above are the reviewed rebased V1.4 candidate pins.
# A different live adapter or ledger is NOT automatically accepted. It needs
# a new candidate review, independently tested source and a new signed manifest.
TRUST = Path("/etc/matrix-internal-release/allowed_signers")
SIGNER = "matrix-v4-release-owner"
RELEASE_FILES = ("v4-owner-release.json", "v4-owner-release.json.sig")
CANDIDATE = "yard-v4-corrective-20261026/brain/dev-toolyard/governance-v4"
RUNNER = "matrix-v4-internal-release-broker-20261026"
HOMENAMES = frozenset(("karan-Inspiron-5379",))

def sha(path: Path) -> str | None:
    if path.is_symlink() or not path.is_file():
        return None
    if path.stat().st_size > 5000000:
        return None
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(262144),b""):
            h.update(block)
    return h.hexdigest()

def trust_is_independent(path: Path) -> bool:
    if path.is_symlink() or not path.is_file() or path.parent.is_symlink():
        return False
    p=path.stat(); d=path.parent.stat()
    if p.st_uid!=0 or d.st_uid!=0 or p.st_mode & 0o022 or d.st_mode & 0o022:
        return False
    if p.st_size>4096 or p.st_nlink!=1:
        return False
    try:
        lines=path.read_text("ascii").strip().splitlines()
        return len(lines)==1 and lines[0].startswith(SIGNER+" ssh-ed25519 ")
    except (OSError,UnicodeError):
        return False

def service_active() -> bool:
    try:
        r=subprocess.run(("systemctl","--user","is-active","--quiet",SERVICE),
                         timeout=4,capture_output=True,check=False)
        return r.returncode==0
    except (OSError,subprocess.TimeoutExpired):
        return False

def assess(home: Path, hostname: str, active: bool,
           trust: Path=TRUST) -> dict[str,Any]:
    root=home/"matrix-controller"
    checks={
        "exact_host":hostname in HOMENAMES,
        "controller_service_active":active,
        "controller_dir_not_symlink":root.is_dir() and not root.is_symlink(),
        "owner_signer_trust_valid":trust_is_independent(trust),
    }
    observed={}
    for name,expected in EXPECTED_NAMES.items():
        actual=sha(root/name)
        observed[name]={"observed":actual,"matches_original_pr33":actual==expected}
        checks["source_"+name]=actual==expected

    approval_dir=home/".matrix-release-authorizations"
    checks["approval_dir_private"]=approval_dir.is_dir() and not approval_dir.is_symlink() and (approval_dir.stat().st_mode & 0o077)==0
    for name in RELEASE_FILES:
        f=approval_dir/name
        checks["owner_"+name+"_present"]=f.is_file() and not f.is_symlink() and (f.stat().st_mode & 0o077)==0
    checks["broker_source_present"]=(home/RUNNER).is_dir()
    checks["candidate_files_present"]=(home/CANDIDATE).is_dir()
    checks["host_activation_runner_certified"]=False  # deliberate, cannot infer this from file presence
    checks["owner_signature_verified"]=False  # a file's existence is not signature verification
    checks["canary_and_rollback_certified"]=False
    # NO auto-admission: this read-only program cannot vouch for external release gates.
    blocked=[name for name,ok in checks.items() if not ok]
    return {
        "schema":1,"component":"dell-v4-guided-install-preflight",
        "host_id":HOST,"hostname_observed":hostname,"project":PROJECT,
        "target_release":"matrix_v4_controller_v14",
        "mode":"READ_ONLY_NO_INSTALL",
        "source_pins":observed,
        "checks":checks,"blockers":blocked,
        "live_controller_changed":False,"credentials_requested":False,
        "privilege_changed":False,"release_authorized":False,
        "ready_to_install":False,
        "next_step":"Rebase V4 candidate on observed adapter/ledger and independently certify signer + host activation/rollback.",
    }

def main(argv: list[str]|None=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=("preflight",),help="Only read-only action supported; no release activation")
    a=p.parse_args(argv)
    home=Path.home()
    report=assess(home,socket.gethostname(),service_active())
    print(json.dumps(report,sort_keys=True,indent=2))
    return 3 if report["blockers"] else 0

if __name__=="__main__":
    raise SystemExit(main())
