import bpy,math,os
from math import sin,cos,pi
from mathutils import kdtree
S=os.path.expanduser('~/shaadi-assets-approval-20261025/sharma-aunty-master-v0.1.blend')
O=os.path.expanduser('~/shaadi-quality-v1-build-20261025')
bpy.ops.wm.open_mainfile(filepath=S)
bad=('Scalp_Hair','Side_Hair','Eye_Ivory','Eye_Pupil','Glasses_','SilkBlouse','Jhumka_Pearl','Gold_Earring','Back_Bun','Wrapped_Bun','Red_Bindi','Nose_Pin','Wedding_Necklace','Pallu_')
for o in list(bpy.data.objects):
 if o.name.startswith(bad):bpy.data.objects.remove(o,do_unlink=True)
h=bpy.data.objects['SharmaAunty_MPFBBasemesh'];rig=bpy.data.objects['SharmaAunty_53Bone_Rig']
C=bpy.data.collections.new('SAD_V1_COUTURE_EDITABLE');bpy.context.scene.collection.children.link(C)
def mat(n,col,met=0,rough=.42,sss=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=met;p.inputs['Roughness'].default_value=rough
 p.inputs['Subsurface Weight'].default_value=sss
 return m
skin=mat('Warm_Skin_PBR',(.63,.35,.24),0,.5,.15)
blouse=mat('Raspberry_Blouse_PBR',(.54,.035,.17),.14,.31)
silk=mat('Raspberry_Saree_Silk',(.6,.035,.17),.16,.35)
saffron=mat('Coral_Saffron_Brocade',(.93,.29,.13),.17,.34)
gold=mat('Antique_Gold_Zari',(.76,.44,.14),.78,.24)
hair=mat('Soft_Obsidian_Hair',(.044,.024,.028),.08,.34)
jasmine=mat('Jasmine_Petals',(.97,.88,.72),0,.42)
ruby=mat('Bindi_Ruby',(.55,.004,.05),.31,.13)
frames=mat('Tortoiseshell_Glasses',(.13,.06,.043),.18,.25)
h.data.materials.clear();h.data.materials.append(skin);h.data.materials.append(blouse)
for f in h.data.polygons:
 c=f.center;f.material_index=1 if 1.03<c.z<1.27 and abs(c.x)<.31 else 0
n=skin.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=130
b=skin.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.06;b.inputs['Distance'].default_value=.02
skin.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);skin.node_tree.links.new(b.outputs['Normal'],skin.node_tree.nodes['Principled BSDF'].inputs['Normal'])
for m in (blouse,silk,saffron):
 nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes['Principled BSDF']
 w=nodes.new('ShaderNodeTexWave');w.inputs['Scale'].default_value=34
 b=nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.075;b.inputs['Distance'].default_value=.006
 links.new(w.outputs['Color'],b.inputs['Height']);links.new(b.outputs['Normal'],p.inputs['Normal'])
o=bpy.data.objects['Pleated_Saree_Skirt'];o.data.materials.clear();o.data.materials.append(silk)
def arm(o):
 if o.type=='MESH' and not any(m.type=='ARMATURE' for m in o.modifiers):
  m=o.modifiers.new('SKINNED_TO_EDITABLE_BODY_RIG','ARMATURE');m.object=rig
arm(o)
def sphere(n,p,sc,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=p)
 o=bpy.context.object;o.name=n;o.scale=sc;o.data.materials.append(m)
 for f in o.data.polygons:f.use_smooth=True
 for col in list(o.users_collection):col.objects.unlink(o)
 C.objects.link(o);return o
def curve(n,pts,r,m):
 pts=list(pts)
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3
 sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for a,v in zip(sp.points,pts):a.co=(*v,1)
 o=bpy.data.objects.new(n,cu);C.objects.link(o);cu.materials.append(m);return o
# Couture pallu, dense editable cloth and transferred MPFB skinning.
V=[];F=[];R=35;N=22
for j in range(R):
 t=j/(R-1);z=1.35-1.11*t;cx=-.20+.34*t;cy=-.24+.028*sin(pi*t)
 for i in range(N):
  u=i/(N-1)-.5
  V.append((cx+(.28+.035*sin(2*pi*t))*u,cy+.014*sin(8*pi*u+3*pi*t),z+.009*sin(4*pi*u)))
for j in range(R-1):
 for i in range(N-1):
  x=j*N+i;F.append((x,x+1,x+N+1,x+N))
me=bpy.data.meshes.new('Pallu_Editable_Topology');me.from_pydata(V,[],F);me.update()
p=bpy.data.objects.new('Sari_Pallu_Skinned_Cloth',me);C.objects.link(p);me.materials.append(saffron)
sol=p.modifiers.new('Cloth_Solidify','SOLIDIFY');sol.thickness=.005
for f in me.polygons:f.use_smooth=True
kd=kdtree.KDTree(len(h.data.vertices))
for i,v in enumerate(h.data.vertices):kd.insert(v.co,i)
kd.balance()
for v in p.data.vertices:
 _,idx,_=kd.find(v.co)
 for g in h.data.vertices[idx].groups:
  name=h.vertex_groups[g.group].name
  vg=p.vertex_groups.get(name) or p.vertex_groups.new(name=name)
  vg.add([v.index],g.weight,'REPLACE')
