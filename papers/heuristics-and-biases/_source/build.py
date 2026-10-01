#!/usr/bin/env python3
"""Build the standalone reading edition from the checked transcription. No dependencies."""
from pathlib import Path
import html,json,math,re
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/'paper.json').read_text())
esc=html.escape

def fig(number,title,lead,body,caption):
 return f'''<figure class="visual" id="visual-{number}" aria-labelledby="visual-title-{number}"><span class="fig-label">Figure {number} · Added explanation</span><h4 id="visual-title-{number}">{title}</h4><p class="lead">{lead}</p>{body}<figcaption>{caption}</figcaption></figure>'''

def svg(label,body,height=280):
 return f'<div class="chart"><svg viewBox="0 0 640 {height}" role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>{body}</svg></div>'

def text(x,y,t,extra=''):
 return f'<text x="{x}" y="{y}" font-size="15" {extra}>{esc(str(t))}</text>'

# 01 — Data explicitly reported by the original paper.
rows=[]
for engineers in (70,30):
 dots=''.join(f'<i class="{"filled" if j<engineers/5 else ""}"></i>' for j in range(20))
 rows.append(f'''<tr><td>{engineers} engineers<br>{100-engineers} lawyers<div class="dot-population" aria-hidden="true">{dots}</div></td><td><span class="number">{engineers}%</span></td><td><span class="number biased">50%</span></td></tr>''')
base=fig(1,'A description can erase the base rate','Dick’s description gives no information that distinguishes an engineer from a lawyer.',
 '<table class="figure-table"><thead><tr><th scope="col">Group of 100</th><th scope="col">Probability with<br>no relevant evidence</th><th scope="col">Reported judgment<br>after the description</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table><div class="math-note">Uninformative evidence → the prior probability stays the same.</div>',
 'Reported values from the paper, pp. 1124–1125. The left probabilities follow the stated group composition; the right probabilities are the judgments reported for Dick. <span class="desktop-explanation">Dots summarize each group: one dot represents five people, and blue denotes engineers.</span>')

# 02 — Exact binomial calculation under the example's idealized assumptions.
tails=[]
for n in (15,45):
 cutoff=math.floor(.6*n)+1
 probability=sum(math.comb(n,k) for k in range(cutoff,n+1))/2**n
 tails.append((n,cutoff,probability))
body=''
for tick in (0,5,10,15,20,25):
 x=155+tick/25*408
 body+=f'<line x1="{x}" y1="26" x2="{x}" y2="199" class="rule"/>'+text(x,225,f'{tick}%', 'text-anchor="middle" class="muted" font-size="13"')
for i,(n,cutoff,p) in enumerate(tails):
 y=48+i*89
 body+=text(0,y+13,f'{n} births / day')+text(0,y+34,f'{cutoff}+ boys', 'class="muted" font-size="12"')
 body+=f'<rect x="155" y="{y}" width="{p/.25*408:.5f}" height="37" rx="3" fill="var(--accent)" opacity="{1 if i==0 else .6}"/>'
 body+=text(164+p/.25*408,y+25,f'{100*p:.1f}%', 'font-weight="650" class="green"')
body+=text(359,260,'Probability of a day with more than 60% boys', 'text-anchor="middle" class="muted" font-size="13"')
hospital=fig(2,'Smaller samples produce more extreme days','The same percentage threshold is easier to cross in the smaller hospital.',
 svg('Chance of more than 60% boys: 15.1% with 15 daily births, and 6.8% with 45 daily births.',body,275),
 'Calculated illustration, not additional study data. Assuming exactly 15 or 45 independent births per day, each with probability 0.5 of a boy, the binomial probabilities are 15.088% and 6.758%. “More than 60%” means at least 10 of 15, or 28 of 45. The paper says “about” these daily birth counts.')

