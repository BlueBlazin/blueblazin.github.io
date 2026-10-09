from pathlib import Path
import html, json, math, subprocess
from catalog import FAMILIES, SOURCES, ENTRIES

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
esc=html.escape
families={f[0]:dict(id=f[0],name=f[1],description=f[2],color=f[3],visual=f[4],tags=f[5]) for f in FAMILIES}
order={f[0]:i for i,f in enumerate(FAMILIES)}
entries=sorted(ENTRIES,key=lambda e:order[e["family"]])
byid={e["id"]:e for e in entries}
used=set(r for e in entries for r in e["refs"])
assert len(byid)==len(entries)
assert all(r in SOURCES for r in used)
assert all(r in byid for e in entries for r in e["related"])

# Use the existing repository's KaTeX runtime to render static MathML + HTML.
formulas=list(dict.fromkeys(e["tex"] for e in entries if e["tex"]))
proc=subprocess.run(["node","-e",r"""
const fs=require('fs'),k=require(process.argv[1]);
const a=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x,{displayMode:true,throwOnError:true,output:'htmlAndMathml'}))));
""",str(OUT.parent/"courses/_source/vendor/katex/katex.min.js")],
input=json.dumps(formulas),text=True,capture_output=True,check=True)
rendered=dict(zip(formulas,json.loads(proc.stdout)))

