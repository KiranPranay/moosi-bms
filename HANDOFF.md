# Session handoff — 27 October 2026

These notes let a new Claude Code session, on a new device, carry on where the last one stopped. Read
[CLAUDE.md](CLAUDE.md) first for the rules (commit to `main`, no AI attribution, public repo).

## 1. Where the project stands

| Item | State |
| --- | --- |
| Synopsis, architecture diagram, guide approval | Done |
| Zeroth review | Done, 22-07-2026 |
| First review | Done, 29-09-2026 |
| Design | **Architecture revision 2.2, 24-10-2026**: two-layer protection plus the predictive thermal layer (section 9) |
| Procurement | Cart reconciled; parts not yet bought. Full replacement value ₹9,260.19 |
| Hardware build | Not started. Next step is Gate 0 in `docs/safe-build-sequence.md` |
| Firmware | **Not written yet.** ESP-IDF, C++ and FreeRTOS are planned |
| Plan | Two phases: Semester 1 = Gates 0–2 with **no lithium cells**; Semester 2 = Gates 3–12 ([docs/project-phases.pdf](docs/project-phases.pdf)) |
| Guide's challenge | The guide judged the project "just a sensing system" and asked for a one-page abstract, a benchmark against existing solutions and the Delta X over the base paper. Answered on 27-10-2026 by [docs/abstract.pdf](docs/abstract.pdf) (one page, also as `.docx`) and [docs/benchmark-delta-x.pdf](docs/benchmark-delta-x.pdf) (10 pages, every calculation and source) |

## 2. Decisions made in the last session, and why

1. **First-review deck restyled** to the department's first-review design: 4:3, green bars, left-aligned
   headings, blue tables. It is implemented as `theme="banded"` in `docs/reviews/deck_common.py`; the
   zeroth-review deck keeps `"classic"`.
2. **Base paper: Ojo et al., 2021.** O. Ojo, H. Lang, Y. Kim, X. Hu, B. Mu and X. Lin, "A neural network based
   method for thermal fault detection in lithium-ion batteries," *IEEE Trans. Ind. Electron.*, vol. 68, no. 5,
   pp. 4068–4078, 2021, doi:10.1109/TIE.2020.2984980. It is ref [7] in the first review. The paper is
   **paywalled**, with no legal free copy (checked on OpenAlex, Unpaywall and Semantic Scholar), so the student
   needs the college's IEEE access. Never commit the PDF. The second choice was Chen et al., 2024 (*Sensors*,
   open access), ref [8].
3. **Delta X over the base paper.** The base paper predicts the surface temperature with an LSTM and flags
   the gap. This project uses a physical model and Kalman filter that need no training, running on an ESP32,
   and it acts as well as detects: separate charge and load relays, latched trips, an independent hardware BMS.
   It also adds the predictive layer below.
