import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { McpServer } from "npm:@modelcontextprotocol/sdk@1.25.3/server/mcp.js";
import { WebStandardStreamableHTTPServerTransport } from "npm:@modelcontextprotocol/sdk@1.25.3/server/webStandardStreamableHttp.js";
import { createClient } from "npm:@supabase/supabase-js@2.75.0";
import { z } from "npm:zod@4.1.13";

const BASE = Deno.env.get("SUPABASE_URL") || "";
const ANON = Deno.env.get("SUPABASE_ANON_KEY") || "";
const SERVICE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
if (!BASE || !ANON || !SERVICE) throw new Error("Missing Supabase runtime configuration");
const admin = createClient(BASE, SERVICE, {auth:{persistSession:false,autoRefreshToken:false}});
const PREFIX = "/functions/v1/pine-chat-mvp-mcp";
const ROOT = BASE + PREFIX;
const RESOURCE = ROOT + "/mcp";
const AUTH = BASE + "/auth/v1";
const headers = {"content-type":"application/json; charset=utf-8","cache-control":"no-store"};
const json = (obj:unknown,status=200,extra:Record<string,string>={}) =>
  new Response(JSON.stringify(obj),{status,headers:{...headers,...extra}});
const tool = (obj:unknown)=>({structuredContent:{data:obj},content:[{type:"text" as const,text:JSON.stringify(obj)}]});
const paths = [
  "/.well-known/oauth-protected-resource",
  "/mcp/.well-known/oauth-protected-resource",
  "/mcp/oauth-protected-resource"
];
const meta = ()=>({
 resource: RESOURCE,
 authorization_servers:[AUTH],
 bearer_methods_supported:["header"],
 scopes_supported:["email","offline_access"]
});
function challenge(){
 return json({error:"authorization_required"},401,{
  "www-authenticate":'Bearer resource_metadata="'+ROOT+'/.well-known/oauth-protected-resource", scope="email offline_access", error="invalid_token"'
 });
}
class AuthUnavailable extends Error{}
async function authorizedOwner(req:Request):Promise<string|false|null>{
 const token=(req.headers.get("authorization")||"").match(/^Bearer\s+(\S+)$/i)?.[1];
 if(!token)return null;
 let resp:Response;
 try {resp=await fetch(AUTH+"/user",{headers:{apikey:ANON,authorization:"Bearer "+token},redirect:"manual",signal:AbortSignal.timeout(6000)});}
 catch{throw new AuthUnavailable("auth_unavailable");}
 if(resp.status===401||resp.status===403)return null;
 if(!resp.ok)throw new AuthUnavailable("auth_unavailable");
 const person=await resp.json().catch(()=>null);
 if(!person||typeof person.id!=="string")throw new AuthUnavailable("auth_response_invalid");
 const {data,error}=await admin.from("pine_mcp_members")
 .select("user_id").eq("user_id",person.id).eq("role","owner").eq("enabled",true).maybeSingle();
 if(error)throw new AuthUnavailable("membership_unavailable");
 return data ? person.id : false;
}
const WORKFLOWS = {
 specification:{
  title:"Strategy specification",
  steps:["Record entry/exit rules and indicator inputs","Define timeframe, lookahead and bar-close semantics","Enumerate risk limits and reproducible acceptance examples","Freeze a versioned test specification"],
  status:"design_only"
 },
 pine_v6:{
  title:"Pine Script v6 implementation review",
  steps:["Review source and immutable version label","Check repaint/lookahead/series semantics","Compile only in the separately authorized TradingView QA chart","Preserve compiler diagnostics and explicit QA receipts"],
  status:"native_compilation_not_run"
 },
 parity:{
  title:"Oracle parity and replay QA",
  steps:["Align feeds, symbols, timeframes and test window","Compare each closed bar against independent oracle output","Validate reload and Bar Replay reproducibility","Verify realtime nonrepaint and owner sign-off before release"],
  status:"validation_not_run"
 }
} as const;

