const root=document.getElementById('cards');
try{
const response=await fetch('./status.json',{cache:'no-cache'});if(!response.ok)throw Error('status_http_'+response.status);
const status=await response.json();
root.replaceChildren();
for(const task of status.tasks){
  const card=document.createElement('article');card.className='card';
  const imageBox=document.createElement('div');imageBox.className='visual';
  const image=document.createElement('img');image.loading='lazy';image.src='./'+task.id+'.webp';image.alt=task.title+' real browser screenshot';imageBox.append(image);
  const body=document.createElement('div');body.className='body';
  const tag=document.createElement('div');tag.className='tag '+(task.status==='LOCAL_PASS'?'ok':'fail');tag.textContent=task.status==='LOCAL_PASS'?'Local QA passed':'Quarantined · not approved';
  const h=document.createElement('h2');h.textContent=task.title;
  const desc=document.createElement('p');desc.className='desc';desc.textContent=task.theme;
  const qa=document.createElement('p');qa.className='qa';qa.textContent=task.unit+' unit · '+task.browser+' browser · '+task.style+' style';
  const ext=document.createElement('p');ext.className='external';ext.textContent=task.externally_verified?'External V2 review passed':task.external_status==='EXTERNAL_REVIEW_BLOCK'?'External V2 review blocked':'External V2 review unverified';
  const actions=document.createElement('div');actions.className='actions';
  if(task.playable){const play=document.createElement('a');play.href='./'+task.id+'/';play.textContent='Play this build';actions.append(play)}
  else{const blocked=document.createElement('span');blocked.className='blocked';blocked.textContent=task.status==='LOCAL_PASS'?'Playable only on private Dell — source retained locally':'Playable review blocked by QA';actions.append(blocked)}
  const detail=document.createElement('a');detail.className='secondary';detail.href='./evidence/'+task.id+'.json';detail.textContent='QA evidence';actions.append(detail);
  const commit=document.createElement('p');commit.className='commit';commit.textContent='Local Git: '+String(task.commit).slice(0,12);
  body.append(tag,h,desc,qa,ext,actions,commit);card.append(imageBox,body);root.append(card);
}
}catch(e){root.textContent='Cannot load sprint receipts. Previous playable game is still available. '+String(e)}
