"use strict";
(() => {
  const $ = id => document.getElementById(id);
  const specimens = [...document.querySelectorAll(".specimen")];
  const filters = [...document.querySelectorAll(".family-filter,.family-card")];
  let family = "all";
  let query = "";
  const names = Object.fromEntries([...document.querySelectorAll(".family-card")].map(x => [x.dataset.family, x.querySelector(".family-card-name").textContent]));
  const format = (x, precision = 3) => Math.abs(x) < 1e-9 ? "0" : Number(x.toFixed(precision)).toString();
  const escapeHTML = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);

  function applyFilters() {
    let count = 0;
    const terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    specimens.forEach(el => {
      const visible = (family === "all" || family === el.dataset.family) && terms.every(q => el.dataset.search.includes(q));
      el.hidden = !visible;
      if (visible) count++;
    });
    filters.forEach(el => {
      const active = el.dataset.family === family;
      el.classList.toggle("active", active);
      el.classList.toggle("selected", active && el.classList.contains("family-card"));
      if (el.classList.contains("family-filter")) el.setAttribute("aria-pressed", String(active));
    });
    $("catalog-title").textContent = family === "all" ? "All kernels" : names[family];
    $("results").textContent = count + (count === 1 ? " entry" : " entries") + (query.trim() ? ' matching “' + query.trim() + '”' : " · open an entry for examples and sources");
    $("empty").hidden = count !== 0;
    $("reset").hidden = family === "all" && query === "";
  }
  function clearFilters() {
    family = "all"; query = ""; $("search").value = ""; applyFilters();
  }
  filters.forEach(el => el.addEventListener("click", () => {
    family = el.dataset.family;
    applyFilters();
    $("catalog").scrollIntoView({behavior:"smooth",block:"start"});
  }));
  $("search").addEventListener("input", e => {query = e.target.value; applyFilters();});
  $("reset").addEventListener("click", clearFilters);
  $("empty-reset").addEventListener("click", clearFilters);
  document.addEventListener("keydown", e => {
    const editing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) || document.activeElement.isContentEditable;
    if (e.key === "/" && !editing && !e.metaKey && !e.ctrlKey && !e.altKey) {e.preventDefault(); $("search").focus();}
    if (e.key === "Escape" && document.activeElement === $("search")) {query="";$("search").value="";applyFilters();}
  });
  function revealEntry(id, scroll = true) {
    const target = $(id);
    if (!target || !target.classList.contains("specimen")) return false;
    if (target.hidden) clearFilters();
    target.open = true;
    if (scroll) requestAnimationFrame(() => target.scrollIntoView({behavior:"smooth",block:"start"}));
    return true;
  }
  document.addEventListener("click", e => {
    const link = e.target.closest("a[href^='#']");
    if (!link) return;
    const id = decodeURIComponent(link.getAttribute("href").slice(1));
    if (revealEntry(id)) {
      e.preventDefault();
      history.pushState(null, "", "#" + id);
      const summary = $(id).querySelector("summary");
      summary.focus({preventScroll:true});
    }
  });
  addEventListener("hashchange", () => revealEntry(decodeURIComponent(location.hash.slice(1))));
  specimens.forEach(el => el.addEventListener("toggle", () => {
    if (el.open && !el.hidden) history.replaceState(null, "", "#" + el.id);
  }));
  if (location.hash) revealEntry(decodeURIComponent(location.hash.slice(1)));
  applyFilters();

  const image = Array.from({length:8}, (_,r) => Array.from({length:8}, (_,c) => (r < 4 ? 1 : 5) + (c >= 3 && c <= 5 ? 5 : 0) + ((r+c)%3)));
  const kernels = {
    blur: Array.from({length:3}, () => [1/9,1/9,1/9]),
    sharpen:[[0,-1,0],[-1,5,-1],[0,-1,0]],
    edge:[[-1,0,1],[-2,0,2],[-1,0,1]],
    asymmetric:[[0,0,0],[0,0,1],[0,0,0]]
  };
  let selected = [3,3];
  function filterGrid(input, weights) {
    return input.map((row,r) => row.map((_,c) => weights.reduce((sum,w,i) =>
      sum + w.reduce((s,v,j) => s + v*(input[r+i-1]?.[c+j-1] ?? 0),0),0)));
  }
  function signedColor(x, scale = 20) {
    const t = Math.min(1,Math.abs(x)/scale);
    const base = x >= 0 ? [8,123,112] : [176,48,76];
    return "rgb(" + base.map(v => Math.round(247*(1-t)+v*t)).join(",") + ")";
  }
  function updateFilter() {
    const chosen = $("filter-choice").value;
    const mode = document.querySelector('input[name="filter-mode"]:checked').value;
    const raw = kernels[chosen];
    const w = mode === "convolution" ? raw.slice().reverse().map(row => row.slice().reverse()) : raw;
    const output = filterGrid(image,w);
    $("input-grid").innerHTML = image.flatMap((row,r) => row.map((v,c) => {
      const shade = Math.round(249-v/12*207);
      const isSelected = r===selected[0] && c===selected[1];
      const neighbor = Math.abs(r-selected[0]) <= 1 && Math.abs(c-selected[1]) <= 1;
      return '<button type="button" class="pixel'+(isSelected?' selected':'')+(neighbor?' neighbor':'')+'" data-row="'+r+'" data-col="'+c+'" style="background:rgb('+shade+','+shade+','+shade+');color:'+(shade<130?'white':'#191f2c')+'" aria-label="Input row '+r+', column '+c+', value '+v+'" aria-pressed="'+isSelected+'">'+v+'</button>';
    })).join("");
    $("output-grid").innerHTML = output.flatMap((row,r) => row.map((v,c) => '<span class="pixel output-pixel'+(r===selected[0] && c===selected[1]?' selected':'')+'" style="background:'+signedColor(v)+';color:'+(Math.abs(v)>11?'white':'#191f2c')+'" title="Output ['+r+','+c+'] = '+format(v)+'">'+format(v,1)+'</span>')).join("");
    const weightFormat = v => Math.abs(v-1/9)<1e-10 ? "1/9" : format(v);
    $("weight-grid").innerHTML = w.flat().map(v => '<span class="weight">'+weightFormat(v)+'</span>').join("");
    const terms = w.flatMap((row,i) => row.map((v,j) => "("+(image[selected[0]+i-1]?.[selected[1]+j-1]??0)+" × "+weightFormat(v)+")")).join(" + ");
    $("filter-calculation").innerHTML = '<span class="calculation-label">Selected output ['+selected.join(",")+'] · '+mode+'</span>'+terms+'<br><strong>= '+format(output[selected[0]][selected[1]],5)+'</strong>';
    $("input-grid").dataset.selectedOutput = output[selected[0]][selected[1]];
    $("output-grid").dataset.values = JSON.stringify(output);
  }
  $("input-grid").addEventListener("click", e => {
    const cell=e.target.closest("button[data-row]");
    if(cell){selected=[Number(cell.dataset.row),Number(cell.dataset.col)];updateFilter();}
  });
  $("filter-choice").addEventListener("change",updateFilter);
  document.querySelectorAll('input[name="filter-mode"]').forEach(x => x.addEventListener("change",updateFilter));
  updateFilter();

  // Jacobi rotations for a small real symmetric matrix.
  function eigenvalues(matrix) {
    const a=matrix.map(row=>row.slice()),n=a.length;
    for(let step=0;step<150;step++){
      let p=0,q=1,max=0;
      for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(Math.abs(a[i][j])>max){max=Math.abs(a[i][j]);p=i;q=j;}
      if(max<1e-12)break;
      const angle=.5*Math.atan2(2*a[p][q],a[q][q]-a[p][p]);
      const c=Math.cos(angle),s=Math.sin(angle),app=a[p][p],aqq=a[q][q],apq=a[p][q];
      for(let k=0;k<n;k++)if(k!==p && k!==q){
        const x=a[k][p],y=a[k][q];
        a[k][p]=a[p][k]=c*x-s*y;
        a[k][q]=a[q][k]=s*x+c*y;
      }
      a[p][p]=c*c*app-2*s*c*apq+s*s*aqq;
      a[q][q]=s*s*app+2*s*c*apq+c*c*aqq;
      a[p][q]=a[q][p]=0;
    }
    return a.map((row,i)=>row[i]).sort((x,y)=>x-y);
  }
  function updateGram() {
    const mode=$("gram-choice").value,length=Number($("length-scale").value);
    $("length-value").textContent=length.toFixed(1);
    $("length-scale").disabled=mode!=="rbf";
    const points=mode==="invalid"?[0,1]:[0,1,2,4];
    const matrix=points.map(x=>points.map(y=>mode==="rbf"?Math.exp(-((x-y)**2)/(2*length*length)):mode==="poly"?(1+x*y)**2:x===y?1:2));
    $("sample-line").textContent=mode==="invalid"?"Two hypothetical inputs":"Input points: "+points.join(" · ");
    const max=Math.max(...matrix.flat());
    $("gram-table").innerHTML='<table aria-label="Pairwise Gram matrix"><thead><tr><th scope="col">x / y</th>'+points.map(x=>'<th scope="col">'+x+'</th>').join('')+'</tr></thead><tbody>'+matrix.map((row,i)=>'<tr><th scope="row">'+points[i]+'</th>'+row.map(v=>'<td style="background:'+signedColor(v,max)+';color:'+(v/max>.55?'white':'#191f2c')+'">'+format(v)+'</td>').join("")+'</tr>').join("")+'</tbody></table>';
    const eigen=eigenvalues(matrix);
    const valid=eigen[0]>=-1e-8;
    $("gram-verdict").innerHTML='<div class="gram-verdict" style="color:'+(valid?'#087b70':'#b43f53')+'">'+(valid?"Positive semidefinite":"Not positive semidefinite")+'</div><div class="gram-eigen">Eigenvalues:<br>'+eigen.map(x=>format(x,5)).join(" · ")+'</div>';
    $("gram-explanation").textContent=mode==="invalid"?"Every matrix entry is positive, yet a=(1,−1) gives aᵀKa=−2. Positive entries do not imply a valid PSD kernel.":mode==="rbf"?"Increasing the length scale makes distant points more similar. Every finite RBF Gram matrix is PSD; this numerical example illustrates the property.":"The scalar feature map φ(x)=(x², √2x, 1) realizes (1+xy)² as an inner product. Four inputs in this three-dimensional feature space give at least one zero eigenvalue.";
    $("gram-table").dataset.matrix=JSON.stringify(matrix);
    $("gram-table").dataset.eigenvalues=JSON.stringify(eigen);
  }
  $("gram-choice").addEventListener("change",updateGram);
  $("length-scale").addEventListener("input",updateGram);
  updateGram();

  function updateLaunch(){
    const n=Number($("vector-length").value),b=Number($("block-size").value),blocks=Math.ceil(n/b),launched=blocks*b;
    $("n-value").textContent=n;
    $("launch-stats").innerHTML=[["Blocks",blocks],["Threads launched",launched],["In-range threads",n],["Extra threads",launched-n]].map(([label,value])=>'<div><strong>'+value+'</strong><span>'+label+'</span></div>').join("");
    $("blocks").innerHTML=Array.from({length:blocks},(_,block)=>'<div class="thread-block"><h4>Block '+block+' · global IDs '+block*b+'–'+(block*b+b-1)+'</h4><div class="threads">'+Array.from({length:b},(_,thread)=>{const id=block*b+thread;return '<span class="thread'+(id>=n?' inactive':'')+'" title="blockIdx='+block+', threadIdx='+thread+', i='+id+(id>=n?': skip':': c[i]=a[i]+b[i]')+'">'+id+'</span>';}).join("")+'</div></div>').join("");
    $("launch-code").textContent="add<<<"+blocks+", "+b+">>>(a, b, c, "+n+");   i = blockIdx.x × "+b+" + threadIdx.x;   if (i < "+n+") c[i] = a[i] + b[i];";
    $("blocks").dataset.launched=launched;
    $("blocks").dataset.extra=launched-n;
  }
  $("vector-length").addEventListener("input",updateLaunch);
  $("block-size").addEventListener("change",updateLaunch);
  updateLaunch();

  function updateNull(){
    const t=Number($("null-t").value),x=-2*t,y=t;
    $("t-value").textContent=t.toFixed(1);
    const X=v=>210+v*19,Y=v=>105-v*19;
    let s='<svg viewBox="0 0 420 220" role="img" aria-label="The nullspace line y = −x/2 with selected vector ('+format(x)+','+format(y)+')"><title>Every point on this line satisfies x + 2y = 0.</title>';
    for(let i=-10;i<=10;i++)s+='<line x1="'+X(i)+'" y1="10" x2="'+X(i)+'" y2="200" stroke="#edf0f5"/>';
    for(let i=-5;i<=5;i++)s+='<line x1="20" y1="'+Y(i)+'" x2="400" y2="'+Y(i)+'" stroke="#edf0f5"/>';
    s+='<line x1="20" y1="105" x2="400" y2="105" stroke="#a7b3c6"/><line x1="210" y1="10" x2="210" y2="200" stroke="#a7b3c6"/><line x1="'+X(-10)+'" y1="'+Y(5)+'" x2="'+X(10)+'" y2="'+Y(-5)+'" stroke="#315ad5" stroke-width="2.5"/><line x1="210" y1="105" x2="'+X(x)+'" y2="'+Y(y)+'" stroke="#d9640b" stroke-width="4"/><circle cx="'+X(x)+'" cy="'+Y(y)+'" r="6" fill="#d9640b" stroke="white" stroke-width="2"/><text x="390" y="97" font-size="13" fill="#566071">x</text><text x="220" y="20" font-size="13" fill="#566071">y</text><text x="223" y="122" font-size="12" fill="#566071">0</text><text x="20" y="216" font-size="12" fill="#566071">x: −10 to 10 · y: −5 to 5</text></svg>';
    $("null-plot").innerHTML=s;
    $("null-calculation").innerHTML='<span class="calculation-label">A = [1 2] · v = (−2t, t)</span>v = ('+format(x)+', '+format(y)+')<br>Av = '+format(x)+' + 2 × ('+format(y)+')<br><strong>= '+format(x+2*y)+'</strong>';
    $("null-plot").dataset.vector=JSON.stringify([x,y]);
  }
  $("null-t").addEventListener("input",updateNull);
  updateNull();
})();
