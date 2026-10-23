#!/usr/bin/env python3
"""Owner-scoped canary listener for the existing Dell SSH duplex mailbox.

No network listener, no task execution, no new credentials. It processes only
the fixed read-only controller-status request delegated to worker_once.
Untrusted task text can never become a command.
"""
from __future__ import annotations

import json
import signal
import threading

from super_dev_ssh_duplex import DEFAULT_DB, Mailbox, canonical
from super_dev_ssh_worker_once import respond_once

STOP = threading.Event()


def stop(_signum, _frame):
    STOP.set()


def serve(poll_seconds: float = 3.0) -> int:
    if not 1.0 <= poll_seconds <= 30.0:
        raise ValueError("invalid_poll_interval")
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    mailbox = Mailbox(DEFAULT_DB)
    print(canonical({"event": "listener_started", "mode": "read_only_fixed_function",
                     "db": "owner_local_mailbox"}), flush=True)
    try:
        while not STOP.is_set():
            outcome = respond_once(mailbox)
            if outcome.get("handled"):
                print(canonical({"event": "dev_response", **outcome}), flush=True)
            STOP.wait(poll_seconds)
    finally:
        mailbox.close()
        print(canonical({"event": "listener_stopped"}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(serve())
