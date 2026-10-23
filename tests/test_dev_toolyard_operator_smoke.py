#!/usr/bin/env python3
"""Bounded, offline smoke/regression checks for operator-led Matrix Dev Tool Yard.

No autonomous dispatch, external network, root, production writes, or paid APIs.
All synthetic writes are confined to TemporaryDirectory, then cleaned by Python.
This is a test suite, NOT a general command-execution gateway.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

CONTROLLER = Path("/var/lib/generic-linux-automator-exec/matrix-controller/controller.py")
EXPECTED_CONTROLLER_SHA256 = "b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e"
AUTONOMY_SERVICE = "bhm-autonomy-controller.service"
STATUS_LINK_SERVICE = "bhm-superdev-ssh-duplex.service"
PRESERVED_SERVICES = (
    "bhm-searxng.service",
    "bhm-marketing-research-api.service",
    "bhm-research-relay.service",
)


def fixed_run(argv: list[str], *, cwd: Path | None = None, timeout: float = 20) -> subprocess.CompletedProcess[str]:
    """Run only caller-specified fixed argv; never invoke a shell."""
    return subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,
    )


def unit_property(unit: str, name: str) -> str:
    result = fixed_run(
        ["/usr/bin/systemctl", "--user", "show", unit, "-p", name, "--value"],
        timeout=10,
    )
    if result.returncode:
        raise AssertionError(f"systemctl show {unit} {name}: {result.stderr.strip()}")
    return result.stdout.strip()


class OperatorLedToolYardSmoke(unittest.TestCase):
    def test_autonomy_dispatcher_inactive(self) -> None:
        self.assertEqual(unit_property(AUTONOMY_SERVICE, "ActiveState"), "inactive")
        self.assertEqual(unit_property(AUTONOMY_SERVICE, "UnitFileState"), "disabled")

    def test_fixed_status_link_preserved(self) -> None:
        self.assertEqual(unit_property(STATUS_LINK_SERVICE, "ActiveState"), "active")
        self.assertEqual(unit_property(STATUS_LINK_SERVICE, "UnitFileState"), "enabled")

    def test_other_research_services_preserved(self) -> None:
        for unit in PRESERVED_SERVICES:
            with self.subTest(unit=unit):
                self.assertEqual(unit_property(unit, "ActiveState"), "active")

    def test_original_v6_controller_unchanged(self) -> None:
        self.assertTrue(CONTROLLER.is_file())
        self.assertEqual(hashlib.sha256(CONTROLLER.read_bytes()).hexdigest(), EXPECTED_CONTROLLER_SHA256)

    def test_python_isolated_edit_compile(self) -> None:
        with tempfile.TemporaryDirectory(prefix="bhm-toolyard-py-") as name:
            workspace = Path(name)
            module = workspace / "price.py"
            module.write_text("def total(a, b):\n    return a + b\n", encoding="utf-8")
            source = module.read_text(encoding="utf-8").replace("return a + b", "return round(a + b, 2)")
            module.write_text(source, encoding="utf-8")
            scope: dict[str, object] = {}
            exec(compile(module.read_text(encoding="utf-8"), str(module), "exec"), scope)
            self.assertEqual(scope["total"](1.005, 2.005), 3.01)

    def test_sqlite_transaction_and_constraint(self) -> None:
        with sqlite3.connect(":memory:") as conn:
            conn.execute("CREATE TABLE tasks (key TEXT PRIMARY KEY, state TEXT NOT NULL)")
            conn.execute("INSERT INTO tasks VALUES (?, ?)", ("synthetic-task-1", "completed"))
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("INSERT INTO tasks VALUES (?, ?)", ("synthetic-task-1", "completed"))
            count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            self.assertEqual(count, 1)

    def test_node_runtime_json(self) -> None:
        node = shutil.which("node")
        self.assertIsNotNone(node)
        result = fixed_run([str(node), "-e", "console.log(JSON.stringify({ok:true,n:2+3}))"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ok": True, "n": 5})

    def test_git_cycle_confined_to_temp_repo(self) -> None:
        git = shutil.which("git")
        self.assertIsNotNone(git)
        with tempfile.TemporaryDirectory(prefix="bhm-toolyard-git-") as name:
            repo = Path(name)
            init = fixed_run([str(git), "init", "-q", str(repo)])
            self.assertEqual(init.returncode, 0, init.stderr)
            (repo / "README.md").write_text("Synthetic Tool Yard fixture\n", encoding="utf-8")
            add = fixed_run([str(git), "-C", str(repo), "add", "README.md"])
            self.assertEqual(add.returncode, 0, add.stderr)
            commit = fixed_run([
                str(git), "-C", str(repo),
                "-c", "user.name=Matrix QA",
                "-c", "user.email=matrix-qa@example.invalid",
                "commit", "-q", "-m", "synthetic fixture",
            ])
            self.assertEqual(commit.returncode, 0, commit.stderr)
            status = fixed_run([str(git), "-C", str(repo), "status", "--porcelain"])
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(status.stdout.strip(), "")

    def test_nonzero_exit_is_observable(self) -> None:
        result = fixed_run([sys.executable, "-c", "import sys; sys.exit(17)"])
        self.assertEqual(result.returncode, 17)

    def test_child_timeout_is_bounded(self) -> None:
        with self.assertRaises(subprocess.TimeoutExpired):
            fixed_run([sys.executable, "-c", "import time; time.sleep(3)"], timeout=0.2)

    def test_firefox_real_offline_render(self) -> None:
        firefox = shutil.which("firefox")
        self.assertIsNotNone(firefox, "Firefox is required for OSS browser QA")
        with tempfile.TemporaryDirectory(prefix="bhm-toolyard-firefox-") as name:
            root = Path(name)
            page = root / "index.html"
            page.write_text(
                "<!doctype html><html><head><title>Tool Yard QA</title></head>"
                "<body><h1>Operator-led QA</h1><p>Offline fixture</p></body></html>",
                encoding="utf-8",
            )
            profile = root / "profile"
            profile.mkdir()
            screenshot = root / "render.png"
            result = fixed_run(
                [str(firefox), "-profile", str(profile), "--headless", "--screenshot",
                 str(screenshot), page.resolve().as_uri()],
                timeout=25,
            )
            self.assertEqual(result.returncode, 0, result.stderr[-1500:])
            self.assertTrue(screenshot.is_file(), result.stderr[-1500:])
            self.assertGreater(screenshot.stat().st_size, 1024)


if __name__ == "__main__":
    unittest.main(verbosity=2)
