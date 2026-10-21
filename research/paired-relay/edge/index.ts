import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.75.0";
const BASE=Deno.env.get("SUPABASE_URL")||"";
const SERVICE=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")||"";
if(!BASE||!SERVICE)throw new Error("Missing existing service context");
const db=createClient(BASE,SERVICE,{auth:{persistSession:false,autoRefreshToken:false}});
const HOST_MAC="mac-linux",HOST_DELL="dell-linux", VERSION="bhm-research-v1";
const reply=(x:unknown,status=200)=>new Response(JSON.stringify(x),{status,headers:{"content-type":"application/json","cache-control":"no-store","x-content-type-options":"nosniff"}});
const validID=(s:unknown)=>typeof s==="string"&&/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(s);
const validBox=(s:unknown,max=150000)=>typeof s==="string"&&s.length>=40&&s.length<=max&&/^[A-Za-z0-9_-]+$/.test(s);
const enc=new TextEncoder();
function from64(s:string){const a=s.replace(/-/g,"+").replace(/_/g,"/");return Uint8Array.from(atob(a+"=".repeat((4-a.length%4)%4)),c=>c.charCodeAt(0))}
async function verify(host:string, message:string, sig:unknown):Promise<boolean>{
 if(typeof sig!=="string"||sig.length>120||!/^[A-Za-z0-9_-]+$/.test(sig))return false;
 const r=await db.from("bhm_research_devices").select("verify_key").eq("host_id",host).eq("enabled",true).maybeSingle();
 if(r.error||!r.data)return false;
 try{
  const key=await crypto.subtle.importKey("raw",from64(r.data.verify_key),{name:"Ed25519"},false,["verify"]);
  return await crypto.subtle.verify("Ed25519",key,from64(sig),enc.encode(message));
 }catch{return false}
}
async function antiReplay(host:string,ts:unknown,nonce:unknown){
 if(!Number.isInteger(ts)||Math.abs(Math.floor(Date.now()/1000)-Number(ts))>60||!validID(nonce))return false;
 const x=await db.from("bhm_research_nonces").insert({host_id:host,nonce});
 return !x.error;
}
async function main(req:Request):Promise<Response>{
 const p=new URL(req.url).pathname.replace(/^\/(?:functions\/v1\/)?bhm-research-relay/,"")||"/";
 if(p==="/health"&&req.method==="GET")return reply({service:VERSION,healthy:true,public_search_port:false,authenticated_jobs_only:true});
 if(req.method!=="POST")return reply({error:"method_not_allowed"},405);
 if((Number(req.headers.get("content-length")||0)>160000))return reply({error:"request_too_large"},413);
 let b:any;try{const t=await req.text();if(t.length>160000)return reply({error:"request_too_large"},413);b=JSON.parse(t)}catch{return reply({error:"invalid_json"},400)}
 if(p==="/submit"){
  if(b?.host!==HOST_MAC||!validID(b.id)||!validBox(b.box,16000)||!Number.isInteger(b.expires)||b.expires<=Math.floor(Date.now()/1000)||b.expires>Math.floor(Date.now()/1000)+180)return reply({error:"invalid_request"},400);
  if(!await verify(HOST_MAC,`${VERSION}|submit|${HOST_MAC}|${b.id}|${b.expires}|${b.box}`,b.sig))return reply({error:"unauthorized"},401);
  const older=await db.from("bhm_research_jobs").select("id,request_box,expires_at,state").eq("id",b.id).maybeSingle();
  if(older.error)return reply({error:"lookup_failed"},503);
  if(older.data)return older.data.request_box===b.box?reply({id:b.id,state:older.data.state,deduplicated:true}):reply({error:"id_collision"},409);
  const count=await db.from("bhm_research_jobs").select("id",{head:true,count:"exact"}).in("state",["queued","claimed"]).gt("expires_at",new Date().toISOString());
  if(count.error)return reply({error:"queue_unavailable"},503);
  if((count.count||0)>=8)return reply({error:"queue_busy"},429);
  const r=await db.from("bhm_research_jobs").insert({id:b.id,request_box:b.box,expires_at:new Date(b.expires*1000).toISOString()});
  if(r.error)return reply({error:"enqueue_failed"},409);
  return reply({id:b.id,state:"queued",deduplicated:false});
 }
 if(p==="/poll"){
  if(b?.host!==HOST_DELL||!await verify(HOST_DELL,`${VERSION}|poll|${HOST_DELL}|${b.ts}|${b.nonce}`,b.sig))return reply({error:"unauthorized"},401);
  if(!await antiReplay(HOST_DELL,b.ts,b.nonce))return reply({error:"stale_or_replayed"},409);
  const now=new Date().toISOString();
  const q=await db.from("bhm_research_jobs").select("id,request_box,expires_at").eq("state","queued").gt("expires_at",now).order("created_at",{ascending:true}).limit(1);
  if(q.error)return reply({error:"lookup_failed"},503);
  const row=q.data?.[0];if(!row)return reply({ok:true,job:null});
  const claim=crypto.randomUUID();
  const r=await db.from("bhm_research_jobs").update({state:"claimed",claim,claimed_at:now}).eq("id",row.id).eq("state","queued").is("claim",null).select("id").maybeSingle();
  if(r.error)return reply({error:"claim_failed"},503);
  return reply({ok:true,job:r.data?{id:row.id,box:row.request_box,claim}:null});
 }
 if(p==="/finish"){
  if(b?.host!==HOST_DELL||!validID(b.id)||!validID(b.claim)||!validBox(b.box))return reply({error:"invalid_receipt"},400);
  if(!await verify(HOST_DELL,`${VERSION}|finish|${HOST_DELL}|${b.id}|${b.claim}|${b.ts}|${b.nonce}|${b.box}`,b.sig))return reply({error:"unauthorized"},401);
  if(!await antiReplay(HOST_DELL,b.ts,b.nonce))return reply({error:"stale_or_replayed"},409);
  const r=await db.from("bhm_research_jobs").update({state:"completed",response_box:b.box,completed_at:new Date().toISOString()}).eq("id",b.id).eq("state","claimed").eq("claim",b.claim).select("id").maybeSingle();
  if(r.error)return reply({error:"receipt_failed"},503);
  if(!r.data){
   const old=await db.from("bhm_research_jobs").select("state,claim,response_box").eq("id",b.id).maybeSingle();
   if(old.data?.state==="completed"&&old.data?.claim===b.claim&&old.data?.response_box===b.box)return reply({ok:true,already_recorded:true});
   return reply({error:"unclaimed_or_mismatched"},409);
  }
  return reply({ok:true,completed:true});
 }
 if(p==="/status"){
  if(b?.host!==HOST_MAC||!validID(b.id))return reply({error:"invalid_request"},400);
  if(!await verify(HOST_MAC,`${VERSION}|status|${HOST_MAC}|${b.id}|${b.ts}|${b.nonce}`,b.sig))return reply({error:"unauthorized"},401);
  if(!await antiReplay(HOST_MAC,b.ts,b.nonce))return reply({error:"stale_or_replayed"},409);
  const r=await db.from("bhm_research_jobs").select("state,response_box,expires_at").eq("id",b.id).eq("from_host",HOST_MAC).maybeSingle();
  if(r.error)return reply({error:"lookup_failed"},503);
  if(!r.data)return reply({error:"not_found"},404);
  return reply({id:b.id,state:r.data.state,box:r.data.state==="completed"?r.data.response_box:null,expired:Date.parse(r.data.expires_at)<Date.now()});
 }
 return reply({error:"not_found"},404);
}
Deno.serve(async req=>{try{return await main(req)}catch{return reply({error:"internal_error"},500)}});
