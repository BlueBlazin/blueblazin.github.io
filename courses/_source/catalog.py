"""Render the course directory from the catalog and each course's live schedule."""
from html import escape
import json


ICONS = {
    'layers': '<path d="m6 11 14-7 14 7-14 7-14-7Zm0 9 14 7 14-7M6 29l14 7 14-7"/>',
    'chip': '<rect x="10" y="10" width="20" height="20" rx="3"/><rect x="16" y="16" width="8" height="8" rx="1"/><path d="M15 4v6m10-6v6M15 30v6m10-6v6M4 15h6m-6 10h6m20-10h6m-6 10h6"/>',
    'nodes': '<path d="m10 12 15-3m-15 7 9 12m9-15-4 14"/><circle cx="8" cy="12" r="5"/><circle cx="30" cy="8" r="5"/><circle cx="22" cy="32" r="5"/>',
}


def build_catalog(root, output, configs, catalog):
    e = escape
    cards = []
    for number, entry in enumerate(catalog['courses'], 1):
        slug = entry['slug']
        cfg = configs[slug]
        schedule = json.loads((root / slug / 'schedule.json').read_text())
        hours = sum(week['hours'] for week in schedule)
        base = cfg['basePath']
        icon = ICONS.get(entry.get('icon'), ICONS['layers'])
        topics = ''.join(f'<li>{e(topic)}</li>' for topic in entry['topics'])
        cards.append(f'''<article class="course-card" style="--accent:{e(cfg['color'])};--tint:{e(cfg['pale'])}" aria-labelledby="title-{slug}">
  <div class="card-top"><span class="course-icon"><svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon}</svg></span><span class="course-number">COURSE {number:02d}</span></div>
  <p class="card-focus">{e(entry['focus'])}</p>
  <h3 id="title-{slug}"><a href="{base}/">{e(cfg['title'])}</a></h3>
  <p class="card-description">{e(cfg['description'])}</p>
  <ul class="topics" aria-label="Topics">{topics}</ul>
  <dl class="course-meta"><div><dt>Hands-on work</dt><dd>{hours} hours</dd></div><div><dt>At 7 hours / week</dt><dd>{len(schedule)} weeks</dd></div></dl>
  <div class="outcome"><h4>What you’ll build</h4><p>{e(entry['outcome'])}</p></div>
  <div class="card-actions"><a class="course-link" href="{base}/">Explore course <span aria-hidden="true">↗</span><span class="sr-only">: {e(cfg['title'])}</span></a><a class="setup-link" href="{base}/week-01/day-00/">Day 0 setup<span class="sr-only">: {e(cfg['title'])}</span></a></div>
</article>''')
    count = len(cards)
    output.joinpath('index.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(catalog['title'])} · BlueBlazin</title>
  <meta name="description" content="{e(catalog['description'], quote=True)}">
  <meta name="theme-color" content="#182b32">
  <link rel="canonical" href="https://blueblazin.github.io/courses/">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='9' fill='%23182b32'/%3E%3Cpath d='m15 12-8 8 8 8m10-16 8 8-8 8' fill='none' stroke='%23dcf3ac' stroke-width='3'/%3E%3C/svg%3E">
  <link rel="stylesheet" href="/courses/catalog.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header wrap">
  <a class="brand" href="/courses/" aria-current="page"><span class="brand-symbol" aria-hidden="true">&lt;/&gt;</span><span>BlueBlazin<span class="brand-subtitle">Course library</span></span></a>
  <nav aria-label="Main navigation"><a href="#courses">Courses</a><a href="#how-to-study">How to study</a><a class="github-link" href="https://github.com/BlueBlazin/blueblazin.github.io/tree/master/courses/_source">View source <span aria-hidden="true">↗</span></a></nav>
</header>
<main id="main">
  <section class="hero wrap" aria-labelledby="hero-title">
    <div class="hero-copy"><p class="eyebrow"><span class="status-dot" aria-hidden="true"></span>Open self-study · Practical AI</p>
      <h1 id="hero-title">Learn by building.<br><span>Understand by doing.</span></h1>
      <p class="hero-description">{e(catalog['description'])}</p>
      <a class="primary-link" href="#courses">Find your next course <span aria-hidden="true">↓</span></a>
      <p class="hero-note">Free course material · Independent tracks · Project-driven</p>
    </div>
    <aside class="rhythm" aria-labelledby="rhythm-title"><div class="rhythm-heading"><span class="small-label">A sustainable study rhythm</span><span class="rhythm-mark" aria-hidden="true">↗</span></div>
      <h2 id="rhythm-title">Small sessions.<br>Serious practice.</h2>
      <p>Make steady progress alongside a full-time job.</p>
      <div class="week-rhythm" role="list" aria-label="Weekly study schedule">
        <div role="listitem"><span>Mon</span><strong>1h</strong></div><div role="listitem"><span>Tue</span><strong>1h</strong></div><div role="listitem"><span>Wed</span><strong>1h</strong></div><div role="listitem"><span>Thu</span><strong>1h</strong></div><div role="listitem"><span>Fri</span><strong>1h</strong></div><div class="saturday" role="listitem"><span>Sat</span><strong>2h</strong></div><div class="sunday" role="listitem"><span>Sun</span><strong>Off</strong></div>
      </div>
      <p class="rhythm-foot">One clear plan for each day.<br>A working artifact at the end of each course.</p>
    </aside>
  </section>
  <section class="catalog-section wrap" id="courses" aria-labelledby="courses-title">
    <div class="section-heading"><div><p class="eyebrow">The course collection</p><h2 id="courses-title">Choose what to build next.</h2></div><span class="course-count">{count} courses · Self-paced</span></div>
    <p class="section-intro">Each course stands on its own. Choose the subject you want to understand more deeply.</p>
    <div class="course-grid">{''.join(cards)}</div>
    <p class="schedule-note">Durations cover scheduled hands-on work at seven hours per week. Setup, reviews, and portfolio preparation may extend the calendar. If you study multiple courses, share the same weekly time budget across them.</p>
  </section>
  <section class="study-section wrap" id="how-to-study" aria-labelledby="study-title">
    <div class="study-intro"><p class="eyebrow">Designed for deliberate practice</p><h2 id="study-title">A course you can<br>keep showing up for.</h2><p>For programmers with some prior ML experience who want to rebuild their foundations through implementation.</p><p>Start with a local machine. Each course explains when cloud GPUs or model APIs become useful and how to bound their cost.</p></div>
    <ol class="study-steps">
      <li><span class="step-number" aria-hidden="true">01</span><div><h3>Set up once in Day 0</h3><p>Check readiness and prepare your environment. Already ready? Begin Day 1 immediately.</p></div></li>
      <li><span class="step-number" aria-hidden="true">02</span><div><h3>Open today’s lesson and build</h3><p>Follow a focused plan with selected readings, implementation work, and a checklist. Save evidence of what works.</p></div></li>
      <li><span class="step-number" aria-hidden="true">03</span><div><h3>Turn experiments into a portfolio</h3><p>Keep your code, measurements, and explanations together. Finish with something another person can run and inspect.</p></div></li>
    </ol>
  </section>
</main>
<footer class="site-footer wrap"><p><strong>Built for curious practitioners.</strong><br>A growing collection of hands-on courses.</p><p><a href="https://github.com/BlueBlazin/blueblazin.github.io/tree/master/courses/_source">Browse the curriculum on GitHub <span aria-hidden="true">↗</span></a><span class="footer-note">Course checklists save in your browser. Export a backup to move devices.</span></p></footer>
</body>
</html>
''')
    output.joinpath('catalog.css').write_text(root.joinpath('catalog.css').read_text())
    print(json.dumps({'catalog': '/courses/', 'courses': count}))
