#!/usr/bin/env python3
"""Dell Dev MCP tool router: Mac-style slot governance, no shared credentials.

This wrapper cannot grant additional MCP tools. The only executable tool is
the pinned, public-source-only external_mcp.py Fetch adapter (stdio).
"""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time

HOME = Path(__file__).resolve().parent
POLICY = Path("/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-router/policy.json")
PYTHON = Path("/var/lib/generic-linux-automator-exec/matrix-external-mcp/venv/bin/python")
FETCH = HOME / "external_mcp.py"
LEDGER = HOME / "mcp-quota.sqlite3"
SLOT = "mcp-fetch-docs"
REQUIRED = {
    "id": SLOT,
    "provider": "mcp-server-fetch",
    "type": "mcp",
    "transport": "stdio",
    "tool": "fetch",
    "self_hosted": True,
    "open_source_license_reviewed": True,
    "license": "MIT",
    "paid_fallback_allowed": False,
    "public_only": True,
    "private_network_allowed": False,
}

def read_slot():
    policy = json.loads(POLICY.read_text())
    if policy.get("version") != 1 or policy.get("paid_inference_allowed") is not False:
        raise RuntimeError("Unsafe global policy")
    slots = policy.get("tool_connections", [])
    if len(slots) != 1:
        raise RuntimeError("Unexpected MCP tool registry")
    slot = slots[0]
    if any(slot.get(key) != val for key, val in REQUIRED.items()):
        raise RuntimeError("Unexpected MCP tool policy")
    if slot.get("quota_group") != "matrix-dev-docs":
        raise RuntimeError("Unexpected quota group")
    for key, cap in (("conservative_daily_requests", 500), ("conservative_minute_requests", 10)):
        n = slot.get(key)
        if type(n) is not int or not 1 <= n <= cap:
            raise RuntimeError("Unsafe tool quota")
    seconds = slot.get("cooldown_seconds")
    if type(seconds) is not int or not 30 <= seconds <= 3600:
        raise RuntimeError("Unsafe cooldown")
    return slot

def ledger():
    db = sqlite3.connect(LEDGER, timeout=15, isolation_level=None)
    db.execute("PRAGMA busy_timeout=15000")
    db.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, slot TEXT, grp TEXT, ts INTEGER, state TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS cooldowns (slot TEXT PRIMARY KEY, until_epoch INTEGER)")
    LEDGER.chmod(0o600)
    return db

def counts(db, slot, now):
    grp = slot["quota_group"]
    day = now - (now % 86400)
    d = db.execute("SELECT count(*) FROM events WHERE grp=? AND ts>=?", (grp, day)).fetchone()[0]
    m = db.execute("SELECT count(*) FROM events WHERE grp=? AND ts>=?", (grp, now - 60)).fetchone()[0]
    row = db.execute("SELECT until_epoch FROM cooldowns WHERE slot=?", (SLOT,)).fetchone()
    return d, m, max(0, row[0] - now) if row else 0

def status():
    s = read_slot()
    db = ledger()
    try:
        d, m, wait = counts(db, s, int(time.time()))
    finally:
        db.close()
    return {
        "slot": SLOT, "provider": s["provider"], "transport": "stdio",
        "enabled": s.get("enabled") is True, "read_only": True,
        "daily_used": d, "daily_cap": s["conservative_daily_requests"],
        "minute_used": m, "minute_cap": s["conservative_minute_requests"],
        "cooldown_seconds_remaining": wait, "paid_fallback": False,
        "credential_source": "none",
    }

def check_url(url):
    if not isinstance(url, str) or len(url) > 500:
        raise ValueError("Invalid URL")
    proc = subprocess.run([str(PYTHON), str(FETCH), "validate", url],
                          capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=12)
    if proc.returncode or json.loads(proc.stdout).get("valid") is not True:
        raise ValueError("Public source URL not allowed")
    return url

def reserve(slot):
    if slot.get("enabled") is not True:
        raise RuntimeError("External MCP slot disabled")
    db = ledger()
    try:
        db.execute("BEGIN IMMEDIATE")
        now = int(time.time())
        d, m, wait = counts(db, slot, now)
        if (wait or d >= slot["conservative_daily_requests"]
                or m >= slot["conservative_minute_requests"]):
            raise RuntimeError("External MCP quota exhausted or cooling down")
        db.execute("INSERT INTO events(slot,grp,ts,state) VALUES(?,?,?,?)",
                   (SLOT, slot["quota_group"], now, "reserved"))
        event_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.commit()
        return event_id
    finally:
        db.close()

def record(event_id, success, slot):
    db = ledger()
    try:
        db.execute("BEGIN IMMEDIATE")
        db.execute("UPDATE events SET state=? WHERE id=?",
                   ("completed" if success else "failed", event_id))
        if not success:
            db.execute("INSERT OR REPLACE INTO cooldowns(slot,until_epoch) VALUES(?,?)",
                       (SLOT, int(time.time()) + slot["cooldown_seconds"]))
        db.commit()
    finally:
        db.close()

def fetch(url):
    check_url(url)
    slot = read_slot()
    event_id = reserve(slot)
    try:
        proc = subprocess.run([str(PYTHON), str(FETCH), "fetch", url],
                              capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=65)
        if proc.returncode:
            raise RuntimeError("MCP upstream failed")
        data = json.loads(proc.stdout)
        if (data.get("provider") != "external-mcp"
                or data.get("server") != "mcp-server-fetch"
                or data.get("writes_performed") is not False
                or data.get("url") != url
                or not data.get("text")):
            raise RuntimeError("MCP result validation failed")
    except Exception:
        record(event_id, False, slot)
        raise
    record(event_id, True, slot)
    data.update({"tool_slot": SLOT, "quota_group": slot["quota_group"],
                 "quota_event_id": event_id})
    return data

def main(argv):
    if len(argv) == 1 and argv[0] == "status":
        print(json.dumps(status())); return
    if len(argv) == 1 and argv[0] == "selftest":
        s = read_slot()
        assert s["enabled"] is True
        check_url("https://docs.python.org/3/library/asyncio-task.html")
        try:
            check_url("https://127.0.0.1/")
        except ValueError:
            pass
        else:
            raise AssertionError("Private source accepted")
        print(json.dumps({"passed": True, "tool_slots": 1, "paid": False,
                          "safe_validation": True})); return
    if len(argv) == 2 and argv[0] == "validate":
        read_slot()
        print(json.dumps({"valid": True, "url": check_url(argv[1])})); return
    if len(argv) == 2 and argv[0] == "fetch":
        print(json.dumps(fetch(argv[1]), ensure_ascii=False)); return
    raise ValueError("Usage: mcp_tool_router.py status|selftest|validate URL|fetch URL")

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ValueError, RuntimeError, sqlite3.Error, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": type(exc).__name__, "detail": str(exc)[:140]}), file=sys.stderr)
        raise SystemExit(2)
