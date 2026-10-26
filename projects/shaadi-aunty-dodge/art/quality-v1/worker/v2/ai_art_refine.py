#!/usr/bin/env python3
"""Allowlisted geometry edits: local, reversible, *uncertified* Blender WIP."""
import bpy,math,json,os,hashlib,random
from mathutils import Vector
from pathlib import Path
random.seed(218)
profile=os.environ["ART_REVISION_PROFILE"]
assert profile in {"jasmine","glasses","zari"}
root=Path(os.environ["ART_CYCLE_DIR"])
root.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
rig=bpy.data.objects.get("SharmaAunty_53Bone_Rig")
assert rig and len(rig.data.bones)>=35
def material(name,color,metal,rough):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
 m.diffuse_color=(*color,1)
 m.use_nodes=True
 bs=m.node_tree.nodes.get("Principled BSDF")
 if bs:
  bs.inputs["Base Color"].default_value=(*color,1)
  bs.inputs["Metallic"].default_value=metal
  bs.inputs["Roughness"].default_value=rough
 return m
petal=material("ARTWORK_Jasmine_Cream",(0.95,0.89,0.70),0,0.75)
core=material("ARTWORK_Jasmine_Center",(0.96,0.63,0.10),0.05,0.5)
gold=material("ARTWORK_Antique_Gold",(0.62,0.32,0.065),0.8,0.22)
tortoise=material("ARTWORK_Tortoise_Rich",(0.18,0.075,0.042),0.07,0.23)
created=[]
def sphere(name,center,size,mat,segments=10):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=6,location=center)
 ob=bpy.context.object;ob.name=name
 ob.scale=size;bpy.context.view_layer.update();ob.data.materials.append(mat)
 created.append(name)
 return ob
def move_with_head(ob):
 bpy.context.view_layer.update()
 mat=ob.matrix_world.copy()
 ob.parent=rig;ob.parent_type='BONE';ob.parent_bone='head'
 ob.matrix_world=mat
 bpy.context.view_layer.update()
 assert max(ob.dimensions)<.09,(ob.name,tuple(ob.dimensions))
if profile=="jasmine":
 # Rosette garland hugs top/bottom of rear coiled bun rather than a white halo.
 bun=bpy.data.objects.get("Coiled_Low_Bun")
 assert bun
 x,y,z=bun.location
 for row in range(2):
  for ix in range(14):
   t=2*math.pi*(ix+row*.46)/14
   a=.092+.014*row; b=.086+.012*row
   pos=Vector((x+math.cos(t)*a, y+.081+row*.007, z+math.sin(t)*b))
   for pet in range(5):
    q=2*math.pi*pet/5+t*.15
    loc=pos+Vector((math.cos(q)*.011,-.001,math.sin(q)*.011))
    ob=sphere("ART_Jasmine_R%02d_F%02d_P%d"%(row,ix,pet),loc,
              (.0135,.006,.008),petal,8)
    ob.rotation_euler.y=-q
    move_with_head(ob)
   ob=sphere("ART_Jasmine_Center_%d_%d"%(row,ix),pos+Vector((0,-.005,0)),
             (.006,.004,.006),core,8)
   move_with_head(ob)
elif profile=="glasses":
 # Refine existing editable tortoiseshell curves instead of swapping spectacles.
 rims=[o for o in s.objects if "Rim_Tortoise" in o.name]
 assert len(rims)>=2
 for rim in rims:
  if rim.type=='CURVE':
   rim.data.bevel_resolution=max(3,rim.data.bevel_resolution)
   rim.data.resolution_u=max(20,rim.data.resolution_u)
   rim.data.bevel_depth=max(.0022,rim.data.bevel_depth)
   if not rim.data.materials:rim.data.materials.append(tortoise)
   else:rim.data.materials[0]=tortoise
 for side in (-1,1):
  # Sculpted nose-pad assembly, visible in close-up; bone parenting at head.
  ob=sphere("ART_Glasses_Nosepad_%d"%side,
      (side*.030,-.234,1.412),(.008,.003,.015),gold,10)
  move_with_head(ob)
elif profile=="zari":
 # Thousands of procedural stitches are not advisable on low-end mobile.
 # Create a sparse ornamental editable floral band on the hanging pallu.
 pallu=bpy.data.objects.get("Sari_Pallu_Skinned_Cloth")
 assert pallu
 for i in range(32):
  z=.34+i*.023
  x=.178+.09*math.sin(i*.19)
  for j in range(3):
   xj=x+(j-1)*.016
   ob=sphere("ART_Zari_Motif_%02d_%d"%(i,j),(xj,-.249,z),
             (.0035,.0015,.008),gold,8)
   world=ob.matrix_world.copy();ob.parent=pallu; ob.matrix_world=world; bpy.context.view_layer.update(); assert max(ob.dimensions)<.09
out=root/("sharma_aunty_%s_wip.blend"%profile)
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
sha=hashlib.sha256(out.read_bytes()).hexdigest()
receipt={"profile":profile,"created_objects":len(created),"source_hash":os.environ["ART_SOURCE_SHA"],
 "out_blend":str(out),"out_sha256":sha,"visual_certified":False,
 "owner_approved":False,"release_authorized":False}
(root/"revision_receipt.json").write_text(json.dumps(receipt,indent=2))
print("ART_REVISION_CREATED",json.dumps(receipt),flush=True)
