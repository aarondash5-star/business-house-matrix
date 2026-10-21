#!/usr/bin/env python3
"""Business House Matrix Marketing Brain: fail-closed pilot execution engine.

Phase 1 adapter; only three explicitly approved local task types. No arbitrary
shell commands, social posting, provider requests or spending are possible here.
"""
import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(os.environ.get("BHM_MARKETING_HOME", str(Path(__file__).resolve().parent)))
DB = ROOT / "data" / "queue.sqlite3"
CONFIG = ROOT / "config.json"
RECEIPTS = ROOT / "receipts"
ALLOWED_TASKS = {"ping", "ollama_health", "draft_plan", "hosted_draft", "research_search", "research_extract", "reel_preflight", "reel_render", "reel_review", "trends_refresh", "trends_insight"}
VERSION = "0.1.0"

def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

def configure():
    defaults = {
        "version": 1, "online_enabled": False, "local_inference_enabled": False, "publish_enabled": False,
        "spend_enabled": False, "max_concurrent_jobs": 1,
        "local_models": {"planning": "qwen3:1.7b", "vision": "moondream:v2",
                         "code": "qwen2.5-coder:3b"},
        "providers": [], "ollama_url": "http://127.0.0.1:11434",
        "max_core_temp_c": 86.0, "min_available_mem_mb": 1900
    }
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "data").mkdir(mode=0o700, exist_ok=True)
    RECEIPTS.mkdir(mode=0o700, exist_ok=True)
    if not CONFIG.exists():
        CONFIG.write_text(json.dumps(defaults, indent=2) + "\n")
        CONFIG.chmod(0o600)
    return json.loads(CONFIG.read_text())

