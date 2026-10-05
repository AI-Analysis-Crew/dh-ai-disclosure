# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website for a Digital Humanities research project on generative AI disclosure. Hosted on GitHub Pages as a project page at `https://ai-analysis-crew.github.io/dh-ai-disclosure/` (repo `AI-Analysis-Crew/dh-ai-disclosure`), i.e. under the `/dh-ai-disclosure/` subpath, not the domain root. No build system, bundler, or package manager — just plain HTML, CSS, and vanilla JavaScript.

## Git Workflow

Three branches promoted in order: `dev` → `stage` → `main`. All work happens on `dev`. The promotion command is in `bash/update-master-bash-code.txt` — it merges dev into stage, then stage into main, and pushes all three.

## Architecture

**Pages:** `index.html` (root), `html/survey.html`, `html/graphs-analysis.html`, `html/accessibility.html`

**Shared components:** `common/nav.html` and `common/footer.html` are loaded at runtime via `fetch()` into `<div data-include="nav">` / `<div data-include="footer">` elements. Each page has its own inline `<script>` that handles this inclusion and rewrites relative paths. The `basePath` variable differs per page (`'./'` for root, `'../'` for pages in `html/`).

**Styles:** Single stylesheet `css/style.css`. Uses a dark-mode color palette (Deep Slate background, cyan/blue text) designed for AAA accessibility (7:1+ contrast ratios). When updating CSS, increment the `?vers=` cache-busting parameter in all HTML files that reference it (currently `index.html`, `html/survey.html`, `html/graphs-analysis.html`, `html/accessibility.html`).

**Visualizations:** Interactive charts in `graphs/` are standalone HTML files (Plotly.js). The Sankey diagram on the homepage uses `js/sankey_data.js` rendered via Plotly CDN, with CSS transform scaling for narrow viewports (no static PNG fallback).

**Images:** Source images in `jpg/`, responsive variants in `jpg/responsive/`. Generated via ImageMagick (`scripts/generate-responsive-images.sh`).

## Key Conventions

- All paths in HTML must be relative (not root-absolute like `/css/...`), because the live site is served from the `/dh-ai-disclosure/` subpath. Root-absolute paths resolve to the domain root and 404 there (tried in commit 33dc780, which broke the live site). Relative paths also work in VS Code Go Live.
- Nav link hrefs in `common/nav.html` are written relative to root (no leading slash); the inclusion script rewrites them based on each page's `basePath`
- `common/nav.html` and `common/footer.html` versioning: bump `?vers=` in the fetch URL when these change, in all four pages (`index.html`, `html/survey.html`, `html/graphs-analysis.html`, `html/accessibility.html`)
- External libraries loaded via CDN with SRI hashes (Font Awesome, Google Fonts, Plotly.js)
- Fonts: Noto Serif (headings), Source Sans Pro (body)
- **Touch-aware hover for Plotly graphs:** All interactive Plotly charts (homepage and `html/graphs-analysis.html`) must detect device capability via `window.matchMedia('(any-hover: hover)')`. On hover-capable devices, use standard Plotly hover events (`plotly_hover`/`plotly_unhover`). On touch-only devices, set `layout.hovermode = false` and use `plotly_click` with tap-to-toggle behavior, displaying info in a visible panel (class `sankey-touch-info`, `q8-touch-info`, or similar) instead of tooltips. See the Q8 network graph script for the reference implementation.
- **Data tables for graphs:** every graph on `html/graphs-analysis.html` has a data table. The markup is a `<button class="data-table-btn" aria-controls="dt-...">` followed by `<div class="sr-only" id="dt-...">` holding a `<p class="data-table-caption">` and the `<table>`. The tables stay in the screen-reader reading order while hidden, and the button shows them on screen. The caption is a `<p>` outside the table (not a `<caption>`); the ids `q6-sr-caption`, `q13-sr-caption`, `q14-sr-caption` and `q15-sr-caption` are rewritten by script when a filter changes (so the population shown stays correct), so keep them. Captions follow the pattern "Survey responses on [subject] ([population], n=N)" and use "GenAI"; n is `TBD` for Q14, Q15 and the heatmap until the respondent counts are confirmed. A button can control several wrappers (Q8 lists two ids in `aria-controls`). The page script at the end of `html/graphs-analysis.html` wraps each table in a `.data-table-block` and draws the scroll bars above and below it, because Firefox hides its own overlay scroll bars. Give tables with many columns `class="data-table-wide"` so they keep a minimum column width on phones and scroll sideways. A table's bottom spacing is `margin-bottom: 2rem` on `.data-table-block` (not on the table), so it merges with the next element's margin instead of stacking.
