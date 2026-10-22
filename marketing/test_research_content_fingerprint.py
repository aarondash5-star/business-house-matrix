#!/usr/bin/env python3
"""Fingerprint regression: transient markup must not trigger market alerts."""
import unittest
import research_engine as e

class ContentFingerprint(unittest.TestCase):
    def html(self,nonce):
        return ("""<html><head><title>Hidden Oak Pricing</title>
        <script>window.sessionNonce='"""+nonce+"""';</script></head>
        <body><main><article><h1>Traditional banya and sauna pricing</h1>
        <p>Regular three-hour wood fired sauna, steam room and rest area with tea.
        The exact session includes sauna and shower. Cold plunge is offered
        as part of a separately priced contrast therapy booking.</p>
        <p>Book sessions through the official public booking page only.</p>
        </article></main></body></html>""").encode()
    def test_transient_script_changes_do_not_count_as_content_change(self):
        x=e.extract_html(self.html("one"),"https://thehiddenoak.space/pricing/",{"thehiddenoak.space"})
        y=e.extract_html(self.html("two"),"https://thehiddenoak.space/pricing/",{"thehiddenoak.space"})
        self.assertEqual(x["status"],"needs_review")
        self.assertEqual(x["sha256"],y["sha256"])
        self.assertNotEqual(x["raw_html_sha256"],y["raw_html_sha256"])
        self.assertEqual(x["digest_basis"],"normalized_reader_content_v2")
    def test_visible_change_does_count(self):
        original=self.html("same")
        modified=original.replace(b"three-hour",b"two-hour")
        x=e.extract_html(original,"https://thehiddenoak.space/pricing/",{"thehiddenoak.space"})
        y=e.extract_html(modified,"https://thehiddenoak.space/pricing/",{"thehiddenoak.space"})
        self.assertNotEqual(x["sha256"],y["sha256"])
if __name__=="__main__":unittest.main()
