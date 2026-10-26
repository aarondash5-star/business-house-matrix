#!/usr/bin/env python3
"""Fail-closed, fixed-purpose internal Dell V4 release broker.

There is deliberately NO SSH/web listener, model, general shell interface,
deployment-approval writer or privilege management here.
Activation requires a real, independently signed approval from an owner key
installed outside the Dev Yard worker's write scope. The current shared
controller must never be patched by using this file as a shell workaround.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from typing import Any

from v4_source_binding_review import (
    render_candidate, inspect_candidate, ReleaseDenied, digest,
    OLD_ADAPTER_SHA, V13, V14, V4_ADAPTER_SHA, V4_GUARD_SHA, V13_GATE_SHA,
)

PROJECT = "matrix_dev_manager"
ACTION = "internal_component_release"
MANIFEST = "matrix_v4_controller_v14"
HOST = "dell-linux"
SERVICE = "bhm-autonomy-controller.service"
REVIEWED_SOURCE_SHA = "5952cf690e65210de039f7fcd0f53caf76548c6c"
ONE_TASK_CANARY = "f0243456-8c15-4363-b1c2-af3cf1d8e118"
QA_RECEIPTS = (
    "da27d9b3-e7f0-4324-b8b1-263b5905f98f",
    "7c549787-c1bb-4dca-bc45-a5d6687a77de",
)
SIGNER_IDENTITY = "matrix-v4-release-owner"
SIGNING_NAMESPACE = "matrix-v4-host-release"
SSHK = "/usr/bin/ssh-keygen"
APPROVAL_FIELDS = frozenset((
    "schema", "host", "project", "manifest", "action", "source_commit",
    "adapter_sha256", "guard_sha256", "v14_gate_sha256", "qa_receipts",
    "release_id", "expires_utc", "production", "spend", "max_activations",
))
_RELEASE_ID = re.compile(r"^v4-controller-20261026-[a-z0-9]{12,40}$")
_APPROVED_CODES = frozenset(("preflight", "stage"))
MAX_DOCUMENT = 8192

class BrokerDenied(ValueError):
    pass

def _canonical(obj: Any) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
            + "\n").encode("ascii")

def _read(path: Path, limit: int = MAX_DOCUMENT) -> bytes:
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise BrokerDenied("unsafe_file")
    s = path.stat()
    if s.st_size < 1 or s.st_size > limit or (s.st_mode & 0o022):
        raise BrokerDenied("untrusted_file_permissions_or_size")
    return path.read_bytes()

def _load_approval(path: Path) -> tuple[dict, bytes]:
    source = _read(path)
    try:
        payload = json.loads(source)
    except (ValueError, UnicodeError) as e:
        raise BrokerDenied("invalid_approval_json") from e
    if not isinstance(payload, dict) or set(payload) != APPROVAL_FIELDS:
        raise BrokerDenied("approval_schema_denied")
    if _canonical(payload) != source:
        raise BrokerDenied("approval_not_canonical")
    expected = {
        "schema": 1, "host": HOST, "project": PROJECT, "manifest": MANIFEST,
        "action": ACTION, "source_commit": REVIEWED_SOURCE_SHA,
        "adapter_sha256": V4_ADAPTER_SHA, "guard_sha256": V4_GUARD_SHA,
        "qa_receipts": list(QA_RECEIPTS), "production": False,
        "spend": False, "max_activations": 1,
    }
    for field, value in expected.items():
        if type(payload[field]) is not type(value) or payload[field] != value:
            raise BrokerDenied("approval_scope_denied:" + field)
    if (not isinstance(payload["v14_gate_sha256"], str) or
        not re.fullmatch(r"[0-9a-f]{64}", payload["v14_gate_sha256"])):
        raise BrokerDenied("invalid_gate_pin")
    if not isinstance(payload["release_id"], str) or not _RELEASE_ID.fullmatch(payload["release_id"]):
        raise BrokerDenied("invalid_release_id")
    try:
        expiry = datetime.fromisoformat(payload["expires_utc"].replace("Z", "+00:00"))
    except (TypeError, ValueError, AttributeError) as e:
        raise BrokerDenied("invalid_release_expiry") from e
    now = datetime.now(timezone.utc)
    if expiry.tzinfo is None or not now < expiry <= (now + __import__("datetime").timedelta(hours=1)):
        raise BrokerDenied("release_expired_or_unbounded")
    return payload, source

def _trust_store(path: Path) -> None:
    """Independent, root-owned trust; never trust a signer file written by worker."""
    p = Path(path)
    if p.is_symlink() or not p.is_file():
        raise BrokerDenied("trust_store_missing")
    parent = p.parent
    if parent.is_symlink():
        raise BrokerDenied("trust_dir_symlink")
    s = p.stat()
    d = parent.stat()
    if s.st_uid != 0 or d.st_uid != 0 or (s.st_mode & 0o022) or (d.st_mode & 0o022):
        raise BrokerDenied("trust_store_not_independently_owned")
    if s.st_size > 4096 or s.st_nlink != 1:
        raise BrokerDenied("trust_store_untrusted")
    allowed = p.read_text(encoding="ascii")
    if allowed.count(SIGNER_IDENTITY + " ") != 1:
        raise BrokerDenied("trust_signer_identity_missing")
    if not allowed.startswith(SIGNER_IDENTITY + " ssh-ed25519 "):
        raise BrokerDenied("trust_signer_key_format")

def verify_signature(data: bytes, signature: Path, trust: Path) -> bool:
    """Cryptographic check; no caller-supplied binary, identity or namespace."""
    _trust_store(trust)
    if not Path(SSHK).is_file():
        raise BrokerDenied("ssh_signature_verifier_missing")
    _read(signature, limit=8192)
    result = subprocess.run(
        [SSHK, "-Y", "verify", "-f", str(trust), "-I", SIGNER_IDENTITY,
         "-n", SIGNING_NAMESPACE, "-s", str(signature)],
        input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=7, check=False,
        env={"PATH":"/usr/bin:/bin", "LC_ALL":"C"},
    )
    if result.returncode != 0:
        raise BrokerDenied("independent_owner_signature_invalid")
    return True

def source_review(live_root: Path, candidate_files: Path) -> dict:
    """Exact original source bytes, no writes or auto-admission."""
    live_root = Path(live_root)
    candidate_files = Path(candidate_files)
    g = _read(live_root/"yard_execution_guard_v13.py", 30000)
    a = _read(live_root/"yard_auto_adapter_v1.py", 30000)
    v4 = _read(candidate_files/"yard_auto_adapter_v1_patched.py", 30000)
    guard = _read(candidate_files/"adapter_guard.py", 9000)
    ledger = json.loads(_read(live_root/"yard_exec_bindings_v13.json", 35000))
    result = render_candidate(g, a, v4, guard, ledger)
    inspect_candidate(result)
    return result

@dataclass(frozen=True)
class BrokerPaths:
    live: Path
    source: Path
    approval: Path
    signature: Path
    allowed_signers: Path
    journal: Path
    def validate(self):
        # No code path allows re-targeting an unrelated project's controller.
        if self.live.name != "matrix-controller" or self.source.name != "governance-v4":
            raise BrokerDenied("controller_path_not_pinned")
        if self.live.is_symlink() or self.source.is_symlink():
            raise BrokerDenied("controller_symlink_denied")
        if self.live.resolve() == self.source.resolve():
            raise BrokerDenied("source_live_overlap_denied")
        if self.journal.is_symlink():
            raise BrokerDenied("journal_symlink_denied")

def assess(paths: BrokerPaths, mode: str = "preflight") -> dict:
    if mode not in _APPROVED_CODES:
        raise BrokerDenied("invalid_fixed_action")
    paths.validate()
    approval, encoded = _load_approval(paths.approval)
    reviewed = source_review(paths.live, paths.source)
    if approval["v14_gate_sha256"] != reviewed["manifest"]["new_source_hashes"]["yard_execution_guard_v13.py"]:
        raise BrokerDenied("approval_candidate_gate_mismatch")
    # The owner signature verification happens AFTER pin checks, BEFORE all mutation.
    if verify_signature(encoded, paths.signature, paths.allowed_signers) is not True:
        raise BrokerDenied("independent_owner_signature_missing")
    state = {"release_id":approval["release_id"],"mode":mode,"host":HOST,
             "source_bound":True,"authenticated_owner_release":True,
             "reviewed_source_commit":REVIEWED_SOURCE_SHA,
             "source_bindings":21,"production":False,"spend":False,
             "candidate_sha256":approval["v14_gate_sha256"]}
    return state

def ensure_replay_free(paths: BrokerPaths, release_id: str) -> bool:
    # The broker never auto-creates or edits owner approval records.
    if not paths.journal.is_dir() or paths.journal.is_symlink():
        raise BrokerDenied("private_journal_missing")
    s=paths.journal.stat()
    if s.st_mode & 0o077:
        raise BrokerDenied("journal_not_private")
    completed=paths.journal/(release_id + ".complete")
    active=paths.journal/(release_id + ".reserved")
    if completed.exists() or active.exists():
        raise BrokerDenied("single_use_release_already_claimed")
    return True

def stage_signed_release(paths: BrokerPaths) -> dict:
    """Create only PRIVATE, source-pinned stage/backup files; never edit live host.

    A genuine independent owner signature and an exclusive O_EXCL reservation
    are required. Interrupted reservations remain reserved; do NOT replay.
    """
    import os
    import shutil
    info = assess(paths, mode="stage")
    release_id = info["release_id"]
    ensure_replay_free(paths, release_id)
    reservation = paths.journal / (release_id + ".reserved")
    try:
        fd = os.open(reservation, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    except FileExistsError as e:
        raise BrokerDenied("single_use_release_already_claimed") from e
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(json.dumps({"release_id":release_id,"status":"reserved",
                                 "host_write_authorized":False},sort_keys=True)+"\n")
        stream.flush(); os.fsync(stream.fileno())
    # Never delete the reservation automatically on failures or uncertain outcomes.
    target = paths.journal / (release_id + ".candidate")
    target.mkdir(mode=0o700)
    if target.is_symlink():
        raise BrokerDenied("candidate_symlink")
    reviewed = source_review(paths.live, paths.source)
    old_ledger = _read(paths.live / "yard_exec_bindings_v13.json", 35000)
    originals = {
        "v13-yard_auto_adapter_v1.py": _read(paths.live / "yard_auto_adapter_v1.py", 30000),
        "v13-yard_execution_guard_v13.py": _read(paths.live / "yard_execution_guard_v13.py", 30000),
        "v13-yard_exec_bindings_v13.json": old_ledger,
    }
    staged = {
        "v14-yard_auto_adapter_v1.py": reviewed["source"]["yard_auto_adapter_v1.py"],
        "v14-adapter_guard_v4.py": reviewed["source"]["adapter_guard_v4.py"],
        "v14-yard_execution_guard_v13.py": reviewed["source"]["yard_execution_guard_v13.py"],
        "v14-yard_exec_bindings_v14.json": _canonical(reviewed["candidate_ledger"]),
    }
    receipts = {}
    for name, data in {**originals, **staged}.items():
        path = target / name
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        fd = os.open(path, flags, 0o600)
        with os.fdopen(fd, "wb") as out:
            out.write(data)
            out.flush(); os.fsync(out.fileno())
        receipts[name] = hashlib.sha256(data).hexdigest()
    audit = {"release_id":release_id, "status":"candidate_staged",
             "source_sha256":receipts,"host_write_authorized":False,
             "old_controller_untouched":True,"production":False}
    final = target / "stage-audit.json"
    fd = os.open(final, flags, 0o600)
    with os.fdopen(fd, "wb") as out:
        out.write(_canonical(audit));out.flush();os.fsync(out.fileno())
    return audit


def status(live: Path, source: Path) -> dict:
    # Safe even without signed owner approval; never creates files.
    try:
        reviewed=source_review(live,source)
    except (BrokerDenied, ReleaseDenied, ValueError, OSError) as e:
        return {"candidate":"denied","reason":type(e).__name__,"live_promotion":False}
    return {"candidate":"pinned","source_bindings":len(reviewed["candidate_ledger"]["bindings"]),
            "independent_owner_approval":"not_provided",
            "live_promotion":False,"dispatch":False}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(description="Internal V4 source-bound release broker (no general shell)")
    p.add_argument("command", choices=("status","preflight","stage"))
    a=p.parse_args()
    # CLI reads the exact existing controlled source locations. It NEVER
    # has an activate/swap operation until a separately reviewed host runner is approved.
    home=Path.home()
    if a.command=="status":
        print(json.dumps(status(home/"matrix-controller",
             home/"yard-v4-corrective-20261026"/"brain/dev-toolyard/governance-v4"),sort_keys=True))
    elif a.command=="stage":
        paths=BrokerPaths(
            home/"matrix-controller",
            home/"yard-v4-corrective-20261026"/"brain/dev-toolyard/governance-v4",
            home/".matrix-release-authorizations"/"v4-owner-release.json",
            home/".matrix-release-authorizations"/"v4-owner-release.json.sig",
            Path("/etc/matrix-internal-release/allowed_signers"),
            home/".matrix-release-journal")
        try:
            print(json.dumps(stage_signed_release(paths),sort_keys=True))
        except (BrokerDenied, ReleaseDenied, ValueError, OSError, subprocess.SubprocessError) as exc:
            print(json.dumps({"state":"blocked","reason":type(exc).__name__+
                                ":"+str(exc)[:130],"live_promotion":False},sort_keys=True))
            raise SystemExit(3)
    else:
        print(json.dumps({"state":"blocked","reason":"independent_release_approval_and_host_runner_not_enrolled",
                          "live_promotion":False},sort_keys=True))
        raise SystemExit(3)
