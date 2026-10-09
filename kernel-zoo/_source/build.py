from pathlib import Path
import html, json, subprocess
from catalog import SOURCES, ENTRIES
from design import SECTIONS, PRIORITY, MAJOR, OVERVIEW, ALIASES, TYPES, DEFAULT_TYPES, LINKS
from icons import svg

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
esc=html.escape
original={e['id']:e for e in ENTRIES}
section_for={entry:sid for sid,name,color,members in SECTIONS for entry in members.split()}
assert len(section_for)==len(ENTRIES) and set(section_for)==set(original), 'Incomplete or duplicate display taxonomy'
assert sum(len(s[3].split()) for s in SECTIONS)==len(ENTRIES), 'Duplicate section assignment'
sections=[dict(id=sid,name=name,color=color,count=len(members.split())) for sid,name,color,members in SECTIONS]
bysection={s['id']:s for s in sections}
rank={eid:i for i,eid in enumerate(PRIORITY)}
entries=[]
for original_entry in ENTRIES:
    e=original_entry.copy()
    e['formalName']=e['name']
    e['name']={'linux':'Linux / OS kernel','psd':'SVM / similarity kernel','nullspace':'Nullspace / linear-algebra kernel','lean':'Lean proof kernel'}.get(e['id'],e['name'])
    e['semanticFamily']=e['family']
    e['family']=section_for[e['id']]
    e['alias']=ALIASES.get(e['id'],e['name'])
    e['type']=TYPES.get(e['id'],DEFAULT_TYPES[e['semanticFamily']])
    e['rank']=rank.get(e['id'],100)
    entries.append(e)
entries.sort(key=lambda e:(e['rank'],e['name'].casefold()))
byid={e['id']:e for e in entries}
used=set(r for e in entries for r in e['refs'])
assert all(r in SOURCES for r in used)
assert all(r in byid for e in entries for r in e['related'])
assert all(a in byid and b in byid for a,b,_,_ in LINKS)
assert set(OVERVIEW)<=set(byid)

formulas=list(dict.fromkeys(e['tex'] for e in entries if e['tex']))
proc=subprocess.run(['node','-e',r"""
const fs=require('fs'),k=require(process.argv[1]);
process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x,{displayMode:true,throwOnError:true,output:'htmlAndMathml'}))));
""",str(OUT.parent/'courses/_source/vendor/katex/katex.min.js')],input=json.dumps(formulas),text=True,capture_output=True,check=True)
rendered=dict(zip(formulas,json.loads(proc.stdout)))
links=[dict(a=a,b=b,label=label,kind=kind) for a,b,label,kind in LINKS]
data=dict(families=sections,entries=entries,sources={r:SOURCES[r] for r in sorted(used)},links=links,major=MAJOR,overview=OVERVIEW)
(OUT/'catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
webentries=[]
for e in entries:
    w=e.copy()
    w['equation']=rendered.get(e['tex'],'')
    w['icon']=svg(e['visual'],e['alias']+' concept diagram')
    webentries.append(w)
webdata={**data,'entries':webentries}
scopes='<option value="common">Common kernels</option><option value="all">All '+str(len(entries))+' kernels</option>'
indexscopes='<option value="all">All fields</option>'
topics=[]
for s in sections:
    option=f'<option value="{s["id"]}">{esc(s["name"])}</option>'
    scopes+=option;indexscopes+=option
    topics.append(f'<button type="button" class="index-topic" data-topic="{s["id"]}" style="--topic:{s["color"]}"><i></i>{esc(s["name"])}<span>{s["count"]}</span></button>')
sources=[]
for r in sorted(used,key=lambda r:SOURCES[r]['publisher'].casefold()):
    s=SOURCES[r]
    sources.append(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a><span>{esc(s["publisher"])}</span></li>')
labs=(HERE/'labs.html').read_text()
for name in ['gram','cuda','null']:labs=labs.replace(f'id="{name}-lab"',f'id="{name}-lab" hidden')
template=(HERE/'template.html').read_text()
replacements={'COUNT':str(len(entries)),'SOURCECOUNT':str(len(used)),'SCOPES':scopes,'INDEXSCOPES':indexscopes,'TOPICS':''.join(topics),'LABS':labs,'SOURCES':''.join(sources),'DATA':json.dumps(webdata,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')}
for key,value in replacements.items():template=template.replace('@@'+key+'@@',value)
assert '@@' not in template
(OUT/'index.html').write_text(template)

static=[]
for e in entries:
    refs=''.join(f'<li><a href="{esc(SOURCES[r]["url"])}">{esc(SOURCES[r]["title"])}</a> — {esc(SOURCES[r]["publisher"])}</li>' for r in e['refs'])
    related=' · '.join(f'<a href="#{r}">{esc(byid[r]["alias"])}</a>' for r in e['related'])
    variants=''
    if e['variants']:
        if isinstance(e['variants'][0],list):variants='<table><thead><tr><th>Type</th><th>Contents</th></tr></thead><tbody>'+''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a,b in e['variants'])+'</tbody></table>'
        else:variants='<p><strong>Variants:</strong> '+esc(' · '.join(e['variants']))+'</p>'
    equation='<div class="equation">'+rendered[e['tex']]+'</div>' if e['tex'] else ''
    code='<pre><code>'+esc(e['code'])+'</code></pre>' if e['code'] else ''
    static.append(f'<details id="{e["id"]}"><summary>{esc(e["name"])}</summary><p class="static-field">{esc(bysection[e["family"]]["name"])} · {esc(e["type"])}</p><p>{esc(e["body"])}</p>{equation}<h3>Example</h3><p>{esc(e["example"])}</p>{code}<p>{esc(e["note"])}</p>{variants}<p>{related}</p><ul>{refs}</ul></details>')
reference='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kernel zoo — static catalogue</title><link rel="stylesheet" href="../courses/assets/katex/katex.min.css"><link rel="stylesheet" href="styles.css?v=2"></head><body class="static-page"><main><a href="./">Interactive map</a><h1>Kernel zoo</h1><p>'+str(len(entries))+' definitions, examples, and sources.</p>'+''.join(static)+'</main></body></html>'
(OUT/'reference.html').write_text(reference)
print(f'Built {len(entries)} entries / {len(sections)} fields / {len(used)} sources / {len(formulas)} equations.')
