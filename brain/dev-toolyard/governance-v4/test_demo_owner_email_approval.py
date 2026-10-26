"""Source-only safety check for the offline owner email-approval demonstration."""
from pathlib import Path
import unittest

DEMO=Path(__file__).with_name("demo_owner_email_approval.html")

class DemoSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=DEMO.read_text("utf-8")

    def test_explicitly_non_live(self):
        for phrase in ("DEMO ONLY", "No real email is sent", "RELEASE NOT SIGNED", "DELL NOT DEPLOYED"):
            self.assertIn(phrase,self.source)

    def test_both_approval_paths(self):
        for fragment in ('id="verify"', 'id="link"', 'finish("mock email link")',
                         'finish("mock one-time code")','state.consumed=true'):
            self.assertIn(fragment,self.source)

    def test_bounded_challenge(self):
        for fragment in ('Date.now()+300000','state.attempts>5','remaining===0',
                         'state.consumed', 'crypto.getRandomValues'):
            self.assertIn(fragment,self.source)

    def test_no_live_email_or_backend_calls(self):
        for bad in ("fetch(", "supabase.auth", "service_role", "signInWithOtp(", "verifyOtp(",
                    "sudo ", "ssh ", "window.location=", "<form action="):
            self.assertNotIn(bad, self.source)

    def test_host_boundary(self):
        self.assertIn("dell-linux",self.source)
        self.assertIn("matrix_dev_manager",self.source)
        self.assertIn("Mac is separately gated",self.source)

if __name__ == "__main__":
    unittest.main()
