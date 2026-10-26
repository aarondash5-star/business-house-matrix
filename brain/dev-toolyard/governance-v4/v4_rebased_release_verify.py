"""V4 rebased source-bound DEV_BETA Ed25519 verifier. No signer and no host writes.

Release contract: canonical UTF-8 ASCII JSON + LF, detached RAW Ed25519
signature (NOT SSHSIG), independently root-owned Ed25519 SPKI public PEM.
The reviewed Git commit and root-owned owner trust must be enrolled separately.
"""
from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import stat

from v4_rebase_live_v12 import (
    CURRENT_LIVE_ADAPTER_SHA, CURRENT_LEDGER_SHA, CURRENT_GUARD_SHA,
    REBASED_ADAPTER_SHA, REBASED_ENFORCEMENT_SHA,
    REBASED_LEDGER_CANONICAL_SHA, REVIEWED_V4_GUARD_SHA,
)
from guided_dell_v4_install_preflight import EXPECTED_NAMES

HOST = "dell-linux"
PROJECT = "matrix_dev_manager"
RELEASE = "matrix_v4_controller_v14_rebased_v12_20261027"
KEY_ID = "DEV_BETA"
# There is deliberately no default signable commit. Independent GitHub
# review freezes an exact 40-character SHA in a root-owned release policy.
SIGNATURE_ALGORITHM = "Ed25519"
OWNER_PEM_FILE = "/etc/matrix-internal-release/dev_beta_owner_public.pem"
OWNER_PEM_SHA256 = "1eee3d266eb1d362b9c7f36d0301b831a8a527828682505ff286d2738606eec1"
SCOPE_KEYS = frozenset((
    "schema","key_id","algorithm","host","project","release","source_commit",
    "old_pins","new_pins","release_id","issued_utc","expires_utc",
    "nonce","production","spend","max_activations","qa_receipts",
))
OLD_PINS = dict(EXPECTED_NAMES)
NEW_PINS = {
    "yard_auto_adapter_v1.py": REBASED_ADAPTER_SHA,
    "adapter_guard_v4.py": REVIEWED_V4_GUARD_SHA,
    "yard_execution_guard_v13.py": REBASED_ENFORCEMENT_SHA,
    "yard_exec_bindings_v14.json": REBASED_LEDGER_CANONICAL_SHA,
}
_RELEASE = re.compile(r"^v4-controller-20261027-[a-f0-9]{24,48}$")
_HEX = re.compile(r"^[0-9a-f]{40}$")
_NONCE = re.compile(r"^[a-f0-9]{32,64}$")

class RebasedReleaseDenied(ValueError):
    pass

