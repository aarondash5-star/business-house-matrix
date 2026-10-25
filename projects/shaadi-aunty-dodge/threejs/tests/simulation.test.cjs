const {test}=require('node:test');const assert=require('node:assert/strict');
const sim=()=>import('../src/simulation.js');
test('exact 10s deterministic result and single obstacle',async()=>{
 const {createSession,step}=await sim();const s=createSession(26);s.phase='play';
 for(let i=0;i<600;i++)step(s,1/60);
 assert.equal(s.phase,'done');assert.ok(Math.abs(s.t-10)<1e-6);assert.equal(s.hits,1);
 assert.equal(s.dodges,0);assert.equal(s.score,0);
});
test('one deliberate lane change dodges character and score is stable',async()=>{
 const {createSession,step,action}=await sim();const s=createSession(26);s.phase='play';
 action(s,'right');for(let i=0;i<600;i++)step(s,1/60);
 assert.equal(s.phase,'done');assert.equal(s.hits,0);assert.equal(s.dodges,1);assert.equal(s.score,150);
});
test('roll in collision window counts as dodge',async()=>{
 const {createSession,step,action}=await sim();const s=createSession(1);s.phase='play';
 for(let i=0;i<302;i++)step(s,1/60);
 action(s,'roll');for(let i=302;i<600;i++)step(s,1/60);
 assert.equal(s.dodges,1);assert.equal(s.hits,0);
});
test('no interaction before start, no out-of-bounds lanes',async()=>{
 const {createSession,action}=await sim();const s=createSession();
 action(s,'right');assert.equal(s.lane,0);s.phase='play';for(let i=0;i<7;i++)action(s,'left');assert.equal(s.lane,-1);
 for(let i=0;i<7;i++)action(s,'right');assert.equal(s.lane,1);
});

