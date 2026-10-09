/* The recto of each plate: a working figure assembled from engraved sprites.
   FIGS[id](box) draws into box and returns a one-line hint. */
(() => {
const NS = 'http://www.w3.org/2000/svg', XL = 'http://www.w3.org/1999/xlink';
const IV = '#efe8d8', AM = '#e9bd4c', RD = '#ee6a48';
const S = (tag, a = {}, p) => { const e = document.createElementNS(NS, tag); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const ease = k => k < .5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const ptr = (svg, ev) => { const p = svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); };
function tween(ms, step, done) { const t0 = performance.now(); const f = t => { const k = reduce ? 1 : clamp((t - t0) / ms, 0, 1); step(ease(k)); if (k < 1) requestAnimationFrame(f); else done && done(); }; requestAnimationFrame(f); }
const svgIn = (box, vb = '0 0 600 600') => S('svg', { viewBox: vb }, box);
// a sprite centered on (x, y), fitted into a size × size box
function spr(parent, name, x, y, size, cls = '') {
  const im = S('image', { width: size, height: size, x: x - size / 2, y: y - size / 2, preserveAspectRatio: 'xMidYMid meet', class: cls }, parent);
  im.setAttribute('href', `img/sprites/${name}.webp`); im.setAttributeNS(XL, 'href', `img/sprites/${name}.webp`);
  return im;
}
const place = (im, x, y, size) => { const s = size ?? +im.getAttribute('width'); im.setAttribute('x', x - s / 2); im.setAttribute('y', y - s / 2); if (size != null) { im.setAttribute('width', s); im.setAttribute('height', s); } };
function gesture(el, svg, { move, tap, down }) {
  el.addEventListener('pointerdown', e => {
    e.stopPropagation(); el.setPointerCapture(e.pointerId);
    const p0 = ptr(svg, e); let moved = false; down && down(p0);
    const mv = ev => { const p = ptr(svg, ev); if (Math.hypot(p.x - p0.x, p.y - p0.y) > 5) moved = true; if (moved && move) move(p); };
    const up = ev => { el.removeEventListener('pointermove', mv); el.removeEventListener('pointerup', up); if (!moved && tap) tap(ptr(svg, ev)); };
    el.addEventListener('pointermove', mv); el.addEventListener('pointerup', up);
  });
}
function picker(box, opts, cur, on) {
  const wrap = document.createElement('div'); wrap.className = 'picker'; box.appendChild(wrap);
  const btns = opts.map(o => {
    const b = document.createElement('button'); b.type = 'button'; b.title = o.title; b.setAttribute('aria-label', o.title); b.setAttribute('aria-pressed', o.v === cur);
    if (o.icon) o.icon(S('svg', { viewBox: '0 0 40 24' }, b)); else { b.className = 't'; b.textContent = o.text; }
    b.onclick = () => { btns.forEach(x => x.setAttribute('aria-pressed', x === b)); on(o.v); };
    wrap.appendChild(b); return b;
  });
}
const curveIcon = fn => s => { let d = ''; for (let i = 0; i <= 40; i++) d += (i ? 'L' : 'M') + i + ' ' + (19 - fn((i - 20) / 20) * 16).toFixed(1); S('path', { d, fill: 'none', stroke: 'currentColor', 'stroke-width': 1.6, 'stroke-linejoin': 'round' }, s); };
const onView = (el, fn) => { const io = new IntersectionObserver(es => { if (es[0].isIntersecting) { io.disconnect(); fn(); } }, { threshold: .55 }); io.observe(el); };
const FIGS = {};

/* I — the seed: the husk and shell come away from the kernel */
FIGS.seed = box => {
  const svg = svgIn(box), C = 300;
  const kernel = spr(svg, 'walnut', C, C, 290);
  const layers = [spr(svg, 'ring-shell', C, C, 430), spr(svg, 'ring-husk', C, C, 580)];
  layers.forEach(l => l.style.transformOrigin = '300px 300px');
  kernel.style.transformOrigin = '300px 300px';
  let open = 0, busy = 0;
  svg.style.cursor = 'pointer';
  svg.addEventListener('click', () => {
    if (busy) return; busy = 1;
    tween(1500, e => {
      const v = open ? 1 - e : e;
      layers.forEach((l, i) => { const q = clamp(v * 1.8 - (1 - i) * .5, 0, 1); l.style.transform = `scale(${1 + q * (.35 + i * .15)}) rotate(${q * (i ? 25 : -18)}deg)`; l.style.opacity = 1 - q; });
      kernel.style.transform = `scale(${1 + v * .22})`;
      kernel.classList.toggle('lit', v > .7);
    }, () => { open = 1 - open; busy = 0; });
  });
  return 'Click to crack it open. The husk and shell come away, and what remains is the kernel.';
};

/* II — the core: every request must pass through the ring of gears to reach the ruby */
FIGS.core = box => {
  const svg = svgIn(box), C = 300, at = (r, a) => [C + r * Math.cos(a), C + r * Math.sin(a)];
  S('circle', { cx: C, cy: C, r: 290, fill: 'none', stroke: IV, 'stroke-opacity': .14, 'stroke-dasharray': '2 6' }, svg);
  const ring = spr(svg, 'ring-gears', C, C, 340); ring.style.transformOrigin = '300px 300px'; ring.style.transition = 'transform .8s';
  const ruby = spr(svg, 'ruby', C, C, 120);
  const svc = [0, 1, 2, 3].map(i => ({ a: -Math.PI / 2 + Math.PI / 4 + i * Math.PI / 2, r: 140, im: spr(svg, 'cog', 0, 0, 46) }));
  const put = () => svc.forEach(s => { const [x, y] = at(s.r, s.a); place(s.im, x, y); });
  put();
  let mode = 'mono';
  for (let i = 0; i < 6; i++) {
    const a = -Math.PI / 2 + i * Math.PI / 3, [x, y] = at(252, a);
    const k = spr(svg, 'key', x, y, 92, 'grab'); k.style.cursor = 'pointer';
    k.addEventListener('click', () => send(a));
  }
  const fx = S('g', { style: 'pointer-events:none' }, svg);
  function setMode(m) {
    mode = m; const r0 = svc[0].r, r1 = m === 'mono' ? 140 : 214;
    ring.style.transform = `scale(${m === 'mono' ? 1 : .72})`;
    tween(800, e => { svc.forEach(s => s.r = r0 + (r1 - r0) * e); put(); });
  }
  function send(a) {
    const letter = spr(fx, 'letter', 0, 0, 42);
    const near = svc.reduce((b, s) => Math.abs(Math.atan2(Math.sin(s.a - a), Math.cos(s.a - a))) < Math.abs(Math.atan2(Math.sin(b.a - a), Math.cos(b.a - a))) ? s : b);
    const kr = mode === 'mono' ? 150 : 112;
    const hops = mode === 'mono' ? [[252, a], [kr, a], [0, a], [kr, a], [252, a]]
      : [[252, a], [kr, a], [kr, near.a], [214, near.a], [kr, near.a], [0, near.a], [kr, a], [252, a]];
    let i = 0;
    const next = () => {
      if (i >= hops.length - 1) { letter.remove(); ring.classList.remove('lit'); ruby.classList.remove('lit'); return; }
      const [r0, a0] = hops[i], [r1, a1] = hops[i + 1]; i++;
      tween(450, e => { const r = r0 + (r1 - r0) * e, [x, y] = at(r, a0 + (a1 - a0) * e); place(letter, x, y);
        ring.classList.toggle('lit', Math.abs(r - kr) < 30); ruby.classList.toggle('lit', r < 40); }, next);
    };
    next();
  }
  picker(box, [
    { v: 'mono', title: 'Monolithic kernel (Linux): services inside the ring', icon: s => S('circle', { cx: 20, cy: 12, r: 7.5, fill: 'none', stroke: 'currentColor', 'stroke-width': 6 }, s) },
    { v: 'micro', title: 'Microkernel (seL4): services moved outside', icon: s => { S('circle', { cx: 20, cy: 12, r: 6, fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, s); [[34, 4], [6, 4], [34, 20], [6, 20]].forEach(([x, y]) => S('circle', { cx: x, cy: y, r: 2.6, fill: 'currentColor' }, s)); } },
  ], 'mono', setMode);
  return 'Click a key to send a sealed request. It must pass through the ring of gears (the kernel) to reach the ruby (the hardware). Switch to a microkernel and the cogs, its services, move outside the ring.';
};

/* III — the routine: one task, one bee per cell, all at once */
FIGS.routine = box => {
  const svg = svgIn(box, '0 0 600 520');
  const n = 43, cols = 8, rows = 6, dx = 66, dy = 58, cs = 74;
  const cells = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const i = r * cols + c, x = 58 + c * dx + (r % 2) * dx / 2, y = 50 + r * dy * 1.42;
    spr(svg, i < n ? 'cell' : 'capped', x, y, cs);
    cells.push({ i, x, y });
  }
  const bees = S('g', { style: 'pointer-events:none' }, svg);
  let timers = [];
  const launch = () => {
    timers.forEach(clearTimeout); timers = []; bees.innerHTML = '';
    cells.forEach(c => { if (c.i >= n) return;
      timers.push(setTimeout(() => {
        const b = spr(bees, 'bee', c.x, c.y, 44); b.style.transformOrigin = `${c.x}px ${c.y}px`;
        b.style.transform = `rotate(${(Math.random() - .5) * 50}deg) scale(.2)`; b.style.opacity = 0; b.style.transition = 'transform .35s cubic-bezier(.3,1.5,.5,1),opacity .2s';
        requestAnimationFrame(() => requestAnimationFrame(() => { b.style.transform = `rotate(${(Math.random() - .5) * 40}deg) scale(1)`; b.style.opacity = 1; }));
      }, reduce ? 0 : 120 + Math.random() * 1500)); });
  };
  svg.style.cursor = 'pointer';
  svg.addEventListener('click', launch);
  onView(svg, launch);
  return 'Click to run it again. Every cell gets its own bee doing the same job, in no fixed order. The sealed cells lie past the end of the data, so no bee goes there.';
};

/* IV — the weighting: the lens gathers nearby pebbles, magnifying each by its weight */
FIGS.weighting = box => {
  const svg = svgIn(box), N = 300, M = 20, X = u => 30 + u * 540;
  const f = Array.from({ length: N }, (_, i) => { const y = i / N; return (y > .14 && y < .38 ? 1 : .08) + Math.exp(-(((y - .55) / .012) ** 2) / 2) + (y > .66 && y < .9 ? (y - .66) / .24 * .85 : 0); });
  const KS = {
    box: t => Math.abs(t) < .04 ? 1 : 0,
    gauss: t => Math.exp(-t * t / (2 * .028 * .028)),
    dirichlet: t => { const s = Math.sin(Math.PI * t), m = 7; return Math.abs(s) < 1e-9 ? 2 * m + 1 : Math.sin((2 * m + 1) * Math.PI * t) / s; },
    fejer: t => { const s = Math.sin(Math.PI * t), m = 8; return Math.abs(s) < 1e-9 ? m : (Math.sin(m * Math.PI * t) / s) ** 2 / m; },
  };
  let kind = 'gauss', x = .3, ker = [], g = [];
  const idx = Array.from({ length: M }, (_, k) => Math.round((k + .5) / M * N));
  const prof = S('path', { fill: 'none', stroke: RD, 'stroke-width': 1.6, opacity: .7 }, svg);
  const base = S('line', { x1: 30, x2: 570, y1: 112, y2: 112, stroke: IV, 'stroke-opacity': .15 }, svg);
  const pebbles = idx.map(j => spr(svg, 'pebble', X(j / N), 210, 10));
  const lens = spr(svg, 'magnifier', 0, 0, 200); lens.style.pointerEvents = 'none';
  S('line', { x1: 30, x2: 570, y1: 330, y2: 330, stroke: IV, 'stroke-opacity': .12, 'stroke-dasharray': '2 6' }, svg);
  const marbles = idx.map(j => spr(svg, 'marble', X(j / N), 450, 10));
  const fmax = Math.max(...f);
  pebbles.forEach((p, k) => p.dataset.s = 16 + 30 * f[idx[k]] / fmax);
  function compute() {
    ker = Array.from({ length: N }, (_, j) => { let t = j / N; if (t > .5) t -= 1; return KS[kind](t); });
    const sum = ker.reduce((a, b) => a + b, 0); ker = ker.map(v => v / sum);
    g = f.map((_, i) => { let s = 0; for (let j = 0; j < N; j++) s += ker[j] * f[(i - j + N) % N]; return s; });
    draw();
  }
  function draw() {
    const i0 = Math.round(x * N) % N, km = Math.max(...ker.map(Math.abs)), gm = Math.max(...g);
    // weight profile above the pebbles
    let d = ''; for (let q = 0; q <= N; q++) d += (q ? 'L' : 'M') + X(q / N).toFixed(1) + ' ' + (112 - ker[(i0 - q + N * 2) % N] / km * 70).toFixed(1);
    prof.setAttribute('d', d);
    pebbles.forEach((p, k) => { const w = ker[(i0 - idx[k] + N * 2) % N] / km, s = +p.dataset.s * (1 + .7 * Math.max(0, w));
      place(p, X(idx[k] / N), 210, s); p.style.opacity = .5 + .5 * Math.max(0, w); p.classList.toggle('neg', w < -.05); });
    marbles.forEach((m, k) => { const v = g[idx[k]] / gm; place(m, X(idx[k] / N), 450, 10 + 44 * Math.max(0, v)); m.style.opacity = idx[k] <= i0 ? 1 : .16; });
    place(lens, X(x), 252, 200);
  }
  const set = p => { x = clamp((p.x - 30) / 540, 0, .999); draw(); };
  svg.style.cursor = 'ew-resize';
  gesture(svg, svg, { down: set, move: set });
  const sinc = (t, m) => { const s = Math.sin(Math.PI * t * .5); return Math.abs(s) < 1e-6 ? 1 : Math.sin(m * Math.PI * t * .5) / s / m; };
  picker(box, [
    { v: 'box', title: 'Box: a plain moving average', icon: curveIcon(t => Math.abs(t) < .35 ? 1 : 0) },
    { v: 'gauss', title: 'Gaussian: the heat and density-estimation kernel', icon: curveIcon(t => Math.exp(-t * t / .08)) },
    { v: 'dirichlet', title: 'Dirichlet: Fourier partial sums (some weights negative)', icon: curveIcon(t => sinc(t, 7)) },
    { v: 'fejer', title: 'Fejér: averaged Fourier sums (never negative)', icon: curveIcon(t => sinc(t, 5) ** 2) },
  ], kind, v => { kind = v; compute(); });
  compute();
  return 'Drag across the figure. The red curve shows the kernel’s weights. Each pebble under the lens grows by its weight, and the weighted sum sets the size of the blue marble below.';
};

/* V — the similarity: shells compared pair by pair; amber beads record how alike */
FIGS.similarity = box => {
  const svg = svgIn(box);
  const pts = [[.6, .5], [.85, .2], [.35, .8], [.8, .82], [-.55, -.4], [-.85, -.7], [-.3, -.82], [-.75, .15]];
  const F = 280, L = 1.12, toS = ([u, v]) => [(u + L) / (2 * L) * F, (L - v) / (2 * L) * F], fromS = p => [clamp(p.x / F * 2 * L - L, -1, 1), clamp(L - p.y / F * 2 * L, -1, 1)];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1], d2 = (a, b) => (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2;
  const KS = { linear: (a, b) => dot(a, b), gauss: (a, b) => Math.exp(-d2(a, b) / (2 * .45 * .45)), negdist: (a, b) => -Math.sqrt(d2(a, b)) };
  let kind = 'gauss', hover = null;
  S('rect', { x: .5, y: .5, width: F, height: F, fill: 'none', stroke: IV, 'stroke-opacity': .18 }, svg);
  const M = { x: 316, c: 35.5 };
  const hdrs = [];
  const cells = [];
  for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) {
    const cx = M.x + j * M.c + M.c / 2, cy = i * M.c + M.c / 2;
    const hit = S('rect', { x: cx - M.c / 2, y: cy - M.c / 2, width: M.c, height: M.c, fill: 'transparent' }, svg);
    const b = spr(svg, 'bead-amber', cx, cy, 10); b.style.pointerEvents = 'none';
    hit.addEventListener('pointerenter', () => { hover = [i, j]; draw(); }); hit.addEventListener('pointerleave', () => { hover = null; draw(); });
    cells.push({ i, j, b, cx, cy });
  }
  const hl = S('rect', { width: M.c, height: M.c, fill: 'none', stroke: IV, 'stroke-width': 1.2, opacity: 0, style: 'pointer-events:none' }, svg);
  const link = S('line', { stroke: AM, 'stroke-width': 2, opacity: 0, 'stroke-dasharray': '4 4', style: 'pointer-events:none' }, svg);
  S('line', { x1: 0, x2: 600, y1: 470, y2: 470, stroke: IV, 'stroke-opacity': .14 }, svg);
  const spec = Array.from({ length: 8 }, (_, k) => spr(svg, 'bead-amber', 40 + k * 74, 470, 10));
  const shells = pts.map((p, i) => { const s = spr(svg, i < 4 ? 'scallop' : 'cowrie', 0, 0, 52, 'grab'); gesture(s, svg, { move: q => { pts[i] = fromS(q); draw(); } }); return s; });
  function eig(A) {
    const n = A.length, a = A.map(r => r.slice());
    for (let sw = 0; sw < 50; sw++) {
      let off = 0; for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += a[p][q] ** 2; if (off < 1e-14) break;
      for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) {
        if (Math.abs(a[p][q]) < 1e-15) continue;
        const th = (a[q][q] - a[p][p]) / (2 * a[p][q]), t = Math.sign(th || 1) / (Math.abs(th) + Math.sqrt(th * th + 1)), c = 1 / Math.sqrt(t * t + 1), s = t * c;
        for (let k = 0; k < n; k++) { const x = a[k][p], y = a[k][q]; a[k][p] = c * x - s * y; a[k][q] = s * x + c * y; }
        for (let k = 0; k < n; k++) { const x = a[p][k], y = a[q][k]; a[p][k] = c * x - s * y; a[q][k] = s * x + c * y; }
      }
    }
    return a.map((r, i) => r[i]).sort((x, y) => y - x);
  }
  const setBead = (im, v, max, x, y, cap) => { const neg = v < 0, name = neg ? 'bead-red' : 'bead-amber'; if (!im.getAttribute('href').includes(name)) { im.setAttribute('href', `img/sprites/${name}.webp`); im.setAttributeNS(XL, 'href', `img/sprites/${name}.webp`); } place(im, x, y, 4 + cap * Math.sqrt(Math.abs(v) / max)); };
  function draw() {
    pts.forEach((p, i) => { const [x, y] = toS(p); place(shells[i], x, y); });
    const G = pts.map(a => pts.map(b => KS[kind](a, b))), m = Math.max(...G.flat().map(Math.abs)) || 1;
    cells.forEach(({ i, j, b, cx, cy }) => setBead(b, G[i][j], m, cx, cy, 28));
    if (hover) { const [i, j] = hover, a = toS(pts[i]), b = toS(pts[j]);
      link.setAttribute('x1', a[0]); link.setAttribute('y1', a[1]); link.setAttribute('x2', b[0]); link.setAttribute('y2', b[1]); link.setAttribute('opacity', 1);
      hl.setAttribute('x', M.x + j * M.c); hl.setAttribute('y', i * M.c); hl.setAttribute('opacity', .6); }
    else { link.setAttribute('opacity', 0); hl.setAttribute('opacity', 0); }
    const ev = eig(G), em = Math.max(...ev.map(Math.abs)) || 1;
    ev.forEach((l, k) => setBead(spec[k], Math.abs(l) < 1e-9 * em ? 0 : l, em, 40 + k * 74, 470, 56));
  }
  picker(box, [
    { v: 'linear', title: 'Dot product', text: '⟨x, y⟩' },
    { v: 'gauss', title: 'Gaussian similarity', icon: curveIcon(t => Math.exp(-t * t / .08)) },
    { v: 'negdist', title: 'Negative distance: looks like a similarity, but is not a kernel', text: '−‖x − y‖' },
  ], kind, v => { kind = v; draw(); });
  draw();
  return 'Drag the shells. Each bead in the grid shows how alike one pair of shells is. The row below shows the grid’s eigenvalues: a valid kernel never gives a red (negative) one.';
};

