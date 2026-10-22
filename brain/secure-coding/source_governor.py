#!/usr/bin/env python3
"""A1 review-only, source-governed proposal gate; no model, shell or file apply.

Run separately from the live Matrix dispatcher. Passing this validator does NOT
authorize sandbox execution; an independent reviewer must approve exact SHA and
the existing reviewed_patch_runner must independently pass its own isolation gate.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

PROJECT = "pine_mcp_chat"
MANIFEST = "pine_chat_v1"
WORK_ID = "pine_chat_b1_synthetic_review_v1"
REPOSITORY = "aarondash5-star/business-house-matrix"
BASE_BRANCH = "docs/modular-mcp-chat-template-20261022"
ARTIFACTS = frozenset({
    "frontend/pine-chat-a11y.html",
    "tests/test_pine_chat_a11y.py",
})
MAX_TOTAL_BYTES = 24000
MAX_FILE_BYTES = 18000
FORBIDDEN = (
    r"\b(?:fetch|XMLHttpRequest|WebSocket|sendBeacon)\b",
    r"\b(?:localStorage|sessionStorage|document\.cookie)\b",
    r"\b(?:eval|exec|__import__)\s*\(",
    r"\b(?:password|service_role|api[_-]?key|private.?key|bearer|auth.?token)\b",
    r"https?://",
    r"<script\b[^>]*\bsrc\s*=",
    r"<iframe\b",
    r"\b(?:child_process|subprocess|socket|ctypes|os\.system|os\.popen)\b",
)
ALLOWED_TEST_IMPORTS = frozenset({"unittest", "pathlib", "re"})

class PolicyDenied(ValueError):
    """Generic denial codes avoid echoing private proposals in logs."""


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _path(value):
    if not isinstance(value, str) or "\x00" in value or "\\" in value:
        raise PolicyDenied("invalid_path")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "." in p.parts or value not in ARTIFACTS:
        raise PolicyDenied("path_not_enrolled")
    return value


def _content(path, value):
    if not isinstance(value, str):
        raise PolicyDenied("content_must_be_text")
    raw = value.encode("utf-8")
    if not raw or len(raw) > MAX_FILE_BYTES:
        raise PolicyDenied("file_size_denied")
    if any(re.search(pattern, value, re.IGNORECASE) for pattern in FORBIDDEN):
        raise PolicyDenied("unsafe_content_pattern")
    if path.endswith(".html"):
        lowered = value.lower()
        for fragment in ('<html lang="en"', "name=\"viewport\"", "<main", "pine", "chat"):
            if fragment not in lowered:
                raise PolicyDenied("required_accessibility_marker_missing")
        if re.search(r"<(?:script|link)\b[^>]*\b(?:src|href)\s*=", value, re.I):
            raise PolicyDenied("external_dependency_denied")
    else:
        try:
            tree = ast.parse(value, filename="synthetic_test.py")
        except SyntaxError as exc:
            raise PolicyDenied("test_syntax_denied") from exc
        imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
        for n in imports:
            names = [a.name.split(".")[0] for a in n.names] if isinstance(n, ast.Import) else [(n.module or "").split(".")[0]]
            if any(name not in ALLOWED_TEST_IMPORTS for name in names):
                raise PolicyDenied("test_import_not_enrolled")
        if "unittest" not in value or not re.search(r"\bdef test_[a-zA-Z_]", value):
            raise PolicyDenied("independent_test_missing")
    return raw


def inspect(envelope, baseline=None):
    """Validate exactly two enrolled synthetic paths and return *non-executable*
    review metadata plus a pinned payload for independent human/security review.

    baseline is collected by a trusted worktree inspector, never by the model.
    No file is created, overwritten, tested or executed in this module.
    """
    if not isinstance(envelope, dict) or set(envelope) != {"project", "manifest", "work_id", "repository", "base_branch", "files"}:
        raise PolicyDenied("envelope_schema_denied")
    expected = (PROJECT, MANIFEST, WORK_ID, REPOSITORY, BASE_BRANCH)
    got = tuple(envelope[k] for k in ("project", "manifest", "work_id", "repository", "base_branch"))
    if got != expected:
        raise PolicyDenied("scope_mismatch")
    files = envelope["files"]
    if not isinstance(files, list) or len(files) != 2:
        raise PolicyDenied("exact_file_count_required")
    if baseline is None:
        baseline = {}
    if not isinstance(baseline, dict) or set(baseline) - ARTIFACTS:
        raise PolicyDenied("baseline_scope_denied")
    if not all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) for v in baseline.values()):
        raise PolicyDenied("baseline_hash_denied")
    prepared = []
    total = 0
    names = set()
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "content"}:
            raise PolicyDenied("proposal_file_schema_denied")
        name = _path(entry["path"])
        if name in names:
            raise PolicyDenied("duplicate_target")
        names.add(name)
        content = _content(name, entry["content"])
        total += len(content)
        prepared.append({"path": name, "content": entry["content"],
                         "expected_sha256": baseline.get(name)})
    if names != ARTIFACTS or total > MAX_TOTAL_BYTES:
        raise PolicyDenied("manifest_artifacts_mismatch")
    payload = {"files": sorted(prepared, key=lambda item: item["path"])}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return {"status": "needs_independent_review", "project": PROJECT, "work_id": WORK_ID,
            "repository": REPOSITORY, "branch": BASE_BRANCH, "review_sha256": _sha(encoded),
            "files": [{"path": item["path"], "sha256": _sha(item["content"].encode("utf-8"))}
                      for item in payload["files"]], "payload": payload,
            "executed": False, "published": False, "approved": False}


def main():
    parser = argparse.ArgumentParser(description="Validate enrolled offline proposal; never execute")
    parser.add_argument("proposal_json", type=Path)
    args = parser.parse_args()
    path = args.proposal_json
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 27000:
        raise PolicyDenied("proposal_file_denied")
    raw = json.loads(path.read_text(encoding="utf-8"))
    receipt = inspect(raw)
    receipt.pop("payload")  # Never log source code or accidental secrets.
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (PolicyDenied, ValueError, OSError, json.JSONDecodeError) as exc:
        reason = str(exc) if isinstance(exc, PolicyDenied) else "malformed_input"
        print(json.dumps({"status": "blocked", "reason": reason}), file=sys.stderr)
        sys.exit(2)
