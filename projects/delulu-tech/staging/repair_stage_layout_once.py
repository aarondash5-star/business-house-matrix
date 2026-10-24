"""One-time recoverable layout repair for Delulu's *new* staging input only."""
import hashlib
import json
from pathlib import Path
import sys

BASE=Path("/var/lib/generic-linux-automator-exec/matrix-controller/staging-inbox/delulu_tech")
IDENT="delulu_homepage_v1"
OLD=BASE/IDENT
HOLD=BASE/(IDENT+"-layout-hold-20261024")
NEW=OLD/"site"
MANIFEST=BASE/(IDENT+".json")

def main():
    if not MANIFEST.is_file() or MANIFEST.is_symlink():
        raise RuntimeError("prepared_manifest_missing")
    manifest=json.loads(MANIFEST.read_text())
    if manifest.get("project")!="delulu_tech" or manifest.get("manifest")!=IDENT:
        raise RuntimeError("unrelated_manifest_denied")
    if HOLD.exists() or NEW.exists() or not (OLD/"index.html").is_file():
        raise RuntimeError("unexpected_existing_layout")
    for name,expected in manifest.get("files",{}).items():
        p=OLD/name
        if p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            raise RuntimeError("input_integrity_failure")
    OLD.rename(HOLD)
    try:
        OLD.mkdir(mode=0o700)
        HOLD.rename(NEW)
        sys.path.insert(0,str(BASE.parents[1]))
        try:
            from project_static_stage import validate_source
            _,_,audit=validate_source("delulu_tech",IDENT,BASE.parents[1])
        finally:
            sys.path.remove(str(BASE.parents[1]))
        print(json.dumps({"status":"layout_repaired","manifest":IDENT,"verified_files":sorted(audit)}))
    except BaseException:
        if NEW.exists():
            NEW.rename(HOLD)
        if OLD.is_dir() and not list(OLD.iterdir()):
            OLD.rmdir()
        if HOLD.exists():
            HOLD.rename(OLD)
        raise

if __name__=="__main__":
    main()
