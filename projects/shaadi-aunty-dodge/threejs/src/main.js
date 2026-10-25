import * as THREE from 'three';
import {createSession,action,step,DURATION,AUNTY} from './simulation.js';
import {createWeddingScene,installApprovedAssets} from './scene.js';
import {assessArtManifest,verifiedGLB,QUALITY_GATE_ID} from './artContract.js';
const root=document.getElementById('stage'),panel=document.getElementById('panel');
const button=document.getElementById('play'),score=document.getElementById('score');
const timer=document.getElementById('timer'),captions=document.getElementById('captions');
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
let s=createSession(),world,renderer,raf=0,last=0,acc=0,ended=false,frames=0,totalDt=0,slow=0;
const QA={engine:'three',renderer:'WebGLRenderer',version:THREE.REVISION,
 webgl2:false,phase:'ready',assets:'DEV_ONLY_PLACEHOLDER',elapsed:0,score:0,dodges:0,hits:0,drawcalls:0,
 frames:0,avgFPS:0,lowFPSFrames:0,devicePixelRatio:0,artApproved:false,qualityGate:QUALITY_GATE_ID,gateStatus:'BLOCKED'};
window.__premiumSliceQA=QA;
const unavailable=(reason)=>{
 panel.hidden=false;panel.querySelector('h1').textContent='Renderer unavailable';
 panel.querySelector('p').textContent=reason+' The original lightweight game is still available.';
 button.textContent='OPEN EXISTING GAME';button.onclick=()=>location.assign('https://shaadi-aunty-dodge.karanbizweb360.workers.dev/');
};
try{
 const probe=document.createElement('canvas').getContext('webgl2');
 if(!probe)throw new Error('WebGL2 unsupported on this device');
 QA.webgl2=true;
 renderer=new THREE.WebGLRenderer({antialias:false,alpha:false,powerPreference:'high-performance'});
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;
 renderer.toneMappingExposure=1.28;
 renderer.shadowMap.enabled=!reduced;
 renderer.shadowMap.type=THREE.PCFShadowMap;
 const dpr=Math.min(window.devicePixelRatio||1,1.5);
 renderer.setPixelRatio(dpr);QA.devicePixelRatio=dpr;
 root.appendChild(renderer.domElement);
 world=createWeddingScene(renderer);
 const resize=()=>world.resize(window.innerWidth,window.innerHeight);
 window.addEventListener('resize',resize,{passive:true});resize();
 renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(raf);unavailable('Graphics context lost.');});
 renderer.domElement.addEventListener('webglcontextrestored',()=>location.reload());
 fetch('./assets/asset-manifest.json',{cache:'no-store'}).then(r=>{
   if(!r.ok)throw new Error('Approved asset manifest missing');
   return r.json();
 }).then(async spec=>{
   const gate=assessArtManifest(spec);
   QA.gateStatus=gate.approved?'MANIFEST_COMPLETE_NEEDS_RUNTIME_QA':'BLOCKED';
   QA.gateIssues=gate.issues;
   if(!gate.approved)return; // Debug placeholders NEVER count as certified art.
   const [characterBytes,venueBytes]=await Promise.all([
     verifiedGLB(spec.character.uri,spec.character.sha256),
     verifiedGLB(spec.venue.uri,spec.venue.sha256)
   ]);
   const installed=await installApprovedAssets(world,{characterBytes,venueBytes});
   QA.assets=installed.installed?'VERIFIED_GLB_PAIR':'DEV_ONLY_PLACEHOLDER';
   QA.artApproved=!!installed.installed;
   QA.gateStatus=installed.installed?'ASSET_PARITY_LOADED_RELEASE_STILL_BLOCKED':'BLOCKED';
 }).catch(e=>{
   QA.artApproved=false;QA.gateStatus='BLOCKED';QA.assetWarning=String(e.message||e);
 });
 const apply=(a)=>{action(s,a);};
 document.querySelectorAll('[data-action]').forEach(b=>{
   b.addEventListener('pointerdown',e=>{e.preventDefault();apply(b.dataset.action);});
 });
 document.addEventListener('keydown',e=>{
   if(['ArrowLeft','a','A'].includes(e.key)){e.preventDefault();if(!e.repeat)apply('left');}
   else if(['ArrowRight','d','D'].includes(e.key)){e.preventDefault();if(!e.repeat)apply('right');}
   else if([' ','ArrowDown'].includes(e.key)){e.preventDefault();if(!e.repeat)apply('roll');}
 });
 let initialX=null;
 root.addEventListener('pointerdown',e=>{initialX=e.clientX;},{passive:true});
 root.addEventListener('pointerup',e=>{
   if(initialX===null)return;
   const dx=e.clientX-initialX;initialX=null;
   if(Math.abs(dx)>32)apply(dx>0?'right':'left');else apply('roll');
 },{passive:true});
 const present=()=>{
  score.textContent=s.score+' pts';timer.textContent=(DURATION-s.t).toFixed(1)+'s';
  const text=s.phase==='play'&&s.t>3.8&&s.t<6.6 ? 'Beta, shaadi kab?' :
   s.phase==='play'&&s.result==='dodged'&&s.t<8 ? 'DODGED! +100' :
   s.phase==='play'&&s.result==='caught'&&s.t<8 ? 'Aunty caught you!' : '';
  captions.textContent=text;
  QA.phase=s.phase;QA.elapsed=s.t;QA.score=s.score;QA.dodges=s.dodges;QA.hits=s.hits;
  QA.drawcalls=renderer.info.render.calls;QA.frames=frames;
  QA.avgFPS=totalDt>0?Math.round(frames/totalDt):0;QA.lowFPSFrames=slow;
 };
 const frame=now=>{
   if(ended)return;
   const dt=Math.min((now-last)/1000,.08);last=now;
   if(s.phase==='play'){
     acc+=dt;let ticks=0;
     while(acc>=1/60&&ticks<6){step(s,1/60);acc-=1/60;ticks++;}
     frames++;totalDt+=dt;if(dt>1/30)slow++;
   }
   world.update(s,dt,now/1000);renderer.render(world.scene,world.camera);
   present();
   if(s.phase==='done'){
     ended=true;panel.hidden=false;panel.querySelector('h1').textContent=s.dodges?'DODGED!':'NICE TRY!';
     panel.querySelector('p').textContent=s.score+' points · '+s.hits+' collision(s). Art release stays blocked until pinned V1 is certified.';
     button.textContent='REPLAY';button.onclick=()=>location.reload();cancelAnimationFrame(raf);return;
   }
   raf=requestAnimationFrame(frame);
 };
 button.addEventListener('click',()=>{
   if(s.phase!=='ready')return;
   s.phase='play';panel.hidden=true;last=performance.now();
   raf=requestAnimationFrame(frame);
   QA.phase='play';
 });
 // One render before first tap proves the world actually boots.
 world.update(s,0,0);renderer.render(world.scene,world.camera);present();
 window.addEventListener('pagehide',()=>{ended=true;cancelAnimationFrame(raf);renderer.dispose();});
}catch(e){unavailable('Three.js initialization failed: '+(e.message||e));QA.error=String(e);}