def svg(kind,label):
    """Small conceptual diagrams, not artwork; plotted curves use actual functions."""
    body=""
    def line(x,y,X,Y,extra=""):
        return f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" {extra}/>'
    def text(x,y,t,extra=""):
        return f'<text x="{x}" y="{y}" {extra}>{esc(t)}</text>'
    def rect(x,y,w,h,extra=""):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {extra}/>'
    if kind in ["wave","gaussian","density","positive","sinc","oscillation","decay","flat","singular","green","pulse"]:
        body=line(12,60,144,60,'class="axis"')+line(78,7,78,64,'class="axis"')
        if kind=="density":
            for mu in [-1,0,1.2]:
                pts=[(12+i*1.1,60-28*math.exp(-((i/120*8-4-mu)/.8)**2/2)) for i in range(121)]
                body+='<path d="'+' '.join(('M' if i==0 else 'L')+f'{x:.2f},{y:.2f}' for i,(x,y) in enumerate(pts))+'" opacity=".3"/>'
        def f(x):
            if kind=="flat": return .5
            if kind=="sinc": return math.sin(2.6*x)/(2.6*x) if abs(x)>1e-10 else 1
            if kind=="oscillation": return .35+math.cos(2.7*x)*.3
            if kind=="decay": return math.exp(-(x+4)/2)
            if kind=="singular": return 1/x if abs(x)>.42 else None
            if kind=="green":return max(0,1-abs(x/4))
            return math.exp(-x*x/2)
        drawing=[];restart=True
        for i in range(121):
            x=i/120*8-4;y=f(x)
            if y is None:restart=True;continue
            y=min(1.15,max(-.2,y))
            drawing.append(("M" if restart else "L")+f'{12+i*1.1:.2f},{60-43*y:.2f}');restart=False
        body+='<path d="'+' '.join(drawing)+'"/>'
    elif kind in ["filter","cross","matrix","gram"]:
        n=3 if kind in ["filter","cross"] else 4
        for i in range(n):
            for j in range(n):
                v=math.exp(-(i-j)**2/2) if kind=="gram" else (i+j+1)/8
                if kind=="cross":v=1 if (i==1 or j==1) else 0
                body+=rect(39+j*19,7+i*15,16,12,f'fill="currentColor" stroke="none" opacity="{.12+.75*v:.3f}"')
        if kind=="filter":body+=text(107,34,"Σ", 'font-size="18"')
    elif kind=="null":
        body=line(16,38,142,38,'class="axis"')+line(78,6,78,68,'class="axis"')+line(22,10,134,66)+text(88,16,"Ax = 0")
    elif kind=="map":
        for i in range(4):
            body+=f'<circle cx="35" cy="{12+i*15}" r="3"/>'+line(41,12+i*15,115,38,'opacity=".5"')
        body+='<circle cx="121" cy="38" r="8"/>'+text(118,42,"0")
    elif kind in ["core","layers"]:
        if kind=="core":
            body+=rect(24,7,107,59,'opacity=".25"')+rect(38,19,79,35,'opacity=".55"')+rect(55,28,45,17,'fill="currentColor" fill-opacity=".1"')+text(61,40,"core")
        else:
            for i,t in enumerate(["interface","core","resources"]):
                body+=rect(25,5+i*23,105,18,'fill="currentColor" fill-opacity="'+(".14" if i==1 else ".03")+'"')+text(78,18+i*23,t,'text-anchor="middle"')
    elif kind in ["bits","factors","features"]:
        vals=["0","1","1","0","1"] if kind=="bits" else (["2³","×","3²","→","2·3"] if kind=="factors" else ["x","x²","√2x","1"])
        for i,t in enumerate(vals):
            body+=text(16+i*(125/(len(vals)-1)),40,t,'text-anchor="middle"')
        body+=line(12,55,143,55,'class="axis"')
    elif kind=="partition":
        for i in range(3):
            body+=rect(15+i*45,7,35,59,'opacity=".4"')
            for j in range(3):body+=f'<circle cx="{32+i*45}" cy="{19+j*17}" r="3"/>'
    elif kind in ["grid","tiles"]:
        for i in range(3):
            for j in range(8):
                body+=rect(14+j*16,10+i*18,12,13,f'fill="currentColor" fill-opacity="{.14 if kind=="grid" else .08+(j//3)*.1}"')
        if kind=="tiles":body+=rect(12,8,48,53,'stroke-width="2"')+rect(60,8,48,53,'stroke-width="2"')
    elif kind in ["graph","reduce"]:
        pts=[(23,37),(60,13),(60,60),(101,37),(138,37)]
        for a,b in [(0,1),(0,2),(1,3),(2,3),(3,4)]:body+=line(*pts[a],*pts[b],'opacity=".4"')
        for i,(x,y) in enumerate(pts):body+=f'<circle cx="{x}" cy="{y}" r="4" fill="currentColor" fill-opacity=".5" />'
    elif kind=="digraph":
        for i,x in enumerate([26,78,130]):
            body+=f'<circle cx="{x}" cy="33" r="11" fill="currentColor" fill-opacity="{.2 if i!=1 else 0}"/>'+text(x,37,["a","b","c"][i],'text-anchor="middle"')
        for x in [38,90]:
            body+=line(x,33,x+27,33)+f'<path d="M{x+21} 29L{x+27} 33L{x+21} 37"/>'
        body+=text(78,65,"K = {a, c}",'text-anchor="middle"')
    elif kind=="region":
        body+='<path d="M20 61V12H81V30H136V61Z" opacity=".5"/>'+rect(20,30,61,31,'fill="currentColor" fill-opacity=".16"')
        body+=text(40,50,"K")
    elif kind=="kern":
        body+=rect(27,8,102,60,'opacity=".5"')+'<path d="M61 38L78 28L95 38L78 48Z" fill="currentColor" fill-opacity=".2"/>'
    elif kind in ["circle","orbit","geometry"]:
        body+='<circle cx="77" cy="37" r="28" opacity=".5"/>'+line(49,37,105,37,'class="axis"')+line(77,9,77,65,'class="axis"')
        body+='<circle cx="90" cy="26" r="4" fill="currentColor"/>'
        if kind=="orbit":body+='<ellipse cx="77" cy="37" rx="60" ry="16" transform="rotate(-20 77 37)" opacity=".7"/>'
        if kind=="geometry":body+='<path d="M31 55L110 15L135 60Z"/>'
    elif kind=="category":
        body+=text(22,23,"K")+text(80,23,"A")+text(134,23,"B")
        body+=line(37,19,72,19)+line(94,19,129,19)+text(50,13,"k")+text(110,13,"f")+text(73,58,"f ∘ k = 0",'text-anchor="middle"')
    elif kind=="probability":
        body+=rect(33,10,90,53,'opacity=".3"')
        for i,row in enumerate([["0.8","0.2"],["0.3","0.7"]]):
            for j,v in enumerate(row):body+=text(56+j*44,30+i*23,v,'text-anchor="middle"')
    elif kind=="cantor":
        for row in range(4):
            for i in range(2**row):
                loc=sum(((i>>(row-1-j))&1)*2/3**(j+1) for j in range(row))
                body+=line(15+loc*126,12+row*15,15+(loc+1/3**row)*126,12+row*15,'stroke-width="4"')
    elif kind=="proof":
        body+=rect(10,18,48,36)+rect(73,18,73,36,'fill="currentColor" fill-opacity=".08"')+line(58,36,73,36)+text(34,40,"p : P",'text-anchor="middle"')+text(109,40,"check",'text-anchor="middle"')
    elif kind in ["timeline","sensitivity"]:
        body+=line(10,55,144,55,'class="axis"')
        for i in range(6):
            body+=line(18+i*22,55,18+i*22,17+(i%3)*10)
            body+=f'<circle cx="{18+i*22}" cy="{17+(i%3)*10}" r="3" fill="currentColor"/>'
    else:body+=text(78,42,"K",'text-anchor="middle" font-size="30"')
    return f'<svg class="glyph" viewBox="0 0 156 76" role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>{body}</svg>'

