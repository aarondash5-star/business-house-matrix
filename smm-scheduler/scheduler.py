"""Provider-neutral, read-only job scheduler. No purchasing actions are supported."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import tempfile

UTC = dt.timezone.utc
ALLOWED_ACTIONS = frozenset({"services", "balance", "status"})
JOB_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,80}$")


def utcnow():
    return dt.datetime.now(UTC)


def timestamp(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def iso(value):
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path, fallback):
    file = pathlib.Path(path)
    if not file.exists():
        return fallback
    with file.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path, payload):
    file = pathlib.Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=file.parent, delete=False, encoding="utf-8") as tmp:
        json.dump(payload, tmp, indent=2, sort_keys=True)
        tmp.write("\n")
        candidate = tmp.name
    os.replace(candidate, file)


def validate_jobs(document):
    if not isinstance(document, dict) or not isinstance(document.get("jobs"), list):
        raise ValueError("jobs.json must be {'jobs': [...]}")
    seen = set()
    for job in document["jobs"]:
        if not isinstance(job, dict):
            raise ValueError("Each job must be an object")
        key = job.get("id")
        if not isinstance(key, str) or not JOB_ID_RE.fullmatch(key) or key in seen:
            raise ValueError("Invalid or duplicate job id")
        seen.add(key)
        if job.get("provider") != "fansmm":
            raise ValueError("Unrecognized provider (register an adapter first)")
        if job.get("action") not in ALLOWED_ACTIONS:
            raise ValueError("Only read-only provider actions are enabled")
        period = job.get("interval_minutes")
        if type(period) is not int or not 5 <= period <= 40320:
            raise ValueError("interval_minutes must be an integer between 5 and 40320")
        if "enabled" in job and type(job["enabled"]) is not bool:
            raise ValueError("enabled must be boolean")
        params = job.get("params", {})
        if not isinstance(params, dict):
            raise ValueError("params must be an object")
        if job["action"] == "status":
            order = params.get("order")
            if not isinstance(order, (int, str)) or not str(order).isdigit():
                raise ValueError("Status requires a numeric order identifier")
        elif params:
            raise ValueError("services/balance do not accept params")
    return document["jobs"]


def run_due(jobs, state, execute, now=None, dry_run=True):
    now = now or utcnow()
    if now.tzinfo is None:
        raise ValueError("now must have a timezone")
    next_state = {"jobs": dict(state.get("jobs", {}))}
    results = []
    for job in jobs:
        if not job.get("enabled", True):
            results.append({"job_id": job["id"], "result": "disabled"})
            continue
        key = job["id"]
        old = next_state["jobs"].get(key, {})
        upcoming = old.get("next_run_at")
        if upcoming and timestamp(upcoming) > now:
            results.append({"job_id": key, "result": "not_due"})
            continue
        if dry_run:
            results.append({"job_id": key, "result": "dry_run_due"})
            continue
        try:
            response = execute(job["provider"], job["action"], job.get("params", {}))
            detail = {"job_id": key, "result": "success"}
            if job["action"] == "status":
                detail["provider_status"] = response.get("status", "unknown")
            next_state["jobs"][key] = {
                "last_run_at": iso(now),
                "next_run_at": iso(now + dt.timedelta(minutes=job["interval_minutes"])),
                "result": "success",
            }
        except Exception as exc:
            # Never persist a provider exception body: it could echo credentials.
            detail = {"job_id": key, "result": "error", "error_type": type(exc).__name__}
            next_state["jobs"][key] = {
                "last_run_at": iso(now),
                "next_run_at": iso(now + dt.timedelta(minutes=min(15, job["interval_minutes"]))),
                "result": "error",
                "error_type": type(exc).__name__,
            }
        results.append(detail)
    return next_state, results


def execute_provider(provider, action, params):
    if provider == "fansmm":
        from providers.fansmm import FanSMM
        return FanSMM.from_environment().call(action, params)
    raise ValueError("Unknown provider")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jobs", default="jobs.json")
    p.add_argument("--state", default="state.json")
    p.add_argument("--execute-read-only", action="store_true")
    a = p.parse_args()
    jobs = validate_jobs(load_json(a.jobs, {"jobs": []}))
    state = load_json(a.state, {"jobs": {}})
    next_state, details = run_due(jobs, state, execute_provider, dry_run=not a.execute_read_only)
    if a.execute_read_only and next_state != state:
        write_json_atomic(a.state, next_state)
    print(json.dumps({"mode": "read_only" if a.execute_read_only else "dry_run", "results": details}, sort_keys=True))
    return 1 if any(x["result"] == "error" for x in details) else 0


if __name__ == "__main__":
    sys.exit(main())
