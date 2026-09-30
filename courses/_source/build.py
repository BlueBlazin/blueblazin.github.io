"""Build independent static courses and their directory for GitHub Pages."""
from pathlib import Path
from urllib.parse import quote,urlsplit
from html import escape as E
import json,re,shutil
from catalog import build_catalog
ROOT=Path(__file__).parent
OUTPUT=ROOT.parent
CATALOG=json.loads((ROOT/'catalog.json').read_text())
SLUGS=[entry['slug'] for entry in CATALOG['courses']]
assert len(SLUGS)==len(set(SLUGS)), 'Duplicate catalog course'
CONFIGS={s:json.loads((ROOT/s/'course-config.json').read_text()) for s in SLUGS}
assert len({cfg['track'] for cfg in CONFIGS.values()})==len(CONFIGS), 'Each course needs a unique progress track ID'
assert all(cfg['slug']==s and cfg['basePath']=='/courses/'+s for s,cfg in CONFIGS.items()), 'Course paths must match catalog slugs'
URLS={v['track']:v['url'] for v in CONFIGS.values()}

from formatting import inline, para, ul, markdown, prepare_math, strings
import hashlib
STYLE_VERSION=hashlib.sha256((ROOT/'style.css').read_bytes()).hexdigest()[:10]
math_sources=[]
for slug in SLUGS:
 for path in (ROOT/slug).glob('*'):
  if path.suffix=='.json' and path.name not in {'course-data.json','course-index.json'}:math_sources.extend(strings(json.loads(path.read_text())))
  elif path.suffix=='.md':math_sources.append(path.read_text())
prepare_math(math_sources)

