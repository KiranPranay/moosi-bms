"""06 - Protection cut-off and passive balancing.

Left: the two cut-off MOSFETs, sources tied together. Their body diodes face
      opposite ways, so each one blocks current in a different direction and
      the pair can stop charging and discharging independently.
Right: the bleed circuit for one cell. Every cell has its own copy.
"""
import schemdraw
import schemdraw.elements as elm
from _style import NAVY, TEAL, AMBER, RED, GREEN, GREY, BLACK, SERIF, save_schemdraw

schemdraw.config(font=SERIF, fontsize=13, lw=2.0, color=BLACK)

def txt(d, x, y, s, color=BLACK, ha="center", size=13):
    d.add(elm.Label().at((x, y)).label(s, color=color, halign=ha, fontsize=size))

with schemdraw.Drawing(show=False) as d:

    # ============ left panel : cut-off pair ==============================
    XC, TIE = 3.6, 4.25
    txt(d, 5.4, 9.0, "Cut-off pair — low side, back to back", NAVY, "center", 16)

    d += elm.Line().down().at((XC, 8.1)).to((XC, 6.0)).color(TEAL)
    txt(d, XC + 0.25, 8.25, "B−  from the pack", TEAL, "left")

    d.add(elm.NFet(bulk=True).anchor("drain").at((XC, 6.0)).color(RED))
    txt(d, XC - 1.80, 5.25, "Q1\ndischarge\nIRLZ44N", RED, "right", 12)

    d += elm.Line().down().at((XC, 4.5)).to((XC, 4.0)).color(TEAL)
    d += elm.Dot().at((XC, TIE))
    d.add(elm.NFet(bulk=True).flip().anchor("source").at((XC, 4.0)).color(RED))
    txt(d, XC - 1.80, 3.25, "Q2\ncharge\nIRLZ44N", RED, "right", 12)

    d += elm.Line().down().at((XC, 2.5)).to((XC, 1.6)).color(TEAL)
    txt(d, XC + 0.25, 1.42, "to  C− / L−", TEAL, "left")

    d += elm.Line().right().at((XC, TIE)).to((7.2, TIE)).color(TEAL)
    txt(d, 5.2, TIE - 0.45, "shared source", GREY, "center", 12)

    # Q1 gate network
    d += elm.Line().right().at((XC + 1.37, 5.25)).to((6.2, 5.25)).color(GREY)
    d += elm.Dot().at((6.2, 5.25))
    d += elm.Resistor().down().at((6.2, 5.25)).to((6.2, TIE)).color(GREY)
    txt(d, 5.62, 4.75, "100 kΩ", GREY, "right", 12)
    d += elm.Dot().at((6.2, TIE))
    d += elm.Resistor().right().at((6.2, 5.25)).to((7.6, 5.25)).color(GREY)
    txt(d, 6.9, 5.85, "10 Ω", GREY, "center", 12)
    d += elm.Line().right().at((7.6, 5.25)).to((8.8, 5.25)).color(GREY)
    d += elm.Dot(open=True).at((8.8, 5.25))
    txt(d, 8.98, 5.25, "DSG_EN\nGPIO16", TEAL, "left", 12)

    # Q2 gate network
    d += elm.Line().right().at((XC + 1.37, 3.25)).to((7.2, 3.25)).color(GREY)
    d += elm.Dot().at((7.2, 3.25))
    d += elm.Resistor().up().at((7.2, 3.25)).to((7.2, TIE)).color(GREY)
    txt(d, 7.78, 3.75, "100 kΩ", GREY, "left", 12)
    d += elm.Dot().at((7.2, TIE))
    d += elm.Resistor().right().at((7.2, 3.25)).to((8.6, 3.25)).color(GREY)
    txt(d, 7.9, 2.65, "10 Ω", GREY, "center", 12)
    d += elm.Line().right().at((8.6, 3.25)).to((8.8, 3.25)).color(GREY)
    d += elm.Dot(open=True).at((8.8, 3.25))
    txt(d, 8.98, 3.25, "CHG_EN\nGPIO17", TEAL, "left", 12)

    txt(d, 5.4, 0.55,
        "The 100 kΩ resistors hold both gates at the shared source, so the\n"
        "pair sits OFF whenever the ESP32 is not driving it.",
        GREY, "center", 12)

    # ============ right panel : balancing one cell =======================
    XB, GN = 19.7, 17.6
    txt(d, 16.8, 9.0, "Passive balancing — one cell", NAVY, "center", 16)

    d += elm.Dot().at((XB, 7.0)).color(TEAL)
    txt(d, XB + 0.28, 7.38, "cell +", TEAL, "left")
    d.add(elm.PFet(bulk=True).reverse().anchor("source").at((XB, 7.0)).color(AMBER))
    txt(d, XB + 1.35, 6.25, "Q3\nP-channel", AMBER, "left", 12)

    d += elm.Resistor().down().at((XB, 5.5)).to((XB, 3.6)).color(NAVY)
    txt(d, XB + 0.35, 4.55, "R_bleed\n33 Ω  1 W", NAVY, "left", 12)
    d += elm.Line().down().at((XB, 3.6)).to((XB, 2.9)).color(TEAL)
    d += elm.Dot().at((XB, 2.9)).color(TEAL)
    txt(d, XB + 0.28, 2.60, "cell −", TEAL, "left")

    d += elm.Line().left().at((XB - 1.37, 6.25)).to((GN, 6.25)).color(GREY)
    d += elm.Dot().at((GN, 6.25))
    d += elm.Resistor().up().at((GN, 6.25)).to((GN, 7.0)).color(GREY)
    txt(d, GN - 0.28, 6.62, "100 kΩ", GREY, "right", 12)
    d += elm.Line().right().at((GN, 7.0)).to((XB, 7.0)).color(GREY)

    d.add(elm.Optocoupler().anchor("collector").at((GN, 5.6)).color(GREEN))
    d += elm.Line().down().at((GN, 6.25)).to((GN, 5.6)).color(GREY)
    txt(d, GN - 1.05, 3.35, "PC817", GREEN, "center", 12)
    d += elm.Line().down().at((GN, 4.20)).to((GN, 2.9)).color(GREY)
    d += elm.Line().right().at((GN, 2.9)).to((XB, 2.9)).color(GREY)

    d += elm.Line().left().at((GN - 2.40, 5.65)).to((14.5, 5.65)).color(GREY)
    d += elm.Resistor().left().at((14.5, 5.65)).to((13.1, 5.65)).color(GREY)
    txt(d, 13.8, 6.25, "1 kΩ", GREY, "center", 12)
    d += elm.Dot(open=True).at((13.1, 5.65))
    txt(d, 12.92, 5.65, "BAL1\nGPIO13", TEAL, "right", 12)
    d += elm.Line().left().at((GN - 2.40, 4.15)).to((14.3, 4.15)).color(GREY)
    d += elm.Ground().at((14.3, 4.15)).color(GREY)

    txt(d, 16.8, 1.30,
        "The optocoupler keeps the drive isolated, so one GPIO referenced to\n"
        "ground can switch a cell that sits several volts above ground.\n"
        "Bleed current at 4.0 V is 4.0 / 33 = 121 mA, about 0.48 W.",
        GREY, "center", 12)

    save_schemdraw(d, "06_cutoff_balancing_schematic")
