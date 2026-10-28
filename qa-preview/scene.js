import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js';
import {createHudPresenter} from './features/hud.js';
import {createFeedbackPresenter} from './features/feedback.js';
const canvas=document.querySelector('#stage'), game=document.querySelector('#game');
const scene=new THREE.Scene();
const camera=new THREE.OrthographicCamera(-5.4,5.4,3.4,-3.4,.1,100);
camera.position.set(0,0,20);camera.lookAt(0,0,0);
let renderer;
try{renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'low-power'});renderer.setPixelRatio(Math.min(1.5,devicePixelRatio));renderer.outputColorSpace=THREE.SRGBColorSpace;}
catch(e){document.querySelector('#game-message').textContent='Graphics unavailable — keyboard and touch controls remain active.';window.__graphicsError=String(e);}
function mat(hex,opacity=1){return new THREE.MeshBasicMaterial({color:hex,transparent:opacity<1,opacity,side:THREE.DoubleSide,depthTest:false});}
function rect(x,y,w,h,c,z=0){const o=new THREE.Mesh(new THREE.PlaneGeometry(w,h),mat(c));o.position.set(x,y,z);scene.add(o);return o;}
function poly(coords,c,z=0){const g=new THREE.Shape();g.moveTo(...coords[0]);coords.slice(1).forEach(v=>g.lineTo(...v));g.closePath();const o=new THREE.Mesh(new THREE.ShapeGeometry(g),mat(c));o.position.z=z;scene.add(o);return o;}
function circ(x,y,r,c,z=0){const o=new THREE.Mesh(new THREE.CircleGeometry(r,40),mat(c));o.position.set(x,y,z);scene.add(o);return o;}
function line(points,c,width=.03,z=0){for(let i=1;i<points.length;i++){const [x1,y1]=points[i-1],[x2,y2]=points[i];const len=Math.hypot(x2-x1,y2-y1);const o=rect((x1+x2)/2,(y1+y2)/2,len,width,c,z);o.rotation.z=Math.atan2(y2-y1,x2-x1);}}
function torus(x,y,r,t,c,z=0){const o=new THREE.Mesh(new THREE.RingGeometry(r-t,r,64),mat(c));o.position.set(x,y,z);scene.add(o);return o;}
function flower(x,y,r,z){for(let i=0;i<7;i++){const a=i*Math.PI*2/7;circ(x+Math.cos(a)*r*.62,y+Math.sin(a)*r*.62,r*.39,i%2?'#eeb873':'#e69d62',z)}circ(x,y,r*.31,'#9d394b',z+.01);}
rect(0,0,12,8,'#593b50',-15);
rect(0,1.7,12,3.8,'#8e6477',-13);
circ(3.7,2.4,2.6,'#bd8a87',-12);circ(-3.9,2,2.2,'#a97879',-12);
rect(0,-2.1,12,2.7,'#b7776c',-11);
poly([[-5.4,-3.4],[-4.2,-.7],[4.2,-.7],[5.4,-3.4]],'#c89273',-10);
poly([[-2.35,-3.4],[-1.45,-.7],[1.45,-.7],[2.35,-3.4]],'#d5a283',-9);
for(const side of [-1,1]){const a=side*2.5;poly([[a,-3.4],[a*.56,-.7],[a*.62,-.7],[a+side*.2,-3.4]],'#e0b394',-8);}
for(let i=0;i<12;i++){const x=-5.1+i*.93;circ(x,2.35,.03,'#f9dcb0',0);circ(x,2.35,.09,'#f1c886',-1);}
for(const side of [-1,1]){
 const x=side*3.9;
 rect(x,.1,.37,4.35,'#f0c996',1);rect(x,.1,.21,4.35,'#ba795f',2);
 rect(x,2.15,.8,.18,'#f2dbad',3);rect(x,-2.2,.8,.24,'#e5b783',3);
 for(let y=-1.9;y<2.1;y+=.52){circ(x,y,.07,'#f7e3c5',4);}
 rect(x+side*.25,-.85,.42,.8,'#e3a377',2);
}
const arch=new THREE.Group();scene.add(arch);
const archOuter=new THREE.Mesh(new THREE.RingGeometry(1.73,2.1,80,1,0,Math.PI),mat('#e5bf8a'));archOuter.position.set(0,.05,3);archOuter.rotation.z=Math.PI;arch.add(archOuter);
for(let side of [-1,1]){rect(side*1.9,-1, .38,2.4,'#e9c593',3);rect(side*1.9,-1.05,.2,2.25,'#b67c61',4);}
torus(0,.06,1.68,.07,'#8c3e55',5);
for(let i=0;i<20;i++){const t=(i+.25)/20*Math.PI;const x=-1.82*Math.cos(t),y=.05+1.72*Math.sin(t);flower(x,y,.13,6);}
rect(0,-1.74,4.8,.22,'#563342',4);
rect(0,-1.51,3.9,.23,'#9b4b54',4);
rect(0,-1.31,3.35,.19,'#bb6d67',4);
for(let i=0;i<13;i++){let x=-4.95+i*.83;line([[x,3.1],[x+.1,2.73]],'#dbb680',.025,5);circ(x+.1,2.72,.08,'#ffdf8e',6);}
for(let side of [-1,1]){let x=side*4.3;line([[x,2.2],[x,1.3]],'#e3ba86',.035,5);rect(x,1.28,.44,.55,'#efc78e',6);rect(x,1.28,.29,.4,'#ad4c55',7);circ(x,1.3,.08,'#ffe59c',8);}
for(let i=0;i<17;i++){const x=-4.7+i*.59;const y=2.5+Math.cos(i*.65)*.11;flower(x,y,.10,7);}
for(let i=0;i<21;i++){let x=(i*2.39)%10-5,y=((i*1.87)%3.4)-1.2;circ(x,y,.025+(i%4)*.009,i%2?'#f9d7a1':'#d68f8e',1);}
const player=new THREE.Group();scene.add(player);
const shadow=new THREE.Mesh(new THREE.CircleGeometry(.53,40),mat('#553044',.62));shadow.scale.y=.26;shadow.position.set(0,-2.65,10);scene.add(shadow);
function part(geom,color,x,y,z){const o=new THREE.Mesh(geom,mat(color));o.position.set(x,y,z);player.add(o);return o;}
part(new THREE.CircleGeometry(.49,44),'#f5d398',0,-1.66,9);
part(new THREE.RingGeometry(.49,.59,44),'#7e334e',0,-1.66,10);
part(new THREE.ConeGeometry(.32,.58,3),'#b13f5a',0,-1.68,11).rotation.z=Math.PI;
part(new THREE.CircleGeometry(.13,30),'#5a3045',0,-1.69,12);
for(let a=0;a<6;a++){const t=a*Math.PI/3;part(new THREE.CircleGeometry(.042,18),'#f7ede1',Math.cos(t)*.36,-1.66+Math.sin(t)*.36,11);}
let lane=1,moves=0,frame=0,encounterEngine=null;
const warning=new THREE.Group();scene.add(warning);
const warningRing=new THREE.Mesh(new THREE.RingGeometry(.38,.46,48),mat('#ffde9c'));warning.add(warningRing);
const warningFace=new THREE.Mesh(new THREE.CircleGeometry(.31,48),mat('#d67a67'));warning.add(warningFace);
for(let i=0;i<7;i++){let a=i*Math.PI*2/7;const petal=new THREE.Mesh(new THREE.CircleGeometry(.08,16),mat(i%2?'#ffe4ab':'#f4b96b'));petal.position.set(Math.cos(a)*.29,Math.sin(a)*.29,.05);warning.add(petal);}
const warningDot=new THREE.Mesh(new THREE.CircleGeometry(.08,24),mat('#5b334b'));warningDot.position.z=.09;warning.add(warningDot);
warning.position.set(0,-.7,11);
const hudPresenter=createHudPresenter({root:document});
const feedbackPresenter=createFeedbackPresenter({root:document});
function paintEncounter(state){
 if(!state||typeof state!=='object')return;
 const safe=Number.isInteger(state.hazard)&&state.hazard>=0&&state.hazard<=2?state.hazard:1;
 warning.position.x=positions[safe];warning.visible=!state.gameOver;
 hudPresenter.render(state);
 feedbackPresenter.render(state);
 window.__encounterState={...state};
}

