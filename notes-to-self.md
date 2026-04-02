# Notes for Q14 Stacked Bar Chart Carry-Over

## What was done for Q13

- Q13 pie chart integrated into "Does Context Matter for AI Disclosure?" section of `html/graphs-analysis.html`
- CSS added to `css/style.css` under "Q13/Q14 CONTEXT CHARTS" section comment (after Q6 touch-info, before Sankey section)
- Filter controls added with `q13-` prefix (shared between Q13 and Q14)
- Script block added as IIFE between Q6 script and sankey_data.js load
- `allData` already contains BOTH `q13_dist` AND `q14_by_q13` for every filter combination
- `q14Labels` and `q13Colors` already defined in the script block
- CSS version bumped to `?vers=032`

## What needs to happen for Q14

### 1. CSS additions needed (in `css/style.css`)

Add after `.q13-touch-info` block, before the Sankey section:

```css
.q14-chart-container    -- same pattern as .q13-chart-container
.q14-chart-scaler       -- overflow: hidden
#q14-chart              -- 1000px wide, 600px height (taller than Q13 for 8 horizontal bars)
                           tablet: 550px height
                           mobile: 768px fixed width, transform-origin top left
.q14-touch-info         -- same as .q13-touch-info
```

### 2. HTML additions (in `html/graphs-analysis.html`)

Insert AFTER the Q13 sr-only table and BEFORE the `<section aria-labelledby="read-3">` line:

- Q14 chart container: `.q14-chart-container` > `.q14-chart-scaler` > `#q14-chart`
  - `role="img"` with descriptive aria-label listing all Q14 options and their totals
- Q14 sr-only table with cross-tabulation data (Q14 options x Q13 responses)

No filter controls needed -- Q14 shares the existing Q13 filter dropdowns.

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

Layout adaptations for dark theme:
- `plot_bgcolor: 'rgba(0,0,0,0)'`, `paper_bgcolor: 'rgba(0,0,0,0)'`
- Axis title/tick colors: light color (#A8D5E2 or #E0E0E0)
- Annotation font color: light (#A8D5E2) instead of #333
- Legend font color: #A8D5E2
- Margin: `{ t: 20, b: 100, l: 280, r: 180 }` (large left margin for long Q14 labels)
- `displayModeBar: false`

Touch-aware hover:
- Desktop: standard Plotly hover with custom hovertemplate
- Touch: tap-to-toggle with `.q14-touch-info` panel, track `q14ActiveBar` state

Responsive scaling:
- Add `scaleQ14Chart()` function following same pattern as `scaleQ13Chart()`
- Call from `updateQ13Charts()` and on window resize

### 4. Post-integration

- Bump CSS version to `?vers=033`
- The "How to Read This Graph" section already describes both charts -- no changes needed
- The "Graph Analysis" section still says "Coming soon!" -- leave as-is

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
