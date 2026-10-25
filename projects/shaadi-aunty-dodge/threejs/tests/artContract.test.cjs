const {test}=require('node:test');
const assert=require('node:assert/strict');
const {createHash,webcrypto}=require('node:crypto');
const open=()=>import('../src/artContract.js');
const sha=s=>'a'.repeat(64);
const base=()=>({
 quality_gate_id:'SAD-VISUAL-QUALITY-V1',
 owner_approval:{approved:true,receipt:'owner-record-not-self-certified',approved_hashes:{character:sha(),venue:sha()}},
 character:{uri:'assets/sharma_v1.glb',sha256:sha(),certified:true,
   license:{source:'MPFB2',terms:'CC0'},independent_qa:{pass:true,evidence_sha256:sha()},
   required_animations:['Idle','Walk','Question','DodgeReaction'],
   required_morph_targets:['Blink','Smile','JawOpen']},
 venue:{uri:'assets/wedding_v1.glb',sha256:sha(),certified:true,
   license:{source:'Kenney',terms:'CC0'},independent_qa:{pass:true,evidence_sha256:sha()}},
 mobile_qa:{passed:true,evidence_sha256:sha()}
});
test('unapproved and previous loose manifest fail closed',async()=>{
 const {assessArtManifest}=await open();
 assert.equal(assessArtManifest(null).approved,false);
 assert.equal(assessArtManifest({character:{approved:true,uri:'assets/a.glb'}}).approved,false);
 const p=base();p.owner_approval.approved=false;
 assert.equal(assessArtManifest(p).approved,false);
});
test('mismatched owner-approved hash and no venue block release',async()=>{
 const {assessArtManifest}=await open();const p=base();
 p.owner_approval.approved_hashes.venue='f'.repeat(64);
 assert.ok(assessArtManifest(p).issues.includes('owner_approval:asset_hash_mismatch'));
 delete p.venue;
 assert.equal(assessArtManifest(p).approved,false);
});
test('complete *synthetic* manifest passes only schema, not actual artistic certification',async()=>{
 const {assessArtManifest}=await open();
 const p=base();assert.equal(assessArtManifest(p).approved,true);
 p.character.uri='https://evil.example/asset.glb';
 assert.equal(assessArtManifest(p).approved,false);
});
test('GLB hash verification rejects byte substitution',async()=>{
 const {verifiedGLB}=await open();
 const bytes=new Uint8Array([0x67,0x6c,0x54,0x46,0,0,0,0]);
 const good=createHash('sha256').update(bytes).digest('hex');
 const fetchImpl=async()=>({ok:true,arrayBuffer:async()=>bytes.buffer});
 assert.deepEqual([...new Uint8Array(await verifiedGLB('assets/a.glb',good,{fetchImpl,subtle:webcrypto.subtle}))],[...bytes]);
 await assert.rejects(()=>verifiedGLB('assets/a.glb','b'.repeat(64),{fetchImpl,subtle:webcrypto.subtle}),/mismatch/);
 await assert.rejects(()=>verifiedGLB('https://remote.example/a.glb',good,{fetchImpl,subtle:webcrypto.subtle}),/same-origin/);
});
test('skinning+clips+morph controls required from actual parsed GLTF',async()=>{
 const {inspectCharacterGLTF}=await open();
 const fake={animations:[{name:'Idle'},{name:'Walk'},{name:'Question'},{name:'DodgeReaction'}],
  scene:{traverse:fn=>fn({isSkinnedMesh:true,skeleton:{bones:Array(53)},morphTargetDictionary:{Blink:1,Smile:2,JawOpen:3}})}};
 assert.equal(inspectCharacterGLTF(fake).passed,true);
 fake.animations=[{name:'Idle'}];
 assert.equal(inspectCharacterGLTF(fake).passed,false);
 assert.deepEqual(inspectCharacterGLTF(fake).missingClips,['Walk','Question','DodgeReaction']);
});
