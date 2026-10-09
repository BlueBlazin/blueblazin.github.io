/* Kernel — Forms of One Word: conspectus, key, plates, register, specimen sheet, finder. */
(() => {
const D = window.KZ, NS = 'http://www.w3.org/2000/svg';
const $ = s => document.querySelector(s);
const S = (tag, a = {}, p) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
const H = (tag, a = {}, p, html) => { const e = document.createElement(tag); for (const k in a) e.setAttribute(k, a[k]); if (html != null) e.innerHTML = html; if (p) p.appendChild(e); return e; };
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tex = s => { try { return katex.renderToString(s, { throwOnError: false }); } catch { return esc(s); } };
const byId = Object.fromEntries(D.entries.map(e => [e.id, e]));
const plate = Object.fromEntries(D.plates.map(p => [p.id, p]));
const INK = '#1d1a15', PAPER = '#ece2c7';
// the specimen that stands for each family in the key
const REP = { seed: 'nut', core: 'linux', routine: 'cuda', weighting: 'convolution', similarity: 'quantum', zero: 'nullspace', remnant: 'kernelization', odd: 'spice' };
const fillOf = pid => pid === 'zero' ? PAPER : plate[pid].color;
// bump when illustrations are regenerated, so browsers fetch the new files
const IMGV = 2;
const img = id => `img/sp/${id}.webp?v=${IMGV}`;
const label = e => e.alias || e.name;
// an engraving, falling back to the concept glyph if the file is missing
function figure(e, cls = '') {
  return `<img class="${cls}" src="${img(e.id)}" alt="" loading="lazy" onerror="this.outerHTML=window.KZ.glyphs['${e.visual}']">`;
}

/* ── tooltip ── */
const tip = $('#tip');
function showTip(ev, e) {
  tip.hidden = false;
  if (tip.dataset.id !== e.id) { tip.dataset.id = e.id; tip.innerHTML = `${figure(e)}<div class="t1">${plate[e.plate].roman} · ${e.no}</div><div class="t2">${esc(e.name)}</div>`; }
  const w = 220, h = tip.offsetHeight || 200;
  tip.style.left = Math.min(ev.clientX + 18, innerWidth - w - 12) + 'px';
  tip.style.top = (ev.clientY + h + 24 > innerHeight ? ev.clientY - h - 14 : ev.clientY + 18) + 'px';
}
const hideTip = () => { tip.hidden = true; };

/* ── conspectus: the whole genus as one seed head ── */
(function conspectus() {
  const svg = $('#seed'), C = 410, R0 = 66, R1 = 322;
  const counts = D.plates.map(p => D.entries.filter(e => e.plate === p.id).length);
  const w = counts.map(c => Math.max(c, 6)), W = w.reduce((a, b) => a + b, 0), GAP = .05;
  const span = 2 * Math.PI - GAP * D.plates.length;
  let a = -Math.PI / 2 - w[0] / W * span / 2;
  const pol = (r, t) => [C + r * Math.cos(t), C + r * Math.sin(t)];
  const lobes = D.plates.map((p, i) => { const s = w[i] / W * span, L = { p, a0: a, a1: a + s }; a += s + GAP; return L; });
  S('circle', { cx: C, cy: C, r: 352, class: 'rim', 'stroke-width': 1.6 }, svg);
  S('circle', { cx: C, cy: C, r: 345, class: 'rim', 'stroke-width': .6 }, svg);
  const lobeG = S('g', {}, svg), linkG = S('g', {}, svg), dotG = S('g', {}, svg);
  const pos = {};
  const rad = e => e.rank < 6 ? 25 : e.rank < 20 ? 19 : e.rank < 40 ? 16 : 13;
  lobes.forEach(L => {
    const { p, a0, a1 } = L, g = S('g', { class: 'lobe' }, lobeG); L.g = g;
    const r0 = R0 - 14, r1 = 338, [x0, y0] = pol(r0, a0), [x1, y1] = pol(r0, a1), [X0, Y0] = pol(r1, a0), [X1, Y1] = pol(r1, a1);
    const big = a1 - a0 > Math.PI ? 1 : 0;
    S('path', { class: 'lobe-bg', d: `M${x0} ${y0}L${X0} ${Y0}A${r1} ${r1} 0 ${big} 1 ${X1} ${Y1}L${x1} ${y1}A${r0} ${r0} 0 ${big} 0 ${x0} ${y0}Z`,
      fill: p.color, 'fill-opacity': .07, stroke: '#34302a', 'stroke-width': 1 }, g);
    const mid = (a0 + a1) / 2, [nx, ny] = pol(384, mid);
    const t = S('text', { x: nx, y: ny + 9, class: 'lobe-num' }, g); t.textContent = p.roman;
    t.addEventListener('click', () => document.getElementById('plate-' + p.id).scrollIntoView());
    const es = D.entries.filter(e => e.plate === p.id), n = es.length;
    es.forEach((e, k) => {
      const rr = R0 + 20 + (R1 - R0 - 20) * Math.sqrt((k + .6) / (n + .2)), fr = n === 1 ? .5 : ((k + 1) * .6180339887) % 1;
      pos[e.id] = { r: rr, t: a0 + .05 + fr * (a1 - a0 - .1), a0: a0 + .04, a1: a1 - .04 };
    });
  });
  // relax so seeds don't touch, keeping each inside its wedge
  const ids = Object.keys(pos);
  for (let it = 0; it < 90; it++) {
    const xy = ids.map(id => pol(pos[id].r, pos[id].t));
    for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) {
      const dx = xy[j][0] - xy[i][0], dy = xy[j][1] - xy[i][1], d = Math.hypot(dx, dy) || .01, m = rad(byId[ids[i]]) + rad(byId[ids[j]]) + 8;
      if (d < m) { const k = (m - d) / 2 / d; xy[i][0] -= dx * k; xy[i][1] -= dy * k; xy[j][0] += dx * k; xy[j][1] += dy * k; }
    }
    ids.forEach((id, i) => { const P = pos[id]; let t = Math.atan2(xy[i][1] - C, xy[i][0] - C);
      while (t < P.a0 - Math.PI) t += 2 * Math.PI; while (t > P.a0 + Math.PI) t -= 2 * Math.PI;
      P.r = Math.max(R0 + 6, Math.min(R1 + 8, Math.hypot(xy[i][0] - C, xy[i][1] - C))); P.t = Math.max(P.a0, Math.min(P.a1, t)); });
  }
  ids.forEach(id => { [pos[id].x, pos[id].y] = pol(pos[id].r, pos[id].t); });
  const lines = D.links.map(l => { const A = pos[l.a], B = pos[l.b]; if (!A || !B) return null;
    const mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2, k = byId[l.a].plate === byId[l.b].plate ? .2 : .75;
    return { l, el: S('path', { d: `M${A.x} ${A.y}Q${mx + (C - mx) * k} ${my + (C - my) * k} ${B.x} ${B.y}`, class: 'ln' + (l.kind === 'contrast' ? ' contrast' : '') }, linkG) }; }).filter(Boolean);
  S('circle', { cx: C, cy: C, r: 44, fill: '#15130f', stroke: '#4a443a', 'stroke-width': 1.2 }, svg);
  S('text', { x: C, y: C + 7, class: 'core-word' }, svg).textContent = 'cyrnel';
  const nodes = {};
  [...D.entries].sort((x, y) => pos[x.id].r - pos[y.id].r).forEach((e, k) => {
    const P = pos[e.id], g = S('g', { class: 'sd', tabindex: 0, role: 'button', 'aria-label': e.name, style: `animation-delay:${200 + k * 12}ms` }, dotG);
    // the illustrations carry their own margins, so the image box is drawn a little larger than the seed's footprint
    const r = rad(e) * 1.4, im = S('image', { x: P.x - r, y: P.y - r, width: 2 * r, height: 2 * r, preserveAspectRatio: 'xMidYMid meet' }, g);
    im.setAttribute('href', img(e.id));
    nodes[e.id] = g;
    g.addEventListener('pointerenter', ev => hot(e.id, ev));
    g.addEventListener('pointermove', ev => showTip(ev, e));
    g.addEventListener('pointerleave', () => hot(null));
    g.addEventListener('click', () => openSheet(e.id));
    g.addEventListener('keydown', ev => { if (ev.key === 'Enter') openSheet(e.id); });
  });
  function hot(id, ev) {
    svg.classList.toggle('dim', !!id);
    Object.values(nodes).forEach(n => n.classList.remove('hot', 'kin'));
    lines.forEach(({ l, el }) => { const on = id && (l.a === id || l.b === id); el.classList.toggle('hot', !!on); if (on) nodes[l.a === id ? l.b : l.a].classList.add('kin'); });
    if (id) { nodes[id].classList.add('hot'); if (ev) showTip(ev, byId[id]); } else hideTip();
  }
  lobes.forEach(L => {
    L.g.querySelector('.lobe-num').addEventListener('pointerenter', () => { svg.classList.add('focus'); L.g.classList.add('on'); });
    L.g.querySelector('.lobe-num').addEventListener('pointerleave', () => { svg.classList.remove('focus'); L.g.classList.remove('on'); });
  });
})();

/* ── clavis: a branching key in the manner of Darwin's single diagram ── */
(function clavis() {
  const svg = $('#tree');
  const leaves = ['core', 'routine', 'similarity', 'weighting', 'zero', 'remnant', 'seed', 'odd'];
  const T = { q: 'Is it code that runs?', c: [
    { e: 'yes', q: 'A central engine, or a routine?', c: [{ e: 'engine', p: 'core' }, { e: 'routine', p: 'routine' }] },
    { e: 'no', q: 'A function of two inputs?', c: [
      { e: 'yes', q: 'Does it measure similarity?', c: [{ e: 'yes', p: 'similarity' }, { e: 'it weights', p: 'weighting' }] },
      { e: 'no', q: 'What a map sends to zero?', c: [{ e: 'yes', p: 'zero' }, { e: 'no', q: 'What is left after pruning?', c: [{ e: 'yes', p: 'remnant' }, { e: 'no', q: 'A physical object?', c: [{ e: 'yes', p: 'seed' }, { e: 'a file', p: 'odd' }] }] }] },
    ] },
  ] };
  const examples = (pid, n) => D.entries.filter(e => e.plate === pid).slice(0, n).map(label).join(', ');
  function leafEvents(g, pid, paths) {
    const on = v => paths[pid].forEach(b => b.classList.toggle('on', v));
    g.addEventListener('pointerenter', () => on(true)); g.addEventListener('pointerleave', () => on(false));
    g.addEventListener('click', () => document.getElementById('plate-' + pid).scrollIntoView());
  }
  function thumb(g, pid, x, y, size) {
    const im = S('image', { x, y: y - size / 2, width: size, height: size, preserveAspectRatio: 'xMidYMid meet' }, g);
    im.setAttribute('href', img(REP[pid]));
  }
  // wide screens: Darwin-style, branching left to right
  function horizontal() {
    svg.setAttribute('viewBox', '0 0 960 560'); svg.classList.remove('vertical');
    const LX = 690, y0 = 34, dy = 70, ly = Object.fromEntries(leaves.map((p, i) => [p, y0 + i * dy]));
    (function layout(n, depth) {
      n.x = 30 + depth * 118;
      if (n.p) { n.x = LX; n.y = ly[n.p]; return; }
      n.c.forEach(c => layout(c, depth + 1)); n.y = (n.c[0].y + n.c[n.c.length - 1].y) / 2;
    })(T, 0);
    const brG = S('g', {}, svg), txG = S('g', {}, svg), paths = {};
    (function draw(n, trail) {
      if (n.p) { paths[n.p] = trail; return; }
      S('circle', { cx: n.x, cy: n.y, r: 4.5, class: 'node' }, txG);
      S('text', { x: n.x + 10, y: n.y - 9, class: 'q' }, txG).textContent = n.q;
      n.c.forEach(c => {
        const br = S('path', { d: `M${n.x} ${n.y}V${c.y}H${c.x - (c.p ? 60 : 0)}`, class: 'br' }, brG);
        S('text', { x: n.x + 10, y: c.y + (c.y > n.y ? 17 : -7), class: 'yn' }, txG).textContent = c.e;
        draw(c, [...trail, br]);
      });
    })(T, []);
    S('path', { d: `M${T.x - 26} ${T.y}H${T.x}`, class: 'br' }, brG);
    leaves.forEach(pid => {
      const p = plate[pid], y = ly[pid], g = S('g', { class: 'leaf', tabindex: 0, role: 'link' }, svg);
      thumb(g, pid, LX - 64, y, 84);
      S('text', { x: LX + 12, y: y + 8, class: 'r' }, g).textContent = p.roman;
      S('text', { x: LX + 52, y: y + 2, class: 'n' }, g).textContent = p.name.replace(/^The /, '');
      S('text', { x: LX + 52, y: y + 20, class: 'e' }, g).textContent = examples(pid, 2);
      leafEvents(g, pid, paths);
    });
  }
  // phones: the same key read top to bottom, one question per row, indented by depth
  function vertical() {
    svg.classList.add('vertical');
    const W = 360, IND = 22, ROW = 46, LEAF = 70;
    let cur = 22;
    (function layout(n, depth) {
      n.x = 12 + depth * IND; n.y = cur; cur += n.p ? LEAF : ROW;
      if (!n.p) n.c.forEach(c => layout(c, depth + 1));
    })(T, 0);
    svg.setAttribute('viewBox', `0 0 ${W} ${cur - 14}`);
    const brG = S('g', {}, svg), txG = S('g', {}, svg), paths = {};
    const edge = (parent, e) => { const t = S('tspan', { class: 'yn' }, parent); t.textContent = e + ' · '; };
    (function draw(n, trail, e) {
      if (n.p) {
        paths[n.p] = trail;
        const p = plate[n.p], g = S('g', { class: 'leaf', tabindex: 0, role: 'link' }, svg);
        thumb(g, n.p, n.x, n.y, 52);
        const t1 = S('text', { x: n.x + 58, y: n.y - 3, class: 'n' }, g); edge(t1, e);
        const r = S('tspan', { class: 'r' }, t1); r.textContent = p.roman + ' ';
        const nm = S('tspan', {}, t1); nm.textContent = p.name.replace(/^The /, '');
        S('text', { x: n.x + 58, y: n.y + 17, class: 'e' }, g).textContent = examples(n.p, 1);
        leafEvents(g, n.p, paths);
        return;
      }
      S('circle', { cx: n.x, cy: n.y, r: 4.5, class: 'node' }, txG);
      const q = S('text', { x: n.x + 12, y: n.y + 6, class: 'q' }, txG);
      if (e) edge(q, e);
      q.appendChild(document.createTextNode(n.q));
      n.c.forEach(c => {
        const br = S('path', { d: `M${n.x} ${n.y + 5}V${c.y}H${c.x - (c.p ? 2 : 5)}`, class: 'br' }, brG);
        draw(c, [...trail, br], c.e);
      });
    })(T, [], null);
  }
  const narrow = matchMedia('(max-width: 760px)');
  const render = () => { svg.innerHTML = ''; (narrow.matches ? vertical : horizontal)(); };
  narrow.addEventListener('change', render);
  render();
})();

/* ── plates: engraving facing diagram, then the tray of specimens ── */
const host = $('#plates');
D.plates.forEach(p => {
  const es = D.entries.filter(e => e.plate === p.id), single = !window.FIGS[p.id];
  const sec = H('section', { class: 'plate' + (single ? ' single' : ''), id: 'plate-' + p.id, 'data-roman': p.roman }, host);
  H('header', { class: 'plate-head' }, sec, `<p class="num">${p.roman}</p><h2>${esc(p.name)}</h2><p class="tag">${esc(p.kicker)}</p><p class="gloss">${esc(p.gloss)}</p>`);
  const spread = H('div', { class: 'spread' }, sec);
  H('div', { class: 'leaf verso' }, spread, `<img src="img/${p.id}.webp?v=${IMGV}" alt="" loading="lazy">`);
  if (!single) {
    H('div', { class: 'gutter' }, spread);
    const recto = H('div', { class: 'leaf recto' }, spread);
    const box = H('div', { class: 'diagram' }, recto);
    const hint = window.FIGS[p.id](box);
    H('div', { class: 'formula' }, recto, tex(p.sig));
    H('p', { class: 'hint' }, recto, esc(hint));
  } else {
    H('div', { class: 'formula' }, spread.firstChild, tex(p.sig));
  }
  const fig = H('div', { class: 'figurae' }, sec);
  H('div', { class: 'figurae-head' }, fig, `<span>${es.length} specimen${es.length > 1 ? 's' : ''}</span>`);
  const tray = H('ol', { class: 'tray' }, fig);
  es.forEach(e => {
    const li = H('li', {}, tray);
    const b = H('button', { type: 'button', class: 'fig-btn', id: 'fig-' + e.id, style: `--c:${p.color}` }, li,
      `<span class="im">${figure(e)}</span><span class="no">${e.no}</span><span class="nm">${esc(label(e))}</span>`);
    b.onclick = () => openSheet(e.id);
  });
});

/* ── register ── */
const reg = $('#reg');
let letter = '';
[...D.entries].sort((x, y) => x.name.localeCompare(y.name)).forEach(e => {
  const L = e.name[0].toUpperCase();
  if (L !== letter) { letter = L; H('li', { class: 'letter' }, reg, L); }
  const b = H('button', { type: 'button' }, H('li', {}, reg), `<span class="d${e.plate === 'zero' ? ' z' : ''}" style="--c:${plate[e.plate].color}"></span><span class="nm">${esc(e.name)}</span>`);
  b.onclick = () => openSheet(e.id);
  b.addEventListener('pointermove', ev => showTip(ev, e)); b.addEventListener('pointerleave', hideTip);
});

/* ── specimen sheet ── */
const sheet = $('#sheet'), scrim = $('#scrim'), body = $('#sheet-body');
const order = D.entries.map(e => e.id);
let lastFocus = null;
function openSheet(id, push = true) {
  const e = byId[id]; if (!e) return;
  hideTip();
  const p = plate[e.plate], kin = [];
  D.links.forEach(l => { if (l.a === id) kin.push([l.b, l.label]); else if (l.b === id) kin.push([l.a, l.label]); });
  e.related.forEach(r => { if (byId[r] && !kin.some(k => k[0] === r)) kin.push([r, '']); });
  const i = order.indexOf(id), prev = byId[order[(i + order.length - 1) % order.length]], next = byId[order[(i + 1) % order.length]];
  sheet.style.setProperty('--c', p.color);
  body.innerHTML = `
    ${figure(e, 'sp-img').replace('loading="lazy"', '')}
    <p class="sp-where"><a href="#plate-${p.id}" data-close>${p.roman} · ${esc(p.name)}</a> · No. ${e.no}</p>
    <h2>${esc(e.name)}</h2>
    <p class="sp-formal">${esc(e.domain)}</p>
    <p class="sp-short">${esc(e.short)}</p>
    <p class="sp-body">${esc(e.body)}</p>
    ${e.tex ? `<div class="sp-tex">${tex(e.tex)}${e.read ? `<p class="sp-read">${esc(e.read)}</p>` : ''}</div>` : ''}
    ${e.example ? `<div class="sp-sec"><h4>Example</h4><p>${esc(e.example)}</p></div>` : ''}
    ${e.why ? `<div class="sp-sec"><h4>Why “kernel”?</h4><p>${esc(e.why)}</p></div>` : ''}
    ${e.note ? `<div class="sp-sec caution"><h4>Watch out</h4><p>${esc(e.note)}</p></div>` : ''}
    ${e.variants.length ? `<div class="sp-sec"><h4>Variants</h4><ul>${e.variants.map(v => `<li>${esc(v)}</li>`).join('')}</ul></div>` : ''}
    ${e.code ? `<div class="sp-sec"><h4>In code</h4><pre>${esc(e.code)}</pre></div>` : ''}
    ${kin.length ? `<div class="sp-sec"><h4>Related</h4><ul class="sp-kin">${kin.map(([k, lab]) => `<li><button type="button" data-id="${k}">${figure(byId[k])}<span class="nm">${esc(label(byId[k]))}</span>${lab ? `<span class="rl">${esc(lab)}</span>` : ''}</button></li>`).join('')}</ul></div>` : ''}
    <div class="sp-sec"><h4>Sources</h4><ul class="sp-refs">${e.refs.map(r => D.sources[r]).filter(Boolean).map(s => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)}</a><small>${esc(s.publisher)}</small></li>`).join('')}</ul></div>
    <nav class="sp-nav"><button type="button" data-id="${prev.id}">← ${esc(label(prev))}</button><button type="button" data-id="${next.id}">${esc(label(next))} →</button></nav>`;
  body.querySelectorAll('button[data-id]').forEach(b => b.onclick = () => openSheet(b.dataset.id));
  body.querySelector('[data-close]').onclick = () => closeSheet(true);
  if (!sheet.classList.contains('open')) lastFocus = document.activeElement;
  scrim.hidden = false; sheet.classList.add('open'); sheet.setAttribute('aria-hidden', 'false'); sheet.scrollTop = 0;
  $('#sheet-close').focus({ preventScroll: true });
  if (push && location.hash !== '#k/' + id) history.pushState(null, '', '#k/' + id);
}
function closeSheet(keepHash) {
  if (!sheet.classList.contains('open')) return;
  sheet.classList.remove('open'); sheet.setAttribute('aria-hidden', 'true'); scrim.hidden = true;
  if (!keepHash && location.hash.startsWith('#k/')) history.pushState(null, '', location.pathname);
  lastFocus && lastFocus.focus && lastFocus.focus({ preventScroll: true });
}
$('#sheet-close').onclick = () => closeSheet(); scrim.onclick = () => closeSheet();
addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });
addEventListener('popstate', () => { const m = location.hash.match(/^#k\/(.+)$/); m ? openSheet(m[1], false) : closeSheet(true); });

/* ── finder ── */
const q = $('#q'), qr = $('#q-results');
let hits = [], cur = 0;
function search(s) {
  const toks = s.trim().toLowerCase().split(/\s+/).filter(Boolean); if (!toks.length) return [];
  return D.entries.map(e => {
    const nm = (e.name + ' ' + (e.alias || '')).toLowerCase(), meta = (e.formalName + ' ' + e.domain + ' ' + e.type).toLowerCase(), txt = (e.short + ' ' + e.body).toLowerCase();
    let sc = 0; for (const t of toks) sc += nm.startsWith(t) ? 10 : nm.includes(t) ? 6 : meta.includes(t) ? 3 : txt.includes(t) ? 1 : -99;
    return [sc - e.rank / 1000, e];
  }).filter(x => x[0] > 0).sort((a, b) => b[0] - a[0]).slice(0, 9).map(x => x[1]);
}
function renderQ() {
  hits = search(q.value); cur = 0;
  if (!q.value.trim()) { qr.hidden = true; return; }
  qr.hidden = false;
  qr.innerHTML = hits.length ? hits.map((e, i) => `<li data-id="${e.id}" aria-selected="${i === 0}">${figure(e)}<span class="nm">${esc(e.name)}</span><span class="pl">${plate[e.plate].roman}</span></li>`).join('') : '<li class="empty">No such specimen.</li>';
  qr.querySelectorAll('li[data-id]').forEach(li => li.onmousedown = ev => { ev.preventDefault(); pick(li.dataset.id); });
}
function pick(id) { q.value = ''; qr.hidden = true; q.blur(); openSheet(id); const f = document.getElementById('fig-' + id); if (f) { f.classList.remove('flash'); void f.offsetWidth; f.classList.add('flash'); } }
q.addEventListener('input', renderQ);
q.addEventListener('blur', () => setTimeout(() => qr.hidden = true, 120));
q.addEventListener('keydown', e => {
  if ((e.key === 'ArrowDown' || e.key === 'ArrowUp') && hits.length) { e.preventDefault(); cur = (cur + (e.key === 'ArrowDown' ? 1 : -1) + hits.length) % hits.length; qr.querySelectorAll('li[data-id]').forEach((li, i) => li.setAttribute('aria-selected', i === cur)); }
  else if (e.key === 'Enter' && hits[cur]) pick(hits[cur].id);
  else if (e.key === 'Escape') { q.value = ''; renderQ(); q.blur(); }
});
addEventListener('keydown', e => { if (e.key === '/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); q.focus(); } });

/* ── folio: the current plate number, bottom right ── */
const folio = $('#folio');
const marks = [['title', ''], ['conspectus', '0'], ['clavis', '∴'], ...D.plates.map(p => ['plate-' + p.id, p.roman]), ['register', 'ℛ']];
const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) folio.textContent = marks.find(m => m[0] === en.target.id)[1]; }), { rootMargin: '-50% 0px -50% 0px' });
marks.forEach(([id]) => { const el = document.getElementById(id); el && io.observe(el); });

const m = location.hash.match(/^#k\/(.+)$/); if (m) openSheet(m[1], false);
})();
