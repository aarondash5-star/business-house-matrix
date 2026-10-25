"""Delulu V4 PRIVATE: original frozen SVG vector letters physically deform as keyframed 3D surfaces.
No alpha masking, no logo replacement, no release. Blender 4.0.2.
"""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector
SVG=Path("/var/lib/generic-linux-automator-exec/delulu-site-v2-20261025/projects/delulu-tech/brand/assets/delulu-tech-mobile-white.svg")
SHA="d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368"
OUT=Path.home()/".local/share/matrix-code-executor/delulu_tech/private-fold-v4"
assert SVG.is_file() and hashlib.sha256(SVG.read_bytes()).hexdigest()==SHA,"frozen_logo_mismatch"
OUT.mkdir(parents=True,exist_ok=True)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def thermal():
 p=Path("/sys/class/thermal/thermal_zone0/temp")
 t=int(p.read_text())/1000 if p.is_file() else None
 if t is not None and t>73:raise RuntimeError("thermal_hold_73c")
 return t
def material(name,rgba,metal=0,rough=.5):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgba,1);m.use_nodes=True
 b=m.node_tree.nodes.get("Principled BSDF");b.inputs["Base Color"].default_value=(*rgba,1)
 b.inputs["Metallic"].default_value=metal;b.inputs["Roughness"].default_value=rough
 return m
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine="BLENDER_EEVEE"
sc.render.resolution_x=800;sc.render.resolution_y=440;sc.render.resolution_percentage=100
sc.render.image_settings.file_format="PNG";sc.render.film_transparent=False
sc.render.fps=12;sc.frame_start=1;sc.frame_end=49
sc.render.image_settings.color_mode="RGBA"
sc.world.color=(.012,.013,.027)
front=material("Unchanged white logo surface",(.95,.95,.94),.15,.42)
rear=material("Visible violet reverse",(.28,.16,.68),.20,.34)
side=material("Dark silver physical edge",(.24,.27,.34),.20,.42)
floor=material("Night ink background",(.021,.026,.046),0,.89)
bpy.ops.import_curve.svg(filepath=str(SVG))
curves=[o for o in bpy.context.scene.objects if o.type=="CURVE"]
if len(curves)!=2:raise RuntimeError("unexpected_svg_path_count")
meshes=[]
for i,o in enumerate(curves):
 o.data.dimensions="2D";o.data.fill_mode="BOTH"
 o.data.extrude=.0018;o.data.bevel_depth=.00010;o.data.bevel_resolution=1
 bpy.ops.object.select_all(action="DESELECT");o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.convert(target="MESH")
 o=bpy.context.view_layer.objects.active
 o.name=f"Frozen SVG Physical Path {i+1}"
 o.data.materials.clear()
 for m in (front,rear,side):o.data.materials.append(m)
 for polygon in o.data.polygons:
  polygon.material_index=0 if polygon.normal.z>.6 else (1 if polygon.normal.z<-.6 else 2)
 meshes.append(o)
bounds=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
xmin=min(v.x for v in bounds);xmax=max(v.x for v in bounds)
ymin=min(v.y for v in bounds);ymax=max(v.y for v in bounds)
cx=(xmin+xmax)/2;cy=(ymin+ymax)/2;width=xmax-xmin;height=ymax-ymin
if width<.15 or height<.04:raise RuntimeError("imported_svg_bad_bounds")
# Shape keys contain *genuine vertices*, including the original letterfront, back and edges.
def deform(world,phase):
 u=(world.x-xmin)/width;v=(world.y-ymin)/height
 k=phase/3
 twist=(1-k)*math.sin(5.2*math.pi*u+v*math.pi*1.6)
 crease=abs(math.sin(3.2*math.pi*u))**2
 z=width*((.095*(1-k))*twist+.052*(1-k)*crease)
 z+=width*(v-.50)*(.13*(1-k))*math.sin(7*math.pi*u)
 xshift=width*(.042*(1-k))*math.sin(4*math.pi*u+v*math.pi)
 yshift=height*(.18*(1-k))*math.sin(3*math.pi*u)
 # folded surfaces remain recognizably linked to every imported original SVG vertex
 return Vector((world.x+xshift,world.y+yshift,world.z+z))
