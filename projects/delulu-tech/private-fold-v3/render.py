"""Private Blender 4.0.2 five-frame *concept* — actual two-sided ribbon mesh, not production logo.
Owner frozen SVG is never edited. Stage-5 geometry is a dimensional study, NOT yet identical
to the frozen 'Impossible Ribbon' mark; separate creative and independent QA required.
"""
import bpy,math,sys,json,hashlib,os,time
from pathlib import Path
from mathutils import Vector
ROOT=Path.home()/".local/share/matrix-code-executor/delulu_tech"
OUT=ROOT/"private-fold-v3"
ORIGINAL=Path("/var/lib/generic-linux-automator-exec/delulu-site-v2-20261025/projects/delulu-tech/brand/assets/delulu-tech-mobile-white.svg")
APPROVED="d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368"
if not ORIGINAL.is_file() or hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()!=APPROVED:raise RuntimeError("frozen_svg_sha_drift")
OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def temp():
 p=Path("/sys/class/thermal/thermal_zone0/temp")
 return round(int(p.read_text())/1000,2) if p.exists() else None
def thermal_gate():
 t=temp()
 if t is not None and t>73:raise RuntimeError("thermal_hold_73C")
 return t
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine="BLENDER_EEVEE"
sc.cycles.samples=12
sc.render.resolution_x=720;sc.render.resolution_y=405;sc.render.resolution_percentage=100
sc.render.image_settings.file_format="PNG"
sc.render.film_transparent=False
sc.world.color=(.015,.018,.03)
# Scene backdrop uses frozen midnight ink.
def material(name,color,metallic=0,roughness=.32):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get("Principled BSDF")
 p.inputs["Base Color"].default_value=(*color,1)
 p.inputs["Metallic"].default_value=metallic;p.inputs["Roughness"].default_value=roughness
 return m
white=material("Soft White Front",(.91,.93,.87),.20,.3)
back=material("Electric Violet Back",(.23,.13,.64),.26,.38)
edge=material("Graphite Edges",(.07,.08,.12),.14,.48)
ground=material("Midnight Ink",(.043,.052,.075),0,.8)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-2.1))
base=bpy.context.object;base.name="Black Stage";base.data.materials.append(ground)
def light(name,location,power,color,size):
 data=bpy.data.lights.new(name,"AREA");data.energy=power;data.color=color;data.shape="DISK";data.size=size
 obj=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(obj);obj.location=location
 obj.rotation_euler=(Vector((0,0,0))-obj.location).to_track_quat("-Z","Y").to_euler()
light("Soft White",(-5,-4,8),550,(.97,.96,1),6)
light("Violet Rim",(4,5,4),520,(.4,.18,1),4)
light("Lime Accent",(1,-7,2),120,(.78,1,.24),3)
cam_data=bpy.data.cameras.new("Perspective Camera")
cam=bpy.data.objects.new("Perspective Camera",cam_data);bpy.context.collection.objects.link(cam)
cam.location=(7,-12,7);cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat("-Z","Y").to_euler()
cam_data.type="ORTHO";cam_data.ortho_scale=11;sc.camera=cam
N=90;M=8
def point(s,u,phase):
 a=phase/4.
 theta=(2.45*math.pi*s+.85*math.sin(s*math.pi*3))*a
 # Physical crossing/loop appears in later stages, actual depth and self occlusion.
 straight=Vector(((s-.5)*7.1,0,0))
 curve=Vector((3.0*math.sin(2*math.pi*s+0.20),2.0*math.cos(2*math.pi*s+0.20),.68*math.sin(4*math.pi*s)))
 blend=min(1,max(0,(phase-0.7)/2.8))
 center=straight.lerp(curve,blend)
 center.z+=.35*math.sin(5*math.pi*s)*a
 width=Vector((.12*a*math.sin(2*math.pi*s),math.cos(theta),math.sin(theta)))
 return center+width*u
def make_ribbon(phase):
 centers=[[point(i/N,(j/M-.5)*1.10,phase) for j in range(M+1)] for i in range(N+1)]
 vertices=[x.copy() for row in centers for x in row]
 # Each side is a physically different layer, with thickness. Backface is not a texture trick.
 vec=Vector((0,0,.045))
 vertices +=[x-vec for x in vertices]
 surface=(N+1)*(M+1);faces=[];matids=[]
 for i in range(N):
  for j in range(M):
   a=i*(M+1)+j;b=a+1;c=a+(M+1);d=c+1
   faces.append((a,c,d,b));matids.append(0)
   faces.append((surface+b,surface+d,surface+c,surface+a));matids.append(1)
 for i in range(N):
  for j in (0,M):
   a=i*(M+1)+j;b=(i+1)*(M+1)+j
   faces.append((a,b,surface+b,surface+a));matids.append(2)
 for i in (0,N):
  for j in range(M):
   a=i*(M+1)+j;b=a+1
   faces.append((a,b,surface+b,surface+a));matids.append(2)
 mesh=bpy.data.meshes.new("actual_front_back_fold_mesh")
 mesh.from_pydata([tuple(x) for x in vertices],[],faces);mesh.update()
 ob=bpy.data.objects.new("Physical Two Sided Impossible Ribbon Study",mesh)
 bpy.context.collection.objects.link(ob)
 for mat in (white,back,edge):ob.data.materials.append(mat)
 for face,idx in zip(mesh.polygons,matids):face.material_index=idx;face.use_smooth=True
 return ob,vertices,faces,matids
phases=["01_entry","02_first_twist","03_crossing","04_depth_climax","05_settled_study"]
receipts=[]
for idx,name in enumerate(phases):
 t=thermal_gate()
 mesh,verts,faces,mats=make_ribbon(idx)
 path=OUT/(name+".png");sc.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 frame={"name":name,"sha256":sha(path),"vertices":len(verts),"faces":len(faces),
        "front_faces":mats.count(0),"back_faces":mats.count(1),"side_faces":mats.count(2),
        "distinct_depth_values":len(set(round(p.z,3) for p in verts)),
        "thermal_c":t,"type":"physical_ribbon_concept_not_owner_approved"}
 receips=json.dumps(frame,sort_keys=True)
 receipts.append(frame)
 if idx!=4:bpy.data.objects.remove(mesh,do_unlink=True)
thermal_gate()
scene=OUT/"private_fold_scene.blend";bpy.ops.wm.save_as_mainfile(filepath=str(scene))
out={"status":"private_review_only","frozen_logo_sha256":APPROVED,"geometry_derived_from_frozen_svg":False,
     "does_not_claim_exact_logo_equivalence":True,"blender_version":bpy.app.version_string,
     "scene_sha256":sha(scene),"frames":receipts,"release_authorized":False,"owner_accepted":False}
p=OUT/"render_evidence.json";p.write_text(json.dumps(out,indent=2)+"\n")
print("FINAL_RENDER_RECEIPT "+json.dumps({"scene":str(scene),"evidence":str(p),"frames":len(receipts),"scene_sha256":out["scene_sha256"]}))
