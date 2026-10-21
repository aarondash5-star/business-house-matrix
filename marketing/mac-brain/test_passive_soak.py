#!/usr/bin/env python3
"""No stress, no reboot; offline QA for passive telemetry gate."""
import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import passive_soak as soak


class PassiveSoakTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="bhm-soak-")
        self.p=patch.object(soak,"ROOT",Path(self.temp.name))
        self.p.start()

    def tearDown(self):
        self.p.stop()
        self.temp.cleanup()

    def test_reject_unsafe_ids(self):
        for v in ("../escape","foo","passive-20261022-../other","passive-20261022-!"):
            with self.assertRaises(ValueError):
                soak.prepare(v)

    def test_owner_only_directory_and_csv_schema(self):
        d=soak.prepare("passive-20261022-test")
        self.assertEqual(d.stat().st_mode&0o077,0)
        self.assertEqual((d/"samples.csv").stat().st_mode&0o077,0)
        r={"utc":"2026-10-22T00:00:00+00:00","max_sensor_c":60.0,
           "fan_rpm":4000,"load1":0.4,"services":{s:True for s in soak.SERVICES}}
        soak.append_sample(d,r)
        with (d/"samples.csv").open() as f:
            rows=list(csv.reader(f))
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[1][1],"60.0")

    def test_status_atomic_and_noncertifying(self):
        d=soak.prepare("passive-20261022-persist")
        state={"state":"running","kind":"passive_no_load","result":"NOT_CERTIFIED"}
        soak.save_status(d/"status.json",state)
        self.assertTrue((d/"status.json").is_file())
        self.assertEqual((d/"status.json").stat().st_mode&0o077,0)

    def test_no_active_load_in_sampler(self):
        def systemctl(args,**kwargs):
            class Result:
                stdout="active\n"
                returncode=0
            self.assertEqual(args[:2],["/usr/bin/systemctl","is-active"])
            return Result()
        with patch.object(soak.reel_bridge,"mac_temperature_c",return_value=62),patch.object(soak,"fan_rpm",return_value=3200),patch.object(soak.subprocess,"run",side_effect=systemctl):
            r=soak.sample()
        self.assertEqual(r["max_sensor_c"],62)
        self.assertTrue(all(r["services"].values()))
        self.assertEqual(r["fan_rpm"],3200)

    def test_missing_thermal_sensor_rejects(self):
        with patch.object(soak.reel_bridge,"mac_temperature_c",return_value=None):
            with self.assertRaises(RuntimeError):
                soak.sample()


if __name__=="__main__":
    unittest.main(verbosity=2)
