import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import process from 'node:process';
const root=path.resolve(process.cwd(),'qa-preview');
function load(file){return JSON.parse(fs.readFileSync(path.join(root,file),'utf8'))}
const manifest=load('checksums.json');
for(const [f,expected] of Object.entries(manifest.files)){
 if(!/^[a-zA-Z0-9_./-]+$/.test(f)||f.includes('..'))throw Error('invalid_manifest_path');
 const full=path.join(root,f);
 if(!fs.statSync(full).isFile())throw Error('missing_asset:'+f);
 const got=crypto.createHash('sha256').update(fs.readFileSync(full)).digest('hex');
 if(got!==expected)throw Error('tampered_or_unchecked:'+f);
}
const b=load('review/browser_qa.json'),s=load('review/style_gate.json'),a=load('review/first_attempt.json'),p=load('review/predeploy_test.json'),r=load('review/release.json');
if(!(b.passed===true && b.pass_count===36 && b.total===36 && Array.isArray(b.checks)&&b.checks.length===36))throw Error('browser_gate_failed');
if(!(s.pass===true && s.passed===8 && s.total===8))throw Error('brand_gate_failed');
if(!(a.first_output_qa_passed===true && a.generation_count===1 && a.retry_count===0))throw Error('first_generation_gate_failed');
if(!(p.pass===true && Array.isArray(p.checks) && p.checks.length===4 && p.checks.every(x=>x.pass)))throw Error('cloud_preview_preflight_failed');
if(!(r.constraints?.art_lanes_frozen && !r.constraints?.owner_approved && !r.constraints?.production_merge))throw Error('owner_freeze_or_scope_failed');
if(!fs.readFileSync(path.join(root,'scene.js'),'utf8').includes('three@0.186.1'))throw Error('unapproved_dependency');
if(fs.existsSync(path.join(root,'vendor')))throw Error('unexpected_worker_artifacts');
console.log('SHAADI_PREVIEW_QUALITY_GATE_PASS',Object.keys(manifest.files).length,'files',b.total,'browser',s.total,'style');
