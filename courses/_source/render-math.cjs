// Build-time math rendering. Browsers receive finished HTML and accessible MathML.
const fs = require('node:fs');
const katex = require('./vendor/katex/katex.min.js');
const expressions = JSON.parse(fs.readFileSync(0, 'utf8'));
const rendered = expressions.map(([tex, displayMode]) => [tex, displayMode,
  katex.renderToString(tex, {
    displayMode, output: 'htmlAndMathml', throwOnError: true,
    strict: 'error', trust: false, maxExpand: 1000
  })
]);
process.stdout.write(JSON.stringify(rendered));
