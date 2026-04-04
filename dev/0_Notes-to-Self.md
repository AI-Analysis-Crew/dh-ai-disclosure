# Notes for Graph Implementations (Carry-Over)

## Lessons Learned from Q13 & Q14 Implementation

### Styling conventions established across all charts
- **Text color**: All Plotly layout fonts must use `color: 'black'` explicitly (Plotly defaults to `#444` gray otherwise).
- **Label boxes**: White background, black text (`#1a1a1a`), `border: 1px solid black`, `border-radius: 3px`, `padding: 4px 8px`, font `Source Sans Pro`, size 16px, no bold.
- **Connecting lines** (for outside labels): `stroke="black" stroke-width="1.5"`, dot at slice end `r="3" fill="black"`.
- **Hover tooltips**: Custom HTML tooltip (`.q13-hover-tooltip`) positioned at mouse, white background, black text, `border: 1px solid #5AAFE0`.
- **Inside label boxes**: SVG rects inserted before text in `.pielayer .slicetext` groups, white fill, black stroke.

### Filter controls & Spacing
- **Breakpoint**: Filters go side-by-side at >= 860px, stacked below that (changed from 768px because filters overflowed the page).
- **Responsive Spacing**: Under 600px, filter containers require a negative bottom margin (e.g., `margin-bottom: -1.5rem;` for Q13, `-1rem;` for Q6) to pull the graph upward and maintain consistent vertical spacing.
- **Font sizes**: Labels at `1.1rem` (do NOT reduce), select display text at `0.95rem` with `padding: 0.5rem 0.75rem` (do NOT reduce), dropdown options at `0.85rem`.
- **Browser limitation**: `<option>` elements ignore `font-family` CSS and render in system default font — leave as-is.

### Plotly Layout Quirks (Crucial for future charts)
- **Grid Legends**: Native Plotly legends don't auto-wrap neatly into grids without spacing hacks. To force a permanent, clean grid (like Q14's 3x2), use multiple independent legends (`legend` and `legend2`). Assign traces to them conditionally (`legend: (t < 3) ? 'legend' : 'legend2'`) and use matching `x` but staggered `y` coordinates.
- **Automargins vs. Padding**: When `automargin: true` is enabled on the y-axis (to accommodate long text labels), setting `margin.l` acts as a *minimum*. To add actual visual padding between the left edge of the white box and the text, `margin.l` must be explicitly *larger* than the width of the longest label (e.g., `l: 240`).
- **Axis Lines**: Never use hardcoded `shapes` to draw vertical/horizontal axis boundaries. They break when domains change. Instead, use `showline: true`, `linecolor: 'black'`, and `linewidth: 1` directly on the `xaxis` or `yaxis` objects so they snap naturally to the labels.
- **Preventing Auto-Shrinking Labels**: If a chart has many items (like Q15's 15 bars), Plotly will aggressively auto-shrink multiline y-axis labels to prevent overlap. To prevent this, force the size explicitly (`yaxis: { tickfont: { size: 16 } }`) AND mathematically calculate the CSS `#chart` height to ensure each bar gets enough vertical pixels (e.g., ~62px per slot).
- **Right-Aligning Multiline Labels**: Plotly struggles to perfectly right-align multiline y-axis labels against the axis line. To force alignment and add padding, split the label at the `<br>` and inject non-breaking spaces: `entry.label.split('<br>').join('\u00A0\u00A0\u00A0\u00A0<br>') + '\u00A0\u00A0\u00A0\u00A0'`.

### Responsive scaling approach
- Charts have a fixed width (e.g., 1000px) and use CSS `transform: scale()` on the **scaler** wrapper div when viewport < 1000px.
- **Key**: Transform the `.chart-scaler` (not the chart div directly) so that HTML legends, outside labels, and the SVG chart all scale together as one unified element.
- Scaler CSS: `width: 1000px; overflow: visible; position: relative; transform-origin: top left;`
- Container CSS: `overflow: hidden;` (clips the overflowing scaler).
- JS scaling sets `scaler.style.transform = 'scale(' + scale + ')'` and `container.style.height` for proper document flow.
- **Known trade-off**: CSS transform scaling causes slight text fuzziness at small viewports. Accepted — not worth fixing with `zoom` due to potential side effects.

### Empty state handling
- When a filter combination produces zero results (`totalResponses === 0`), show an SVG outline with "Option not selected" label in a white box.
- Uses actual container dimensions via `offsetWidth`/`offsetHeight`.
- Text fill must be `#1a1a1a` (not white) on the `#f5f5f5` background.

### Q13/Q14 Context Section Specifics
- **Q13 Small Slices**: Slices below `smallSliceThreshold` (5%) get HTML div labels positioned outside the pie. `addQ13SmallSliceLabels()` uses `getBoundingClientRect()` to compute placement. Labels are appended to the scaler, NOT the chart div, so coordinates align.
- **Q14 Bar Alignment**: Uses a stacked horizontal bar chart (`barmode: 'stack'`, `orientation: 'h'`).
- **Q14 Data Linking**: The Q14 chart rebuilds dynamically using `allData["Q2"]["all"]["q14_by_q13"]` without needing its own separate filter UI.
- Both charts share a touch-aware configuration: hover-capable devices use `plotly_hover` with highlights; touch devices use `plotly_click` with a custom `.touch-info` DOM panel.
### Accessibility & Dynamic SR-Only Tables
- **JavaScript Scoping**: When writing logic to dynamically rebuild a `.sr-only` `<tbody>` after a filter change, the update loop **must** sit outside the `if (hasHover) { ... } else { ... }` interactive blocks. If trapped inside the touch-device `else` block, desktop screen reader users will not receive updated data.
- **Cleaning Labels**: Strip out HTML tags (`<br>`) and non-breaking spaces (`\u00A0`) from the Plotly labels before injecting them into the screen reader table using `.replace(/<br>/g, ' ').replace(/\u00A0/g, '').trim()`.

### CSS Versioning
- Currently at `?vers=041` in `graphs-analysis.html`.
- Always bump `vers` query parameter when making CSS/JS changes to clear browser cache.

---

## Next Steps: Q15 / Q21 Heatmap (Practice vs. Principles)

### Upcoming Tasks
- **Chart Type**: Heatmap (`type: 'heatmap'`).
- **HTML Container**: Needs `.heatmap-filter-container`, `.heatmap-chart-container`, `.heatmap-chart-scaler`, `#heatmap-chart`, and `.heatmap-touch-info` (do not reuse `.q15-` classes to avoid colliding with the standalone activities chart).
- **SR-Only Table**: Will need a complex grid structure `<th>` for rows and columns.
- **Interactivity requirement**: Needs checkboxes to filter specific activities (rows/columns) in addition to the standard demographic dropdown filters.
- **Color Scale**: Will require a custom colorscale representing "alignment" (darker = stronger alignment, lighter = weaker alignment).
