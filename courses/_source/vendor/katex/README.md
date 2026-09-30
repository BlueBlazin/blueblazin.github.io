# KaTeX 0.18.9

Source: https://www.npmjs.com/package/katex/v/0.18.9
Upstream: https://github.com/KaTeX/KaTeX
License: MIT (see LICENSE).

The build-only `katex.min.js` is copied unchanged from `dist/katex.min.js` in the published npm archive. The public CSS and WOFF2 fonts come from the same archive. Only the CSS font URLs were reduced to WOFF2; unused WOFF/TTF fallbacks are not shipped. The browser does not download the KaTeX JavaScript bundle.

Source archive SHA-256: `78174318fa53363e4321ac3c10b39d3598aaa73a92dc75362eb08b16f6705782`.

To update, replace the build bundle, CSS, fonts, and licenses together; change the stylesheet version in `build.py`; then rebuild and run all verification commands in the parent README.
