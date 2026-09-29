"""Render the minimal course directory."""
from html import escape
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
    <img src="/courses/covers/{e(entry['cover'])}" alt="" width="768" height="512">
    <h2 id="title-{slug}">{e(cfg['title'])}</h2>
    <p class="description">{e(entry['description'])}</p>
    <p class="duration">{hours} hands-on hours</p>
  </a>
</li>''')
    output.joinpath('index.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(catalog['title'])} · BlueBlazin</title>
  <meta name="description" content="{e(catalog['description'], quote=True)}">
  <link rel="canonical" href="https://blueblazin.github.io/courses/">
  <link rel="stylesheet" href="/courses/catalog.css">
</head>
<body>
  <main>
    <h1>{e(catalog['title'])}</h1>
    <ul class="courses" aria-label="Courses">{''.join(cards)}</ul>
  </main>
  <footer><a href="https://github.com/BlueBlazin/blueblazin.github.io/tree/master/courses/_source">Source on GitHub</a></footer>
</body>
</html>
''')
    output.joinpath('catalog.css').write_text(root.joinpath('catalog.css').read_text())
    print(json.dumps({'catalog': '/courses/', 'courses': len(cards)}))
