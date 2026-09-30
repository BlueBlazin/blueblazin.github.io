"""Read-only checks of diagram coverage, placement, assets, and numerical drawings."""
from pathlib import Path
from html.parser import HTMLParser
import itertools
import json
import math
import re
import struct
import xml.etree.ElementTree as ET
from diagrams import asset_key, svg_info, mermaid_metadata, validate_visual_audit, ASSETS, CACHE, PUBLIC
from formatting import markdown, iter_code_blocks, prepare_math, MATH, strings
ROOT=Path(__file__).parent; WEB=ROOT.parent
SLUGS=[c['slug'] for c in json.loads((ROOT/'catalog.json').read_text())['courses']]

# Inspect what the build produced. Never repair, copy, delete, or rerender assets here.
sources={}; prose_keys={}; manifests={}; first_mermaid=None
for slug in SLUGS:
    folder=ROOT/slug
    lessons=json.loads((folder/'lessons-course.json').read_text())
    manifests[slug]=json.loads((folder/'visuals.json').read_text())
    validate_visual_audit(folder,lessons,manifests[slug])
    for visual in manifests[slug]:
        source=(folder/visual['source']).read_text();renderer=visual['renderer']
        sources[asset_key(source,renderer)]=(source,renderer)
        if renderer=='mermaid' and first_mermaid is None:first_mermaid=source.strip()
    prose=[];prose_keys[slug]=set()
    for path in folder.glob('*'):
        if path.suffix=='.json' and path.name not in {'course-data.json','course-index.json'}:prose.extend(strings(json.loads(path.read_text())))
        elif path.suffix=='.md':prose.append(path.read_text())
    for value in prose:
        for block in iter_code_blocks(value):
            if block['language']=='mermaid':
                source=block['body'].strip();mermaid_metadata(source);key=asset_key(source,'mermaid')
                sources[key]=(source,'mermaid');prose_keys[slug].add(key)

ASSETS.clear()
for key,(source,renderer) in sources.items():
    cached=CACHE/(key+'.svg');public=PUBLIC/(key+'.svg')
    assert cached.is_file() and public.is_file(),(key,'Missing built diagram asset')
    assert cached.read_bytes()==public.read_bytes(),(key,'Public asset differs from cache')
    if renderer=='svg':assert cached.read_text()==source,(key,'SVG source differs from cache')
    rendered=public.read_text();width,height=svg_info(rendered)
    assert len(rendered)<150_000 and width<=1200 and height<=1000,(key,'Oversized diagram',width,height)
    if renderer=='mermaid':
        title,description=mermaid_metadata(source);root=ET.fromstring(rendered)
        assert root.find('{http://www.w3.org/2000/svg}title').text==title,(key,'Mermaid title mismatch')
    ASSETS[key]={'url':'/courses/assets/diagrams/'+key+'.svg','width':width,'height':height,'renderer':renderer}
assert {p.stem for p in PUBLIC.glob('*.svg')}==sources.keys(),'Stale or unrecognized public diagrams'

class Figures(HTMLParser):
    def __init__(self):super().__init__();self.figures=[];self.images=[];self.stack=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='figure' and 'lesson-visual' in a.get('class','').split():
            containers=[d['id'] for t,d in self.stack if d.get('id','').startswith(('hour-','reference-'))]
            slots=[d['data-visual-slot'] for t,d in self.stack if 'data-visual-slot' in d]
            answers=[d for t,d in self.stack if t=='details' and 'selfcheck' in d.get('class','').split()]
            row={'id':a.get('data-visual-id'),'asset':a.get('data-diagram-asset'),'container':containers[-1] if containers else None,'slot':slots[-1] if slots else None,'answer':bool(answers),'open_answer':any('open' in d for d in answers),'images':[],'links':[]}
            self.figures.append(row);a['_figure']=row
        parents=[d['_figure'] for t,d in self.stack if '_figure' in d]
        if tag=='img' and '/assets/diagrams/' in a.get('src',''):
            assert parents,'Diagram image outside a figure'
            self.images.append(a);parents[-1]['images'].append(a)
        if tag=='a' and parents:parents[-1]['links'].append(a.get('href'))
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append((tag,a))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:del self.stack[i:];break

