# CLAUDE.md

Major-project repository for **Predictive Thermal Battery Management System for Li-ion Battery Packs**
(4S1P NCR18650GA pack, ESP32 supervisor and an independent hardware BMS). Student: Muskan Sulathana,
Roll No. 23WH1A0208, EEE, BVRIT HYDERABAD College of Engineering for Women. Guide: Dr. M. Rupesh,
Associate Professor.

**Start every session by reading [HANDOFF.md](HANDOFF.md)**: current state, open items and how to rebuild everything.

## Rules for working here

- **Git:** commit straight to `main` and push with `git push origin main`; do not create feature branches.
  Commit messages follow the existing style (`docs: ...`).
- **No Claude attribution.** Never add a `Co-Authored-By: Claude` trailer or any other AI attribution to
  commits or PRs. This is an organisation policy.
- **The repository is PUBLIC.** Never commit:
  - other students' decks or names and roll numbers (the classmate reference decks are git-ignored);
  - company documents, such as the purchase indent (`Purchase-Indent_single.xlsx`);
  - copyrighted papers (for example the base paper's PDF).
- **Build authority:** [docs/current-architecture.md](docs/current-architecture.md) (revision 2.2) decides
  every engineering value. The decks, the plan and the notes follow it, never the other way round. If you change
  a threshold or a part, update the architecture first, then
  [docs/safe-build-sequence.md](docs/safe-build-sequence.md), `docs/bom.csv` / `docs/costing.csv`, `data.js`,
  [docs/project-phases.md](docs/project-phases.md) and the deck.
- **Every file in `docs/` gets an entry in `data.js`** (see [docs/README.md](docs/README.md)). Bump
  `DATA_VERSION` when phases or tasks change; a bump never wipes the tracker's saved progress.
- **Generated files are committed.** After editing a source (`*.md`, `build_slides.py`, a diagram `*.py`),
  rebuild its PDF, PPTX or PNG and check the render before committing.
- **Writing voice:** student-facing documents are first person (Muskan), in plain words, with no unexplained
  jargon. Claims of novelty are stated as "within the papers reviewed", never "first in the world". Results
  are never claimed before the test that produces them; the firmware is not written yet.
- **Safety:** never plan or describe a test that drives a live cell into thermal runaway, overcharge or
  over-discharge. Limits are proven with simulated signals, dummy heat sources, or the external-resistor
  soft-short emulation in Gate 11.

## Decks

- First review: `docs/reviews/first-review/build_slides.py`, using `configure(..., theme="banded")`: the
  department's 4:3 first-review design with green bars and blue tables.
- Zeroth review: `docs/reviews/zeroth-review/build_slides.py`, using the default `"classic"` 16:9 theme.
  It is a historical record; do not change it.
- Shared furniture: `docs/reviews/deck_common.py`. Design notes for both themes:
  `docs/reviews/template-notes.md`.
