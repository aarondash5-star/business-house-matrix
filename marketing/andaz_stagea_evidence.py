"""BHM Andaz Stage A: OFFLINE signed evidence contracts. Never imports live transport.
No new grants; no page requests; no publication capability.
"""
import base64
import datetime as dt
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

UTC = dt.timezone.utc
TOLERANCE = dt.timedelta(minutes=5)
KINDS = {"identity", "amenity", "checkout_rate"}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def timestamp(raw, now=None, max_age_days=7):
    try:
        v = dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        if v.tzinfo is None: raise ValueError()
        t = v.astimezone(UTC)
    except (ValueError, TypeError):
        raise ValueError("timezone_timestamp_required") from None
    now = now or dt.datetime.now(UTC)
    if t > now + TOLERANCE or now - t > dt.timedelta(days=max_age_days):
        raise ValueError("missing_or_stale_timestamp")
    return t

def signed_proof(body, public_key, context):
    if not isinstance(body, dict) or set(body) != {"payload", "signature"}:
        raise ValueError("malformed_signed_envelope")
    try:
        signature = base64.b64decode(body["signature"], validate=True)
        public = base64.b64decode(public_key, validate=True)
        Ed25519PublicKey.from_public_bytes(public).verify(
            signature, context.encode() + b"\n" + canonical(body["payload"]))
    except Exception:
        raise ValueError("signature_not_verified") from None
    return body["payload"]

def source_receipt(envelope, registry, now=None):
    payload = envelope.get("payload", {})
    issuer = payload.get("issuer")
    if issuer not in registry.get("extractors", {}):
        raise ValueError("untrusted_extractor")
    p = signed_proof(envelope, registry["extractors"][issuer], "BHM-SOURCE-v1")
    required = ("receipt_id", "issuer", "url", "entity_id", "sha256",
                "observed_utc", "excerpt")
    if any(not p.get(k) for k in required):
        raise ValueError("incomplete_source_receipt")
    spec = registry.get("sources", {}).get(p["url"])
    if not spec or spec.get("entity_id") != p["entity_id"]:
        raise ValueError("url_or_entity_not_granted")
    u = urlsplit(p["url"])
    if u.scheme != "https" or u.username or u.password or u.port not in (None,443):
        raise ValueError("invalid_source_url")
    if not re.fullmatch(r"[0-9a-f]{64}", str(p["sha256"])):
        raise ValueError("invalid_source_digest")
    if not isinstance(p["excerpt"], str) or not (10 <= len(p["excerpt"]) <= 800):
        raise ValueError("invalid_source_excerpt")
    timestamp(p["observed_utc"], now=now, max_age_days=14)
    if spec.get("role") not in ("first_party", "independent_ota"):
        raise ValueError("untrusted_source_role")
    if not spec.get("origin_id"):
        raise ValueError("missing_source_origin")
    return {**p, "origin_id":spec["origin_id"], "role":spec["role"]}

def verified_claim(claim, receipts, approval, registry, now=None):
    if claim.get("kind") not in KINDS or not claim.get("entity_id"):
        raise ValueError("invalid_claim")
    if claim["kind"] == "checkout_rate":
        raise ValueError("checkout_prices_require_separate_ota_review")
    if not isinstance(claim.get("quote_by_receipt"), dict):
        raise ValueError("direct_source_quotes_required")
    timestamp(claim.get("observed_utc"), now, 7)
    trusted = [source_receipt(x, registry, now) for x in receipts]
    ids = [x["receipt_id"] for x in trusted]
    if len(ids) < 2 or len(ids) != len(set(ids)):
        raise ValueError("two_distinct_receipts_required")
    if len({x["origin_id"] for x in trusted}) < 2:
        raise ValueError("independent_origins_required")
    if not any(x["role"] == "first_party" for x in trusted):
        raise ValueError("first_party_required")
    if set(ids) != set(claim["quote_by_receipt"]):
        raise ValueError("claim_receipt_mismatch")
    for src in trusted:
        quote = claim["quote_by_receipt"][src["receipt_id"]]
        if (src["entity_id"] != claim["entity_id"] or
                not isinstance(quote, str) or len(quote) < 6 or
                quote.casefold() not in src["excerpt"].casefold()):
            raise ValueError("claim_not_supported_by_source")
    if not isinstance(claim.get("value"), str) or not claim["value"].strip() or \
            claim["value"].casefold() not in " ".join(claim["quote_by_receipt"].values()).casefold():
        raise ValueError("claim_value_not_in_evidence")
    reviewer = approval.get("payload", {}).get("reviewer_id")
    person = registry.get("reviewers", {}).get(reviewer)
    if not person or person.get("role") != "human_qa" or not person.get("active"):
        raise ValueError("not_authorized_reviewer")
    decision = signed_proof(approval, person["public_key"], "BHM-REVIEW-v1")
    if (decision.get("reviewer_id") != reviewer or decision.get("decision") != "approve"
            or decision.get("claim_digest") != digest(claim)
            or set(decision.get("receipt_ids", [])) != set(ids)):
        raise ValueError("review_not_bound_to_claim_and_receipts")
    issued = timestamp(decision.get("issued_at"), now, 7)
    expires = timestamp(decision.get("expires_at"), now, 7)
    if not issued < expires or (now or dt.datetime.now(UTC)) >= expires:
        raise ValueError("review_expired")
    return {"status":"cryptographically_reviewed", "claim_digest":digest(claim),
            "reviewer_id":reviewer, "receipt_ids":ids, "publish_allowed":False,
            "qualification":"Key authentication is not a substitute for out-of-band human identity vetting."}

