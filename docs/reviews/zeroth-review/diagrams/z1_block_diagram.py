"""Zeroth review - block diagram of the proposed system.

Kept deliberately high level. The detailed version, with part numbers and pin
assignments, belongs in the first review.
"""
from _style import (canvas, box, anchor, arrow, save, check_layout,
                    NAVY, BLUE, TEAL, AMBER, GREEN, GREY)

fig, ax = canvas(7.6, 7.0, scale=0.92)

pack  = box(ax, 3.70, 6.35, 4.60, 0.90, ["4S Li-ion Pack", "4 × 18650 cells"], TEAL, fs=13)
sense = box(ax, 3.70, 4.95, 6.20, 1.10,
            ["Sensing", "cell voltages · pack current", "cell temperatures"], BLUE, fs=13)
esp   = box(ax, 3.70, 3.30, 6.20, 1.30,
            ["ESP32 Controller", "filters the readings, works out how",
             "fast the temperature is rising, decides"], NAVY, fs=13)
prot  = box(ax, 2.05, 1.70, 3.00, 0.95, ["Protection", "MOSFET cut-off"], AMBER, fs=13)
wifi  = box(ax, 5.35, 1.70, 3.00, 0.95, ["Wi-Fi", "sends the readings"], GREEN, fs=13)
load  = box(ax, 2.05, 0.48, 3.00, 0.72, ["Charger / Load"], TEAL, fs=13, bold_first=False)
dash  = box(ax, 5.35, 0.48, 3.00, 0.72, ["Dashboard"], GREEN, fs=13, bold_first=False)

arrow(ax, anchor(pack, "B"), anchor(sense, "T"))
arrow(ax, anchor(sense, "B"), anchor(esp, "T"))
arrow(ax, (2.05, 2.65), anchor(prot, "T"), "switch", fs=12, lab_dx=-0.82, lab_dy=-0.02)
arrow(ax, (5.35, 2.65), anchor(wifi, "T"), "publish", fs=12, lab_dx=0.88, lab_dy=-0.02)
arrow(ax, anchor(prot, "B"), anchor(load, "T"))
arrow(ax, anchor(wifi, "B"), anchor(dash, "T"))
arrow(ax, anchor(pack, "L"), anchor(prot, "L"), "power", fs=12, lab_dx=-0.20, lab_dy=0.30,
      color=TEAL, lw=2.4, waypoints=[(0.42, 6.35), (0.42, 1.70)])

check_layout()
save(fig, "z1_block_diagram")
