# Notes for Q14 Stacked Bar Chart (Carry-Over)

## Lessons Learned from Q13 Implementation

### Styling conventions established across all charts
- **Text color**: All Plotly layout fonts must use `color: 'black'` explicitly (Plotly defaults to `#444` gray otherwise)
- **Label boxes**: White background, black text (`#1a1a1a`), `border: 1px solid black`, `border-radius: 3px`, `padding: 4px 8px`, font `Source Sans Pro`, size 16px, no bold
- **Connecting lines** (for outside labels): `stroke="black" stroke-width="1.5"`, dot at slice end `r="3" fill="black"`
- **Hover tooltips**: Custom HTML tooltip (`.q13-hover-tooltip`) positioned at mouse, white background, black text, `border: 1px solid #5AAFE0`
- **Inside label boxes**: SVG rects inserted before text in `.pielayer .slicetext` groups, white fill, black stroke

### Filter controls
- **Breakpoint**: Filters go side-by-side at >= 860px, stacked below that (was 768px, changed because filters overflowed the page)
- **Font sizes**: Labels at `1.1rem` (do NOT reduce), select display text at `0.95rem` with `padding: 0.5rem 0.75rem` (do NOT reduce), dropdown options at `0.85rem`
- **Browser limitation**: `<option>` elements ignore `font-family` CSS and render in system default font — leave as-is
- Q14 shares the Q13 filter controls (no new filter HTML needed)

### Responsive scaling approach
- Charts have a fixed width (1000px for Q13) and use CSS `transform: scale()` on the **scaler** wrapper div when viewport < 1000px
- **Key**: Transform the `.q13-chart-scaler` (not `#q13-chart` directly) so that legend, outside labels, and chart all scale together as one unit
- Scaler CSS: `width: 1000px; overflow: visible; position: relative; transform-origin: top left;`
- Container CSS: `overflow: hidden;` (clips the overflowing scaler)
- JS `scaleQ13Chart()` sets `scaler.style.transform = 'scale(' + scale + ')'` and `container.style.height` for proper flow
- **Known trade-off**: CSS transform scaling causes slight text fuzziness at small viewports. Accepted — not worth fixing with `zoom` due to potential side effects.
- The Q6 and Q8 charts scale only the chart div (not the scaler), because they don't have outside HTML labels/legends that need to scale with the chart

### Empty state handling
- When a filter combination produces zero results (`totalResponses === 0`), show an SVG circle outline with "Option not selected" label in a white box
- Uses actual container dimensions via `offsetWidth`/`offsetHeight`, pie centered at 61% width
- Text fill must be `#1a1a1a` (not white) on the `#f5f5f5` background

### Outside labels for small slices
- Slices below `smallSliceThreshold` (0.05 = 5%) get HTML div labels positioned outside the pie
- `addQ13SmallSliceLabels()` uses `getBoundingClientRect()` to find slice positions and compute label placement
- Labels appended to `chartEl.parentNode` (the scaler), NOT to `chartEl` — moving them inside the chart div breaks coordinate math because `getBoundingClientRect()` returns viewport-relative coordinates that don't account for the chart's CSS transform
- `labelDist` controls how far the label sits from the slice (currently ~145px, user adjusted from 120)
- Labels, lines, and chart all scale together because the scaler is the transformed element

### Q13 chart-specific details
- Pie domain: `{ x: [0.22, 1] }` — offsets pie rightward to leave room for the HTML legend
- Legend: HTML `<ul class="q13-legend">` with `position: absolute; left: 170px; top: 50%; transform: translateY(-50%)`
- Zero-value slices are filtered out before passing to Plotly (prevents phantom slices)
- `textposition: 'inside'`, `textinfo: 'label+percent'`, `insidetextorientation: 'horizontal'`
- SVG label background boxes added in `.then()` callback via `addQ13LabelBoxes()`

### CSS version
- Currently at `?vers=040` in `graphs-analysis.html`
- Bump when making CSS changes

---

## What was done for Q13

