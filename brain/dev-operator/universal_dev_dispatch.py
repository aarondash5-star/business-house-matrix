"""Candidate Dev Brain dynamic-intake workcell, separate from certified v6.

Universal toolchain commands execute INSIDE an isolated rootless OCI container,
not through arbitrary host shell or the generic SSH bridge. Owner-approved jobs
are signed locally; Github issue bodies and model outputs cannot grant access.
No daemon is installed by importing this module. Production release is gated.
"""
from __future__ import annotations
import dataclasses
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import time
import urllib.request

ID = re.compile(r"^[a-z][a-z0-9._:-]{5,110}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[0-9a-f]{40}$")
IMAGE = re.compile(r"^[a-z0-9./:_-]+@sha256:[0-9a-f]{64}$")
MODEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_./:-]{1,80}$")
MAX_OUTPUT = 10000
MAX_CMD = 5000

class Denied(ValueError):
    pass

def canonical(doc):
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf8")

def sign_owner(doc, key):
    if not isinstance(key, bytes) or len(key) < 32:
        raise Denied("owner_signing_key_missing")
    return hmac.new(key, canonical(doc), hashlib.sha256).hexdigest()

def validate_request(doc, signature, key):
    """No hardcoded project/task-name allowlist: owner signature IS enrollment.

    An owner-approved *data descriptor* is required for isolation and audit.
    Unauthenticated GitHub content must never become executable authority.
    """
    if not isinstance(doc, dict) or doc.get("schema") != 1:
        raise Denied("bad_schema")
    required = {"schema", "task_id", "project", "repository", "base_sha",
                "objective", "model", "image", "test_command", "approval_ref",
                "max_steps", "max_seconds", "trusted_tests"}
    if set(doc) != required:
        raise Denied("unexpected_scope_fields")
    if not isinstance(signature, str) or not re.fullmatch(r"[0-9a-f]{64}", signature):
        raise Denied("signature_format")
    if not hmac.compare_digest(sign_owner(doc, key), signature):
        raise Denied("owner_signature_mismatch")
    if not all(isinstance(doc[k], str) and doc[k] for k in (
            "task_id", "project", "repository", "base_sha", "objective",
            "model", "image", "test_command", "approval_ref")):
        raise Denied("invalid_fields")
    if not ID.fullmatch(doc["task_id"]) or not ID.fullmatch(doc["project"]):
        raise Denied("invalid_identity")
    if (not REPO.fullmatch(doc["repository"]) or not SHA.fullmatch(doc["base_sha"])
        or any(segment in (".", "..") or segment.startswith(".")
               or ".." in segment for segment in doc["repository"].split("/"))):
        raise Denied("unapproved_repository_identity")
    if not IMAGE.fullmatch(doc["image"]):
        raise Denied("image_must_be_pinned_by_digest")
    if not MODEL.fullmatch(doc["model"]):
        raise Denied("invalid_model_identity")
    if not 30 <= len(doc["objective"]) <= 9000:
        raise Denied("invalid_objective")
    trusted = doc["trusted_tests"]
    if not isinstance(trusted, dict) or not 1 <= len(trusted) <= 40:
        raise Denied("trusted_tests_required")
    for rel, digest in trusted.items():
        if (not isinstance(rel, str) or not isinstance(digest, str)
            or not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_./-]{0,170}", rel)
            or rel.startswith("/") or ".." in Path(rel).parts or
            not re.fullmatch(r"[a-f0-9]{64}", digest)):
            raise Denied("invalid_trusted_test_identity")
    if not 8 <= len(doc["approval_ref"]) <= 500:
        raise Denied("approval_record_missing")
    if not 1 <= len(doc["test_command"]) <= MAX_CMD:
        raise Denied("trusted_test_command_invalid")
    # These strings are sent to a container; still disallow control characters.
    if any(ord(c) < 32 and c not in "\n\t" for c in doc["test_command"]):
        raise Denied("test_control_character")
    if type(doc["max_steps"]) is not int or not 1 <= doc["max_steps"] <= 100:
        raise Denied("step_budget")
    if type(doc["max_seconds"]) is not int or not 60 <= doc["max_seconds"] <= 14400:
        raise Denied("runtime_budget")
    return doc

