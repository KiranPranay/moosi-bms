"""Build references-explained.pdf from references-explained.md.

    python build_references.py                          # references-explained.md
    python build_references.py ../project-phases.md     # any other document
    python build_references.py --one-page ../abstract.md

The markdown is the source, and the PDF is written next to it. It is turned into a styled HTML page and printed to
PDF with headless Chrome, so the PDF previews in the tracker like the decks do. --one-page uses tighter type and
margins and fails if the result runs past one A4 page.
"""
import os
import re
import subprocess
import sys
import tempfile

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "references-explained.md")
LOGO = os.path.join(HERE, "assets", "logo.png")

CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm;
        @bottom-center { content: counter(page); } }
body  { font-family: "Times New Roman", "Liberation Serif", serif; font-size: 11.5pt;
        line-height: 1.45; color: #000; }
header { display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }
header img { height: 58px; }
h1    { font-size: 20pt; color: #002060; margin: 0; }
h2    { font-size: 14pt; color: #002060; margin: 22px 0 6px; padding-bottom: 3px;
        border-bottom: 1px solid #c8cfdc; page-break-after: avoid; }
h3    { font-size: 12pt; color: #002060; margin: 16px 0 4px; page-break-after: avoid; }
p     { margin: 6px 0; }
a     { color: #1f4e8c; text-decoration: none; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; margin: 8px 0 4px;
        page-break-inside: avoid; }
th    { background: #002060; color: #fff; text-align: left; padding: 5px 7px; }
td    { padding: 4px 7px; border-bottom: 1px solid #e3e3e3; vertical-align: top; }
tr:nth-child(even) td { background: #f3f3f3; }
th:first-child { white-space: nowrap; }
.byline { color: #333; font-size: 10.5pt; margin: 4px 0 14px; }
.breakable table { page-break-inside: auto; }  /* long tables: wrap in <div markdown="1" class="breakable"> */
.wide table { font-size: 9pt; }                 /* tables with six or more columns */
tr    { page-break-inside: avoid; }
pre   { font-family: "DejaVu Sans Mono", "Liberation Mono", monospace; font-size: 9.5pt; line-height: 1.4;
        background: #f3f5f9; border-left: 3px solid #002060; padding: 6px 10px; margin: 8px 0;
        white-space: pre-wrap; page-break-inside: avoid; }
"""

ONE_PAGE_CSS = """
@page { size: A4; margin: 10mm 12mm 9mm 12mm; @bottom-center { content: none; } }
body  { font-size: 9.6pt; line-height: 1.3; }
header img { height: 40px; }
h1    { font-size: 15pt; }
h2    { font-size: 10.6pt; margin: 7px 0 2px; padding-bottom: 1px; }
p     { margin: 3px 0; text-align: justify; }
ul    { margin: 2px 0; padding-left: 16px; }
li    { margin: 1px 0; }
table { font-size: 8.3pt; margin: 3px 0 2px; }
th    { padding: 2px 5px; }
td    { padding: 1.5px 5px; }
.byline { font-size: 9pt; margin: 1px 0 4px; }
"""


def page_count(pdf):
    return len(re.findall(rb"/Type\s*/Page[^s]", open(pdf, "rb").read()))


def build(src=SRC, one_page=False):
    out = os.path.splitext(src)[0] + ".pdf"
    text = open(src, encoding="utf-8").read()
    title, _, rest = text.partition("\n")
    byline, _, body = rest.strip("\n").partition("\n\n")
    html_body = markdown.markdown(body, extensions=["tables", "md_in_html", "fenced_code"])
    byline_html = markdown.markdown(byline).replace("<p>", '<p class="byline">')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title.lstrip('# ').strip()}</title><style>{CSS}{ONE_PAGE_CSS if one_page else ""}</style></head><body>
<header><img src="file://{LOGO}" alt=""><h1>{title.lstrip('# ').strip()}</h1></header>
{byline_html}
{html_body}
</body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(page)
        tmp = fh.name
    profile = tempfile.mkdtemp()
    subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
                    "--user-data-dir=" + profile, "--no-pdf-header-footer",
                    "--print-to-pdf=" + out, "file://" + tmp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(tmp)
    pages = page_count(out)
    print("saved", os.path.basename(out), f"({pages} page{'s' if pages != 1 else ''})")
    if one_page and pages != 1:
        sys.exit(f"{os.path.basename(out)} must fit on one page; shorten the source")


if __name__ == "__main__":
    args = sys.argv[1:]
    one_page = "--one-page" in args
    for path in [a for a in args if a != "--one-page"] or [SRC]:
        build(os.path.abspath(path), one_page)
