"""Small safe Markdown renderer for course prose, code, and LaTeX math.

Raw HTML is escaped. Math is rendered at build time with pinned, local KaTeX.
Single-dollar delimiters deliberately exclude currency such as A$300 and $10.
"""
from html import escape as E
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).parent
MATH = {}
TOKEN = re.compile(
    r'(?P<code>`+)(?P<codebody>[^`]*?)(?P=code)'
    r'|\\\((?P<math>.+?)\\\)'
    r'|(?<![\w\\])\$(?![\s$\d])(?P<dollar>[^\n$]+?)(?<![\s\\])\$(?!\d)'
    r'|\[(?P<label>[^\]\n]+)\]\((?P<url>https?://[^\s)]+)\)',
    re.S,
)
DISPLAY = re.compile(r'(?m)^\s*(?:\$\$(?P<dollars>.*?)\$\$|\\\[(?P<brackets>.*?)\\\])\s*$',re.S)
FENCE = re.compile(r'^\s*(`{3,}|~{3,})([\w+-]*)\s*$')


def read_fence(lines, start):
    """Return a complete block using the same grammar in preflight and rendering."""
    fence = FENCE.match(lines[start].strip())
    if not fence: return None
    marker, language = fence.groups(); body=[]; end=start+1
    closing = re.compile(r'\s*'+re.escape(marker[0])+'{'+str(len(marker))+r',}\s*')
    while end < len(lines) and not closing.fullmatch(lines[end]):
        body.append(lines[end]); end += 1
    if end == len(lines): raise ValueError('Unclosed code fence')
    return {'start':start,'end':end+1,'language':language.lower(),'body':'\n'.join(body)}


def iter_code_blocks(text):
    lines=str(text).splitlines(); i=0
    while i<len(lines):
        block=read_fence(lines,i)
        if block:
            yield block
            i=block['end']
        else: i+=1


def strings(value):
    if isinstance(value, str): yield value
    elif isinstance(value, dict):
        for v in value.values(): yield from strings(v)
    elif isinstance(value, list):
        for v in value: yield from strings(v)


def prepare_math(values):
    wanted = set()
    for value in values:
        # Literal examples, including dollars and LaTeX inside code, stay literal.
        lines=value.splitlines()
        for block in iter_code_blocks(value):
            lines[block['start']:block['end']]=['']*(block['end']-block['start'])
        value='\n'.join(lines)
        for m in DISPLAY.finditer(value): wanted.add(((m['dollars'] or m['brackets']).strip(), True))
        value = DISPLAY.sub('', value)
        for m in TOKEN.finditer(value):
            if m['math'] or m['dollar']: wanted.add(((m['math'] or m['dollar']).strip(), False))
    if wanted:
        result = subprocess.run(['node',str(ROOT/'render-math.cjs')], input=json.dumps(sorted(wanted)), text=True, capture_output=True, check=True)
        MATH.update({(tex, display): html for tex, display, html in json.loads(result.stdout)})


def math(tex, display=False):
    key = (tex.strip(), display)
    if key not in MATH:
        result = subprocess.run(['node',str(ROOT/'render-math.cjs')], input=json.dumps([key]), text=True, capture_output=True, check=True)
        MATH[key] = json.loads(result.stdout)[0][2]
    tag = 'div' if display else 'span'
    cls = 'math-block' if display else 'math-inline'
    return f'<{tag} class="{cls}" data-math-source="{E(key[0],quote=True)}">{MATH[key]}</{tag}>'


def plain(text):
    return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',E(text))


def inline(text):
    out=[]; start=0
    for m in TOKEN.finditer(str(text)):
        out.append(plain(str(text)[start:m.start()]))
        if m['code']: out.append('<code>'+E(m['codebody'])+'</code>')
        elif m['math'] or m['dollar']: out.append(math(m['math'] or m['dollar']))
        else: out.append('<a href="'+E(m['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+inline(m['label'])+'</a>')
        start=m.end()
    out.append(plain(str(text)[start:]))
    return ''.join(out)


def ul(items):
    return '<ul>'+''.join('<li>'+inline(x)+'</li>' for x in items)+'</ul>'


def code_block(text, language=''):
    language=language.lower()
    labels={'py':'Python','python':'Python','bash':'Shell','sh':'Shell','shell':'Shell','json':'JSON','cpp':'C++','cuda':'CUDA','text':'Text','javascript':'JavaScript','js':'JavaScript'}
    label=labels.get(language,language or 'Code')
    return '<figure class="code-block"><figcaption>'+E(label)+'</figcaption><pre tabindex="0" aria-label="'+E(label,quote=True)+' code"><code class="language-'+E(language or 'text',quote=True)+'">'+E(text)+'</code></pre></figure>'


def table_cells(line):
    # Pipes inside inline code/math must not become table column boundaries.
    held=[]
    def keep(m): held.append(m[0]); return '\x00'+str(len(held)-1)+'\x00'
    line=TOKEN.sub(keep,line.strip().strip('|'))
    cells=re.split(r'(?<!\\)\|',line)
    return [re.sub(r'\x00(\d+)\x00',lambda m:held[int(m[1])],c.strip()).replace('\\|','|') for c in cells]


def markdown(text):
    lines=str(text).strip().splitlines();out=[];i=0
    def special(line):
        s=line.strip()
        return not s or FENCE.match(s) or s.startswith(('$$',r'\[','|','#','- ')) or re.match(r'^\d+[.)] ',s)
    while i<len(lines):
        line=lines[i].strip()
        if not line: i+=1;continue
        block=read_fence(lines,i)
        if block:
            if block['language']=='mermaid':
                from diagrams import mermaid_figure
                out.append(mermaid_figure(block['body']))
            else: out.append(code_block(block['body'],block['language']))
            i=block['end'];continue
        if line.startswith(('$$',r'\[')):
            opener='$$' if line.startswith('$$') else r'\[';closer='$$' if opener=='$$' else r'\]'
            body=line[len(opener):];i+=1
            while closer not in body and i<len(lines):body+='\n'+lines[i];i+=1
            if closer not in body:raise ValueError('Unclosed display math')
            tex,tail=body.split(closer,1)
            if tail.strip():raise ValueError('Display math must end on its own line')
            out.append(math(tex,True));continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=table_cells(lines[i])
                if not all(re.fullmatch(r':?-+:?',x) for x in row):rows.append(row)
                i+=1
            out.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+inline(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');continue
        if line.startswith('- ') or re.match(r'^\d+[.)] ',line):
            ordered=not line.startswith('- ');pattern=r'^\d+[.)] (.*)' if ordered else r'^- (.*)';items=[]
            while i<len(lines) and (m:=re.match(pattern,lines[i].strip())):items.append(m[1]);i+=1
            tag='ol' if ordered else 'ul'
            out.append('<'+tag+'>'+''.join('<li>'+inline(x)+'</li>' for x in items)+'</'+tag+'>');continue
        if line.startswith('#'):
            # Content sections live beneath the page's h1/h2 structure.
            level=min(6,max(3,len(line)-len(line.lstrip('#'))))
            out.append(f'<h{level}>'+inline(line.lstrip('# '))+f'</h{level}>');i+=1;continue
        block=[line];i+=1
        while i<len(lines) and not special(lines[i]):block.append(lines[i].strip());i+=1
        out.append('<p>'+inline(' '.join(block))+'</p>')
    return '\n'.join(out)


def para(text):
    return markdown(text)
