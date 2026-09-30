"""Regression checks for technical prose and every generated course page."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
from formatting import inline, markdown, prepare_math

ROOT = Path(__file__).parent
WEB = ROOT.parent

sample = r'''Text with `x < y` and \(x^2\).

\[
\begin{aligned}y &= x^2\\ z &= 2x\end{aligned}
\]

```python
if x < 2:
    print("$literal$", r"\(literal\)")
```

$$a+b$$

1. First
2. Second

| Operation | Value |
| --- | --- |
| `a | b` | \(\lvert x\rvert\) |
'''
prepare_math([sample])
html = markdown(sample)
assert html.count('class="math-block"') == 2
assert html.count('class="math-inline"') == 2
assert html.count('<math ') == 4 and 'katex-error' not in html
assert '<ol><li>First</li><li>Second</li></ol>' in html
assert '<code>a | b</code>' in html and html.count('<td>') == 2
assert 'if x &lt; 2:\n    print(&quot;$literal$&quot;, r&quot;\\(literal\\)&quot;)' in html
assert inline('A$300; $10; $20; `$x$`') == 'A$300; $10; $20; <code>$x$</code>'
assert 'math-inline' in inline('$x^2$')
assert inline('<script>alert(1)</script>') == '&lt;script&gt;alert(1)&lt;/script&gt;'
assert 'href="https://' in inline('[**Guide**](https://example.org/)')
for bad in ('```python\nx = 1', '\\[x^2'):
    try: markdown(bad)
    except ValueError: pass
    else: raise AssertionError('Malformed blocks must fail the build')

class Content(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.prose=[]; self.inline_code=0; self.blocks=0; self.math=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append(tag)
        if tag=='code': self.inline_code+=1
        if a.get('class')=='code-block': self.blocks+=1
        if 'data-math-source' in a: self.math+=1
    def handle_endtag(self,tag):
        if tag in self.stack:
            while self.stack.pop()!=tag: pass
    def handle_data(self,text):
        if not set(self.stack)&{'code','pre','math','script','style'}: self.prose.append(text)

counts={}
for slug in ('llm-architectures','gpu-kernels','agent-harnesses'):
    counts[slug]={'pages':0,'math':0,'code_blocks':0,'inline_code':0}
    for p in (WEB/slug).rglob('*.html'):
        source=p.read_text(); d=Content(); d.feed(source)
        assert not re.search(r'```|~~~|\\[\[\]() ]|\$\$', ''.join(d.prose)),p
        assert 'katex-error' not in source,p
        if d.math: assert '/courses/assets/katex/katex.min.css?v=0.18.9' in source,p
        counts[slug]['pages']+=1; counts[slug]['math']+=d.math
        counts[slug]['code_blocks']+=d.blocks; counts[slug]['inline_code']+=d.inline_code-d.blocks
    # Formatting must never invalidate previously saved progress.
    p=ROOT/slug/'course-index.json'
    previous=json.loads(subprocess.run(['git','show','HEAD:'+str(p.relative_to(WEB.parent))],capture_output=True,text=True,check=True).stdout)
    current=json.loads(p.read_text())
    assert [(d['id'],d['checks'],d['url']) for d in current]==[(d['id'],d['checks'],d['url']) for d in previous],slug
css=WEB/'assets/katex/katex.min.css'
for url in re.findall(r'url\(([^)]+)\)',css.read_text()):assert (css.parent/url.strip('"\'')).is_file(),url
print('PASS: math/code rendering, literal escaping, currency, lists/tables, all-page markup audit, local fonts, and stable saved-progress IDs.')
print(json.dumps(counts,indent=2))
