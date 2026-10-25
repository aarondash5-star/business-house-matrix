/**
 * SAD-VISUAL-QUALITY-V1. This is a *fail-closed client-side safeguard*, NOT a
 * substitute for independent QA, cryptographically signed owner approval or
 * production release authorization.
 */
export const QUALITY_GATE_ID='SAD-VISUAL-QUALITY-V1';
const HEX64=/^[a-f0-9]{64}$/i;
const allowedUri=/^\.?(?:\/)?assets\/[a-zA-Z0-9/_-]+\.glb$/;
const requiredClips=['Idle','Walk','Question','DodgeReaction'];
const requiredMorphs=['Blink','Smile','JawOpen'];

function checkAsset(issues,asset,field) {
 if(!asset||typeof asset!=='object'){issues.push(field+':missing');return;}
 if(asset.certified!==true)issues.push(field+':not_certified');
 if(!allowedUri.test(asset.uri||''))issues.push(field+':unsafe_uri');
 if(!HEX64.test(asset.sha256||''))issues.push(field+':missing_sha256');
 if(!asset.license?.source||!asset.license?.terms)issues.push(field+':missing_provenance');
 if(!asset.independent_qa?.pass || !asset.independent_qa?.evidence_sha256 ||
    !HEX64.test(asset.independent_qa.evidence_sha256))issues.push(field+':independent_qa_missing');
}
export function assessArtManifest(manifest) {
 const issues=[];
 if(!manifest||typeof manifest!=='object')return {approved:false,issues:['manifest:missing']};
 if(manifest.quality_gate_id!==QUALITY_GATE_ID)issues.push('quality_gate:wrong_or_missing');
 if(manifest.owner_approval?.approved!==true||
    !manifest.owner_approval?.receipt||
    !manifest.owner_approval?.approved_hashes?.character||
    !manifest.owner_approval?.approved_hashes?.venue)issues.push('owner_approval:missing');
 checkAsset(issues,manifest.character,'character');
 checkAsset(issues,manifest.venue,'venue');
 if(manifest.character){
   if(!requiredClips.every(c=>manifest.character.required_animations?.includes(c)))
     issues.push('character:required_animation_manifest_incomplete');
   if(!requiredMorphs.every(m=>manifest.character.required_morph_targets?.includes(m)))
     issues.push('character:facial_control_manifest_incomplete');
 }
 if(manifest.mobile_qa?.passed!==true ||
    !manifest.mobile_qa?.evidence_sha256||
    !HEX64.test(manifest.mobile_qa.evidence_sha256))issues.push('mobile_qa:not_certified');
 if(manifest.owner_approval?.approved_hashes?.character!==manifest.character?.sha256 ||
    manifest.owner_approval?.approved_hashes?.venue!==manifest.venue?.sha256)
   issues.push('owner_approval:asset_hash_mismatch');
 return {approved:issues.length===0,issues};
}
/**
 * Verify the actual downloaded GLB bytes. The output is handed directly to the
 * Three.js GLTFLoader; never perform a second unchecked download.
 */
export async function verifiedGLB(uri,sha256,{fetchImpl=fetch,subtle=globalThis.crypto?.subtle}={}) {
 if(!allowedUri.test(uri))throw new Error('Only same-origin assets/*.glb allowed');
 if(!HEX64.test(sha256))throw new Error('Missing pinned GLB SHA256');
 if(!subtle)throw new Error('WebCrypto unavailable: fail closed');
 const response=await fetchImpl(uri,{cache:'no-store',credentials:'same-origin'});
 if(!response.ok)throw new Error('GLB fetch error '+response.status);
 const bytes=await response.arrayBuffer();
 const hash=Array.from(new Uint8Array(await subtle.digest('SHA-256',bytes)))
  .map(b=>b.toString(16).padStart(2,'0')).join('');
 if(hash.toLowerCase()!==sha256.toLowerCase())throw new Error('GLB SHA256 mismatch');
 if(new DataView(bytes).getUint32(0,true)!==0x46546c67)throw new Error('Not binary glTF');
 return bytes;
}
/**
 * Runtime validation; manifest cannot claim animations/eyes that GLB lacks.
 * Materials and artistic likeness still require independent visual inspection.
 */
export function inspectCharacterGLTF(gltf) {
 const foundClips=gltf?.animations?.map(x=>x.name)??[];
 const morphs=new Set();let skinned=0,bones=0;
 gltf?.scene?.traverse?.(obj=>{
  if(obj.isSkinnedMesh){skinned++;bones=Math.max(bones,obj.skeleton?.bones?.length||0);}
  for(const name of Object.keys(obj.morphTargetDictionary||{}))morphs.add(name);
 });
 const missingClips=requiredClips.filter(x=>!foundClips.includes(x));
 const missingMorphs=requiredMorphs.filter(x=>!morphs.has(x));
 return {passed:skinned>0&&bones>=35&&missingClips.length===0&&missingMorphs.length===0,
  skinned,bones,missingClips,missingMorphs,foundClips:[...foundClips]};
}
