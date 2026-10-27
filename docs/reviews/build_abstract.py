"""Build the one-page project abstract: ../abstract.docx, then ../abstract.pdf.

    python build_abstract.py

Layout: A4, Times New Roman, a bold 16 pt centred title, a centred "Abstract" heading, justified 12 pt body
text, the student's name and roll number in bold towards the right, and the guide's signature block below.
Every figure in the text is worked out, with its source, in ../benchmark-delta-x.md.
"""
import os
import re
import subprocess
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, Twips

from build_references import page_count

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "abstract.docx")
FONT = "Times New Roman"

TITLE = "Predictive Thermal Battery Management System for Li-ion Battery Packs"
STUDENT = "Ms. Muskan Sulathana (23WH1A0208)"
SIGNATURE = ["Signature", "Dr. M. Rupesh", "Associate Professor", "EEE Department"]

BODY = [
    "Thermal runaway is a major safety hazard in lithium-ion battery packs, and one of its main causes is an "
    "internal short circuit, which in its early stage slowly discharges the affected cell and generates only a "
    "fraction of a watt of heat. Conventional battery management systems (BMS) and battery protection ICs act "
    "only when a voltage, current or temperature crosses a fixed threshold, and therefore cannot detect this "
    "stage. This project presents a predictive thermal battery management system for a 4S1P lithium-ion pack "
    "of NCR18650GA cells. The system has two independent protection layers: a hardware BMS that provides "
    "over-voltage, under-voltage, over-current and short-circuit protection, and an ESP32-based supervisory "
    "controller that samples the four cell voltages through a 16-bit ADS1115 ADC, the pack current through an "
    "INA226 with a 5 mΩ shunt, and the four cell temperatures and the ambient temperature through NTC "
    "thermistors at 5 Hz. A two-state (core and surface) lumped thermal model of each cell is combined with a "
    "Kalman filter to estimate the core temperature and the abnormal heat generation, in watts, that the "
    "cell's I²R losses cannot explain. The model predicts each cell's temperature 1 and 5 minutes ahead and "
    "confirms every prediction against the measured value. Additional algorithms track the internal "
    "resistance online, estimate the self-discharge current of each cell at rest from its relative voltage "
    "drift, cross-check the thermal and electrical evidence through an energy balance, forecast the time to "
    "the temperature limit and the safe continuous current, and detect self-accelerating heating. These "
    "indicators are combined into a four-level risk classification (Normal, Watch, Warning and Trip) that "
    "controls separate charge and load relays with latched, fail-safe tripping, and a Wi-Fi dashboard "
    "displays the estimates. Compared with the LSTM neural-network method of the base paper, which requires "
    "offline GPU training and responds only to rapid temperature rises of about 9 °C/min, the proposed "
    "model-based method needs no training data, runs on a low-cost microcontroller and is designed to detect "
    "abnormal heat of about 0.4 W (0.5 °C/min), a temperature rise about eighteen times slower. The system is "
    "evaluated through "
    "sensor calibration, controlled charge and discharge tests, and a safely emulated soft internal short "
    "circuit created with an external resistor.",
]


def keep_units(text):
    """Join each number to its unit with a non-breaking space, so a value never splits across lines."""
    return re.sub(r"(\d) (°C|s\b|W\b|mA\b|minutes\b)", "\\1\u00a0\\2", text)


def paragraph(doc, text="", size=12, bold=False, align=None, before=0, after=0, line=1.08,
              left=None, right=None):
    p = doc.add_paragraph()
    f = p.paragraph_format
    f.space_before, f.space_after, f.line_spacing = Twips(before), Twips(after), line
    if align is not None:
        p.alignment = align
    if left is not None:
        f.left_indent = Twips(left)
    if right is not None:
        f.right_indent = Twips(right)
    if text:
        run = p.add_run(keep_units(text))
        run.bold, run.font.size = bold, Pt(size)
    return p


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Twips(11910), Twips(16840)             # A4
    sec.top_margin, sec.bottom_margin = Twips(1360), Twips(720)
    sec.left_margin = sec.right_margin = Twips(1417)                         # 2.5 cm

    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = FONT, Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)

    zoom = doc.settings.element.find(qn("w:zoom"))      # the default template omits the required percent
    if zoom is not None:
        zoom.set(qn("w:percent"), "100")

    core = doc.core_properties
    core.author = core.last_modified_by = "Muskan Sulathana"
    core.title, core.subject, core.comments, core.keywords = TITLE, "Project abstract", "", ""

    paragraph(doc, TITLE, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, before=350, after=120)
    paragraph(doc, "Abstract", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=240)
    for text in BODY:
        paragraph(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=120)

    paragraph(doc, STUDENT, bold=True, before=960, left=4344, line=398 / 240)
    for i, line in enumerate(SIGNATURE):
        paragraph(doc, line, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
                  before=1000 if i == 0 else 0, left=5600, line=379 / 240)

    doc.save(OUT)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(OUT), OUT],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pages = page_count(os.path.splitext(OUT)[0] + ".pdf")
    print(f"saved abstract.docx and abstract.pdf ({pages} page{'s' if pages != 1 else ''})")
    if pages != 1:
        sys.exit("the abstract must fit on one page; shorten BODY")


if __name__ == "__main__":
    build()
