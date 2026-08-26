"""02 — Detailed hardware architecture and ESP32 pin map.

Four columns: pack → front end → mux → controller. Signal flow is drawn;
static wiring (mux select, balance gates, buck input) is stated inside the
relevant box so no long arrow has to cross the figure.
The power path itself is diagram 03 (the SLD).
"""
from _style import (canvas, box, anchor, arrow, group, caption, save,
                    check_layout, NAVY, BLUE, TEAL, AMBER, GREEN, GREY, BLACK)

fig, ax = canvas(19.0, 8.6)

# ── column 1 · pack with cell taps ──────────────────────────────────────
group(ax, 0.45, 3.05, 3.30, 8.05, "4S pack", TEAL)
CELL_Y = [7.30, 6.40, 5.50, 4.60]
for i, y in enumerate(CELL_Y):
    box(ax, 1.62, y, 1.95, 0.72, ["B%d   18650" % (4 - i)], TEAL, fs=13,
        bold_first=False, name="cell%d" % (4 - i))

TAPS = [("T4  pack +", 7.72), ("T3", 6.85), ("T2", 5.95), ("T1", 5.05), ("B−  GND", 4.15)]
for name, y in TAPS:
    ax.plot([2.60], [y], marker="o", ms=6, color=NAVY, zorder=5)
    ax.plot([2.60, 3.10 if name.startswith("B−") else 3.55], [y, y], color=NAVY, lw=1.5, zorder=4)
    ax.text(1.62, y, name, ha="center", va="center", fontsize=11.5, color=NAVY, zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
ax.plot([3.55, 3.55], [5.05, 7.72], color=NAVY, lw=2.0, zorder=4)     # tap bus
ax.text(3.55, 7.92, "4 taps", ha="center", va="bottom", fontsize=12.5, color=NAVY)

# ── column 2 · analogue front end ───────────────────────────────────────
bal = box(ax, 6.10, 8.10, 4.20, 0.74,
          ["Balancing ×4 — 33 Ω bleed + P-FET", "gates: GPIO13 / 14 / 18 / 19"],
          GREY, fs=12, name="balancing")
div = box(ax, 6.10, 6.45, 4.20, 1.85,
          ["Cell-tap dividers ×4", "R1 68 kΩ / R2 10 kΩ  →  ratio 0.128",
           "16.8 V pack tap → 2.15 V at the pin", "1 % metal film + 100 nF"],
          BLUE, fs=13, name="dividers")
ntc = box(ax, 6.10, 4.20, 4.20, 1.45,
          ["NTC thermistors ×4", "10 kΩ B3950, clamped to cell cans",
           "10 kΩ reference + RC filter"], AMBER, fs=13, name="ntc")
ina = box(ax, 6.10, 2.15, 4.20, 1.30,
          ["INA226 + 5 mΩ shunt", "16-bit, bidirectional",
           "I²C — consumes no ADC pin"], TEAL, fs=13, name="ina226")

# ── column 3 · multiplexer ──────────────────────────────────────────────
mux = box(ax, 10.15, 4.20, 2.55, 1.45,
          ["CD4051B", "8 : 1 analogue mux", "select A/B/C from", "GPIO25 / 26 / 27"],
          AMBER, fs=12.5, name="mux")

# ── column 4 · controller and drive ─────────────────────────────────────
esp = box(ax, 15.15, 5.55, 6.30, 4.30,
          ["ESP32-WROOM-32",
           "",
           "GPIO32 · 33 · 34 · 35    cell taps           ADC1",
           "GPIO36                   NTC mux output      ADC1",
           "GPIO39                   spare               ADC1",
           "GPIO25 · 26 · 27         mux select A/B/C",
           "GPIO21 · 22              I²C SDA / SCL",
           "GPIO16 · 17              charge / discharge gate",
           "GPIO13 · 14 · 18 · 19    balance gates",
           "",
           "ADC2 unused — it is shared with the Wi-Fi radio"],
          NAVY, fs=12.5, align="left", name="esp32")
buck = box(ax, 13.00, 1.60, 2.60, 1.40,
           ["MP1584EN buck", "pack + → 3.3 V", "(not an LDO:", "13.5 V drop)"],
           GREEN, fs=12.5, name="buck")
drv = box(ax, 16.55, 1.60, 3.50, 1.40,
          ["TC4420 gate driver", "3.3 V logic in → 5 V gate out",
           "100 kΩ pull-down = fail-safe OFF", "MOSFETs: see SLD (diagram 03)"],
          AMBER, fs=12, name="driver")

# ── arrows ──────────────────────────────────────────────────────────────
arrow(ax, (3.55, 6.45), anchor(div, "L"), None, color=NAVY, lw=1.8)
arrow(ax, (3.30, 4.60), (4.00, 4.60), "on cell cans", fs=12, lab_dy=0.26,
      color=AMBER, dashed=True, lw=1.5)
arrow(ax, (2.62, 3.05), anchor(ina, "L"), "B− current", fs=12, lab_dx=-0.10, lab_dy=0.42,
      color=TEAL, lw=1.5, waypoints=[(2.62, 2.15)])

arrow(ax, anchor(div, "R"), (12.00, 6.45), "GPIO32–35", fs=12.5, lab_dx=1.55, lab_dy=0.26, color=BLUE)
arrow(ax, anchor(ntc, "R"), anchor(mux, "L"), "4 ch", fs=12, lab_dy=0.26, color=AMBER)
arrow(ax, anchor(mux, "R"), (12.00, 4.20), "GPIO36", fs=12.5, lab_dy=0.26, color=AMBER)
arrow(ax, anchor(ina, "R"), (12.00, 3.15), "I²C", fs=12.5, lab_dx=0.55, lab_dy=0.30,
      color=TEAL, waypoints=[(11.30, 2.15), (11.30, 3.15)])

arrow(ax, anchor(buck, "T"), (13.00, 3.40), "3.3 V", fs=12.5, lab_dx=0.62, lab_dy=0.0, color=GREEN)
arrow(ax, (16.55, 3.40), anchor(drv, "T"), "GPIO16 / 17", fs=12.5, lab_dx=1.20, lab_dy=0.0, color=AMBER)

caption(ax, 9.4, 0.38,
        "4 cell taps + 4 thermistors = 8 analogue channels, but a DevKit exposes only 6 ADC1 pins "
        "— so the thermistors are multiplexed",
        fs=12.5)
check_layout()
save(fig, "02_hardware_architecture")
