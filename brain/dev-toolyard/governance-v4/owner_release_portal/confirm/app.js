"use strict";
// This PUBLIC Supabase publishable key is designed for browser clients.
// No owner identifiers, privileged credentials or secret signing material are embedded.
const AUTH="https://saczglesalubroyaucqe.supabase.co";
const PUBLISHABLE="sb_publishable_QWn0aEO4-fHulmZaUacbIQ_1ejYsDXY";
const el=id=>document.getElementById(id);
let jwt="",verifiedPublic=null;
const cleanFragment=()=>{
 const fragment=window.location.hash.replace(/^#/,"");
 if(!fragment)return null;
 // Strip auth credentials from navigation history immediately; never log them.
 history.replaceState(null,"",window.location.pathname);
 const parsed=new URLSearchParams(fragment);
 const access=parsed.get("access_token");
 return access&&/^[A-Za-z0-9._-]{30,8000}$/.test(access)?access:null;
};
function status(message){el("status").textContent=message;}
async function unlock(token){
 // Never trust a token or a decoded JWT claim on the client by itself.
 // Verify the existing owner identity against the private registry on Supabase.
 jwt="";el("derive").disabled=true;el("reviewPanel").hidden=true;
 status("Checking the authenticated owner's identity against Supabase...");
 try{
  const r=await api("/functions/v1/matrix-devbeta-public-attest/owner-session",{
   host_id:"dell-linux",project:"matrix_dev_manager"
  },token);
  if(!r.ok||r.json.state!=="VERIFIED_EXISTING_OWNER"){
   el("identityStatus").textContent="The session was not verified as the enrolled owner.";
   status("Owner authentication not verified. Release signing remains disabled.");return;
  }
  jwt=token;el("derive").disabled=false;el("reviewPanel").hidden=false;
  el("identityStatus").textContent="Verified existing owner. You can review the authentication UI here.";
  status("Supabase owner authentication confirmed. No release signed or deployed.");
 }catch{
  el("identityStatus").textContent="Owner session verification unavailable.";
  status("Authentication check failed; no release action is possible.");
 }
}
async function api(path,body,token=""){
 const headers={"content-type":"application/json","apikey":PUBLISHABLE};
 if(token)headers.authorization="Bearer "+token;
 const response=await fetch(AUTH+path,{method:"POST",headers,body:JSON.stringify(body),
  cache:"no-store",credentials:"omit",referrerPolicy:"no-referrer"});
 const json=await response.json().catch(()=>({}));
 return {ok:response.ok,status:response.status,json};
}
el("send").addEventListener("click",async()=>{
 const email=el("email").value.trim();
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){status("Enter your verified email.");return;}
 el("send").disabled=true;status("Requesting an existing-account email from Supabase...");
 try{
  const redirect=window.location.origin+window.location.pathname;
  const r=await api("/auth/v1/otp?redirect_to="+encodeURIComponent(redirect),{
    email,create_user:false
  });
  status(r.ok?"Check your inbox. Use the code or sign-in link supplied by Supabase.":`Supabase email request was not accepted (HTTP ${r.status}). Check email configuration or delivery limits.`);
 }catch{status("Email request could not be completed.")}
 finally{el("send").disabled=false;}
});
el("verify").addEventListener("click",async()=>{
 const email=el("email").value.trim(),code=el("code").value.trim();
 if(!/^[0-9]{6,8}$/.test(code)||!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){status("Enter the owner email and numeric code.");return;}
 el("verify").disabled=true;status("Verifying the code with Supabase...");
 try{
  const r=await api("/auth/v1/verify",{type:"email",email,token:code});
  if(r.ok&&typeof r.json.access_token==="string")unlock(r.json.access_token);
  else status("The email code was not verified by Supabase.");
 }catch{status("Code verification was unavailable.")}
 finally{el("verify").disabled=false;el("code").value="";}
});
el("derive").addEventListener("click",async()=>{
 if(!jwt)return;
 el("derive").disabled=true;status("Checking the DEV_BETA public key through the owner-restricted attestation service...");
 try{
  const r=await api("/functions/v1/matrix-devbeta-public-attest/derive-public",{
   host_id:"dell-linux",project:"matrix_dev_manager"
  },jwt);
  if(!r.ok||r.json.state!=="PUBLIC_KEY_DERIVED_AND_PROVED"){
   status(`Attestation not certified (HTTP ${r.status}). Release signing remains disabled.`);return;
  }
  verifiedPublic={public_pem:r.json.public_pem,fingerprint_sha256:r.json.fingerprint_sha256};
  el("pem").textContent=verifiedPublic.public_pem;
  el("fingerprint").textContent=verifiedPublic.fingerprint_sha256;
  el("result").hidden=false;
  status("DEV_BETA public-key possession verified by Supabase. No release signed. Dell remains unchanged.");
 }catch{status("Could not verify keypair. Check approved origin and owner session.")}
 finally{el("derive").disabled=!jwt;}
});
el("copy").addEventListener("click",async()=>{
 if(!verifiedPublic)return;
 await navigator.clipboard.writeText(verifiedPublic.public_pem+"\nSHA256(PEM)="+verifiedPublic.fingerprint_sha256);
 status("Only public-key material copied. No private key was accessed by the browser.");
});
// A custom GoTrue email-link template can deliver a token_hash here.
// Do not consume it on page load: email link scanners may prefetch GET URLs.
const query=new URLSearchParams(window.location.search);
let pendingHash=query.get("token_hash")??"";
if(query.has("token_hash"))history.replaceState(null,"",window.location.pathname);
if(/^[A-Za-z0-9._-]{20,512}$/.test(pendingHash)&&query.get("type")==="email"){
 el("confirmLink").hidden=false;
 status("Email link received. Press Confirm email link to verify it with Supabase. No release action will run.");
}else pendingHash="";
el("confirmLink").addEventListener("click",async()=>{
 if(!pendingHash)return;
 el("confirmLink").disabled=true;status("Verifying the email link through Supabase...");
 try{
  const r=await api("/auth/v1/verify",{type:"email",token_hash:pendingHash});
  pendingHash="";
  el("confirmLink").hidden=true;
  if(r.ok&&typeof r.json.access_token==="string")unlock(r.json.access_token);
  else status("Supabase did not verify this email link. Request another link/code.");
 }catch{pendingHash="";el("confirmLink").hidden=true;status("Link verification unavailable. Request another code.");}
});
async function submitUiReview(decision){
 if(!jwt)return;
 if(!["ui_acceptable","needs_changes"].includes(decision))return;
 el("uiAccept").disabled=true;el("uiNeeds").disabled=true;
 status("Saving UI feedback to the owner-only review register...");
 try{
  const r=await api("/functions/v1/matrix-devbeta-public-attest/review",{
    host_id:"dell-linux",project:"matrix_dev_manager",decision,
    notes:el("reviewNotes").value.trim().slice(0,500)
  },jwt);
  if(r.ok&&r.json.state==="UI_REVIEW_RECORDED"){
   status("UI review recorded. This does not authorize signing or Dell deployment.");
  }else status("UI review could not be saved. Authentication and release remain separate.");
 }catch{status("UI review submission unavailable.")}
 finally{el("uiAccept").disabled=false;el("uiNeeds").disabled=false;}
}
el("uiAccept").addEventListener("click",()=>submitUiReview("ui_acceptable"));
el("uiNeeds").addEventListener("click",()=>submitUiReview("needs_changes"));
const linkToken=cleanFragment();
if(linkToken)unlock(linkToken);
