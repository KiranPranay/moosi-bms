"""Review-1 - schematic of the power path and protection.

Follows section 4 of docs/current-architecture.md:

    4S1P cells -> BMS B-/B1/B2/B3/B+ -> P+
    P+ -> 7.5 A fuse -> 5 mohm shunt -> FUSED+ -> LOAD+ and CHARGE+
    P- -> K_LOAD NO contact -> LOAD-      P- -> K_CHARGE NO contact -> CHARGE-
    P+/P- -> LM2596 (5.0 V) -> ESP32 VIN + relay coils

Drawn as a ladder: the positive rail across the top, P- along the bottom, and
each branch hanging between them, so no two conductors cross.
"""
import schemdraw
import schemdraw.elements as elm
from _style import NAVY, TEAL, AMBER, RED, GREEN, GREY, BLACK, SERIF, save_schemdraw

schemdraw.config(font=SERIF, fontsize=14, lw=2.0, color=BLACK)

YP, YN = 5.6, 0.8                  # positive rail, P- rail
TAPS = [(0.8, "B−"), (2.0, "B1"), (3.2, "B2"), (4.4, "B3"), (5.6, "B+")]
XL, XC = 12.6, 15.4                # load and charge branches
XP = XC                            # the positive rail ends at the last branch


def txt(d, x, y, s, color=BLACK, ha="center", size=14):
    d.add(elm.Label().at((x, y)).label(s, color=color, halign=ha, fontsize=size))


def rect(d, x0, y0, x1, y1, color):
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                 ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        d += elm.Line().at(a).to(b).color(color)


with schemdraw.Drawing(show=False) as d:

    # ── cells and balance taps ──────────────────────────────────────────
    for (y0, _), (y1, _) in zip(TAPS[:-1], TAPS[1:]):
        d += elm.BatteryCell().at((0, y0)).to((0, y1)).color(TEAL)
    for y, name in TAPS:
        d += elm.Dot().at((0, y)).color(TEAL)
        d += elm.Line().at((0, y)).to((2.4, y)).color(TEAL)
        txt(d, 1.2, y + 0.24, name, TEAL, size=12.5)
    txt(d, 0.0, 6.30, "4S1P pack", TEAL)

    # ── hardware BMS ────────────────────────────────────────────────────
    rect(d, 2.4, 0.35, 5.4, 6.05, AMBER)
    txt(d, 3.9, 3.2, "Hardware BMS\n4S NMC · 20 A\n\nOV · UV\nOC · SC\nbalancing", AMBER, size=13)

    # ── positive rail ───────────────────────────────────────────────────
    d += elm.Line().at((5.4, YP)).to((XP, YP)).color(TEAL)
    txt(d, 5.8, YP + 0.30, "P+", TEAL, size=13)
    d += elm.Dot().at((6.6, YP))
    d += elm.Fuse().at((7.3, YP)).to((8.8, YP)).color(RED)
    d += elm.Line().at((6.6, YP)).to((7.3, YP)).color(TEAL)
    txt(d, 8.05, YP + 0.62, "F1  7.5 A", RED)
    d += elm.Line().at((8.8, YP)).to((9.4, YP)).color(TEAL)
    d += elm.Resistor().at((9.4, YP)).to((11.0, YP)).color(NAVY)
    txt(d, 10.2, YP + 0.62, "5 mΩ shunt", NAVY)
    d += elm.Line().at((11.0, YP)).to((XC, YP)).color(TEAL)
    d += elm.Dot().at((11.7, YP))
    txt(d, 11.7, YP + 0.30, "FUSED+", TEAL, size=12.5)
    d += elm.Dot().at((XL, YP))

    # ── P- rail ─────────────────────────────────────────────────────────
    d += elm.Line().at((5.4, YN)).to((XC, YN)).color(TEAL)
    txt(d, 5.8, YN - 0.30, "P−", TEAL, size=13)
    d += elm.Dot().at((6.6, YN))
    d += elm.Dot().at((XL, YN))

    # ── LM2596 branch ───────────────────────────────────────────────────
    d += elm.Line().at((6.6, YP)).to((6.6, 4.0)).color(GREEN)
    rect(d, 5.72, 2.6, 7.48, 4.0, GREEN)
    txt(d, 6.6, 3.3, "LM2596\n5.0 V", GREEN, size=12.5)
    d += elm.Line().at((6.6, 2.6)).to((6.6, YN)).color(GREEN)
    txt(d, 7.66, 3.3, "to ESP32\nand relays", GREEN, ha="left", size=12.5)

    # ── INA226 sensing across the shunt (Kelvin connection) ─────────────
    for x in (9.4, 11.0):
        d += elm.Line().at((x, YP)).to((x, 4.2)).color(NAVY).linestyle("--")
    rect(d, 9.25, 3.4, 11.15, 4.2, NAVY)
    txt(d, 10.2, 3.8, "INA226", NAVY, size=12.5)

    # ── load and charge branches, each switched in P- ───────────────────
    for x, name, relay, pin in ((XL, "LOAD", "K_LOAD", "GPIO25"),
                                (XC, "CHARGER\n16.8 V", "K_CHARGE", "GPIO26")):
        d += elm.Line().at((x, YP)).to((x, 4.95)).color(TEAL)
        rect(d, x - 1.08, 3.85, x + 1.08, 4.95, GREY)
        txt(d, x, 4.40, name, BLACK, size=12.5)
        d += elm.Line().at((x, 3.85)).to((x, 3.35)).color(TEAL)
        d += elm.Switch(action="open").at((x, 3.35)).to((x, 1.75)).color(AMBER)
        d += elm.Line().at((x, 1.75)).to((x, YN)).color(TEAL)
        txt(d, x + 0.78, 2.55, "%s\n%s" % (relay, pin), AMBER, ha="left", size=12.5)

    # ── measurement points on the cells ─────────────────────────────────
    d += elm.MeterV().at((-3.0, 4.4)).right().length(1.0).color(NAVY)
    d += elm.Line().at((-2.0, 4.4)).to((-0.35, 4.4)).color(NAVY).linestyle("--")
    txt(d, -2.5, 5.35, "ADS1115\n4 cell taps", NAVY, size=12.5)

    d += elm.Thermistor().at((-3.2, 1.9)).right().length(1.4).color(AMBER)
    d += elm.Line().at((-1.8, 1.9)).to((-0.35, 1.9)).color(AMBER).linestyle("--")
    txt(d, -2.5, 0.85, "4 × NTC\non the cells", AMBER, size=12.5)

    save_schemdraw(d, "r1_schematic")
