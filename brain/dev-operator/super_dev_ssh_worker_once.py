#!/usr/bin/env python3
"""One-shot, read-only Dev Brain responder for the staged SSH duplex mailbox.

This adapter has exactly one fixed action: report existing controller health.
It cannot execute a task, mutate controller state, run arbitrary model commands,
publish, spend, or change the v6 SSH gateway. The Super Brain triggers it via
the already authenticated Dell development lane; replies are polled via SSH.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from super_dev_ssh_duplex import DEFAULT_DB, Mailbox, canonical

CONTROLLER = Path("/var/lib/generic-linux-automator-exec/matrix-controller/controller.py")
PYTHON = Path("/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-brain/venv/bin/python")


def controller_status() -> dict:
    if not CONTROLLER.is_file() or not PYTHON.is_file():
        return {"state": "unavailable", "reason": "known_controller_missing"}
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(Path.home()),
        "LANG": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    try:
        run = subprocess.run(
            [str(PYTHON), str(CONTROLLER), "status"],
            capture_output=True, text=True, timeout=18, env=env,
            stdin=subprocess.DEVNULL,
        )
        if run.returncode != 0:
            return {"state": "unavailable", "reason": "controller_status_failed",
                    "exit_code": run.returncode}
        doc = json.loads(run.stdout)
        service = subprocess.run(
            ["/usr/bin/systemctl", "--user", "is-active", "bhm-autonomy-controller.service"],
            capture_output=True, text=True, timeout=8, env=env,
            stdin=subprocess.DEVNULL,
        )
        return {
            "state": "ready" if service.stdout.strip() == "active" else "degraded",
            "controller_version": doc.get("controller_version"),
            "host": doc.get("host"),
            "counts": doc.get("counts", {}),
            "paid": doc.get("paid"),
            "auto_publish": doc.get("auto_publish"),
            "controller_service": service.stdout.strip(),
        }
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return {"state": "unavailable", "reason": "status_exception"}


def respond_once(mailbox: Mailbox) -> dict:
    inbox = mailbox.poll(recipient="dev", after=0, limit=100)
    replies = mailbox.poll(recipient="super", after=0, limit=100)
    handled = {m["in_reply_to"] for m in replies if m["in_reply_to"]}
    for message in inbox:
        if message["kind"] != "task" or message["message_id"] in handled:
            continue
        body = message["body"]
        if body.get("operation") != "controller_status" or set(body) != {"operation", "nonce"}:
            continue
        nonce = body["nonce"]
        if not isinstance(nonce, str) or not 1 <= len(nonce) <= 64 or not nonce.isascii():
            continue
        receipt = controller_status()
        receipt["nonce"] = nonce
        ident = "dev-result-" + hashlib.sha256(
            message["message_id"].encode("ascii")
        ).hexdigest()[:20]
        inserted = mailbox.send(
            message_id=ident, thread_id=message["thread_id"],
            sender="dev", kind="result", body=receipt,
            in_reply_to=message["message_id"],
        )
        return {"handled": True, "thread_id": message["thread_id"],
                "message_id": ident, "insert": inserted,
                "brain_state": receipt["state"]}
    return {"handled": False, "reason": "no_pending_supported_task"}


def main() -> int:
    box = Mailbox(DEFAULT_DB)
    try:
        print(canonical(respond_once(box)))
        return 0
    finally:
        box.close()


if __name__ == "__main__":
    raise SystemExit(main())
