"""07 - Firmware main loop and safety state machine.

The canvas is kept close to 2.25:1 on purpose. That is the shape of the slide
area the picture lands in, so the drawing fills the full width and the labels
come out as large as they can be.
"""
from _style import (canvas, box, diamond, stadium, anchor, arrow, group, caption,
                    save, check_layout, NAVY, BLUE, TEAL, AMBER, RED, GREEN, GREY)

fig, ax = canvas(14.0, 6.3)
LX, RX = 3.55, 10.45

# ── main loop ───────────────────────────────────────────────────────────
group(ax, 0.28, 0.28, 6.85, 6.02, "Main loop  ·  10 Hz", BLUE)
st   = stadium(ax, LX, 5.58, 2.40, 0.44, "START", GREEN, fs=11.5)
rd   = box(ax, LX, 4.86, 4.25, 0.62, ["Read sensors", "4 taps · 4 NTC · INA226"], BLUE, fs=11)
flt  = box(ax, LX, 4.06, 4.25, 0.62, ["Filter", "median, then EMA (α = 0.2)"], BLUE, fs=11)
der  = box(ax, LX, 3.26, 4.25, 0.62, ["Compute dT/dt per cell", "1 s window, EMA of the slope"], NAVY, fs=11)
chk  = diamond(ax, LX, 2.22, 4.10, 1.20, ["Any limit exceeded?", "OV · UV · OC · OT · dT/dt"], AMBER, fs=11)
pub  = box(ax, LX, 1.16, 4.25, 0.58, ["Publish telemetry", "JSON over WebSocket, 1 Hz"], GREEN, fs=11)
wait = box(ax, LX, 0.60, 4.25, 0.42, ["Wait for the next 100 ms tick"], GREY, fs=11, bold_first=False)

arrow(ax, anchor(st, "B"), anchor(rd, "T"))
arrow(ax, anchor(rd, "B"), anchor(flt, "T"))
arrow(ax, anchor(flt, "B"), anchor(der, "T"))
arrow(ax, anchor(der, "B"), anchor(chk, "T"))
arrow(ax, anchor(chk, "B"), anchor(pub, "T"), "no", fs=11, lab_dx=0.34, lab_dy=0.02)
arrow(ax, anchor(pub, "B"), anchor(wait, "T"))
arrow(ax, anchor(wait, "L"), anchor(rd, "L"), None, color=GREY,
      waypoints=[(0.72, 0.60), (0.72, 4.86)])
caption(ax, 0.98, 2.75, "loop", fs=11, color=GREY)

# ── safety state machine ────────────────────────────────────────────────
group(ax, 7.15, 0.28, 13.72, 6.02, "Safety state machine", RED)
norm = box(ax, RX, 5.55, 4.55, 0.62, ["NORMAL", "charge and discharge enabled"], GREEN, fs=11)
balc = box(ax, RX, 4.65, 4.55, 0.62, ["BALANCING", "bleed the highest cell"], GREY, fs=11)
warn = box(ax, RX, 3.75, 4.55, 0.62, ["WARNING", "flagged, both FETs still on"], AMBER, fs=11)
cut  = box(ax, RX, 2.85, 4.55, 0.62, ["CUTOFF", "both FETs off within 100 ms"], RED, fs=11)
latch= box(ax, RX, 1.95, 4.55, 0.62, ["LATCHED", "off until reset by hand"], RED, fs=11)
box(ax, RX, 0.88, 4.55, 0.78,
    ["Recovery condition", "leave CUTOFF only when dT/dt < 0.2 °C/s",
     "and T < 40 °C, both held for 5 s"], GREEN, fs=10.5)

arrow(ax, anchor(norm, "B"), anchor(balc, "T"), "ΔV > 30 mV", fs=10.5, lab_dx=1.35)
arrow(ax, anchor(balc, "B"), anchor(warn, "T"), "dT/dt ≥ 0.5 °C/s", fs=10.5, lab_dx=1.55)
arrow(ax, anchor(warn, "B"), anchor(cut, "T"), "dT/dt ≥ 1.0 °C/s", fs=10.5, lab_dx=1.55)
arrow(ax, anchor(cut, "B"), anchor(latch, "T"), "3rd trip in 10 min", fs=10.5, lab_dx=1.62)
arrow(ax, anchor(cut, "R"), anchor(norm, "R"), None, color=GREEN,
      waypoints=[(13.28, 2.85), (13.28, 5.55)])
arrow(ax, anchor(chk, "R"), anchor(warn, "L"), "yes", fs=11, lab_dx=-0.15, lab_dy=0.26, color=RED)

check_layout()
save(fig, "07_firmware_flowchart")
