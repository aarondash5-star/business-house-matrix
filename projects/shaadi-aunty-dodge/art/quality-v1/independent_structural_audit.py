import bpy,os,json,hashlib,sys
from datetime import datetime,timezone
R=os.path.expanduser('~/shaadi-quality-v1-build-20261025')
files={'character':R+'/sharma_aunty_editable_v1_candidate.blend','wedding':R+'/grand_wedding_scene_editable_v1_candidate.blend'}
out={'gate':'SAD-VISUAL-QUALITY-V1','timestamp_utc':datetime.now(timezone.utc).isoformat(),
 'source_qa':'INDEPENDENT_MECHANICAL_TEST','creative_qa':'FAIL_NOT_REFERENCE_MATCH',
 'owner_approval':False,'release_allowed':False,'candidates':{}}
for kind,file in files.items():
 bpy.ops.wm.open_mainfile(filepath=file)
 checks={}
 def check(name,good,detail):checks[name]={'pass':bool(good),'detail':detail}
 if kind=='character':
  h=bpy.data.objects.get('SharmaAunty_MPFBBasemesh')
  rig=bpy.data.objects.get('SharmaAunty_53Bone_Rig')
  cloth=bpy.data.objects.get('Sari_Pallu_Skinned_Cloth')
  check('body_is_real_editable_mesh',h is not None and h.type=='MESH' and len(h.data.vertices)>18000,
   f"{len(h.data.vertices) if h else 0} vertices")
  check('armature_editable',rig is not None and rig.type=='ARMATURE' and len(rig.data.bones)>=53,
   f"{len(rig.data.bones) if rig else 0} bones")
  check('pallu_has_skin_weights',cloth is not None and len(cloth.vertex_groups)>8,
   f"{len(cloth.vertex_groups) if cloth else 0} weighted groups")
  check('pallu_deformer',cloth is not None and any(m.type=='ARMATURE' and m.object==rig for m in cloth.modifiers),
   'Required armature modifier')
  keys=[k.name for k in h.data.shape_keys.key_blocks] if h and h.data.shape_keys else []
  check('expression_geometry_available',all(k in keys for k in ('SAD_Amused','SAD_Alarmed','SAD_Disapproval')),
   str(len(keys))+' total shape keys')
  check('eye_aim_blink',False,'Dedicated eyelid/blink and eye aim animation unverified')
  check('garment_deforms_without_clipping',False,'No posed cloth collision validation')
  check('facial_likeness',False,'Reference face and mature silhouette visibly not matched')
 else:
  cols=bpy.data.collections
  check('scene_editable', 'SAD_V1_GRAND_MANDAP_EDITORIAL_COUTURE' in cols,
   f"{len(bpy.data.objects)} separate scene objects")
  check('both_cameras_present',all(c in bpy.data.objects for c in ('V1_GrandMandap_16by9','V1_WeddingRunway_9by16')),
   'Native wide and portrait cameras')
  check('flower_geometry',sum('HandModeled_FloralBloom' in o.name for o in bpy.data.objects)>100,'Modular flower meshes')
  check('palace_architecture_fidelity',False,'Approved Indian palatial venue not recreated')
  check('real_mobile_runtime_parity',False,'Interactive Three.js captures unverified')
 check('provenance_complete',False,'Upstream URLs and hashes for each component not fully reconciled')
 checks_passed=sum(c['pass'] for c in checks.values())
 out['candidates'][kind]={'file':os.path.basename(file),'sha256':hashlib.sha256(open(file,'rb').read()).hexdigest(),
 'bytes':os.path.getsize(file),'checks':checks,'passed':checks_passed,'total':len(checks),'certified':False}
with open(R+'/qa_independent_structural.json','w') as f:json.dump(out,f,indent=2)
print('CERTIFICATION_WITHHELD')
for k,v in out['candidates'].items():print(k,v['passed'],'/',v['total'],'mechanical checks; visual FAIL')
