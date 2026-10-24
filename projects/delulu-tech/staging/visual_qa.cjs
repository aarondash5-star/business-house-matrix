'use strict';
/* Delulu V1 private static visual smoke QA. No third-party navigation or publishing. */
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('/var/lib/generic-linux-automator-exec/moksha-browser/node_modules/playwright');

const site = '/var/lib/generic-linux-automator-exec/matrix-controller/staging-private/delulu_tech/a22ec4a63144f2f3e80c/index.html';
const widths = [360,390,768,1440];
const results = [];
const errors = [];
async function main() {
  if (!fs.existsSync(site)) throw Error('Private Delulu stage not found');
  const browser = await chromium.launch({
    executablePath:'/usr/bin/google-chrome',headless:true,
    args:['--disable-dev-shm-usage','--no-first-run']
  });
  try {
    for (const width of widths) {
      const context = await browser.newContext({
        viewport:{width,height:860},
        reducedMotion:'no-preference'
      });
      const page = await context.newPage();
      page.on('pageerror',e=>errors.push(width+':'+String(e.message).slice(0,160)));
      await page.route('**/*',route=>{
        const protocol=new URL(route.request().url()).protocol;
        return protocol==='file:'||protocol==='data:' ? route.continue():route.abort();
      });
      await page.goto(pathToFileURL(site).href,{waitUntil:'load',timeout:25000});
      await page.waitForTimeout(1800);
      const metrics = await page.evaluate(()=>{
        const img=document.querySelector('.logo-stage img');
        const cta=document.querySelector('.cta');
        const html=document.documentElement;
        const target=document.querySelector('#identity');
        const bg=getComputedStyle(document.body).backgroundColor;
        return {
          width:innerWidth,
          scrollWidth:html.scrollWidth,
          noHorizontalOverflow:html.scrollWidth<=innerWidth+1,
          title:document.title,
          logoLoaded:!!img&&img.complete&&img.naturalWidth>0,
          logoSrc:img?.getAttribute('src'),
          logoVisible:!!img&&img.getBoundingClientRect().width>0,
          background:bg,
          approvedPalette:!!document.querySelector('style')?.textContent.includes('#C9FF3D'),
          CTAValid:cta?.getAttribute('href')==='#identity'&&!!target,
          noindex:!!document.querySelector('meta[name="robots"]')?.content.includes('noindex')
        };
      });
      await page.locator('.cta').click({timeout:5000});
      metrics.ctaNavigation=await page.evaluate(()=>location.hash==='#identity');
      await page.locator('#skip-motion').click({timeout:5000});
      metrics.skipWorks=await page.evaluate(()=>document.body.classList.contains('motion-finished')&&document.getElementById('skip-motion').disabled);
      results.push(metrics);
      await context.close();
    }
    const context=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
    const page=await context.newPage();
    await page.goto(pathToFileURL(site).href,{waitUntil:'load',timeout:25000});
    const reduced=await page.evaluate(()=>getComputedStyle(document.querySelector('.logo-stage img')).animationName==='none');
    results.push({reducedMotionAnimationDisabled:reduced});
    await context.close();
  }finally{await browser.close();}
  const all=results.slice(0,4).every(x=>x.noHorizontalOverflow&&x.logoLoaded&&x.logoVisible&&x.approvedPalette&&x.CTAValid&&x.ctaNavigation&&x.skipWorks&&x.noindex)&&results[4].reducedMotionAnimationDisabled&&errors.length===0;
  const receipt={status:all?'pass':'fail',site:'delulu-tech-private-v1',testedWidths:widths,results,errors,publicServer:false};
  process.stdout.write(JSON.stringify(receipt,null,2)+'\n');
  process.exitCode=all?0:2;
}
main().catch(e=>{process.stderr.write(JSON.stringify({status:'blocked',error:e.message})+'\n');process.exitCode=1;});
