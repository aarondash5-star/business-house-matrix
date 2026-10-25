from pathlib import Path
p=Path('/var/lib/generic-linux-automator-exec/shaadi-three-premium-slice-20261025/src/scene.js')
s=p.read_text()
old=""" for(let n=0;n<9;n++){
   const z=4-n*6;
   for(const side of [-1,1]){
     cylinder(.21,.29,5.8,color(0x512641,.16,.56),[side*3.5,2.9,z],scene);
     const lantern=ball(.34,mats.gold,[side*3.5,4.7,z],scene,[.8,1.2,.8]);
     lantern.castShadow=false;
   }
   const bar=box(7.1,.17,.2,mats.gold,[0,5.75,z],scene);
   bar.castShadow=false;
   for(let j=-3;j<=3;j++) {
     const garland=ball(.14,(j%2)?mats.pink:mats.gold,[j,5.55-.28*(1-Math.abs(j/3)),z],scene,[1.5,.65,1.1]);
     garland.castShadow=false;
   }
 }
"""
new=""" // One draw call per repeated motif. Avoid >150 individual wedding arch meshes.
 function instances(geometry,material,positions,scale=[1,1,1],shadows=false){
   const m=new THREE.InstancedMesh(geometry,material,positions.length);
   const dummy=new THREE.Object3D();
   positions.forEach((p,i)=>{dummy.position.set(...p);dummy.scale.set(...scale);dummy.updateMatrix();m.setMatrixAt(i,dummy.matrix);});
   m.instanceMatrix.needsUpdate=true;m.castShadow=shadows;m.receiveShadow=shadows;scene.add(m);return m;
 }
 const columns=[],lanterns=[],bars=[],flowersGold=[],flowersPink=[];
 for(let n=0;n<9;n++){
   const z=4-n*6;
   for(const side of [-1,1]){
     columns.push([side*3.5,2.9,z]);lanterns.push([side*3.5,4.7,z]);
   }
   bars.push([0,5.75,z]);
   for(let j=-3;j<=3;j++){
     (j%2?flowersPink:flowersGold).push([j,5.55-.28*(1-Math.abs(j/3)),z]);
   }
 }
 instances(new THREE.CylinderGeometry(.21,.29,5.8,16),color(0x512641,.16,.56),columns);
 instances(new THREE.SphereGeometry(.34,12,8),mats.gold,lanterns,[.8,1.2,.8]);
 instances(new THREE.BoxGeometry(7.1,.17,.2),mats.gold,bars);
 const flowerGeo=new THREE.SphereGeometry(.14,8,6);
 instances(flowerGeo,mats.gold,flowersGold,[1.5,.65,1.1]);
 instances(flowerGeo,mats.pink,flowersPink,[1.5,.65,1.1]);
"""
assert s.count(old)==1,('ANCHOR_DRIFT',s.count(old))
p.write_text(s.replace(old,new))
print('INSTANCED_ARCH_PATCH_APPLIED',p,'bytes',p.stat().st_size)

