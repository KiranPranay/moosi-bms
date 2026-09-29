"""Review-1 - block diagram of the two-layer system.

Drawn from docs/current-architecture.md (revision 2.1). Layer A is the
hardware BMS, which protects the cells on its own; Layer B is the ESP32
supervisor that adds early warning and separate charge / load control.
"""
from _style import (canvas, box, anchor, arrow, group, caption, save, check_layout,
                    NAVY, BLUE, TEAL, AMBER, RED, GREEN, GREY)

fig, ax = canvas(15.0, 9.3, scale=0.76)

# ── power path, top band ────────────────────────────────────────────────
pack = box(ax, 1.50, 7.80, 2.70, 1.62,
           ["4S1P pack", "4 × NCR18650GA", "14.4 V nom · 16.8 V max", "3.3 Ah"], TEAL, fs=12.5)
bms = box(ax, 5.20, 7.80, 3.35, 1.62,
          ["Layer A · hardware BMS", "OV 4.25 V · UV 2.7 V", "over-current · short circuit",
           "passive balancing"], AMBER, fs=12.5)
fuse = box(ax, 8.18, 7.80, 1.40, 0.92, ["Fuse", "7.5 A"], RED, fs=12.5)
shunt = box(ax, 9.88, 7.80, 1.50, 0.92, ["Shunt", "5 mΩ"], NAVY, fs=12.5)
load = box(ax, 13.10, 8.45, 3.20, 0.92, ["Load branch", "LOAD+ / LOAD−"], TEAL, fs=12.5)
chg = box(ax, 13.10, 7.05, 3.20, 0.92, ["Charge branch", "16.8 V · 1.5 A charger"], TEAL, fs=12.5)

arrow(ax, anchor(pack, "R"), anchor(bms, "L"), None, color=TEAL, lw=2.2)
ax.text(3.18, 8.92, "B− B1 B2 B3 B+", ha="center", va="center", fontsize=11, color=TEAL)
arrow(ax, anchor(bms, "R"), anchor(fuse, "L"), "P+", fs=11.5, lab_dy=0.24, color=TEAL, lw=2.2)
arrow(ax, anchor(fuse, "R"), anchor(shunt, "L"), None, color=TEAL, lw=2.2)
arrow(ax, anchor(shunt, "R"), anchor(load, "L"), None, color=TEAL, lw=2.2,
      waypoints=[(11.05, 7.80), (11.05, 8.45)])
arrow(ax, (11.05, 7.80), anchor(chg, "L"), None, color=TEAL, lw=2.2,
      waypoints=[(11.05, 7.05)])
ax.plot([11.05], [7.80], marker="o", ms=6, color=TEAL, zorder=5)
ax.text(11.05, 8.80, "FUSED+", ha="center", va="center", fontsize=11, color=TEAL)

# ── Layer B ─────────────────────────────────────────────────────────────
group(ax, 3.30, 0.55, 10.75, 5.85, "Layer B · ESP32 supervisor", NAVY)
esp = box(ax, 7.00, 3.15, 3.10, 1.72,
          ["ESP32", "samples at 5 Hz", "dT/dt over 30 s", "latched state machine"], NAVY, fs=12.5)
ads = box(ax, 4.60, 4.85, 2.25, 1.05, ["ADS1115", "4 cell taps · 16-bit"], BLUE, fs=12)
ina = box(ax, 9.40, 4.85, 2.25, 1.05, ["INA226", "pack current"], BLUE, fs=12)
ntc = box(ax, 4.60, 1.55, 2.25, 1.05, ["4 × NTC 10 kΩ", "ADC1 · GPIO32–35"], AMBER, fs=12)
alarm = box(ax, 9.55, 1.28, 2.25, 1.05, ["Alarm", "buzzer + LED"], RED, fs=12)

arrow(ax, anchor(ads, "R"), (6.20, 4.01), "I²C", fs=11, lab_dx=0.30, lab_dy=-0.42,
      color=BLUE, waypoints=[(6.20, 4.85)])
arrow(ax, anchor(ina, "L"), (7.80, 4.01), "I²C", fs=11, lab_dx=-0.30, lab_dy=-0.42,
      color=BLUE, waypoints=[(7.80, 4.85)])
arrow(ax, anchor(ntc, "R"), (6.20, 2.29), "ADC1", fs=11, lab_dx=0.40, lab_dy=0.38,
      color=AMBER, waypoints=[(6.20, 1.55)])
arrow(ax, (8.50, 2.29), (8.50, 1.805), "GPIO27", fs=11, lab_dx=0.60, lab_dy=0.0, color=RED)

# sensing links up to the power path
arrow(ax, (2.55, 6.99), anchor(ads, "L"), "cell taps", fs=11, lab_dx=-0.50, lab_dy=1.45,
      color=BLUE, dashed=True, waypoints=[(2.55, 4.85)])
arrow(ax, (0.30, 6.99), anchor(ntc, "L"), "bonded to cells", fs=11, lab_dx=0.15, lab_dy=2.85,
      color=AMBER, dashed=True, waypoints=[(0.30, 1.55)], lab_ha="left")
arrow(ax, anchor(shunt, "B"), anchor(ina, "T"), "Kelvin sense", fs=11, lab_dx=0.92, lab_dy=0.05,
      color=NAVY, dashed=True, waypoints=[(9.88, 5.95), (9.40, 5.95)])

# ── outputs on the right ────────────────────────────────────────────────
relay = box(ax, 13.10, 4.25, 3.20, 1.55,
            ["2-channel relay", "K_LOAD · K_CHARGE", "normally open · OFF on reset"], AMBER, fs=12)
dash = box(ax, 13.10, 1.55, 3.20, 1.05, ["Wi-Fi dashboard", "monitoring only"], GREEN, fs=12)
lm = box(ax, 1.72, 3.15, 2.10, 1.30, ["LM2596", "P+ / P− → 5.0 V", "ESP32 + relays"], GREEN, fs=12)

arrow(ax, (8.55, 3.55), anchor(relay, "L"), "GPIO25 / 26", fs=11, lab_dx=-1.30, lab_dy=-0.47,
      color=AMBER, waypoints=[(11.05, 3.55), (11.05, 4.25)])
arrow(ax, anchor(relay, "T"), anchor(chg, "B"), "switches P−", fs=11, lab_dx=0.95, lab_dy=0.0,
      color=AMBER)
arrow(ax, (8.55, 2.75), anchor(dash, "L"), "Wi-Fi", fs=11, lab_dx=-1.25, lab_dy=1.43,
      color=GREEN, waypoints=[(11.35, 2.75), (11.35, 1.55)])
arrow(ax, anchor(lm, "R"), (5.45, 3.15), "5 V", fs=11, lab_dy=0.24, color=GREEN)

caption(ax, 7.5, 0.18,
        "Layer A protects the cells on its own. Layer B adds early warning and separate "
        "charge and load control, and opens both relays if it fails.", fs=11.5)
check_layout()
save(fig, "r1_block_diagram")
