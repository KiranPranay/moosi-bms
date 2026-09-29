"""First review - block diagram of the two-layer system.

Drawn from docs/current-architecture.md (revision 2.1). Layer A is the
hardware BMS, which protects the cells on its own; Layer B is the ESP32
supervisor that adds early warning and separate charge / load control.

Laid out wide (about 2.2 : 1) so it fills a 16:9 slide: the power path runs
along the top, Layer B sits in the band below, and the outputs are on the right.
"""
from _style import (canvas, box, anchor, arrow, group, caption, save, check_layout,
                    NAVY, BLUE, TEAL, AMBER, RED, GREEN, GREY)

fig, ax = canvas(18.0, 8.25, scale=0.72)
PY_, BY = 7.10, 2.85          # power-row centre, Layer B centre line

# ── power path along the top ────────────────────────────────────────────
pack = box(ax, 1.55, PY_, 2.70, 1.55,
           ["4S1P pack", "4 × NCR18650GA", "14.4 V nom · 16.8 V max"], TEAL, fs=12.5)
bms = box(ax, 5.35, PY_, 3.40, 1.55,
          ["Layer A · hardware BMS", "OV 4.25 V · UV 2.7 V", "over-current · short circuit",
           "passive balancing"], AMBER, fs=12.5)
fuse = box(ax, 8.35, PY_, 1.40, 0.90, ["Fuse", "7.5 A"], RED, fs=12.5)
shunt = box(ax, 10.15, PY_, 1.50, 0.90, ["Shunt", "5 mΩ"], NAVY, fs=12.5)
load = box(ax, 13.65, 7.70, 3.00, 0.88, ["Load branch", "LOAD+ / LOAD−"], TEAL, fs=12.5)
chg = box(ax, 13.65, 6.50, 3.00, 0.88, ["Charge branch", "16.8 V · 1.5 A charger"], TEAL, fs=12.5)

arrow(ax, anchor(pack, "R"), anchor(bms, "L"), None, color=TEAL, lw=2.2)
ax.text(3.28, 8.08, "B− B1 B2 B3 B+", ha="center", va="center", fontsize=11, color=TEAL)
arrow(ax, anchor(bms, "R"), anchor(fuse, "L"), "P+", fs=11.5, lab_dy=0.24, color=TEAL, lw=2.2)
arrow(ax, anchor(fuse, "R"), anchor(shunt, "L"), None, color=TEAL, lw=2.2)
arrow(ax, anchor(shunt, "R"), anchor(load, "L"), None, color=TEAL, lw=2.2,
      waypoints=[(11.55, PY_), (11.55, 7.70)])
arrow(ax, (11.55, PY_), anchor(chg, "L"), None, color=TEAL, lw=2.2, waypoints=[(11.55, 6.50)])
ax.plot([11.55], [PY_], marker="o", ms=6, color=TEAL, zorder=5)
ax.text(11.55, 8.38, "FUSED+", ha="center", va="center", fontsize=11, color=TEAL)

# ── Layer B ─────────────────────────────────────────────────────────────
group(ax, 3.35, 0.70, 14.25, 5.30, "Layer B · ESP32 supervisor", NAVY)
ads = box(ax, 5.10, 4.15, 2.50, 1.00, ["ADS1115", "4 cell taps · 16-bit"], BLUE, fs=12)
ntc = box(ax, 5.10, 1.55, 2.50, 1.00, ["4 × NTC 10 kΩ", "ADC1 · GPIO32–35"], AMBER, fs=12)
esp = box(ax, 8.90, BY, 3.20, 1.75,
          ["ESP32", "samples at 5 Hz", "dT/dt over 30 s", "latched state machine"], NAVY, fs=12.5)
ina = box(ax, 12.40, 4.15, 2.30, 1.00, ["INA226", "pack current"], BLUE, fs=12)
alarm = box(ax, 12.40, 1.55, 2.30, 1.00, ["Alarm", "buzzer + LED"], RED, fs=12)

arrow(ax, anchor(ads, "R"), (7.85, anchor(esp, "T")[1]), None,
      color=BLUE, waypoints=[(7.85, 4.15)])
arrow(ax, anchor(ina, "L"), (9.95, anchor(esp, "T")[1]), None,
      color=BLUE, waypoints=[(9.95, 4.15)])
arrow(ax, anchor(ntc, "R"), (7.85, anchor(esp, "B")[1]), None,
      color=AMBER, waypoints=[(7.85, 1.55)])
arrow(ax, (9.95, anchor(esp, "B")[1]), anchor(alarm, "L"), None,
      color=RED, waypoints=[(9.95, 1.55)])

# ── supply and sensing links ────────────────────────────────────────────
lm = box(ax, 1.75, BY, 2.10, 1.30, ["LM2596", "P+ / P− → 5 V", "ESP32 + relays"], GREEN, fs=12)
arrow(ax, anchor(lm, "R"), anchor(esp, "L"), "5 V", fs=11, lab_dx=-0.90, lab_dy=0.24, color=GREEN)
arrow(ax, (2.50, anchor(pack, "B")[1]), anchor(ads, "L"), "cell taps", fs=11, lab_dx=-0.55, lab_dy=0.95,
      color=BLUE, dashed=True, waypoints=[(2.50, 4.15)])
arrow(ax, (0.32, anchor(pack, "B")[1]), anchor(ntc, "L"), "bonded to cells", fs=11,
      lab_dx=0.14, lab_dy=2.30, color=AMBER, dashed=True, waypoints=[(0.32, 1.55)], lab_ha="left")
arrow(ax, anchor(shunt, "B"), anchor(ina, "T"), "Kelvin sense", fs=11, lab_dx=0.95, lab_dy=0.0,
      color=NAVY, dashed=True, waypoints=[(10.15, 5.65), (12.40, 5.65)])

# ── outputs on the right ────────────────────────────────────────────────
relay = box(ax, 16.45, 4.15, 2.95, 1.45,
            ["2-channel relay", "K_LOAD · K_CHARGE", "open on reset"], AMBER, fs=12)
dash = box(ax, 16.45, 1.55, 2.95, 1.00, ["Wi-Fi dashboard", "monitoring only"], GREEN, fs=12)

arrow(ax, (anchor(esp, "R")[0], 3.30), anchor(relay, "L"), None, color=AMBER, waypoints=[(14.55, 3.30), (14.55, 4.15)])
arrow(ax, (anchor(esp, "R")[0], 2.40), anchor(dash, "L"), None, color=GREEN, waypoints=[(14.75, 2.40), (14.75, 1.55)])
arrow(ax, anchor(relay, "T"), anchor(chg, "R"), None, color=AMBER,
      waypoints=[(16.45, 6.50)])
arrow(ax, (16.45, 6.50), anchor(load, "R"), None, color=AMBER, waypoints=[(16.45, 7.70)])
ax.text(16.60, 5.55, "switches P−", ha="left", va="center", fontsize=11)

# link labels placed by hand, each on a clear stretch of its own line
for x, y, t in ((7.10, 4.40, "I²C"), (10.60, 4.40, "I²C"), (7.10, 1.80, "ADC1"),
                (10.65, 1.30, "GPIO27"), (12.40, 3.06, "GPIO25 / 26"), (12.40, 2.64, "Wi-Fi")):
    ax.text(x, y, t, ha="center", va="center", fontsize=11, zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

caption(ax, 9.0, 0.28,
        "Layer A protects the cells on its own. Layer B adds early warning and separate "
        "charge and load control, and opens both relays if it fails.", fs=11.5)
check_layout()
save(fig, "r1_block_diagram")