def task_workspace(root, ident):
    root = Path(root).expanduser().resolve(strict=True)
    if not root.is_dir() or root.is_symlink() or not ID.fullmatch(ident):
        raise Denied("bad_workspace_root")
    work = root / ident
    if work.is_symlink() or not work.is_dir() or work.resolve() != work:
        raise Denied("unregistered_workspace")
    # Never allow model/container controlled symlinks to influence host path resolution.
    return work

def verify_trusted_tests(work, approved):
    """Independent QA files must stay exactly as the owner approved."""
    for rel, digest in approved.items():
        path=work/rel
        if (path.is_symlink() or not path.is_file()
            or not path.resolve().is_relative_to(work.resolve())):
            raise Denied("trusted_test_missing_or_symlink")
        if path.stat().st_size > 1_000_000:
            raise Denied("trusted_test_size_limit")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise Denied("trusted_test_modified")

def validate_source(work, base_sha, repository):
    """Source was independently imported into private disposable workspace."""
    if not (work / ".git").is_dir() or (work / ".git").is_symlink():
        raise Denied("staged_source_not_a_checkout")
    p = subprocess.run(
        ["/usr/bin/git", "-c", "core.hooksPath=/dev/null", "rev-parse", "HEAD"],
        cwd=str(work), capture_output=True, text=True, timeout=12,
        env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
             "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": "/dev/null",
             "GIT_CONFIG_NOSYSTEM": "1"})
    if p.returncode or p.stdout.strip() != base_sha:
        raise Denied("repository_sha_mismatch")
    origin = subprocess.run(
        ["/usr/bin/git", "-c", "core.hooksPath=/dev/null", "remote", "get-url", "origin"],
        cwd=str(work), capture_output=True, text=True, timeout=12,
        env={"PATH":"/usr/bin:/bin", "HOME":"/nonexistent",
             "GIT_TERMINAL_PROMPT":"0","GIT_CONFIG_GLOBAL":"/dev/null",
             "GIT_CONFIG_NOSYSTEM":"1"})
    allowed={"https://github.com/"+repository,
             "https://github.com/"+repository+".git"}
    if origin.returncode or origin.stdout.strip() not in allowed:
        raise Denied("repository_origin_mismatch")
    # Refuse pre-dirty imports; never mistake previously modified workspace for pinned source.
    p = subprocess.run(
        ["/usr/bin/git", "-c", "core.hooksPath=/dev/null", "status", "--porcelain"],
        cwd=str(work), capture_output=True, text=True, timeout=12,
        env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
             "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": "/dev/null",
             "GIT_CONFIG_NOSYSTEM": "1"})
    if p.returncode or p.stdout.strip():
        raise Denied("source_workspace_not_clean")

def podman_argv(podman, image, work, command, *, read_only=False, cpu="2", memory="2g"):
    """Arbitrary developer commands are confined to the guest, never host shell."""
    if not isinstance(command, str) or not 1 <= len(command) <= MAX_CMD:
        raise Denied("invalid_guest_command")
    if not IMAGE.fullmatch(image):
        raise Denied("image_not_approved")
    work = Path(work).resolve(strict=True)
    if not work.is_dir() or work.is_symlink():
        raise Denied("invalid_workcell")
    if podman != "/usr/bin/podman":
        raise Denied("host_engine_must_be_pinned")
    git_dir = work / ".git"
    if not git_dir.is_dir() or git_dir.is_symlink():
        raise Denied("git_metadata_not_isolated")
    mount = f"{work}:/workspace:{'ro' if read_only else 'rw'},Z"
    metadata_mount = f"{git_dir}:/workspace/.git:ro,Z"
    return [
        podman, "run", "--rm", "--pull=never", "--network=none",
        "--cap-drop=all",
        "--security-opt=no-new-privileges", "--read-only",
        "--pids-limit=128", "--memory="+memory, "--cpus="+cpu,
        "--tmpfs=/tmp:rw,nosuid,nodev,size=128m",
        "--volume", mount, "--volume", metadata_mount,
        "--workdir", "/workspace",
        "--env=HOME=/tmp", "--env=CI=1", "--env=PYTHONDONTWRITEBYTECODE=1",
        "--entrypoint", "/bin/sh", image, "-lc", command
    ]

