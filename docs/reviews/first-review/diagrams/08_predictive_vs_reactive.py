"""08 - Why a rate trip fires earlier than a fixed temperature trip.

Simulated curve for illustration. The cell warms slowly, then self-heating
takes over and the temperature climbs exponentially. A fixed 60 °C trip waits
for the absolute value; the rate trip fires as soon as the climb starts.
"""
import numpy as np
from _style import (plt, save, NAVY, RED, GREEN, AMBER, GREY, BLACK)

T_AMB, DRIFT, T_KNEE, TAU = 30.0, 0.05, 20.0, 6.0
RATE_TRIP, ABS_TRIP = 1.0, 60.0

t = np.linspace(0, 46, 4600)
T = np.where(t < T_KNEE,
             T_AMB + DRIFT * t,
             T_AMB + DRIFT * T_KNEE + (np.exp((t - T_KNEE) / TAU) - 1.0))
dT = np.gradient(T, t)

t_rate = t[np.argmax(dT >= RATE_TRIP)]
t_abs = t[np.argmax(T >= ABS_TRIP)]
T_rate = T[np.argmax(dT >= RATE_TRIP)]
gained = t_abs - t_rate

fig, ax = plt.subplots(figsize=(13.2, 6.6))
ax2 = ax.twinx()

ax.plot(t, T, color=NAVY, lw=3.0, label="Cell temperature", zorder=5)
ax2.plot(t, dT, color=AMBER, lw=2.2, ls="--", label="Rate of change  dT/dt", zorder=4)

ax.axhline(ABS_TRIP, color=RED, lw=1.6, ls=":", zorder=2)
ax.text(0.4, ABS_TRIP + 1.4, "fixed limit  60 °C", color=RED, fontsize=13, va="bottom")
ax2.axhline(RATE_TRIP, color=AMBER, lw=1.6, ls=":", zorder=2)
ax2.text(45.6, RATE_TRIP + 0.12, "rate limit  1 °C/s", color=AMBER, fontsize=13,
         va="bottom", ha="right")

ax.axvspan(t_rate, t_abs, color=GREEN, alpha=0.13, zorder=1)
for xt, col in ((t_rate, GREEN), (t_abs, RED)):
    ax.axvline(xt, color=col, lw=1.8, zorder=3)

ax.plot([t_rate], [T_rate], "o", ms=11, mfc=GREEN, mec="white", mew=2, zorder=7)
ax.plot([t_abs], [ABS_TRIP], "o", ms=11, mfc=RED, mec="white", mew=2, zorder=7)

ax.annotate("rate trip fires here\n%.1f s, cell at %.0f °C" % (t_rate, T_rate),
            xy=(t_rate, T_rate), xytext=(t_rate - 15.5, 62),
            fontsize=13, color=GREEN, ha="left",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
ax.annotate("fixed trip fires here\n%.1f s, cell at 60 °C" % t_abs,
            xy=(t_abs, ABS_TRIP), xytext=(t_abs - 13.0, 92),
            fontsize=13, color=RED, ha="left",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
ax.annotate("", xy=(t_rate, 20), xytext=(t_abs, 20),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2.2))
ax.text((t_rate + t_abs) / 2, 23.0, "%.1f s earlier" % gained, color=GREEN,
        fontsize=15, fontweight="bold", ha="center")

ax.set_xlabel("Time  (s)", fontsize=14)
ax.set_ylabel("Cell temperature  (°C)", fontsize=14, color=NAVY)
ax2.set_ylabel("dT/dt  (°C/s)", fontsize=14, color=AMBER)
ax.set_xlim(0, 46); ax.set_ylim(15, 105); ax2.set_ylim(0, 6.0)
ax.tick_params(labelsize=12); ax2.tick_params(labelsize=12, colors=AMBER)
ax.spines["top"].set_visible(False); ax2.spines["top"].set_visible(False)
ax.grid(True, color="#E6E6E6", lw=0.9, zorder=0)
ax.set_axisbelow(True)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=13, frameon=True,
          framealpha=0.95, edgecolor="#DDDDDD")
ax.set_title("Simulated thermal runaway — illustrative curve, not measured data",
             fontsize=13, color=GREY, style="italic", pad=12)
fig.tight_layout()
save(fig, "08_predictive_vs_reactive")
print("   rate trip %.2f s (%.1f °C) · fixed trip %.2f s · gained %.2f s"
      % (t_rate, T_rate, t_abs, gained))
