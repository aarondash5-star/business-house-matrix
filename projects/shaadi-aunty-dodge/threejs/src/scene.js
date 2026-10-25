import * as THREE from 'three';
import {inspectCharacterGLTF} from './artContract.js';
import {auntyPosition,limit} from './simulation.js';
const V=(x,y,z)=>new THREE.Vector3(x,y,z);
const color=(v,metalness=0,roughness=0.75)=>new THREE.MeshStandardMaterial({color:v,metalness,roughness});
const mats={
  gold:color(0xf7be68,.45,.26),pink:color(0xe9509e,.15,.55),wine:color(0x80244d,.18,.55),
  ivory:color(0xffedd7,.08,.66),skin:color(0xc68e66,.05,.75),hair:color(0x210e26,.2,.65),
  jewel:color(0xffdc72,.55,.15),eye:color(0x211522),rose:color(0xd73974,.2,.35)
};
function mesh(geo,mat,xyz,parent,scale){
  const m=new THREE.Mesh(geo,mat);m.position.set(...xyz);if(scale)m.scale.set(...scale);
  m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function ball(r,mat,pos,parent,scale){return mesh(new THREE.SphereGeometry(r,18,12),mat,pos,parent,scale);}
function box(a,b,c,mat,pos,parent){return mesh(new THREE.BoxGeometry(a,b,c),mat,pos,parent);}
function cylinder(rt,rb,h,mat,pos,parent){return mesh(new THREE.CylinderGeometry(rt,rb,h,20),mat,pos,parent);}
function torus(r,t,mat,pos,parent){return mesh(new THREE.TorusGeometry(r,t,8,22),mat,pos,parent);}

export function createWeddingScene(renderer){
 const scene=new THREE.Scene();
 scene.background=new THREE.Color(0x28162d);scene.fog=new THREE.FogExp2(0x2a1739,.026);
 const camera=new THREE.PerspectiveCamera(48,1,.08,80);
 scene.add(new THREE.HemisphereLight(0xffdbb8,0x63437e,2.0));
 const key=new THREE.DirectionalLight(0xffeccb,3.3);key.position.set(-4,10,8);scene.add(key);
 key.castShadow=true;key.shadow.mapSize.set(512,512);key.shadow.camera.left=-12;
 key.shadow.camera.right=12;key.shadow.camera.top=14;key.shadow.camera.bottom=-14;
 scene.add(new THREE.AmbientLight(0xffffff,.3));
 const point=new THREE.PointLight(0xff7c84,65,20,2);point.position.set(4,4,-3);scene.add(point);
 const floor=box(13,.2,57,color(0x2b1d3b),[0,-.14,-16],scene);floor.receiveShadow=true;
 const carpet=box(5,.045,55,color(0x9d175d,.05,.8),[0,0,-15],scene);carpet.receiveShadow=true;
 for(const edge of [-2.43,2.43])box(.075,.025,53,mats.gold,[edge,.05,-15],scene);
 for(let n=0;n<17;n++){
   const z=3-n*3.15;
   for(const x of [-.8,.8]){const shape=ball(.062,mats.jewel,[x,.065,z],scene);shape.castShadow=false;}
 }
 // One draw call per repeated motif. Avoid >150 individual wedding arch meshes.
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
 const particles=new THREE.InstancedMesh(new THREE.SphereGeometry(.055,6,5),mats.rose,150);
 const dummy=new THREE.Object3D();
 for(let i=0;i<150;i++){
   const side=(i%2)?1:-1;
   const x=side*(2.7+(i*37%17)/19);const y=.08+(i*17%11)/12;const z=5-(i*13%70)*.7;
   dummy.position.set(x,y,z);dummy.scale.set(1,.55,1);dummy.updateMatrix();particles.setMatrixAt(i,dummy.matrix);
 }
 particles.instanceMatrix.needsUpdate=true;scene.add(particles);

 const player=new THREE.Group();scene.add(player);
 cylinder(.36,.45,1.25,color(0x43b5b4),[0,.82,0],player);
 ball(.37,mats.skin,[0,1.6,0],player);
 cylinder(.42,.32,.2,color(0x8d214f),[0,1.95,0],player);
 for(const x of [-.25,.25]){
   const hand=ball(.13,mats.skin,[x,.9,.06],player);hand.castShadow=false;
 }
 const aunty=new THREE.Group();scene.add(aunty);
 const sari=cylinder(.46,.88,1.52,mats.pink,[0,.85,0],aunty);
 box(.25,1.55,.07,mats.gold,[-.35,.91,.48],aunty).rotation.z=-.14;
 cylinder(.42,.38,.61,mats.wine,[0,1.82,0],aunty);
 const head=new THREE.Group();head.position.y=2.30;aunty.add(head);
 ball(.36,mats.skin,[0,0,0],head,[1.07,1.03,.95]);
 ball(.30,mats.hair,[0,.24,-.12],head,[1.18,.7,1.04]);
 ball(.19,mats.hair,[0,.37,-.26],head);
 const eyebrowL=box(.16,.029,.025,mats.hair,[-.15,.10,.326],head);
 const eyebrowR=box(.16,.029,.025,mats.hair,[.15,.10,.326],head);
 for(const side of [-1,1]){
   ball(.06,mats.ivory,[side*.155,.013,.326],head,[1.05,.68,.35]);
   ball(.024,mats.eye,[side*.155,.013,.371],head);
   torus(.062,.012,mats.gold,[side*.375,-.15,.08],head).rotation.y=Math.PI/2;
 }
 ball(.041,mats.rose,[0,.17,.35],head,[1,.5,.48]);
 const mouth=ball(.067,mats.rose,[0,-.17,.346],head,[1,.27,.27]);
 const left=new THREE.Group(),right=new THREE.Group();left.position.set(-.47,1.90,0);right.position.set(.47,1.90,0);
 aunty.add(left,right);
 for(const arm of [left,right]){
   cylinder(.13,.105,.66,mats.skin,[0,-.36,0],arm);
   torus(.13,.031,mats.gold,[0,-.58,0],arm).rotation.x=Math.PI/2;
   ball(.14,mats.skin,[0,-.72,0],arm);
 }
 const shadow=new THREE.Mesh(new THREE.CircleGeometry(.85,28),new THREE.MeshBasicMaterial({color:0x210c25,transparent:true,opacity:.35,depthWrite:false}));
 shadow.rotation.x=-Math.PI/2;shadow.position.set(0,.071,0);aunty.add(shadow);

 const out={scene,camera,player,aunty,head,eyebrowL,eyebrowR,mouth,left,right,assets:'PLACEHOLDER',mixer:null};
 out.update=(s,dt,elapsed)=>{
   const alpha=Math.min(1,dt*10);
   const px=s.lane*1.55;
   player.position.x=THREE.MathUtils.lerp(player.position.x,px,alpha);
   player.position.y=s.roll>0?.32:Math.abs(Math.sin(s.t*8))*.045;
   player.rotation.x=THREE.MathUtils.lerp(player.rotation.x,s.roll>0?-1.05:0,alpha);
   const z=auntyPosition(s.t);aunty.position.set(0,0,z);
   const near=s.t>4.5&&s.t<7.2;
   const reaction=s.resolved&&s.result==='dodged';
   head.rotation.z=near?.12*Math.sin(s.t*5):0;head.rotation.x=near?-.10:0;
   eyebrowL.rotation.z=near?.25:0;eyebrowR.rotation.z=near?-.25:0;
   mouth.scale.y=near?1+.55*Math.abs(Math.sin(s.t*12)):1;
   right.rotation.z=near?-1.8+.4*Math.sin(s.t*10):-.4;
   left.rotation.z=near?.3+.15*Math.cos(s.t*7):-.2;
   aunty.rotation.y=near?.1*Math.sin(s.t*3):0;
   if(reaction)head.rotation.z=.32;
   camera.position.lerp(V(player.position.x*.18,3.75,8.0),alpha*.7);
   camera.lookAt(player.position.x*.25,1.4,-5.0);
   if(out.mixer)out.mixer.update(Math.min(dt,.1));
 };
 out.resize=(w,h)=>{camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);};
 return out;
}