# 03 — A fully specified theoretical model, not fabricated observations.
body=text(138,23,'Selected on test 1','text-anchor="middle" font-weight="600"')+text(464,23,'Expected on test 2','text-anchor="middle" font-weight="600"')
for score in (-2,-1,0,1,2):
 y=192-54*score
 body+=f'<line x1="83" y1="{y}" x2="555" y2="{y}" class="rule" stroke-dasharray="3 5"/>'+text(65,y+5,('+' if score>0 else '')+str(score),'text-anchor="end" class="muted" font-size="13"')
body+=text(600,198,'Mean','text-anchor="end" class="muted" font-size="12"')
for score,col in ((2,'var(--accent)'),(-2,'var(--warm)')):
 y1=192-54*score;y2=192-54*.5*score
 body+=f'<line x1="153" y1="{y1}" x2="442" y2="{y2}" stroke="{col}" stroke-width="3"/><path d="M 435 {y2-6} L 445 {y2} L 435 {y2+6}" fill="none" stroke="{col}" stroke-width="2"/><circle cx="138" cy="{y1}" r="9" fill="{col}"/><circle cx="463" cy="{y2}" r="9" fill="{col}"/>'
 body+=text(481,y2+5,('+1' if score>0 else '−1'),'font-weight="650"')
body+=text(319,342,'Scores in standard deviations from the mean','text-anchor="middle" class="muted" font-size="13"')
regression=fig(3,'An extreme first result need not repeat','Selecting a group for an unusually high or low first score also selects some temporary good or bad luck.',
 svg('In a jointly normal model with correlation 0.5, a first score of plus 2 predicts plus 1 on the second test, while minus 2 predicts minus 1.',body,355)+'<div class="math-note">In this example: E[Y | X = x] = 0.5x.</div>',
 'Illustrative model: two standardized, jointly normal test scores with correlation 0.5. The second-test values are conditional group expectations, not individual outcomes. No reward or punishment is applied. The figure illustrates regression; it does not establish that feedback has no effect.')

# 04 — Exact counts, alongside only the two estimates actually reported.
body=text(48,30,'Number of committees','class="muted" font-size="13"')
for tick in (0,50,100,150,200,250):
 y=280-tick*.8
 body+=f'<line x1="48" y1="{y}" x2="610" y2="{y}" class="rule"/>'+text(36,y+5,tick,'text-anchor="end" class="muted" font-size="12"')
for k in range(2,9):
 count=math.comb(10,k);x=72+(k-2)*78;y=280-.8*count
 body+=f'<rect x="{x}" y="{y}" width="44" height="{count*.8}" rx="3" fill="var(--accent)" opacity="{1 if k in (2,8) else .5}"/>'+text(x+22,270 if k==2 else y-10,count,'text-anchor="middle" font-size="13"'+(' style="fill:var(--paper)"' if k==2 else ''))+text(x+22,307,k,'text-anchor="middle" class="muted"')
 if k in (2,8):
  estimate=70 if k==2 else 20;ey=280-estimate*.8
  body+=f'<circle cx="{x+22}" cy="{ey}" r="6" fill="var(--warm)" stroke="var(--card)" stroke-width="2"/>'+text(x+41,ey+5,estimate,'class="warm" font-weight="650" font-size="12"')
body+=text(325,342,'Members per committee (k)','text-anchor="middle" class="muted" font-size="13"')
committees=fig(4,'Easy to imagine does not mean more numerous','Every two-person committee determines exactly one eight-person complement. Both counts must therefore be equal.',
 '<div class="figure-key"><span class="key-item"><i class="swatch"></i>Exact count</span><span class="key-item"><i class="swatch warm"></i>Reported median estimate</span></div>'+svg('The exact committee counts for sizes 2 through 8 are 45, 120, 210, 252, 210, 120, 45. Reported median estimates were 70 for size 2 and 20 for size 8.',body,355),
 'Exact counts are calculated as 10! / [k!(10 − k)!]. The two median estimates are reported in the paper, pp. 1127–1128. No estimates are supplied for the intermediate committee sizes.')

