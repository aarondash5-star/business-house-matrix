#!/usr/bin/env python3
"""Bounded two-way Super Brain <-> Dev Brain mailbox over the *existing* v6 SSH lane.

This is a transport/data-plane candidate, NOT an execution gateway or a new
identity provider. The authenticated Generic SSH gateway is the ingress; this
module never opens a listener, launches commands, grants privileges or invokes
models. Its SSH-facing CLI only submits Super messages; fixed Dev adapters use the
internal API. This is defense-in-depth, not an independent local role identity.
Worker receipts remain independently verified by the existing ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import time

SCHEMA = 1
ID = re.compile(r"^[a-z][a-z0-9._:-]{7,95}$")
KINDS = {
    "super": frozenset(("task", "answer", "cancel")),
    "dev": frozenset(("accepted", "progress", "question", "result", "error")),
}
MAX_BODY_BYTES = 16384
MAX_EVENTS_PER_THREAD = 256
DEFAULT_DB = Path.home() / ".local/share/matrix-dev-brain/ssh_duplex_v1.sqlite3"


class Denied(ValueError):
    pass


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def valid_id(value: str) -> bool:
    return isinstance(value, str) and ID.fullmatch(value) is not None


class Mailbox:
    def __init__(self, path: Path):
        self.path = Path(path)
        if self.path.is_symlink():
            raise Denied("database_symlink_denied")
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.path.exists() and not self.path.is_file():
            raise Denied("database_not_regular")
        self.db = sqlite3.connect(self.path, timeout=10)
        self.db.execute("PRAGMA busy_timeout=10000")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS messages(
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT NOT NULL UNIQUE,
            thread_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            kind TEXT NOT NULL,
            body TEXT NOT NULL,
            in_reply_to TEXT,
            created_at INTEGER NOT NULL,
            prev_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL
            )"""
        )
        self.db.execute(
            "CREATE INDEX IF NOT EXISTS messages_thread_seq ON messages(thread_id,seq)"
        )
        self.db.execute(
            "CREATE INDEX IF NOT EXISTS messages_reply_lookup ON messages(in_reply_to,sender)"
        )
        self.db.commit()
        try:
            self.path.chmod(0o600)
        except OSError:
            pass

    def close(self):
        self.db.close()

    def send(
        self,
        *,
        message_id: str,
        thread_id: str,
        sender: str,
        kind: str,
        body: dict,
        in_reply_to: str | None = None,
    ) -> dict:
        if not valid_id(message_id) or not valid_id(thread_id):
            raise Denied("invalid_message_or_thread_id")
        if sender not in KINDS or kind not in KINDS[sender]:
            raise Denied("invalid_actor_or_message_kind")
        if not isinstance(body, dict) or not body:
            raise Denied("body_must_be_nonempty_object")
        encoded = canonical(body)
        if len(encoded.encode("utf8")) > MAX_BODY_BYTES:
            raise Denied("message_size_limit")
        if in_reply_to is not None and not valid_id(in_reply_to):
            raise Denied("invalid_reply_reference")
        doc = {
            "schema": SCHEMA,
            "message_id": message_id,
            "thread_id": thread_id,
            "sender": sender,
            "kind": kind,
            "body": body,
            "in_reply_to": in_reply_to,
        }
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            old = self.db.execute(
                "SELECT seq,thread_id,sender,kind,body,in_reply_to FROM messages WHERE message_id=?",
                (message_id,),
            ).fetchone()
            if old is not None:
                same = (
                    old[1] == thread_id
                    and old[2] == sender
                    and old[3] == kind
                    and old[4] == encoded
                    and old[5] == in_reply_to
                )
                if not same:
                    raise Denied("message_idempotency_conflict")
                return {"seq": old[0], "message_id": message_id, "deduplicated": True}
            rows = self.db.execute(
                "SELECT message_id,sender,kind,event_hash FROM messages WHERE thread_id=? ORDER BY seq",
                (thread_id,),
            ).fetchall()
            if len(rows) >= MAX_EVENTS_PER_THREAD:
                raise Denied("thread_event_limit")
            if any(r[2] in ("result", "error") for r in rows):
                raise Denied("terminal_thread_closed")
            if not rows:
                if (sender, kind, in_reply_to) != ("super", "task", None):
                    raise Denied("thread_requires_owner_task")
            else:
                if kind == "task":
                    raise Denied("one_task_per_thread")
                if in_reply_to is None:
                    raise Denied("reply_reference_required")
                parent = next((r for r in rows if r[0] == in_reply_to), None)
                if parent is None:
                    raise Denied("reply_not_in_thread")
                if parent[1] == sender:
                    raise Denied("reply_must_cross_roles")
                if kind == "answer" and parent[2] != "question":
                    raise Denied("answer_requires_question")
                if parent[2] == "result" or parent[2] == "error":
                    raise Denied("terminal_thread_closed")
            prev = rows[-1][3] if rows else "0" * 64
            stamp = int(time.time())
            event_hash = hashlib.sha256(
                (prev + canonical(doc) + str(stamp)).encode("utf8")
            ).hexdigest()
            cur = self.db.execute(
                """INSERT INTO messages(message_id,thread_id,sender,kind,body,
                in_reply_to,created_at,prev_hash,event_hash)
                VALUES(?,?,?,?,?,?,?,?,?)""",
                (message_id, thread_id, sender, kind, encoded, in_reply_to,
                 stamp, prev, event_hash),
            )
        return {"seq": cur.lastrowid, "message_id": message_id, "deduplicated": False}

    def poll(self, *, recipient: str, after: int = 0, limit: int = 50) -> list[dict]:
        if recipient not in KINDS:
            raise Denied("invalid_recipient")
        if type(after) is not int or after < 0 or type(limit) is not int or not 1 <= limit <= 100:
            raise Denied("invalid_cursor_or_limit")
        sender = "dev" if recipient == "super" else "super"
        rows = self.db.execute(
            """SELECT seq,message_id,thread_id,sender,kind,body,in_reply_to,
            created_at,event_hash FROM messages
            WHERE seq>? AND sender=? ORDER BY seq LIMIT ?""",
            (after, sender, limit),
        ).fetchall()
        return [
            {
                "seq": r[0], "message_id": r[1], "thread_id": r[2],
                "sender": r[3], "kind": r[4], "body": json.loads(r[5]),
                "in_reply_to": r[6], "created_at": r[7], "event_hash": r[8],
            }
            for r in rows
        ]

    def verify_thread(self, thread_id: str) -> dict:
        if not valid_id(thread_id):
            raise Denied("invalid_thread_id")
        rows = self.db.execute(
            """SELECT message_id,sender,kind,body,in_reply_to,created_at,
            prev_hash,event_hash FROM messages WHERE thread_id=? ORDER BY seq""",
            (thread_id,),
        ).fetchall()
        prev = "0" * 64
        for r in rows:
            doc = {
                "schema": SCHEMA, "message_id": r[0], "thread_id": thread_id,
                "sender": r[1], "kind": r[2], "body": json.loads(r[3]),
                "in_reply_to": r[4],
            }
            calculated = hashlib.sha256(
                (prev + canonical(doc) + str(r[5])).encode("utf8")
            ).hexdigest()
            if r[6] != prev or r[7] != calculated:
                raise Denied("audit_hash_chain_mismatch")
            prev = calculated
        return {"thread_id": thread_id, "events": len(rows), "chain_verified": True,
                "head_hash": prev}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fixed-function SSH duplex mailbox; no execution")
    sub = parser.add_subparsers(dest="action", required=True)
    send = sub.add_parser("send")
    send.add_argument("--message-id", required=True)
    send.add_argument("--thread-id", required=True)
    send.add_argument("--sender", choices=("super",), required=True)
    send.add_argument("--kind", required=True)
    send.add_argument("--body-json", required=True)
    send.add_argument("--reply-to")
    poll = sub.add_parser("poll")
    poll.add_argument("--recipient", choices=tuple(KINDS), required=True)
    poll.add_argument("--after", type=int, default=0)
    poll.add_argument("--limit", type=int, default=50)
    verify = sub.add_parser("verify")
    verify.add_argument("--thread-id", required=True)
    args = parser.parse_args()
    mailbox = Mailbox(DEFAULT_DB)
    try:
        if args.action == "send":
            result = mailbox.send(
                message_id=args.message_id, thread_id=args.thread_id,
                sender=args.sender, kind=args.kind,
                body=json.loads(args.body_json), in_reply_to=args.reply_to,
            )
        elif args.action == "poll":
            result = {"messages": mailbox.poll(
                recipient=args.recipient, after=args.after, limit=args.limit)}
        else:
            result = mailbox.verify_thread(args.thread_id)
        print(canonical(result))
        return 0
    except (Denied, json.JSONDecodeError) as exc:
        print(canonical({"denied": str(exc)}))
        return 2
    finally:
        mailbox.close()


if __name__ == "__main__":
    raise SystemExit(main())