4. **A reviewer said "it only senses, how does it predict?"** That was a fair point about revision 2.1, where
   the only step beyond sensing was a dT/dt slope. The answer was the **predictive thermal layer** in
   architecture section 9, which the user accepted and asked to make deeper:
   - 9.1 a two-state (core and surface) thermal model for each cell, following ref [9] Lin et al.;
   - 9.2 a Kalman observer estimating the core temperature and the **abnormal heat Q_ab in watts**, plus the
     cell-to-cell comparison and sensor-contact detection;
   - 9.3 **predict and confirm** (the user's own idea): forecast each cell's temperature 1 and 5 minutes
     ahead, then check the forecast against the real reading. Within ±0.5 °C is normal; +1.0 °C or more
     raises Watch. A running RMS accuracy record is kept;
   - 9.4 online internal resistance; 9.5 rest self-discharge (leak) estimate with an **energy cross-check**
     against Q_ab;
   - 9.6 settling temperature, time to limit and **safe continuous current**; 9.7 self-acceleration test;
     9.8 risk levels Normal → Watch → Warning → Trip (thermal and electrical evidence must agree for a soft
     fault); 9.9 fallback; 9.10 ESP32 budget; 9.11 "what is new" (scoped to the papers reviewed).
5. **Limits changed:** abnormal heat now carries the 0.5 °C/min warning and 1.0 °C/min trip (about 0.4 W and
   0.75 W). The raw dT/dt limit is a backstop at 1.0 °C/min warning and 2.0 °C/min trip. The reason is that a
   healthy cell at 5 A may heat at about 1 °C/min, which is an estimate to be measured at Gate 9. Until the
   model is fitted, the raw limits revert to 0.5 / 1.0.
6. **Fifth NTC** for ambient temperature on GPIO36 (ADC1_CH0, input-only), +₹14 in the BOM and costing.
7. **Gate 11 now includes an emulated soft short:** a 47 Ω 1 W resistor bonded to one cell and wired across
   that cell's taps through a fused lead, supervised, with the cell kept below 40 °C. No fault is ever created
   inside a cell.
8. `docs/reviews/build_references.py` now builds **any** markdown file to PDF
   (`python build_references.py ../project-phases.md`). It supports `<div markdown="1" class="breakable">`
   for long tables that may break across pages, `class="breakable wide"` for smaller type in six- or seven-column
   tables, and fenced ```text blocks for worked calculations.
10. **The abstract is a Word file** built by `docs/reviews/build_abstract.py` (python-docx), in the layout of a
   classmate's abstract the user shared as a format reference: A4, Times New Roman, bold 16 pt centred title,
   centred "Abstract", justified 12 pt prose, the student's name and roll number in bold to the right, and the
   guide's signature block. It is a formal academic abstract in the third person (problem, system, algorithms,
   features, improvement over the base paper), with no prices or semester and gate details; the user rejected
   a first-person version with those. The benchmark tables and the Delta X working are in `benchmark-delta-x`.
   The reference `.docx` stays local only (`*[Bb]atch*.docx` is git-ignored).
9. **Delta X numbers** (all derived from the base paper's own figures; working in `docs/benchmark-delta-x.md`
   section 4): its 0.69 °C threshold inside the 4.5 s feedback window only catches heating above about
   9.2 °C/min (≈ 6.9 W), against our 0.5 °C/min warning (18×) and the 0.2 W 5-minute check (34×); 0.5 % per-sample
   false positives at 2 Hz = up to 36 flags an hour; about 21,000 weights and 206,000 multiply-adds per estimate
   against about 100 for the Kalman filter (≈ 2,000×). The base paper's PDF is kept local only (`ojo2021*.pdf` is
   git-ignored).

## 3. Open items (nothing below has been done)

- **Reviewer paragraph needs a rewrite.** The paragraph sent to the reviewer (section 6) predates
  predict-and-confirm and the leak cross-check. The user was offered a rewrite and has not answered yet.
- **First-review timeline slide** still shows "Month 1–5" with no semester split, so it doesn't match the
  two-phase plan. The title slide is still dated 29-09-2026.
- **Review dates for the Stage-1 end-of-semester review and Semester 2** are unknown; the plan says they will be
  added when announced.
- **The purchase indent may already cover the fifth NTC.** The local, uncommitted `Purchase-Indent_single.xlsx`
  requests **8** × 10k NTC (Robu SKU 871999), while the BOM lists 5. So the tracker task "Add a fifth NTC to the
  Robu cart" may already be covered; confirm with the user.
- **Estimates to validate at Gates 9–11:** C ≈ 45 J/°C, R_u ≈ 30 °C/W, R ≈ 35 mΩ, about 1 °C/min heating at
  5 A, a 20 mA leak giving about 6 mV/h, 5-minute forecasts within 0.5 °C RMS, and whether the two-state
  model's parameters can be identified on this small pack. If they cannot, fall back to a single thermal mass.
- **ESP32 price has moved.** Robu listed the ESP32-WROOM-32D board at ₹759 on 27-10-2026, against ₹639 in
  `bom.csv` and `costing.csv`. The BOM, costing and the documents still say ₹639; update them together if the
  new price holds when ordering.
- **Files kept local only (copy them by hand if needed):** `Purchase-Indent_single.xlsx` (company form; must
  not go in the public repo), `outputs/` (a tool's scratch copy of the same sheet), and
  `Major_Project_Review1_Batch(10) (3).pdf` (another team's deck; git-ignored).

## 4. Setting up the new device

```bash
git clone git@github.com:KiranPranay/moosi-bms.git && cd moosi-bms
python3 -m venv .venv && .venv/bin/pip install -r docs/reviews/first-review/requirements.txt
# System tools (Debian/Ubuntu names):
sudo apt install libreoffice poppler-utils imagemagick fonts-liberation fonts-crosextra-carlito
# plus Google Chrome: build_references.py calls the `google-chrome` binary for markdown -> PDF
```

- `.venv/` is git-ignored.
- The PPTX files name Times New Roman and Calibri. Liberation Serif and Carlito are the metric-compatible
  stand-ins that keep line breaks the same in the LibreOffice-rendered PDFs.
- On macOS or Windows, change the `google-chrome` call in `build_references.py` to the local Chrome path.

## 5. Rebuilding everything

| Output | Command (from the repo root) |
| --- | --- |
| First-review diagrams | `cd docs/reviews/first-review && ../../../.venv/bin/python diagrams/r1_methodology.py` (also `r1_block_diagram.py`, `r1_schematic.py`) |
| First-review deck | `cd docs/reviews/first-review && ../../../.venv/bin/python build_slides.py && soffice --headless --convert-to pdf Predictive_BMS_First_Review.pptx` |
| Zeroth-review deck | the same in `docs/reviews/zeroth-review` (historical; leave it alone) |
| Plan PDF | `cd docs/reviews && ../../.venv/bin/python build_references.py ../project-phases.md` |
| References PDF | `cd docs/reviews && ../../.venv/bin/python build_references.py` |
| Abstract (`.docx` and PDF, one page) | `cd docs/reviews && ../../.venv/bin/python build_abstract.py` (the text is in `BODY` in the script; it stops if the PDF runs past one page) |
| Benchmarking and Delta X PDF | `cd docs/reviews && ../../.venv/bin/python build_references.py ../benchmark-delta-x.md` |
| Tracker site | `python3 -m http.server 8080`, then open <http://localhost:8080> |

Check every rebuilt PDF visually before committing, for example with `pdftoppm -r 60 -png file.pdf out/p`
and then looking at the pages. `build_slides.py` prints overflow warnings, but it cannot detect every overlap.

## 6. The paragraph sent to the reviewer (for reference)

> Our system does much more than sensing; the sensors are only its inputs. Five times every second, the ESP32
> uses a simple thermal model of each cell to predict how fast that cell should be heating. The model uses the
> heat made by the current flowing through the cell (I²R), and how quickly the cell should lose heat to the
> surrounding air, which a fifth sensor measures. It then compares this prediction with how fast the cell is
> actually heating. Normal heating under load is expected and is not flagged. But heat that the current cannot
> explain is treated as an early sign of a fault, for example a cell warming up with little or no current,
> which is how an internal short begins. Because all four cells carry the same current, the system also checks
> whether one cell is heating faster than the other three. It also forecasts how many minutes each cell has
> left before it reaches its temperature limit. If the unexplained heating keeps growing, the system
> disconnects the charger, the load or both, and keeps the fault latched, before any fixed temperature limit is
> reached. This is the same predict-and-compare idea as our base paper (Ojo et al., IEEE TIE 2021), which uses
> a neural network to predict the cell temperature. We use a physics model instead, so it needs no training
> data, runs on a low-cost ESP32, and every decision can be checked by hand.

## 7. Where things are

| Path | What it is |
| --- | --- |
| `docs/current-architecture.md` | Build authority, revision 2.2; section 9 is the predictive layer |
| `docs/safe-build-sequence.md` | Gates 0–12 with pass and stop criteria |
| `docs/project-phases.md` / `.pdf` | The two-semester plan, for the guide and reviewers |
| `docs/abstract.docx` / `.pdf` | One-page abstract with the benchmark and the Delta X, for the guide; source is `docs/reviews/build_abstract.py` |
| `docs/benchmark-delta-x.md` / `.pdf` | Full benchmark (6 products, 7 research methods), Delta X, worked soft-short example, sources |
| `docs/bom.csv`, `docs/costing.csv` | Parts and costs (₹9,260.19) |
| `docs/reviews/first-review/` | Review-1 deck, its diagrams, research notes (reference checks) |
| `docs/reviews/references-explained.md` / `.pdf` | What each reference contributes |
| `docs/reviews/deck_common.py`, `template-notes.md` | Deck themes and their measured design values |
| `index.html`, `app.js`, `data.js`, `styles.css` | The procurement and progress tracker site (separate from the BMS dashboard) |
