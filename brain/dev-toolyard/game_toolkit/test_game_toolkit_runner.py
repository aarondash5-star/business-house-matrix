"""Independent negative tests for Shaadi fixed-recipe Matrix game tooling."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("game_toolkit_runner", ROOT / "game_toolkit_runner.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class GameToolkitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "toolkit"
        self.root.mkdir()
        (self.root / "tools").mkdir()
        (self.root / "tools/smoke.mjs").write_text("const smoke = 1;")
        (self.root / "node_modules").mkdir()
        (self.root / "package-lock.json").write_text('{"lockfileVersion":3}')
        (self.root / "toolchain-manifest.json").write_text(json.dumps({
            "schema_version": 1, "name": "matrix-shaadi-game-development-toolkit",
            "package_lock_sha256": m.LOCK_SHA256
        }))
        self.original_digest = m.digest

    def tearDown(self):
        self.tmp.cleanup()

    def validated(self, project=m.PROJECT, manifest="shaadi_toolkit_verify_v1"):
        with mock.patch.object(m, "digest", return_value=m.LOCK_SHA256):
            return m.validate(project, manifest, self.root)

    def test_accepts_only_exact_registered_project(self):
        self.assertEqual(self.validated()["project"], m.PROJECT)
        for bad in ("delulu_tech", "moksha_overhaul", "shaadi_aunty_dodge;whoami",
                    "../shaadi_aunty_dodge", ""):
            with self.assertRaises(m.ToolkitDenied):
                self.validated(project=bad)

    def test_unknown_command_and_path_strings_rejected(self):
        for bad in ("../tools", "run", "shell", "shaadi_toolkit_smoke_v1;echo",
                    "/var/lib", "shaadi_toolkit_smoke_v1 "):
            with self.assertRaises(m.ToolkitDenied):
                self.validated(manifest=bad)

    def test_symlink_toolkit_denied(self):
        alias = Path(self.tmp.name) / "pointer"
        alias.symlink_to(self.root)
        with self.assertRaisesRegex(m.ToolkitDenied, "symlink"):
            m.validate(m.PROJECT, "shaadi_toolkit_verify_v1", alias)

    def test_locked_deps_drift_denied(self):
        with self.assertRaisesRegex(m.ToolkitDenied, "package_lock_drift"):
            m.validate(m.PROJECT, "shaadi_toolkit_verify_v1", self.root)

    def test_manifest_identity_drift_denied(self):
        doc = json.loads((self.root / "toolchain-manifest.json").read_text())
        doc["name"] = "other_project"
        (self.root / "toolchain-manifest.json").write_text(json.dumps(doc))
        with self.assertRaisesRegex(m.ToolkitDenied, "manifest_contract_drift"):
            self.validated()

    def test_symbolic_manifest_file_denied(self):
        manifest = self.root / "toolchain-manifest.json"
        manifest.unlink()
        manifest.symlink_to(self.root / "package-lock.json")
        with self.assertRaisesRegex(m.ToolkitDenied, "symlink"):
            self.validated()

    def test_missing_bubblewrap_denied_closed(self):
        with mock.patch.object(m, "BWRAP", self.root / "no-bwrap"):
            with self.assertRaisesRegex(m.ToolkitDenied, "bubblewrap_required"):
                m._sandbox_command("node_smoke", self.root)

    def test_sandbox_is_offline_and_static(self):
        with mock.patch.object(m, "BWRAP", self.root / "package-lock.json"):
            cmd = m._sandbox_command("node_smoke", self.root)
        self.assertIn("--unshare-all", cmd)
        self.assertIn("--die-with-parent", cmd)
        self.assertIn("--ro-bind", cmd)
        self.assertNotIn("sh", cmd)
        self.assertNotIn("-c", cmd)
        self.assertEqual(cmd[-2:], [str(m.NODE), "/toolkit/tools/smoke.mjs"])
        self.assertNotIn("delulu_tech", " ".join(cmd))
        self.assertNotIn("business-house-matrix", " ".join(cmd))
        self.assertNotIn("mac-linux", " ".join(cmd))

    def test_only_fixed_qa_recipes_supported(self):
        with mock.patch.object(m, "BWRAP", self.root / "package-lock.json"):
            with self.assertRaises(m.ToolkitDenied):
                m._sandbox_command("npm_install", self.root)

    def test_cc0_archive_evidence_required(self):
        d = self.root / "third_party/downloads"
        d.mkdir(parents=True)
        with self.assertRaises(FileNotFoundError):
            m.asset_inventory(self.root)

    def test_pinned_read_only_verification_does_not_run_shell(self):
        with mock.patch.object(m, "digest", return_value=m.LOCK_SHA256):
            with mock.patch.object(m.subprocess, "run") as call:
                out = m.execute(m.PROJECT, "shaadi_toolkit_verify_v1", self.root)
        self.assertTrue(out["qa_passed"])
        self.assertFalse(out["published"])
        self.assertFalse(out["game_repository_modified"])
        call.assert_not_called()

    def test_shell_never_selected_from_inputs(self):
        with mock.patch.object(m, "digest", return_value=m.LOCK_SHA256):
            with mock.patch.object(m.subprocess, "run") as call:
                with self.assertRaises(m.ToolkitDenied):
                    m.execute("shaadi_aunty_dodge", "rm -rf /", self.root)
        call.assert_not_called()

    def test_smoke_failure_does_not_promote(self):
        with mock.patch.object(m, "digest", return_value=m.LOCK_SHA256):
            with mock.patch.object(m, "BWRAP", self.root / "package-lock.json"):
                p = mock.Mock(returncode=1, stdout="test failure", stderr="fixture error")
                with mock.patch.object(m.subprocess, "run", return_value=p) as call:
                    result = m.execute(m.PROJECT, "shaadi_toolkit_smoke_v1", self.root)
        self.assertFalse(result["qa_passed"])
        self.assertFalse(result["published"])
        kwargs = call.call_args.kwargs
        self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
        self.assertLessEqual(kwargs["timeout"], 95)

    def test_smoke_success_is_technical_only(self):
        with mock.patch.object(m, "digest", return_value=m.LOCK_SHA256):
            with mock.patch.object(m, "BWRAP", self.root / "package-lock.json"):
                p = mock.Mock(returncode=0, stdout=json.dumps({"passed": 13, "failed": 0}), stderr="")
                with mock.patch.object(m.subprocess, "run", return_value=p):
                    out = m.execute(m.PROJECT, "shaadi_toolkit_smoke_v1", self.root)
        self.assertTrue(out["qa_passed"])
        self.assertTrue(out["technical_only"])
        self.assertFalse(out["published"])
        self.assertFalse(out["game_repository_modified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
