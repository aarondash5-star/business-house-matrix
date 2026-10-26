// Owner-authenticated DEV_BETA *public* key derivation and possession test.
// No release signatures, no arbitrary message signing, no host actions.
// The existing DEV_BETA private key remains inside Supabase environment.
import { Buffer } from "node:buffer";
import { createPrivateKey, createPublicKey, sign, verify, createHash } from "node:crypto";

const sbUrl=Deno.env.get("SUPABASE_URL")??"";
const anon=Deno.env.get("SUPABASE_ANON_KEY")??"";
const service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")??"";
const HOST="dell-linux";
const PROJECT="matrix_dev_manager";
const OWNER_PORTAL_ORIGIN="https://matrix-owner-key-preview.vercel.app";
const HEADERS={"content-type":"application/json","cache-control":"no-store","x-content-type-options":"nosniff","referrer-policy":"no-referrer"};
function reply(code:number,body:Record<string,unknown>,origin=""){
 const headers=new Headers(HEADERS);
 if(origin) {headers.set("access-control-allow-origin",origin);headers.set("vary","Origin");headers.set("access-control-allow-headers","authorization,apikey,content-type");headers.set("access-control-allow-methods","POST,OPTIONS");}
 return new Response(JSON.stringify(body),{status:code,headers});
}
async function ownerSession(req:Request):Promise<string|null>{
 const authorization=req.headers.get("authorization")??"";
 if(!/^Bearer [A-Za-z0-9._-]{30,8000}$/.test(authorization)||!sbUrl.startsWith("https://")||!anon||!service)return null;
 const [id,auth]=await Promise.all([
  fetch(sbUrl+"/rest/v1/matrix_v4_owner_registry?host_id=eq.dell-linux&project_name=eq.matrix_dev_manager&identity_enrolled=eq.true&release_signing_enabled=eq.false&select=owner_uid,owner_email&limit=2",
   {headers:{apikey:service,authorization:"Bearer "+service},signal:AbortSignal.timeout(5000)}),
  fetch(sbUrl+"/auth/v1/user",{headers:{apikey:anon,authorization},signal:AbortSignal.timeout(5000)})
 ]);
 if(!id.ok||!auth.ok)return null;
 const rows=await id.json(),user=await auth.json();
 const verified=Array.isArray(rows)&&rows.length===1&&rows[0].owner_uid===user.id
  &&rows[0].owner_email===user.email&&!!user.email_confirmed_at;
 return verified?String(user.id):null;
}
function deriveOnlyPublic() {
 const b64=Deno.env.get("DEV_BETA_ED25519_PRIVATE_PKCS8_B64")??"";
 if(!/^[A-Za-z0-9+/]+={0,2}$/.test(b64)||b64.length>5000)
  throw new Error("private_key_unavailable");
 const pk=createPrivateKey({key:Buffer.from(b64,"base64"),format:"der",type:"pkcs8"});
 if(pk.asymmetricKeyType!=="ed25519")throw new Error("wrong_key_algorithm");
 const pub=createPublicKey(pk);
 // This random challenge is generated and verified entirely inside the server.
 // Its signature is not returned and cannot approve any deployment.
 const challenge=Buffer.alloc(64);crypto.getRandomValues(challenge);
 const signed=sign(null,challenge,pk);
 if(!verify(null,challenge,pub,signed))throw new Error("proof_failed");
 const pem=String(pub.export({format:"pem",type:"spki"})).replace(/\r\n/g,"\n");
 if(!/^-----BEGIN PUBLIC KEY-----\n[A-Za-z0-9+/]{59}=\n-----END PUBLIC KEY-----\n$/.test(pem))
   throw new Error("bad_spki");
 return {public_pem:pem,fingerprint_sha256:createHash("sha256").update(pem).digest("hex")};
}
Deno.serve(async req=>{
 try{
  const route=new URL(req.url).pathname.split("/").pop()??"";
  const origin=req.headers.get("origin")??"";
  // Explicit fixed origin for this public-proof portal. No generic browser origins,
  // dynamic caller-supplied redirects, or release-signing capability.
  const permitted=OWNER_PORTAL_ORIGIN;
  if(origin && (!permitted||origin!==permitted))return reply(403,{state:"ORIGIN_DENIED"});
  if(req.method==="OPTIONS"){
   if(!origin||origin!==permitted)return reply(403,{state:"ORIGIN_DENIED"});
   const h=new Headers(HEADERS);h.set("access-control-allow-origin",origin);
   h.set("access-control-allow-headers","authorization,apikey,content-type");
   h.set("access-control-allow-methods","POST,OPTIONS");h.set("vary","Origin");
   return new Response(null,{status:204,headers:h});
  }
  if(req.method!=="POST"||!["derive-public","owner-session","review"].includes(route))return reply(404,{state:"NOT_FOUND"});
  if(req.headers.get("content-type")?.split(";")[0]!=="application/json")
   return reply(415,{state:"JSON_REQUIRED"});
  const body=await req.json();
  if(!body||typeof body!=="object"||Array.isArray(body)||
    body.host_id!==HOST||body.project!==PROJECT)return reply(400,{state:"SCOPE_DENIED"},origin);
  const exactKeys=Object.keys(body).sort().join(",");
  if(route==="review" ? exactKeys!=="decision,host_id,notes,project" : exactKeys!=="host_id,project")
   return reply(400,{state:"INVALID_FIELDS"},origin);
  const verifiedUid=await ownerSession(req);
  if(!verifiedUid)return reply(403,{state:"OWNER_AUTH_REQUIRED"},origin);
  if(route==="review"){
   if(!["ui_acceptable","needs_changes"].includes(body.decision)||
      typeof body.notes!=="string"||body.notes.length>500)
      return reply(400,{state:"INVALID_REVIEW"},origin);
   const inserted=await fetch(sbUrl+"/rest/v1/matrix_v4_owner_ui_reviews",{
    method:"POST",headers:{apikey:service,authorization:"Bearer "+service,
      "content-type":"application/json",prefer:"return=minimal"},
    body:JSON.stringify({owner_uid:verifiedUid,host_id:HOST,project_name:PROJECT,
      decision:body.decision,notes:body.notes,release_approved:false}),
    signal:AbortSignal.timeout(5000)
   });
   if(!inserted.ok)return reply(503,{state:"REVIEW_STORE_UNAVAILABLE"},origin);
   return reply(200,{state:"UI_REVIEW_RECORDED",host:HOST,project:PROJECT,
     release_approved:false,release_signed:false,can_activate:false},origin);
  }
  // Auth-only review is independent of DEV_BETA private-key enrollment.
  if(route==="owner-session")return reply(200,{
   state:"VERIFIED_EXISTING_OWNER",host:HOST,project:PROJECT,
   email_confirmed:true,approval_challenge_created:false,
   release_signed:false,host_trust_installed:false,can_activate:false
  },origin);
  const pub=deriveOnlyPublic();
  return reply(200,{state:"PUBLIC_KEY_DERIVED_AND_PROVED",key_id:"DEV_BETA",
   host:HOST,project:PROJECT,...pub,release_signed:false,host_trust_installed:false,can_activate:false},origin);
 }catch{return reply(503,{state:"NO_KEY_ATTESTATION",release_signed:false,can_activate:false});}
});