@dataclasses.dataclass
class Outcome:
    exit: int
    output: str
    stderr: str

class PodmanWorkcell:
    def __init__(self, work):
        self.work = Path(work)
    def execute(self, image, command, timeout, read_only=False):
        argv = podman_argv("/usr/bin/podman", image, self.work, command, read_only=read_only)
        # Podman itself needs the owner's existing rootless storage/runtime context.
        # Only the guest receives the restricted HOME=/tmp and approved volume.
        engine_env={"PATH":"/usr/bin:/bin", "HOME":str(Path.home()), "LANG":"C.UTF-8"}
        for name in ("XDG_RUNTIME_DIR", "CONTAINERS_STORAGE_CONF", "XDG_CONFIG_HOME"):
            value=os.environ.get(name)
            if value:
                engine_env[name]=value
        try:
            p = subprocess.run(argv, input="", capture_output=True, text=True,
                               timeout=timeout, env=engine_env)
        except subprocess.TimeoutExpired:
            return Outcome(124, "", "workcell_timeout")
        return Outcome(p.returncode, p.stdout[-MAX_OUTPUT:], p.stderr[-MAX_OUTPUT:])

class LocalModel:
    """Brain's existing loopback inference only; it has no host tools."""
    def __init__(self, name):
        self.name = name
    def next_action(self, request, history):
        prompt = (
            "You are the Development Matrix Brain. You own coding decisions, but all "
            "commands are executed by a disposable isolated project workcell. "
            "Reply exactly one JSON object: "
            '{"action":"command","command":"..."} or '
            '{"action":"finish","summary":"..."}. '
            "You may run normal build, coding, lint and test commands INSIDE the "
            "container. Do not request host/root/SSH, credentials, publishing or "
            "production side effects. The independent trusted tests run before final "
            "acceptance. If tests fail, repair source and retry. "
            "Goal: " + request["objective"] + "\n" +
            "Recent receipts: " + json.dumps(history[-5:])[-14000:]
        )
        body = canonical({
            "model": self.name, "stream": False, "format": "json",
            "prompt": prompt, "options": {"temperature": .1, "num_predict": 4000}
        })
        req = urllib.request.Request("http://127.0.0.1:11434/api/generate",
                                     body, headers={"Content-Type": "application/json"},
                                     method="POST")
        with urllib.request.urlopen(req, timeout=180) as res:
            if res.status != 200:
                raise Denied("model_http_failure")
            raw = res.read(120000)
        x = json.loads(raw)
        if x.get("model") not in (self.name, self.name+":latest"):
            raise Denied("model_response_identity")
        action = json.loads(x.get("response", ""))
        if not isinstance(action, dict):
            raise Denied("model_action_invalid")
        return action

