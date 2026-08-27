# Predictive BMS Tracker 🌻

A small, unhurried project tracker for the **Predictive BMS** build — six phases,
a handful of tasks each, and a progress bar that fills up as they get ticked off.
Open any card and you get that phase's notes and its documents: the abstract, the
Phase 0 deck, the bill of materials, the costing sheet, the single line diagram.
Spreadsheets render as real tables, diagrams and PDFs preview in place.

It is a single static page: plain HTML, vanilla ES modules, and Tailwind via the
Play CDN. No build step, no `npm install`, no bundler. Serve the folder and it
works. Ticked tasks and personal notes are remembered in the browser's
`localStorage`, so they survive reloads without any server or account.

---

## How to edit progress globally

Local ticks live in the visitor's own browser. To mark something complete **for
everyone**, hardcode it in [`data.js`](data.js):

```js
{ id: "p1-synopsis", title: "Synopsis", done: true },   // ← was false
```

Commit and push. That task now renders as checked, **disabled**, and tooltipped
"Marked complete 🌻" for every visitor, regardless of what is in their
`localStorage`. Setting it back to `false` releases it again, and each visitor
falls back to their own local checkbox state.

### The ID rule

> **Never change a task's `id`. Change titles freely.**

Saved progress is keyed on `id`, not on title. Renaming
`title: "Synopsis"` → `title: "Project Synopsis"` keeps every tick intact.
Renaming `id: "p1-synopsis"` → `id: "p1-project-synopsis"` silently orphans it,
and the task reappears unticked for everyone who had already completed it.

IDs are kebab-case and prefixed with their phase number (`p4-cutoff`) so they
stay readable and collision-free. The same rule applies to document ids.

---

## Documents

Drop the file in [`docs/`](docs/), then add an entry for it in `data.js`.

```js
// a file in this repo
{ id: "p2-doc-quotes", title: "Supplier Quotes", file: "./docs/quotes.pdf" },

// or a link to somewhere else
{ id: "doc-live-bom", title: "Live BOM", url: "https://docs.google.com/..." },
```

Entries can go in three places:

| Where | What it's for |
| --- | --- |
| `PROJECT_DOCS` | Spans the whole build — abstract, BOM, costing, SLD. Shown in the **Project documents** card. |
| a phase's `docs: []` | Belongs to that phase. Shown when you open that card. |
| a task's `docs: []` | Belongs to one task. Shown in its phase's panel, labelled with the task. |

A phase can also point at a project-wide document with
`docRefs: ["doc-bom", "doc-costing"]` — it then appears under **Related
documents** on that card without being duplicated in `data.js`.

### What each file type does

The viewer is chosen from the file extension, so a `.csv` just works:

| Extension | Behaviour |
| --- | --- |
| `.csv` `.tsv` | Rendered as a real table, with numeric columns right-aligned |
| `.png` `.jpg` `.svg` `.webp` `.gif` | Previews inline |
| `.pdf` | Previews inline, and opens in a new tab |
| `.pptx` `.docx` `.xlsx` `.stp` `.stl` `.zip` … | Downloads |
| a `url:` instead of `file:` | Opens in a new tab |

Optional fields on any document:

```js
{
  id: "doc-costing",
  title: "Costing Sheet",
  file: "./docs/costing.csv",
  note: "One line of context shown under the title.",
  kind: "pdf",                  // override the inferred viewer
  totalColumn: "Amount (INR)",  // .csv only: sum this column into a total row
  pending: true,                // not filed yet — renders as a soft placeholder
}
```

`pending: true` is how you list something you haven't produced yet: it shows a
muted "Not filed yet" chip instead of a link that 404s. Delete the line once you
commit the real file.

---

## Notes

Two kinds, side by side in every phase panel:

- **Yours**, written in `data.js` as `notes: ["…", "…"]` on a phase. Pushed with
  the code, read-only, the same for everyone.
- **Theirs**, typed into the panel and saved to `localStorage`. Private to that
  browser, autosaved as you type, and **kept by "Reset my progress"** — a reset
  clears ticks, not notes.

---

## Review decks

The presentations for each review are built from code, so the diagrams and the
slides stay in step with each other.