nav='<button type="button" class="family-filter active" data-family="all" aria-pressed="true"><span>All families</span><span class="nav-count">'+str(len(entries))+'</span></button>'
mapcards=[]
for i,f in enumerate(families.values(),1):
    count=sum(e["family"]==f["id"] for e in entries)
    nav+=f'<button type="button" class="family-filter" data-family="{f["id"]}" aria-pressed="false" style="--family:{f["color"]}"><span class="family-dot"></span><span>{esc(f["name"])}</span><span class="nav-count">{count}</span></button>'
    mapcards.append(f'<button type="button" class="family-card" data-family="{f["id"]}" style="--family:{f["color"]}"><span class="family-card-top"><span class="eyebrow">{i:02d}</span>{svg(f["visual"],f["name"]+" conceptual diagram")}</span><span class="family-card-name">{esc(f["name"])}</span><span class="family-question">{esc(f["description"])}</span><span class="family-tags">{esc(" · ".join(f["tags"]))}</span><span class="family-size">{count} entries</span></button>')
specimens=[]
for i,e in enumerate(entries,1):
    f=families[e["family"]]
    source_links="".join(f'<a href="{esc(SOURCES[r]["url"])}" target="_blank" rel="noopener">{esc(SOURCES[r]["title"])}<span>{esc(SOURCES[r]["publisher"])}</span></a>' for r in e["refs"])
    related="".join(f'<a href="#{r}" class="related-link">{esc(byid[r]["name"])}</a>' for r in e["related"])
    if e["variants"] and isinstance(e["variants"][0],list):
        variants='<table class="variant-table"><caption>SPICE file families</caption><thead><tr><th scope="col">Type</th><th scope="col">Contents</th></tr></thead><tbody>'+''.join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td></tr>' for a,b in e["variants"])+'</tbody></table>'
    else:variants=('<div class="variant-label">Also in this family</div><ul class="variants">'+''.join(f'<li>{esc(v)}</li>' for v in e["variants"])+'</ul>') if e["variants"] else ""
    code=f'<pre><code>{esc(e["code"])}</code></pre>' if e["code"] else ""
    equation=f'<div class="equation">{rendered[e["tex"]]}</div>' if e["tex"] else ""
    search=" ".join([e["name"],e["domain"],e["short"],e["body"],e["note"],f["name"],str(e["variants"])]).lower()
    specimens.append(f'''<details class="specimen" id="{e["id"]}" data-family="{e["family"]}" data-search="{esc(search)}" style="--family:{f["color"]}">
<summary><span class="specimen-meta"><span>{i:03d} / {esc(e["domain"])}</span><span class="disclosure" aria-hidden="true">+</span></span><span class="specimen-title">{esc(e["name"])}</span><span class="specimen-bottom"><span class="specimen-short">{esc(e["short"])}</span>{svg(e["visual"],"Concept sketch: "+e["name"])}</span></summary>
<div class="specimen-content"><div class="specimen-main"><span class="status-label">{esc(e["status"])}</span><p class="definition">{esc(e["body"])}</p>{equation}<div class="worked"><h4>One example</h4><p>{esc(e["example"])}</p>{code}</div><div class="distinction"><h4>Keep the distinction</h4><p>{esc(e["note"])}</p></div>{variants}</div><aside class="specimen-aside"><h4>Connections</h4><div class="related">{related or '<span>No cross-family connection implied.</span>'}</div><h4>Read the sources</h4><div class="entry-sources">{source_links}</div><a class="permalink" href="#{e["id"]}">Link to this entry</a></aside></div></details>''')

bibliography=[]
for n,r in enumerate(sorted(used,key=lambda r:SOURCES[r]["publisher"].lower()),1):
    s=SOURCES[r]
    bibliography.append(f'<li id="source-{r}"><span class="source-no">{n:03d}</span><div><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a><p>{esc(s["publisher"])} <span>· {esc(s["kind"])}</span></p></div></li>')

template=(HERE/"template.html").read_text()
for key,value in {"COUNT":str(len(entries)),"SOURCECOUNT":str(len(used)),"NAV":nav,"MAP":"".join(mapcards),"SPECIMENS":"".join(specimens),"SOURCES":"".join(bibliography)}.items():
    template=template.replace("@@"+key+"@@",value)
assert "@@" not in template
(OUT/"index.html").write_text(template)
(OUT/"catalog.json").write_text(json.dumps({"families":list(families.values()),"entries":entries,"sources":{r:SOURCES[r] for r in sorted(used)}},ensure_ascii=False,indent=2))
print(f"Built {len(entries)} entries / {len(used)} cited sources / {len(formulas)} checked equations.")
