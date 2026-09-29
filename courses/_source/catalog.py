"""Render the course directory."""
from html import escape
import hashlib
import json


def build_catalog(root, output, configs, catalog):
    e = escape
    cards = []
    for entry in catalog['courses']:
        slug = entry['slug']
        cfg = configs[slug]
        schedule = json.loads((root / slug / 'schedule.json').read_text())
        hours = sum(week['hours'] for week in schedule)
        cover = output / 'covers' / entry['cover']
        assert cover.is_file(), f'Missing course cover: {cover}'
        cards.append(f'''<li>
  <a class="course" href="{e(cfg['basePath'])}/" aria-labelledby="title-{slug}">
    <img class="cover" src="/courses/covers/{e(entry['cover'])}" alt="" width="768" height="512">
    <div class="course-body">
      <h2 id="title-{slug}">{e(cfg['title'])}</h2>
      <p class="description">{e(entry['description'])}</p>
      <div class="course-footer"><span class="duration"><strong>{hours}</strong> hands-on hours</span><span class="course-action">View course <span aria-hidden="true">↗</span></span></div>
    </div>
  </a>
</li>''')
    css = root.joinpath('catalog.css').read_text()
    version = hashlib.sha256(css.encode()).hexdigest()[:10]
    output.joinpath('index.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(catalog['title'])} · BlueBlazin</title>
  <meta name="description" content="{e(catalog['description'], quote=True)}">
  <meta name="theme-color" content="#f5f6f8">
  <link rel="canonical" href="https://blueblazin.github.io/courses/">
  <link rel="stylesheet" href="/courses/catalog.css?v={version}">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><div class="header-inner">
    <a class="brand" href="/courses/" aria-label="BlueBlazin courses">BlueBlazin<span class="brand-dot" aria-hidden="true">.</span></a>
    <a class="source-link" href="https://github.com/BlueBlazin/blueblazin.github.io/tree/master/courses/_source">GitHub <span aria-hidden="true">↗</span></a>
  </div></header>
  <main id="main">
    <div class="page-heading"><h1>{e(catalog['title'])}</h1><p>Language models, GPU programming, and agents.</p></div>
    <ul class="courses" aria-label="Courses">{''.join(cards)}</ul>
    <footer class="study-note">1 hour on weekdays · 2 hours on Saturday · Sundays off</footer>
  </main>
</body>
</html>
''')
    output.joinpath('catalog.css').write_text(css)
    print(json.dumps({'catalog': '/courses/', 'courses': len(cards)}))
