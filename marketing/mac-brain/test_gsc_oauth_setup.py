#!/usr/bin/env python3
"""Offline regression: no real Google authentication or token files accessed."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import gsc_oauth_setup as oauth
import gsc_metrics


class OAuthSetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="bhm-gsc-oauth-")
        d = Path(self.tmp.name)
        self.token = patch.object(oauth, "TOKEN_FILE", d / "enrollment.json")
        self.sec = patch.object(gsc_metrics, "SECRETS", d / "gsc-readonly.json")
        self.token.start(); self.sec.start()

    def tearDown(self):
        self.token.stop(); self.sec.stop(); self.tmp.cleanup()

    def sample(self):
        return json.dumps({
            "installed": {"client_id": "public-id.apps.googleusercontent.com",
                          "client_secret": "google-secret-placeholder",
                          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                          "token_uri": "https://oauth2.googleapis.com/token",
                          "redirect_uris": ["http://localhost"]}
        }).encode()

    def test_desktop_client_only(self):
        parsed = oauth.valid_client(self.sample())
        self.assertTrue(parsed["client_id"].endswith(".apps.googleusercontent.com"))
        with self.assertRaises(ValueError):
            oauth.valid_client(json.dumps({"web": json.loads(self.sample())["installed"]}).encode())
        with self.assertRaises(ValueError):
            oauth.valid_client(json.dumps({"installed": {
                **json.loads(self.sample())["installed"], "token_uri": "https://evil.invalid/token"}}).encode())

    def test_ephemeral_local_setup_link_and_fail_closed_repeat(self):
        link = oauth.issue()
        self.assertTrue(link.startswith(f"http://{oauth.HOST}:{oauth.PORT}/setup/"))
        self.assertEqual(oauth.TOKEN_FILE.stat().st_mode & 0o077, 0)
        with self.assertRaises(RuntimeError):
            oauth.issue()

    def test_no_auth_grant_prevents_api(self):
        with self.assertRaises(RuntimeError):
            gsc_metrics.fetch_api("2026-09-01", "2026-09-28")

    def test_existing_access_not_overwritten(self):
        gsc_metrics.SECRETS.write_text("existing", encoding="utf8")
        with self.assertRaises(RuntimeError):
            oauth.issue()

    def test_invalid_form_rejected(self):
        with self.assertRaises(ValueError):
            oauth.parse_form_upload("application/json", self.sample())


if __name__ == "__main__":
    unittest.main(verbosity=2)
