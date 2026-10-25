import bpy,math,os
from math import sin,cos,pi
from mathutils import Vector
SRC=os.path.expanduser('~/shaadi-assets-approval-20261025/wedding-scene-master-v0.1.blend')
OUT=os.path.expanduser('~/shaadi-quality-v1-build-20261025')
bpy.ops.wm.open_mainfile(filepath=SRC)
sc=bpy.context.scene
C=bpy.data.collections.new('SAD_V1_GRAND_MANDAP_EDITORIAL_COUTURE');sc.collection.children.link(C)
def mat(n,c,metal=0,rough=.5,em=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF']
 p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if em:
  p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=em
 return m
rose=mat('Velvet_Pink',(.53,.022,.116),.1,.47)
saffron=mat('Golden_Marigold',(.96,.34,.035),0,.72)
carnation=mat('Cerise_Floral',(.79,.04,.27),0,.64)
ivory=mat('Mogra_Ivory',(.97,.78,.49),0,.67)
gold=mat('Embossed_Antique_Gold',(.75,.42,.12),.78,.23)
cream=mat('Silk_Drape_Ivory',(.83,.67,.46),.1,.46)
light=mat('Warm_Fairy_Lamp', (1,.64,.22),0,.26,12)
def mesh(name,coords,faces,ma):
 me=bpy.data.meshes.new(name);me.from_pydata(coords,[],faces);me.update()
 ob=bpy.data.objects.new(name,me);C.objects.link(ob);me.materials.append(ma)
 for f in me.polygons:f.use_smooth=True
 return ob
def curve(name,points,r,ma):
 pts=list(points);d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=3
 sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 ob=bpy.data.objects.new(name,d);C.objects.link(ob);d.materials.append(ma)
 return ob
def flower(x,y,z,scale=1,ma=None,normal=0):
 ma=ma or saffron
 V=[];F=[];petals=10
 for p in range(petals):
  a=2*pi*p/petals
  for t,r in [(0,.009),(.45,.074),(.8,.064),(1,.008)]:
   px=x+scale*r*cos(a);py=y+scale*r*sin(a);pz=z+scale*(.015+.046*sin(pi*t))
   V.append((px,py,pz))
  i=p*4;F.append((i,i+1,i+2,i+3))
 me=mesh('HandModeled_FloralBloom',V,F,ma);return me
# Flourishing canopy front lattice, florals rather than bland arch primitives.
for ypos in [-3.0,2.25,7.50,12.55]:
 for k in range(46):
  theta=pi*k/45
  x=2*cos(theta);z=4.0+1.11*sin(theta)
  flower(x,ypos-.22,z,.7,carnation if k%4==0 else saffron)
  if k%3==0:flower(x,ypos+.02,z-.125,.65,ivory)
  if k%5==0:curve('Hanging_Floral_Chain',[(x,ypos,z-.06-i*.09) for i in range(15)],.009,gold)
  if k%5==0:
   for j in range(0,14,2):flower(x,ypos,z-.07-.09*j,.36,saffron)
# Dancing silk curtains, drapery built as editable proper surface grids.
def drape(name,x,y,z,width,height,ma,phase=0):
 V=[];F=[];nx=36;nz=32
 for j in range(nz):
  v=j/(nz-1)
  for i in range(nx):
   u=i/(nx-1)
   xx=x+width*(u-.5)
   yy=y+.15*sin(6*pi*u+phase)*(.16+.84*v)
   zz=z-height*v+.12*sin(pi*u)*(1-v)
   V.append((xx,yy,zz))
 for j in range(nz-1):
  for i in range(nx-1):
   k=j*nx+i;F.append((k,k+1,k+1+nx,k+nx))
 ob=mesh(name,V,F,ma);so=ob.modifiers.new('Silk_Fabric_Thickness','SOLIDIFY');so.thickness=.013
 return ob
for y in [-3,2.25,7.5,12.5]:
 for x in [-2.0,2.0]:
  drape('GrandSatinSwag',(x+(.18 if x<0 else -.18)),y+.13,4.7,.88,3.55,rose if y in [-3,7.5] else cream,phase=x)
  curve('GoldCurtainTie',[(x-.2,y-.01,2.72),(x+.2,y-.01,2.70)],.018,gold)
# Delicate ornate mandap, lace rods and bead fringes.
for x in (-2.45,2.45):
 for y in (11.6,14.15):
  for a in range(7):
   theta=2*pi*a/7
   curve('Mandap_GoldFiligreePost',[(x+.105*cos(theta),y+.105*sin(theta),z) for z in [i*.16 for i in range(31)]],.004,gold)
for x in [i*.23-2.3 for i in range(21)]:
 for y in (11.65,14.0):
  curve('CanopyMograHanging',[(x,y,4.84),(x,y,4.20-.2*sin(x*2))],.004,gold)
  flower(x,y,4.20-.2*sin(x*2),.36,ivory)
# Carpet borders and path motifs — centreline stays unobstructed for dodge path.
for side in (-1,1):
 for y in [i*.65-4.1 for i in range(29)]:
  curve('Runner_Embroidery_Leaf',[(side*(1.17+.12*cos(t)),y+.13*sin(t),.080) for t in [pi*k/12 for k in range(13)]],.009,gold)
for y in [i*.84-3.8 for i in range(21)]:
 # understated intricate gold accent; actual collision path remains clear
 for side in (-1,1):
  x=side*1.03
  curve('ZariCarpet_Paisley',[(x+.055*cos(t),y+.12*sin(t),.077) for t in [2*pi*k/24 for k in range(25)]],.004,gold)
# Warm practical lamps and fairy string sources
for y in [-3.2,0.5,4.5,8.3,12.1]:
 curve('FestoonWire',[(x,y,5.7-.38*cos(x/6*pi)) for x in [i*.25-6 for i in range(49)]],.008,gold)
 for i in range(25):
  x=-6+i*.5
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.045,location=(x,y,5.7-.38*cos(x/6*pi)))
  ob=bpy.context.object;ob.name='Real_Festoon_Bulb';ob.data.materials.append(light)
 for side in (-1,1):
  x=side*1.8
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.09,location=(x,y,.43))
  bpy.context.object.name='Aisle_Lantern_Light';bpy.context.object.data.materials.append(light)