// Fail-closed installation: assets remain debug-only until owner gate and
// SHA-256 verification in main.js; inspect actual parsed GLTF again here.
export async function installApprovedAssets(world,{characterBytes,venueBytes}){
  if(!(characterBytes instanceof ArrayBuffer)||!(venueBytes instanceof ArrayBuffer))
    throw new Error('Raw verified binary GLB buffers required');
  const {GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js');
  const loader=new GLTFLoader();
  const [character,venue]=await Promise.all([
    loader.parseAsync(characterBytes,''),
    loader.parseAsync(venueBytes,'')
  ]);
  const rig=inspectCharacterGLTF(character);
  if(!rig.passed)throw new Error('Art rig contract not met: '+JSON.stringify(rig));
  if(!venue.scene)throw new Error('Wedding environment scene missing');
  let venueMeshes=0;
  venue.scene.traverse(o=>{if(o.isMesh)venueMeshes++;});
  if(venueMeshes<10)throw new Error('Modular wedding venue insufficient');
  // Commit the GLBs only once both buffers and both scene graphs passed.
  for(const o of [...world.scene.children]){
    if(o.isMesh||o.isInstancedMesh)world.scene.remove(o);
  }
  world.aunty.clear();world.aunty.add(character.scene);
  character.scene.traverse(o=>{
    if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}
  });
  world.scene.add(venue.scene);
  world.mixer=new THREE.AnimationMixer(character.scene);
  const idle=character.animations.find(a=>a.name==='Idle');
  world.mixer.clipAction(idle).play();
  world.assets='VERIFIED_GLB_PAIR';
  return {installed:true,rig,venueMeshes};
}
