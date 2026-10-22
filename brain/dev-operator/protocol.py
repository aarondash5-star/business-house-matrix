"""Pure policy validator for repo-enrolled, offline Dev Operator proposals.

No host writes, model calls, commands or outbound connections in this module.
A manifest must be loaded by trusted controller code, never from model output.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import PurePosixPath
import re

class PolicyError(ValueError):
    pass

PROJECT = re.compile(r"^[a-z][a-z0-9_-]{1,31}$")
SHA40 = re.compile(r"^[a-f0-9]{40}$")
SAFE_PATH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_./-]{0,139}$")
MAX_FILE_BYTES = 32000
MAX_TOTAL_BYTES = 64000
MAX_FILE_COUNT = 8
MAX_ATTEMPTS = 3
ALLOWED_TEST_PROFILES = frozenset({"python-unittest", "static-html", "node-test"})

@dataclass(frozen=True)
class Manifest:
    project: str
    repository: str
    base_sha: str
    files: tuple[str, ...]
    test_profile: str
    write_enabled: bool = False

def path(value: object) -> str:
    if not isinstance(value, str) or not SAFE_PATH.fullmatch(value):
        raise PolicyError("bad_path")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "." in p.parts or value.startswith(".") or "//" in value:
        raise PolicyError("path_escape")
    if any(x.startswith(".") for x in p.parts):
        raise PolicyError("hidden_path_denied")
    if not (p.suffix in (".py", ".html", ".css", ".js", ".json", ".md", ".txt")):
        raise PolicyError("file_type_denied")
    return value

def enroll(record: object) -> Manifest:
    if not isinstance(record, dict) or set(record) != {
        "project", "repository", "base_sha", "files", "test_profile", "write_enabled"}:
        raise PolicyError("manifest_schema")
    project = record["project"]
    repo = record["repository"]
    sha = record["base_sha"]
    if not isinstance(project, str) or not PROJECT.fullmatch(project):
        raise PolicyError("project_id")
    if not isinstance(repo, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", repo):
        raise PolicyError("repository_id")
    if not isinstance(sha, str) or not SHA40.fullmatch(sha):
        raise PolicyError("unpinned_baseline")
    files = record["files"]
    if (not isinstance(files, list) or not 1 <= len(files) <= MAX_FILE_COUNT
            or any(not isinstance(x, str) for x in files)):
        raise PolicyError("scope_size")
    frozen = tuple(path(x) for x in files)
    if len(set(frozen)) != len(frozen):
        raise PolicyError("duplicate_path")
    profile = record["test_profile"]
    if profile not in ALLOWED_TEST_PROFILES:
        raise PolicyError("test_profile")
    if record["write_enabled"] is not True:
        raise PolicyError("not_enrolled_for_write")
    return Manifest(project, repo, sha, frozen, profile, True)

def validate_proposal(enrolled: Manifest, proposal: object):
    if not isinstance(enrolled, Manifest) or enrolled.write_enabled is not True:
        raise PolicyError("missing_enrollment")
    if not isinstance(proposal, dict) or set(proposal) != {"files", "summary"}:
        raise PolicyError("proposal_schema")
    if not isinstance(proposal["summary"], str) or len(proposal["summary"]) > 1000:
        raise PolicyError("summary_invalid")
    files = proposal["files"]
    if not isinstance(files, list) or not 1 <= len(files) <= len(enrolled.files):
        raise PolicyError("files_schema")
    total = 0
    seen = set()
    normalized = []
    for f in files:
        if not isinstance(f, dict) or set(f) != {"path", "content"}:
            raise PolicyError("file_schema")
        name = path(f["path"])
        if name not in enrolled.files or name in seen or name.startswith("tests/"):
            raise PolicyError("path_not_enrolled")
        seen.add(name)
        contents = f["content"]
        if not isinstance(contents, str):
            raise PolicyError("non_text_source")
        data = contents.encode("utf-8")
        total += len(data)
        if len(data) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
            raise PolicyError("source_size")
        # Deny evident attempts at credential exfiltration and dangerous native binaries.
        if re.search(r"(?i)(?:-----BEGIN PRIVATE KEY-----|(?:api[_-]?key|token|password)\s*[:=]\s*['\"][^'\" ]{12,})", contents):
            raise PolicyError("credential_literal")
        normalized.append({"path": name, "content": contents, "sha256": hashlib.sha256(data).hexdigest()})
    review = {"project": enrolled.project, "repository": enrolled.repository,
              "base_sha": enrolled.base_sha, "test_profile": enrolled.test_profile,
              "files": normalized, "status": "needs_independent_qa",
              "remote_write": False, "published": False}
    review["review_sha256"] = hashlib.sha256(
        json.dumps(review, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return review