summary={}
for slug in SLUGS:
    manifest=manifests[slug];schedule=json.loads((ROOT/slug/'schedule.json').read_text())
    lessons=json.loads((ROOT/slug/'lessons-course.json').read_text());audit=json.loads((ROOT/slug/'visual-audit.json').read_text())
    by_lesson={key:[] for key in lessons}
    for v in manifest:by_lesson[v['lesson']].append(v['id'])
    routes={s['key']:WEB/slug/f"week-{w['week']:02d}"/f"day-{i:02d}"/'index.html' for w in schedule for i,d in enumerate(w['days'],1) for s in d['steps']}
    containers={s['key']:'hour-'+str(i) for w in schedule for d in w['days'] for i,s in enumerate(d['steps'],1)}
    visual_by_id={v['id']:v for v in manifest}
    expected={v['id']:routes.get(v['lesson'],WEB/slug/'week-01/day-00/index.html') for v in manifest};actual={}
    for p in (WEB/slug).rglob('*.html'):
        doc=Figures();doc.feed(p.read_text())
        assert len(doc.figures)==len(doc.images),p
        for figure in doc.figures:
            identifier=figure['id'];key=figure['asset']
            assert key in ASSETS and len(figure['images'])==1,(p,identifier,'Invalid figure asset')
            asset=ASSETS[key];image=figure['images'][0]
            assert image['src']==asset['url'] and asset['url'] in figure['links'],(p,identifier,'Wrong SVG or full-size link')
            assert image.get('width')==str(round(asset['width'])) and image.get('height')==str(round(asset['height'])),(p,identifier,'Wrong image dimensions')
            assert image.get('loading')=='lazy' and image.get('decoding')=='async',p
            if identifier is None:
                assert key in prose_keys[slug],(p,'Unnamed figure has no Mermaid source fence')
                assert image.get('alt')==mermaid_metadata(sources[key][0])[1],p
                continue
            assert identifier in visual_by_id and identifier not in actual,(p,'Unknown or duplicate figure',identifier)
            actual[identifier]=p;v=visual_by_id[identifier]
            expected_key=asset_key((ROOT/slug/v['source']).read_text(),v['renderer'])
            assert key==expected_key,(p,identifier,'Figure points to another diagram source')
            assert image.get('alt')==v['description'] and len(v['description'])>=60,(p,identifier,'Wrong text alternative')
            container=containers.get(v['lesson'],'reference-'+v['lesson'])
            assert (figure['container'],figure['slot'],figure['answer'],figure['open_answer'])==(container,v['placement'],v['placement']=='self-check',False),(slug,identifier,'Wrong lesson/slot or exposed answer',figure)
    assert actual==expected,(slug,'Diagram placed on wrong page')
    summary[slug]={'lessons_reviewed':len(audit),'lessons_with_visuals':sum(bool(ids) for ids in by_lesson.values()),'figures':len(manifest),'mermaid':sum(v['renderer']=='mermaid' for v in manifest)}

# A published source exercises real pre-rendered Mermaid output, including parser edge cases.
for opening,closing in ([('```mermaid','```'),('```Mermaid','````'),('~~~MERMAID','~~~~')] if first_mermaid else []):
    html=markdown(opening+'\n'+first_mermaid+'\n'+closing)
    assert 'lesson-visual' in html and 'language-mermaid' not in html
    parsed=Figures();parsed.feed(html)
    assert len(parsed.figures)==len(parsed.images)==1 and parsed.figures[0]['id'] is None
    assert parsed.figures[0]['asset']==asset_key(first_mermaid,'mermaid')
    assert parsed.images[0]['src']==ASSETS[parsed.figures[0]['asset']]['url']
literal='````text\n```mermaid\nnot a diagram\n```\n````'
blocks=list(iter_code_blocks(literal));assert len(blocks)==1 and blocks[0]['language']=='text'
assert '<code class="language-text">```mermaid' in markdown(literal)
prepare_math([literal.replace('not a diagram',r'\(not valid TeX!\)')])
assert ('not valid TeX!',False) not in MATH

