#!/usr/bin/env python3
"""Smoke + safety tests for isolated Marketing Brain (no network calls)."""
import importlib.util
import os
import sqlite3
import tempfile
import unittest
from unittest import mock
from pathlib import Path

MODULE = Path(__file__).with_name("brain.py")


class MarketingBrainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="bhm-brain-test-")
        os.environ["BHM_MARKETING_HOME"] = self.tmp.name
        spec = importlib.util.spec_from_file_location("bhm_brain_test", MODULE)
        self.brain = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.brain)
        self.brain.connect().close()

    def tearDown(self):
        os.environ.pop("BHM_MARKETING_HOME", None)
        self.tmp.cleanup()

    def test_durable_queue_and_receipt(self):
        a = self.brain.enqueue("ping", {}, "sample")
        b = self.brain.enqueue("ping", {}, "sample")
        self.assertEqual(a["id"], b["id"])
        receipt = self.brain.work_once()
        self.assertEqual(receipt["state"], "completed")
        self.assertEqual(receipt["id"], a["id"])
        stored = self.brain.RECEIPTS / (a["id"] + ".json")
        self.assertTrue(stored.exists())
        self.assertEqual(self.brain.work_once()["state"], "idle")

    def test_unsafe_job_rejected(self):
        with self.assertRaises(ValueError):
            self.brain.enqueue("publish", {}, "bad")
        with self.assertRaises(ValueError):
            self.brain.enqueue("draft_plan", {}, "empty")
        self.assertEqual(self.brain.show_status()["queue"], {})

    def test_recover_stale_job(self):
        a = self.brain.enqueue("ping", {}, "stale")
        conn = self.brain.connect()
        conn.execute("UPDATE jobs SET state='running',updated='2020-01-01T00:00:00+00:00',attempts=1 WHERE id=?", (a["id"],))
        conn.commit()
        self.assertEqual(self.brain.recover_stale(conn, minutes=5), 1)
        conn.close()
        self.assertEqual(self.brain.work_once()["state"], "completed")

    def test_resource_guards(self):
        config = self.brain.configure()
        with self.assertRaisesRegex(RuntimeError, "memory"):
            self.brain.local_resource_guard({**config, "min_available_mem_mb": 999999})
        # CI runners may expose no coretemp devices; simulate one deterministically
        # rather than treating absence of a host sensor as a policy failure.
        with tempfile.TemporaryDirectory(prefix="bhm-temp-sensor-test-") as root:
            fake_hwmon = Path(root)
            dev = fake_hwmon / "hwmon0"
            dev.mkdir()
            (dev / "name").write_text("coretemp")
            (dev / "temp1_input").write_text("85000")
            original_path = Path
            def sensor_path(value):
                return fake_hwmon if str(value) == "/sys/class/hwmon" else original_path(value)
            with mock.patch.object(self.brain, "Path", side_effect=sensor_path):
                with self.assertRaisesRegex(RuntimeError, "temperature"):
                    self.brain.local_resource_guard({
                        **config, "min_available_mem_mb": 0, "max_core_temp_c": 1
                    })


if __name__ == "__main__":
    unittest.main(verbosity=2)