def money(value):
    try:
        v = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError("invalid_money") from None
    if not v.is_finite() or v < 0 or v.as_tuple().exponent < -2:
        raise ValueError("invalid_money")
    return v

def validate_checkout(quote, now=None):
    required = ("property_id","source_receipt_id","observed_utc","checkin","checkout",
                "product","adults","rooms","beds","ac","currency","base","tax",
                "fees","total","availability","checkout_stage","cancellation",
                "payment_terms","inclusions")
    if any(k not in quote for k in required):
        raise ValueError("incomplete_checkout")
    now = now or dt.datetime.now(UTC)
    timestamp(quote["observed_utc"], now, 1)
    try:
        checkin = dt.date.fromisoformat(quote["checkin"])
        checkout = dt.date.fromisoformat(quote["checkout"])
    except ValueError:
        raise ValueError("invalid_stay_dates") from None
    if checkin <= now.date() or checkout <= checkin or (checkout-checkin).days > 30:
        raise ValueError("invalid_future_stay")
    if quote["product"] == "dorm_bed":
        if (quote["adults"],quote["rooms"],quote["beds"]) != (1,0,1):
            raise ValueError("dorm_occupancy_mismatch")
    elif quote["product"] == "private_room":
        if (quote["adults"],quote["rooms"],quote["beds"]) != (2,1,0):
            raise ValueError("private_occupancy_mismatch")
    else:
        raise ValueError("invalid_room_category")
    if quote["ac"] not in ("ac","non_ac","unknown"):
        raise ValueError("invalid_ac")
    if quote["currency"] != "INR" or quote["availability"] != "available" or \
            quote["checkout_stage"] != "final_review_before_payment":
        raise ValueError("not_final_live_inr_quote")
    if not all(isinstance(quote[k],str) and quote[k].strip() for k in
               ("property_id","source_receipt_id","cancellation","payment_terms")):
        raise ValueError("missing_terms")
    if not isinstance(quote["inclusions"],list) or \
            not all(isinstance(v,str) and v.strip() for v in quote["inclusions"]):
        raise ValueError("invalid_inclusions")
    base,tax,fees,total = [money(quote[k]) for k in ("base","tax","fees","total")]
    if base+tax+fees != total:
        raise ValueError("non_reconciling_checkout_total")
    return {"status":"needs_review","quote_digest":digest(quote),
            "product":quote["product"],"checkin":quote["checkin"],
            "checkout":quote["checkout"],"currency":"INR","total":str(total),
            "nights":(checkout-checkin).days,"publish_allowed":False}

def comparable_quotes(quotes, now=None):
    validated = [validate_checkout(q,now) for q in quotes]
    if len({q["property_id"] for q in quotes}) < 5:
        raise ValueError("five_distinct_properties_required")
    for key in ("checkin","checkout","product","adults","rooms","beds","ac"):
        if len({q[key] for q in quotes}) != 1:
            raise ValueError("non_comparable_"+key)
    return {"status":"requires_independent_checkout_review", "count":len(validated),
            "checkin":quotes[0]["checkin"],"checkout":quotes[0]["checkout"],
            "publish_allowed":False}
