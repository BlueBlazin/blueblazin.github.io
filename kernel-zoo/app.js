"use strict";
(() => {
 const $=id=>document.getElementById(id);
 const data=JSON.parse($("catalog-data").textContent);
 const entries=new Map(data.entries.map(e=>[e.id,e]));
 const topics=new Map(data.families.map(s=>[s.id,s]));
 const major=new Set(data.major);
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
 const color=id=>topics.get(entries.get(id).family).color;
 const state={view:"map",selected:null,mapScope:"common",indexScope:"all",query:"",sort:"common",lab:"filter"};
 let model={nodes:[],edges:[],groups:[],width:1240,height:1000};
 let transform={s:1,x:0,y:0},searchActive=-1,lastTrigger=null,pan=null,pinch=null;
 const pointers=new Map();
 const small=()=>innerWidth<=650;
 const svgNS="http://www.w3.org/2000/svg";
 const make=(name,attrs={},text="")=>{const e=document.createElementNS(svgNS,name);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(text)e.textContent=text;return e;};

 function matches(e){const terms=state.query.trim().toLowerCase().split(/\s+/).filter(Boolean);const hay=[e.name,e.alias,e.domain,e.short,e.body,e.note,e.example,e.type,topics.get(e.family).name,JSON.stringify(e.variants)].join(" ").toLowerCase();return terms.every(t=>hay.includes(t));}
 function sorted(list){return list.sort(state.sort==="alpha"?(a,b)=>a.name.localeCompare(b.name):(a,b)=>a.rank-b.rank||a.name.localeCompare(b.name));}
 function updateTabs(){document.querySelectorAll("[data-view]").forEach(b=>{const active=b.dataset.view===state.view;b.classList.toggle("active",active);b.setAttribute("aria-pressed",active);});}
 function setView(view,push=true){
   state.view=view;["map","index","experiments"].forEach(v=>$(v+"-view").hidden=v!==view);
   if(view==="experiments")closeReader(false);
   updateTabs();document.body.dataset.view=view;
   if(view==="index")renderIndex();
   if(view==="map")requestAnimationFrame(()=>buildMap());
   if(push)history.pushState(null,"","#"+view);
 }
 document.querySelectorAll("[data-view]").forEach(b=>b.addEventListener("click",()=>{closeReader(false);setView(b.dataset.view);}));

 function closeSearch(){ $("search-popup").hidden=true;$("search").setAttribute("aria-expanded","false");$("search").removeAttribute("aria-activedescendant");searchActive=-1; }
 function showSearch(){
   const result=sorted([...entries.values()].filter(matches));
   const list=state.query.trim()?result.slice(0,8):data.major.map(id=>entries.get(id));
   $("search-results").innerHTML=list.length?list.map((e,i)=>'<button type="button" class="search-result" role="option" id="search-option-'+i+'" data-entry="'+e.id+'" aria-selected="false"><i style="background:'+color(e.id)+'"></i><span>'+esc(e.alias)+'</span><small>'+esc(e.type)+'</small></button>').join(""):'<p class="search-empty">No matching kernels</p>';
   $("search-all").textContent=state.query.trim()?"See all "+result.length+" results":"Open the complete index";
   $("search-popup").hidden=false;$("search").setAttribute("aria-expanded","true");searchActive=-1;
 }
 $("search").addEventListener("focus",showSearch);
 $("search").addEventListener("input",e=>{state.query=e.target.value;showSearch();if(state.view==="index")renderIndex();});
 $("search").addEventListener("keydown",e=>{
   const options=[...$("search-results").querySelectorAll("[role=option]")];
   if(e.key==="ArrowDown"||e.key==="ArrowUp"){
     e.preventDefault();if($("search-popup").hidden)showSearch();
     searchActive=Math.max(0,Math.min(options.length-1,searchActive+(e.key==="ArrowDown"?1:-1)));
     options.forEach((o,i)=>o.setAttribute("aria-selected",i===searchActive));
     if(options[searchActive])$("search").setAttribute("aria-activedescendant",options[searchActive].id);
   }else if(e.key==="Enter"){
     e.preventDefault();const item=options[searchActive<0?0:searchActive];if(item){openEntry(item.dataset.entry,{forceMap:true});closeSearch();$("search").blur();}
   }else if(e.key==="Escape"){e.preventDefault();closeSearch();$("search").blur();}
 });
 $("search-results").addEventListener("click",e=>{const item=e.target.closest("[data-entry]");if(item){openEntry(item.dataset.entry,{forceMap:true});closeSearch();$("search").blur();}});
 $("search-all").addEventListener("click",()=>{closeSearch();closeReader(false);state.indexScope="all";setView("index");$("search").blur();});
 document.addEventListener("click",e=>{if(!e.target.closest(".search-box"))closeSearch();});
 document.addEventListener("keydown",e=>{
   const editing=/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)||document.activeElement.isContentEditable;
   if(e.key==="/"&&!editing&&!e.metaKey&&!e.ctrlKey){e.preventDefault();$("search").focus();}
   if(e.key==="Escape"&&!$("about-dialog").open&&!editing){closeSearch();closeReader();}
 });

 function renderIndex(){
   const list=sorted([...entries.values()].filter(e=>(state.indexScope==="all"||e.family===state.indexScope)&&matches(e)));
   $("index-title").textContent=state.indexScope==="all"?"All kernels":topics.get(state.indexScope).name;
   $("index-count").textContent=list.length+" "+(list.length===1?"entry":"entries")+(state.query.trim()?' matching “'+state.query.trim()+'”':"");
   $("index-scope").value=state.indexScope;
   document.querySelectorAll(".index-topic").forEach(b=>{b.classList.toggle("active",b.dataset.topic===state.indexScope);b.setAttribute("aria-pressed",b.dataset.topic===state.indexScope);});
   $("index-list").innerHTML=list.map(e=>'<li><button type="button" class="index-row'+(e.id===state.selected?' selected':'')+'" data-entry="'+e.id+'"><span class="index-name"><i style="background:'+color(e.id)+'"></i>'+esc(e.name)+'</span><span class="index-field">'+esc(topics.get(e.family).name)+'</span><span class="index-type">'+esc(e.type)+'</span></button></li>').join("");
   $("index-empty").hidden=list.length>0;
 }
 document.querySelectorAll(".index-topic").forEach(b=>b.addEventListener("click",()=>{state.indexScope=b.dataset.topic;renderIndex();$("index-view").scrollTop=0;}));
 $("index-scope").addEventListener("change",e=>{state.indexScope=e.target.value;renderIndex();});
 $("index-sort").addEventListener("change",e=>{state.sort=e.target.value;renderIndex();});
 $("index-list").addEventListener("click",e=>{const row=e.target.closest("[data-entry]");if(row)openEntry(row.dataset.entry);});
 $("index-reset").addEventListener("click",()=>{state.query="";$("search").value="";state.indexScope="all";renderIndex();});

 function neighbors(id){
   const explicit=data.links.filter(l=>l.a===id||l.b===id).map(l=>l.a===id?l.b:l.a);
   return [...new Set([...explicit,...entries.get(id).related])].filter(x=>x!==id).slice(0,10);
 }
 function linked(a,b){return data.links.find(l=>(l.a===a&&l.b===b)||(l.a===b&&l.b===a));}
 const labFor=id=>["cnn","filter","convolution"].includes(id)?"filter":["psd","rbf","rkhs","gp","kernel-families"].includes(id)?"gram":["cuda","opencl","hip","metal","triton","pallas","compute-cpu"].includes(id)?"cuda":id==="nullspace"?"null":null;
 function renderReader(){
   const e=entries.get(state.selected),section=topics.get(e.family),near=neighbors(e.id),lab=labFor(e.id);
   const variant=e.variants.length?(Array.isArray(e.variants[0])?'<table class="variant-table"><caption>SPICE file types</caption><thead><tr><th scope="col">Type</th><th scope="col">Contents</th></tr></thead><tbody>'+e.variants.map(([a,b])=>'<tr><th scope="row">'+esc(a)+'</th><td>'+esc(b)+'</td></tr>').join("")+'</tbody></table>':'<details class="variant-details"><summary>Variants in this entry</summary><ul>'+e.variants.map(v=>'<li>'+esc(v)+'</li>').join("")+'</ul></details>'):"";
   const refs=e.refs.map(r=>{const s=data.sources[r];return '<li><a href="'+esc(s.url)+'" target="_blank" rel="noopener">'+esc(s.title)+'</a><span>'+esc(s.publisher)+'</span></li>';}).join("");
   const related=near.map(id=>{const l=linked(e.id,id);return '<button type="button" class="related-entry" data-entry="'+id+'"><i style="background:'+color(id)+'"></i><span>'+esc(entries.get(id).alias)+(l?'<small>'+esc(l.label)+'</small>':'<small>Related entry</small>')+'</span></button>';}).join("");
   $("entry").style.setProperty("--entry",section.color);
   $("entry").innerHTML='<div class="entry-heading"><span class="entry-field">'+esc(section.name)+'</span><h1 tabindex="-1">'+esc(e.name)+'</h1><div class="entry-type">'+esc(e.type)+'</div></div><p class="entry-definition">'+esc(e.body)+'</p>'+(e.equation?'<div class="equation">'+e.equation+'</div>':"")+'<section class="entry-example"><h2>Example</h2><p>'+esc(e.example)+'</p>'+(e.code?'<pre><code>'+esc(e.code)+'</code></pre>':"")+(lab?'<button type="button" class="experiment-link" data-open-lab="'+lab+'">'+({filter:"Try image filtering",gram:"Try a similarity matrix",cuda:"Try a CUDA launch",null:"Move along the nullspace"}[lab])+'</button>':"")+'</section><p class="entry-note">'+esc(e.note)+'</p>'+variant+'<section class="entry-related"><h2>Connections</h2>'+related+'</section><section class="entry-sources"><h2>Sources</h2><ul>'+refs+'</ul></section><div class="entry-bottom"><a href="#'+e.id+'" class="permalink">Link to this kernel</a>'+(e.status!=="Meaning"?'<span>'+esc(e.status)+'</span>':'')+'</div>';
   $("reader-map").textContent=state.view==="map"?"View map":"Show connections";
   $("reader").scrollTop=0;
 }
 function openEntry(id,{push=true,forceMap=false,focus=true}={}){
   if(!entries.has(id))return;
   lastTrigger=document.activeElement;state.selected=id;
   if(forceMap||state.view!=="index"){
     state.mapScope="neighbors";setView("map",false);
   }
   $("reader").hidden=false;document.body.classList.add("has-reader");renderReader();
   if(state.view==="index")renderIndex();else requestAnimationFrame(()=>buildMap());
   if(push)history.pushState({view:state.view,indexScope:state.indexScope},"","#"+id);
   if(focus)$("entry").querySelector("h1").focus({preventScroll:true});
 }
 function closeReader(push=true){
   if($("reader").hidden)return;
   const previous=state.selected;
   $("reader").hidden=true;document.body.classList.remove("has-reader");
   const keep=push&&state.view==="map"&&state.mapScope==="neighbors";
   if(!keep){state.selected=null;if(state.mapScope==="neighbors")state.mapScope="common";}
   if(state.view==="map")requestAnimationFrame(()=>{buildMap();if(push){const target=$("network").querySelector('[data-entry="'+previous+'"]');(target||$("map-scope")).focus({preventScroll:true});}});
   if(state.view==="index"){renderIndex();if(push)$("index-list").querySelector('[data-entry="'+previous+'"]')?.focus({preventScroll:true});}
   if(push)history.pushState({view:state.view,selected:state.selected,mapScope:state.mapScope,reader:false},"","#"+state.view);
 }
 $("reader-close").addEventListener("click",()=>closeReader());
 $("reader-map").addEventListener("click",()=>{if(state.view==="map"){closeReader();return;}state.mapScope="neighbors";setView("map",false);buildMap();});
 $("entry").addEventListener("click",e=>{
   const target=e.target.closest("[data-entry]");if(target)openEntry(target.dataset.entry);
   const lab=e.target.closest("[data-open-lab]");if(lab)openLab(lab.dataset.openLab);
 });

 function nodeIcon(id){
   let body="";
   if(id==="linux")body='<rect x="15" y="12" width="70" height="20" rx="2"/><rect x="15" y="38" width="70" height="26" rx="2" fill="currentColor" fill-opacity=".13"/><rect x="15" y="70" width="70" height="18" rx="2"/><text x="50" y="26">apps</text><text x="50" y="55" font-size="14">kernel</text><text x="50" y="83" font-size="10">hardware</text>';
   else if(id==="cuda"){
     for(let r=0;r<3;r++)for(let c=0;c<4;c++)body+='<rect x="'+(15+c*19)+'" y="'+(17+r*21)+'" width="14" height="16" rx="1" fill="currentColor" fill-opacity="'+(.18+(r+c)%3*.22)+'"/>';
     body+='<text x="50" y="88" font-size="11">threads</text>';
   }else if(id==="cnn"){
     const w=[-1,0,1,-2,0,2,-1,0,1];for(let r=0;r<3;r++)for(let c=0;c<3;c++){const v=w[r*3+c];body+='<rect x="'+(15+c*25)+'" y="'+(12+r*25)+'" width="21" height="21" fill="currentColor" fill-opacity="'+(Math.abs(v)*.13+.04)+'"/><text x="'+(25.5+c*25)+'" y="'+(26+r*25)+'" font-size="11">'+v+'</text>';}
     body+='<text x="50" y="96" font-size="11">weights</text>';
   }else if(id==="psd"){
     for(let r=0;r<4;r++)for(let c=0;c<4;c++)body+='<rect x="'+(15+c*18)+'" y="'+(9+r*18)+'" width="15" height="15" fill="currentColor" fill-opacity="'+(.08+.75*Math.exp(-((r-c)**2)/2))+'" stroke="none"/>';
     body+='<text x="50" y="94" font-size="14">k(x, y)</text>';
   }else if(id==="nullspace")body='<path d="M8 50H92M50 10V88" opacity=".3"/><path d="M8 29L92 71" stroke-width="3"/><circle cx="70" cy="60" r="4" fill="currentColor"/><text x="48" y="92" font-size="14">Ax = 0</text>';
   else if(id==="lean")body='<text x="46" y="46" font-size="24" font-family="Georgia,serif">p : P</text><circle cx="66" cy="68" r="15" fill="currentColor" fill-opacity=".1"/><path d="M59 68L64 73L74 61" stroke-width="3"/>';
   return '<svg x="-43" y="-43" width="86" height="86" viewBox="0 0 100 100" class="node-icon" aria-hidden="true">'+body+'</svg>';
 }
 function commonModel(){
   if(small()){
     const points={linux:[105,95],cuda:[315,95],psd:[105,320],cnn:[315,320],nullspace:[105,550],lean:[315,550]};
     return {nodes:data.major.map(id=>({id,x:points[id][0],y:points[id][1],major:true})),groups:[],width:420,height:680};
   }
   return {nodes:Object.entries(data.overview).map(([id,[x,y]])=>({id,x:x*1.25,y:y*.8,major:major.has(id)})),groups:[],width:1560,height:870};
 }
 function neighborhoodModel(){
   const center=state.selected||"cnn",near=neighbors(center);
   if(small()){
     const nodes=[{id:center,x:210,y:130,major:true,center:true},...near.map((id,i)=>({id,x:i%2?315:105,y:360+Math.floor(i/2)*190,major:major.has(id)}))];
     return {nodes,groups:[],width:420,height:460+Math.ceil(near.length/2)*190};
   }
   const n=near.length,rx=n>6?390:345,ry=n>6?300:260;
   const nodes=[{id:center,x:550,y:415,major:true,center:true},...near.map((id,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;return {id,x:550+rx*Math.cos(a),y:415+ry*Math.sin(a),major:major.has(id)};})];
   return {nodes,groups:[],width:1100,height:850};
 }
 function categoryModel(topic){
   const list=sorted([...entries.values()].filter(e=>e.family===topic));
   const cols=small()?2:list.length>12?5:list.length>6?4:Math.min(3,list.length);
   const stepX=small()?210:215,stepY=small()?185:205;
   return {nodes:list.map((e,i)=>({id:e.id,x:100+(i%cols)*stepX,y:115+Math.floor(i/cols)*stepY,major:major.has(e.id)})),groups:[],width:cols*stepX,height:175+Math.ceil(list.length/cols)*stepY};
 }
 function allModel(){
   const groups=[],nodes=[];const cols=small()?1:3,w=500,h=310;
   data.families.forEach((s,i)=>{
     const X=i%cols*w,Y=Math.floor(i/cols)*h;
     groups.push({id:s.id,x:X+35,y:Y+38,width:430,name:s.name,count:s.count});
     const list=sorted([...entries.values()].filter(e=>e.family===s.id));
     list.forEach((e,j)=>nodes.push({id:e.id,x:X+65+(j%5)*85,y:Y+115+Math.floor(j/5)*62,major:false,compact:true}));
   });
   return {nodes,groups,width:cols*w,height:Math.ceil(data.families.length/cols)*h};
 }
 function buildMap(){
   if(state.view!=="map")return;
   if(state.mapScope==="neighbors"&&!state.selected)state.mapScope="common";
   const select=$("map-scope");const existing=select.querySelector('[value="neighbors"]');
   if(state.mapScope==="neighbors"){
     if(!existing)select.add(new Option("Connections: "+entries.get(state.selected).alias,"neighbors"),0);else existing.textContent="Connections: "+entries.get(state.selected).alias;
   }else existing?.remove();
   select.value=state.mapScope;
   $("back-overview").hidden=state.mapScope==="common";
   $("map-description").textContent=state.mapScope==="common"?"Select a kernel to see its definition and connections.":state.mapScope==="all"?"Select a field to expand it.":state.mapScope==="neighbors"?"Select a connected kernel to continue.":topics.get(state.mapScope).count+" kernels";
   model=state.mapScope==="common"?commonModel():state.mapScope==="neighbors"?neighborhoodModel():state.mapScope==="all"?allModel():categoryModel(state.mapScope);
   const ids=new Set(model.nodes.map(n=>n.id));
   model.edges=data.links.filter(l=>ids.has(l.a)&&ids.has(l.b)&&(state.mapScope!=="neighbors"||l.a===state.selected||l.b===state.selected));
   if(state.mapScope==="neighbors"){
     model.nodes.filter(n=>!n.center).forEach(n=>{if(!linked(state.selected,n.id))model.edges.push({a:state.selected,b:n.id,label:"Related entry",kind:"suggestion"});});
   }
   drawMap();fitGraph();
   $("graph-status").textContent=model.nodes.length+" kernels shown.";
   $("map-hint").innerHTML=small()?"Drag to pan <span>·</span> Pinch to zoom":"Drag to pan <span>·</span> Scroll to zoom";
 }
 function drawMap(){
   const graph=$("graph");graph.replaceChildren();
   const paths=make("g",{class:"graph-edges"}),groups=make("g",{class:"graph-groups"}),nodes=make("g",{class:"graph-nodes"}),labels=make("g",{class:"graph-edge-labels","aria-hidden":"true"});
   graph.append(paths,groups,nodes,labels);
   model.groups.forEach(g=>{
     const box=make("g",{class:"graph-group",transform:'translate('+g.x+' '+g.y+')',role:"button",tabindex:"0","aria-label":g.name+", "+g.count+" kernels","data-topic":g.id});
     box.append(make("rect",{class:"group-hit",x:-8,y:-29,width:g.width,height:48,fill:"transparent"}),make("line",{class:"group-rule",x1:0,y1:31,x2:g.width,y2:31,stroke:topics.get(g.id).color,"stroke-opacity":".25"}),make("text",{class:"group-title",fill:topics.get(g.id).color},g.name));groups.append(box);
   });
   const bynode=new Map(model.nodes.map(n=>[n.id,n]));
   model.edges.forEach((e,i)=>{
     const a=bynode.get(e.a),b=bynode.get(e.b),rA=a.center?73:a.major?55:a.compact?6:9,rB=b.center?73:b.major?55:b.compact?6:9;
     const dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy)||1;
     const start={x:a.x+dx/len*(rA+4),y:a.y+dy/len*(rA+4)},end={x:b.x-dx/len*(rB+4),y:b.y-dy/len*(rB+4)};
     const bend=(state.mapScope==="neighbors"?16:32)*(i%2?1:-1),mid={x:(start.x+end.x)/2-dy/len*bend,y:(start.y+end.y)/2+dx/len*bend};
     let d='M'+start.x+','+start.y+' Q'+mid.x+','+mid.y+' '+end.x+','+end.y;
     let labelX=(start.x+end.x+2*mid.x)/4,labelY=(start.y+end.y+2*mid.y)/4;
     // Downward vertical edges take a side port so they do not run through labels.
     if(Math.abs(dx)<len*.35){
       const direction=dy>0?1:-1;
       const A={x:a.x+rA+5,y:a.y+direction*rA*.25},B={x:b.x+rB+5,y:b.y-direction*rB*.25};
       const side=small()?80:200;
       const C={x:A.x+side,y:A.y+dy*.28},D={x:B.x+side,y:B.y-dy*.28};
       d='M'+A.x+','+A.y+' C'+C.x+','+C.y+' '+D.x+','+D.y+' '+B.x+','+B.y;
       labelX=(A.x+3*C.x+3*D.x+B.x)/8;labelY=(A.y+3*C.y+3*D.y+B.y)/8;
     }
     const path=make("path",{id:"edge-"+i,d,class:'edge '+(e.kind==="contrast"?'edge-dashed':e.kind==="suggestion"?'edge-suggestion':''),"data-a":e.a,"data-b":e.b});path.append(make("title",{},entries.get(e.a).alias+" · "+e.label+" · "+entries.get(e.b).alias));paths.append(path);
     const intro=state.mapScope==='common'&&!small()&&((e.a==='linux'&&e.b==='cuda')||(e.a==='cuda'&&e.b==='cnn'));
     const label=make("g",{class:"edge-label"+(intro?' intro-edge':''),"data-path":"edge-"+i,transform:'translate('+labelX+' '+labelY+')',"data-a":e.a,"data-b":e.b});
     label.append(make("text",{"text-anchor":"middle",dy:"-.3em",class:"edge-text"},e.label));labels.append(label);
   });
   model.nodes.forEach(n=>{
     const e=entries.get(n.id),c=color(n.id),radius=n.center?73:n.major?55:n.compact?7:9;
     const node=make("g",{class:'graph-node'+(n.major?' major':'')+(n.center?' center':'')+(n.compact?' compact':''),transform:'translate('+n.x+' '+n.y+')',role:"button",tabindex:"0","aria-label":e.alias+". "+e.type,"data-entry":n.id,style:'--node:'+c});
     node.append(make("title",{},e.name+" — "+e.type),make("rect",{class:"node-hit",x:n.compact?-13:-100,y:n.compact?-13:-radius-12,width:n.compact?26:200,height:n.compact?26:radius*2+85,fill:"transparent"}),make("circle",{class:"node-halo",r:radius+8}),make("circle",{class:"node-circle",r:radius}));
     if(n.major){
       const icon=major.has(n.id)?nodeIcon(n.id):e.icon.replace('<svg ','<svg x="-54" y="-31" width="108" height="62" ');
       const holder=make("g",{class:"node-figure"});holder.innerHTML=icon;node.append(holder);
     }
     const text=make("text",{class:"node-label","text-anchor":"middle",y:radius+28});
     const words=e.alias.split(" "),lines=[];let line="";
     for(const word of words){if(line&&(line+" "+word).length>(n.major?22:20)){lines.push(line);line=word;}else line+=(line?" ":"")+word;}if(line)lines.push(line);
     lines.forEach((line,i)=>text.append(make("tspan",{x:0,dy:i?"1.18em":0},line)));node.append(text);
     if(n.major||state.mapScope==="neighbors")node.append(make("text",{class:"node-type","text-anchor":"middle",y:radius+54+(lines.length-1)*22},e.type));
     nodes.append(node);
   });
   graph.classList.toggle("focused",state.mapScope==="neighbors");
   requestAnimationFrame(()=>refreshEdgeLabels());
 }
 function refreshEdgeLabels(){
   const blocks=[];
   if(state.mapScope==='neighbors')model.nodes.forEach(n=>{
     const g=$("network").querySelector('[data-entry="'+n.id+'"]');
     [g.querySelector('.node-circle'),g.querySelector('.node-label'),g.querySelector('.node-type')].filter(Boolean).forEach(el=>{const b=el.getBBox();blocks.push({x:b.x+n.x,y:b.y+n.y,w:b.width,h:b.height});});
   });
   const collides=b=>blocks.some(a=>Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>-5&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>-5);
   document.querySelectorAll(".edge-label").forEach(g=>{
     const t=g.querySelector("text"),box=t.getBBox();let r=g.querySelector("rect");if(!r){r=make("rect",{rx:3});g.prepend(r);}r.setAttribute("x",box.x-7);r.setAttribute("y",box.y-3);r.setAttribute("width",box.width+14);r.setAttribute("height",box.height+6);
     if(state.mapScope!=='neighbors')return;
     const path=$(g.dataset.path),length=path.getTotalLength();let choice=null;
     for(const offset of [0,24,-24,45,-45,70,-70]){
       for(const fraction of [.5,.36,.64,.25,.75]){
         const p=path.getPointAtLength(length*fraction),q=path.getPointAtLength(Math.min(length,length*fraction+1)),dx=q.x-p.x,dy=q.y-p.y,n=Math.hypot(dx,dy)||1;
         const x=p.x-dy/n*offset,y=p.y+dx/n*offset,b={x:x+box.x-7,y:y+box.y-3,w:box.width+14,h:box.height+6};
         if(!collides(b)){choice={x,y,b,p,offset};break;}
       }if(choice)break;
     }
     if(choice){
       g.setAttribute('transform','translate('+choice.x+' '+choice.y+')');blocks.push(choice.b);
       let leader=g.querySelector('line');
       if(Math.abs(choice.offset)>24){if(!leader){leader=make('line',{stroke:'#bdcbd1','stroke-width':1,'vector-effect':'non-scaling-stroke'});g.prepend(leader);}leader.setAttribute('x1',choice.p.x-choice.x);leader.setAttribute('y1',choice.p.y-choice.y);leader.setAttribute('x2',0);leader.setAttribute('y2',0);}else leader?.remove();
     }
   });
 }
 function applyTransform(){
   $("graph").setAttribute("transform",'translate('+transform.x+' '+transform.y+') scale('+transform.s+')');
   const scale=transform.s;
   document.querySelectorAll(".node-label").forEach(e=>e.style.fontSize=Math.max(e.closest(".major")?21:16,(e.closest(".major")?20:14)/scale)+"px");
   document.querySelectorAll(".node-type").forEach(e=>e.style.fontSize=Math.max(13,14/scale)+"px");
   document.querySelectorAll(".graph-group").forEach(g=>{
     const e=g.querySelector(".group-title"),topic=model.groups.find(t=>t.id===g.dataset.topic);
     e.style.fontSize=Math.max(22,15/scale)+"px";e.replaceChildren();
     let line=make("tspan",{x:0,dy:0});e.append(line);
     for(const word of topic.name.split(" ")){
       const previous=line.textContent;line.textContent=previous+(previous?" ":"")+word;
       if(previous&&line.getComputedTextLength()>topic.width-12){line.textContent=previous;line=make("tspan",{x:0,dy:"1.15em"},word);e.append(line);}
     }
     const b=e.getBBox(),ruleY=b.y+b.height+12;
     g.querySelector(".group-rule").setAttribute("y1",ruleY);g.querySelector(".group-rule").setAttribute("y2",ruleY);
     g.querySelector(".group-hit").setAttribute("y",b.y-8);g.querySelector(".group-hit").setAttribute("height",b.height+20);
   });
   document.querySelectorAll(".edge-text").forEach(e=>e.style.fontSize=Math.max(14,12/scale)+"px");
   $("graph").classList.toggle("hide-compact-labels",state.mapScope==="all"&&scale<.8);
   refreshEdgeLabels();
 }
 function fitGraph(){
   const box=$("map-frame").getBoundingClientRect();if(box.width===0||box.height===0)return;
   let scale=Math.min((box.width-70)/model.width,(box.height-90)/model.height);
   scale=Math.min(1.2,Math.max(.18,scale));
   if(small()&&state.mapScope!=="all")scale=Math.max(.64,scale);
   if(small()&&state.mapScope==="all")scale=Math.min(.64,(box.width-50)/model.width);
   transform={s:scale,x:(box.width-model.width*scale)/2,y:(box.height-model.height*scale)/2};
   if(small()&&model.height*scale>box.height-70)transform.y=40;
   applyTransform();
 }
 function zoom(factor,x,y){
   const box=$("map-frame").getBoundingClientRect();x=x??box.width/2;y=y??box.height/2;
   const s=Math.max(.18,Math.min(3.5,transform.s*factor)),ratio=s/transform.s;
   transform={s,x:x-(x-transform.x)*ratio,y:y-(y-transform.y)*ratio};applyTransform();
 }
 $("zoom-in").addEventListener("click",()=>zoom(1.25));$("zoom-out").addEventListener("click",()=>zoom(.8));$("fit-map").addEventListener("click",fitGraph);
 $("map-scope").addEventListener("change",e=>{state.mapScope=e.target.value;if(state.mapScope!=="neighbors")closeReader(false);buildMap();});
 $("back-overview").addEventListener("click",()=>{closeReader(false);state.mapScope="common";state.query="";$("search").value="";buildMap();history.pushState(null,"","#map");});
 $("network").addEventListener("click",e=>{
   if(pan?.moved)return;
   const node=e.target.closest("[data-entry]");if(node){openEntry(node.dataset.entry);return;}
   const group=e.target.closest("[data-topic]");if(group){state.mapScope=group.dataset.topic;closeReader(false);buildMap();}
 });
 $("network").addEventListener("keydown",e=>{
   if(e.key==="Enter"||e.key===" "){const target=e.target.closest("[data-entry],[data-topic]");if(target){e.preventDefault();target.dispatchEvent(new MouseEvent("click",{bubbles:true}));}}
   if(e.key==="+"){e.preventDefault();zoom(1.25);}if(e.key==="-"){e.preventDefault();zoom(.8);}if(e.key==="0"){e.preventDefault();fitGraph();}
 });
 $("network").addEventListener("wheel",e=>{e.preventDefault();const b=$("map-frame").getBoundingClientRect();zoom(Math.exp(-e.deltaY*.0015),e.clientX-b.x,e.clientY-b.y);},{passive:false});
 $("network").addEventListener("pointerdown",e=>{
   pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
   if(pointers.size===2){const p=[...pointers.values()];pinch={distance:Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y)};pan=null;}
   else {pan={id:e.pointerId,x:e.clientX,y:e.clientY,tx:transform.x,ty:transform.y,moved:false};}
 });
 $("network").addEventListener("pointermove",e=>{
   if(pointers.has(e.pointerId))pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});
   if(pinch&&pointers.size===2){const p=[...pointers.values()],dist=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y),b=$("map-frame").getBoundingClientRect();zoom(dist/pinch.distance,(p[0].x+p[1].x)/2-b.x,(p[0].y+p[1].y)/2-b.y);pinch.distance=dist;return;}
   if(pan?.id===e.pointerId&&e.buttons!==0){const dx=e.clientX-pan.x,dy=e.clientY-pan.y;if(Math.hypot(dx,dy)>5){pan.moved=true;$("network").setPointerCapture(e.pointerId);transform.x=pan.tx+dx;transform.y=pan.ty+dy;applyTransform();}}
 });
 const release=e=>{pointers.delete(e.pointerId);if(pointers.size<2)pinch=null;if(pan?.id===e.pointerId){const moved=pan.moved;setTimeout(()=>{if(pan?.id===e.pointerId)pan=null;},moved?80:0);}};
 $("network").addEventListener("pointerup",release);$("network").addEventListener("pointercancel",release);
 $("network").addEventListener("pointerover",e=>{const n=e.target.closest("[data-entry]");if(n)highlight(n.dataset.entry);});
 $("network").addEventListener("pointerout",e=>{if(!e.relatedTarget?.closest?.("[data-entry]"))highlight(null);});
 function highlight(id){
   document.querySelectorAll(".edge,.edge-label").forEach(e=>e.classList.toggle("hovered",id&&(e.dataset.a===id||e.dataset.b===id)));
 }
 let lastSmall=small();let resizeTimer;new ResizeObserver(()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(state.view==="map"){if(lastSmall!==small()){lastSmall=small();buildMap();}else fitGraph();}},60);}).observe($("map-frame"));

 function openLab(lab,push=true){state.lab=lab;setView("experiments",false);document.querySelectorAll("[data-lab]").forEach(b=>{const active=b.dataset.lab===lab;b.classList.toggle("active",active);b.setAttribute("aria-pressed",active);});document.querySelectorAll(".lab").forEach(e=>e.hidden=e.id!==lab+"-lab");if(push)history.pushState(null,"","#experiment-"+lab);$("experiments-view").scrollTop=0;}
 document.querySelectorAll("[data-lab]").forEach(b=>b.addEventListener("click",()=>openLab(b.dataset.lab)));
 document.addEventListener("click",e=>{const a=e.target.closest("a[href^='#']");if(!a)return;const id=decodeURIComponent(a.hash.slice(1));if(entries.has(id)){e.preventDefault();openEntry(id,{forceMap:state.view==="experiments"});}else if(id==="map"){e.preventDefault();closeReader(false);state.mapScope="common";setView("map");}});
 function showAbout(){closeSearch();$("about-dialog").showModal();}
 $("about-open").addEventListener("click",showAbout);$("footer-about").addEventListener("click",showAbout);$("about-close").addEventListener("click",()=>$("about-dialog").close());
 $("about-dialog").addEventListener("click",e=>{if(e.target===$("about-dialog")){const b=$("about-dialog").getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)$("about-dialog").close();}});
 function route(){const id=decodeURIComponent(location.hash.slice(1));if(entries.has(id)){if(history.state?.view==="index"){state.indexScope=history.state.indexScope||"all";setView("index",false);}openEntry(id,{push:false,forceMap:history.state?.view!=="index",focus:false});}else if(id.startsWith("experiment-")&&["filter","gram","cuda","null"].includes(id.slice(11)))openLab(id.slice(11),false);else if(id==="sources"||id==="scope")showAbout();else{const saved=history.state;closeReader(false);if(id==="map"&&saved?.selected){state.selected=saved.selected;state.mapScope=saved.mapScope||"neighbors";}setView(id==="index"||id==="catalog"?"index":id==="experiments"||id==="labs"?"experiments":"map",false);}}
 addEventListener("hashchange",route);route();renderIndex();
})();