/* VI — the vanishing: the map folds the plane; beads on the dashed line fall into the brass ring */
FIGS.zero = box => {
  const svg = svgIn(box), O = 300, U = 44;
  const gcd = (x, y) => y ? gcd(y, x % y) : Math.abs(x);
  const DIRS = []; for (let a = -3; a <= 3; a++) for (let b = 0; b <= 3; b++) if ((b > 0 || a > 0) && gcd(Math.abs(a), b) === 1) DIRS.push([a, b]);
  let dir = [2, 1], t = 0;
  const u = [Math.cos(-.5), Math.sin(-.5)];
  const lat = []; for (let a = -6; a <= 6; a++) for (let b = -6; b <= 6; b++) if (a * a + b * b <= 40) lat.push([a, b]);
  const imL = S('line', { stroke: AM, 'stroke-width': 1.4 }, svg);
  const kerL = S('line', { stroke: IV, 'stroke-width': 1.4, 'stroke-dasharray': '6 7' }, svg);
  const beads = lat.map(() => spr(svg, 'bead-ochre', 0, 0, 20));
  const zero = spr(svg, 'ring-brass', O, O, 52);
  const toS = ([a, b]) => [O + a * U, O - b * U];
  const setName = (im, n) => { if (!im.getAttribute('href').endsWith(n + '.webp')) { im.setAttribute('href', `img/sprites/${n}.webp`); im.setAttributeNS(XL, 'href', `img/sprites/${n}.webp`); } };
  function draw() {
    const L = Math.hypot(...dir), d = [dir[0] / L, dir[1] / L], n = [d[1], -d[0]], e = ease(t);
    lat.forEach((p, i) => {
      const s = p[0] * n[0] + p[1] * n[1], img = [s * u[0] * 1.1, s * u[1] * 1.1];
      const [x, y] = toS([p[0] + (img[0] - p[0]) * e, p[1] + (img[1] - p[1]) * e]), inK = Math.abs(s) < 1e-9;
      setName(beads[i], inK ? 'ring-brass' : s > 0 ? 'bead-blue' : 'bead-ochre');
      place(beads[i], x, y, inK ? 18 : 20); beads[i].style.opacity = inK && e > .97 ? 0 : 1;
    });
    const a = toS([-d[0] * 7, -d[1] * 7]), b = toS([d[0] * 7, d[1] * 7]);
    kerL.setAttribute('x1', a[0]); kerL.setAttribute('y1', a[1]); kerL.setAttribute('x2', b[0]); kerL.setAttribute('y2', b[1]); kerL.setAttribute('opacity', .7 * (1 - e));
    const c1 = toS([-u[0] * 6.6, -u[1] * 6.6]), c2 = toS([u[0] * 6.6, u[1] * 6.6]);
    imL.setAttribute('x1', c1[0]); imL.setAttribute('y1', c1[1]); imL.setAttribute('x2', c2[0]); imL.setAttribute('y2', c2[1]); imL.setAttribute('opacity', .15 + .6 * e);
    zero.classList.toggle('lit', e > .9);
  }
  svg.style.cursor = 'pointer';
  gesture(svg, svg, {
    tap: () => { const from = t, to = t > .5 ? 0 : 1; tween(1500, e => { t = from + (to - from) * e; draw(); }); },
    move: p => { if (t > .01) return; const a = Math.atan2(O - p.y, p.x - O); let best = dir, bd = 9;
      DIRS.forEach(D => { const q = 2 * (Math.atan2(D[1], D[0]) - a), diff = Math.abs(Math.atan2(Math.sin(q), Math.cos(q))); if (diff < bd) { bd = diff; best = D; } }); dir = best; draw(); },
  });
  draw();
  return 'Click to apply the map. The plane folds onto one line, and every bead on the dashed line lands in the brass ring at zero. Before clicking, drag to rotate the line.';
};

