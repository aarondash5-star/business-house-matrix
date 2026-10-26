#!/usr/bin/env python3
"""Adversarial visual provenance and fixed-function capability tests."""
import hashlib,importlib.util,json,os,struct,tempfile,unittest,zlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
def get(n):
    q=importlib.util.spec_from_file_location(n,HERE/(n+".py"))
    m=importlib.util.module_from_spec(q);q.loader.exec_module(m);return m
vis=get("visual_evidence")
cap=get("capability_probe")

def make_png(width,height):
    hdr=struct.pack(">IIBBBBB",width,height,8,2,0,0,0)
    raw=b"".join(b"\x00"+b"\x75\x9d\xb1"*width for _ in range(height))
    body=zlib.compress(raw,8)
    def chunk(kind,data):
        return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
    return vis.PNG+chunk(b"IHDR",hdr)+chunk(b"IDAT",body)+chunk(b"IEND",b"")

class Visual(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/"screenshots").mkdir()
        self.p=self.root/"screenshots"/"inbox-390.png"
        self.p.write_bytes(make_png(390,600))
        self.item={"screen":"inbox","file":"inbox-390.png","width":390,
                   "sha256":hashlib.sha256(self.p.read_bytes()).hexdigest()}
    def test_actual_png_and_dims(self):
        a=vis.review_inventory(self.root,[self.item])
        self.assertEqual(a["images"],1)
        self.assertFalse(a["independent_visual_approval"])
        self.assertFalse(a["release_authorized"])
    def test_forged_renamed_text_denied(self):
        self.p.write_bytes(b"PNG fake 390px not a screenshot" * 6)
        with self.assertRaisesRegex(vis.VisualDenied,"not_png"):vis.inspect_png(self.p,390)
    def test_wrong_viewport_denied(self):
        with self.assertRaisesRegex(vis.VisualDenied,"viewport"):vis.inspect_png(self.p,360)
    def test_unrelated_sha_denied(self):
        self.item["sha256"]="f"*64
        with self.assertRaisesRegex(vis.VisualDenied,"hash_drift"):vis.review_inventory(self.root,[self.item])
    def test_relative_escape_denied(self):
        self.item["file"]="../credentials.png"
        with self.assertRaisesRegex(vis.VisualDenied,"path_escape"):vis.review_inventory(self.root,[self.item])
    def test_self_signed_visual_claim_unavailable(self):
        self.assertFalse(vis.inspect_png(self.p,390)["owner_approved"])
        self.assertFalse(vis.inspect_png(self.p,390)["visually_compliant"])

class Capability(unittest.TestCase):
    def test_unapproved_tool_not_admitted(self):
        a=cap.probe("arbitrary_shell")
        self.assertEqual(a["reason"],"unknown_tool")
        self.assertFalse(a["production_enabled"])
    def test_discovery_does_not_prove_feature(self):
        a=cap.probe("python3")
        self.assertFalse(a["feature_compatibility_verified"])
        self.assertFalse(a["method_used"])
    def test_missing_binary_denied(self):
        a=cap.probe("blender",which=lambda _:None)
        self.assertEqual(a["reason"],"binary_missing")
    def test_symlink_binary_requires_review(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"python3";p.symlink_to("/usr/bin/python3")
            a=cap.probe("python3",which=lambda _:str(p))
            self.assertEqual(a["reason"],"binary_symlink_requires_review")

if __name__=="__main__":unittest.main()
