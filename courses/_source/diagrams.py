"""Pre-rendered, accessible SVG figures for course lessons and Mermaid fences."""
from html import escape
from pathlib import Path
import hashlib
import json
import math
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from formatting import iter_code_blocks

ROOT = Path(__file__).parent
CACHE = ROOT / 'diagram-cache'
PUBLIC = ROOT.parent / 'assets' / 'diagrams'
CONFIG = (ROOT / 'mermaid-config.json').read_text()
RENDERER = 'mermaid-cli-12.0.0'
ASSETS = {}
VISUALS = {}


def svg_info(svg):
    """Reject broken/executable/external SVG content before publishing it."""
    root = ET.fromstring(svg)
    assert root.tag == '{http://www.w3.org/2000/svg}svg', 'Expected an SVG root'
    bounds = [float(x) for x in re.split(r'[ ,]+', root.attrib.get('viewBox', '').strip())]
    assert len(bounds) == 4 and all(math.isfinite(x) for x in bounds) and min(bounds[2:]) > 0, 'SVG needs a finite viewBox'
    assert root.find('{http://www.w3.org/2000/svg}title') is not None, 'SVG needs a title'
    assert root.find('{http://www.w3.org/2000/svg}desc') is not None, 'SVG needs a description'
    for element in root.iter():
        tag = element.tag.rsplit('}', 1)[-1]
        assert tag not in {'script', 'foreignObject', 'iframe', 'image', 'a', 'animate', 'set'}, f'Unsupported SVG element: {tag}'
        for key, value in element.attrib.items():
            key = key.rsplit('}', 1)[-1]
            assert not key.lower().startswith('on'), 'Event attributes are not allowed'
            if key in {'href', 'src'}: assert value.startswith('#'), 'External SVG references are not allowed'
    assert not re.search(r'@import|url\(\s*["\']?(?!#)[a-z]+:', svg, re.I), 'External SVG assets are not allowed'
    return bounds[2], bounds[3]


def mermaid_metadata(source):
    assert not re.search(r'%%\{|^\s*click\s|^---\s*$', source, re.M), 'Use the shared Mermaid configuration; no directives or links'
    title = re.search(r'^\s*accTitle:\s*(.+)$', source, re.M)
    description = re.search(r'^\s*accDescr:\s*(.+)$', source, re.M)
    if not description: description = re.search(r'^\s*accDescr\s*\{(.*?)\}', source, re.S | re.M)
    assert title and description, 'Mermaid diagrams need accTitle and accDescr'
    return title[1].strip(), ' '.join(description[1].split())


def asset_key(source, renderer):
    if renderer == 'mermaid': source = source.strip()
    settings = (RENDERER + CONFIG) if renderer == 'mermaid' else 'course-svg-v1'
    return hashlib.sha256((settings + '\n' + source).encode()).hexdigest()[:24]


def prepare_diagrams(slugs, prose):
    ASSETS.clear(); VISUALS.clear()
    sources = {}
    for slug in slugs:
        folder = ROOT / slug
        manifest = folder / 'visuals.json'
        if not manifest.exists(): continue
        lessons = json.loads((folder / 'lessons-course.json').read_text())
        resource_ids = {r['id'] for r in json.loads((folder / 'resources.json').read_text())}
        ids = set()
        for visual in json.loads(manifest.read_text()):
            required = {'id','lesson','placement','title','description','caption','renderer','source','evidence','checks'}
            assert required <= visual.keys(), (slug, visual)
            assert re.fullmatch(r'[a-z0-9-]+', visual['id']) and visual['id'] not in ids
            ids.add(visual['id'])
            assert visual['lesson'] in lessons, visual['lesson']
            placement = visual['placement']
            assert placement == 'key-idea' or (re.fullmatch(r'plan-[0-9]+', placement) and int(placement[5:]) < len(lessons[visual['lesson']]['plan'])), placement
            assert visual['renderer'] in {'mermaid','svg'}
            assert all(visual[k].strip() for k in ('title','description','caption'))
            assert visual['checks'] and visual['evidence']
            assert all(ref in resource_ids or ref.startswith('https://') for ref in visual['evidence']), visual['evidence']
            path = (folder / visual['source']).resolve()
            assert path.is_relative_to((folder / 'visuals').resolve()), path
            source = path.read_text()
            if visual['renderer'] == 'mermaid': mermaid_metadata(source)
            key = asset_key(source, visual['renderer'])
            sources[key] = (source, visual['renderer'])
            visual = {**visual, 'asset': key}
            VISUALS.setdefault((slug, visual['lesson'], placement), []).append(visual)
    for value in prose:
        for block in iter_code_blocks(value):
            if block['language'] != 'mermaid': continue
            source = block['body'].strip()
            mermaid_metadata(source)
            sources[asset_key(source, 'mermaid')] = (source, 'mermaid')
    CACHE.mkdir(exist_ok=True); PUBLIC.mkdir(parents=True, exist_ok=True)
    pending = []
    for key, (source, renderer) in sources.items():
        cached = CACHE / (key + '.svg')
        if renderer == 'svg': cached.write_text(source)
        elif not cached.exists(): pending.append({'id':'diagram-'+key,'source':source,'output':str(cached)})
    if pending:
        run = subprocess.run(['node',str(ROOT/'render-diagrams.mjs')],input=json.dumps(pending),text=True,capture_output=True)
        if run.returncode: raise RuntimeError('Diagram rendering failed. Run npm ci in courses/_source when creating new diagrams.\n'+run.stderr)
    used = set()
    for key, (source, renderer) in sources.items():
        cached = CACHE / (key + '.svg')
        width, height = svg_info(cached.read_text())
        target = PUBLIC / cached.name
        shutil.copyfile(cached, target); used.add(target.name)
        ASSETS[key] = {'url':'/courses/assets/diagrams/'+target.name,'width':width,'height':height,'renderer':renderer}
    # Keep only currently used public figures; the source cache retains build history.
    for path in PUBLIC.glob('*.svg'):
        if path.name not in used: path.unlink()


def figure(visual, identifier=''):
    asset = ASSETS[visual['asset']]
    url = asset['url']; title = escape(visual['title']); desc = escape(visual['description'], quote=True)
    width = round(asset['width']); height = round(asset['height'])
    attrs = f' id="visual-{escape(identifier,quote=True)}" data-visual-id="{escape(identifier,quote=True)}"' if identifier else ''
    # Preserve legible labels at narrow widths: the canvas scrolls, and the SVG opens at full size.
    minimum = min(width, 560)
    return (f'<figure class="lesson-visual"{attrs}>'
            f'<div class="visual-canvas" tabindex="0" role="group" aria-label="{title} diagram" style="--visual-min:{minimum}px;--visual-width:{width}px">'
            f'<img src="{url}" alt="{desc}" width="{width}" height="{height}" loading="lazy" decoding="async"></div>'
            f'<figcaption><strong>{title}</strong><p>{escape(visual["caption"])}</p>'
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Open full-size diagram: {title}">Open full-size diagram ↗</a></figcaption></figure>')


def lesson_visuals(slug, lesson, placement):
    return ''.join(figure(v, v['id']) for v in VISUALS.get((slug,lesson,placement), []))


def mermaid_figure(source):
    source = source.strip(); key = asset_key(source, 'mermaid')
    title, desc = mermaid_metadata(source)
    if key not in ASSETS: raise ValueError('Mermaid source was not prepared before page rendering')
    return figure({'asset':key,'title':title,'description':desc,'caption':desc})
