#!/usr/bin/env python3
"""Screenshot provenance and viewport guard for independent Yard art/UX QA.

This checks actual PNG structure, dimensions, capture hash and scoped directory.
It is not an independent artistic review or owner acceptance.
"""
from __future__ import annotations
import argparse,hashlib,json,struct,zlib
from pathlib import Path

PNG=b"\x89PNG\r\n\x1a\n"
WIDTHS={320,360,375,390,414,768,800,1024,1440}
class VisualDenied(ValueError):pass

def inspect_png(path:Path,expected_width:int):
    p=Path(path)
    if p.is_symlink() or not p.is_file():raise VisualDenied("capture_file_missing_or_symlink")
    n=p.stat().st_size
    if n<75 or n>5_000_000:raise VisualDenied("capture_size_invalid")
    data=p.read_bytes()
    if data[:8]!=PNG or data[12:16]!=b"IHDR" or struct.unpack(">I",data[8:12])[0]!=13:
        raise VisualDenied("capture_not_png_ihdr")
    if (zlib.crc32(data[12:29])&0xffffffff)!=struct.unpack(">I",data[29:33])[0]:
        raise VisualDenied("capture_header_crc_invalid")
    w,h=struct.unpack(">II",data[16:24])
    if expected_width not in WIDTHS or w!=expected_width or not (300<=h<=8000):
        raise VisualDenied("capture_viewport_mismatch")
    if b"IDAT" not in data or not data.endswith(b"\x00\x00\x00\x00IEND\xaeB\x60\x82"):
        raise VisualDenied("capture_image_data_incomplete")
    return {"width":w,"height":h,"bytes":n,"sha256":hashlib.sha256(data).hexdigest(),
            "structurally_valid_capture":True,
            "visually_compliant":False,"owner_approved":False}

def review_inventory(task_root:Path,items:list):
    root=Path(task_root).resolve(strict=True)
    folder=(root/"screenshots").resolve(strict=True)
    if not isinstance(items,list) or not items or len(items)>150:
        raise VisualDenied("bounded_screenshot_manifest_required")
    seen=set();captures=[]
    for item in items:
        if not isinstance(item,dict) or set(item)!={"screen","file","width","sha256"}:
            raise VisualDenied("capture_contract_fields")
        name=item["file"]
        if not isinstance(name,str) or "/" in name or "\\" in name or not name.endswith(".png") or name.startswith("."):
            raise VisualDenied("capture_path_escape")
        if (item["screen"],item["width"]) in seen:raise VisualDenied("capture_duplicate")
        seen.add((item["screen"],item["width"]))
        p=folder/name
        if p.is_symlink() or not p.resolve(strict=True).is_relative_to(folder):
            raise VisualDenied("capture_symlink_or_outside")
        result=inspect_png(p,item["width"])
        if result["sha256"]!=item["sha256"]:raise VisualDenied("capture_hash_drift")
        captures.append({"screen":item["screen"],"width":item["width"],
                         "sha256":result["sha256"],"structurally_valid":True})
    return {"status":"image_evidence_structurally_verified",
            "images":len(captures),"captures":captures,
            "independent_visual_approval":False,"owner_design_accepted":False,
            "release_authorized":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("manifest",type=Path)
    x=p.parse_args()
    try:
        if x.manifest.is_symlink() or not x.manifest.is_file() or x.manifest.stat().st_size>24000:
            raise VisualDenied("unsafe_capture_manifest")
        print(json.dumps(review_inventory(x.root,json.loads(x.manifest.read_text())["captures"]),indent=2))
    except (OSError,KeyError,TypeError,VisualDenied,json.JSONDecodeError) as e:
        print(json.dumps({"status":"blocked","reason":str(e),"release_authorized":False}))
        raise SystemExit(2)
if __name__=="__main__":main()