# 05 — Anchors and estimates share a number line; no invented ground truth.
body=''
for tick in (0,25,50,75,100):
 x=62+tick*5.2
 body+=f'<line x1="{x}" y1="20" x2="{x}" y2="200" class="rule"/>'+text(x,227,tick,'text-anchor="middle" class="muted" font-size="13"')
for y,a,estimate in ((70,10,25),(160,65,45)):
 xa=62+a*5.2;xe=62+estimate*5.2
 body+=f'<line x1="{xa}" y1="{y}" x2="{xe}" y2="{y}" class="accent-stroke" stroke-width="2"/><circle cx="{xa}" cy="{y}" r="7" fill="var(--card)" stroke="var(--muted)" stroke-width="2"/><circle cx="{xe}" cy="{y}" r="8" fill="var(--accent)"/>'
 body+=text(xa,y-23,str(a),'text-anchor="middle" class="muted"')+text(xe,y+31,str(estimate)+'%','text-anchor="middle" font-weight="650" class="green"')
anchor=fig(5,'An arbitrary number shifts the final estimate','The wheel’s number came first; the estimate of the percentage of African countries in the United Nations came afterward.',
 '<div class="figure-key"><span class="key-item"><i class="swatch hollow"></i>Wheel result</span><span class="key-item"><i class="swatch" style="border-radius:50%"></i>Median estimate</span></div>'+svg('Starting point 10 led to a median estimate of 25%; starting point 65 led to a median estimate of 45%.',body,240),
 'Reported group medians from the paper, p. 1128. Each starting number is paired with its group’s median estimate. These are not measurements of how individual participants adjusted their answers.')

# 06 — The paper's marble example, with a small mathematical exploration.
all_p=.9**7;any_p=1-all_p
compound=fig(6,'All of them, or at least one?','Combining likely events can make success less likely. Combining several small chances can make at least one success more likely.',
 f'''<table class="figure-table"><thead><tr><th scope="col">Event</th><th scope="col">Calculation</th><th scope="col">Probability</th></tr></thead><tbody>
<tr><td><span class="event-name" id="all-label">Red on all 7 draws</span><span class="event-detail">90% red marbles · replacement</span></td><td id="all-formula">0.9⁷</td><td><span class="event-result" id="all-value">{all_p*100:.2f}%</span><div class="prob-bar" aria-hidden="true"><span id="all-bar" style="width:{100*all_p}%"></span></div></td></tr>
<tr><td><span class="event-name">Red on one draw</span><span class="event-detail">50% red marbles</span></td><td>0.5</td><td><span class="event-result">50.00%</span><div class="prob-bar" aria-hidden="true"><span style="width:50%"></span></div></td></tr>
<tr><td><span class="event-name" id="any-label">Red at least once in 7 draws</span><span class="event-detail">10% red marbles · replacement</span></td><td id="any-formula">1 − 0.9⁷</td><td><span class="event-result" id="any-value">{any_p*100:.2f}%</span><div class="prob-bar" aria-hidden="true"><span id="any-bar" style="width:{100*any_p}%"></span></div></td></tr></tbody></table>
<div class="controls js-only"><label for="draws">Explore draws: <output id="draws-value" for="draws">7</output></label><input id="draws" type="range" min="1" max="20" value="7" step="1" aria-label="Number of draws"><button type="button" id="reset-draws">Reset to 7</button></div>
<p class="figure-note" id="compound-note" aria-live="polite">At seven draws, the ranking is: all seven &lt; one draw &lt; at least one.</p>''',
 'Exact calculations for independent draws with replacement. The paper rounds these probabilities to .48, .50, and .52 and reports choices favoring the less likely event in both comparisons. The slider explores the mathematics; the reported choices apply to seven draws.')

def mobile_table(headers,rows):
 return '<div class="mobile-chart-data"><table class="figure-table"><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def add_mobile(figure,table):
 return figure.replace('<figcaption>',table+'<figcaption>')
