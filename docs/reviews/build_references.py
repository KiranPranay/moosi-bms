"""Build references-explained.pdf from references-explained.md.

    python build_references.py                          # references-explained.md
    python build_references.py ../project-phases.md     # any other document

The markdown is the source, and the PDF is written next to it. It is turned into a styled HTML page and printed to
PDF with headless Chrome, so the PDF previews in the tracker like the decks do.
"""
import os
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
tr    { page-break-inside: avoid; }
"""


def build(src=SRC):
    out = os.path.splitext(src)[0] + ".pdf"
    text = open(src, encoding="utf-8").read()
    title, _, rest = text.partition("\n")
    byline, _, body = rest.strip("\n").partition("\n\n")
    html_body = markdown.markdown(body, extensions=["tables", "md_in_html"])
    byline_html = markdown.markdown(byline).replace("<p>", '<p class="byline">')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title.lstrip('# ').strip()}</title><style>{CSS}</style></head><body>
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
    print("saved", os.path.basename(out))


if __name__ == "__main__":
    for path in sys.argv[1:] or [SRC]:
        build(os.path.abspath(path))
