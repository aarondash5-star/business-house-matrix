"""Bounded, read-only provenance inventory for the art worker.
Never infer a commercial license from an asset's filename.
"""
import json,hashlib,os
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=Path.home()/"matrix-game-toolkit-20261025/third_party"
ART=Path.home()/"shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1"
OUTPUT=ART/"iterations/20261026-art-worker-v1"
roots=[BASE/"mpfb2-src", BASE/"blender-xdg-config/blender/4.5/extensions/user_default/mpfb"]
ext={".blend",".obj",".fbx",".glb",".gltf",".mhclo",".mhmat",".mhpxy",".json"}
assets=[]
for root in roots:
 if not root.is_dir() or root.is_symlink():continue
 for p in root.rglob("*"):
  if len(assets)>=400:break
  if p.is_file() and not p.is_symlink() and p.suffix.lower() in ext:
   assets.append({"path":str(p.relative_to(BASE)),"type":p.suffix.lower(),
                  "size":p.stat().st_size,"license":"verification_required"})
markers=[]
for root in roots:
 if not root.exists():continue
 for pattern in ("LICENSE*","COPYING*"):
  for p in root.rglob(pattern):
   if p.is_file() and not p.is_symlink() and len(markers)<40:
    markers.append({"path":str(p.relative_to(BASE)),
                    "sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
report={"project":"shaadi_aunty_dodge","scope":"source_inventory_only",
  "assets_inspected":len(assets),"files":assets[:120],
  "licenses_found":markers,"all_assets_commercially_cleared":False,
  "owner_approved":False,"release_authorized":False}
OUTPUT.mkdir(parents=True,exist_ok=True)
(OUTPUT/"foundation_inventory.json").write_text(json.dumps(report,indent=2))
print("FOUNDATION_INVENTORY_OK",len(assets),len(markers))
