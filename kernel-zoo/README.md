# Kernel zoo

An interactive map of STEM meanings of **kernel**, published at
<https://blueblazin.github.io/kernel-zoo/>.

The catalogue has 103 entries in 14 fields and 105 cited sources. The opening map
emphasizes familiar computing and mathematical uses. This is an editorial order,
not a measured popularity ranking. Selecting a node opens its definition and a
focused graph of connections. The complete index is searchable and can be sorted
by name or filtered by field. Four numerical experiments cover filtering, Gram
matrices, GPU launches, and nullspaces.

Categories are reading aids, not exclusive mathematical classifications. Named
edges describe explicit relationships; dashed edges compare different senses;
dotted edges are additional cross-references. They do not assert historical
ancestry. Some entries are separate meanings; others are named specializations,
architectures, or related terms. The scope note explains the limits of a finite
survey.

## Editing

- `_source/catalog.py`: researched definitions, examples, and source registry.
- `_source/design.py`: display categories, familiar-entry order, aliases, and
  explicit edge labels. The common map uses authored coordinates so it stays
  stable while the reader explores.
- `_source/icons.py`: original SVG concept diagrams.
- `_source/template.html` and `_source/labs.html`: interface and experiment markup.
- `_source/build.py`: generates the map page, machine-readable `catalog.json`,
  and the JavaScript-free `reference.html`.
- `app.js`: map, search, index, reader, navigation, and touch interactions.
- `experiments.js`: the four numerical examples.
- `styles.css`: responsive layout and presentation.

From the repository root:

```sh
python kernel-zoo/_source/build.py
node --check kernel-zoo/app.js
node --check kernel-zoo/experiments.js
```

The builder uses Python's standard library, Node, and the repository's existing
vendored KaTeX runtime. Equations are rendered at build time to HTML and MathML.
The pages use the existing `courses/assets/katex/` stylesheet and fonts. No
framework, external CDN, package installation, or server is required.

## Research and verification

Definitions are original paraphrases with entry-level references to official
technical documentation, research papers, mathematical texts, and university
notes. Examples and SVG diagrams were created for this catalogue. Some papers
require publisher access. Research was checked on 9 October 2026.

Filtering and convolution outputs were compared with SciPy; Gram matrices and
eigenvalues with NumPy. Browser checks cover every entry panel, every category,
search and keyboard selection, index sorting, back navigation, pan and zoom,
responsive layouts, enlarged text, touch input, and the static version. Desktop
and mobile screenshots are visually inspected before publication.

The GPU experiment shows logical threads and blocks, not physical cores or
execution order. The filter uses synthetic numbers. Gram-matrix eigenvalues are
numerical approximations.
