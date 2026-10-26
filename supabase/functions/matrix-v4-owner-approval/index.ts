// Dell V4 owner approval backend — exact release only; fail closed by default.
// Reuses existing Supabase Auth email OTP / magic link, PostgREST RLS-private
// service ledger and already-stored DEV_BETA PKCS8 key. No general signer API.
// Installation does not require new root/sudo privileges or public SSH.
const BASE="matrix_v4_owner_challenges";
const HOST="dell-linux", PROJECT="matrix_dev_manager";
const RELEASE="matrix_v4_controller_v14_rebased_v12_20261027";
const OLD_PINS={
  "controller.py":"e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836",
  "yard_auto_adapter_v1.py":"adad20add5e247c515c48d8e2d0c61f2b91e2238d489ed8b4c2e674c845d1abe",
  "yard_execution_guard_v13.py":"7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e",
  "yard_exec_bindings_v13.json":"9c084832984c1471a22079cc606daccd0a49b78c942ddfee0800a800176c43a9"
};
const NEW_PINS={
  "yard_auto_adapter_v1.py":"2ea43e8953c59726f510b6db9a8d0127a64efd7acb0fb824db5c70cb130a8837",
  "adapter_guard_v4.py":"90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30",
  "yard_execution_guard_v13.py":"664d4681747282561755dd34201210ce19306e15beeb506c8c02a024bf7ae644",
  "yard_exec_bindings_v14.json":"81edd213acfd4c66359d1a217a62c392c283358e972a7ea87b4948687fc5012f"
};
const QA=["github:40391381715","dell:a0c34b4e-5a12-47bb-a2c9-7ad280a34887"];
const encoder=new TextEncoder();
const env=(n:string)=>Deno.env.get(n)??"";
const secret=(name:string)=>env(name);
const header={"content-type":"application/json","cache-control":"no-store,private",
 "x-content-type-options":"nosniff","referrer-policy":"no-referrer"};
const asciiHex=(a:Uint8Array)=>Array.from(a,x=>x.toString(16).padStart(2,"0")).join("");
const randHex=(n:number)=>{const a=new Uint8Array(n);crypto.getRandomValues(a);return asciiHex(a)};
const hash=async(s:string)=>asciiHex(new Uint8Array(await crypto.subtle.digest("SHA-256",encoder.encode(s))));
const plain=(x:unknown):boolean=>!!x&&typeof x==="object"&&!Array.isArray(x);
const sorted=(x:unknown):unknown=>Array.isArray(x)?x.map(sorted):(plain(x)?
 Object.fromEntries(Object.entries(x as Record<string,unknown>).sort(([a],[b])=>a<b?-1:a>b?1:0).map(([k,v])=>[k,sorted(v)])):x);
