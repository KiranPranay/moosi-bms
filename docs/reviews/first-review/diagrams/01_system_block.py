"""01 — High-level system block diagram.

Two lanes: the power path along the top, the signal/control chain below.
Every box and label is placed at an explicit coordinate so nothing can
collide; cross-lane arrows run in the clear band between the two lanes.
"""
from _style import (canvas, box, anchor, arrow, group, caption, save,
                    NAVY, BLUE, TEAL, AMBER, GREEN, GREY)

fig, ax = canvas(15.6, 7.4, scale=0.78)

POWER_Y, SIG_Y = 5.85, 2.55          # lane centre lines
GAP_Y = 4.15                          # clear band between the lanes

# ── power lane ──────────────────────────────────────────────────────────
group(ax, 0.35, 4.55, 15.25, 7.15, "Power path", TEAL)
pack = box(ax, 2.55, POWER_Y, 3.5, 1.55,
           ["4S Li-ion Pack", "4 × 18650  ·  14.8 V nom", "16.8 V max  ·  ≤ 10 A"], TEAL, fs=13)
prot = box(ax, 7.90, POWER_Y, 3.9, 1.55,
           ["Protection Stage", "charge + discharge MOSFETs", "fuse · back-to-back, low side"], AMBER, fs=13)
load = box(ax, 13.05, POWER_Y, 3.4, 1.55,
           ["Charger / Load", "shared ground"], TEAL, fs=13)

arrow(ax, anchor(pack, "R"), anchor(prot, "L"), "pack current", lw=2.6, color=TEAL, fs=12)
arrow(ax, anchor(prot, "R"), anchor(load, "L"), "switched power", lw=2.6, color=TEAL, fs=12, both=True)

# ── signal lane ─────────────────────────────────────────────────────────
group(ax, 0.35, 0.35, 15.25, 3.75, "Sensing, control and telemetry", BLUE)
sense = box(ax, 2.55, SIG_Y, 3.5, 1.60,
            ["Sensing Front End", "4 × cell-tap dividers", "4 × NTC via CD4051 mux",
             "INA226 shunt monitor"], BLUE, fs=12)
esp = box(ax, 7.90, SIG_Y, 3.9, 1.60,
          ["ESP32", "acquisition · filtering", "dT/dt prediction", "safety state machine"], NAVY, fs=12)
wifi = box(ax, 11.55, SIG_Y, 1.95, 1.00, ["Wi-Fi", "802.11 b/g/n"], GREEN, fs=12)
dash = box(ax, 14.15, SIG_Y, 1.95, 1.00, ["Dashboard", "browser"], GREEN, fs=12)
bal = box(ax, 4.55, 1.00, 3.0, 0.95,
          ["Passive balancing", "one bleed resistor per cell"], GREY, fs=11.5)

arrow(ax, anchor(sense, "R"), anchor(esp, "L"), "ADC1 · I²C", fs=12)
arrow(ax, anchor(esp, "R"), anchor(wifi, "L"), "JSON", fs=12)
# label lifted above both boxes — the 0.65 gap is too narrow to hold it inline
arrow(ax, anchor(wifi, "R"), anchor(dash, "L"), "WebSocket", fs=11, lab_dy=0.72)

# ── cross-lane links, both vertical, inside the clear band ──────────────
arrow(ax, (1.65, POWER_Y - 0.775), (1.65, SIG_Y + 0.80),
      "cell taps", fs=12, lab_dx=0.72, lab_dy=0.0, color=BLUE)
arrow(ax, (9.10, SIG_Y + 0.80), (9.10, POWER_Y - 0.775),
      "gate drive", fs=12, lab_dx=0.82, lab_dy=0.0, color=AMBER)

arrow(ax, anchor(esp, "B"), (7.90, 1.00), None, color=GREY)
arrow(ax, (7.90, 1.00), anchor(bal, "R"), "enable", fs=11, lab_dy=0.24, color=GREY)

caption(ax, 7.8, 0.03, "ADC2 is unusable while Wi-Fi is active — every analogue input is on ADC1", fs=11)
save(fig, "01_system_block")
