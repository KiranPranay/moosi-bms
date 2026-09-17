# docs/

Everything filed in the tracker lives here. Drop a file in this folder, add an
entry for it in `../data.js`, commit and push — it shows up for everyone.

```js
// in data.js, inside a phase:
docs: [
  { id: "p2-doc-quotes", title: "Supplier Quotes", file: "./docs/quotes.pdf" },
],
```

## What each file type does

| Extension | Behaviour in the panel |
| --- | --- |
| `.csv` | Rendered as a real table. Add `totalColumn: "Amount (INR)"` to sum a column. |
| `.png` `.jpg` `.svg` `.webp` `.gif` | Previews inline. |
| `.pdf` | Previews inline, plus opens in a new tab. |
| `.pptx` `.docx` `.xlsx` `.stp` `.zip` … | Downloads. |
| a `url:` instead of `file:` | Opens in a new tab. |

## Files currently here

- `current-architecture.md` — authoritative design envelope, wiring, pin map,
  thresholds, failure behaviour and source links
- `current-architecture.svg` — current power/protection/sensing architecture
- `safe-build-sequence.md` — twelve build gates with pass and stop criteria
- `bom.csv` — redesigned procurement checklist, including add/keep/remove actions
- `costing.csv` — full replacement-cost budget with a confidence label on every
  price; owned stock remains costed and shipping and lab tools are excluded
- `sld-placeholder.svg` — obsolete placeholder retained only as an unused archive

The first-review diagrams are historical. Do not use them as construction
instructions; the `current-architecture.*` files are the build authority.

Anything referenced in `data.js` with `pending: true` has no file here yet —
it renders as a soft "not filed yet" placeholder rather than a broken link.
Delete that line once you commit the real file.
