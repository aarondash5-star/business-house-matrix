#!/usr/bin/env python3
"""SuperGPT promotion policy: checks inputs and evidence; no deployments or merges.

Important: CI is not a substitute for GitHub branch protection or human QA.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = ROOT / "docs/supergpt/qa/RELEASE_EVIDENCE.json"
REQUIRED = [
    "docs/supergpt/README.md",
    "docs/supergpt/PROJECT_PLAN.md",
    "docs/supergpt/RELEASE_POLICY.md",
    "docs/supergpt/qa/RELEASE_EVIDENCE.json",
    "docs/supergpt/qa/EVIDENCE_GUIDE.md",
    "scripts/supergpt/release_gate.py",
    ".github/workflows/supergpt-release-gates.yml",
    ".github/workflows/supergpt-android-debug.yml",
    ".github/CODEOWNERS",
]
EXPECTED = {
    "super-gpt/test": "super-gpt/dev",
    "super-gpt/production": "super-gpt/test",
}
RUN_RE = re.compile(
    r"^https://github\.com/aarondash5-star/business-house-matrix/actions/runs/([0-9]+)$"
)
HEX40 = re.compile(r"^[0-9a-fA-F]{40}$")
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


class GateError(Exception):
    """Policy violation or unverifiable evidence."""


def require(condition, message):
    if not condition:
        raise GateError(message)


def validate_route(event, base="", head=""):
    if event == "pull_request":
        require(base in EXPECTED, "Invalid SuperGPT PR destination: " + base)
        require(head == EXPECTED[base],
                "Promotion to %s must originate from %s, not %s" % (base, EXPECTED[base], head))
        return base == "super-gpt/production"
    require(event in ("push", "workflow_dispatch"), "Unexpected event: " + event)
    return False  # Direct pushes cannot be blocked by CI without branch rules.


def validate_documents(root=ROOT):
    absent = [name for name in REQUIRED if not (root / name).is_file()]
    require(not absent, "Required canonical source files missing: " + ", ".join(absent))
    docs = (root / "docs/supergpt/README.md").read_text(encoding="utf-8")
    require("PROJECT_PLAN.md" in docs and "RELEASE_POLICY.md" in docs,
            "SuperGPT canonical README must link product and release policy")
    evidence = json.loads((root / "docs/supergpt/qa/RELEASE_EVIDENCE.json")
                          .read_text(encoding="utf-8"))
    require(evidence.get("schema_version") == "1.0", "Unknown QA evidence schema")
    for key in ("android_build", "android_runtime", "independent_qa", "owner_acceptance"):
        require(isinstance(evidence.get(key), dict), "Evidence must contain " + key)
    return evidence


def verify_build_from_github(evidence, tested_commit):
    build = evidence["android_build"]
    match = RUN_RE.fullmatch(build.get("run_url", ""))
    require(match is not None, "Provide valid GitHub Actions build run URL")
    run_id = match.group(1)
    token = os.getenv("GITHUB_TOKEN", "")
    require(token, "Missing read-only GITHUB_TOKEN for Actions provenance verification")

    def read_json(path):
        req = urllib.request.Request(
            "https://api.github.com/repos/aarondash5-star/business-house-matrix/" + path,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + token,
                "User-Agent": "SuperGPT-CI-release-policy",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.load(res)

    run = read_json("actions/runs/" + run_id)
    require(run.get("conclusion") == "success", "Build run is not successful")
    require(run.get("head_sha") == tested_commit, "Build run SHA != tested commit")
    require(run.get("path") == ".github/workflows/supergpt-android-debug.yml",
            "Evidence run is not the documented Android workflow")
    artifacts = read_json("actions/runs/" + run_id + "/artifacts")
    require(any(
        a.get("name") == build.get("artifact_name") and not a.get("expired", True)
        for a in artifacts.get("artifacts", [])
    ), "Expected Android artifact is missing or expired")


def validate_production(evidence, git_ancestry=True, online=True):
    build = evidence["android_build"]
    runtime = evidence["android_runtime"]
    qa = evidence["independent_qa"]
    owner = evidence["owner_acceptance"]

    require(evidence.get("candidate") not in ("", "UNASSIGNED", None),
            "A release candidate name/version is required")
    require(build.get("source_mode") == "project-integrated",
            "An upstream-only PocketPal prototype cannot be certified as SuperGPT")
    sha = evidence.get("tested_commit", "")
    require(bool(HEX40.fullmatch(sha)), "Provide actual 40-character tested source commit")
    require(bool(HEX64.fullmatch(build.get("apk_sha256", ""))),
            "Provide 64-hex SHA256 of APK file, not artifact ZIP")
    for check in ("install", "cold_start", "crash_scan", "interaction"):
        require(runtime.get(check) == "passed", "Android runtime check not passed: " + check)
    require(runtime.get("device_type") in ("emulator", "physical"),
            "Record emulator or physical device type")
    require(isinstance(runtime.get("android_api"), int)
            and runtime["android_api"] >= 23, "Record actual tested Android API level")
    require(runtime.get("receipt_url", "").startswith("https://"),
            "Link actual Android test receipts")
    require(qa.get("status") == "passed", "Independent QA not certified")
    require(qa.get("reviewer", "").strip(), "QA reviewer required")
    require(qa.get("receipt_url", "").startswith("https://"), "QA receipt URL required")
    require(owner.get("status") == "passed", "Owner acceptance missing")
    require(owner.get("approval_reference", "").startswith("https://"),
            "Link exact candidate owner approval")
    require(not evidence.get("known_blockers"), "Unresolved release blockers remain")

    if git_ancestry:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", sha, "HEAD"],
            check=False, capture_output=True, text=True,
        )
        require(result.returncode == 0,
                "Tested build source SHA is not an ancestor of the proposed release")
    if online:
        verify_build_from_github(evidence, sha)


def main():
    event = os.getenv("GITHUB_EVENT_NAME", "workflow_dispatch")
    base = os.getenv("GITHUB_BASE_REF", "")
    head = os.getenv("GITHUB_HEAD_REF", "")
    evidence = validate_documents()
    production_pr = validate_route(event, base, head)
    if production_pr:
        validate_production(evidence)
        print("PASS: production PR includes validated candidate evidence")
    else:
        print("PASS: SuperGPT source documents and promotion route are valid")
        print("INFO: a non-production result is NOT an Android runtime certification")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (GateError, OSError, ValueError, KeyError, urllib.error.URLError) as exc:
        print("SUPERGPT GATE FAILED:", str(exc), file=sys.stderr)
        sys.exit(1)
