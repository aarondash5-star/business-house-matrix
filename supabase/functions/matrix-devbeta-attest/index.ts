// Matrix DEV_BETA owner keypair verifier. Fail closed; NEVER signs release payloads.
// No customer data, no secret exports, no mutable remote shell or deployment actions.
// Deliberately DISABLED unless owner-scoped environment and public PEM are independently enrolled.
const HEADERS: Record<string,string> = {"content-type":"application/json","cache-control":"no-store, private","x-content-type-options":"nosniff"};
const PROJECT = "matrix_dev_manager";
const allowedHosts = new Set(["dell-linux","mac-linux"]);
const decoder = new TextEncoder();
function response(status:number, body:Record<string,unknown>) {
  return new Response(JSON.stringify(body),{status,headers:HEADERS});
}
function encodeHex(bytes:Uint8Array) {return Array.from(bytes,x=>x.toString(16).padStart(2,"0")).join("");}
function parsePublicPem(pem:string) {
  const format=/^-----BEGIN PUBLIC KEY-----\n([A-Za-z0-9+/]{59}=)\n-----END PUBLIC KEY-----\n$/;
  const m=pem.match(format);
  if(!m) throw new Error("public_pem_format_invalid");
  const der=Uint8Array.from(atob(m[1]),x=>x.charCodeAt(0));
  if(der.length!==44 || encodeHex(der.subarray(0,12))!=="302a300506032b6570032100") throw new Error("not_ed25519_spki");
  return der;
}
function decodeSecret(encoded:string) {
  if(!/^[A-Za-z0-9+/]+={0,2}$/.test(encoded)||encoded.length>5000) throw new Error("invalid_private_key_format");
  return Uint8Array.from(atob(encoded),x=>x.charCodeAt(0));
}
async function authenticatedOwner(req:Request,ownerUid:string):Promise<boolean>{
  const header=req.headers.get("authorization")??"";
  if(!/^Bearer [A-Za-z0-9_\-.]+$/.test(header)) return false;
  const sbUrl=Deno.env.get("SUPABASE_URL");
  const apikey=Deno.env.get("SUPABASE_ANON_KEY");
  if(!sbUrl||!apikey) return false;
  const u=await fetch(sbUrl+"/auth/v1/user",{headers:{authorization:header,apikey},signal:AbortSignal.timeout(4000)});
  if(!u.ok) return false;
  const user=await u.json();
  return user.id===ownerUid && !!user.email_confirmed_at;
}
Deno.serve(async req=>{
  try{
    if(req.method==="GET" && new URL(req.url).pathname.endsWith("/health")){
      // Gateway verify_jwt=true protects this even in disabled state.
      return response(200,{component:"matrix-devbeta-attest",enabled:false,host_release_enabled:false,release_signing_enabled:false});
    }
    if(req.method!=="POST" || !new URL(req.url).pathname.endsWith("/attest"))
      return response(404,{error:"not_found"});
    if(Deno.env.get("MATRIX_DEV_BETA_ATTEST_ENABLED")!=="true")
      return response(503,{state:"DISABLED",reason:"owner_enrollment_incomplete"});
    const ownerUid=Deno.env.get("MATRIX_DEV_BETA_OWNER_UID");
    if(!ownerUid || !/^[a-f0-9-]{36}$/.test(ownerUid))
      return response(503,{state:"DISABLED",reason:"owner_uuid_not_enrolled"});
    if(!(await authenticatedOwner(req,ownerUid)))
      return response(403,{state:"DENIED",reason:"unauthorized_owner"});
    const obj=await req.json();
    if(!obj || obj.project!==PROJECT || !allowedHosts.has(obj.host_id) || Object.keys(obj).sort().join(",")!=="host_id,project")
      return response(400,{state:"DENIED",reason:"invalid_scope"});
    const pem=Deno.env.get("MATRIX_DEV_BETA_PUBLIC_PEM")??"";
    const expected=(Deno.env.get("MATRIX_DEV_BETA_PUBLIC_SHA256")??"").toLowerCase();
    if(!/^[a-f0-9]{64}$/.test(expected) || !pem)
      return response(503,{state:"DISABLED",reason:"public_key_not_enrolled"});
    const publicDer=parsePublicPem(pem);
    const digest=encodeHex(new Uint8Array(await crypto.subtle.digest("SHA-256",decoder.encode(pem))));
    if(digest!==expected)
      return response(409,{state:"DENIED",reason:"public_key_fingerprint_mismatch"});
    const encoded=Deno.env.get("DEV_BETA_ED25519_PRIVATE_PKCS8_B64");
    if(!encoded) return response(503,{state:"DISABLED",reason:"private_key_not_available"});
    const privateKey=await crypto.subtle.importKey("pkcs8",decodeSecret(encoded),{name:"Ed25519"},false,["sign"]);
    const publicKey=await crypto.subtle.importKey("spki",publicDer,{name:"Ed25519"},false,["verify"]);
    const challenge=new Uint8Array(48);
    crypto.getRandomValues(challenge);
    const prefix=decoder.encode("matrix-devbeta-keypair-attestation-v1;not-a-release-signature;");
    const bytes=new Uint8Array(prefix.length+challenge.length);
    bytes.set(prefix);bytes.set(challenge,prefix.length);
    const sig=await crypto.subtle.sign("Ed25519",privateKey,bytes);
    const matches=await crypto.subtle.verify("Ed25519",publicKey,sig,bytes);
    return response(matches?200:409,{
      state:matches?"VERIFIED_KEYPAIR":"KEYPAIR_MISMATCH",
      key_id:"DEV_BETA",fingerprint:matches?expected:null,
      host_id:obj.host_id,project:PROJECT,
      release_approved:false,release_signed:false,host_trust_installed:false,
      host_release_enabled:false
    });
  } catch {
    return response(400,{state:"DENIED",reason:"invalid_request_or_unverified_keypair"});
  }
});
