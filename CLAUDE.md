# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website for a Digital Humanities research project on generative AI disclosure. Hosted on GitHub Pages at `https://dh-ai-disclosure.github.io/`. No build system, bundler, or package manager — just plain HTML, CSS, and vanilla JavaScript.

## Git Workflow

Three branches promoted in order: `dev` → `stage` → `main`. All work happens on `dev`. The promotion command is in `bash/update-master-bash-code.txt` — it merges dev into stage, then stage into main, and pushes all three.

## Architecture

**Pages:** `index.html` (root), `html/survey.html`, `html/graphs-analysis.html`

**Shared components:** `common/nav.html` and `common/footer.html` are loaded at runtime via `fetch()` into `<div data-include="nav">` / `<div data-include="footer">` elements. Each page has its own inline `<script>` that handles this inclusion and rewrites relative paths. The `basePath` variable differs per page (`'./'` for root, `'../'` for pages in `html/`).

**Styles:** Single stylesheet `css/style.css`. Uses a dark-mode color palette (Deep Slate background, cyan/blue text) designed for AAA accessibility (7:1+ contrast ratios). When updating CSS, increment the `?vers=` cache-busting parameter in all HTML files that reference it (currently `index.html`, `html/survey.html`, `html/graphs-analysis.html`).

**Visualizations:** Interactive charts in `graphs/` are standalone HTML files (Plotly.js). The Sankey diagram on the homepage uses `js/sankey_data.js` rendered via Plotly CDN, with a static PNG fallback (`png/sankey-diagram.png`) for mobile.

**Images:** Source images in `jpg/`, responsive variants in `jpg/responsive/`. Generated via ImageMagick (`scripts/generate-responsive-images.sh`).

## Key Conventions

- All paths in HTML must be relative (not absolute) for GitHub Pages subdirectory hosting compatibility
- Nav link hrefs in `common/nav.html` are written relative to root; the inclusion script rewrites them based on each page's `basePath`
- `common/nav.html` and `common/footer.html` versioning: bump `?vers=` in the fetch URL when these change
- External libraries loaded via CDN with SRI hashes (Font Awesome, Google Fonts, Plotly.js)
- Fonts: Noto Serif (headings), Source Sans Pro (body)
- **Touch-aware hover for Plotly graphs:** All interactive Plotly charts on `html/graphs-analysis.html` must detect device capability via `window.matchMedia('(any-hover: hover)')`. On hover-capable devices, use standard Plotly hover events (`plotly_hover`/`plotly_unhover`). On touch-only devices, set `layout.hovermode = false` and use `plotly_click` with tap-to-toggle behavior, displaying info in a visible panel (class `q8-touch-info` or similar) instead of tooltips. See the Q8 network graph script for the reference implementation.
