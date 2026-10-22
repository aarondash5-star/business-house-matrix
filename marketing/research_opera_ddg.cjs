#!/usr/bin/env node
"use strict";
/**
 * BHM independent public-research Opera adapter.
 * Reuses existing running Opera CDP server; creates a fresh isolated,
 * ephemeral browser context, NEVER the Moksha/Let's Goa signed-in tabs.
 * Read-only DuckDuckGo search. No CAPTCHA evasion, logins, page submissions.
 */
const path = require("path");
const { chromium } = require(path.join(process.env.HOME,"moksha-browser/node_modules/playwright"));
const QUERY = process.argv[2] || "";
const MAX = 5;
function safeQuery(q) {
  if (typeof q !== "string" || q.length < 2 || q.length > 180 ||
      /[\x00-\x1f]/.test(q) ||
      /[\w.+-]+@[\w.-]+\.[a-z]{2,}/i.test(q) ||
      /\b(api.?key|private.?key|password|bearer|guest.?data|secret)\b/i.test(q)) {
    throw Error("invalid_public_query");
  }
  return q.trim();
}
function publicURL(link) {
  try {
    const u = new URL(link);
    if (u.protocol !== "https:" || u.username || u.password || u.port ||
        !u.hostname || /^(localhost|127\.|10\.|192\.168\.|169\.254\.)/.test(u.hostname)) return null;
    if (u.hostname === "duckduckgo.com" && u.pathname.startsWith("/l/")) {
      const dest = u.searchParams.get("uddg");
      return dest ? publicURL(dest) : null;
    }
    if (/duckduckgo\.com$/.test(u.hostname) || u.hostname === "duck.co") return null;
    u.hash="";u.search="";
    return u.toString().slice(0,700);
  } catch {return null;}
}
async function main() {
  const q=safeQuery(QUERY);
  let browser,ctx;
  try {
    browser=await chromium.connectOverCDP("http://127.0.0.1:9231",{timeout:8000});
    ctx=await browser.newContext({acceptDownloads:false,viewport:{width:1280,height:860},
                                  javaScriptEnabled:true,serviceWorkers:"block"});
    const page=await ctx.newPage();
    // Isolated context: never mutate existing operator/session tab or use saved credentials.
    await page.route("**/*",route=>{
      let u;
      try{u=new URL(route.request().url())}catch{return route.abort()}
      const host=u.hostname;
      const allow=u.protocol==="https:" && (
         host==="duckduckgo.com" || host==="www.duckduckgo.com" ||
         host==="links.duckduckgo.com" || host==="staticcdn.duckduckgo.com" ||
         host==="icons.duckduckgo.com" || host==="duck.co");
      return allow ? route.continue() : route.abort();
    });
    const target="https://duckduckgo.com/?"+new URLSearchParams({q,ia:"web"}).toString();
    await page.goto(target,{waitUntil:"domcontentloaded",timeout:18000});
    await page.waitForTimeout(1700);
    const data=await page.evaluate(()=>{
      const text=(document.body?.innerText||"").slice(0,5000);
      const links=[...document.querySelectorAll('a[href]')].map(a=>({
        title:(a.innerText||a.textContent||"").trim().slice(0,180),
        href:a.getAttribute("href")||"",outer:a.outerHTML.slice(0,200)
      })).filter(x=>x.title.length>12).slice(0,100);
      return {title:document.title,body:text,links};
    });
    const blocked=/captcha|verify you are human|unusual traffic|verify you're not a robot|automated traffic/i.test(data.body);
    const results=[];
    for(const row of data.links){
      const u=publicURL(new URL(row.href,"https://duckduckgo.com").href);
      if(!u || results.some(x=>x.url===u))continue;
      results.push({url:u,title:row.title,verified:false,engine:"duckduckgo_opera"});
      if(results.length>=MAX)break;
    }
    process.stdout.write(JSON.stringify({
      provider:"duckduckgo_via_isolated_opera",status:blocked?"blocked_captcha":results.length?"observed":"unavailable",
      captcha_detected:blocked,isolated_ephemeral_context:true,
      existing_session_touched:false,results:blocked?[]:results,
      publish_approval:false,spend_approval:false,paid_fallback:false,
      extraction_verified:false
    })+"\n");
  }catch(err){
    process.stdout.write(JSON.stringify({provider:"duckduckgo_via_isolated_opera",status:"unavailable",
      reason:String(err?.message||err).slice(0,100),results:[],existing_session_touched:false})+"\n");
    process.exitCode=2;
  }finally{
    if(ctx)await ctx.close().catch(()=>{});
    if(browser)await browser.close().catch(()=>{});
  }
}
main();
