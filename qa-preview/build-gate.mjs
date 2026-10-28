import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
const root=path.resolve(process.cwd(),'qa-preview');
const load=x=>JSON.parse(fs.readFileSync(path.join(root,x),'utf8'));
const manifest=load('checksums.json');
if(manifest.format!==3||manifest.version!=='lane1-sprint-all-work-20261028')throw Error('wrong_release_version');
for(const [rel,hash] of Object.entries(manifest.files)){
 if(!/^[a-zA-Z0-9_./-]+$/.test(rel)||rel.includes('..'))throw Error('invalid_asset_path:'+rel);
 const actual=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,rel))).digest('hex');
 if(actual!==hash)throw Error('tampered_or_unchecked:'+rel);
}
const actualFiles=fs.readdirSync(root,{recursive:true,withFileTypes:true}).filter(x=>x.isFile()).length-2;
if(actualFiles!==Object.keys(manifest.files).length)throw Error('unverified_file_count');
const b=load('review/browser_qa.json'),u=load('review/streak_unit.json'),legacy=load('review/style_gate.json'),style=load('review/streak_style_gate.json'),v=load('review/viewport_qa.json'),first=load('review/first_attempt.json'),live=load('review/predeploy_test.json'),release=load('review/release.json');
if(!b.passed||b.pass_count!==52||b.total!==52||!u.passed||u.pass_count!==16||u.total!==16)throw Error('existing_feature_quality_missing');
if(!legacy.pass||legacy.passed!==8||!style.pass||style.passed!==9)throw Error('existing_style_quality_missing');
if(!v.pass||v.checks?.length!==3||!first.first_output_qa_passed||first.generation_count!==1||first.retry_count!==0)throw Error('existing_first_output_missing');
if(!live.pass||live.checks?.length!==4||!live.checks.every(x=>x.pass))throw Error('existing_smoke_missing');
if(!release.art_lanes_frozen||release.owner_approved!==false||release.production_merge!==false)throw Error('owner_scope_invalid');
const sprint=load('sprint/status.json'),smoke=load('sprint/browser_qa.json');
if(sprint.session_status!=='STOPPED_AT_DEADLINE'||sprint.local_pass!==5||sprint.quarantined!==1||sprint.tasks.length!==6||!sprint.frozen_art_lanes&&sprint.art_lanes!=='OWNER_FROZEN')throw Error('sprint_receipt_bad');
if(!smoke.all||smoke.checks.length!==5||!smoke.checks.every(x=>x.ok))throw Error('sprint_browser_qa_failed');
const qualified=sprint.tasks.filter(x=>x.playable),blocked=sprint.tasks.filter(x=>!x.playable);
if(qualified.length!==2||blocked.length!==4||!blocked.some(x=>x.id==='finale-energy'&&x.status==='QUARANTINED')||sprint.local_pass!==5||sprint.quarantined!==1)throw Error('quality_quarantine_failed');
for(const x of qualified){
 for(const file of ['index.html','scene.js','features/mission.js','features/mission-ui.js','features/mission.css'])if(!manifest.files['sprint/'+x.id+'/'+file])throw Error('missing_'+x.id+'_'+file);
 if(x.status!=='LOCAL_PASS'||!x.commit)throw Error('uncertified_published_variant');
}
for(const x of blocked)if(manifest.files['sprint/'+x.id+'/index.html']||manifest.files['sprint/'+x.id+'/scene.js'])throw Error('unreleased_source_published:'+x.id);
console.log('SHAADI_SPRINT_ALL_WORK_GATE_PASS',Object.keys(manifest.files).length,'files',qualified.length,'playable',blocked.length,'quarantined',smoke.checks.length,'browser smoke');
