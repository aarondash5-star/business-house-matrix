"""Actual Blender WIP candidate frames (not quality-acceptance renders)."""
import bpy,hashlib,json,os
from pathlib import Path
from mathutils import Vector
root=Path(os.environ["SHAADI_ART_OUTPUT"])
root.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
s.render.engine="CYCLES"
s.cycles.samples=14
s.render.film_transparent=True
s.use_nodes=False
s.cycles.device="CPU"
s.render.resolution_x=480
s.render.resolution_y=672
s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
s.render.image_settings.color_mode='RGBA'
back=bpy.data.objects.get("Backcloth")
if back:back.hide_render=True
body=bpy.data.objects["SharmaAunty_MPFBBasemesh"]
rig=bpy.data.objects["SharmaAunty_53Bone_Rig"]
cam=bpy.data.objects.get("QA_WORKER_CAMERA")
if cam is None:
 cdata=bpy.data.cameras.new("QA_WORKER_CAMERA")
 cam=bpy.data.objects.new("QA_WORKER_CAMERA",cdata)
 s.collection.objects.link(cam)
cam.data.type="ORTHO"
cam.data.clip_start=.01;cam.data.clip_end=100
frames=[
 ("neutral_front",Vector((0,-5,2.1)),Vector((0,0,.82)),2.25,None,0),
 ("three_quarter",Vector((3.3,-4,2.1)),Vector((0,0,.82)),2.25,None,0),
 ("facial_smile",Vector((.4,-4,1.78)),Vector((0,0,1.32)),.84,"Smile",.72),
 ("facial_blink",Vector((.4,-4,1.78)),Vector((0,0,1.32)),.84,"Blink",1.0)
]
results={}
for label,location,target,scale,morph,val in frames:
 cam.location=location
 cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.data.ortho_scale=scale
 s.camera=cam
 for k in body.data.shape_keys.key_blocks:
  if k.name in ("Smile","Blink","JawOpen"):k.value=0
 if morph:body.data.shape_keys.key_blocks[morph].value=val
 p=root/(label+".png")
 s.render.filepath=str(p)
 bpy.ops.render.render(write_still=True)
 results[label]={"path":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"size":p.stat().st_size}
for k in body.data.shape_keys.key_blocks:
 if k.name in ("Smile","Blink","JawOpen"):k.value=0
receipt={"status":"rendered_for_review","gate":"SAD-VISUAL-QUALITY-V1",
 "views":results,"visual_pass":False,"owner_approved":False,
 "production_authorized":False}
(root/"render_study_receipt.json").write_text(json.dumps(receipt,indent=2))
print("ART_RENDER_STUDY",json.dumps(receipt),flush=True)
