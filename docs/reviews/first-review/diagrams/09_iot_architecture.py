"""09 - How readings reach the dashboard."""
from _style import (canvas, box, anchor, arrow, group, caption, save, check_layout,
                    NAVY, BLUE, TEAL, GREEN, GREY, MONO, BLACK)

fig, ax = canvas(16.0, 7.1)

group(ax, 0.35, 3.45, 9.55, 6.95, "On the ESP32", NAVY)
t1 = box(ax, 2.40, 5.95, 3.50, 0.88, ["Sensor task", "10 Hz · reads and filters"], BLUE, fs=11.5)
t2 = box(ax, 2.40, 4.45, 3.50, 0.88, ["Safety task", "dT/dt and the limits"], NAVY, fs=11.5)
enc = box(ax, 7.30, 5.20, 3.70, 1.45,
          ["Telemetry task", "builds one JSON message", "once a second"], TEAL, fs=11.5)
srv = box(ax, 12.75, 5.20, 4.90, 1.45,
          ["WebSocket server", "ESPAsyncWebServer, port 80", "endpoint  /ws"], GREEN, fs=11.5)
brw = box(ax, 12.75, 2.15, 4.90, 1.75,
          ["Dashboard in the browser", "plain HTML and JavaScript",
           "live gauges, charts and state", "no install, no build step"], GREEN, fs=11.5)

# merge the two tasks into the encoder without stray arrowheads
ax.plot([4.15, 4.80], [5.95, 5.95], color=GREY, lw=1.7, zorder=1)
ax.plot([4.15, 4.80], [4.45, 4.45], color=GREY, lw=1.7, zorder=1)
ax.plot([4.80, 4.80], [4.45, 5.95], color=GREY, lw=1.7, zorder=1)
ax.plot([4.80], [5.20], marker="o", ms=6, color=GREY, zorder=3)
arrow(ax, (4.80, 5.20), anchor(enc, "L"), None, color=GREY)

arrow(ax, anchor(enc, "R"), anchor(srv, "L"), "JSON", fs=11.5, lab_dy=0.28, color=TEAL)
arrow(ax, anchor(srv, "B"), anchor(brw, "T"), "over Wi-Fi", fs=11.5, lab_dx=1.25, color=GREEN)
arrow(ax, anchor(brw, "R"), anchor(srv, "R"), "reset the latch", fs=11,
      lab_dx=1.05, lab_dy=0.0, color=GREY, dashed=True,
      waypoints=[(15.55, 2.15), (15.55, 5.20)])

ax.text(0.55, 2.95, "One message looks like this", fontsize=11.5, color=GREY,
        style="italic", ha="left", va="top")
for i, line in enumerate([
        "{",
        '  "cell_mv" : [4141, 4138, 4150, 4133],',
        '  "pack_ma" : 2480,',
        '  "temp_c"  : [31.2, 30.8, 32.5, 31.0],',
        '  "dtdt"    : [0.02, 0.01, 0.31, 0.02],',
        '  "state"   : "NORMAL",',
        '  "uptime_s": 4312',
        "}"]):
    ax.text(0.55, 2.55 - i * 0.275, line, fontsize=11.5, family=MONO,
            color=BLACK, ha="left", va="top")

caption(ax, 12.75, 0.55, "A phone and a laptop open the same page on the local network.", fs=11)
check_layout()
save(fig, "09_iot_architecture")