# Bind mathematical assertions to the geometry that the student actually sees.
ns={'s':'http://www.w3.org/2000/svg'}
def svg(slug,name):return ET.parse(ROOT/slug/'visuals'/(name+'.svg')).getroot()
mask=svg('llm-architectures','causal-attention-mask')
cells=[e for e in mask.iter() if 'data-row' in e.attrib]
assert len(cells)==64
for c in cells:assert (c.attrib['data-allowed']=='true')==(int(c.attrib['data-col'])<=int(c.attrib['data-row']))
assert sum(c.attrib['data-allowed']=='true' for c in cells)==36
mask=svg('gpu-kernels','causal-tiles')
cells=[e for e in mask.iter() if e.tag.endswith('rect') and e.get('width')=='34' and e.get('height')=='34']
assert len(cells)==64
for c in cells:
    row=(int(c.get('y'))-121)//36;col=(int(c.get('x'))-116)//36
    assert (c.get('fill')=='#e1f0ec')==(col<=row)

chart=svg('llm-architectures','mla-cache-comparison')
bars=[e for e in chart.iter() if 'data-mib' in e.attrib]
assert len(bars)==4
expected=[2*1*8*2048*4*64*2/2**20,1*8*2048*(128+32)*2/2**20,32,10]
for bar,mib in zip(bars,expected):assert float(bar.get('data-mib'))==mib and float(bar.get('width'))==16*mib
chart=svg('gpu-kernels','amdahl-limit')
curve=chart.find('.//s:polyline',ns);points=[tuple(map(float,p.split(','))) for p in curve.get('points').split()]
assert len(points)==181
# Axes in this drawing: kernel speedup 1..10 maps x=97..739; overall 1..1.27 maps y=356..124.
for x,y in points:
    speed=1+(x-97)*9/(739-97);expected_y=356-(1/(.8+.2/speed)-1)*(356-124)/.27
    assert abs(y-expected_y)<.03,(x,y,expected_y)

# Hybrid storage uses different dtypes for fixed recurrent state and growing KV state.
chart=svg('llm-architectures','hybrid-state-scaling')
lines=[e for e in chart.iter() if e.tag.endswith('line') and e.get('stroke-width')=='3']
fixed=1*8*4*32*32*4/2**20
per_token=2*1*2*2*32*2/2**20
assert len(lines)==3 and fixed==.125 and per_token==1/2048
for line,(left,right) in zip(lines,[(fixed,fixed),(0,4096*per_token),(fixed,fixed+4096*per_token)]):
    assert float(line.get('x1'))==130 and float(line.get('x2'))==688
    # The zero baseline is y=331; the plotted range is 2.25 MiB over 218 pixels.
    assert math.isclose(float(line.get('y1')),331-left*218/2.25,abs_tol=1e-8)
    assert math.isclose(float(line.get('y2')),331-right*218/2.25,abs_tol=1e-8)
assert fixed+512*per_token==.375 and fixed+4096*per_token==2.125

# Independently round through IEEE binary32, rather than using the diagram's labels as arithmetic.
large=2**24
rounded=[struct.unpack('f',struct.pack('f',large+i))[0] for i in range(3)]
assert rounded==[large,large,large+2]
rounding_text=' '.join(svg('gpu-kernels','input-rounding').itertext())
assert '16,777,216' in rounding_text and '[0, 0, 2]' in rounding_text

# Recalculate the illustrated online-softmax example independently from dense weights.
weights=[math.exp(s-4) for s in [1,2,4]];denom=sum(weights)
result=[(weights[0]+weights[2])/denom,(weights[1]+weights[2])/denom]
text=' '.join(svg('gpu-kernels','online-rescaling').itertext())
assert all(f'{value:.4f}' in text for value in result)
assert len(set(itertools.product(range(16),range(2),range(3))))==96
print('PASS: complete lesson audit; every figure placement and answer disclosure; source/cache/public agreement; accessibility; fence parsing; causal masks, cache bars, hybrid storage, FP32 rounding, Amdahl curve, and online-softmax arithmetic.')
print(json.dumps(summary,indent=2))
