(() => {
  'use strict';
  document.documentElement.classList.add('has-js');
  const root = document.documentElement;
  const $ = id => document.getElementById(id);
  const storage = {get(k){try{return localStorage.getItem(k)}catch{return null}},set(k,v){try{localStorage.setItem(k,v)}catch{}}};
  const prefix='heuristics-reader-';
  function theme(value){root.dataset.theme=value;$('theme').textContent=value==='dark'?'Light':'Dark';$('theme').setAttribute('aria-label',`Switch to ${value==='dark'?'light':'dark'} theme`)}
  theme(storage.get(prefix+'theme')==='dark'?'dark':'light');
  $('theme').addEventListener('click',()=>{const value=root.dataset.theme==='dark'?'light':'dark';theme(value);storage.set(prefix+'theme',value)});
  const sizes={normal:null,large:'23px',larger:'25px'};
  const stored=storage.get(prefix+'size');
  if(stored && Object.hasOwn(sizes,stored)) $('font-size').value=stored;
  function font(){const value=$('font-size').value;if(sizes[value])root.style.setProperty('--body-size',sizes[value]);else root.style.removeProperty('--body-size');storage.set(prefix+'size',value);progress()}
  $('font-size').addEventListener('change',font);
  function visuals(){document.body.classList.toggle('no-visuals',!$('visuals').checked);storage.set(prefix+'visuals',String($('visuals').checked));progress()}
  if(storage.get(prefix+'visuals')==='false')$('visuals').checked=false;
  $('visuals').addEventListener('change',visuals);
  const headings=[...document.querySelectorAll('article h2')];
  function progress(){const article=$('paper');const top=window.scrollY+article.getBoundingClientRect().top;const end=window.scrollY+$('paper-end').getBoundingClientRect().top-window.innerHeight;const pct=Math.max(0,Math.min(100,100*(window.scrollY-top)/Math.max(1,end-top)));$('progress').style.width=pct+'%';$('read-percent').textContent=Math.round(pct)+'%';let active='intro';for(const h of headings){if(h.getBoundingClientRect().top<180)active=h.id;else break}document.querySelectorAll('.toc a').forEach(a=>a.setAttribute('aria-current',String(a.getAttribute('href')==='#'+active)))}
  let pending=false;
  window.addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(()=>{progress();pending=false})}},{passive:true});
  window.addEventListener('resize',progress);
  function compound(){const n=Number($('draws').value);const all=0.9**n;const any=1-0.9**n;$('draws-value').textContent=String(n);$('all-value').textContent=(all*100).toFixed(2)+'%';$('any-value').textContent=(any*100).toFixed(2)+'%';$('all-formula').textContent=`0.9${superscript(n)}`;$('any-formula').textContent=`1 − 0.9${superscript(n)}`;$('all-bar').style.width=100*all+'%';$('any-bar').style.width=100*any+'%';$('all-label').textContent=`Red on all ${n} ${n===1?'draw':'draws'}`;$('any-label').textContent=`Red at least once in ${n} ${n===1?'draw':'draws'}`;$('compound-note').textContent=n===7?'At seven draws, the ranking is: all seven < one draw < at least one.':'The formulas show independent draws with replacement. The paper’s reported choices concern seven draws.'}
  function superscript(n){return String(n).split('').map(c=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[Number(c)]).join('')}
  $('draws').addEventListener('input',compound);
  $('reset-draws').addEventListener('click',()=>{$('draws').value=7;compound()});
  document.querySelectorAll('.mobile-toc a').forEach(a=>a.addEventListener('click',()=>a.closest('details').open=false));
  font();visuals();compound();progress();
})();
