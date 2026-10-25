// Deterministic, renderer-independent 10-second interaction contract.
export const DURATION=10;
export const AUNTY={appear:2.8,hit:5.3,leave:7.2,lane:0};
export const limit=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));
export function createSession(seed=26025){
  return {seed,t:0,lane:0,roll:0,hearts:3,score:0,resolved:false,result:'',phase:'ready',hits:0,dodges:0};
}
export function action(s,a){
  if(s.phase!=='play')return;
  if(a==='left')s.lane=limit(s.lane-1,-1,1);
  if(a==='right')s.lane=limit(s.lane+1,-1,1);
  if(a==='roll'&&s.roll<=0)s.roll=0.72;
}
export function step(s,dt){
  if(s.phase!=='play')return s;
  const prev=s.t;
  s.t=Math.min(DURATION,s.t+limit(dt,0,0.1));
  s.roll=Math.max(0,s.roll-dt);
  if(!s.resolved&&prev<AUNTY.hit&&s.t>=AUNTY.hit){
    s.resolved=true;
    if(s.lane===AUNTY.lane&&s.roll<=0){
      s.hearts--;s.hits++;s.result='caught';s.score=Math.max(0,s.score-20);
    } else {s.dodges++;s.score+=100;s.result='dodged';}
  }
  if(s.t>=DURATION){s.phase='done';if(s.dodges>0)s.score+=50;}
  return s;
}
export function auntyPosition(t){
  if(t<AUNTY.appear)return -28;
  if(t>AUNTY.leave)return 8;
  return -17+(t-AUNTY.appear)/(AUNTY.hit-AUNTY.appear)*17;
}