const canonical=(x:Record<string,unknown>)=>JSON.stringify(sorted(x))+"\n";
function respond(code:number,body:Record<string,unknown>,origin=""){
 const h={...header};if(origin)Object.assign(h,{"access-control-allow-origin":origin,"vary":"Origin",
 "access-control-allow-headers":"authorization,content-type","access-control-allow-methods":"POST,OPTIONS"});
 return new Response(JSON.stringify(body),{status:code,headers:h});
}
function config(){
 const uid=env("MATRIX_V4_OWNER_UID"),email=env("MATRIX_V4_OWNER_EMAIL");
 const commit=env("MATRIX_V4_REVIEWED_COMMIT");
 const url=env("SUPABASE_URL"),pub=env("SUPABASE_ANON_KEY"),service=secret("SUPABASE_SERVICE_ROLE_KEY");
 const privateKey=secret("DEV_BETA_ED25519_PRIVATE_PKCS8_B64");
 const pem=env("MATRIX_V4_OWNER_PUBLIC_PEM");
 const expected=env("MATRIX_V4_OWNER_PUBLIC_SHA256");
 const allowedOrigin=env("MATRIX_V4_OWNER_ORIGIN");
 const enrolled=/^[a-f0-9-]{36}$/.test(uid)&&email.includes("@")&&/^[a-f0-9]{40}$/.test(commit)
  &&/^https:\/\/[a-zA-Z0-9.-]+$/.test(allowedOrigin)
  &&url.startsWith("https://")&&pub&&service&&privateKey&&pem
  &&/^[0-9a-f]{64}$/.test(expected);
 return {uid,email,commit,url,pub,service,privateKey,pem,expected,allowedOrigin,
   ready:env("MATRIX_V4_OWNER_APPROVAL_ENABLED")==="true"&&
      env("MATRIX_V4_RELEASE_SIGNER_ENABLED")==="true"&&!!enrolled};
}
type Cfg=ReturnType<typeof config>;
async function api(c:Cfg,route:string,init:RequestInit={},service=false){
 const token=service?c.service:c.pub;
 const headers={"apikey":token,"authorization":"Bearer "+token,
   "content-type":"application/json","cache-control":"no-store",...(init.headers??{})};
 return await fetch(c.url+route,{...init,headers,signal:AbortSignal.timeout(8000)});
}
async function database(c:Cfg,method:string,filter:string,payload?:unknown){
 const response=await api(c,"/rest/v1/"+BASE+filter,{
  method,headers:{"prefer":"return=representation"},body:payload===undefined?undefined:JSON.stringify(payload)
 },true);
 if(!response.ok)throw new Error("private_ledger_unavailable");
 const result=await response.json();if(!Array.isArray(result))throw new Error("private_ledger_bad_response");
 return result as Record<string,unknown>[];
}
async function owner(c:Cfg,token:string):Promise<{id:string,email:string}|null>{
 if(!/^[A-Za-z0-9_.-]{30,8000}$/.test(token))return null;
 const r=await api(c,"/auth/v1/user",{method:"GET",headers:{"authorization":"Bearer "+token}});
 if(!r.ok)return null;
 const u=await r.json();
 return u.id===c.uid&&u.email===c.email&&u.email_confirmed_at?{id:u.id,email:u.email}:null;
}
function bearer(req:Request){const h=req.headers.get("authorization")??"";
 return h.startsWith("Bearer ")?h.slice(7):"";}