def build(slug):
 folder=ROOT/slug;cfg=CONFIGS[slug];base=cfg['basePath'];track=cfg['track']
 lessons=json.loads((folder/'lessons-course.json').read_text());schedule=json.loads((folder/'schedule.json').read_text())
 original=json.loads((folder/'original-schedule.json').read_text());originalsteps=[s for w in original for d in w['days'] for s in d['steps']]
 plan=json.loads((folder/'reorganization.json').read_text());catalog=json.loads((folder/'resources.json').read_text());resources={r['id']:r for r in catalog}
 day0=plan['day0'];dispositions=plan['dispositions'];acts={a['id']:a for a in json.loads((folder/'activities.json').read_text())}
 def href(route):return base+route
 def anchor(key):return 'reference-'+re.sub(r'[^a-zA-Z0-9_-]','-',key)
 def cid(s,i):return f"a{s.get('source_activity',s['activity']) or 'flex'}-p{s['part']}-c{i}"
 def daytitle(day):return ' + '.join(s['title'] for s in day['steps'])
 def heading(title,desc='',kicker='COURSE GUIDE'):
  return '<div class="pagehead"><p class="eyebrow">'+E(kicker)+'</p><h1>'+E(title)+'</h1>'+para(desc)+'</div>'
 index=[];entries=[];stepurls={};hours=sum(w['hours'] for w in schedule)
 for w in schedule:
  for n,d in enumerate(w['days'],1):
   if not d['hours']:continue
   route=f"/week-{w['week']:02d}/day-{n:02d}/";entry={'id':f"{track.lower()}-week-{w['week']:02d}-day-{n:02d}",'week':w['week'],'day':d['day'],'dayNumber':n,'minutes':d['hours']*60,'url':href(route),'title':daytitle(d),'checks':[cid(s,i) for s in d['steps'] for i in range(1,len(lessons[s['key']]['checks'])+1)],'track':track}
   index.append(entry);entries.append((entry,w,d,route))
   for j,s in enumerate(d['steps'],1):stepurls[s['key']]=entry['url']+f'#hour-{j}'
 regular=index[:];day0entry={'id':track.lower()+'-day0','week':1,'day':'Day 0','minutes':0,'day0':True,'url':href('/week-01/day-00/'),'title':'Day 0 · Setup & course handbook','checks':[f'day0-{track.lower()}-{i}' for i in range(1,len(day0['readyChecks'])+1)],'track':track}
 index.insert(0,day0entry)
 known=list(dict.fromkeys([cid(s,i) for s in originalsteps for i in range(1,len(lessons[s['key']]['checks'])+1)]+[c for x in index for c in x['checks']]))
 for s in originalsteps:
  if s['key'] not in stepurls:stepurls[s['key']]=day0entry['url']+'#'+anchor(s['key'])
 def reading(refs):
  out=[]
  for r in refs:
   source=resources[r['id']];kind=source.get('kind','Reference');minutes=r.get('minutes',10)
   meta=('Optional alternative · ' if r.get('optional') else 'Core · ')+str(minutes)+' min · '+kind
   body='<div class="resource-meta">'+E(meta)+'</div><a href="'+E(source['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+E(source['title'])+'</a>'+para(r['focus'])
   if source.get('youtubeId'):
    assert re.fullmatch(r'[\w-]{11}',source['youtubeId'])
    body+='<details class="video-resource"><summary>Watch here</summary><div class="video-frame"><button type="button" class="button secondary" data-video="'+source['youtubeId']+'" data-video-title="'+E(source['title'],quote=True)+'">Load video</button></div><p class="small muted">Play only the assigned topic. The source link opens the original video if embedding is unavailable.</p></details>'
   out.append('<li>'+body+'</li>')
  return '<ul class="reading-list">'+''.join(out)+'</ul>'
 def progress_tools():
  return '<details class="progress-tools"><summary>Back up or move your progress</summary><p class="small">Checklists are saved in this browser. Export a backup before clearing browser data or changing devices. Import a backup to merge saved work.</p><button type="button" class="button secondary" id="export-progress">Export progress</button><label class="file-label">Import progress<input id="import-progress" type="file" accept="application/json,.json"></label><p id="progress-message" role="status" aria-live="polite" class="small"></p></details>'
 def checks(entry,groups,nexturl=None):
  out='<aside class="checklist" aria-label="Lesson checklist"><h2>Readiness checklist</h2>' if entry.get('day0') else '<aside class="checklist" aria-label="Lesson checklist"><h2>Lesson checklist</h2>'
  out+=f'<div class="progress-line"><span id="check-count">0 of {len(entry["checks"])} checked</span></div><progress id="lesson-progress" value="0" max="{len(entry["checks"])}" aria-label="Checklist progress"></progress>'
  for label,ids,texts in groups:
   if label:out+='<p class="checklist-label">'+E(label)+'</p>'
   out+=''.join('<label class="checkitem"><input type="checkbox" data-check="'+id+'" disabled><span>'+inline(text)+'</span></label>' for id,text in zip(ids,texts))
  out+='<p id="save-status" class="save-status" role="status" aria-live="polite">Loading this browser’s progress…</p><button id="retry-load" class="retry" hidden>Retry loading</button><button id="retry-save" class="retry" hidden>Retry saving</button><p id="lesson-complete" class="small" hidden>Checklist complete.</p>'
  if nexturl:out+='<a class="button" href="'+nexturl+'">'+('Begin Day 1' if entry.get('day0') else 'Next lesson')+'</a>'
  return out+'<p class="small">Mark verified work. Checkboxes record your assessment; they do not grade code.</p>'+progress_tools()+'</aside>'
 def shell(title,body,active='/',entry=None):
  nav=[('/','Course outline'),('/week-01/day-00/','Day 0 · Setup & handbook'),('/projects/','Project & assessment'),('/resources/','Reading library'),('/compute/','Compute & budget')]
  sidebar='<nav aria-label="Course navigation">'+''.join('<a class="navlink" href="'+href(url)+'"'+(' aria-current="page"' if url==active else '')+'>'+E(label)+'</a>' for url,label in nav)+'</nav>'
  if entry and not entry.get('day0'):
   sidebar+='<div class="divider"></div><p class="sidebar-label">Week '+str(entry['week'])+'</p>'
   for other in regular:
    if other['week']==entry['week']:sidebar+='<a class="mini-lesson" href="'+other['url']+'"'+(' aria-current="page"' if other['id']==entry['id'] else '')+'><strong>Day '+str(other['dayNumber'])+' · '+other['day']+' · '+str(other['minutes'])+' min</strong>'+E(other['title'])+'</a>'
  sidebar+='<div class="sidebar-foot"><p>Mon–Fri <strong>1 hour</strong><br>Saturday <strong>2 hours</strong><br>Sunday <strong>off</strong></p><a href="'+href('/syllabus.md')+'" download>Download handbook</a></div><div class="divider"></div><p class="sidebar-label">Other courses</p>'+''.join('<a class="navlink" href="'+v['url']+'">'+E(v['title'])+'</a>' for s,v in CONFIGS.items() if s!=slug)
  favicon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="5" fill="'+cfg['color']+'"/><text x="20" y="28" text-anchor="middle" fill="white" font-family="sans-serif" font-size="25">'+track+'</text></svg>'
  return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(title)+' · '+E(cfg['title'])+'</title><meta name="description" content="'+E(cfg['description'],quote=True)+'"><meta name="theme-color" content="'+cfg['color']+'"><link rel="icon" href="data:image/svg+xml,'+quote(favicon)+'"><link rel="stylesheet" href="'+href('/style.css')+'?v='+STYLE_VERSION+'">'+('<link rel="stylesheet" href="/courses/assets/katex/katex.min.css?v=0.18.9">' if 'data-math-source' in body else '')+'<script src="'+href('/course.js')+'" defer></script></head><body'+(' data-lesson="'+entry['id']+'"' if entry else '')+'><a class="skip" href="#main">Skip to content</a><header class="topbar"><a class="brand" href="'+href('/')+'"><span class="brandmark" aria-hidden="true">'+E(cfg['symbol'])+'</span><span>'+E(cfg['title'])+'<small>'+E(cfg['tagline'])+'</small></span></a><span class="topmeta">'+str(hours)+' hands-on hours · '+str(len(schedule))+' weeks</span><button id="menu-button" class="menu-button" aria-expanded="false" aria-controls="sidebar">Course menu</button></header><div class="layout"><aside class="sidebar" id="sidebar">'+sidebar+'</aside><main id="main">'+body+'<footer class="page-footer">'+E(cfg['title'])+' · Weekdays 1 hour · Saturdays 2 hours · Sundays off · <a href="https://github.com/BlueBlazin/blueblazin.github.io/tree/master/courses/_source/'+slug+'">Course source</a></footer></main></div></body></html>'
 pages={}
 def add(route,body,title,active='/',entry=None):pages[route]=shell(title,body,active,entry)
 first=regular[0]
 home='<div class="breadcrumb"><a href="/courses/">← All courses</a></div>'+heading(cfg['title'],cfg['description'],'INDEPENDENT PRACTICAL COURSE')
 home+='<div class="day-zero-callout"><div><strong>Week 1 · Day 0</strong><p>Set up once, check readiness, and keep the handbook nearby. Ready already? Begin Day 1 immediately.</p></div><a class="button secondary" href="'+day0entry['url']+'">Open Day 0</a></div>'
 home+='<section class="panel resume"><div><p class="eyebrow">NEXT HANDS-ON LESSON</p><h2 id="resume-title">'+E(first['title'])+'</h2><p class="muted small" id="resume-detail">Week 1 · Monday · 60 min</p><div class="progress-line"><span data-total-progress>Loading progress…</span></div><progress data-course-progress max="'+str(len(regular))+'" value="0" aria-label="Course progress"></progress><p id="save-status" class="save-status" role="status" aria-live="polite"></p><button id="retry-load" class="retry" hidden>Retry loading</button>'+progress_tools()+'</div><a class="button" href="'+first['url']+'" data-resume-link>Begin Day 1</a></section>'
 home+='<div class="course-stats"><span><strong>'+str(len(schedule))+'</strong> weeks</span><span><strong>'+str(hours)+'</strong> hands-on hours</span><span><strong>'+str(len(regular))+'</strong> lesson pages</span><span><strong>A$'+str(cfg['budget'])+'</strong> allowance</span></div><p class="help-note">Choose one course at a time, or divide the same seven-hour weekly budget across courses. Day 0 holds setup and reference material outside the hands-on calendar. Setup time varies; stop at your daily limit and shift the calendar when needed. Sundays stay free.</p><h2>Course outline</h2>'
 for w in schedule:
  xs=[x for x in regular if x['week']==w['week']];rows=[]
  for x in xs:rows.append('<a class="lesson-row" href="'+x['url']+'" data-lesson-row="'+x['id']+'"><span class="status-circle" role="img" aria-label="Not started"></span><span class="weekday">Day '+str(x['dayNumber'])+'<br>'+x['day']+'</span><span class="lesson-row-title">'+E(x['title'])+'</span><span class="lesson-time">'+str(x['minutes'])+' min</span></a>')
  modules=list(dict.fromkeys(s['module'] for d in w['days'] for s in d['steps']))
  title=' / '.join(cfg['modules'][str(m)] for m in modules)
  home+='<details class="week" id="week-'+str(w['week'])+'"'+(' open' if w['week']==1 else '')+'><summary><span class="weekno">Week '+str(w['week'])+'</span><span class="week-title">'+E(title)+'<small>'+str(len(xs))+' days · '+str(w['hours'])+' hours</small></span><span class="week-status" data-week-progress="'+str(w['week'])+'">'+str(len(xs))+' lessons</span></summary><div class="week-days">'+''.join(rows)+'<div class="week-rest">Sunday — no assigned work.</div></div></details>'
 add('/','<div class="content-width">'+home+'</div>','Course outline')
 # The opening handbook collects setup plus use-later reviews/admin without assigning them as learning days.
 body=heading('Day 0 · Setup & course handbook',day0['summary'],'WEEK 1 · DAY 0')
 main='<section class="lesson-section"><h2>Get ready, then start building</h2><p>This is a reference and readiness page, not a mandatory study day. Complete only the setup you need, then continue to Day 1 in the same session if time allows. Later review and portfolio instructions are filed below for when their prerequisites exist.</p>'+ul(cfg['prerequisites'])
 for section in day0['sections']:
  main+='<div class="subsection"><h3>'+E(section['title'])+'</h3>'+markdown(section['text'])
  refs=[{'id':id,'focus':resources[id].get('focus','Use this reference only for the setup step above.'),'minutes':5,'optional':True} for id in section.get('resources',[]) if id in resources]
  if refs:main+=reading(refs)
  links=[k for k in section.get('sourceKeys',[]) if dispositions.get(k,{}).get('placement')!='scheduled']
  if links:main+='<p class="reference-links">'+ ' · '.join('<a href="#'+anchor(k)+'">'+E(next(s['title'] for s in originalsteps if s['key']==k))+'</a>' for k in links)+'</p>'
  main+='</div>'
 if track=='K':main+='<p><a class="button secondary" href="'+href('/downloads/decoder.py')+'" download>Download decoder fixture</a></p>'
 main+='</section><section class="lesson-section"><h2>Setup, reviews & course administration</h2><p>Expand what you need. Items marked “Use later” are reference checkpoints after the relevant practical work, not prerequisites for Day 1.</p>'
 for s in sorted(originalsteps,key=lambda s:0 if dispositions[s['key']]['placement']=='day0' else 1):
  key=s['key'];placement=dispositions[key]['placement']
  if placement=='scheduled':continue
  c=lessons[key];when='Before Day 1 / when setup is needed' if placement=='day0' else 'Use later · after the relevant labs'
  main+='<details class="reference-note" id="'+anchor(key)+'"><summary>'+E(s['title'])+'<small>'+E(when)+'</small></summary>'+para(dispositions[key]['reason'])+para(c['explanation'])+ul(c['before'])+'<ol>'+''.join('<li><strong>'+E(x['title'])+'</strong>'+para(x['text'])+'</li>' for x in c['plan'])+'</ol><h3>Reference checklist</h3>'+ul(c['checks'])
  if plan['lessonResources'].get(key):main+=reading(plan['lessonResources'][key])
  main+='<details class="selfcheck"><summary>Self-check</summary>'+para(c['selfCheck']['question'])+para(c['selfCheck']['answer'])+'</details></details>'
 main+='</section>'
 body+='<div class="lesson-layout"><div class="lesson-main">'+main+'</div>'+checks(day0entry,[('',day0entry['checks'],day0['readyChecks'])],first['url'])+'</div>'
 add('/week-01/day-00/',body,'Day 0 · Setup & handbook','/week-01/day-00/',day0entry)
 for n,(entry,w,d,route) in enumerate(entries):
  body='<div class="breadcrumb"><a href="'+href('/')+'">Course</a><span>/</span><a href="'+href('/#week-'+str(w['week']))+'">Week '+str(w['week'])+'</a><span>/</span>Day '+str(entry['dayNumber'])+'</div>'+heading(entry['title'],'','WEEK '+str(w['week'])+' · DAY '+str(entry['dayNumber'])+' · '+d['day'].upper())+'<div class="meta-line"><span>'+str(entry['minutes'])+' minutes</span><span>Lesson '+str(n+1)+' of '+str(len(regular))+'</span></div>'
  blocks=[];groups=[]
  for b,s in enumerate(d['steps'],1):
   c=lessons[s['key']];refs=plan['lessonResources'][s['key']]
   assert refs and any(not r.get('optional') for r in refs),s['key']
   assert sum(x['minutes'] for x in c['plan'])==60,s['key']
   section='<section class="lesson-section" id="hour-'+str(b)+'"><p class="step-meta">Hour '+str(b)+' of '+str(d['hours'])+' · 60 minutes</p><h2>'+E(s['title'])+'</h2><div class="objectives"><h3>By the end of this hour</h3>'+ul(c['objectives'])+'</div><div class="before"><h3>Before you begin</h3>'+ul(c['before'])+'<p class="small">Environment or workflow question? <a href="'+day0entry['url']+'">Day 0 handbook</a>.</p></div><div class="subsection"><h3>The key idea</h3>'+para(c['explanation'])+'</div><div class="subsection"><h3>Resources for this hour</h3><p class="reading-description">Read the indicated section, not the entire source. The core reading fits inside the plan below. A video is an alternative to reading, not extra homework.</p>'+reading(refs)+'</div><div class="subsection"><h3>Your 60-minute plan</h3><ol class="plan">'
   section+=''.join('<li><div class="plan-head"><h4>'+E(x['title'])+'</h4><span class="time">'+str(x['minutes'])+' min</span></div>'+para(x['text'])+'</li>' for x in c['plan'])+'</ol></div><div class="evidence"><strong>What to save</strong>'+para(s['evidence'])+'</div><p class="pitfall"><strong>Watch for:</strong> '+inline(c['pitfall'])+'</p><div class="subsection"><h3>Check your understanding</h3>'+para(c['selfCheck']['question'])+'<details class="selfcheck"><summary>Check your reasoning</summary>'+para(c['selfCheck']['answer'])+'</details></div><p class="small">'+('Activity '+str(s['activity'])+' · step '+str(s['part'])+'. ' if s['activity'] else '')+'<a href="'+href('/projects/')+'">Project standards</a></p></section>'
   blocks.append(section);groups.append(('Hour '+str(b) if d['hours']>1 else '',[cid(s,i) for i in range(1,len(c['checks'])+1)],c['checks']))
  prev=regular[n-1] if n else day0entry;nxt=regular[n+1] if n+1<len(regular) else None
  nav='<nav class="pagination" aria-label="Lesson navigation"><a href="'+prev['url']+'"><small>Previous</small>'+E(prev['title'])+'</a>'+(('<a href="'+nxt['url']+'"><small>Next</small>'+E(nxt['title'])+'</a>') if nxt else '<a href="'+day0entry['url']+'"><small>Practical work complete</small>Portfolio & assessment checklist</a>')+'</nav>'
  body+='<div class="lesson-layout"><div class="lesson-main">'+''.join(blocks)+nav+'</div>'+checks(entry,groups,nxt['url'] if nxt else None)+'</div>'
  add(route,body,entry['title'],entry=entry)
 project=cfg['project'];body=heading(project['title'],project['description'],'PROJECT & ASSESSMENT')+'<section class="panel prose"><h2>Portfolio requirements</h2>'+ul(project['requirements'])+'</section><section class="panel prose">'+markdown(cfg['standards'])+'</section><section class="panel prose">'+markdown(cfg['assessment'])+'<p>Review rubrics and portfolio administration are collected in <a href="'+day0entry['url']+'">Day 0</a>. Apply them when the relevant work exists; they do not occupy separate days in the learning calendar.</p></section>'
 add('/projects/',body,'Project & assessment','/projects/')
 body=heading('Compute & budget','A$'+str(cfg['budget'])+' within A$1,000 across all three courses.')+'<section class="panel prose">'+para(cfg['compute'])+'<p>Allowances: architectures A$300, kernels A$450, harnesses A$250. Check current provider prices, currency conversion, taxes and storage charges before paying. Start from a local smoke test, set a job cap and stop idle resources.</p><p>Setup and spending checklists are in <a href="'+day0entry['url']+'">Day 0</a>. Rent hardware only when the scheduled experiment needs it.</p></section>'
 add('/compute/',body,'Compute & budget','/compute/')
 body=heading('Reading library','Vetted resources, with lesson-specific sections and timeboxes on each day page.','REFERENCE MATERIAL')
 for r in catalog:
  body+='<article class="panel resource-row" id="resource-'+E(r['id'])+'"><span class="resource-id">'+E(r['id'])+'</span><div><h2><a href="'+E(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+E(r['title'])+'</a></h2>'+para(r.get('focus',r.get('description','')))+'<p class="small muted">'+E(r.get('kind','Reference'))+' · Checked '+E(r.get('verifiedDate','2026-09-29'))+'</p></div></article>'
 extended=(folder/'reading-catalog.md').read_text()
 extended_html=markdown(extended)
 for code in re.findall(r'^- \*\*([AKHPC]\d+) —',extended,re.M):
  if code in resources:continue
  extended_html=extended_html.replace('<strong>'+code+' —','<strong id="resource-'+code+'">'+code+' —')
 body+='<section class="panel prose"><h2>Extended paper & project catalog</h2>'+extended_html+'</section>'
 add('/resources/',body,'Reading library','/resources/')
 # Portable aliases keep module references meaningful after administrative steps leave the calendar.
 for aid,a in acts.items():
  xs=[s for s in originalsteps if s['activity']==aid]
  content=heading(a['title'],a['work'],'ACTIVITY REFERENCE')+'<section class="panel prose">'+para(a['evidence'])+'<ul>'+''.join('<li><a href="'+stepurls[s['key']]+'">'+E(s['title'])+'</a></li>' for s in xs)+'</ul></section>'
  add('/labs/'+str(aid)+'/',content,a['title'],'/projects/')
 add('/404.html',heading('Page not found','Choose a lesson from the course outline.')+'<a class="button" href="'+href('/')+'">Course outline</a>','Page not found')
 # References mentioned in lesson prose retain working catalog anchors, including composite legacy IDs.
 for route,text in pages.items():
  text=re.sub(r'\b([AKHPC]\d+)\b',lambda m:m[0],text)
  pages[route]=text
 out=OUTPUT/slug
 if out.exists():shutil.rmtree(out)
 out.mkdir()
 for route,text in pages.items():
  dest=out/route.lstrip('/') if route.endswith('.html') else out/route.lstrip('/')/'index.html'
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
 client_cfg={'track':track,'title':cfg['title'],'basePath':base,'courseUrls':URLS,'knownCheckIds':known}
 (out/'course.js').write_text('const COURSE_INDEX='+json.dumps(index,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\nconst COURSE_CONFIG='+json.dumps(client_cfg,ensure_ascii=False,separators=(',',':'))+';\n'+(ROOT/'course.js').read_text())
 (out/'style.css').write_text((ROOT/'style.css').read_text()+f"\n:root{{--blue:{cfg['color']};--blue-light:{cfg['pale']}}}\n")
 if (folder/'downloads').exists():shutil.copytree(folder/'downloads',out/'downloads')
 handbook=f"# {cfg['title']}\n\n{hours} scheduled hands-on hours over {len(schedule)} weeks. Day 0 contains setup, review and administration outside the regular calendar. Weekdays: 1 hour. Saturday: up to 2 hours. Sunday: off.\n\n## Day 0\n\n{day0['summary']}\n\n"+'\n'.join('- '+x for x in day0['readyChecks'])+'\n\n'
 for section in day0['sections']:handbook+='### '+section['title']+'\n\n'+section['text']+'\n\n'
 handbook+='## Study calendar\n\n'
 for w in schedule:
  handbook+='### Week '+str(w['week'])+'\n\n'
  for d in w['days']:
   if d['hours']:handbook+='- '+d['day']+' ('+str(d['hours'])+'h): '+daytitle(d)+'\n'
  handbook+='- Sunday: off.\n\n'
 handbook+='## Project standards\n\n'+cfg['standards']+'\n\n## Assessment\n\n'+cfg['assessment']+'\n\n## Extended reading catalog\n\n'+(folder/'reading-catalog.md').read_text()
 (out/'syllabus.md').write_text(handbook)
 (folder/'course-index.json').write_text(json.dumps(index,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'course':slug,'hours':hours,'weeks':len(schedule),'lesson_pages':len(regular),'resources':len(catalog),'html_pages':len(pages)}))

for slug in SLUGS:build(slug)
build_catalog(ROOT,OUTPUT,CONFIGS,CATALOG)
