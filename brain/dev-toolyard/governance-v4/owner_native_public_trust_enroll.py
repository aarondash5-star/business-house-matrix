"""Dell DEV_BETA public-key trust installer. Independent owner-native terminal ONLY.

Never run this installer from the non-root Dev Yard / Generic SSH worker.
No controller deployment, no source promotion, no signature issuance.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

EXPECTED_PEM_SHA256="1eee3d266eb1d362b9c7f36d0301b831a8a527828682505ff286d2738606eec1"
TRUST_PATH=Path("/etc/matrix-internal-release/dev_beta_owner_public.pem")

class TrustEnrollmentDenied(ValueError):
    pass

def validate_public_pem(pem:bytes)->str:
    if not isinstance(pem,bytes) or len(pem)>512:
        raise TrustEnrollmentDenied("pem_too_large_or_wrong_type")
    if not re.fullmatch(rb"-----BEGIN PUBLIC KEY-----\n[A-Za-z0-9+/]{59}=\n-----END PUBLIC KEY-----\n",pem):
        raise TrustEnrollmentDenied("not_canonical_lf_public_pem")
    from cryptography.hazmat.primitives.serialization import (
        load_pem_public_key, Encoding, PublicFormat
    )
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    try:
        pub=load_pem_public_key(pem)
    except ValueError as exc:
        raise TrustEnrollmentDenied("invalid_public_der") from exc
    if not isinstance(pub,Ed25519PublicKey) or pub.public_bytes(Encoding.PEM,PublicFormat.SubjectPublicKeyInfo)!=pem:
        raise TrustEnrollmentDenied("not_canonical_ed25519_spki")
    digest=hashlib.sha256(pem).hexdigest()
    if digest!=EXPECTED_PEM_SHA256:
        raise TrustEnrollmentDenied("public_key_fingerprint_mismatch")
    return digest

def enroll_from_verified_stdin(pem:bytes, target:Path=TRUST_PATH)->str:
    """Root-only; exact fixed trust path. No root control via tool-yard."""
    if target!=TRUST_PATH:
        raise TrustEnrollmentDenied("target_override_denied")
    if os.geteuid()!=0:
        raise TrustEnrollmentDenied("independent_admin_root_required")
    validate_public_pem(pem)
    parent=target.parent
    if parent.is_symlink():
        raise TrustEnrollmentDenied("trust_dir_symlink_denied")
    if not parent.exists():
        # /etc is already root-owned; no worker-owned paths involved.
        if not parent.parent.is_dir() or parent.parent.stat().st_uid!=0:
            raise TrustEnrollmentDenied("parent_not_root_controlled")
        parent.mkdir(mode=0o755)
    st=parent.stat()
    if not parent.is_dir() or st.st_uid!=0 or st.st_mode & 0o022:
        raise TrustEnrollmentDenied("trust_dir_not_root_owned")
    if target.exists() or target.is_symlink():
        if target.is_symlink() or not target.is_file():
            raise TrustEnrollmentDenied("trust_target_symlink_or_device")
        old=target.stat()
        if old.st_uid!=0 or old.st_nlink!=1 or old.st_mode & 0o022:
            raise TrustEnrollmentDenied("trust_target_permissions")
        if target.read_bytes()!=pem:
            raise TrustEnrollmentDenied("existing_trust_differs")
        return "EXISTING_ROOT_TRUST_MATCHES"
    fd,path=tempfile.mkstemp(dir=parent,prefix=".dev-beta-pub-stage-")
    try:
        os.fchmod(fd,0o644)
        with os.fdopen(fd,"wb") as f:
            f.write(pem);f.flush();os.fsync(f.fileno())
        os.replace(path,target)
        dirfd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(dirfd)
        finally:os.close(dirfd)
    finally:
        if os.path.exists(path):os.unlink(path)
    st=target.stat()
    if st.st_uid!=0 or st.st_mode & 0o022 or target.read_bytes()!=pem:
        raise TrustEnrollmentDenied("readback_failed")
    return "ROOT_PUBLIC_TRUST_ENROLLED_ONLY"

def main(argv:list[str]|None=None)->int:
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("action",choices=["validate","enroll"])
    args=a.parse_args(argv)
    if args.action=="enroll" and os.geteuid()!=0:
        print("DENIED: independent native root terminal required",file=sys.stderr)
        return 2
    data=sys.stdin.buffer.read(513)
    try:
        result=enroll_from_verified_stdin(data) if args.action=="enroll" else validate_public_pem(data)
    except TrustEnrollmentDenied as exc:
        print("DENIED: "+str(exc),file=sys.stderr)
        return 2
    print(result)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
