# Doranalytics brand guidelines

Version 1 · October 6, 2026

## Direction and status

A Florentine palette inspired by shutters, plaster, gilding, and Renaissance architecture, expressed through precise technical graphics. All four chart palette options below were approved by Brian as a set to retain. All five font pairings are approved options. Usage defaults are recommendations rather than a requirement to select one permanent font.

## Color palettes

Hex values are the source of truth. Keep each set intact when reproducing the examples.

| Token | Florentine original | Sharper light | Phthalo luminous | Ink Florentine |
|---|---|---|---|---|
| Surface | #F3EDE1 | #F3EDE1 | #082E28 | #20231F |
| Text | #20231F | #20231F | #F3EDE1 | #F3EDE1 |
| Secondary text | #685F52 | #685F52 | #B6C8BD | #C2BBAE |
| Grid / border | #D8D0C1 | #D8D0C1 | #31534A | #45483F |
| Series 1 | #103F35 | #08745C | #35E8B5 | #35E8B5 |
| Series 2 | #B99A58 | #A52F50 | #FFC247 | #FFC247 |
| Series 3 | #6B303D | #4655BB | #F47798 | #F47798 |
| Series 4 | #88715B | #B97808 | #9BAAFF | #9BAAFF |

Florentine original: editorial, website, warm charts. Sharper light: daylight technical dashboards. Phthalo luminous: signature dark technical graphics. Ink Florentine: neutral dark alternative. These are options, not a requirement to use all four in one product. The luminous accents are designed for dark surfaces; use the light sets on cream.

## Typography — Cortex pairing

- Orbitron 500 and 700: wordmark-like treatments, short titles, section headings, technical display headlines. Sentence/title case by default. Use sparingly; wide letters need room. Avoid long paragraphs, chart ticks, and dense navigation.
- Geist 400, 500, 600: paragraphs, chart labels, tooltips, controls, legends. This is the everyday reading face.
- Geist Mono 400 and 500: measurements, code, timestamps, tables of numbers, compact metadata. Use tabular figures on aligned values. Do not put whole explanatory paragraphs in monospace.
- Retain an editorial serif as an optional website treatment; no new serif is finalized in this version.

Suggested web sizes: display 32–48 px, short section titles 20–24 px, chart titles 16–18 px, body 15–16 px, chart labels 12–14 px. Adapt for the actual viewing size. For social video, test at phone size and use substantially larger labels.

Load via next/font/google in Next.js; use a font stylesheet or self-hosted font files in other environments. Fallbacks must be specified. The included browser specimen loads Google Fonts and the preview requires network access for fonts and chart libraries.

## Charts

Five preserved examples: acquisition lines, stacked install bars, revenue area, traffic-share donut, channel conversion bars. Sample data is synthetic, not actual business performance.

Keep color mappings stable within a dashboard. Pair color with names and line patterns. Organic is solid and paid is dashed in the line example. Use faint neutral grids, explicit units, readable labels, and restrained fills; inspect real data rather than assuming every combination is accessible. Never claim dollars and counts are interchangeable: separate scales or separate panels when needed. Distinguish zero from missing data.

Use Orbitron for short chart titles only; Geist for labels and Geist Mono for numerical summaries. Do not recolor axis labels with series colors. Preview at narrow widths before publishing.

## Composition

Thin borders, 10–12 px corners, little or no shadow, deliberate spacing. Prefer flat surfaces and purposeful motion. Use gold selectively; no default metallic gradients. Renaissance influence comes from hue and proportion rather than ornamental frames or aged textures everywhere.

For Instagram at 1080×1920, preserve essential information within x=35–980 and y=220–1470, with breathing room; validate actual frames using the exclusion overlay. Preserve existing presenter framing and applicable workspace video instructions.

## Saved examples and implementation

- index.html: browser specimen and all four selectable palettes / five charts. Runs from a local server or file with network access; not published.
- tokens.css: reusable palette and typography variables.
- examples/BrandCharts.jsx and examples/brand-charts.css: React implementation importing actual shadcn Card and ChartContainer components. Add card and chart to an initialized shadcn project before use. React, Recharts, Tailwind, and the normal @ alias are expected. Import tokens.css and load fonts in the host application.
- The browser preview uses the same chart definitions with lightweight container adapters; it is not a complete shadcn application build.

## Font pairing explorer

The saved browser preview has independent palette and font selectors. Five approved pairing options are available; no single pairing is required across all content.

| Pairing | Display | Body / labels | Data |
|---|---|---|---|
| Cortex futuristic | Orbitron | Geist | Geist Mono |
| Technical editorial | Space Grotesk | Geist | Geist Mono |
| Geometric modern | Sora | Geist | Geist Mono |
| Research journal | IBM Plex Sans | IBM Plex Sans | IBM Plex Mono |
| Renaissance editorial | Newsreader | Geist | Geist Mono |

For data essays, compare Space Grotesk as the everyday heading face, Orbitron for short technical hooks, and Newsreader for reflective editorial openings. Keep body text and labels clear. The dropdown updates specimens, chart headings, body text, and numerical typography together.

## Animation, video overlays, and interchangeable styles

Brian approved retaining all five font pairing options alongside all four palettes. They are available across charts, data essays, animation, and video overlays; no single font is mandatory for every piece.

| Font | Recommended use |
|---|---|
| Orbitron | Short technical hooks, product reveals, futuristic animation |
| Space Grotesk | Everyday video titles, charts, explanatory overlays; suggested workhorse |
| Sora | Product walkthroughs and clean motion graphics |
| IBM Plex Sans / Mono | Detailed data essays, research, analytical breakdowns |
| Newsreader | Editorial openings, storytelling, reflective essays |

### Swapping styles

Switch pairings between pieces or at deliberate section boundaries. Keep a consistent pairing within a chart or scene. Preserve stable series colors and category meanings throughout a piece, even when typography changes. All saved palette/font combinations are exploratory tools; inspect contrast and composition before final delivery.

Changing a font requires checking line breaks, width, weight, and visual hierarchy. Orbitron needs room for wide letterforms; Newsreader needs sufficient size and weight to preserve fine details. Do not assume a dropdown swap produces a finished video layout. Preserve body and data font roles from the selected pairing.

### Motion and overlays

Use larger type, stronger weights, and fewer words for phone viewing. Prefer purposeful reveals, chart builds, and restrained transitions that follow the explanation. Keep quantitative marks accurate while animating; hold important results long enough to read. Review entry, middle, and exit frames, including presenter movement and foreground masking.

Use the existing Instagram safe rectangle and original presenter-framing rules above. Preserve approved titles, cuts, speed, and audio during visual-only revisions. For this workspace's video edits, the persistent title remains the only added text unless Brian explicitly requests other text. Use image overlays; preserve genuine chart and screenshot text, and do not use word cards or text rendered into PNGs to bypass the rule. Apply the project's design and spoken-cue timing workflows when producing actual overlays.

Suggested defaults: Space Grotesk for routine explanations, Orbitron for occasional short technical emphasis, and Newsreader for editorial character. The shared Florentine color system supplies continuity across these styles.
