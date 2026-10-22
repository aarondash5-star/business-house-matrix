#!/usr/bin/env python3
"""Mandatory fail-closed Bubblewrap isolation probe, separate from pytest."""
from pathlib import Path
import sys
import tempfile
sys.path.insert(0,"brain/dev-operator")
import workcell_runner

with tempfile.TemporaryDirectory(prefix="gate-e-ci-") as directory:
    doctor=workcell_runner.doctor(Path(directory))
    if doctor["passed"] is not True:
        raise SystemExit("Gate E Bubblewrap isolation not certified")
    print("NESTED_BUBBLEWRAP_ISOLATION_PASS",doctor["probe"])
