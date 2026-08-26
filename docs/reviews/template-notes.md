# Review-deck template — extracted design system

The First Review deck has to look like the review decks the department already
uses. A classmate's Zeroth Review deck was shared as a formatting reference, and
the measurements below were taken from it: page size, fonts, colours, margins
and the college logo.

That file is not committed here. It is another team's work, and its title slide
lists four students by name with their roll numbers. This repository is public,
so only the layout measurements and the logo were taken from it. None of its
project content appears in our slides.

---

## Page geometry

| Property | Value |
| --- | --- |
| Page size | 960 × 540 pt = **13.333 in × 7.5 in** |
| Aspect ratio | **16:9** (PowerPoint "Widescreen") |

## Type

| Role | Font | Size | Style |
| --- | --- | --- | --- |
| Title-slide review label | Times New Roman | 18 pt | Bold, navy, centred |
| Title-slide project title | Times New Roman | 28 pt | Bold, black, centred |
| Title-slide body (names, guide) | Times New Roman | 18 pt | Regular; column heads bold |
| Content-slide heading | Times New Roman | 24 pt | **Bold + underlined**, centred |
| Content-slide body | Times New Roman | 16–18 pt | Regular, justified |
| Bullet glyph | Arial (`•`) | matches body | — |
| Footer | Calibri | 12 pt | Grey |

Bullets are a literal `•` in Arial at the left margin with the text indented
separately — reproduced here with a real PowerPoint bullet at the same indents.

**Font substitution on the build machine:** this Linux box has no Times New
Roman or Calibri. The `.pptx` stores the correct names (so PowerPoint renders
them properly); the LibreOffice QA render substitutes the metric-compatible
**Liberation Serif** and **Carlito**. Line breaks in the QA PDF therefore match
what PowerPoint will produce.

## Colour

| Token | Hex | Where |
| --- | --- | --- |
| `ACCENT_NAVY` | `#002060` | Title-slide review label |
| `TEXT_BLACK` | `#000000` | All headings and body |
| `FOOTER_GREY` | `#898989` | Footer date / label / slide number |
| `TABLE_BAND` | `#EDEDED` | Alternating literature-survey table rows |
| Background | `#FFFFFF` | Every slide — no title bar, no fill |

The template has **no coloured title bar**. Headings are plain centred,
underlined black text on white. Rules are horizontal only; the survey table has
no vertical gridlines.

## Layout (inches from the top-left corner)

| Element | Left | Top | Width | Height |
| --- | --- | --- | --- | --- |
| Logo | 0.313 | 0.120 | 0.707 | 1.040 |
| Content heading | centred | ≈0.42 | full | 0.55 |
| Body text block | 1.278 | ≈1.45 | 11.15 | to 6.75 |
| Footer baseline | — | 7.083 | — | — |
| Footer date (left) | 1.017 | 7.083 | — | — |
| Footer slide no. (right edge) | 12.317 | 7.083 | — | — |

Body left margin is 92 pt (bullet) / 114.5 pt (text) → 1.278 in / 1.590 in.
Body right edge is 895 pt → 12.43 in.

The logo sits above and left of the body block on every slide, including the
title slide. Nothing else appears in the header area.

## Zeroth-review slide order (for an accurate Recap slide)

1. Title
2. Contents
3. Abstract
4. Problem Statement **+** Objective (two headings on one slide)
5. Implementation Outline (Block Diagram / Flowchart)
6. Literature Survey (2-column table: *References* | *Summary of the work*)
7. References (IEEE-style, unnumbered bullets)

There is no section-divider slide and no closing "Thank You" slide in the
reference deck — the deck simply ends on References. Our deck adds a Thank You /
Q&A slide, which is the only structural addition.

## Footer convention

```
22-07-2026        Zeroth Review-2026-27 (Batch No: 15)        1
```

Left = export date, centre = `<Review name>-<academic year> (Batch No: N)`,
right = slide number. Our deck follows the same pattern with
`First Review-2026-27`; the batch number is omitted until it is known.

## Logo

Cropped from a 600 dpi render of page 2 and saved to
[`assets/logo.png`](assets/logo.png) (448 × 648 px, white made transparent).
Not downloaded from the web.
