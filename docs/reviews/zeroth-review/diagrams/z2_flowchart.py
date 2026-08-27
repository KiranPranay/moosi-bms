"""Zeroth review - what the firmware does, in outline."""
from _style import (canvas, box, diamond, stadium, anchor, arrow, save, caption,
                    check_layout, NAVY, BLUE, AMBER, RED, GREEN, GREY)

fig, ax = canvas(8.4, 7.2, scale=0.92)

st    = stadium(ax, 2.60, 6.62, 2.30, 0.52, "START", GREEN, fs=13)
read  = box(ax, 2.60, 5.62, 4.40, 0.82,
            ["Read the sensors", "voltage · current · temperature"], BLUE, fs=12.5)
rate  = box(ax, 2.60, 4.52, 4.40, 0.82,
            ["Work out dT/dt", "how fast each cell is heating"], NAVY, fs=12.5)
chk   = diamond(ax, 2.60, 3.20, 4.20, 1.45,
                ["Rising too fast,", "or a limit crossed?"], AMBER, fs=12.5)
cut   = box(ax, 6.75, 3.20, 2.90, 1.10,
            ["Cut off", "charging and", "discharging"], RED, fs=12.5)
pub   = box(ax, 2.60, 1.75, 4.40, 0.78,
            ["Send the readings", "to the dashboard"], GREEN, fs=12.5)
wait  = box(ax, 2.60, 0.72, 4.40, 0.62, ["Wait for the next reading"], GREY,
            fs=12.5, bold_first=False)

arrow(ax, anchor(st, "B"), anchor(read, "T"))
arrow(ax, anchor(read, "B"), anchor(rate, "T"))
arrow(ax, anchor(rate, "B"), anchor(chk, "T"))
arrow(ax, anchor(chk, "R"), anchor(cut, "L"), "yes", fs=12, lab_dy=0.28, color=RED)
arrow(ax, anchor(chk, "B"), anchor(pub, "T"), "no", fs=12, lab_dx=0.36, lab_dy=0.04)
arrow(ax, anchor(pub, "B"), anchor(wait, "T"))
arrow(ax, anchor(wait, "L"), anchor(read, "L"), None, color=GREY,
      waypoints=[(0.30, 0.72), (0.30, 5.62)])
caption(ax, 0.78, 6.18, "repeat", fs=12, color=GREY)

check_layout()
save(fig, "z2_flowchart")
