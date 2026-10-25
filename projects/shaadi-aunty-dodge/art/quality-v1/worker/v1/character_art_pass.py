"""Bounded Blender artistic-rig WIP: editable morphs and four bone action studies.
Always stage only; never touch the original or claim visual approval.
"""
import bpy,math,hashlib,json,os
from pathlib import Path
from mathutils import Vector
root=Path(os.environ["SHAADI_ART_OUTPUT"])
root.mkdir(parents=True,exist_ok=True)
source=Path(bpy.data.filepath)
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
body=bpy.data.objects["SharmaAunty_MPFBBasemesh"]
rig=bpy.data.objects["SharmaAunty_53Bone_Rig"]
# Morphs are additive prototype action controls; they require art-direction review.
if not body.data.shape_keys:body.shape_key_add(name="Basis",from_mix=False)
names=[k.name for k in body.data.shape_keys.key_blocks]
controls={"Blink":0,"Smile":0,"JawOpen":0}
for name in controls:
 if name not in names:body.shape_key_add(name=name,from_mix=False)
keys=body.data.shape_keys.key_blocks
for index,v in enumerate(body.data.vertices):
 x,y,z=v.co
 if y>-0.09:continue
 def g(xc,zc,sx,sz):return math.exp(-((x-xc)/sx)**2-((z-zc)/sz)**2)
 if 1.405<z<1.52:
  eye=g(.075,1.435,.067,.033)+g(-.075,1.435,.067,.033)
  if eye>0.06:
   k=keys["Blink"].data[index]
   k.co.z-=0.0075*eye
   controls["Blink"]+=1
 if 1.20<z<1.40:
  smile=g(.10,1.289,.055,.040)+g(-.10,1.289,.055,.040)
  if smile>0.07:
   keys["Smile"].data[index].co.z+=0.009*smile
   controls["Smile"]+=1
  jaw=g(0,1.25,.15,.080)
  if jaw>0.10:
   keys["JawOpen"].data[index].co.z-=0.014*jaw
   controls["JawOpen"]+=1
assert all(v>0 for v in controls.values()),controls
# Persistent Blender actions: distinct readable movements, never static image substitution.
pose=rig.pose
bone_names={"head":"head","spine":"spine_03","left":"upperarm_l",
 "right":"upperarm_r","leg_l":"thigh_l","leg_r":"thigh_r"}
for n in bone_names.values():
 assert n in pose.bones,n
for b in pose.bones:b.rotation_mode="XYZ"
def pose_frame(frame,changes):
 for b in pose.bones:
  b.rotation_euler=(0,0,0)
 for name,xyz in changes.items():
  pose.bones[bone_names[name]].rotation_euler=xyz
 for n in bone_names.values():
  pose.bones[n].keyframe_insert(data_path="rotation_euler",frame=frame,group=n)
actions={
 "Idle":[(1,{}),(16,{"head":(.012,0,.018),"spine":(0,0,.014)}),(32,{"head":(-.012,0,-.02)}),(48,{})],
 "Walk":[(1,{"leg_l":(.22,0,0),"leg_r":(-.22,0,0),"left":(-.11,0,0),"right":(.11,0,0)}),
         (13,{"leg_l":(-.20,0,0),"leg_r":(.2,0,0),"left":(.11,0,0),"right":(-.11,0,0)}),
         (25,{"leg_l":(.22,0,0),"leg_r":(-.22,0,0),"left":(-.11,0,0),"right":(.11,0,0)})],
 "Question":[(1,{}),(12,{"head":(.04,0,-.15),"right":(-.30,.11,-.20)}),
             (30,{"head":(0,0,.13),"right":(-.25,-.12,.10)}),(48,{})],
 "DodgeReaction":[(1,{}),(7,{"spine":(.05,0,-.18),"head":(0,0,.12),"right":(-.30,0,0)}),
                 (18,{"spine":(-.04,0,.20),"head":(.06,0,-.15),"left":(-.20,0,0)}),
                 (36,{})]}
rig.animation_data_create()
for name,frames in actions.items():
 act=bpy.data.actions.new(name=name)
 act.use_fake_user=True
 rig.animation_data.action=act
 for frame,changes in frames:pose_frame(frame,changes)
 if name!="Idle":
  track=rig.animation_data.nla_tracks.new()
  track.name=name
  strip=track.strips.new(name,1,act)
  strip.mute=True
rig.animation_data.action=bpy.data.actions["Idle"]
for b in pose.bones:b.rotation_euler=(0,0,0)
bpy.context.scene.frame_set(1)
# Save in isolated art job output only. Approved baseline remains untouched.
dst=root/"sharma_aunty_art_rig_wip_v1.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
result={"status":"development_only","gate":"SAD-VISUAL-QUALITY-V1",
 "source_sha256":source_hash,"editable_blend":dst.name,
 "editable_sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),
 "morphs":controls,"actions":sorted(actions),
 "owner_approved":False,"visual_certified":False,"release_authorized":False}
(root/"art_pass_receipt.json").write_text(json.dumps(result,indent=2))
print("ART_WORKER_PASS",json.dumps(result),flush=True)