def canonical(obj:dict)->bytes:
    if type(obj) is not dict:
        raise RebasedReleaseDenied("payload_not_dict")
    return (json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\n").encode("ascii")

def read_private(path:Path, max_bytes:int)->bytes:
    p=Path(path)
    if p.is_symlink() or not p.is_file():
        raise RebasedReleaseDenied("missing_or_symlink")
    st=p.stat()
    if not 0<st.st_size<=max_bytes or st.st_mode & 0o022 or st.st_nlink!=1:
        raise RebasedReleaseDenied("file_unsafe")
    return p.read_bytes()

def owner_trust(pem:Path)->bytes:
    p=Path(pem)
    if p.is_symlink() or p.parent.is_symlink() or not p.is_file():
        raise RebasedReleaseDenied("owner_public_trust_missing")
    st=p.stat();dt=p.parent.stat()
    if st.st_uid!=0 or dt.st_uid!=0 or st.st_mode & 0o022 or dt.st_mode & 0o022 or st.st_nlink!=1:
        raise RebasedReleaseDenied("trust_not_independently_owned")
    data=read_private(p,1024)
    if not data.startswith(b"-----BEGIN PUBLIC KEY-----\n") or not data.endswith(b"-----END PUBLIC KEY-----\n"):
        raise RebasedReleaseDenied("trust_not_spki_pem")
    if sha256(data).hexdigest()!=OWNER_PEM_SHA256:
        raise RebasedReleaseDenied("owner_public_fingerprint_mismatch")
    return data

def parse_payload(encoded:bytes, reviewed_commit:str|None, now:datetime|None=None)->dict:
    if reviewed_commit is None or not _HEX.fullmatch(reviewed_commit):
        raise RebasedReleaseDenied("independent_review_commit_not_frozen")
    if not isinstance(encoded,bytes) or not 0<len(encoded)<=8192:
        raise RebasedReleaseDenied("invalid_payload_size")
    try:
        payload=json.loads(encoded)
    except (UnicodeDecodeError,ValueError,TypeError) as e:
        raise RebasedReleaseDenied("invalid_json") from e
    if type(payload) is not dict or set(payload)!=SCOPE_KEYS or canonical(payload)!=encoded:
        raise RebasedReleaseDenied("noncanonical_or_unexpected_fields")
    required={
        "schema":1,"key_id":KEY_ID,"algorithm":SIGNATURE_ALGORITHM,
        "host":HOST,"project":PROJECT,"release":RELEASE,
        "source_commit":reviewed_commit,"old_pins":OLD_PINS,
        "new_pins":NEW_PINS,"production":False,"spend":False,"max_activations":1,
    }
    for k,val in required.items():
        if type(payload[k]) is not type(val) or payload[k]!=val:
            raise RebasedReleaseDenied("release_scope_mismatch:"+k)
    if not isinstance(payload["release_id"],str) or not _RELEASE.fullmatch(payload["release_id"]):
        raise RebasedReleaseDenied("invalid_release_id")
    if not isinstance(payload["nonce"],str) or not _NONCE.fullmatch(payload["nonce"]):
        raise RebasedReleaseDenied("invalid_nonce")
    receipts=payload["qa_receipts"]
    if not isinstance(receipts,list) or not receipts or len(receipts)>8 or any(
        type(x) is not str or not re.fullmatch(r"[a-z0-9_.:-]{8,120}",x) for x in receipts
    ):
        raise RebasedReleaseDenied("qa_receipts_missing")
    try:
        issued=datetime.fromisoformat(payload["issued_utc"].replace("Z","+00:00"))
        expiry=datetime.fromisoformat(payload["expires_utc"].replace("Z","+00:00"))
    except (ValueError,TypeError,AttributeError) as e:
        raise RebasedReleaseDenied("invalid_dates") from e
    now=now or datetime.now(timezone.utc)
    if (issued.utcoffset()!=timedelta(0) or expiry.utcoffset()!=timedelta(0) or
        not (now-timedelta(minutes=5)<issued<=now+timedelta(seconds=30)) or
        not (now<expiry<=issued+timedelta(minutes=5))):
        raise RebasedReleaseDenied("release_expired_or_time_unbounded")
    return payload

def verify_detached(payload:bytes,signature_b64:str,public_pem:bytes)->bool:
    # Import only the public half; never access Supabase signing secrets.
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature
        k=load_pem_public_key(public_pem)
        if not isinstance(k,Ed25519PublicKey):
            raise RebasedReleaseDenied("not_ed25519_public_key")
        if not isinstance(signature_b64,str) or len(signature_b64)>100:
            raise RebasedReleaseDenied("invalid_signature_format")
        sig=base64.b64decode(signature_b64,validate=True)
        if len(sig)!=64:
            raise RebasedReleaseDenied("invalid_signature_length")
        try:
            k.verify(sig,payload)
        except InvalidSignature as e:
            raise RebasedReleaseDenied("signature_invalid") from e
        return True
    except RebasedReleaseDenied:
        raise
    except (ValueError,TypeError) as e:
        raise RebasedReleaseDenied("invalid_signature_encoding") from e

def verified_release(encoded:bytes,signature_b64:str,pem_path:Path,
                     reviewed_commit:str|None,now:datetime|None=None)->dict:
    payload=parse_payload(encoded,reviewed_commit,now)
    public_pem=owner_trust(pem_path)
    if verify_detached(encoded,signature_b64,public_pem) is not True:
        raise RebasedReleaseDenied("signature_not_verified")
    return {"state":"OWNER_SIGNATURE_VERIFIED","release_id":payload["release_id"],
            "host":HOST,"project":PROJECT,"payload_sha256":sha256(encoded).hexdigest(),
            "signer_key_id":KEY_ID,"production":False,"spend":False,
            "can_activate":False}  # activation is separately certified