names=["Early Twist","Crossing Folds","Reversing Fold","Near Settled"]
timeline=[1,13,25,37,49]
for obj in meshes:
 original=[(obj.matrix_world@v.co).copy() for v in obj.data.vertices]
 obj.shape_key_add(name="Frozen Original",from_mix=False)
 inv=obj.matrix_world.inverted_safe()
 for stage,name in enumerate(names):
  sk=obj.shape_key_add(name=name,from_mix=False)
  for point,world in zip(sk.data,original):
   point.co=inv@deform(world,stage)
 for f in timeline:
  obj.data.shape_keys.key_blocks[0].value if False else None
  sc.frame_set(f)
  for stage,name in enumerate(names):
   sk=obj.data.shape_keys.key_blocks[name]
   sk.value=float((f!=49) and (stage==timeline.index(f)))
   sk.keyframe_insert(data_path="value",frame=f)
 for key in obj.data.shape_keys.key_blocks:
  if key.name=="Frozen Original":continue
  if not obj.data.shape_keys.animation_data or not obj.data.shape_keys.animation_data.action:
   raise RuntimeError("missing_shape_key_animation")
# Camera straight-on to preserve exact SVG planar geometry in final frame.
cam=bpy.data.cameras.new("Logo Truth Camera");c=bpy.data.objects.new("Logo Truth Camera",cam)
bpy.context.collection.objects.link(c);c.location=(cx,cy,2);c.rotation_euler=(0,0,0)
cam.type="ORTHO";cam.ortho_scale=width*1.14;sc.camera=c
for name,loc,power,color,size in [
 ("Neutral Key",(cx-width*.28,cy+height*.7,.65),90,(1,1,1),.34),
 ("Violet Edge",(cx+width*.24,cy-height*.4,.5),110,(.6,.38,1),.26)]:
 ld=bpy.data.lights.new(name,"AREA");ld.energy=power;ld.shape="DISK";ld.size=size;ld.color=color
 l=bpy.data.objects.new(name,ld);bpy.context.collection.objects.link(l);l.location=loc
 l.rotation_euler=(Vector((cx,cy,0))-l.location).to_track_quat("-Z","Y").to_euler()
bpy.ops.mesh.primitive_plane_add(size=10,location=(cx,cy,-.35))
bg=bpy.context.object;bg.name="Private Black Canvas";bg.data.materials.append(floor)
sc.view_settings.view_transform="Standard"
sc.view_settings.look="Medium High Contrast"
receipts=[]
for name,f in zip(["01_folds","02_crossing","03_reverse","04_settling","05_frozen_exact_vector"],timeline):
 t=thermal();sc.frame_set(f);sc.render.filepath=str(OUT/(name+".png"))
 bpy.ops.render.render(write_still=True)
 receipts.append({"frame":f,"label":name,"sha256":digest(sc.render.filepath),"thermal_c":t})
sc.frame_set(49)
scene=OUT/"logo_vector_keyframed.blend";bpy.ops.wm.save_as_mainfile(filepath=str(scene))
fc=sum(len(o.data.shape_keys.animation_data.action.fcurves) for o in meshes)
if fc<8:raise RuntimeError("shape_key_animation_not_saved")
receipt={"stage":"private_review_only","frozen_svg_sha256":SHA,
"source_is_actual_svg_mesh":True,"exact_final_vertex_basis":True,"materials":["front white","back violet","side metal"],
"object_count":len(meshes),"total_vertices":sum(len(o.data.vertices) for o in meshes),
"shape_key_fcurves":fc,"frame_range":[1,49],"fps":12,
"scene_sha256":digest(scene),"frames":receipts,
"animation_mp4":False,"owner_approved":False,"independent_review":False,"release_authorized":False}
(OUT/"vector_animation_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print("VECTOR_ANIMATION_RECEIPT "+json.dumps(receipt))
