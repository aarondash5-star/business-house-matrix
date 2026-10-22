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
  try{
    for(const width of sizes){
      const page=await browser.newPage({viewport:{width,height:850},deviceScaleFactor:1});
      const errors=[],externals=[];
      page.on("pageerror",e=>errors.push(e.message));
      page.on("request",req=>{if(!req.url().startsWith("file://"))externals.push(req.url().slice(0,80));});
      await page.goto(pathToFileURL(source).href,{waitUntil:"load"});
      assert.equal(await page.locator("#intro").isVisible(),true,"intro "+width);
      assert.equal(await page.locator("#history button").count(),1,"initial thread "+width);
      await page.locator("#input").fill("Explain Pine v6 compilation");
      await page.locator("#send").click();
      assert.equal(await page.locator("#messages article").count(),2,"messages "+width);
      assert.match(await page.locator("#messages").innerText(),/NO LIVE COMPILATION PERFORMED/);
      await page.locator("#details").click();
      assert.equal(await page.locator("#inspector").isVisible(),true);
      await page.locator("#inspectIntent").click();
      assert.match(await page.locator("#intentStatus").innerText(),/^Denied:/);
      await page.keyboard.press("Escape");
      assert.equal(await page.locator("#inspector").isVisible(),false);
      if(width<=800)await page.locator("#toggleNav").click();
      await page.locator("#newchat").click();
      assert.equal(await page.locator("#intro").isVisible(),true,"reset "+width);
      assert.equal(await page.locator("#messages article").count(),0);
      if(width<=800)await page.locator("#toggleNav").click();
      await page.locator("#threadSearch").fill("Explain Pine");
      assert.equal(await page.locator("#history button").count(),1,"search "+width);
      await page.locator("#history button").first().click();
      assert.equal(await page.locator("#messages article").count(),2,"restore "+width);
      if(width<=800){
        await page.locator("#toggleNav").click();
        assert.equal(await page.locator("#sidebar").getAttribute("aria-hidden"),"false");
        await page.keyboard.press("Escape");
        assert.equal(await page.locator("#toggleNav").getAttribute("aria-expanded"),"false");
      }else{
        await page.locator("#theme").click();
        assert.equal(await page.locator("html").evaluate(el=>el.classList.contains("light")),true);
      }
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
      assert.equal(overflow,false,"horizontal overflow "+width);
      assert.deepEqual(errors,[],"page exceptions "+width);
      assert.deepEqual(externals,[],"unexpected network "+width);
      if(width===390||width===1440){
        await page.screenshot({path:path.join(screenRoot,"b1-"+width+".png"),fullPage:true});
      }
      records.push({width,tests:["send","reset","thread_search","restore","inspect_denial","a11y_navigation","overflow","no_errors","no_network"],passed:true});
      await page.close();
    }
    console.log(JSON.stringify({status:"PASS",widths:sizes,checks:records.length*9,screens:screenRoot,records}));
  }finally{await browser.close();}
}
run().catch(err=>{console.error("QA_FAILED",err.stack);process.exitCode=1;});
