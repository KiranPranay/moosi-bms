"""Review-1 - methodology: the supervisory control loop.

Follows section 8 of docs/current-architecture.md: 5 Hz sampling, a
median-of-5 stage, a 10 s low-pass, dT/dt by linear regression over the last
30 s, plausibility checks, warning and trip limits with persistence, and
latched trips that need a manual reset.
"""
from _style import (canvas, box, diamond, stadium, anchor, arrow, caption, save,
                    check_layout, NAVY, BLUE, TEAL, AMBER, RED, GREEN, GREY)

fig, ax = canvas(14.6, 9.5, scale=0.72)
C1, C2, C3 = 2.35, 7.05, 11.55

# ── column 1: acquisition ───────────────────────────────────────────────
st = stadium(ax, C1, 8.85, 2.20, 0.52, "START", GREEN, fs=12.5)
ini = box(ax, C1, 7.75, 3.70, 1.10,
          ["Initialise", "I²C: ADS1115 and INA226", "both relays OPEN"], NAVY, fs=12)
smp = box(ax, C1, 6.25, 3.70, 1.10,
          ["Sample at 5 Hz", "4 cell taps · current", "4 NTC temperatures"], BLUE, fs=12)
flt = box(ax, C1, 4.75, 3.70, 1.10,
          ["Filter", "median of 5 samples,", "then 10 s low-pass"], BLUE, fs=12)
cmp_ = box(ax, C1, 3.20, 3.70, 1.25,
           ["Compute", "cell voltages by tap subtraction",
            "dT/dt by 30 s linear regression"], NAVY, fs=12)

arrow(ax, anchor(st, "B"), anchor(ini, "T"))
arrow(ax, anchor(ini, "B"), anchor(smp, "T"))
arrow(ax, anchor(smp, "B"), anchor(flt, "T"))
arrow(ax, anchor(flt, "B"), anchor(cmp_, "T"))

# ── column 2: decisions ─────────────────────────────────────────────────
pl = diamond(ax, C2, 7.75, 3.50, 1.40, ["Sensors", "plausible?"], AMBER, fs=12)
tr = diamond(ax, C2, 5.55, 3.50, 1.40, ["Trip limit", "crossed?"], AMBER, fs=12)
wn = diamond(ax, C2, 3.35, 3.50, 1.40, ["Warning limit", "crossed?"], AMBER, fs=12)
pub = box(ax, C2, 1.45, 3.50, 0.95, ["Publish telemetry", "Wi-Fi dashboard"], GREEN, fs=12)

arrow(ax, anchor(cmp_, "R"), anchor(pl, "L"), None, waypoints=[(4.72, 3.20), (4.72, 7.75)])
arrow(ax, anchor(pl, "B"), anchor(tr, "T"), "yes", fs=11.5, lab_dx=0.34, lab_dy=0.02)
arrow(ax, anchor(tr, "B"), anchor(wn, "T"), "no", fs=11.5, lab_dx=0.30, lab_dy=0.02)
arrow(ax, anchor(wn, "B"), anchor(pub, "T"), "no", fs=11.5, lab_dx=0.30, lab_dy=0.02)

# ── column 3: actions ───────────────────────────────────────────────────
flt_act = box(ax, C3, 7.75, 3.55, 1.10,
              ["Sensor fault", "open both relays", "latch the fault"], RED, fs=12)
trp_act = box(ax, C3, 5.55, 3.55, 1.25,
              ["Trip", "open the affected relay", "latch, log the cause, alarm"], RED, fs=12)
wrn_act = box(ax, C3, 3.35, 3.55, 1.10,
              ["Warning", "alarm on", "both branches stay on"], AMBER, fs=12)

arrow(ax, anchor(pl, "R"), anchor(flt_act, "L"), "no", fs=11.5, lab_dy=0.24, color=RED)
arrow(ax, anchor(tr, "R"), anchor(trp_act, "L"), "yes", fs=11.5, lab_dy=0.24, color=RED)
arrow(ax, anchor(wn, "R"), anchor(wrn_act, "L"), "yes", fs=11.5, lab_dy=0.24, color=AMBER)

# every outcome is published, then the loop repeats
for b in (flt_act, trp_act, wrn_act):
    ax.plot([anchor(b, "R")[0], 13.95], [anchor(b, "R")[1]] * 2, color=GREY, lw=1.7, zorder=1)
ax.plot([13.95, 13.95], [7.75, 1.45], color=GREY, lw=1.7, zorder=1)
arrow(ax, (13.95, 1.45), anchor(pub, "R"), None, color=GREY)
arrow(ax, anchor(pub, "B"), anchor(smp, "L"), "repeat", fs=11.5, lab_dx=2.80, lab_dy=0.22,
      color=GREY, waypoints=[(C2, 0.55), (0.25, 0.55), (0.25, 6.25)])

caption(ax, 7.3, 0.10,
        "Every trip stays latched. Manual reset only after 60 s healthy: "
        "all cells 3.20–4.10 V and all NTCs below 40 °C.", fs=11.5)
check_layout()
save(fig, "r1_methodology")
