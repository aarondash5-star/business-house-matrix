"""Fixed-function, read-only Mac preflight collection proposal.

Not installed as an MCP action. No dynamic shell, arbitrary paths, network,
permissions, credential reading, publication or extraction. The trusted worker
must inject the existing authenticated signature callback, not supply a key.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Callable

SCHEMA = "bhm.mac.fixed_preflight.v1"
CONTEXT = b"BHM-MAC-STAGEB-PREFLIGHT-v1\n"
MAC_ROOT = Path("/opt/business-house-matrix/marketing/brain")
BRIDGE_ROOT = Path("/var/lib/generic-linux-automator-exec/matrix-research-transport")
ARTIFACTS = {
    "marketing_report_orchestrator.py": MAC_ROOT / "marketing_report_orchestrator.py",
    "searxng_research.py": MAC_ROOT / "searxng_research.py",
    "matrix-research-transport/transport.py": BRIDGE_ROOT / "transport.py",
}
TIMER = "bhm-marketing-queue-worker.timer"
GATE_MARKER = b"BHM_EXACT_EXTRACT_GATE_20261022"
MAX_ARTIFACT_SIZE = 8 * 1024 * 1024
MAX_STATUS_SIZE = 64 * 1024


def _hash_fixed(path: Path) -> tuple[str, bool]:
    """Open only a compiled-in regular-file target; never follow final symlink."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(path, flags)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or not 0 < st.st_size <= MAX_ARTIFACT_SIZE:
            raise ValueError("artifact_not_bounded_regular_file")
        digest = hashlib.sha256()
        marker = False
        tail = b""
        while True:
            chunk = os.read(fd, 64 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            segment = tail + chunk
            marker |= GATE_MARKER in segment
            tail = segment[-len(GATE_MARKER):]
        if os.fstat(fd).st_size != st.st_size:
            raise ValueError("artifact_changed_during_read")
        return digest.hexdigest(), marker
    finally:
        os.close(fd)


def _fixed_exec(args: list[str], *, cwd: Path | None = None) -> str:
    """No shell. Caller passes one of two internal constant argv sequences."""
    completed = subprocess.run(
        args, shell=False, check=True, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        timeout=8, cwd=cwd,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(Path.home()),
             "XDG_RUNTIME_DIR": os.environ.get("XDG_RUNTIME_DIR", "")},
    )
    if len(completed.stdout) > MAX_STATUS_SIZE:
        raise ValueError("status_output_too_large")
    return completed.stdout.decode("utf-8")


def _brain_flags(status_text: str) -> tuple[bool, bool]:
    try:
        parsed = json.loads(status_text)
    except json.JSONDecodeError:
        raise ValueError("brain_status_not_json") from None
    found = {"publish_enabled": [], "spend_enabled": []}
    def visit(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in found:
                    if type(v) is not bool:
                        raise ValueError("invalid_brain_flag_type")
                    found[k].append(v)
                elif isinstance(v, (dict, list)):
                    visit(v)
        elif isinstance(obj, list):
            for v in obj:
                if isinstance(v, (dict, list)):
                    visit(v)
    visit(parsed)
    if not all(found.values()):
        raise ValueError("brain_flags_missing")
    if any(any(values) for values in found.values()):
        raise ValueError("unsafe_brain_flags")
    return False, False


def collect_fixed_attestation(nonce: str, sign_bytes: Callable[[bytes], bytes],
                              *, clock: Callable[[], dt.datetime] | None = None) -> dict:
    """Fixed only: nonce + service-attested signer, no command/path arguments.

    Must be wrapped by a separately approved typed connector action. Signing
    callback belongs to authenticated connector, never arbitrary request data.
    """
    if not isinstance(nonce, str) or not re.fullmatch(r"[A-Za-z0-9_-]{24,64}", nonce):
        raise ValueError("invalid_nonce")
    if not callable(sign_bytes):
        raise ValueError("authenticated_signer_required")
    if _fixed_exec(["systemctl", "--user", "is-active", TIMER]).strip() != "active":
        raise ValueError("brain_timer_not_active")
    flags = _brain_flags(_fixed_exec([sys.executable, "brain.py", "status", "--verbose"], cwd=MAC_ROOT))
    fingerprints = {}
    active_gate = False
    for label, path in ARTIFACTS.items():
        fingerprint, marker = _hash_fixed(path)
        fingerprints[label] = fingerprint
        active_gate |= marker
    if active_gate:
        raise ValueError("extraction_gate_already_active")
    observed = (clock or (lambda: dt.datetime.now(dt.timezone.utc)))()
    if observed.tzinfo is None:
        raise ValueError("timezone_required")
    payload = {
        "schema": SCHEMA, "host_id": "mac-linux",
        "observed_utc": observed.astimezone(dt.timezone.utc).isoformat(),
        "units": {TIMER: "active"}, "artifacts": fingerprints,
        "extract_gate_active": False,
        "publish_enabled": flags[0], "spend_enabled": flags[1],
        "preflight_nonce": nonce,
    }
    message = CONTEXT + json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    signature = sign_bytes(message)
    if not isinstance(signature, bytes) or len(signature) != 64:
        raise ValueError("invalid_signer_signature")
    return {"payload": payload, "signature": base64.b64encode(signature).decode()}
