#!/usr/bin/env python3
"""Mac-native read-only BHM research evidence adapter (NOT installed on Mac).

Run only after independent host deployment authorization. Reuses the existing
guarded research_engine evidence schema. Does not enqueue Dell work, fetch pages,
accept URLs, run shell commands, switch live services, or publish claims.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3

# The existing engine is cross-platform Python but historically hosted on Dell.
# Import is pure: its __main__ branch alone permits network extraction.
import research_engine as engine

VERSION = "bhm.mac.research-staging.v1"
TOPICS = frozenset(("moksha_arambol", "andaz_arambol"))
DB = Path.home() / ".local" / "share" / "bhm-research" / "evidence.sqlite3"
MODULES = ("research_engine.py", "research_entities.py", "research_monitor.py")
RELEASE_GATES = (
    "mac_connector_platform_security_approved",
    "mac_host_worker_deployment_approved",
    "pinned_artifact_hashes_and_backup_verified",
    "private_evidence_snapshot_verified",
    "mac_local_sandbox_qa_passed",
    "existing_signed_search_unmodified",
    "human_reviewer_and_source_identity_verified",
    "robots_terms_for_each_target_verified",
)
POLICY = {
    "mac_primary_requested": True,
    "mac_primary_active": False,
    "fallback": "dell-linux (existing; unchanged)",
    "network_source_grants": [],
    "automated_extraction": False,
    "automated_monitoring": False,
    "publication": False,
    "spending": False,
    "root_changes": False,
}


def _readonly_connection(path: Path) -> sqlite3.Connection:
    if path.is_symlink() or not path.is_file():
        raise ValueError("private_evidence_snapshot_missing_or_symlinked")
    if path.stat().st_size == 0:
        raise ValueError("empty_snapshot")
    # Do not create a database, sidecar, schema or fresh source claims.
    return sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True)


def describe(path: Path = DB, *, code_dir: Path | None = None) -> dict:
    base = code_dir or Path(__file__).resolve().parent
    modules = {name: (base / name).is_file() for name in MODULES}
    exists = path.is_file() and not path.is_symlink() and path.stat().st_size > 0
    return {
        "version": VERSION,
        "execution": "offline_readonly_not_live_mac",
        "host_target": "mac-linux",
        "required_modules_present": modules,
        "private_evidence_snapshot_present": bool(exists),
        "snapshot_sha256": _hash_file(path) if exists else None,
        "migration_release_gates": list(RELEASE_GATES),
        "release_ready": False,
        "policy": dict(POLICY),
    }


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def packet(topic: str, *, path: Path = DB) -> dict:
    if topic not in TOPICS:
        raise ValueError("topic_not_granted")
    with _readonly_connection(path) as db:
        check = db.execute("PRAGMA quick_check").fetchone()
        if check is None or check[0] != "ok":
            raise ValueError("evidence_integrity_failed")
        # This core uses existing SQLite FTS5 source memory and evidence model.
        payload = engine.packet(db, "wellness" if topic == "moksha_arambol" else "hostel")
    # Always unverified; source snippets are not a fact or hotel checkout-rate
    # certification. No direct page fetching or accepted claims.
    payload.update({
        "topic": topic,
        "compute_target": "mac-linux",
        "offline_mac_staging_only": True,
        "facts_verified": False,
        "price_claims_approved": False,
        "approved_for_design_claims": False,
        "publish_approval": False,
        "spend_approval": False,
        "source_grants": [],
        "stage_b_certified": False,
    })
    if topic == "andaz_arambol":
        payload["required_visual_brand_constraints"] = [
            "real Andaz Vibe Stay imagery", "mobile-first",
            "no production booking or PMS edits",
        ]
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline Mac research staging; no URLs or shell input.")
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("status")
    cmd = sub.add_parser("packet")
    cmd.add_argument("--topic", choices=sorted(TOPICS), required=True)
    args = parser.parse_args()
    result = describe() if args.operation == "status" else packet(args.topic)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
