"""03 - Single-line diagram of the power path.

Single-line convention: one line carries the power path, the protective
devices sit in line with it, and each measurement point is shown as an
instrument bubble tapped off the line.

Both switching devices sit in the negative return, so both gates are driven
against system ground. The full MOSFET symbols and gate drive are shown in
diagram 06.
"""
import schemdraw
import schemdraw.elements as elm
from _style import NAVY, TEAL, AMBER, RED, GREY, BLACK, SERIF, save_schemdraw

schemdraw.config(font=SERIF, fontsize=14, lw=2.0, color=BLACK)

YP, YN = 4.0, 0.0            # positive rail, negative return
XR = 12.3                    # right-hand terminals

with schemdraw.Drawing(show=False) as d:

    # ---- pack ----------------------------------------------------------
    d += elm.Battery().up().at((0, 0.8)).length(2.4).color(TEAL)
    d += elm.Line().up().at((0, 3.2)).to((0, YP)).color(TEAL)
    d += elm.Line().down().at((0, 0.8)).to((0, YN)).color(TEAL)
    d.add(elm.Label().at((1.5, 2.55)).label(
        "4S Li-ion pack\n4 × 18650 cells\n14.8 V nominal · 16.8 V full", color=TEAL,
        halign="left"))

    # ---- positive rail -------------------------------------------------
    d += elm.Line().right().at((0, YP)).to((2.6, YP)).color(TEAL)
    d += elm.Fuse().right().at((2.6, YP)).to((4.4, YP)).color(AMBER).label(
        "F1   15 A", loc="top", ofst=0.20)
    d += elm.Line().right().at((4.4, YP)).to((XR, YP)).color(TEAL)
    d += elm.Dot().at((XR, YP))
    d.add(elm.Label().at((XR - 0.05, YP + 0.42)).label("C+ / L+", color=TEAL))

    # ---- negative return -----------------------------------------------
    d += elm.Line().right().at((0, YN)).to((1.9, YN)).color(TEAL)
    d += elm.Resistor().right().at((1.9, YN)).to((3.7, YN)).color(NAVY).label(
        "R1  shunt  5 mΩ", loc="top", ofst=0.20)
    d += elm.Line().right().at((3.7, YN)).to((5.0, YN)).color(TEAL)
    d += elm.Switch(action="open").right().at((5.0, YN)).to((6.8, YN)).color(RED).label(
        "Q1  discharge\nMOSFET", loc="bottom", ofst=0.35)
    d += elm.Line().right().at((6.8, YN)).to((8.2, YN)).color(TEAL)
    d += elm.Switch(action="open").right().at((8.2, YN)).to((10.0, YN)).color(RED).label(
        "Q2  charge\nMOSFET", loc="bottom", ofst=0.35)
    d += elm.Line().right().at((10.0, YN)).to((XR, YN)).color(TEAL)
    d += elm.Dot().at((XR, YN))
    d.add(elm.Label().at((XR - 0.05, YN - 0.45)).label("C− / L−", color=TEAL))

    # ---- charger / load, drawn as four lines so it cannot float ---------
    bx0, bx1, by0, by1 = 13.6, 16.3, 1.2, 2.8
    for a, b in (((bx0, by0), (bx1, by0)), ((bx1, by0), (bx1, by1)),
                 ((bx1, by1), (bx0, by1)), ((bx0, by1), (bx0, by0))):
        d += elm.Line().at(a).to(b).color(GREY)
    d.add(elm.Label().at(((bx0 + bx1) / 2, (by0 + by1) / 2)).label("Charger\nor Load"))
    d += elm.Line().right().at((XR, YP)).to(((bx0 + bx1) / 2, YP)).color(TEAL)
    d += elm.Line().down().at((((bx0 + bx1) / 2), YP)).to((((bx0 + bx1) / 2), by1)).color(TEAL)
    d += elm.Line().right().at((XR, YN)).to(((bx0 + bx1) / 2, YN)).color(TEAL)
    d += elm.Line().up().at((((bx0 + bx1) / 2), YN)).to((((bx0 + bx1) / 2), by0)).color(TEAL)

    # ---- instrument bubbles --------------------------------------------
    d += elm.MeterV().at((-3.4, 3.1)).right().length(1.1).color(NAVY)
    d.add(elm.Label().at((-2.85, 4.05)).label("cell voltages\n4 taps", color=NAVY))
    d += elm.Line().right().at((-2.3, 3.1)).to((0, 3.1)).color(NAVY).linestyle("--")

    d += elm.Thermistor().at((-3.7, 1.1)).right().length(1.5).color(AMBER)
    d.add(elm.Label().at((-2.95, 0.15)).label("cell temperature\n4 thermistors", color=AMBER))
    d += elm.Line().right().at((-2.2, 1.1)).to((0, 1.1)).color(AMBER).linestyle("--")

    d += elm.MeterA().at((2.8, -2.9)).up().length(1.1).color(NAVY)
    d.add(elm.Label().at((4.9, -2.35)).label("pack current", color=NAVY))
    d += elm.Line().up().at((2.8, -1.8)).to((2.8, YN)).color(NAVY).linestyle("--")

    save_schemdraw(d, "03_power_path_sld")