hospital=add_mobile(hospital,mobile_table(['Daily births','More than 60% boys','Probability'],[['15','10 or more','<strong>15.1%</strong>'],['45','28 or more','<strong>6.8%</strong>']]))
regression=add_mobile(regression,mobile_table(['Selected on test 1','Expected on test 2'],[['+2','<strong>+1</strong>'],['−2','<strong>−1</strong>']])+'<p class="mobile-chart-data figure-note">Scores in standard deviations from the mean. Both expected results are closer to zero.</p>')
committees=add_mobile(committees,mobile_table(['Members','Exact count','Reported estimate'],[[str(k),'<strong>'+str(math.comb(10,k))+'</strong>',str({2:70,8:20}[k]) if k in (2,8) else '—'] for k in range(2,9)]))
anchor=add_mobile(anchor,mobile_table(['Wheel result','Median estimate'],[['10','<strong>25%</strong>'],['65','<strong>45%</strong>']]))
FIGS={'worthless-evidence':base,'hospital-explanation':hospital,'reward-punishment':regression,'committee-counts':committees,'wheel':anchor,'planning':compound}

# Formatting changes are markup only: original words remain in their original order.
def format_text(s,citations=True):
 s=esc(s)
 s=s.replace('BINOM10K','<span class="binom" role="math" aria-label="10 choose k" data-canonical="BINOM10K"><span class="stack"><span>10</span><i>k</i></span></span>')
 s=re.sub(r'\bX(01|10|90|99|Π)\b',r'<i>X</i><sub>\1</sub>',s)
 # Link the original reference numbers without altering their visible text.
 if citations:
  def ref(m):
   nums=m.group(0)[1:-1].split(', ')
   return '('+', '.join(f'<a class="ref-link" href="#ref-{n}" aria-label="Reference {n}">{n}</a>' for n in nums)+')'
  s=re.sub(r'\(([1-9]|1[0-4])(?:, (?:[1-9]|1[0-4]))*\)',ref,s)
 return s
# All original textual records have one data-record marker. Added material has none.
parts=[];h2n=0;in_list=False;in_refs=False
for record in D['records']:
 kind=record['type'];rid=record['id'];source=record['text'];s=format_text(source,kind not in ['ref','equation'])
 if in_list and kind!='li':parts.append('</ul>');in_list=False
 if kind=='h2':
  h2n+=1
  if rid=='references':parts.append('<div class="references">');in_refs=True
  parts.append(f'<h2 id="{rid}"><span class="section-no" aria-hidden="true">{h2n:02d}</span><span data-record="{rid}">{s}</span></h2>')
 elif kind=='h3':parts.append(f'<h3 id="{rid}" data-record="{rid}">{s}</h3>')
 elif kind=='li':
  if not in_list:parts.append('<ul class="paper-list">');in_list=True
  parts.append(f'<li id="{rid}" data-record="{rid}">{s.removeprefix("- ")}</li>')
 elif kind=='quote':parts.append(f'<blockquote class="paper-quote" id="{rid}"><p data-record="{rid}">{s}</p></blockquote>')
 elif kind=='equation':parts.append(f'<p class="paper-equation" id="{rid}" data-record="{rid}">{s}</p>')
 elif kind=='ref':parts.append(f'<p class="reference" id="{rid}" data-record="{rid}">{s}</p>')
 else:parts.append(f'<p id="{rid}" data-record="{rid}">{s}</p>')
 if rid in FIGS:parts.append(FIGS[rid])
