# The Kernel Zoo

A visual, searchable field guide to the word **kernel** across STEM, published at
<https://blueblazin.github.io/kernel-zoo/>.

The atlas contains 103 entries in nine conceptual families, 105 cited sources,
and four interactive numerical examples. Entries distinguish independent senses,
named specializations, architecture variants, and related terminology. Families
are reading aids, not mutually exclusive mathematical classes or a historical
genealogy. The scope note on the website explains the limits of any finite survey.

## Editing and building

- `_source/catalog.py` contains the curated entries and source registry.
- `_source/template.html` contains the page structure and interactive-example markup.
- `_source/build.py` generates `index.html` and the reusable `catalog.json` export.
- `styles.css` and `app.js` provide presentation and interactions.

From the repository root, run:

```sh
python kernel-zoo/_source/build.py
node --check kernel-zoo/app.js
```

The builder uses Python's standard library, Node, and the repository's existing
vendored KaTeX runtime. Equations are rendered at build time to HTML and MathML.
The published page uses the existing `courses/assets/katex/` stylesheet and fonts.
No framework, package installation, external CDN, or server is needed to read it.

## Research and verification

Definitions are original paraphrases with entry-level references to official
documentation, research papers, mathematical texts, and university notes. Examples
and SVG concept diagrams were created for this atlas. Some papers require access
through their publisher. Source URLs and the complete bibliography are included
in both the page and the JSON export. Research was checked on 9 October 2026.

Before publication, filtering and convolution outputs were compared with SciPy,
and Gram matrices and eigenvalues with NumPy. Browser checks covered search,
family filters, cross-family links, GPU launch bounds, nullspace values, equation
rendering, five viewport widths from 320 to 1440 pixels, enlarged text, and reading
with JavaScript disabled. Desktop and mobile screenshots were visually inspected.

The numerical labs are teaching examples: the GPU diagram shows logical threads
and blocks, not physical cores; the filter uses a synthetic numerical grid; the
Gram-matrix eigenvalues are numerical approximations.
