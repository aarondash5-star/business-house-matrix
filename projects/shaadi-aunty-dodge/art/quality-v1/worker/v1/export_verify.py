"""QA-only export of an unapproved Blender WIP and glTF JSON inspection."""
import bpy,hashlib,json,os,struct
from pathlib import Path
out=Path(os.environ["SHAADI_ART_OUTPUT"])
out.mkdir(parents=True,exist_ok=True)
glb=out/"sharma_aunty_art_rig_wip_v1.glb"
bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",
 export_animations=True,export_animation_mode='ACTIONS',
 export_skins=True,export_morph=True,export_cameras=False,export_lights=False)
data=glb.read_bytes()
assert data[:4]==b'glTF'
assert len(data)>10000
json_chunk_length=struct.unpack_from("<I",data,12)[0]
assert data[16:20]==b'JSON'
g=json.loads(data[20:20+json_chunk_length])
animations=[x.get('name','') for x in g.get('animations',[])]
morphs=[]
for mesh in g.get('meshes',[]):
 morphs.extend(mesh.get('extras',{}).get('targetNames',[]))
for mesh in g.get('meshes',[]):
 for prim in mesh.get('primitives',[]):
  if prim.get('targets') and not mesh.get('extras',{}).get('targetNames'):
   morphs.append("unnamed_targets_present")
check={
 'glb_sha256':hashlib.sha256(data).hexdigest(),
 'bytes':len(data),'animations':animations,
 'morph_target_names':sorted(set(morphs)),
 'required_actions':['Idle','Walk','Question','DodgeReaction'],
 'required_morphs':['Blink','Smile','JawOpen'],
 'actions_complete':all(x in animations for x in ['Idle','Walk','Question','DodgeReaction']),
 'morphs_complete':all(x in morphs for x in ['Blink','Smile','JawOpen']),
 'visual_certified':False,'owner_approved':False,
 'release_authorized':False}
(out/'export_qa.json').write_text(json.dumps(check,indent=2))
print("ART_EXPORT_QA",json.dumps(check),flush=True)