if in_refs:parts.append('</div>')
body='\n'.join(parts)
nav=[('intro','Opening'),('representativeness','Representativeness'),('prior-probability','Prior probability'),('sample-size','Sample size'),('chance','Chance'),('predictability','Predictability'),('validity','Validity'),('regression','Regression'),('availability','Availability'),('retrievability','Retrievability'),('search-set','Search sets'),('imaginability','Imaginability'),('illusory-correlation','Illusory correlation'),('anchoring','Adjustment and Anchoring'),('adjustment','Insufficient adjustment'),('compound-events','Compound events'),('subjective-distributions','Subjective distributions'),('discussion','Discussion'),('summary','Summary'),('references','References and Notes')]
main_ids={'intro','representativeness','availability','anchoring','discussion','summary','references'}
toc=''.join(f'<a href="#{i}"'+(' class="sub"' if i not in main_ids else '')+f'>{esc(t)}</a>' for i,t in nav)
mobile_toc=''.join(f'<a href="#{i}">{esc(t)}</a>' for i,t in nav if i in main_ids)
css=(HERE/'styles.css').read_text();js=(HERE/'reader.js').read_text()
result=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A single-column reading edition of Tversky and Kahneman’s 1974 paper, with the original text and clearly labeled visual explanations."><meta name="theme-color" content="#ffffff"><title>Judgment under Uncertainty — Tversky &amp; Kahneman</title><style>{css}</style></head>
<body><a class="skip" href="#paper">Skip to paper</a>
<header class="topbar"><a class="brand" href="/">BlueBlazin</a><nav><a href="{D['source']}">Original PDF</a><details class="reading-options js-only"><summary>Reading options</summary><div class="tools"><label class="tool-label"><input id="visuals" type="checkbox" checked> Show added figures</label><label class="tool-label" for="font-size">Text size <select id="font-size"><option value="normal">Default</option><option value="large">Large</option><option value="larger">Larger</option></select></label><button id="theme" type="button" aria-label="Switch to dark theme">Dark</button></div></details></nav></header>
<div class="toolbar" aria-hidden="true"><span id="read-percent" hidden></span><div id="progress" class="progress-line"></div></div>
<div class="layout"><aside class="sidebar" aria-label="Paper navigation"><div class="nav-title">Contents</div><nav class="toc">{toc}</nav></aside>
<main class="main"><header class="hero"><h1 data-meta="title">Judgment under Uncertainty:<br> Heuristics and Biases</h1><p class="subtitle" data-meta="subtitle">{D['subtitle']}</p></header>
<div class="article-meta"><div><span class="meta-label">Authors</span><p data-meta="authors">{D['authors']}</p></div><div><span class="meta-label">Published</span><p>27 September 1974<br>Science, 185 (4157), 1124–1131</p></div></div>
<p class="edition-note">Single-column reading edition. The original text is preserved; six added figures provide explanations and are labeled separately.</p>
<details class="mobile-toc"><summary>Contents</summary><nav aria-label="Mobile paper navigation">{mobile_toc}</nav></details>
<article id="paper" aria-label="Original paper with labeled added visual explanations">{body}<p class="affiliation" data-meta="affiliation">{D['affiliation']}</p><div id="paper-end"></div></article>
<details class="edition-details"><summary>About this reading edition</summary><p>The paper’s wording, sequence, mathematical expressions, and references are preserved. Column wrapping and line-end word breaks have been removed, and OCR errors corrected against the scanned pages. Original typographical oddities are retained. Running journal headers, the archive cover sheet, and the separate article beginning on the final scanned page are outside the reading text.</p><p>All six figures are additions to this edition. Their captions distinguish values reported in the paper from calculations and illustrative models. The paper remains readable without JavaScript, and this self-contained HTML can be saved and read offline.</p><p>Original publication: {D['journal']}. Published by the American Association for the Advancement of Science. <a href="{D['source']}">Source PDF</a> · <a href="https://www.jstor.org/stable/1738360">JSTOR record</a>.</p></details>
<footer class="page-footer"><span>Amos Tversky &amp; Daniel Kahneman · 1974</span><span><a href="index.html" download="heuristics-and-biases.html">Download HTML</a> · <a href="#paper">Back to the beginning ↑</a></span></footer></main></div><script>{js}</script></body></html>'''
(HERE.parent/'index.html').write_text(result)
print('Built',HERE.parent/'index.html',len(result.encode()),'bytes')
print('Binomial tail probabilities:',tails)