const names=['LEFT','CENTER','RIGHT'],positions=[-2.05,0,2.05];
function update(){document.querySelector('#lane-text').textContent=names[lane];document.querySelector('#moves-count').textContent=moves+' MOVES';document.querySelector('#game-message').textContent=moves?'Nice dodge. The aunty is still looking for you.':'Use ← and → or swipe to dodge the Aunty.';window.__pilotState={ready:true,lane,moves,renderReady:!!renderer,controlsReady:window.__pilotState?.controlsReady===true,ownerApproved:false,production:false};if(encounterEngine)paintEncounter(encounterEngine.snapshot());}
function move(step){if(!Number.isFinite(step))return;const next=Math.max(0,Math.min(2,lane+Math.sign(step)));if(next!==lane){lane=next;moves++;if(encounterEngine)encounterEngine.choose(lane);update();}}
function reset(){lane=1;moves=0;if(encounterEngine)encounterEngine.reset();update();}
function paint(){if(!renderer)return;const target=positions[lane];player.position.x+=(target-player.position.x)*.16;player.position.y=Math.sin(frame*.035)*.04;shadow.position.x+=(target-shadow.position.x)*.16;frame++;renderer.render(scene,camera);requestAnimationFrame(paint);}
function resize(){if(!renderer)return;const b=game.getBoundingClientRect();renderer.setSize(Math.max(240,b.width),Math.max(240,b.height),false);const aspect=b.width/b.height;camera.left=-3.4*aspect;camera.right=3.4*aspect;camera.updateProjectionMatrix();}
window.addEventListener('resize',resize);
resize();update();paint();
import('./logic.js').then(({installDodgeControls})=>{
 const dispose=installDodgeControls({container:game,leftButton:document.querySelector('#go-left'),rightButton:document.querySelector('#go-right'),restartButton:document.querySelector('#restart'),move,reset});
 if(typeof dispose!=='function')throw Error('controls_dispose_missing');
 window.__pilotState.controlsReady=true;
}).catch(e=>{window.__pilotState.controlsReady=false;window.__pilotState.error=String(e);document.querySelector('#game-message').textContent='Controls failed to load.';});

import('./encounter.js').then(({createEncounterEngine})=>{
 const candidate=createEncounterEngine({onState:paintEncounter});
 if(!candidate||['choose','advance','reset','snapshot'].some(k=>typeof candidate[k]!=='function'))throw Error('encounter_contract_invalid');
 encounterEngine=candidate;
 document.querySelector('#go-next').addEventListener('click',()=>{encounterEngine.choose(lane);encounterEngine.advance();update();});
 encounterEngine.choose(lane);update();
 window.__encounterReady=true;
}).catch(e=>{window.__encounterReady=false;window.__encounterError=String(e);document.querySelector('#game-message').textContent='Encounter module failed to load.';});
