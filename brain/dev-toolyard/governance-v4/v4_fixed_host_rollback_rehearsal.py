"""Fixed-purpose Dell V4 replacement *rehearsal*. Real filesystem, temp sandbox only.

No live controller access, sudo, SSH, systemd, authentication, or dynamic shell.
The future host runner must add independent owner signature, source review,
queue freeze, privilege split, watchdog, service restart and tested rollback
BEFORE it may be enabled on real Dell. Never use these tests as live evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

ORIGINAL=("yard_auto_adapter_v1.py","yard_execution_guard_v13.py","yard_exec_bindings_v13.json")
CANDIDATE=("yard_auto_adapter_v1.py","adapter_guard_v4.py",
           "yard_exec_bindings_v14.json","yard_execution_guard_v13.py")
PROTECTED=Path("/var/lib/generic-linux-automator-exec/matrix-controller")

class RehearsalDenied(ValueError):pass

def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def check_file(p:Path,expected_hash:str)->bytes:
    if p.is_symlink() or not p.is_file():
        raise RehearsalDenied("missing_or_symlink")
    s=p.stat()
    if s.st_nlink!=1 or s.st_mode & 0o022 or not 0<s.st_size<2_000_000:
        raise RehearsalDenied("file_metadata_denied")
    b=p.read_bytes()
    if digest(b)!=expected_hash:
        raise RehearsalDenied("file_sha_drift")
    return b

def ensure_sandbox(target:Path,staged:Path,backup:Path)->None:
    root=Path(tempfile.gettempdir()).resolve(strict=True)
    dirs=[target,staged,backup]
    for p in dirs:
        if p.is_symlink() or not p.is_dir():
            raise RehearsalDenied("directory_missing_or_symlink")
        resolved=p.resolve(strict=True)
        if not resolved.is_relative_to(root) or resolved.is_relative_to(PROTECTED):
            raise RehearsalDenied("protected_host_path_denied")
        for item in p.parents:
            if item==root:break
            if item.is_symlink():raise RehearsalDenied("ancestor_symlink")
    if len(set(str(p.resolve()) for p in dirs))!=3:
        raise RehearsalDenied("overlapping_directories")

def write_atomic(dest:Path,data:bytes)->None:
    if dest.exists() and (dest.is_symlink() or not dest.is_file()):
        raise RehearsalDenied("replacement_path_unsafe")
    tmp=dest.with_suffix(dest.suffix+".new")
    if tmp.exists() or tmp.is_symlink():
        raise RehearsalDenied("preexisting_staging_collision")
    flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW
    fd=os.open(tmp,flags,0o600)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,dest)
    finally:
        if tmp.exists():tmp.unlink()

@dataclass(frozen=True)
class RehearsalResult:
    status:str
    applied:tuple[str,...]
    backups_verified:bool
    restored_verified:bool
    live_controller_touched:bool=False
    systemd_touched:bool=False
    authenticated_release:bool=False

def rehearse(target:Path,staged:Path,backup:Path,old_pins:dict,new_pins:dict,
             fault_after:int|None=None)->RehearsalResult:
    """Write ONLY under verified tmp sandbox. No CLI entry point for live service."""
    if set(old_pins)!=set(ORIGINAL) or set(new_pins)!=set(CANDIDATE):
        raise RehearsalDenied("unexpected_manifest_paths")
    if fault_after is not None and (type(fault_after) is not int or
                                    not 0<=fault_after<=len(CANDIDATE)):
        raise RehearsalDenied("invalid_injected_fault")
    ensure_sandbox(target,staged,backup)
    originals={name:check_file(target/name,old_pins[name]) for name in ORIGINAL}
    future={name:check_file(staged/name,new_pins[name]) for name in CANDIDATE}
    # Backups taken and read back BEFORE first staged file replacement.
    if list(backup.iterdir()):
        raise RehearsalDenied("backup_dir_must_be_empty")
    applied=[]
    lock=backup/"exclusive-rehearsal.lock"
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        for name,src in originals.items():
            write_atomic(backup/name,src)
            check_file(backup/name,old_pins[name])
        try:
            if fault_after==0:raise OSError("fault_before_first_write")
            for step,name in enumerate(CANDIDATE,1):
                write_atomic(target/name,future[name])
                applied.append(name)
                check_file(target/name,new_pins[name])
                if fault_after==step:raise OSError("fault_after_step")
            for name in CANDIDATE:check_file(target/name,new_pins[name])
            return RehearsalResult("TEMP_FILES_REPLACED",tuple(applied),True,False)
        except (OSError,RehearsalDenied):
            # Fail shut: restore original files and remove candidate-only additions.
            for name in CANDIDATE:
                if name not in ORIGINAL:
                    f=target/name
                    if f.exists() and not f.is_symlink():f.unlink()
            for name in ORIGINAL:
                write_atomic(target/name,originals[name])
                check_file(target/name,old_pins[name])
            return RehearsalResult("TEMP_FILES_RESTORED",tuple(applied),True,True)
    finally:
        os.close(fd)
