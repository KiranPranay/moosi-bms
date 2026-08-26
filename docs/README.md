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

- `bom.csv` — bill of materials, doubles as a procurement checklist
- `costing.csv` — running budget; the prices are **indicative placeholders**,
  replace them with real quotes
- `sld-placeholder.svg` — a clearly-marked placeholder single line diagram.
  Replace it with your own drawing and update the entry in `data.js`.

Anything referenced in `data.js` with `pending: true` has no file here yet —
it renders as a soft "not filed yet" placeholder rather than a broken link.
Delete that line once you commit the real file.
