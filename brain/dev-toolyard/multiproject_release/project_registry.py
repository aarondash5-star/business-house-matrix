"""Owner-approved, fail-closed multi-project Matrix Tool Yard registry.

The registry is a local owner-reviewed manifest; it is never filled by model text.
No wildcard projects, shell commands, filesystem paths or executables from JSON.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
import sys

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "project_registry_v1.json"
SAFE = re.compile(r"^[a-z][a-z0-9_-]{1,39}$")
ENGINES = {
    "website_stage": {"legacy_moksha", "static_v1"},
    "dev_project_build": {"reviewed_patch_v1"},
}

class EnrollmentError(ValueError):
    pass

def _slug(value: str) -> str:
    if not isinstance(value, str) or not SAFE.fullmatch(value):
        raise EnrollmentError("invalid_project_or_manifest_id")
    return value

def load_registry(path: Path = REGISTRY) -> dict:
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise EnrollmentError("registry_missing_or_symlinked")
    st = path.stat()
    if st.st_size > 65536 or st.st_size < 20:
        raise EnrollmentError("registry_size_rejected")
    if st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise EnrollmentError("registry_not_owner_private")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or set(obj) != {"schema_version", "projects"} or obj["schema_version"] != 1:
        raise EnrollmentError("bad_registry_schema")
    projects = obj["projects"]
    if not isinstance(projects, list) or not (1 <= len(projects) <= 100):
        raise EnrollmentError("invalid_project_count")
    seen = set()
    approved = {}
    for item in projects:
        if not isinstance(item, dict) or set(item) != {"project", "approved", "actions"}:
            raise EnrollmentError("invalid_project_record")
        name = _slug(item["project"])
        if name in seen:
            raise EnrollmentError("duplicate_project")
        seen.add(name)
        if item["approved"] is not True:
            continue
        actions = item["actions"]
        if not isinstance(actions, dict) or not actions or set(actions) - set(ENGINES):
            raise EnrollmentError("unsupported_action")
        recorded = {}
        for action, manifests in actions.items():
            if not isinstance(manifests, dict) or not manifests or len(manifests) > 30:
                raise EnrollmentError("invalid_manifest_table")
            checked = {}
            for manifest, engine in manifests.items():
                _slug(manifest)
                if engine not in ENGINES[action]:
                    raise EnrollmentError("unapproved_runner")
                if engine == "legacy_moksha" and (name, action, manifest) != (
                        "moksha_overhaul", "website_stage", "moksha_overhaul_v1"):
                    raise EnrollmentError("legacy_runner_restricted")
                checked[manifest] = engine
            recorded[action] = checked
        approved[name] = recorded
    return approved

def enroll_check(project: str, action: str, manifest: str, registry_path: Path = REGISTRY) -> str:
    _slug(project)
    _slug(manifest)
    if action not in ENGINES:
        raise EnrollmentError("unknown_project_action")
    engine = load_registry(registry_path).get(project, {}).get(action, {}).get(manifest)
    if engine is None:
        raise EnrollmentError("project_manifest_not_enrolled")
    return engine

def website_command(home: Path, project: str, manifest: str, registry_path: Path = REGISTRY) -> list[str]:
    engine = enroll_check(project, "website_stage", manifest, registry_path)
    script = "site_staging.py" if engine == "legacy_moksha" else "project_static_stage.py"
    return [sys.executable, str(Path(home) / script), "build", project, manifest]

def patch_allowed(project: str, registry_path: Path = REGISTRY) -> bool:
    _slug(project)
    return bool(load_registry(registry_path).get(project, {}).get("dev_project_build"))

def fixed_patch_path(home: Path, project: str, manifest: str,
                     registry_path: Path = REGISTRY) -> Path:
    enroll_check(project, "dev_project_build", manifest, registry_path)
    path = Path(home) / "engineering-inbox" / project / (manifest + ".json")
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 330000:
        raise EnrollmentError("reviewed_patch_missing_or_invalid")
    return path

def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("status", "check", "patch-check"))
    p.add_argument("project", nargs="?")
    p.add_argument("action", nargs="?")
    p.add_argument("manifest", nargs="?")
    args = p.parse_args()
    if args.command == "status":
        data = load_registry()
        print(json.dumps({"schema_version": 1, "projects": sorted(data),
                          "enrolled": sum(sum(len(v) for v in a.values()) for a in data.values())}))
    elif args.command == "check":
        print(json.dumps({"project": args.project, "action": args.action,
                          "manifest": args.manifest,
                          "engine": enroll_check(args.project, args.action, args.manifest)}))
    else:
        print(json.dumps({"allowed": patch_allowed(args.project)}))

if __name__ == "__main__":
    main()
