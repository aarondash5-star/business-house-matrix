'use strict';
// Deterministic visual sampling of the original private Delulu reveal.
// 12 time positions x 2 viewport classes, no external navigation or publication.
const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('/var/lib/generic-linux-automator-exec/moksha-browser/node_modules/playwright');
const INDEX='/var/lib/generic-linux-automator-exec/matrix-controller/staging-private/delulu_tech/a22ec4a63144f2f3e80c/index.html';
const OUT='/var/lib/generic-linux-automator-exec/delulu-frame-qa-20261024-run1';
const TIMES=[0,120,240,360,480,600,800,1000,1200,1450,1800,2500];
const MODES=[{name:'mobile',width:390,height:844,thumbW:234,thumbH:506},
             {name:'desktop',width:1440,height:900,thumbW:360,thumbH:225}];
async function montage(browser,buffers,times,mode){
  const p=await browser.newPage();
  const img64=buffers.map(b=>b.toString('base64'));
  const result=await p.evaluate(async ({img64,times,mode})=>{
    const cols=3,rows=Math.ceil(img64.length/cols),pad=7,labelH=23;
    const tw=mode.thumbW,th=mode.thumbH;
    const canvas=document.createElement('canvas');
    canvas.width=cols*(tw+pad)+pad;
    canvas.height=rows*(th+labelH+pad)+pad;
    const ctx=canvas.getContext('2d');
    ctx.fillStyle='#171A22';ctx.fillRect(0,0,canvas.width,canvas.height);
    for(let i=0;i<img64.length;i++){
      const img=new Image();
      img.src='data:image/png;base64,'+img64[i];
      await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=reject});
      const col=i%cols,row=Math.floor(i/cols);
      const x=pad+col*(tw+pad),y=pad+row*(th+labelH+pad);
      ctx.fillStyle='#252A36';ctx.fillRect(x-1,y-1,tw+2,th+2);
      ctx.drawImage(img,x,y,tw,th);
      ctx.fillStyle='#F5F6F2';ctx.font='bold 14px system-ui,sans-serif';
      ctx.fillText(mode.name+'  '+times[i]+'ms',x+5,y+th+17);
    }
    return canvas.toDataURL('image/jpeg',.48).split(',')[1];
  },{img64,times,mode});
  await p.close();
  return Buffer.from(result,'base64');
}
async function main(){
  if(!fs.existsSync(INDEX))throw Error('staging_missing');
  fs.mkdirSync(OUT,{mode:0o700,recursive:false});
  const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,
    args:['--disable-dev-shm-usage','--no-first-run']});
  const reports=[];
  try{
    for(const mode of MODES){
      const context=await browser.newContext({viewport:{width:mode.width,height:mode.height},reducedMotion:'no-preference'});
      const page=await context.newPage();
      await page.route('**/*',route=>{
        const url=route.request().url();
        const protocol=new URL(url).protocol;
        return protocol==='file:'||protocol==='data:'?route.continue():route.abort();
      });
      await page.goto(pathToFileURL(INDEX).href,{waitUntil:'load',timeout:25000});
      await page.evaluate(()=>{
        window.__deluluVisualAnimations=document.getAnimations({subtree:true});
        window.__deluluVisualAnimations.forEach(a=>a.pause());
      });
      const buffers=[],motion=[];
      for(const ms of TIMES){
        const state=await page.evaluate(ms=>{
          window.__deluluVisualAnimations.forEach(a=>{a.currentTime=ms;a.pause()});
          const mark=document.querySelector('.logo-stage img'),copy=document.querySelector('.hero-copy');
          const logo=getComputedStyle(mark),body=getComputedStyle(copy);
          return {ms,logoOpacity:logo.opacity,logoTransform:logo.transform,copyOpacity:body.opacity,
            scrollWidth:document.documentElement.scrollWidth,viewport:innerWidth};
        },ms);
        await page.waitForTimeout(35);
        buffers.push(await page.screenshot({type:'png',animations:'allow'}));
        motion.push(state);
      }
      const contact=await montage(browser,buffers,TIMES,mode);
      const file=path.join(OUT,mode.name+'-12-frames.jpg');
      fs.writeFileSync(file,contact,{mode:0o600,flag:'wx'});
      reports.push({mode:mode.name,width:mode.width,frames:TIMES.length,sheet:file,bytes:contact.length,
        motion,overflowFree:motion.every(x=>x.scrollWidth<=x.viewport+1)});
      await context.close();
    }
  }finally{await browser.close();}
  const success=reports.every(r=>r.overflowFree&&r.frames===12);
  console.log(JSON.stringify({status:success?'captured':'failed',framesTotal:24,reports},null,2));
  process.exitCode=success?0:2;
}
main().catch(err=>{console.error(JSON.stringify({status:'blocked',reason:err.message}));process.exitCode=1;});
