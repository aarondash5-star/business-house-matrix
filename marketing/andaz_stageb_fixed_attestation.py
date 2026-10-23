"""BHM Stage B: verify a fixed-shape Mac preflight attestation OFFLINE.

This is a schema and signature verifier for an eventual reviewed fixed-function
connector action. It DOES NOT contact any worker, execute commands, enroll
identities, change an allowlist, or authorize any extraction.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import re
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

CONTEXT = b"BHM-MAC-STAGEB-PREFLIGHT-v1\n"
HOST_ID = "mac-linux"
REQUIRED_UNITS = frozenset({"bhm-marketing-queue-worker.timer"})
REQUIRED_ARTIFACTS = frozenset({
    "marketing_report_orchestrator.py",
    "searxng_research.py",
    "matrix-research-transport/transport.py",
})
EXPECTED_KEYS = frozenset({
    "schema", "host_id", "observed_utc", "units", "artifacts",
    "extract_gate_active", "publish_enabled", "spend_enabled", "preflight_nonce",
})
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
UTC = dt.timezone.utc

def canonical(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def verify(attestation: dict, pinned_public_key_b64: str, *, expected_nonce: str,
           now: dt.datetime | None = None) -> dict:
    """Verify trust and fixed shape. This never authorizes page extraction.

    The pinned key must come from an independently approved identity registry.
    Never trust a key embedded in the received attestation.
    """
    now = now or dt.datetime.now(UTC)
    if now.tzinfo is None:
        raise ValueError("timezone_required")
    if not isinstance(attestation, dict) or set(attestation) != {"payload", "signature"}:
        raise ValueError("bad_attestation_envelope")
    payload = attestation["payload"]
    if not isinstance(payload, dict) or set(payload) != EXPECTED_KEYS:
        raise ValueError("bad_attestation_schema")
    if payload["schema"] != "bhm.mac.fixed_preflight.v1" or payload["host_id"] != HOST_ID:
        raise ValueError("wrong_host_or_schema")
    if payload["preflight_nonce"] != expected_nonce or not re.fullmatch(r"[A-Za-z0-9_-]{24,64}", expected_nonce):
        raise ValueError("nonce_not_bound")
    try:
        issued = dt.datetime.fromisoformat(payload["observed_utc"].replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        raise ValueError("bad_timestamp") from None
    if issued.tzinfo is None or not dt.timedelta(0) <= now.astimezone(UTC) - issued.astimezone(UTC) <= dt.timedelta(minutes=5):
        raise ValueError("expired_or_future_attestation")
    if payload["units"] != {name: "active" for name in REQUIRED_UNITS}:
        raise ValueError("required_unit_not_active")
    artifacts = payload["artifacts"]
    if not isinstance(artifacts, dict) or set(artifacts) != REQUIRED_ARTIFACTS:
        raise ValueError("unexpected_artifact_labels")
    if any(not isinstance(v, str) or HEX64.fullmatch(v) is None for v in artifacts.values()):
        raise ValueError("invalid_artifact_digest")
    if payload["extract_gate_active"] is not False:
        raise ValueError("extraction_already_active")
    if payload["publish_enabled"] is not False or payload["spend_enabled"] is not False:
        raise ValueError("unsafe_marketing_flags")
    try:
        key = Ed25519PublicKey.from_public_bytes(base64.b64decode(pinned_public_key_b64, validate=True))
        signature = base64.b64decode(attestation["signature"], validate=True)
        key.verify(signature, CONTEXT + canonical(payload))
    except Exception:
        raise ValueError("attestation_signature_invalid") from None
    return {
        "verified_transport_identity": True,
        "host_id": HOST_ID,
        "observed_utc": payload["observed_utc"],
        "artifact_sha256": dict(artifacts),
        "status": "preflight_evidence_only",
        "stage_b_certified": False,
        "source_permissions_granted": False,
        "extract_allowed": False,
        "publish_allowed": False,
        "reason": "Robots/terms, live transport fingerprints and real reviewer enrollment require independent approval",
    }
