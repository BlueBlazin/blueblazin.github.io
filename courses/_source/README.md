# Practical AI courses

A course directory at `/courses/` and three independent static course websites, published alongside the existing blog:

- `/courses/llm-architectures/`
- `/courses/gpu-kernels/`
- `/courses/agent-harnesses/`

Each course has a Week 1, Day 0 handbook for setup, optional reviews, and administration. Regular days contain substantive implementation, experiments, derivations, or technical analysis. Weekdays are capped at one hour, Saturdays at two hours, and Sundays have no assigned work. Setup and later portfolio work are outside the displayed practical-hour totals and should fit within the learner's available time by extending the calendar as needed.

## Edit and build

The three named source directories own their course configuration, lesson content, schedule, direct resource catalog, and Day 0 organization. Stable checklist IDs are retained from `original-schedule.json`; they do not depend on current calendar positions. `resources.json` records vetted direct URLs, publisher/provenance, verification date, and optional video IDs. `reorganization.json` maps each practical hour to its precise resource focus and reading time.

The directory uses `catalog.json` for its ordered course inventory, topic tags, and project summaries; `catalog.py` renders it and `catalog.css` styles it. Titles, descriptions, colors, links, and duration totals come from each course's existing configuration and schedule. To add a course, create its source directory using the same schema and add an entry to `catalog.json`; no catalog HTML or grid changes are needed. Use one of the existing icon names, or add another to `catalog.py`. The build produces `courses/index.html` and `courses/catalog.css` alongside the course sites. Commit these generated files as well as the sources and course pages.

From the repository root, run:

```bash
python3 courses/_source/build.py
python3 courses/_source/verify.py
node courses/_source/verify-client.mjs courses/_source/course.js
```

Commit both the changed sources and generated `courses/<course>/` files. The existing GitHub Pages branch build publishes the generated HTML as static files. No new build service, account, API key, server, or database is required. This directory begins with an underscore so Jekyll excludes build sources from the published website while they remain available in GitHub.

Do not add a root `.nojekyll` file: the existing blog still uses Jekyll. The course HTML has no front matter and is copied without a template. Existing blog files and settings are unchanged.

## Progress

Checklists save in localStorage separately for each course. They do not sync between devices automatically. Export/import JSON provides portable backups, with strict course/record validation and timestamp-based merging, including explicit unchecked values. Archived check IDs are retained without contributing to current lesson totals. Storage failures are visible and do not claim a successful save.

No personal progress, credentials, or runtime data is committed. Videos use click-to-load, privacy-enhanced YouTube embeds; their original links remain available if embedding fails. Video alternatives replace the assigned reading block rather than adding homework.

## Verification — 2026-09-29

250 HTML pages, including the course directory; 5,442 local/cross-course links; 152 practical day pages; 176 one-hour practical steps. Every practical hour has focused verified resources inside its ten-minute reading allocation. The direct catalogs contain 103 distinct URLs and six selected video alternatives. Structural checks, resource coverage, day limits, and eight browser-progress regression scenarios pass. The public build does not run paid API experiments or students' GPU implementations.
