"""First review - methodology: the supervisory control loop.

Follows section 8 of docs/current-architecture.md: 5 Hz sampling, a
median-of-5 stage, a 10 s low-pass, dT/dt by linear regression over the last
30 s, plausibility checks, warning and trip limits, and latched trips that need
a manual reset.

Laid out wide (about 2.3 : 1) so it fills a 16:9 slide: the acquisition chain
runs left to right along the top, the decisions run right to left through the
middle, and each decision's action hangs below it.
"""
from _style import (canvas, box, diamond, stadium, anchor, arrow, caption, save,
                    check_layout, NAVY, BLUE, AMBER, RED, GREEN, GREY)

fig, ax = canvas(17.0, 7.5, scale=0.82)
TOP, MID, ACT, RAIL = 6.45, 4.10, 1.85, 0.95

# ── acquisition, left to right ──────────────────────────────────────────
st = stadium(ax, 0.95, TOP, 1.40, 0.56, "START", GREEN, fs=12.5)
ini = box(ax, 3.55, TOP, 2.70, 1.10, ["Initialise", "ADS1115 and INA226", "both relays OPEN"], NAVY, fs=12)
smp = box(ax, 6.65, TOP, 2.70, 1.10, ["Sample at 5 Hz", "4 cell taps · current", "4 NTC temperatures"], BLUE, fs=12)
flt = box(ax, 9.75, TOP, 2.70, 1.10, ["Filter", "median of 5 samples", "then 10 s low-pass"], BLUE, fs=12)
cmp_ = box(ax, 13.05, TOP, 3.10, 1.10, ["Compute", "cell voltages by subtraction", "dT/dt over a 30 s window"], NAVY, fs=12)

arrow(ax, anchor(st, "R"), anchor(ini, "L"))
arrow(ax, anchor(ini, "R"), anchor(smp, "L"))
arrow(ax, anchor(smp, "R"), anchor(flt, "L"))
arrow(ax, anchor(flt, "R"), anchor(cmp_, "L"))

# ── decisions, right to left ────────────────────────────────────────────
d1 = diamond(ax, 15.40, MID, 2.90, 1.40, ["Sensors", "plausible?"], AMBER, fs=12)
d2 = diamond(ax, 11.40, MID, 2.90, 1.40, ["Trip limit", "crossed?"], AMBER, fs=12)
d3 = diamond(ax, 7.40, MID, 2.90, 1.40, ["Warning limit", "crossed?"], AMBER, fs=12)
pub = box(ax, 3.20, MID, 2.90, 1.00, ["Publish telemetry", "Wi-Fi dashboard"], GREEN, fs=12)

arrow(ax, anchor(cmp_, "R"), anchor(d1, "T"), None, waypoints=[(15.40, TOP)])
arrow(ax, anchor(d1, "L"), anchor(d2, "R"), "yes", fs=11.5, lab_dy=0.24)
arrow(ax, anchor(d2, "L"), anchor(d3, "R"), "no", fs=11.5, lab_dy=0.24)
arrow(ax, anchor(d3, "L"), anchor(pub, "R"), "no", fs=11.5, lab_dy=0.24)

# ── actions below each decision ─────────────────────────────────────────
a1 = box(ax, 15.40, ACT, 2.90, 1.10, ["Sensor fault", "open both relays", "latch the fault"], RED, fs=12)
a2 = box(ax, 11.40, ACT, 3.20, 1.10, ["Trip", "open the affected relay", "latch, log, alarm"], RED, fs=12)
a3 = box(ax, 7.40, ACT, 2.90, 1.10, ["Warning", "alarm on", "both branches stay on"], AMBER, fs=12)

arrow(ax, anchor(d1, "B"), anchor(a1, "T"), "no", fs=11.5, lab_dx=0.30, lab_dy=0.0, color=RED)
arrow(ax, anchor(d2, "B"), anchor(a2, "T"), "yes", fs=11.5, lab_dx=0.34, lab_dy=0.0, color=RED)
arrow(ax, anchor(d3, "B"), anchor(a3, "T"), "yes", fs=11.5, lab_dx=0.34, lab_dy=0.0, color=AMBER)

# every outcome is published: a rail under the actions leads back to Publish
for a in (a1, a2, a3):
    ax.plot([anchor(a, "B")[0]] * 2, [anchor(a, "B")[1], RAIL], color=GREY, lw=1.7, zorder=1)
ax.plot([3.20, 15.40], [RAIL, RAIL], color=GREY, lw=1.7, zorder=1)
arrow(ax, (3.20, RAIL), anchor(pub, "B"), None, color=GREY)

# then the loop repeats from sampling
arrow(ax, anchor(pub, "T"), anchor(smp, "B"), "repeat", fs=11.5, lab_dx=-1.55, lab_dy=0.24,
      color=GREY, waypoints=[(3.20, 5.30), (6.65, 5.30)])

caption(ax, 8.5, 0.30,
        "Every trip stays latched. Manual reset only after 60 s healthy: "
        "all cells 3.20–4.10 V and all NTCs below 40 °C.", fs=11.5)
check_layout()
save(fig, "r1_methodology")
