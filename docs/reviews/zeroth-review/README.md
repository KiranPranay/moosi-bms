# Zeroth review

The deck for the zeroth review. It follows the order zeroth reviews are
presented in the department: abstract, problem statement and objective,
implementation outline, implementation and tools, literature survey,
references.

| File | What it is |
| --- | --- |
| `Predictive_BMS_Zeroth_Review.pptx` | Edit this one |
| `Predictive_BMS_Zeroth_Review.pdf` | The version to hand in |
| `build_slides.py` | Builds the pptx from the diagrams |
| `diagrams/` | One script per figure |

To rebuild:

```bash
cd diagrams && for f in z*.py; do ../../../../.venv/bin/python "$f"; done
cd .. && ../../../.venv/bin/python build_slides.py
soffice --headless --convert-to pdf Predictive_BMS_Zeroth_Review.pptx
```

The slide layout comes from [`../deck_common.py`](../deck_common.py) and the
figure styling from [`../diagram_style.py`](../diagram_style.py), so this deck
and the first review look the same.

**The date in the footer is 22-07-2026.** Change `export_date` at the top of
`build_slides.py` if the review is on another day.