async function issue(c:Cfg,req:Request){
 if(!(await owner(c,bearer(req))))return respond(403,{state:"DENIED"});
 const recent=new Date(Date.now()-60000).toISOString();
 const qs="?owner_uid=eq."+encodeURIComponent(c.uid)+"&created_at=gte."+encodeURIComponent(recent)+"&select=id&limit=1";
 if((await database(c,"GET",qs)).length!==0)return respond(429,{state:"RATE_LIMITED"});
 const now=new Date();
 // A pending expired challenge is never valid for release and must be aged out.
 await database(c,"PATCH","?owner_uid=eq."+encodeURIComponent(c.uid)+
  "&status=eq.pending&expires_at=lt."+encodeURIComponent(now.toISOString()),{status:"expired"});
 const id=crypto.randomUUID(),nonce=randHex(24);
 const preview={host:HOST,project:PROJECT,release:RELEASE,source_commit:c.commit,
  old_pins:OLD_PINS,new_pins:NEW_PINS,production:false,spend:false};
 const manifest_sha256=await hash(canonical(preview));
 const row={id,owner_uid:c.uid,host_id:HOST,project_name:PROJECT,
  source_commit:c.commit,manifest_sha256,nonce_sha256:await hash(nonce),
  expires_at:new Date(now.getTime()+300000).toISOString(),status:"pending"};
 const inserted=await database(c,"POST","?select=id,created_at,expires_at",row);
 if(inserted.length!==1)throw new Error("challenge_insert_failure");
 // This emails the OWNER ONLY, using the existing Auth template. The template
 // must independently be certified to contain BOTH Token and ConfirmationURL.
 const sent=await api(c,"/auth/v1/otp",{method:"POST",body:JSON.stringify({
  email:c.email,create_user:false
 })});
 if(!sent.ok)return respond(503,{state:"EMAIL_DELIVERY_UNVERIFIED"});
 return respond(200,{state:"EMAIL_CHALLENGE_SENT",challenge_id:id,
   nonce,expires_at:row.expires_at,host:HOST,project:PROJECT,
   source_commit:c.commit,manifest_sha256,issue_signature:false});
}
async function linkedIdentity(c:Cfg,req:Request,row:Record<string,unknown>){
 const token=bearer(req);
 if(!(await owner(c,token)))return false;
 // Authentication is confirmed server-side by Supabase /auth/v1/user above.
 // Decode signed GoTrue session *only after* that check to inspect freshness.
 try{
  const b=token.split(".")[1].replace(/-/g,"+").replace(/_/g,"/");
  const claim=JSON.parse(atob(b));
  const issued=Math.floor(new Date(String(row.created_at)).getTime()/1000);
  const amr=Array.isArray(claim.amr)?claim.amr:[];
  const fresh=Number.isInteger(claim.iat)&&claim.iat>=issued;
  const emailFactor=amr.some((v:unknown)=>plain(v)&&["otp","magiclink","email"].includes(String((v as Record<string,unknown>).method)));
  return fresh&&emailFactor;
 }catch{return false;}
}
async function verifyCode(c:Cfg,req:Request,token:string){
 if(!/^[0-9]{6}$/.test(token))return false;
 const resp=await api(c,"/auth/v1/verify",{method:"POST",body:JSON.stringify({
  type:"email",email:c.email,token
 })});
 if(!resp.ok)return false;
 const session=await resp.json();
 if(!session.access_token)return false;
 return !!(await owner(c,String(session.access_token)));
}
function decodePkcs8(s:string){
 if(!/^[A-Za-z0-9+/]+={0,2}$/.test(s)||s.length>5000)throw new Error("bad_signer_key_encoding");
 return Uint8Array.from(atob(s),x=>x.charCodeAt(0));
}
function loadPem(pem:string){
 const b64=pem.replace(/-----BEGIN PUBLIC KEY-----|-----END PUBLIC KEY-----|\s+/g,"");
 const der=Uint8Array.from(atob(b64),x=>x.charCodeAt(0));
 if(der.length!==44||asciiHex(der.subarray(0,12))!=="302a300506032b6570032100")
  throw new Error("bad_ed25519_public_spki");
 return der;
}
async function signAndSelfVerify(c:Cfg,plainText:string){
 const observed=await hash(c.pem);
 if(observed!==c.expected)throw new Error("owner_public_fingerprint_mismatch");
 const privateKey=await crypto.subtle.importKey("pkcs8",decodePkcs8(c.privateKey),
  {name:"Ed25519"},false,["sign"]);
 const pub=await crypto.subtle.importKey("spki",loadPem(c.pem),
  {name:"Ed25519"},false,["verify"]);
 const raw=new Uint8Array(await crypto.subtle.sign("Ed25519",privateKey,encoder.encode(plainText)));
 if(!(await crypto.subtle.verify("Ed25519",pub,raw,encoder.encode(plainText))))
  throw new Error("owner_keypair_mismatch");
 return btoa(String.fromCharCode(...raw));
}
async function complete(c:Cfg,req:Request,kind:"otp"|"link"){
 const body=await req.json();
 if(!plain(body)||Object.keys(body).some(x=>!["challenge_id","nonce","code"].includes(x)))
  return respond(400,{state:"INVALID_REQUEST"});
 const id=String(body.challenge_id??""),nonce=String(body.nonce??"");
 if(!/^[a-f0-9-]{36}$/.test(id)||!/^[a-f0-9]{48}$/.test(nonce))
  return respond(400,{state:"INVALID_CHALLENGE"});
 const rows=await database(c,"GET","?id=eq."+encodeURIComponent(id)+
  "&owner_uid=eq."+encodeURIComponent(c.uid)+"&status=eq.pending&select=*&limit=1");
 if(rows.length!==1)return respond(409,{state:"NOT_PENDING"});
 const row=rows[0];
 if(new Date(String(row.expires_at)).getTime()<=Date.now() ||
   row.host_id!==HOST||row.project_name!==PROJECT||row.source_commit!==c.commit||
   row.nonce_sha256!==await hash(nonce))return respond(409,{state:"CHALLENGE_REJECTED"});
 const verified=kind==="otp" ?
   !!(await owner(c,bearer(req)))&&await verifyCode(c,req,String(body.code??"")):
   await linkedIdentity(c,req,row);
 if(!verified)return respond(403,{state:"OWNER_VERIFICATION_FAILED"});
 // Single SQL UPDATE WHERE pending+unexpired is the atomic winner across code/link.
 const consumed=await database(c,"PATCH","?id=eq."+encodeURIComponent(id)+
  "&owner_uid=eq."+encodeURIComponent(c.uid)+
  "&status=eq.pending&expires_at=gt."+encodeURIComponent(new Date().toISOString())+
  "&select=id,status",{
    status:"consumed",consumed_at:new Date().toISOString(),consumed_method:kind
  });
 if(consumed.length!==1)return respond(409,{state:"ALREADY_CONSUMED"});
 const issue=new Date(),expires=new Date(Math.min(
  issue.getTime()+300000,new Date(String(row.expires_at)).getTime()));
 const payload={
  schema:1,key_id:"DEV_BETA",algorithm:"Ed25519",
  host:HOST,project:PROJECT,release:RELEASE,source_commit:c.commit,
  old_pins:OLD_PINS,new_pins:NEW_PINS,
  release_id:"v4-controller-20261027-"+randHex(16),nonce:randHex(16),
  issued_utc:issue.toISOString(),expires_utc:expires.toISOString(),
  production:false,spend:false,max_activations:1,qa_receipts:QA
 };
 const canonical_json=canonical(payload);
 const detached_signature_base64=await signAndSelfVerify(c,canonical_json);
 return respond(200,{
  state:"ONE_TIME_OWNER_RELEASE_SIGNED",
  approval:canonical_json,signature_base64:detached_signature_base64,
  algorithm:"Ed25519",key_id:"DEV_BETA",host:HOST,production:false,spend:false,
  release_activation_executed:false
 });
}
Deno.serve(async(req)=>{
 const cfg=config();
 const origin=req.headers.get("origin")??"";
 const cors=origin&&origin===cfg.allowedOrigin?origin:"";
 try{
  if(req.method==="OPTIONS")
   return cors?respond(204,{},cors):respond(403,{state:"ORIGIN_DENIED"});
  if(origin && !cors)return respond(403,{state:"ORIGIN_DENIED"});
  if(req.method!=="POST")return respond(404,{state:"NOT_FOUND"});
  if(!cfg.ready)return respond(503,{
   state:"DISABLED",owner_enrolled:false,release_signing_enabled:false
  },cors);
  if(!String(req.headers.get("content-type")??"").startsWith("application/json"))
   return respond(415,{state:"JSON_REQUIRED"},cors);
  const route=new URL(req.url).pathname.split("/").pop();
  const res=route==="begin"?await issue(cfg,req):
    route==="finish-code"?await complete(cfg,req,"otp"):
    route==="finish-link"?await complete(cfg,req,"link"):
    respond(404,{state:"NOT_FOUND"});
  // Add allowed origin only, never wildcard; don't log email or approval bytes.
  if(cors){const h=new Headers(res.headers);h.set("access-control-allow-origin",cors);
   h.set("vary","Origin");h.set("access-control-allow-headers","authorization,content-type");
   return new Response(res.body,{status:res.status,headers:h});}
  return res;
 }catch{return respond(503,{state:"DENIED",reason:"server_verification_failed"},cors);}
});
