"use strict";
(async () => {
 const host = document.querySelector('[data-candidate-manifest]');
 const status = document.getElementById('status');
 try {
  const response = await fetch(host.dataset.candidateManifest);
  if (!response.ok) throw new Error('Unable to load candidate index');
  const manifest = await response.json();
  const nav = document.getElementById('pages');
  const label = document.createElement('label'); label.textContent = 'Page '; nav.append(label);
  const select = document.createElement('select'); select.setAttribute('aria-label', 'Candidate page');
  manifest.parts.forEach((_, i) => {const o = document.createElement('option'); o.value=i; o.textContent=`${i+1} of ${manifest.parts.length}`; select.append(o)});
  label.append(select);
  const prev=document.createElement('button');prev.textContent='Previous';nav.prepend(prev);
  const next=document.createElement('button');next.textContent='Next';nav.append(next);
  let sequence=0;
  async function load(index) {
   const seq=++sequence;
   select.value=index;prev.disabled=index===0;next.disabled=index===manifest.parts.length-1;
   status.textContent='Loading candidates…';
   try {
    const r=await fetch(manifest.parts[index]);if(!r.ok)throw new Error('Unable to load candidates');
    const decompressed=r.body.pipeThrough(new DecompressionStream('gzip'));
    const text=await new Response(decompressed).text();
    if(seq!==sequence)return;
    host.innerHTML=text;
    status.textContent=`Candidates ${index*manifest.page_size+1}–${Math.min((index+1)*manifest.page_size,manifest.count)} of ${manifest.count.toLocaleString()}`;
    history.replaceState(null,'',`#page=${index+1}`);
   } catch(e) {status.textContent=`Could not load candidates: ${e.message}. Please retry.`;}
  }
  select.onchange=()=>load(Number(select.value));
  prev.onclick=()=>load(Number(select.value)-1);next.onclick=()=>load(Number(select.value)+1);
  const initial=Math.max(0,Math.min(manifest.parts.length-1,Number(new URLSearchParams(location.hash.slice(1)).get('page')||1)-1));
  await load(Number.isFinite(initial)?initial:0);
 } catch(e) {status.textContent=`Could not load candidates: ${e.message}. Please retry.`;}
})();
