"""Independent acceptance gate for the Andaz pure-static Stage 1 output.

This file is staged outside all model-editable directories. Zero calls to WP,
StayCore or the public website. No made-up prices or booking confirmations.
"""
import pathlib
import re
import unittest
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOME = ROOT / "site" / "index.html"

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.links=[]
        self.scripts=[]
        self.forms=[]
        self.labels=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag=="script" and "src" in a:
            self.scripts.append(a["src"])
        if tag=="form":
            self.forms.append(a)
        if tag=="label" and "for" in a:
            self.labels.append(a["for"])

class StaticAndaz(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=HOME.read_text(encoding="utf8")
        cls.dom=Markup()
        cls.dom.feed(cls.html)
    def test_real_static_document(self):
        self.assertIn("<!doctype html",self.html.lower())
        self.assertNotIn("<?php",self.html)
        self.assertNotIn("wp_head(",self.html)
        self.assertNotIn("wp_footer(",self.html)
        self.assertLess(len(self.html.encode()),200000)
    def test_brand_and_experiences(self):
        lower=self.html.lower()
        for term in ("andaz vibe stay","arambol","stay","connect","play","reset","moksha"):
            self.assertIn(term,lower)
    def test_marketing_and_booking_sections(self):
        self.assertEqual(len(self.dom.ids),len(set(self.dom.ids)))
        for id_ in ("stay","connect","reset","location","booking","bookingForm",
                    "checkin","checkout","guests","stayType","bookingStatus"):
            self.assertIn(id_,self.dom.ids)
    def test_accessible_booking_form(self):
        self.assertTrue(self.dom.forms)
        for id_ in ("checkin","checkout","guests","stayType"):
            self.assertIn(id_,self.dom.labels)
        self.assertRegex(self.html,r'role=["\']status["\']|aria-live=["\']polite["\']')
    def test_no_unverified_ratings_or_checkout(self):
        self.assertNotIn('"aggregateRating"',self.html)
        self.assertNotRegex(self.html,r'(?i)fake|dummy price|guaranteed booking|instant confirmed')
        self.assertNotIn("/staycore/v1/reservations",self.html)
        self.assertNotIn("/wp-admin",self.html)
    def test_external_booking_logic_isolated(self):
        self.assertTrue(any("booking" in s and s.endswith(".js") for s in self.dom.scripts))
        scripts=[]
        for script in self.dom.scripts:
            if script.startswith("https://") or script.startswith("//"):
                continue
            scripts.append((HOME.parent/script).resolve())
        for p in scripts:
            self.assertTrue(p.is_relative_to(ROOT.resolve()))
            self.assertTrue(p.is_file(),f"Missing script {p}")
        logic="\n".join(p.read_text() for p in scripts if p.is_file())
        self.assertIn("checkin",logic.lower())
        self.assertIn("checkout",logic.lower())
        self.assertRegex(logic.lower(),r"unavailable|enquiry|enquire|not confirmed")
        self.assertNotRegex(logic,r"(?i)staff[_ -]?token|woocommerce_payment_complete")
    def test_mobile_accessibility(self):
        self.assertRegex(self.html,r'name=["\']viewport["\']')
        self.assertRegex(self.html,r'@media|stylesheet')
        self.assertIn("href=\"#booking\"",self.html)
    def test_source_remains_independent(self):
        original=(ROOT/"index.html").read_text()
        self.assertIn("Andaz",original)
        self.assertNotIn("<?php",original)

if __name__=="__main__":
    unittest.main()
