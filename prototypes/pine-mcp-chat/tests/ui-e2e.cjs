/* B1 offline Chrome/Playwright QA. Uses existing local Playwright installation.
 * No remote endpoint, external scripts, credentials or real Pine automation.
 * NODE_PATH=<existing-node_modules> node tests/ui-e2e.cjs <path-to-index.html>
 */
"use strict";
const {chromium}=require("playwright");
const assert=require("node:assert/strict");
const path=require("node:path");
const fs=require("node:fs");
const {pathToFileURL}=require("node:url");
const source=path.resolve(process.argv[2]||path.join(__dirname,"..","index.html"));
if(!fs.statSync(source).isFile())throw Error("missing_local_fixture");
const screenRoot=path.join(path.dirname(source),"qa-screens");
fs.mkdirSync(screenRoot,{recursive:true,mode:0o700});
const sizes=[320,360,375,390,430,768,1440];
async function run(){
  const browser=await chromium.launch({
    headless:true,executablePath:process.env.CHROME_BIN||"/usr/bin/google-chrome",
    args:["--disable-background-networking","--no-first-run","--disable-extensions"]
  });
  const records=[];
  const {createVisibleWindowGuard}=await import(pathToFileURL(path.resolve(__dirname,"../../../brain/automation/visible_window_tag.mjs")).href);
  try{
    for(const width of sizes){
      // Always construct a new, disposable automation-owned page; NEVER capture
      // the owner's pre-existing browsing tab or a TradingView chart.
      const context=await browser.newContext({viewport:{width,height:850},deviceScaleFactor:1});
      const guard=createVisibleWindowGuard(context);
      const lease={
        project:"PINE-QA",worker:"MATRIX",taskId:"AW1-B1-"+width,
        mode:"EDIT-QA",state:"RUNNING",expiresAt:Date.now()+600000,
        allowedOrigins:[],offlineFixtureUrl:pathToFileURL(source).href
      };
      const page=await guard.open(lease,pathToFileURL(source).href);
      const ui=(action,fn)=>guard.run(page,lease,action,fn);
      const errors=[],externals=[];
      page.on("pageerror",e=>errors.push(e.message));
      page.on("request",req=>{if(!req.url().startsWith("file://"))externals.push(req.url().slice(0,80));});
      await guard.inspect(page,lease);
      assert.equal(await page.locator("#aw1-automation-owner-tag #aw1-label").isVisible(),true,"AW-1 tag "+width);
      assert.equal(await page.locator("#intro").isVisible(),true,"intro "+width);
      assert.equal(await page.locator("#history button").count(),1,"initial thread "+width);
      await ui("fill",()=>page.locator("#input").fill("Explain Pine v6 compilation"));
      await ui("click",()=>page.locator("#send").click());
      assert.equal(await page.locator("#messages article").count(),2,"messages "+width);
      assert.match(await page.locator("#messages").innerText(),/NO LIVE COMPILATION PERFORMED/);
      await ui("click",()=>page.locator("#details").click());
      assert.equal(await page.locator("#inspector").isVisible(),true);
      await ui("click",()=>page.locator("#inspectIntent").click());
      assert.match(await page.locator("#intentStatus").innerText(),/^Denied:/);
      await ui("press",()=>page.keyboard.press("Escape"));
      assert.equal(await page.locator("#inspector").isVisible(),false);
      if(width<=800)await ui("click",()=>page.locator("#toggleNav").click());
      await ui("click",()=>page.locator("#newchat").click());
      assert.equal(await page.locator("#intro").isVisible(),true,"reset "+width);
      assert.equal(await page.locator("#messages article").count(),0);
      if(width<=800)await ui("click",()=>page.locator("#toggleNav").click());
      await ui("fill",()=>page.locator("#threadSearch").fill("Explain Pine"));
      assert.equal(await page.locator("#history button").count(),1,"search "+width);
      await ui("click",()=>page.locator("#history button").first().click());
      assert.equal(await page.locator("#messages article").count(),2,"restore "+width);
      if(width<=800){
        await ui("click",()=>page.locator("#toggleNav").click());
        assert.equal(await page.locator("#sidebar").getAttribute("aria-hidden"),"false");
        await ui("press",()=>page.keyboard.press("Escape"));
        assert.equal(await page.locator("#toggleNav").getAttribute("aria-expanded"),"false");
      }else{
        await ui("click",()=>page.locator("#theme").click());
        assert.equal(await page.locator("html").evaluate(el=>el.classList.contains("light")),true);
      }
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
      assert.equal(overflow,false,"horizontal overflow "+width);
      assert.deepEqual(errors,[],"page exceptions "+width);
      assert.deepEqual(externals,[],"unexpected network "+width);
      if([320,390,768,1440].includes(width)){
        await ui("screenshot",()=>page.screenshot({path:path.join(screenRoot,"aw1-b1-"+width+".png"),fullPage:true}));
      }
      records.push({width,tests:["send","reset","thread_search","restore","inspect_denial","a11y_navigation","overflow","no_errors","no_network","aw1_visible"],passed:true});
      await guard.finish(page,lease);
      await page.close();
      await context.close();
    }
    console.log(JSON.stringify({status:"PASS",widths:sizes,checks:records.length*10,aw1:"TAGGED_AUTOMATION_ONLY",screens:screenRoot,records}));
  }finally{await browser.close();}
}
run().catch(err=>{console.error("QA_FAILED",err.stack);process.exitCode=1;});
