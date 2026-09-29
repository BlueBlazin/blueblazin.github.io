"""Validate static routes, resource coverage, checklists, calendar limits and public scope."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from html.parser import HTMLParser
import json,re
ROOT=Path(__file__).parent;WEB=ROOT.parent;REPO=WEB.parent
class Doc(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.checks=[];self.stack=[];self.errors=[];self.videos=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append('duplicate id '+a['id'])
   self.ids.add(a['id'])
  if tag in {'a','script','link','iframe'}:
   url=a.get('href') or a.get('src')
   if url:self.links.append(url)
  if tag=='input' and 'data-check' in a:self.checks.append(a['data-check'])
  if 'data-video' in a:self.videos.append(a['data-video'])
  if tag not in {'meta','link','input','br','hr','img','source','wbr','area','base','col','embed','param','track'}:self.stack.append(tag)
 def handle_endtag(self,tag):
  if not self.stack or self.stack[-1]!=tag:self.errors.append(('unbalanced',tag,self.stack[-4:]));return
  self.stack.pop()
docs={};pages={};totalhours=0;resources=set();videoids=set();nlessons=0
for folder in WEB.iterdir():
 if not folder.is_dir() or folder.name.startswith('_'):continue
 for file in folder.rglob('*'):
  if not file.is_file():continue
  url='/'+file.relative_to(REPO).as_posix();pages[url]=file
  if file.name=='index.html':pages[url.removesuffix('index.html')]=file
  if file.suffix=='.html':
   d=Doc();d.feed(file.read_text());assert not d.errors,(file,d.errors[:5]);assert not d.stack,(file,d.stack);docs[file]=d
 for d in docs.values():videoids.update(d.videos)
 source=ROOT/folder.name;index=json.loads((source/'course-index.json').read_text());schedule=json.loads((source/'schedule.json').read_text());lessons=json.loads((source/'lessons-course.json').read_text());plan=json.loads((source/'reorganization.json').read_text());catalog=json.loads((source/'resources.json').read_text());catalogids={r['id'] for r in catalog}
 assert len(catalogids)==len(catalog)
 for r in catalog:
  assert r['url'].startswith('https://') and r.get('verifiedDate') and r.get('provenanceUrl'),r
  resources.add(r['url'])
  if r.get('youtubeId'):assert re.fullmatch(r'[\w-]{11}',r['youtubeId'])
 for x in index:
  file=REPO/x['url'].lstrip('/')/'index.html';assert file in docs,x
  assert docs[file].checks==x['checks'],x['id']
 assert len({c for x in index for c in x['checks']})==sum(len(x['checks']) for x in index)
 assert sum(x.get('day0',False) for x in index)==1
 for w in schedule:
  assert w['hours']==sum(d['hours'] for d in w['days'])
  assert 0<w['hours']<=7
  for d in w['days']:
   limit=0 if d['day']=='Sunday' else 2 if d['day']=='Saturday' else 1
   assert d['hours']==len(d['steps']) and d['hours']<=limit
   for s in d['steps']:
    k=s['key'];assert plan['dispositions'][k]['placement']=='scheduled'
    assert sum(x['minutes'] for x in lessons[k]['plan'])==60,k
    refs=plan['lessonResources'][k];assert refs and all(r['id'] in catalogids for r in refs)
    assert 0<sum(r['minutes'] for r in refs if not r.get('optional'))<=10,k
    assert all(0<r['minutes']<=10 for r in refs),k
  totalhours+=w['hours']
 nlessons+=len(index)-1
 assert not list(folder.rglob('*.sql')) and not list(folder.rglob('hosting.json'))
 assert '/api/progress' not in (folder/'course.js').read_text()
 assert 'chatgpt.site' not in (folder/'course.js').read_text()
errors=[];links=0
for file,doc in docs.items():
 for link in doc.links:
  u=urlsplit(link)
  if u.scheme in {'mailto','data'}:continue
  if u.netloc and u.netloc!='blueblazin.github.io':continue
  if u.scheme and u.scheme not in {'http','https'}:continue
  if u.path.startswith('/'):
   target=pages.get(u.path)
  elif not u.path:target=file
  else:target=(file.parent/u.path).resolve()
  if not target or not target.exists():errors.append((file.relative_to(REPO).as_posix(),link,'missing route'));continue
  if u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:errors.append((str(file),link,'missing anchor'))
  links+=1
assert not errors,errors[:30]
assert all(p.parts[0]=='courses' for p in (f.relative_to(REPO) for f in pages.values()))
print(f'PASS: {len(docs)} HTML pages; {links} local/cross-course links; {nlessons} hands-on days; {totalhours} one-hour lessons; {len(resources)} distinct focused sources; {len(videoids)} embedded video choices; daily budgets and browser-only progress.')