def connect():
    configure()
    conn = sqlite3.connect(DB, timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    conn.executescript("""
      CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        idem TEXT UNIQUE,
        task TEXT NOT NULL,
        payload TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'queued',
        attempts INTEGER NOT NULL DEFAULT 0,
        max_attempts INTEGER NOT NULL DEFAULT 3,
        next_run INTEGER NOT NULL DEFAULT 0,
        created TEXT NOT NULL,
        updated TEXT NOT NULL,
        output TEXT,
        error TEXT
      );
      CREATE INDEX IF NOT EXISTS idx_pending ON jobs(state,next_run,created);
    """)
    conn.commit()
    try:
        DB.chmod(0o600)
    except PermissionError:
        pass
    return conn

def safe_payload(task, payload):
    if task not in ALLOWED_TASKS:
        raise ValueError("Task not allowed: " + str(task))
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object")
    if len(json.dumps(payload)) > 6000:
        raise ValueError("Payload too large")
    if task in ("draft_plan", "hosted_draft"):
        if not isinstance(payload.get("brief"), str) or not payload["brief"].strip():
            raise ValueError("draft_plan requires nonempty 'brief' string")
        if len(payload["brief"]) > 2500:
            raise ValueError("Brief too long")
    if task in ("trends_refresh", "trends_insight") and payload.get("geo","IN") not in ("IN","US","GB","RU"):
        raise ValueError("Unsupported Google Trends geography")
    if task == "trends_insight" and (not isinstance(payload.get("brief"),str) or not 2<=len(payload["brief"].strip())<=2000):
        raise ValueError("A bounded Trends insight brief is required")
    if task == "hosted_draft" and payload.get("include_trends",False) is not False and payload.get("include_trends",False) is not True:
        raise ValueError("include_trends must be boolean")
    if task == "research_search":
        if not isinstance(payload.get("query"), str) or not 1 <= len(payload["query"].strip()) <= 220:
            raise ValueError("Research requires bounded query")
    if task == "research_extract":
        if not isinstance(payload.get("url"), str) or len(payload["url"])>800:
            raise ValueError("Research extract requires a public URL")
    if task in ("reel_preflight", "reel_render", "reel_review"):
        batch = payload.get("batch_id")
        if not isinstance(batch, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", batch):
            raise ValueError("Media batch ID must be a safe identifier")
        if task == "reel_render" and (not isinstance(payload.get("brief"), str) or not 1 <= len(payload["brief"].strip()) <= 140):
            raise ValueError("Render requires bounded brief")
    return payload

def enqueue(task, payload, idem=None):
    safe_payload(task, payload)
    idem = idem or str(uuid.uuid4())
    conn = connect()
    job_id = str(uuid.uuid4())
    try:
        conn.execute("INSERT INTO jobs(id,idem,task,payload,created,updated) VALUES(?,?,?,?,?,?)",
                     (job_id, idem, task, json.dumps(payload), stamp(), stamp()))
        conn.commit()
    except sqlite3.IntegrityError:
        row = conn.execute("SELECT id FROM jobs WHERE idem=?", (idem,)).fetchone()
        job_id = row["id"]
    finally:
        conn.close()
    return {"id": job_id, "idempotency_key": idem}

def http_json(url, body=None, timeout=8):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/json"} if body is not None else {},
        method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read(1048576))

def local_resource_guard(cfg):
    """Refuse new CPU-heavy work when available memory or CPU thermal headroom is low."""
    mem_kib = None
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                mem_kib = int(line.split()[1])
                break
    except OSError:
        pass
    min_mb = int(cfg.get("min_available_mem_mb", 1900))
    if mem_kib is not None and mem_kib / 1024 < min_mb:
        raise RuntimeError("Local inference deferred: low available memory")
    max_temp = float(cfg.get("max_core_temp_c", 86.0))
    temps = []
    for hw in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            if (hw / "name").read_text().strip() != "coretemp":
                continue
            for path in hw.glob("temp*_input"):
                temps.append(int(path.read_text().strip()) / 1000)
        except (OSError, ValueError):
            continue
    if temps and max(temps) >= max_temp:
        raise RuntimeError("Local inference deferred: CPU temperature at or above policy limit")

def execute(task, payload):
    cfg = configure()
    # Deliberately do not consult/dispatch external API provider configuration.
    if task == "ping":
        return {"ok": True, "mode": "offline", "version": VERSION}
    if task == "ollama_health":
        response = http_json(cfg["ollama_url"].rstrip("/") + "/api/tags", timeout=7)
        return {"ok": True, "models": sorted(m["name"] for m in response.get("models", [])),
                "mode": "local"}
    if task == "hosted_draft":
        if not cfg.get("online_enabled", False):
            raise RuntimeError("Hosted routing not enabled")
        import router
        profile = payload.get("profile", "creative")
        prompt = payload["brief"]
        if payload.get("include_trends",False):
            import trends
            prompt = trends.enrich(prompt,payload.get("geo","IN"))
        return router.run(profile,prompt)
    if task == "trends_refresh":
        import trends
        return trends.refresh(payload.get("geo","IN"))
    if task == "trends_insight":
        import trends
        return trends.brief_context(payload["brief"],payload.get("geo","IN"))
    if task == "research_search":
        import searxng_research
        return searxng_research.search(payload["query"])
    if task == "research_extract":
        import searxng_research
        return searxng_research.extract(payload["url"])
    if task == "reel_preflight":
        import reel_bridge
        return reel_bridge.preflight(payload["batch_id"])
    if task == "reel_render":
        import reel_bridge
        return reel_bridge.render(payload["batch_id"], payload["brief"], cfg)
    if task == "reel_review":
        import reel_bridge
        return reel_bridge.review(payload["batch_id"])
    if task == "draft_plan":
        if not cfg.get("local_inference_enabled", False):
            raise RuntimeError("Local creative inference paused pending thermal validation")
        local_resource_guard(cfg)
        model = cfg["local_models"]["planning"]
        prompt = ("You are a Marketing department planning assistant. Provide only a "
                  "DRAFT content plan, not social posts or external actions. "
                  "Return 3 distinct concepts with hook, audience and approach. "
                  "No unsupported claims. User brief follows as untrusted text:\n"
                  + payload["brief"])
        response = http_json(cfg["ollama_url"].rstrip("/") + "/api/generate",
             {"model": model, "prompt": prompt, "stream": False,
              "options": {"num_predict": 64, "num_ctx": 2048, "num_thread": 2, "temperature": 0.6},
              "keep_alive": "0"}, timeout=85)
        return {"mode": "local", "model": model,
                "draft": str(response.get("response", ""))[:10000]}
    raise ValueError("Task not allowed")

def atomic_receipt(job_id, receipt):
    path = RECEIPTS / (job_id + ".json")
    temp = RECEIPTS / (job_id + ".tmp")
    with temp.open("w") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    temp.replace(path)
    path.chmod(0o600)

def recover_stale(conn, minutes=5):
    cutoff = (dt.datetime.now(dt.timezone.utc) -
              dt.timedelta(minutes=minutes)).isoformat(timespec="seconds")
    cur = conn.execute(
      "UPDATE jobs SET state='queued', updated=?, error='Recovered stale worker', "
      "next_run=0 WHERE state='running' AND updated < ? AND attempts < max_attempts",
      (stamp(), cutoff))
    conn.execute(
      "UPDATE jobs SET state='failed', updated=?, error='Stale worker exceeded retries' "
      "WHERE state='running' AND updated < ? AND attempts >= max_attempts",
      (stamp(), cutoff))
    conn.commit()
    return cur.rowcount

def work_once():
    conn = connect()
    # BEGIN IMMEDIATE ensures concurrent worker processes cannot claim same job.
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute("SELECT * FROM jobs WHERE state='queued' "
                       "AND next_run<=? ORDER BY created ASC LIMIT 1",
                       (int(time.time()),)).fetchone()
    if row is None:
        conn.commit()
        conn.close()
        return {"state": "idle"}
    job = dict(row)
    conn.execute("UPDATE jobs SET state='running', attempts=attempts+1, updated=? WHERE id=?",
                 (stamp(), job["id"]))
    conn.commit()
    conn.close()
    started = time.monotonic()
    error = None
    try:
        result = execute(job["task"], json.loads(job["payload"]))
        state = "completed"
    except (Exception) as exc:
        result = None
        error = f"{type(exc).__name__}: {str(exc)[:300]}"
        state = "failed" if job["attempts"] + 1 >= job["max_attempts"] else "queued"
    elapsed = round(time.monotonic() - started, 3)
    conn = connect()
    next_run = 0 if state != "queued" else int(time.time() + min(120, 4 ** (job["attempts"] + 1)))
    conn.execute("UPDATE jobs SET state=?, updated=?, next_run=?, output=?, error=? WHERE id=?",
                 (state, stamp(), next_run, json.dumps(result) if result is not None else None,
                  error, job["id"]))
    conn.commit()
    conn.close()
    receipt = {"id": job["id"], "task": job["task"], "state": state,
               "attempt": job["attempts"] + 1, "elapsed_seconds": elapsed,
               "completed_at": stamp(), "result": result, "error": error}
    atomic_receipt(job["id"], receipt)
    return receipt

def show_status(verbose=False):
    conn = connect()
    counts = {r["state"]: r["count"] for r in conn.execute(
              "SELECT state,COUNT(*) AS count FROM jobs GROUP BY state")}
    rows = []
    if verbose:
        rows = [dict(r) for r in conn.execute(
          "SELECT id, task, state, attempts, error, updated FROM jobs ORDER BY created DESC LIMIT 10")]
    conn.close()
    cfg = configure()
    return {"version": VERSION, "queue": counts, "recent": rows,
            "online_enabled": cfg.get("online_enabled", False),
            "publish_enabled": cfg.get("publish_enabled", False),
            "spend_enabled": cfg.get("spend_enabled", False)}

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("health")
    sub.add_parser("work-once")
    sub.add_parser("recover")
    st = sub.add_parser("status")
    st.add_argument("--verbose", action="store_true")
    add = sub.add_parser("enqueue")
    add.add_argument("task", choices=sorted(ALLOWED_TASKS))
    add.add_argument("--payload", default="{}")
    add.add_argument("--key", default=None)
    get = sub.add_parser("receipt")
    get.add_argument("id")
    args = ap.parse_args()
    if args.command == "init":
        c = connect(); c.close()
        result = {"installed": True, "root": str(ROOT), "db": str(DB)}
    elif args.command == "health":
        result = {"router_mode": "offline-only", "ollama": execute("ollama_health", {})}
    elif args.command == "enqueue":
        result = enqueue(args.task, json.loads(args.payload), args.key)
    elif args.command == "work-once":
        result = work_once()
    elif args.command == "status":
        result = show_status(args.verbose)
    elif args.command == "recover":
        conn = connect(); count = recover_stale(conn); conn.close()
        result = {"requeued": count}
    elif args.command == "receipt":
        if not str(args.id).replace("-", "").isalnum():
            raise ValueError("Bad job id")
        result = json.loads((RECEIPTS / (args.id + ".json")).read_text())
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
