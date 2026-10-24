"""Offline, bounded, per-project static staging. No network or public server."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
INBOX = ROOT / "staging-inbox"
OUTPUT = ROOT / "staging-private"
SAFE = re.compile(r"^[a-z][a-z0-9_-]{1,39}$")
FILE_SUFFIX = {".html", ".css", ".js", ".json", ".svg", ".png", ".webp", ".jpg", ".jpeg", ".txt"}
MAX_TOTAL = 3_500_000
MAX_FILES = 80

def reject(msg: str):
    raise ValueError(msg)

def checked_name(name):
    if not isinstance(name, str) or not SAFE.fullmatch(name):
        reject("invalid_id")
    return name

def checked_relative(value):
    if not isinstance(value, str) or len(value) > 180 or "\\" in value:
        reject("invalid_relative_path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in ("", ".", "..") or x.startswith(".") for x in p.parts):
        reject("path_escape")
    if not 1 <= len(p.parts) <= 5 or p.suffix.lower() not in FILE_SUFFIX:
        reject("unsupported_static_file")
    if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", x) for x in p.parts):
        reject("unexpected_file_name")
    return p

def validate_source(project, manifest_id, root=ROOT):
    checked_name(project); checked_name(manifest_id)
    inbox = Path(root) / "staging-inbox" / project
    manifest_path = inbox / (manifest_id + ".json")
    if manifest_path.is_symlink() or not manifest_path.is_file() or manifest_path.stat().st_size > 40000:
        reject("manifest_missing_or_unsafe")
    obj = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or set(obj) != {
        "schema_version", "project", "manifest", "publish", "spend", "files"
    } or obj["schema_version"] != 1 or obj["project"] != project or obj["manifest"] != manifest_id:
        reject("manifest_schema_mismatch")
    if obj["publish"] is not False or obj["spend"] is not False:
        reject("external_action_denied")
    files = obj["files"]
    if not isinstance(files, dict) or not (1 <= len(files) <= MAX_FILES) or "index.html" not in files:
        reject("file_list_missing_index")
    source_dir = inbox / manifest_id / "site"
    if source_dir.is_symlink() or not source_dir.is_dir():
        reject("site_source_missing")
    total = 0
    audited = {}
    for relative, expected in files.items():
        rel = checked_relative(relative)
        if not isinstance(expected, str) or not re.fullmatch("[a-f0-9]{64}", expected):
            reject("digest_required")
        source = source_dir.joinpath(*rel.parts)
        if any(x.is_symlink() for x in (source, *source.parents) if x != Path(root).parent):
            reject("symlink_denied")
        if not source.is_file():
            reject("missing_approved_file")
        size = source.stat().st_size
        total += size
        if size > 1_500_000 or total > MAX_TOTAL:
            reject("static_size_limit")
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            reject("source_digest_mismatch")
        if rel.suffix == ".html":
            low = data.decode("utf-8").lower()
            if ("noindex" not in low or "<form" in low or
                "http://" in low or "https://" in low or
                "<iframe" in low or 'src="//' in low or
                'href="//' in low or "serviceworker" in low):
                reject("unsafe_or_indexable_markup")
        audited[relative] = source
    listed = set(files)
    on_disk = {p.relative_to(source_dir).as_posix() for p in source_dir.rglob("*") if p.is_file()}
    if on_disk != listed:
        reject("unlisted_or_missing_file")
    return obj, manifest_path, audited

def build(project, manifest_id, root=ROOT):
    from project_registry import enroll_check
    enroll_check(project, "website_stage", manifest_id, Path(root)/"project_registry_v1.json")
    obj, manifest_path, audited = validate_source(project, manifest_id, root)
    digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()[:20]
    parent = Path(root) / "staging-private" / project
    if parent.is_symlink():
        reject("stage_parent_symlink")
    parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    parent.chmod(0o700)
    target = parent / digest
    if target.exists():
        receipt_path = target / "receipt.json"
        if receipt_path.is_symlink() or not receipt_path.is_file():
            reject("existing_stage_unverified")
        old = json.loads(receipt_path.read_text())
        if old.get("project") != project or old.get("manifest_id") != manifest_id:
            reject("existing_stage_inconsistent")
        return {**old, "deduplicated": True}
    tmp = Path(tempfile.mkdtemp(prefix=".multi-stage-", dir=parent))
    try:
        for name, source in audited.items():
            dest = tmp.joinpath(*PurePosixPath(name).parts)
            dest.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            shutil.copyfile(source, dest, follow_symlinks=False)
            dest.chmod(0o600)
        (tmp/"robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
        receipt = {
            "state": "private_preview_ready", "project": project, "manifest_id": manifest_id,
            "sha256_prefix": digest, "files": sorted(audited), "pages": sum(n.endswith(".html") for n in audited),
            "local_path": str(target), "publication": False, "spend": False,
            "nonindexed": True, "external_services": False, "server_started": False,
            "qa_passed": True, "created_utc": datetime.now(timezone.utc).isoformat()
        }
        (tmp/"receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        (tmp/"receipt.json").chmod(0o600)
        tmp.chmod(0o700)
        tmp.rename(target)
        return receipt
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("action", choices=("validate", "build"))
    p.add_argument("project"); p.add_argument("manifest")
    args=p.parse_args()
    if args.action == "build":
        print(json.dumps(build(args.project,args.manifest),indent=2))
    else:
        obj,_,audited=validate_source(args.project,args.manifest)
        print(json.dumps({"valid":True,"files":len(audited),"publish":False,"spend":False}))
