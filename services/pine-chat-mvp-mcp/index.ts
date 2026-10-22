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
async function authorizedOwner(req:Request):Promise<boolean|null>{
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
 return !!data;
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
    return json({ok:true,service:"pine-chat-mvp-mcp",version:"0.1.0",auth:"owner_oauth_required",tools:3,data:"synthetic_only"});
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
  },async()=>tool({project:"pine_mcp_chat",mode:"read_only",tools:["pine_chat_workspace_info","pine_chat_workflow","pine_chat_preview_info"],can_execute:false,can_trade:false,can_read_private_files:false,tenant:"owner_oauth_only",state:"mvp_protocol_connected"}));
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