class JobLedger:
    """Durable/idempotent. A crash never leads to accidental source-write replay."""
    def __init__(self, path):
        self.db = sqlite3.connect(str(path))
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("""CREATE TABLE IF NOT EXISTS jobs(
            task_id TEXT PRIMARY KEY, request TEXT NOT NULL, signature TEXT NOT NULL,
            state TEXT NOT NULL, steps INTEGER NOT NULL DEFAULT 0,
            receipt TEXT NOT NULL DEFAULT '{}', created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL)""")
        self.db.commit()
    def submit(self, request, signature, key):
        validate_request(request, signature, key)
        data=canonical(request).decode()
        now=int(time.time())
        try:
            self.db.execute("INSERT INTO jobs(task_id,request,signature,state,created_at,updated_at) VALUES(?,?,?,?,?,?)",
                            (request["task_id"],data,signature,"queued",now,now))
            self.db.commit()
            return {"task_id":request["task_id"],"state":"queued","deduplicated":False}
        except sqlite3.IntegrityError:
            row=self.db.execute("SELECT request,signature,state FROM jobs WHERE task_id=?",
                                (request["task_id"],)).fetchone()
            if row is None or row[0]!=data or row[1]!=signature:
                raise Denied("idempotency_key_conflict")
            return {"task_id":request["task_id"],"state":row[2],"deduplicated":True}
    def claim(self, ident):
        """No retry of running/blocked/failed jobs, even after machine crash."""
        with self.db:
            r=self.db.execute("UPDATE jobs SET state='running',updated_at=? WHERE task_id=? AND state='queued'",
                              (int(time.time()),ident))
        if r.rowcount!=1:
            raise Denied("not_claimable")
        row=self.db.execute("SELECT request,signature FROM jobs WHERE task_id=?",(ident,)).fetchone()
        return json.loads(row[0]),row[1]
    def finish(self, ident, state, steps, receipt):
        if state not in ("review_ready","needs_review","blocked","cancelled"):
            raise Denied("invalid_terminal_state")
        with self.db:
            self.db.execute("UPDATE jobs SET state=?,steps=?,receipt=?,updated_at=? WHERE task_id=? AND state='running'",
                            (state,steps,json.dumps(receipt),int(time.time()),ident))
    def status(self, ident):
        row=self.db.execute("SELECT state,steps,receipt,updated_at FROM jobs WHERE task_id=?",(ident,)).fetchone()
        return None if not row else {"state":row[0],"steps":row[1],
                                    "receipt":json.loads(row[2]),"updated_at":row[3]}
    def quarantine_orphaned(self):
        with self.db:
            return self.db.execute("UPDATE jobs SET state='needs_review', receipt='{\"reason\":\"orphaned_no_replay\"}' WHERE state='running'").rowcount


def verified_source_changes(work, request):
    """Require actual reviewable edits. Baseline passing tests alone are insufficient."""
    work = Path(work).resolve(strict=True)
    env = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent",
           "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": "/dev/null",
           "GIT_CONFIG_NOSYSTEM": "1"}
    def git(*argv):
        done = subprocess.run(
            ["/usr/bin/git", "-c", "core.hooksPath=/dev/null", *argv],
            cwd=str(work), capture_output=True, timeout=15, env=env)
        if done.returncode:
            raise Denied("source_identity_or_diff_failed")
        return done.stdout
    if git("rev-parse", "HEAD").decode().strip() != request["base_sha"]:
        raise Denied("source_baseline_modified")
    if git("remote", "get-url", "origin").decode().strip() not in {
            "https://github.com/"+request["repository"],
            "https://github.com/"+request["repository"]+".git"}:
        raise Denied("source_origin_modified")
    entries = git("-c", "status.renames=false", "status", "--porcelain=v1",
                  "--untracked-files=all", "-z").split(b"\0")
    names = []
    protected = set(request["trusted_tests"])
    for entry in entries:
        if not entry:
            continue
        if len(entry) < 4 or entry[2:3] != b" ":
            raise Denied("unexpected_git_status")
        name = entry[3:].decode("utf8", "surrogateescape")
        rel = Path(name)
        if (rel.is_absolute() or "." in rel.parts or ".." in rel.parts
            or name.startswith(".git") or name in protected):
            raise Denied("protected_source_change")
        full = work/rel
        if (not full.is_file() or full.is_symlink()
            or not full.resolve().is_relative_to(work)
            or full.stat().st_size > 1000000):
            raise Denied("unreviewable_source_change")
        if name not in names:
            names.append(name)
    if not names:
        raise Denied("no_source_changes")
    if len(names) > 100:
        raise Denied("source_change_budget")
    verify_trusted_tests(work, request["trusted_tests"])
    fingerprint = hashlib.sha256()
    for name in sorted(names):
        body = (work/name).read_bytes()
        fingerprint.update(name.encode("utf8", "surrogateescape")
                           + b"\0" + hashlib.sha256(body).digest())
    return {"changed_files": sorted(names),
            "change_sha256": fingerprint.hexdigest()}

