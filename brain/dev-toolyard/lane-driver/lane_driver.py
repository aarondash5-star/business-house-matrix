"""Deterministic lane follow-through. No model, shell, network or credential access.

Governed controller code is the only allowed transport adapter. A receipt verifier
must independently check gateway/controller terminal evidence before acknowledge().
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path
from typing import Callable

HOSTS = {"dell-linux", "mac-linux"}
LANES = {"control", "operations", "development"}
STATES = {"ready", "reserved", "running", "gate_pending", "blocked", "complete"}
TERMINALS = {"completed", "failed", "blocked", "outcome_unknown", "expired", "stale_running"}
IDENT = re.compile(r"^[a-z][a-z0-9_-]{2,63}$")
SHA = re.compile(r"^[a-f0-9]{64}$")
EVENT_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:-]{7,119}$")
MAX_STAGES = 12


class DriverDenied(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj):
    return hashlib.sha256(canonical(obj).encode("ascii")).hexdigest()


def _valid_name(name):
    return isinstance(name, str) and bool(IDENT.fullmatch(name))


def _validate(spec):
    if not isinstance(spec, dict) or set(spec) != {
        "schema", "task_id", "project_id", "host_id", "lane", "brief_sha256",
        "stages", "max_corrections", "release_allowed", "spend_allowed",
    }:
        raise DriverDenied("invalid_envelope")
    if spec["schema"] != 1 or spec["host_id"] not in HOSTS or spec["lane"] not in LANES:
        raise DriverDenied("invalid_lane_identity")
    if not _valid_name(spec["project_id"]) or not _valid_name(spec["task_id"]):
        raise DriverDenied("invalid_scope")
    if not isinstance(spec["brief_sha256"], str) or not SHA.fullmatch(spec["brief_sha256"]):
        raise DriverDenied("invalid_source_hash")
    if spec["release_allowed"] is not False or spec["spend_allowed"] is not False:
        raise DriverDenied("privilege_escalation_denied")
    if type(spec["max_corrections"]) is not int or not 0 <= spec["max_corrections"] <= 2:
        raise DriverDenied("invalid_retry_budget")
    stages = spec["stages"]
    if not isinstance(stages, list) or not 1 <= len(stages) <= MAX_STAGES:
        raise DriverDenied("invalid_stage_count")
    ids = []
    for stage in stages:
        if not isinstance(stage, dict) or set(stage) != {"id", "action", "manifest", "return_to"}:
            raise DriverDenied("invalid_stage_schema")
        if not all(_valid_name(stage[k]) for k in ("id", "action", "manifest")):
            raise DriverDenied("invalid_stage_action")
        ids.append(stage["id"])
    if len(set(ids)) != len(ids):
        raise DriverDenied("duplicate_stage")
    for i, stage in enumerate(stages):
        back = stage["return_to"]
        if back is not None and (not _valid_name(back) or back not in ids[:i]):
            raise DriverDenied("invalid_return_edge")
    return spec


class Ledger:
    def __init__(self, path: Path):
        self.path = Path(path)
        if self.path.is_symlink():
            raise DriverDenied("symlink_database_denied")
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.path.exists() and not self.path.is_file():
            raise DriverDenied("database_not_regular_file")
        self.db = sqlite3.connect(str(self.path), timeout=10, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA busy_timeout=10000")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
          task_id TEXT PRIMARY KEY, project TEXT NOT NULL, host TEXT NOT NULL,
          lane TEXT NOT NULL, spec TEXT NOT NULL, spec_sha TEXT NOT NULL,
          stage_idx INTEGER NOT NULL, version INTEGER NOT NULL,
          state TEXT NOT NULL, corrections INTEGER NOT NULL,
          lease TEXT, last_receipt TEXT, updated INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS events (
          seq INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL,
          kind TEXT NOT NULL, stage_idx INTEGER NOT NULL, version INTEGER NOT NULL,
          payload TEXT NOT NULL, prev_hash TEXT NOT NULL, event_hash TEXT NOT NULL,
          FOREIGN KEY(task_id) REFERENCES tasks(task_id));
        CREATE INDEX IF NOT EXISTS driver_events_task ON events(task_id,seq);
        """)
        self.path.chmod(0o600)
        self.db.execute("PRAGMA foreign_keys=ON")

    def close(self):
        self.db.close()

    def _tx(self, fn):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            result = fn()
            self.db.execute("COMMIT")
            return result
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def _event(self, row, kind, payload, new_version):
        tail = self.db.execute(
            "SELECT event_hash FROM events WHERE task_id=? ORDER BY seq DESC LIMIT 1",
            (row["task_id"],)
        ).fetchone()
        prev = tail["event_hash"] if tail else "0" * 64
        document = {"task_id": row["task_id"], "kind": kind,
                    "stage_idx": row["stage_idx"], "version": new_version,
                    "payload": payload, "prev_hash": prev}
        h = digest(document)
        self.db.execute(
            "INSERT INTO events(task_id,kind,stage_idx,version,payload,prev_hash,event_hash)"
            " VALUES(?,?,?,?,?,?,?)",
            (row["task_id"], kind, row["stage_idx"], new_version,
             canonical(payload), prev, h)
        )

    def enroll(self, spec: dict, owner_admit: Callable[[dict], bool]):
        spec = _validate(spec)
        if not callable(owner_admit) or owner_admit(spec) is not True:
            raise DriverDenied("owner_admission_required")
        identity = digest(spec)
        def apply():
            old = self.db.execute("SELECT * FROM tasks WHERE task_id=?", (spec["task_id"],)).fetchone()
            if old:
                if old["spec_sha"] != identity:
                    raise DriverDenied("conflicting_task_identity")
                return self.get(spec["task_id"])
            self.db.execute(
                "INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (spec["task_id"], spec["project_id"], spec["host_id"], spec["lane"],
                 canonical(spec), identity, 0, 0, "ready", 0, None, None, int(time.time()))
            )
            row = self.db.execute("SELECT * FROM tasks WHERE task_id=?", (spec["task_id"],)).fetchone()
            self._event(row, "enrolled", {"spec_sha": identity}, 0)
            return self.get(spec["task_id"])
        return self._tx(apply)

    def get(self, task_id):
        row = self.db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        if row is None:
            raise DriverDenied("unknown_task")
        return dict(row)

    def reserve(self, task_id, version, admit_action: Callable[[dict, dict], bool]):
        def apply():
            row = self.get(task_id)
            if row["version"] != version:
                raise DriverDenied("stale_stage_version")
            if row["state"] == "reserved":
                return {"task_id": task_id, "lease": row["lease"], "deduplicated": True}
            if row["state"] != "ready":
                raise DriverDenied("task_not_dispatchable")
            spec = json.loads(row["spec"])
            stage = spec["stages"][row["stage_idx"]]
            if not callable(admit_action) or admit_action(spec, stage) is not True:
                raise DriverDenied("controller_stage_admission_denied")
            lease = digest({"task": task_id, "version": version, "stage": stage["id"]})[:48]
            self.db.execute(
                "UPDATE tasks SET state='reserved',lease=?,version=version+1,updated=? WHERE task_id=?",
                (lease, int(time.time()), task_id))
            )
            self._event(row, "dispatch_reserved", {"lease": lease, "stage": stage["id"]}, version + 1)
            return {"task_id": task_id, "lease": lease, "deduplicated": False}
        return self._tx(apply)

    def observe(self, task_id, version, lease, receipt: dict,
                verify_receipt: Callable[[dict, dict, dict], bool]):
        """Only a trusted adapter may pass its independent verifier callback.

        Receipt references must be exact and terminal. Unknown outcomes quarantine
        without replay. Correctable failures return only along pinned stage graph.
        """
        def apply():
            row = self.get(task_id)
            if row["version"] != version or row["state"] != "reserved" or row["lease"] != lease:
                raise DriverDenied("stale_or_unowned_receipt")
            spec = json.loads(row["spec"])
            stage = spec["stages"][row["stage_idx"]]
            if not isinstance(receipt, dict) or set(receipt) != {
                "receipt_id", "task_id", "host_id", "lane", "state", "exit_code",
                "gate", "source_sha256", "evidence_sha256",
            }:
                raise DriverDenied("invalid_receipt_schema")
            if (receipt["task_id"] != task_id or receipt["host_id"] != row["host"] or
                receipt["lane"] != row["lane"] or
                not isinstance(receipt["receipt_id"], str) or
                not EVENT_ID.fullmatch(receipt["receipt_id"]) or
                not isinstance(receipt["source_sha256"], str) or
                not SHA.fullmatch(receipt["source_sha256"]) or
                receipt["source_sha256"] != spec["brief_sha256"] or
                not isinstance(receipt["evidence_sha256"], str) or
                not SHA.fullmatch(receipt["evidence_sha256"]) or
                receipt["state"] not in TERMINALS or
                (type(receipt["exit_code"]) is not int and receipt["exit_code"] is not None) or
                receipt["gate"] not in {"pass", "correctable_fail", "block", "uncertain"}):
                raise DriverDenied("receipt_identity_or_integrity_denied")
            if not callable(verify_receipt) or verify_receipt(spec, stage, receipt) is not True:
                raise DriverDenied("independent_receipt_verification_required")
            if receipt["state"] in {"outcome_unknown", "expired", "stale_running"} or receipt["gate"] == "uncertain":
                new_state, target, corrections = "blocked", row["stage_idx"], row["corrections"]
                reason = "uncertain_no_replay"
            elif receipt["state"] == "completed" and receipt["exit_code"] == 0 and receipt["gate"] == "pass":
                target, corrections = row["stage_idx"] + 1, row["corrections"]
                new_state = "complete" if target == len(spec["stages"]) else "ready"
                reason = "gate_pass"
            elif receipt["gate"] == "correctable_fail" and stage["return_to"] is not None:
                target = next(i for i, x in enumerate(spec["stages"]) if x["id"] == stage["return_to"])
                corrections = row["corrections"] + 1
                new_state = "ready" if corrections <= spec["max_corrections"] else "blocked"
                reason = "returned_for_repair" if new_state == "ready" else "retry_limit_exhausted"
            else:
                new_state, target, corrections = "blocked", row["stage_idx"], row["corrections"]
                reason = "noncorrectable_gate"
            self.db.execute(
                "UPDATE tasks SET state=?,stage_idx=?,corrections=?,version=version+1,"
                "last_receipt=?,lease=NULL,updated=? WHERE task_id=?",
                (new_state, target, corrections, receipt["receipt_id"], int(time.time()), task_id))
            )
            self._event(row, reason, {"receipt_id": receipt["receipt_id"],
                                      "next_stage_idx": target, "state": new_state}, version + 1)
            return {"task_id": task_id, "state": new_state, "stage_idx": target,
                    "corrections": corrections, "reason": reason}
        return self._tx(apply)

    def verify_chain(self, task_id):
        self.get(task_id)
        prev = "0" * 64
        rows = self.db.execute(
            "SELECT * FROM events WHERE task_id=? ORDER BY seq", (task_id,)).fetchall()
        for row in rows:
            doc = {"task_id": task_id, "kind": row["kind"],
                   "stage_idx": row["stage_idx"], "version": row["version"],
                   "payload": json.loads(row["payload"]), "prev_hash": prev}
            if row["prev_hash"] != prev or row["event_hash"] != digest(doc):
                raise DriverDenied("event_chain_tampering")
            prev = row["event_hash"]
        return {"task_id": task_id, "events": len(rows), "valid": True, "head": prev}
