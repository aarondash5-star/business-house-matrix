"""Offline regression coverage for Stage A, no network or production access."""
import base64
import datetime as dt
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import andaz_stagea_evidence as a

NOW = dt.datetime(2026,10,23,0,0,tzinfo=dt.timezone.utc)
def iso(seconds=0):
    return (NOW+dt.timedelta(seconds=seconds)).isoformat()
def key():
    return Ed25519PrivateKey.generate()
def pub(private):
    return base64.b64encode(private.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)).decode()
def sign(p,private,context):
    return {"payload":p,"signature":base64.b64encode(
        private.sign(context.encode()+b"\n"+a.canonical(p))).decode()}

class StageAEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.r=key(); self.e=key()
        self.s1="https://property.example/rooms/"
        self.s2="https://ota.example/property/123"
        self.policy={
            "extractors":{"dell-paired":pub(self.e)},
            "reviewers":{"reviewer-01":{"public_key":pub(self.r),"role":"human_qa","active":True}},
            "sources":{
                self.s1:{"entity_id":"happy-panda","origin_id":"owner-1","role":"first_party"},
                self.s2:{"entity_id":"happy-panda","origin_id":"ota-1","role":"independent_ota"}
            }}
        self.p1={"receipt_id":"src-1","issuer":"dell-paired","url":self.s1,
                 "entity_id":"happy-panda","sha256":"a"*64,
                 "observed_utc":iso(-300),
                 "excerpt":"Happy Panda Hostel rooms with dorm beds near Arambol beach."}
        self.p2={"receipt_id":"src-2","issuer":"dell-paired","url":self.s2,
                 "entity_id":"happy-panda","sha256":"b"*64,
                 "observed_utc":iso(-300),
                 "excerpt":"Happy Panda Hostel rooms with dorm beds available."}
        self.claim={"kind":"identity","entity_id":"happy-panda",
                    "value":"Happy Panda Hostel","observed_utc":iso(-180),
                    "quote_by_receipt":{"src-1":"Happy Panda Hostel rooms",
                                        "src-2":"Happy Panda Hostel rooms"}}
    def receipts(self):
        return [sign(self.p1,self.e,"BHM-SOURCE-v1"),
                sign(self.p2,self.e,"BHM-SOURCE-v1")]
    def approval(self,claim=None,receipts=None):
        claim=claim or self.claim; receipts=receipts or self.receipts()
        payload={"reviewer_id":"reviewer-01","decision":"approve",
                 "claim_digest":a.digest(claim),
                 "receipt_ids":[x["payload"]["receipt_id"] for x in receipts],
                 "issued_at":iso(-30),"expires_at":iso(180)}
        return sign(payload,self.r,"BHM-REVIEW-v1")
    def test_signed_claim_passes_with_distinct_origins(self):
        out=a.verified_claim(self.claim,self.receipts(),self.approval(),self.policy,NOW)
        self.assertEqual(out["status"],"cryptographically_reviewed")
        self.assertFalse(out["publish_allowed"])
    def test_forged_source_signature_rejected(self):
        proofs=self.receipts(); proofs[0]["payload"]["excerpt"]="altered page"
        with self.assertRaisesRegex(ValueError,"signature_not_verified"):
            a.verified_claim(self.claim,proofs,self.approval(),self.policy,NOW)
    def test_untrusted_source_and_entity_rejected(self):
        p={**self.p1,"url":"https://not-granted.example/"}
        with self.assertRaisesRegex(ValueError,"url_or_entity_not_granted"):
            a.source_receipt(sign(p,self.e,"BHM-SOURCE-v1"),self.policy,NOW)
    def test_same_origin_rejected(self):
        self.policy["sources"][self.s2]["origin_id"]="owner-1"
        with self.assertRaisesRegex(ValueError,"independent_origins_required"):
            a.verified_claim(self.claim,self.receipts(),self.approval(),self.policy,NOW)
    def test_claim_quote_must_exist_in_both_snapshots(self):
        c={**self.claim,"quote_by_receipt":{"src-1":"Happy Panda Hostel rooms",
                                              "src-2":"imaginary 600% discount"}}
        with self.assertRaisesRegex(ValueError,"claim_not_supported_by_source"):
            a.verified_claim(c,self.receipts(),self.approval(c),self.policy,NOW)
    def test_review_not_bound_to_other_claim(self):
        c={**self.claim,"value":"Panda Hostel"}
        with self.assertRaisesRegex(ValueError,"review_not_bound"):
            a.verified_claim(c,self.receipts(),self.approval(),self.policy,NOW)
    def test_review_not_bound_to_other_receipts(self):
        ap=self.approval(); ap["payload"]["receipt_ids"]=["src-1","another"]
        with self.assertRaisesRegex(ValueError,"signature_not_verified"):
            a.verified_claim(self.claim,self.receipts(),ap,self.policy,NOW)
    def test_inactive_reviewer_rejected(self):
        self.policy["reviewers"]["reviewer-01"]["active"]=False
        with self.assertRaisesRegex(ValueError,"not_authorized_reviewer"):
            a.verified_claim(self.claim,self.receipts(),self.approval(),self.policy,NOW)
    def test_expired_review_rejected(self):
        data=self.approval()["payload"]; data["expires_at"]=iso(-1)
        with self.assertRaisesRegex(ValueError,"review_expired"):
            a.verified_claim(self.claim,self.receipts(),sign(data,self.r,"BHM-REVIEW-v1"),self.policy,NOW)
    def test_stale_snapshot_rejected(self):
        p={**self.p1,"observed_utc":iso(-15*86400)}
        with self.assertRaisesRegex(ValueError,"missing_or_stale_timestamp"):
            a.source_receipt(sign(p,self.e,"BHM-SOURCE-v1"),self.policy,NOW)

    def test_checkout_rate_cannot_bypass_review_via_generic_claim(self):
        c={**self.claim,"kind":"checkout_rate","value":"395.00"}
        with self.assertRaisesRegex(ValueError,"checkout_prices_require_separate_ota_review"):
            a.verified_claim(c,self.receipts(),self.approval(c),self.policy,NOW)
    def test_signed_false_value_without_quote_is_rejected(self):
        c={**self.claim,"value":"Invented property never stated"}
        with self.assertRaisesRegex(ValueError,"claim_value_not_in_evidence"):
            a.verified_claim(c,self.receipts(),self.approval(c),self.policy,NOW)

