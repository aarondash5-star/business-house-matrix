#!/usr/bin/env python3
"""Offline acceptance for the standalone reviewed-patch runner."""
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

SRC=Path(__file__).resolve().parents[1]/"reviewed_patch_runner.py"
spec=importlib.util.spec_from_file_location("reviewed_patch_runner",SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# The GitHub-hosted runner denies the network namespace used by our actual
# rootless Bubblewrap acceptance tests. Do not simulate a sandbox or report
# these tests as passed on that host: mark as SKIPPED and require the separate
# enrolled Dell 5/5 host receipts before any sandbox certification.
@unittest.skipIf(os.environ.get("GITHUB_ACTIONS") == "true",
                 "Requires enrolled Dell rootless Bubblewrap namespace; GitHub runner prohibits RTM_NEWADDR")
class SecuredExecutorTest(unittest.TestCase):
    def test_negative_host_and_network(self):
        result=mod.check("pine_mcp_chat")
        self.assertTrue(result["passed"],result)
        self.assertTrue(result["detail"]["private_hidden"])
        self.assertTrue(result["detail"]["net_blocked"])

    def test_cross_project_denied(self):
        with self.assertRaisesRegex(ValueError,"not_enrolled"):
            mod.workspace("pine_private")
        with self.assertRaisesRegex(ValueError,"not_enrolled"):
            mod.isolated("ashwakaal","probe")

    def test_traversal_rejected(self):
        with self.assertRaisesRegex(RuntimeError,"outside_allowlist"):
            mod.isolated("pine_mcp_chat","apply",{"files":[{"path":"../private.txt","content":"bad"}]})

    def test_absolute_and_dotfile_rejected(self):
        for name in ("/etc/passwd","frontend/.ssh/key","backend/../../etc/test"):
            with self.subTest(name=name):
                with self.assertRaises(RuntimeError):
                    mod.isolated("pine_mcp_chat","apply",{"files":[{"path":name,"content":"bad"}]})

    def test_synthetic_write_and_qa(self):
        path="frontend/qa-sandbox-fixture.html"
        workspace=mod.workspace("pine_mcp_chat")
        payload={"files":[{"path":path,"content":"<main>Mock Pine Chat</main>"}]}
        present=workspace/path
        if present.exists():
            payload["files"][0]["expected_sha256"]=hashlib.sha256(present.read_bytes()).hexdigest()
        out=mod.isolated("pine_mcp_chat","apply",payload)
        self.assertEqual(len(out["written"]),1)
        # Cannot overwrite an existing path without matching expected SHA.
        with self.assertRaisesRegex(RuntimeError,"stale_or_unapproved_overwrite"):
            mod.isolated("pine_mcp_chat","apply",{"files":[{"path":path,"content":"changed"}]})
        self.assertEqual(present.read_text(),"<main>Mock Pine Chat</main>")
        with self.assertRaisesRegex(RuntimeError,"stale_or_unapproved_overwrite"):
            mod.isolated("pine_mcp_chat","apply",{"files":[{"path":path,"content":"evil","expected_sha256":"0"*64}]})
        self.assertEqual(present.read_text(),"<main>Mock Pine Chat</main>")
        tests=workspace/"tests"/"test_secure_fixture.py"
        t="import unittest\nfrom pathlib import Path\nclass Smoke(unittest.TestCase):\n def test_fixture(self): self.assertTrue(Path('frontend/qa-sandbox-fixture.html').is_file())\n"
        contents={"files":[{"path":"tests/test_secure_fixture.py","content":t}]}
        if tests.exists():
            contents["files"][0]["expected_sha256"]=hashlib.sha256(tests.read_bytes()).hexdigest()
        mod.isolated("pine_mcp_chat","apply",contents)
        self.assertTrue(mod.isolated("pine_mcp_chat","test")["passed"])

if __name__=="__main__":
    unittest.main()
