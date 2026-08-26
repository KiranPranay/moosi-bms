"""05 - NTC thermistor input, one of four.

The thermistor sits in a divider against a fixed 10 kohm reference, so the
node is near half supply at room temperature.
"""
import schemdraw
import schemdraw.elements as elm
from _style import NAVY, TEAL, AMBER, GREY, BLACK, SERIF, save_schemdraw

schemdraw.config(font=SERIF, fontsize=14, lw=2.0, color=BLACK)

def txt(d, x, y, s, color=BLACK, ha="center"):
    d.add(elm.Label().at((x, y)).label(s, color=color, halign=ha))

with schemdraw.Drawing(show=False) as d:
    d += elm.Vdd().at((0, 6.2)).color(TEAL)
    txt(d, 0.0, 6.85, "3.3 V", TEAL)

    d += elm.Resistor().down().at((0, 6.2)).to((0, 4.2)).color(NAVY)
    txt(d, -0.75, 5.2, "R_ref\n10 kΩ  1 %", NAVY, "right")

    d += elm.Dot().at((0, 4.2))
    d += elm.Thermistor().down().at((0, 4.2)).to((0, 2.2)).color(AMBER)
    txt(d, -0.85, 3.2, "NTC\n10 kΩ at 25 °C\nβ = 3950 K", AMBER, "right")
    d += elm.Ground().at((0, 2.2))

    d += elm.Resistor().right().at((0, 4.2)).to((2.6, 4.2)).color(GREY)
    txt(d, 1.3, 4.95, "R_f   1 kΩ", GREY)
    d += elm.Dot().at((2.6, 4.2))
    d += elm.Capacitor().down().at((2.6, 4.2)).to((2.6, 2.2)).color(GREY)
    txt(d, 3.25, 3.2, "C_f\n100 nF", GREY, "left")
    d += elm.Ground().at((2.6, 2.2))

    d += elm.Line().right().at((2.6, 4.2)).to((5.2, 4.2)).color(TEAL)
    d += elm.Dot(open=True).at((5.2, 4.2))
    txt(d, 5.45, 4.2, "to CD4051 channel\nthen GPIO36   ADC1", TEAL, "left")

    save_schemdraw(d, "05_ntc_schematic")