class CheckoutSchemaTests(unittest.TestCase):
    def quote(self,**updates):
        q={"property_id":"happy-panda","source_receipt_id":"src-11",
            "observed_utc":iso(-60),"checkin":"2026-11-06","checkout":"2026-11-07",
            "product":"dorm_bed","adults":1,"rooms":0,"beds":1,"ac":"non_ac",
            "currency":"INR","base":"350.00","tax":"35.00","fees":"10.00",
            "total":"395.00","availability":"available",
            "checkout_stage":"final_review_before_payment",
            "cancellation":"Nonrefundable","payment_terms":"Pay at property",
            "inclusions":["one bed","wifi"]}
        q.update(updates)
        return q
    def test_valid_quote_is_not_certified(self):
        self.assertEqual(a.validate_checkout(self.quote(),NOW)["status"],"needs_review")
    def test_missing_checkout_component_rejected(self):
        q=self.quote(); q.pop("tax")
        with self.assertRaisesRegex(ValueError,"incomplete_checkout"):
            a.validate_checkout(q,NOW)
    def test_wrong_total_rejected(self):
        with self.assertRaisesRegex(ValueError,"non_reconciling"):
            a.validate_checkout(self.quote(total="400.00"),NOW)
    def test_not_live_quote_rejected(self):
        with self.assertRaisesRegex(ValueError,"not_final_live"):
            a.validate_checkout(self.quote(checkout_stage="search_result"),NOW)
    def test_stale_observation_rejected(self):
        with self.assertRaisesRegex(ValueError,"missing_or_stale"):
            a.validate_checkout(self.quote(observed_utc=iso(-2*86400)),NOW)
    def test_wrong_occupancy_rejected(self):
        with self.assertRaisesRegex(ValueError,"dorm_occupancy_mismatch"):
            a.validate_checkout(self.quote(adults=2),NOW)
    def test_private_room_separate_product_passes(self):
        q=self.quote(product="private_room",adults=2,rooms=1,beds=0,ac="ac")
        self.assertEqual(a.validate_checkout(q,NOW)["product"],"private_room")
    def test_past_stay_rejected(self):
        with self.assertRaisesRegex(ValueError,"invalid_future_stay"):
            a.validate_checkout(self.quote(checkin="2026-10-20"),NOW)
    def test_non_inr_and_nan_rejected(self):
        with self.assertRaisesRegex(ValueError,"not_final_live"):
            a.validate_checkout(self.quote(currency="EUR"),NOW)
        with self.assertRaisesRegex(ValueError,"invalid_money"):
            a.validate_checkout(self.quote(base="NaN"),NOW)
    def test_five_distinct_comparable_properties(self):
        qs=[self.quote(property_id="hotel-"+str(i)) for i in range(5)]
        self.assertEqual(a.comparable_quotes(qs,NOW)["count"],5)
        qs[2]["ac"]="ac"
        with self.assertRaisesRegex(ValueError,"non_comparable_ac"):
            a.comparable_quotes(qs,NOW)
    def test_duplicate_properties_rejected(self):
        with self.assertRaisesRegex(ValueError,"five_distinct_properties_required"):
            a.comparable_quotes([self.quote() for _ in range(5)],NOW)

if __name__=="__main__": unittest.main()
