"""Check diagram placement, portable assets, fence behavior, and numerical drawings."""
from pathlib import Path
from html.parser import HTMLParser
import itertools
import json
import math
import re
import xml.etree.ElementTree as ET
from diagrams import prepare_diagrams, asset_key, svg_info, ASSETS, CACHE, PUBLIC
from formatting import markdown, iter_code_blocks, prepare_math, MATH
ROOT=Path(__file__).parent; WEB=ROOT.parent
SLUGS=[c['slug'] for c in json.loads((ROOT/'catalog.json').read_text())['courses']]
prepare_diagrams(SLUGS, [])

class Figures(HTMLParser):
    def __init__(self):super().__init__();self.figures=[];self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='figure' and 'data-visual-id' in a:self.figures.append(a['data-visual-id'])
        if tag=='img' and '/assets/diagrams/' in a.get('src',''):self.images.append(a)

summary={}; first_mermaid=None
for slug in SLUGS:
    manifest=json.loads((ROOT/slug/'visuals.json').read_text());schedule=json.loads((ROOT/slug/'schedule.json').read_text())
    routes={s['key']:WEB/slug/f"week-{w['week']:02d}"/f"day-{i:02d}"/'index.html' for w in schedule for i,d in enumerate(w['days'],1) for s in d['steps']}
    expected={}; actual={}
    for v in manifest:
        source=(ROOT/slug/v['source']).read_text();key=asset_key(source,v['renderer'])
        assert (CACHE/(key+'.svg')).read_bytes()==(PUBLIC/(key+'.svg')).read_bytes(),v['id']
        svg=(PUBLIC/(key+'.svg')).read_text();width,height=svg_info(svg)
        assert len(svg)<150_000,(v['id'],'unexpectedly heavy SVG')
        assert width<=1200 and height<=1000,(v['id'],width,height)
        assert '<foreignObject' not in svg and '<script' not in svg
        assert len(v['description'])>=60 and v['checks'] and v['evidence'],v['id']
        route=routes.get(v['lesson'],WEB/slug/'week-01/day-00/index.html')
        expected[v['id']]=route
        if v['renderer']=='mermaid' and first_mermaid is None:first_mermaid=source.strip()
    for p in (WEB/slug).rglob('*.html'):
        d=Figures();d.feed(p.read_text())
        assert len(d.figures)==len(d.images),p
        for id in d.figures:
            assert id not in actual,('duplicate figure',id)
            actual[id]=p
        for image in d.images:
            assert len(image.get('alt',''))>=60 and image.get('width') and image.get('height'),p
            assert image.get('loading')=='lazy' and image.get('decoding')=='async',p
            assert (WEB.parent/image['src'].lstrip('/')).exists(),p
    assert actual==expected,(slug,'diagram placed on wrong page')
    summary[slug]={'figures':len(manifest),'mermaid':sum(v['renderer']=='mermaid' for v in manifest)}

# A published source exercises real pre-rendered Mermaid output, including parser edge cases.
for opening,closing in [('```mermaid','```'),('```Mermaid','````'),('~~~MERMAID','~~~~')]:
    html=markdown(opening+'\n'+first_mermaid+'\n'+closing)
    assert 'lesson-visual' in html and 'language-mermaid' not in html
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

# Recalculate the illustrated online-softmax example independently from dense weights.
weights=[math.exp(s-4) for s in [1,2,4]];denom=sum(weights)
result=[(weights[0]+weights[2])/denom,(weights[1]+weights[2])/denom]
text=' '.join(svg('gpu-kernels','online-rescaling').itertext())
assert all(f'{value:.4f}' in text for value in result)
assert len(set(itertools.product(range(16),range(2),range(3))))==96
print('PASS: every figure placement, source/cache/public agreement, SVG accessibility, fence parsing, causal masks, cache bars, Amdahl curve, and online-softmax arithmetic.')
print(json.dumps(summary,indent=2))
