#!/usr/bin/env node
/* Dell Gaming Dev Tool Yard end-to-end V2 QA: real video decode + browser + reduced motion.
 * Private local source only. Requires installed OSS Playwright/Chrome.
 */
const {chromium}=require('/var/lib/generic-linux-automator-exec/matrix-game-toolkit-20261025/node_modules/playwright-core');
const fs=require('fs'),path=require('path');
const site=path.resolve(__dirname);
const out=path.join(site,'qa-evidence');
const file='file://'+path.join(site,'index.html');
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch({headless:true,executablePath:'/usr/bin/google-chrome',
  args:['--disable-dev-shm-usage','--no-first-run','--autoplay-policy=no-user-gesture-required']});
 const results=[];
 for(const spec of [
  {name:'mobile-390',width:390,height:844,reducedMotion:'no-preference'},
  {name:'small-360',width:360,height:780,reducedMotion:'no-preference'},
  {name:'tablet-768',width:768,height:1024,reducedMotion:'no-preference'},
  {name:'desktop-1440',width:1440,height:900,reducedMotion:'no-preference'},
  {name:'reduced-mobile',width:390,height:844,reducedMotion:'reduce'},
  {name:'reduced-desktop',width:1440,height:900,reducedMotion:'reduce'}
 ]){
   const page=await b.newPage({viewport:{width:spec.width,height:spec.height},reducedMotion:spec.reducedMotion,deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(String(e)));
   const response=await page.goto(file,{waitUntil:'domcontentloaded'});
   await page.waitForTimeout(5500);
   const metrics=await page.evaluate(()=>{
      const section=document.querySelector('.hero'),host=document.getElementById('logo-motion');
      const vid=document.querySelector(window.innerWidth<=650?'#logo-film-tall':'#logo-film-wide');
      return {title:document.title,
        horizontalOverflow:document.documentElement.scrollWidth>window.innerWidth+1,
        logoLoaded:Array.from(document.querySelectorAll('.wordmark img, .logo-still img')).every(im=>im.complete&&im.naturalWidth>0),
        videoReadyState:vid.readyState,videoCurrentTime:vid.currentTime,videoEnded:vid.ended,
        videoPlaying:host.classList.contains('is-playing'),
        visibleIntroControls:!document.getElementById('skip-motion').hidden,
        heroTitle:document.querySelector('h1').textContent.trim(),
        linkTargets:Array.from(document.querySelectorAll('a[href^="#"]')).every(a=>document.querySelector(a.getAttribute('href'))!==null),
        bodyFont:getComputedStyle(document.body).fontFamily,
        centerColor:getComputedStyle(section).backgroundColor};
   });
   await page.screenshot({path:path.join(out,spec.name+'-viewport.png'),fullPage:false});
   // Full-page captures are supplemental: some headless Chrome builds omit composited video surfaces.
   await page.screenshot({path:path.join(out,spec.name+'.png'),fullPage:true,animations:'disabled'});
   const pass=!metrics.horizontalOverflow&&metrics.logoLoaded&&metrics.linkTargets&&errors.length===0
     &&(spec.reducedMotion==='reduce'?!metrics.videoPlaying:metrics.videoReadyState>=2);
   results.push({viewport:spec.name,reducedMotion:spec.reducedMotion,...metrics,errors,passed:pass});
   if(spec.name==='mobile-390'){
     await page.getByRole('button',{name:'Skip logo animation'}).click();
     const after=await page.evaluate(()=>!document.getElementById('logo-motion').classList.contains('is-playing')&&document.getElementById('skip-motion').disabled);
     results.push({test:'skip-animation',passed:after});
   }
   await page.close();
 }
 await b.close();
 const report={project:'delulu_tech',stage:'V2 site with original motion',timestamp:new Date().toISOString(),checks:results,passed:results.every(x=>x.passed)};
 fs.writeFileSync(path.join(out,'qa-report.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({passed:report.passed,checks:results.map(x=>({name:x.viewport||x.test,passed:x.passed,videoReadyState:x.videoReadyState,overflow:x.horizontalOverflow,errors:x.errors}))},null,2));
 if(!report.passed)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