- Q13 pie chart integrated into "Does Context Matter for AI Disclosure?" section of `html/graphs-analysis.html`
- CSS added to `css/style.css` under "Q13/Q14 CONTEXT CHARTS" section comment (after Q6 touch-info, before Sankey section)
- Filter controls added with `q13-` prefix (shared between Q13 and Q14)
- Script block added as IIFE between Q6 script and sankey_data.js load
- `allData` already contains BOTH `q13_dist` AND `q14_by_q13` for every filter combination
- `q14Labels` and `q13Colors` already defined in the script block
- Custom HTML hover tooltip (not Plotly's built-in) for reliable positioning
- Touch-aware: hover-capable devices use plotly_hover/plotly_unhover with highlight; touch devices use plotly_click with info panel

---

## What needs to happen for Q14

### 1. CSS additions needed (in `css/style.css`)

Add after `.q13-touch-info` block, before the Sankey section:

```css
.q14-chart-container    -- same pattern as .q13-chart-container (overflow: hidden, breakout at 1000px)
.q14-chart-scaler       -- width: 1000px, overflow: visible, position: relative, transform-origin: top left
#q14-chart              -- 1000px wide, 600px height (taller than Q13 for 8 horizontal bars)
.q14-touch-info         -- same as .q13-touch-info
```

**Important**: Apply the transform to `.q14-chart-scaler` (not `#q14-chart`) so all content scales together.

### 2. HTML additions (in `html/graphs-analysis.html`)

Insert AFTER the Q13 sr-only table and BEFORE the `<section aria-labelledby="read-3">` line:

- Q14 chart container: `.q14-chart-container` > `.q14-chart-scaler` > `#q14-chart`
  - `role="img"` with descriptive aria-label listing all Q14 options and their totals
- Q14 sr-only table with cross-tabulation data (Q14 options x Q13 responses)

No filter controls needed — Q14 shares the existing Q13 filter dropdowns.

### 3. Script changes

Extend `updateQ13Charts()` to also render the Q14 stacked bar chart. The function already has access to `allData`, `q14Labels`, `q13Labels`, and `q13Colors`.

Q14 chart details from dev source:
- Type: horizontal stacked bar (`barmode: 'stack'`, `orientation: 'h'`)
- Y-axis: 8 Q14 option labels (reversed order), using `q14Labels`
- X-axis: "Number of Respondents"
- One trace per Q13 category (6 traces), colored by `q13Colors`
- Bar width: 0.5
- Annotations: total count at end of each bar (`xanchor: 'left'`, `xshift: 5`)
- Desired order: ['1','2','3','4','5','6','7','8'] reversed for display
- **Layout font must include `color: 'black'`** (don't rely on Plotly default)

Layout adaptations for light-bg chart area (#f5f5f5):
- `plot_bgcolor: 'rgba(0,0,0,0)'`, `paper_bgcolor: 'rgba(0,0,0,0)'`
- Axis title/tick colors: use black (matching Q13 style inside chart area)
- Annotation font color: black
- Legend font color: match page dark-mode if legend is outside chart, or black if inside
- Margin: `{ t: 20, b: 100, l: 280, r: 180 }` (large left margin for long Q14 labels)
- `displayModeBar: false`

Touch-aware hover:
- Desktop: standard Plotly hover with custom hovertemplate
- Touch: tap-to-toggle with `.q14-touch-info` panel, track `q14ActiveBar` state

Responsive scaling:
- Add `scaleQ14Chart()` following the scaler-transform pattern (transform the scaler, not the chart div)
- Call from `updateQ13Charts()` and on window resize

### 4. Post-integration

- Bump CSS version (`?vers=` in graphs-analysis.html)
- The "How to Read This Graph" section already describes both charts — no changes needed
- The "Graph Analysis" section still says "Coming soon!" — leave as-is

### 5. Q14 default data (all respondents)

From allData["Q2"]["all"]["q14_by_q13"]:
- Conference presentations (1): total ~61
- Publications (2): total ~72
- Project documentation (3): total ~60
- Websites/DH projects (4): total ~57
- Creative works (5): total ~70
- Grant applications (6): total ~53
- Other (7): total ~6
- Prefer not to answer (8): total ~3
