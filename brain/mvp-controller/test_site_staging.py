#!/usr/bin/env python3
"""Non-networked tests for sandboxed private static staging."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("site_staging", HERE/"site_staging.py")
stage=importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)

class StagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="site-stage-qa-")
        self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)
        stage.ROOT=self.home
        stage.INBOX=self.home/"staging-inbox"
        stage.OUTPUT=self.home/"staging-private"
        self.p=stage.INBOX/"moksha_overhaul"/"moksha_overhaul_v1.json"
        self.p.parent.mkdir(parents=True)
        self.manifest={"version":1,"project":"moksha_overhaul","publish":False,"spend":False,"assets":{},
          "pages":[{"slug":"home","title":"Welcome","eyebrow":"Goa Sanctuary","headline":"Rooftop sauna and ice","summary":"Verified description",
            "hero":{"role":"sauna","label":"Actual photo pending"},
            "cta":{"label":"More","target":"experiences"},
            "sections":[{"title":"Test","text":"No misleading claims","role":"ice","image_label":"Actual ice tub pending"}]},
           {"slug":"experiences","title":"Experiences","eyebrow":"Explore","headline":"Choose a ritual","summary":"Descriptions pending",
            "hero":{"role":"garden","label":"Garden photo pending"},
            "cta":{"label":"Home","target":"home"},
            "sections":[{"title":"A ritual","text":"Edited only in sandbox","role":"mud","image_label":"Mud photo pending"}]}]}
        self.save()
    def save(self):
        self.p.write_text(json.dumps(self.manifest))
    def test_build_and_idempotency(self):
        a=stage.build("moksha_overhaul","moksha_overhaul_v1")
        self.assertEqual(a["state"],"private_preview_ready")
        self.assertTrue(a["nonindexed"])
        self.assertFalse(a["server_started"])
        self.assertFalse(a["publication"])
        self.assertEqual(a["pages"],2)
        self.assertTrue(Path(a["local_path"],"index.html").exists())
        self.assertTrue(stage.build("moksha_overhaul","moksha_overhaul_v1")["deduplicated"])
    def test_escaped_html(self):
        self.manifest["pages"][0]["headline"]='<img src=x onerror="alert(1)">'
        self.save()
        p=stage.build("moksha_overhaul","moksha_overhaul_v1")["local_path"]
        source=Path(p,"index.html").read_text()
        self.assertIn("&lt;img",source)
        self.assertNotIn('<img src=x',source)
        self.assertIn("noindex,nofollow",source)
    def test_missing_nav_target_rejected(self):
        self.manifest["pages"][0]["cta"]["target"]="evil"
        self.save()
        with self.assertRaises(ValueError): stage.build("moksha_overhaul","moksha_overhaul_v1")
    def test_traversal_rejected(self):
        with self.assertRaises(ValueError): stage.build("..","moksha_overhaul_v1")
        self.manifest["pages"][0]["slug"]="../escape"
        self.save()
        with self.assertRaises(ValueError): stage.build("moksha_overhaul","moksha_overhaul_v1")
    def test_unapproved_asset_rejected(self):
        self.manifest["assets"]={"sauna":{"filename":"sauna.jpg","source":"Owner","license":"Original","rights_verified":False}}
        self.save()
        with self.assertRaises(ValueError): stage.build("moksha_overhaul","moksha_overhaul_v1")
    def test_publish_and_spend_rejected(self):
        for key in ("publish","spend"):
            self.manifest[key]=True
            self.save()
            with self.assertRaises(ValueError):stage.build("moksha_overhaul","moksha_overhaul_v1")
            self.manifest[key]=False
    def test_manifest_symlink_rejected(self):
        original=self.p.with_suffix(".original")
        self.p.rename(original)
        self.p.symlink_to(original)
        with self.assertRaises(ValueError):stage.build("moksha_overhaul","moksha_overhaul_v1")

if __name__=="__main__":
    unittest.main(verbosity=2)