/* VII — the remnant: a room, and the patch of carpet from which one lantern sees every wall */
FIGS.remnant = box => {
  const svg = svgIn(box);
  const star = (k, Ro, Ri) => Array.from({ length: 2 * k }, (_, i) => { const a = -Math.PI / 2 + i * Math.PI / k, r = i % 2 ? Ri : Ro; return [300 + r * Math.cos(a), 300 + r * Math.sin(a)]; });
  const SH = { star: star(6, 280, 140), cross: [[215, 22], [385, 22], [385, 215], [578, 215], [578, 385], [385, 385], [385, 578], [215, 578], [215, 385], [22, 385], [22, 215], [215, 215]], room: [[22, 40], [578, 40], [578, 560], [430, 560], [430, 200], [170, 200], [170, 560], [22, 560]] };
  let pts = SH.star.map(p => p.slice()), guard = null, KP = [];
  const uid = 'r' + Math.random().toString(36).slice(2, 7);
  const defs = S('defs', {}, svg);
  const roomClip = S('path', {}, S('clipPath', { id: uid + 'a' }, defs)), kerClip = S('path', {}, S('clipPath', { id: uid + 'b' }, defs));
  const floor = S('image', { x: 0, y: 0, width: 600, height: 600, preserveAspectRatio: 'xMidYMid slice', 'clip-path': `url(#${uid}a)` }, svg);
  floor.setAttribute('href', 'img/sprites/tex-floor.webp');
  const carpet = S('image', { x: 0, y: 0, width: 600, height: 600, preserveAspectRatio: 'xMidYMid slice', 'clip-path': `url(#${uid}b)` }, svg);
  carpet.setAttribute('href', 'img/sprites/tex-carpet.webp');
  S('rect', { x: 0, y: 0, width: 600, height: 600 }, S('clipPath', { id: uid + 'c' }, defs));
  const cuts = S('g', { style: 'pointer-events:none', 'clip-path': `url(#${uid}c)` }, svg);
  const wall = S('path', { fill: 'none', stroke: IV, 'stroke-width': 3, 'stroke-linejoin': 'round' }, svg);
  const kerLine = S('path', { fill: 'none', stroke: IV, 'stroke-width': 1, 'stroke-opacity': .6 }, svg);
  const sight = S('g', { style: 'pointer-events:none' }, svg);
  const lamp = spr(svg, 'lantern', 300, 300, 52); lamp.style.pointerEvents = 'none'; lamp.style.display = 'none';
  const vg = S('g', {}, svg);
  const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const area = ps => ps.reduce((s, p, i) => { const q = ps[(i + 1) % ps.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0) / 2;
  const inside = (p, ps) => { let c = false; for (let i = 0, j = ps.length - 1; i < ps.length; j = i++) { const a = ps[i], b = ps[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]) c = !c; } return c; };
  const segX = (p, q, a, b) => cross(p, q, a) * cross(p, q, b) < -1e-9 && cross(a, b, p) * cross(a, b, q) < -1e-9;
  function kernel() {
    const sg = Math.sign(area(pts)) || 1; let K = [[-3e3, -3e3], [3e3, -3e3], [3e3, 3e3], [-3e3, 3e3]];
    for (let i = 0; i < pts.length && K.length; i++) {
      const a = pts[i], b = pts[(i + 1) % pts.length], out = [], side = p => sg * cross(a, b, p);
      for (let j = 0; j < K.length; j++) { const p = K[j], q = K[(j + 1) % K.length], sp = side(p), sq = side(q);
        if (sp >= 0) out.push(p); if ((sp >= 0) !== (sq >= 0)) { const tt = sp / (sp - sq); out.push([p[0] + (q[0] - p[0]) * tt, p[1] + (q[1] - p[1]) * tt]); } }
      K = out;
    }
    return Math.abs(area(K)) < 1 ? [] : K;
  }
  const visible = (p, k) => { const v = pts[k];
    for (let i = 0; i < pts.length; i++) { const j = (i + 1) % pts.length; if (i === k || j === k) continue; if (segX(p, v, pts[i], pts[j])) return false; }
    return [.2, .5, .8].every(f => inside([p[0] + (v[0] - p[0]) * f, p[1] + (v[1] - p[1]) * f], pts)); };
  const path = ps => ps.length ? 'M' + ps.map(p => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('L') + 'Z' : 'M0 0Z';
  function draw() {
    const d = path(pts); wall.setAttribute('d', d); roomClip.setAttribute('d', d);
    cuts.innerHTML = '';
    pts.forEach((a, i) => { const b = pts[(i + 1) % pts.length], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
      S('line', { x1: a[0] - dx / L * 900, y1: a[1] - dy / L * 900, x2: a[0] + dx / L * 900, y2: a[1] + dy / L * 900, stroke: IV, 'stroke-width': .7, opacity: .12 }, cuts); });
    KP = kernel(); kerClip.setAttribute('d', path(KP)); kerLine.setAttribute('d', KP.length ? path(KP) : '');
    vg.innerHTML = '';
    pts.forEach((p, i) => { const s = spr(vg, 'starfish', p[0], p[1], 38, 'grab'); gesture(s, svg, { move: q => { pts[i] = [clamp(q.x, 0, 600), clamp(q.y, 0, 600)]; draw(); } }); });
    drawGuard();
  }
  function drawGuard() {
    sight.innerHTML = '';
    if (!guard || !inside(guard, pts)) { lamp.style.display = 'none'; return; }
    lamp.style.display = '';
    pts.forEach((v, k) => { const ok = visible(guard, k);
      S('line', { x1: guard[0], y1: guard[1], x2: v[0], y2: v[1], stroke: ok ? AM : RD, 'stroke-width': ok ? 1.1 : 1.6, 'stroke-dasharray': ok ? '' : '4 6', opacity: ok ? .75 : .9 }, sight); });
    place(lamp, guard[0], guard[1]); lamp.classList.toggle('lit', KP.length > 2 && inside(guard, KP));
  }
  svg.addEventListener('pointermove', e => { if (e.buttons) return; const p = ptr(svg, e); guard = [p.x, p.y]; drawGuard(); });
  svg.addEventListener('pointerleave', () => { guard = null; drawGuard(); });
  const icon = shape => s => { const xs = shape.map(p => p[0]), ys = shape.map(p => p[1]), mx = Math.min(...xs), my = Math.min(...ys), sc = 22 / Math.max(Math.max(...xs) - mx, Math.max(...ys) - my);
    S('path', { d: path(shape.map(([x, y]) => [9 + (x - mx) * sc, 1 + (y - my) * sc])), fill: 'none', stroke: 'currentColor', 'stroke-width': 1.5, 'stroke-linejoin': 'round' }, s); };
  picker(box, Object.entries(SH).map(([k, v]) => ({ v: k, title: { star: 'Star-shaped room', cross: 'Cross-shaped room', room: 'U-shaped room' }[k], icon: icon(v) })), 'star', k => { pts = SH[k].map(p => p.slice()); draw(); });
  draw();
  return 'Move the lantern around the room. Only from the carpet, the kernel, does its light reach every corner. Drag the starfish to reshape the walls.';
};

window.FIGS = FIGS;
})();
