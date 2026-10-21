#!/usr/bin/env python3
"""Non-network, non-render tests for Marketing's Reel Studio adapter."""
import importlib.util
import tempfile
from pathlib import Path
import unittest

SRC=Path(__file__).with_name("reel_bridge.py")
class ReelBridgeTest(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(prefix="reel-bridge-test-")
        self.root=Path(self.t.name)
        spec=importlib.util.spec_from_file_location("reel_bridge_test",SRC)
        self.mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.mod.INBOX=self.root/"inbox"
        self.mod.OUTBOX=self.root/"outbox"
        self.mod.REEL=self.root/"reel.py"
    def tearDown(self):self.t.cleanup()
    def media(self):
        d=self.mod.INBOX/"batch1"
        d.mkdir(parents=True)
        (d/"media.jpg").write_bytes(b"a"*2048)
        return d
    def test_only_safe_batches(self):
        for v in ("../root","/tmp","a b","", "x"*65):
            with self.assertRaises(ValueError):self.mod.batch_paths(v)
    def test_preflight_without_render(self):
        self.media()
        info=self.mod.preflight("batch1")
        self.assertEqual(info["media_count"],1)
        self.assertFalse(info["publish_allowed"])
        self.assertFalse(self.mod.OUTBOX.exists())
    def test_symlink_rejected(self):
        d=self.media()
        (d/"unsafe.png").symlink_to(d/"media.jpg")
        with self.assertRaisesRegex(RuntimeError,"no links"):
            self.mod.scan("batch1")
    def test_render_off_by_default(self):
        self.media()
        with self.assertRaisesRegex(RuntimeError,"not enabled"):
            self.mod.render("batch1","sample",{"render_enabled":False})
        self.assertFalse(self.mod.OUTBOX.exists())

if __name__=="__main__":unittest.main(verbosity=2)
