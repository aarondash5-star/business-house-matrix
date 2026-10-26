"""Source-only security contracts for the owner public-key verification portal."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
PAGE=ROOT/"owner_release_portal"/"confirm"/"index.html"
JS=ROOT/"owner_release_portal"/"confirm"/"app.js"
TEMPLATE=ROOT.parents[2]/"docs"/"fixtures"/"MATRIX_V4_OWNER_EMAIL_TEMPLATE_REVIEW_ONLY.html"

class OwnerPortalSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=PAGE.read_text(encoding="utf-8")
        cls.js=JS.read_text(encoding="utf-8")
        cls.email=TEMPLATE.read_text(encoding="utf-8")

    def test_static_page_content_security_policy(self):
        for token in ("default-src 'none'", "script-src 'self'", "connect-src https://saczglesalubroyaucqe.supabase.co",
                      'meta name="referrer" content="no-referrer"'):
            self.assertIn(token,self.html)

    def test_uses_publishable_not_privileged_key(self):
        self.assertIn("sb_publishable_",self.js)
        for token in ("service_role", "SUPABASE_SERVICE_ROLE_KEY", "DEV_BETA_ED25519_PRIVATE_PKCS8_B64",
                      "MATRIX_V4_OWNER_UID", "MATRIX_V4_OWNER_EMAIL"):
            self.assertNotIn(token,self.js)
        self.assertNotIn("karanbizweb360@gmail.com",self.js.lower())
        self.assertNotIn("karanbizweb360@gmail.com",self.html.lower())

    def test_otp_and_manual_link_choices(self):
        for token in ('/auth/v1/otp', '/auth/v1/verify', 'create_user:false',
                      'confirmLink', 'token_hash', 'type:"email"'):
            self.assertIn(token,self.js)
        self.assertIn('window.location.search',self.js)
        self.assertIn('addEventListener("click"',self.js)

    def test_tokens_not_persisted_or_logged(self):
        for token in ("localStorage", "sessionStorage", "console.log", "console.info",
                      "alert(", "window.opener", "window.name"):
            self.assertNotIn(token,self.js)
        self.assertIn("history.replaceState",self.js)
        self.assertIn('let jwt=""',self.js)

    def test_only_public_attestation_not_sign_or_deploy(self):
        self.assertIn("/matrix-devbeta-public-attest/derive-public",self.js)
        self.assertIn('el("derive").disabled=false',self.js)
        for path in ("/sign-release", "/activate", "/root", "/ssh/", "/matrix-v4-owner-approval"):
            self.assertNotIn(path,self.js)

    def test_live_owner_session_verified_before_unlock(self):
        self.assertIn("/matrix-devbeta-public-attest/owner-session",self.js)
        self.assertIn('r.json.state!=="VERIFIED_EXISTING_OWNER"',self.js)
        self.assertIn('jwt="";el("derive").disabled=true',self.js)
        self.assertIn('el("reviewPanel").hidden=false',self.js)

    def test_feedback_is_ui_only_never_release_approval(self):
        self.assertIn("/matrix-devbeta-public-attest/review",self.js)
        self.assertIn('UI_REVIEW_RECORDED',self.js)
        self.assertIn('id="uiAccept"',self.html)
        self.assertIn('id="uiNeeds"',self.html)
        self.assertIn("This is a UI review only",self.html)
        self.assertNotIn("/matrix-v4-owner-approval",self.js)

    def test_email_fixture_not_live_and_both_methods(self):
        for part in ("{{ .Token }}", "{{ .TokenHash }}", "{{ .RedirectTo }}",
                     "DO NOT DEPLOY", "click"):
            self.assertIn(part,self.email)

    def test_not_confused_with_real_release_approval(self):
        self.assertIn("This page cannot sign a release",self.html)
        self.assertNotIn("OWNER_RELEASE_SIGNED",self.html)

if __name__=="__main__":
    unittest.main()
