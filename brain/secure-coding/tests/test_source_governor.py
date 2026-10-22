"""Independent stdlib tests for A1 fail-closed source governance."""
import copy
import importlib.util
from pathlib import Path
import unittest

SRC = Path(__file__).resolve().parents[1] / "source_governor.py"
spec = importlib.util.spec_from_file_location("source_governor", SRC)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

HTML = '<!doctype html><html lang="en"><meta name="viewport" content="width=device-width"><main><h1>Pine Chat</h1></main></html>'
TEST = 'import unittest\nfrom pathlib import Path\nclass UI(unittest.TestCase):\n def test_pine(self): self.assertIn("Pine", Path("frontend/pine-chat-a11y.html").read_text())\n'

def fixture():
    return {
        "project": gate.PROJECT, "manifest": gate.MANIFEST,
        "work_id": gate.WORK_ID, "repository": gate.REPOSITORY,
        "base_branch": gate.BASE_BRANCH,
        "files": [
            {"path": "frontend/pine-chat-a11y.html", "content": HTML},
            {"path": "tests/test_pine_chat_a11y.py", "content": TEST},
        ],
    }

class GovernanceTest(unittest.TestCase):
    def deny(self, obj, reason):
        with self.assertRaisesRegex(gate.PolicyDenied, reason):
            gate.inspect(obj)

    def test_valid_review_only_with_pinned_sha(self):
        receipt = gate.inspect(fixture())
        self.assertEqual(receipt["status"], "needs_independent_review")
        self.assertFalse(receipt["executed"])
        self.assertFalse(receipt["approved"])
        self.assertEqual(len(receipt["files"]), 2)
        self.assertEqual(set(f["path"] for f in receipt["payload"]["files"]), gate.ARTIFACTS)
        self.assertEqual(len(receipt["review_sha256"]), 64)

    def test_second_enrolled_task_is_exactly_scoped(self):
        f=fixture()
        f["work_id"]="dev_matrix_synthetic_release_v1"
        f["files"][0]["path"]="frontend/dev-autonomy-validated-v1.html"
        f["files"][1]["path"]="tests/test_dev_autonomy_validated_v1.py"
        allowed=gate.inspect(f)
        self.assertFalse(allowed["executed"])
        self.assertEqual(allowed["work_id"],"dev_matrix_synthetic_release_v1")
        f["files"][1]["path"]="tests/test_pine_chat_a11y.py"
        self.deny(f,"path_not_enrolled")

    def test_cross_tenant_denied(self):
        f = fixture(); f["project"] = "pine_private"
        self.deny(f, "scope_mismatch")

    def test_cross_repo_denied(self):
        f = fixture(); f["repository"] = "private/real-pine"
        self.deny(f, "scope_mismatch")

    def test_wrong_manifest_and_task_denied(self):
        for k in ("manifest", "work_id", "base_branch"):
            with self.subTest(k=k):
                f = fixture(); f[k] = "unapproved"
                self.deny(f, "scope_mismatch")

    def test_arbitrary_tool_command_field_denied(self):
        f = fixture(); f["tool"] = "shell"
        self.deny(f, "envelope_schema_denied")

    def test_absolute_traversal_and_symlink_like_paths_denied(self):
        for path in ("/etc/passwd", "frontend/../secrets.py", "frontend/.ssh/key",
                     "frontend/pine-chat-a11y.html/../../x", "frontend\\pine-chat-a11y.html"):
            with self.subTest(path=path):
                f = fixture(); f["files"][0]["path"] = path
                self.deny(f, "path")

    def test_duplicate_denied(self):
        f = fixture(); f["files"][1] = copy.deepcopy(f["files"][0])
        self.deny(f, "duplicate_target")

    def test_secret_network_and_script_import_denied(self):
        for token in ("fetch('/secret')", "WebSocket", "api_key", "https://example.org",
                      "<script src='remote'>", "localStorage"):
            with self.subTest(token=token):
                f = fixture(); f["files"][0]["content"] += token
                self.deny(f, "unsafe_content")
        f = fixture(); f["files"][1]["content"] += "\nimport subprocess\n"
        self.deny(f, "unsafe_content_pattern|test_import_not_enrolled")

    def test_missing_test_denied(self):
        f = fixture(); f["files"][1]["content"] = 'import unittest\nprint("test")\n'
        self.deny(f, "independent_test_missing")

    def test_extra_file_and_unknown_metadata_denied(self):
        f = fixture(); f["files"].append({"path": "frontend/extra.html", "content": HTML})
        self.deny(f, "exact_file_count_required")
        f = fixture(); f["files"][0]["expected_sha256"] = "0" * 64
        self.deny(f, "proposal_file_schema_denied")

    def test_baseline_cannot_be_model_supplied(self):
        f = fixture()
        receipt = gate.inspect(f, baseline={"frontend/pine-chat-a11y.html": "f" * 64})
        html = next(v for v in receipt["payload"]["files"] if v["path"].endswith(".html"))
        self.assertEqual(html["expected_sha256"], "f" * 64)
        with self.assertRaisesRegex(gate.PolicyDenied, "baseline_hash_denied"):
            gate.inspect(f, baseline={"frontend/pine-chat-a11y.html": "../abc"})

    def test_size_and_non_json_denied(self):
        f = fixture(); f["files"][0]["content"] = HTML + "z" * 19000
        self.deny(f, "file_size_denied")

if __name__ == "__main__":
    unittest.main()