Deno.serve(async (req:Request)=>{
 try{
  const parsed=new URL(req.url);
  const route=parsed.pathname.replace(/^\/(?:functions\/v1\/)?pine-chat-mvp-mcp/,"") || "/";
  if(req.method==="GET"&&route==="/health")
    return json({ok:true,service:"pine-chat-mvp-mcp",version:"0.2.0",auth:"owner_oauth_required",tools:10,data:"owner_oauth_beta_tools"});
  if(req.method==="GET"&&paths.includes(route))return json(meta());
  if(route!=="/mcp")return json({error:"not_found"},404);
  const membership=await authorizedOwner(req);
  if(membership===null)return challenge();
  if(!membership)return json({error:"not_enrolled_for_pine_chat"},403);
  const server=new McpServer({name:"Pine Chat Scoped MVP",version:"0.1.0"});
  server.registerTool("pine_chat_workspace_info",{
   title:"Pine chat workspace scope",
   description:"Read synthetic-only chat MVP scope. Never reads private chart, customer or trading account data.",
   inputSchema:{},
   annotations:{readOnlyHint:true,destructiveHint:false}
  },async()=>tool({project:"pine_mcp_chat",mode:"read_only",tools:["pine_chat_workspace_info","pine_chat_workflow","pine_chat_preview_info","pine_beta_feature_catalog","pine_beta_native_request","pine_beta_job_status","pine_beta_submit_feedback","pine_beta_paper_order","pine_beta_preview_event","pine_beta_recent_receipts"],can_execute:true,can_execute_native:false,can_trade:false,can_read_private_files:false,tenant:"owner_oauth_only",state:"mvp_protocol_connected"}));
  server.registerTool("pine_chat_workflow",{
   title:"Pine engineering workflow",
   description:"Read a static development checklist. Does not compile, run or modify code.",
   inputSchema:{workflow:z.enum(["specification","pine_v6","parity"])},
   annotations:{readOnlyHint:true,destructiveHint:false}
  },async({workflow})=>tool({workflow,...WORKFLOWS[workflow],tools_executed:false,generated_content:false}));
  server.registerTool("pine_chat_preview_info",{
   title:"Pine chat preview reference",
   description:"Read status and source location of a public synthetic UI prototype.",
   inputSchema:{},
   annotations:{readOnlyHint:true,destructiveHint:false}
  },async()=>tool({status:"private_demo_generated",source:"https://github.com/aarondash5-star/business-house-matrix/blob/docs/modular-mcp-chat-template-20261022/prototypes/pine-mcp-chat/index.html",mobile_viewports_passed:[320,360,390,430,768,1440],live_ui_hosted:false,live_tradingview_connected:false,real_chat_model_connected:false}));

  const ownerId = membership as string;
  const betaOperations = ["idea_capture","specification","golden_cases","pine_v6_draft",
    "independent_review","offline_static_qa","mcp_feed_ingest","native_compile",
    "repair_loop","native_signal_parity","bar_replay","realtime_nonrepaint",
    "source_versioning","release_review","alert_schema","alert_native_test",
    "webhook_gateway","notifications","paper_execution","broker_execution",
    "qa_evidence","tester_feedback"];
  const restrictedNative = ["native_compile","repair_loop","native_signal_parity",
    "bar_replay","realtime_nonrepaint","alert_native_test"] as const;
  const terminal = (err:string)=>tool({ok:false,error:err});
  const fingerprint=(x:string)=>/^[0-9a-f]{64}$/.test(x);
  const nonce=(x:string)=>/^[A-Za-z0-9_.:-]{12,96}$/.test(x);
  server.registerTool("pine_beta_feature_catalog",{
    title:"Pine beta full-vision feature inventory",
    description:"Show complete 22-feature Pine vision. Discovery does not certify native capability.",
    inputSchema:{},annotations:{readOnlyHint:true,destructiveHint:false}
  },async()=>tool({count:betaOperations.length,capabilities:betaOperations,
    safe_beta:"Pine source drafts and independent offline tests available in owner PWA",
    native_task_submission:"durably recorded; requires separately verified controller",
    live_order_enabled:false,production_alert_enabled:false,publishing_enabled:false,
    phase3_certified:false}));
  server.registerTool("pine_beta_native_request",{
    title:"Record guarded native TradingView QA request",
    description:"Owner-authorized typed QA request with immutable source hash and target chart. Does NOT yet run Windows or compile Pine.",
    inputSchema:{
      operation:z.enum(restrictedNative),
      source_sha256:z.string().regex(/^[0-9a-f]{64}$/),
      chart_path:z.string().min(15).max(120),
      idempotency_key:z.string().min(12).max(96)
    },annotations:{readOnlyHint:false,destructiveHint:false}
  },async({operation,source_sha256,chart_path,idempotency_key})=>{
    if(!nonce(idempotency_key)||!/^\/chart\/[A-Za-z0-9]{6,24}\/$/.test(chart_path)||
       /JvxzE0Bg|wHwOPnE1|tUblZ9Ev/.test(chart_path))return terminal("chart_identity_or_reserved_layout_denied");
    const payload={source_sha256,chart_path,operation,submitted_by:"owner_oauth_beta"};
    const {data,error}=await admin.from("pine_beta_jobs_v1")
      .insert({owner_id:ownerId,job_type:operation,source_sha256,target_chart:chart_path,
        idempotency_key,payload,status:"PENDING_NATIVE_ENROLLMENT"})
      .select("id,status,created_at,job_type,source_sha256,target_chart").single();
    if(error){
      if(error.code==="23505"){
        const prior=await admin.from("pine_beta_jobs_v1")
          .select("id,status,job_type,source_sha256,target_chart")
          .eq("owner_id",ownerId).eq("idempotency_key",idempotency_key).maybeSingle();
        if(prior.error||!prior.data||prior.data.source_sha256!==source_sha256||
           prior.data.job_type!==operation||prior.data.target_chart!==chart_path)
           return terminal("idempotency_key_conflict");
        return tool({ok:true,job:prior.data,replayed_existing:true,native_executed:false});
      }
      return terminal("qa_journal_unavailable");
    }
    return tool({ok:true,job:data,queued_for_manual_enrollment:true,native_executed:false});
  });
  server.registerTool("pine_beta_job_status",{
    title:"Read exact Pine native QA job and receipt",
    description:"Read an owned QA journal entry. No Windows commands.",
    inputSchema:{job_id:z.string().uuid()},
    annotations:{readOnlyHint:true,destructiveHint:false}
  },async({job_id})=>{
    const {data,error}=await admin.from("pine_beta_jobs_v1")
      .select("id,job_type,source_sha256,target_chart,status,created_at,finished_at,receipt")
      .eq("owner_id",ownerId).eq("id",job_id).maybeSingle();
    return error?terminal("qa_journal_unavailable"):tool({found:!!data,job:data,native_executed:data?.status==="COMPLETE"});
  });
  server.registerTool("pine_beta_submit_feedback",{
    title:"Persist beta QA feedback",
    description:"Create an owner-scoped durable beta feedback receipt; no publishing.",
    inputSchema:{feature:z.string().min(3).max(64),
      expected:z.string().min(1).max(1600),actual:z.string().min(1).max(1600),
      status:z.enum(["PASS","FAIL","BLOCKED","INCONCLUSIVE"]),
      idempotency_key:z.string().min(12).max(96)},
    annotations:{readOnlyHint:false,destructiveHint:false}
  },async({feature,expected,actual,status,idempotency_key})=>{
    if(!nonce(idempotency_key)||!betaOperations.includes(feature))return terminal("invalid_feature_or_idempotency");
    const payload={feature,expected,actual,status};
    const {data,error}=await admin.from("pine_beta_events_v1")
      .insert({owner_id:ownerId,event_type:"tester_feedback",idempotency_key,payload,
        result:{stored:true}})
      .select("id,created_at").single();
    if(error)return terminal(error.code==="23505"?"duplicate_feedback_id":"feedback_journal_unavailable");
    return tool({ok:true,id:data?.id,created_at:data?.created_at,stored:true});
  });
  server.registerTool("pine_beta_paper_order",{
    title:"Record simulated paper order",
    description:"Compute and durably journal cash/notional risk simulation. Never contacts broker.",
    inputSchema:{
      side:z.enum(["buy","sell"]),symbol:z.string().min(2).max(64),
      quantity:z.number().positive().max(100000),price:z.number().positive().max(100000000),
      cash:z.number().nonnegative().max(1000000000),
      max_notional:z.number().positive().max(1000000000),
      idempotency_key:z.string().min(12).max(96)},
    annotations:{readOnlyHint:false,destructiveHint:false}
  },async({side,symbol,quantity,price,cash,max_notional,idempotency_key})=>{
    if(!nonce(idempotency_key)||!/^[A-Za-z0-9:._/-]+$/.test(symbol))
      return terminal("invalid_paper_order");
    const notional=quantity*price;
    if(!Number.isFinite(notional))return terminal("invalid_notional");
    const rejected=notional>max_notional?"max_notional":side==="buy"&&notional>cash?"insufficient_cash":null;
    const result={mode:"PAPER_ONLY",state:rejected?"REJECTED":"SIMULATED",
      reason:rejected,notional,estimated_cash_after:rejected?cash:cash+(side==="buy"?-notional:notional),
      live_broker_order_sent:false,fill_confirmed:false};
    const {data,error}=await admin.from("pine_beta_events_v1")
      .insert({owner_id:ownerId,event_type:"paper_order",idempotency_key,
        payload:{side,symbol,quantity,price,cash,max_notional},result})
      .select("id,created_at").single();
    if(error)return terminal(error.code==="23505"?"duplicate_paper_order":"paper_ledger_unavailable");
    return tool({ok:true,receipt_id:data?.id,created_at:data?.created_at,...result});
  });
  server.registerTool("pine_beta_preview_event",{
    title:"Persist validated alert or notification dry run",
    description:"Creates an owner-scoped audit receipt. Does not create TradingView alerts or send Telegram/email.",
    inputSchema:{event_type:z.enum(["alert_dry_run","notification_dry_run"]),
      symbol:z.string().min(2).max(64),signal_id:z.string().min(2).max(128),
      idempotency_key:z.string().min(12).max(96)},
    annotations:{readOnlyHint:false,destructiveHint:false}
  },async({event_type,symbol,signal_id,idempotency_key})=>{
    if(!nonce(idempotency_key)||!/^[A-Za-z0-9:._/-]+$/.test(symbol))return terminal("invalid_alert_preview");
    const result={mode:"DRY_RUN",notification_sent:false,tradingview_alert_created:false,
      event_id:signal_id};
    const {data,error}=await admin.from("pine_beta_events_v1")
      .insert({owner_id:ownerId,event_type,idempotency_key,payload:{symbol,signal_id},result})
      .select("id,created_at").single();
    if(error)return terminal(error.code==="23505"?"duplicate_event":"event_journal_unavailable");
    return tool({ok:true,receipt_id:data?.id,created_at:data?.created_at,...result});
  });
  server.registerTool("pine_beta_recent_receipts",{
    title:"Inspect owner beta paper, alert and feedback receipts",
    description:"Read durable receipts without private source/credentials.",
    inputSchema:{limit:z.number().int().min(1).max(25).default(10)},
    annotations:{readOnlyHint:true,destructiveHint:false}
  },async({limit})=>{
    const {data,error}=await admin.from("pine_beta_events_v1")
      .select("id,event_type,created_at,result").eq("owner_id",ownerId)
      .order("created_at",{ascending:false}).limit(limit);
    return error?terminal("receipt_query_unavailable"):tool({receipts:data??[]});
  });

  const transport=new WebStandardStreamableHTTPServerTransport({sessionIdGenerator:undefined,enableJsonResponse:true});
  await server.connect(transport);
  try{return await transport.handleRequest(req);}
  finally{await server.close().catch(()=>undefined);}
 }catch(e){
  if(e instanceof AuthUnavailable)return json({error:"auth_temporarily_unavailable"},503,{"retry-after":"5"});
  console.error("Pine Chat MCP:",e instanceof Error?e.name:"error");
  return json({error:"internal_error"},500);
 }
});