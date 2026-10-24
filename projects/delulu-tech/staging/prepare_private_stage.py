"""Prepare a hash-verified, local-only Delulu stage package for Matrix Tool Yard.

No production website, external network, payments, publishing or root privileges.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

PROJECT=Path(__file__).resolve().parents[1]
CONTROLLER=Path("/var/lib/generic-linux-automator-exec/matrix-controller")
DEST_ROOT=CONTROLLER/"staging-inbox"/"delulu_tech"
MANIFEST_ID="delulu_homepage_v1"
SOURCE_COMMIT="f073228d685cc56e7b4cb5a5a1b1a00de71b94ce"
LOGO_SHA256="d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368"
OLD_SRC="../../brand/assets/delulu-tech-mobile-white.svg"
NEW_SRC="assets/delulu-tech-mobile-white.svg"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    historic=subprocess.run(["git","-C",str(PROJECT),"show",
        SOURCE_COMMIT+":projects/delulu-tech/staging/site/index.html"],
        capture_output=True,timeout=10)
    if historic.returncode or historic.stdout != (PROJECT/"staging/site/index.html").read_bytes():
        raise RuntimeError("approved_homepage_source_drift")
    from sys import path as python_path
    python_path.insert(0,str(CONTROLLER))
    try:
        from project_registry import enroll_check
        if enroll_check("delulu_tech","website_stage",MANIFEST_ID)!="static_v1":
            raise RuntimeError("project_not_approved_for_static_stage")
    finally:
        python_path.remove(str(CONTROLLER))
    page=(PROJECT/"staging/site/index.html").read_text(encoding="utf-8")
    if page.count(OLD_SRC)!=1:
        raise RuntimeError("approved_logo_reference_mismatch")
    page=page.replace(OLD_SRC,NEW_SRC)
    logo=(PROJECT/"brand/assets/delulu-tech-mobile-white.svg").read_bytes()
    if sha(logo)!=LOGO_SHA256:
        raise RuntimeError("logo_integrity_mismatch")
    if not all(v in page for v in (
        "noindex,nofollow", "#0B0D13", "#F5F6F2", "#C9FF3D", "#6544EA",
        'id="skip-motion"', "@media(prefers-reduced-motion:reduce)"
    )):
        raise RuntimeError("approved_brand_or_accessibility_lock_missing")
    files={"index.html":page.encode("utf-8"),NEW_SRC:logo}
    manifest={
        "schema_version":1,"project":"delulu_tech","manifest":MANIFEST_ID,
        "publish":False,"spend":False,
        "files":{name:sha(data) for name,data in files.items()}
    }
    DEST_ROOT.mkdir(mode=0o700,parents=True,exist_ok=True)
    site_parent=DEST_ROOT/MANIFEST_ID
    site_dir=site_parent/"site"
    manifest_path=DEST_ROOT/(MANIFEST_ID+".json")
    if site_parent.exists() or manifest_path.exists():
        raise RuntimeError("existing_stage_input_requires_readonly_audit")
    with tempfile.TemporaryDirectory(prefix=".prepare-delulu-",dir=DEST_ROOT) as tempname:
        temp=Path(tempname)
        work=temp/"site"
        work.mkdir(mode=0o700)
        for name,data in files.items():
            dest=work/name
            dest.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            dest.write_bytes(data);dest.chmod(0o600)
        checker=CONTROLLER/"project_static_stage.py"
        import sys
        sys.path.insert(0,str(CONTROLLER))
        try:
            import project_static_stage
            project_static_stage.validate_source
        finally:
            sys.path.remove(str(CONTROLLER))
        # Place the prepared site atomically; manifest is the final commit marker.
        site_parent.mkdir(mode=0o700)
        work.rename(site_dir)
        manifest_path.write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n",encoding="utf-8")
        manifest_path.chmod(0o600)
    print(json.dumps({"state":"input_prepared","project":"delulu_tech",
                      "manifest":MANIFEST_ID,"source_commit":SOURCE_COMMIT,
                      "logo_sha256":LOGO_SHA256,"files":list(files),
                      "publication":False,"spend":False},indent=2))

if __name__=="__main__":
    main()
