"""04 - Cell-tap voltage divider (top tap shown).

All four taps use the same divider, so the top tap sets the ratio: it has to
bring the full pack voltage inside the ADC input range.
The numbers that go with it are on the slide, so the drawing stays compact
enough to read when two schematics share one slide.
"""
import schemdraw
import schemdraw.elements as elm
from _style import NAVY, TEAL, GREY, BLACK, SERIF, save_schemdraw

schemdraw.config(font=SERIF, fontsize=14, lw=2.0, color=BLACK)

def txt(d, x, y, s, color=BLACK, ha="center"):
    d.add(elm.Label().at((x, y)).label(s, color=color, halign=ha))

with schemdraw.Drawing(show=False) as d:
    d += elm.Dot().at((0, 6.0)).color(TEAL)
    txt(d, 0.25, 6.6, "T4   pack +   16.8 V full", TEAL, "left")

    d += elm.Resistor().down().at((0, 6.0)).to((0, 4.0)).color(NAVY)
    txt(d, -0.75, 5.0, "R1\n68 kΩ  1 %", NAVY, "right")

    d += elm.Dot().at((0, 4.0))
    d += elm.Resistor().down().at((0, 4.0)).to((0, 2.0)).color(NAVY)
    txt(d, -0.75, 3.0, "R2\n10 kΩ  1 %", NAVY, "right")
    d += elm.Ground().at((0, 2.0))

    d += elm.Line().right().at((0, 4.0)).to((2.0, 4.0)).color(TEAL)
    d += elm.Dot().at((2.0, 4.0))
    d += elm.Capacitor().down().at((2.0, 4.0)).to((2.0, 2.0)).color(GREY)
    txt(d, 2.65, 3.0, "C1\n100 nF", GREY, "left")
    d += elm.Ground().at((2.0, 2.0))

    d += elm.Line().right().at((2.0, 4.0)).to((4.8, 4.0)).color(TEAL)
    d += elm.Dot(open=True).at((4.8, 4.0))
    txt(d, 5.05, 4.0, "GPIO35   ADC1", TEAL, "left")

    save_schemdraw(d, "04_voltage_sense_schematic")