def execute_job(ledger, ident, key, *, workspace_root, model_factory=LocalModel, backend_factory=PodmanWorkcell):
    request, signature = ledger.claim(ident)
    history=[]
    work = None
    try:
        validate_request(request, signature, key)
        work=task_workspace(workspace_root, request["task_id"])
        validate_source(work, request["base_sha"], request["repository"])
        verify_trusted_tests(work, request["trusted_tests"])
        engine=backend_factory(work)
        model=model_factory(request["model"])
        expires=time.monotonic()+request["max_seconds"]
        for step in range(1,request["max_steps"]+1):
            remaining=int(expires-time.monotonic())
            if remaining <= 0: raise Denied("task_time_budget")
            action=model.next_action(request, history)
            kind=action.get("action")
            if kind=="command" and set(action)=={"action","command"}:
                result=engine.execute(request["image"],action["command"],min(remaining,150))
                history.append({"step":step,"exit":result.exit,"output":result.output[-2500:],
                                "stderr":result.stderr[-1000:]})
                # Completion is determined by independent immutable QA, not by
                # the model saying 'finished' or exhausting an arbitrary step budget.
                if result.exit == 0:
                    try:
                        changed=verified_source_changes(work,request)
                    except Denied as exc:
                        if str(exc)!="no_source_changes":
                            raise
                    else:
                        qa_time=int(expires-time.monotonic())
                        if qa_time>2:
                            qa=engine.execute(request["image"],request["test_command"],
                                              min(qa_time,90),read_only=True)
                            if qa.exit==0:
                                verified_source_changes(work,request)
                                receipt={"summary":"independent_tests_passed_after_model_action",
                                         "qa_exit":qa.exit,"qa_stdout":qa.output[-5000:],
                                         "qa_stderr":qa.stderr[-2000:],
                                         "source_changes":changed,"model":request["model"],
                                         "workcell":"rootless_podman_offline",
                                         "model_steps":step,"published":False,"pushed":False}
                                ledger.finish(ident,"review_ready",step,receipt)
                                return ledger.status(ident)
                            history.append({"step":step,"independent_qa_exit":qa.exit,
                                            "qa_stderr":qa.stderr[-1200:]})
            elif kind=="finish" and set(action)=={"action","summary"}:
                if not history or not isinstance(action["summary"],str):
                    raise Denied("fake_finish_without_work")
                # Independent immutable owner-signed command; model cannot override it.
                diff_proof=verified_source_changes(work, request)
                verified=engine.execute(request["image"],request["test_command"],
                                        min(remaining,150),read_only=True)
                receipt={"summary":action["summary"][:1000],"qa_exit":verified.exit,
                         "qa_stdout":verified.output[-5000:],
                         "qa_stderr":verified.stderr[-2000:],
                         "model":request["model"],"workcell":"rootless_podman_offline",
                         "published":False,"pushed":False,"model_steps":step,
                         "source_changes":diff_proof}
                state="review_ready" if verified.exit==0 else "needs_review"
                ledger.finish(ident,state,step,receipt)
                return ledger.status(ident)
            else:
                history.append({"step":step,"denial":"unknown_model_action"})
        raise Denied("step_budget_exhausted")
    except Exception as exc:
        ledger.finish(ident,"needs_review",len(history),
                      {"reason":type(exc).__name__+":"+str(exc)[:220],"published":False})
        return ledger.status(ident)