arm(p)
for i in (0,N-1):curve('Pallu_Woven_Gold_Edge',[V[j*N+i] for j in range(R)],.007,gold)
for j in range(2,R-2,3):
 for i in range(3,N-3,3):
  x,y,z=V[j*N+i]
  curve('Gold_Zari_Motif',[(x+.009*cos(a),y-.003,z+.012*sin(a)) for a in [2*pi*k/12 for k in range(13)]],.0018,gold)
# The old balloon wig and fake cartoon googly eyeballs are explicitly deleted.
sphere('Hair_Crown_Mesh',(0,.053,1.49),(.145,.121,.071),hair)
sphere('Coiled_Low_Bun',(0,.14,1.435),(.101,.084,.099),hair)
for j in range(23):
 x=-.13+.26*(j+.5)/23
 curve('Swept_Hair_Strands',[(x*.17,-.007,1.555),(.5*x,-.028,1.535),(x,-.008,1.493),(.74*x,.076,1.461)],.001,hair)
for j in range(22):
 a=2*pi*j/22;x=.102*cos(a);y=.176+.04*sin(a);z=1.435+.106*sin(a)
 for k in range(5):
  q=2*pi*k/5
  sphere('Individual_Jasmine_Petal',(x+.009*cos(q),y,z+.012*sin(q)),(.011,.006,.013),jasmine)
# Glasses now track the underlying real face eyes instead of floating above them.
for sign in (-1,1):
 x=sign*.073;y=-.229;z=1.39
 curve('Rim_Tortoise',( (x+.06*cos(a),y,z+.035*sin(a)) for a in [2*pi*i/30 for i in range(31)] ),.0035,frames)
 curve('Temple_Sidearm',[(sign*.134,y,z),(sign*.163,-.13,z+.015)],.003,frames)
curve('Nose_Glasses_Bridge',[(-.014,-.23,1.40),(.014,-.23,1.40)],.0035,frames)
sphere('Bindi_RealGem',(0,-.239,1.466),(.012,.005,.015),ruby)
for sign in (-1,1):
 sphere('Jhumka_Earrings',(sign*.156,-.046,1.307),(.029,.025,.044),gold)
 for i in range(8):
  a=2*pi*i/8
  sphere('Jhumka_Bells',(sign*.156+.023*cos(a),-.047,1.277+.012*sin(a)),(.006,.006,.006),jasmine)
curve('Gold_Mangalsutra',[(.15*cos(a),-.12-.047*sin(a),1.19-.075*sin(a)) for a in [pi*i/32 for i in range(33)]],.005,gold)
sphere('Gold_Heart_Pendant',(0,-.179,1.107),(.034,.012,.044),gold)
sphere('Ruby_In_Pendant',(0,-.193,1.104),(.016,.004,.02),ruby)
# Dedicated morph controls for actual face mesh; retain all MPFB base shapekeys.
for name,mode in [('SAD_Amused','smile'),('SAD_Alarmed','surprise'),('SAD_Disapproval','frown')]:
 sk=h.shape_key_add(name=name,from_mix=False)
 for i,v in enumerate(h.data.vertices):
  x,y,z=v.co
  if y<-.11:
   if mode=='smile' and 1.25<z<1.33 and .03<abs(x)<.1:sk.data[i].co.z+=.012
   if mode=='surprise' and 1.25<z<1.32 and abs(x)<.065:sk.data[i].co.z-=.008
   if mode=='frown' and 1.345<z<1.43 and .035<abs(x)<.12:sk.data[i].co.z-=.008
 sk.value=0
rig['quality_gate']='SAD-VISUAL-QUALITY-V1';rig['status']='UNCERTIFIED_OWNER_REVIEW_CANDIDATE'
rig['source']='MPFB2 base rig with original editable couture and expression modifications'
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=9;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=85
s.cycles.use_denoising=False; s.view_layers[0].cycles.use_denoising=False
s.render.resolution_x=560;s.render.resolution_y=780;s.render.resolution_percentage=100;s.view_settings.exposure=.15
bpy.ops.wm.save_as_mainfile(filepath=O+'/sharma_aunty_editable_v1_candidate.blend')
for cam,out in [('FULL_BODY','sharma_v1_full.jpg'),('PORTRAIT','sharma_v1_face.jpg')]:
 s.camera=bpy.data.objects[cam];s.render.filepath=O+'/'+out;bpy.ops.render.render(write_still=True)
print('CANDIDATE_RIG',len(rig.data.bones),len(h.data.vertices),len(h.data.shape_keys.key_blocks),len(p.vertex_groups),flush=True)