```
docs/reviews/
├── deck_common.py               slide layout, shared by both decks
├── diagram_style.py             colours and type, shared by all figures
├── template-notes.md            the measurements the decks follow
├── assets/logo.png              college logo, cropped from a printed deck
├── zeroth-review/
│   ├── Predictive_BMS_Zeroth_Review.pptx / .pdf
│   ├── build_slides.py
│   └── diagrams/                block diagram, firmware flowchart
└── first-review/
    ├── Predictive_BMS_First_Review.pptx      edit this in PowerPoint
    ├── Predictive_BMS_First_Review.pdf       the version to hand in
    ├── build_slides.py                       builds the pptx
    ├── requirements.txt
    ├── research-notes.md                     sources behind the numbers
    └── diagrams/                             one script per figure
```

To rebuild a deck from scratch:

```bash
python3 -m venv .venv
.venv/bin/pip install -r docs/reviews/first-review/requirements.txt

# the first review
cd docs/reviews/first-review/diagrams && for f in [0-9]*.py; do ../../../../.venv/bin/python "$f"; done
cd .. && ../../../.venv/bin/python build_slides.py
soffice --headless --convert-to pdf Predictive_BMS_First_Review.pptx
```

The zeroth review works the same way, from `docs/reviews/zeroth-review/`.

Each diagram script writes both a `.png` and an `.svg`. `build_slides.py` picks
up the PNGs, so re-run a diagram script before rebuilding the deck if you change
one. Every slide carries speaker notes.

Both decks show up inside the tracker: they are listed in `data.js` under
`PROJECT_DOCS`, so they preview in the **Project documents** card, and there is a
small link in the footer.

---

## How to add a task or a phase

**A task** — add an object to that phase's `tasks` array:

```js
tasks: [
  { id: "p3-pack",    title: "Assemble 4S pack",       done: false },
  { id: "p3-balance", title: "Test passive balancing", done: false },  // ← new
],
```

**A phase** — append an object to `PHASES`:

```js
{
  id: "p7",
  number: 7,
  title: "Demo Day",
  blurb: "Showing it off.",
  notes: ["Charge a spare pack the night before."],
  docs: [{ id: "p7-doc-script", title: "Demo Script", file: "./docs/demo.pdf", pending: true }],
  tasks: [
    { id: "p7-rehearse", title: "Rehearse the demo", done: false },
  ],
},
```

The grid, the counters, both progress bars and every panel derive from `PHASES`
— there is nothing else to update. Bump `DATA_VERSION` when you change the
structure; existing local progress is **not** wiped by a version bump, it just
carries over every ID that still exists.

---

## Deploy to GitHub Pages

1. Push this folder to a GitHub repository (files at the repo root).
2. Go to **Settings → Pages**.
3. **Source:** "Deploy from a branch".
4. **Branch:** `main`, **folder:** `/ (root)`.
5. **Save**, then wait a minute for the first build.

The site will be live at `https://<username>.github.io/<repo>/`.

The empty [`.nojekyll`](.nojekyll) file tells Pages to skip Jekyll processing and
serve every file exactly as-is. Every asset and import in this project uses a
relative path (`./app.js`, `./docs/bom.csv`), so it works correctly under a
repository sub-path — never switch those to absolute `/` paths.

---

## Run it locally

ES modules and the CSV tables are both blocked by the browser over `file://`, so
open it through a local server rather than double-clicking `index.html`:

```bash
python3 -m http.server 8080
```

Then visit <http://localhost:8080>.

---

## Files

| File | What it is |
| --- | --- |
| `index.html` | Markup shell, Tailwind config, fonts, panel, inline SVG favicon |
| `data.js` | **The only file you normally edit** — phases, tasks, notes, documents |
| `app.js` | Rendering, `localStorage`, progress, panel, CSV tables |
| `styles.css` | Strikethrough, sparkle, phase glow, panel, table styling |
| `docs/` | The documents themselves — see [`docs/README.md`](docs/README.md) |
| `.nojekyll` | Tells GitHub Pages to serve files as-is |

> The prices in `docs/costing.csv` and the drawing in
> `docs/sld-placeholder.svg` are **placeholders**. Replace them with your own.