# floral urns frame the aisle without intruding into playable lane
for y in [-3.8,.2,4.1,8.1,11.8]:
 for side in (-1,1):
  x=side*2.36
  for j in range(11):
   a=j*2*pi/11
   flower(x+.19*cos(a),y+.18*sin(a),.78+.08*sin(j),.75,[carnation,saffron,ivory][j%3])
# Real editable lights and 9:16 mobile composition.
from mathutils import Vector
def camera(name,pos,target,ortho):
 cam=bpy.data.objects.get(name)
 if not cam:
  bpy.ops.object.camera_add(location=pos);cam=bpy.context.object;cam.name=name
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.data.type='ORTHO';cam.data.ortho_scale=ortho
 return cam
wide=camera('V1_GrandMandap_16by9',(9,-13,7),(0,6,2),17)
portrait=camera('V1_WeddingRunway_9by16',(0,-6,3.7),(0,7,1.65),8.3)
sc.render.engine='CYCLES';sc.cycles.samples=7
sc.cycles.use_denoising=False;sc.view_layers[0].cycles.use_denoising=False
sc.render.image_settings.file_format='JPEG';sc.render.image_settings.quality=83
sc.world.color=(.11,.062,.095)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/grand_wedding_scene_editable_v1_candidate.blend')
for cam,f,w,h in [(wide,'wedding_v1_wide.jpg',720,408),(portrait,'wedding_v1_phone.jpg',450,800)]:
 sc.camera=cam;sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.resolution_percentage=100
 sc.render.filepath=OUT+'/'+f;bpy.ops.render.render(write_still=True)
print('CANDIDATE_WEDDING',len(bpy.data.objects),'objects',len(C.objects),'couture objects',flush=True)

