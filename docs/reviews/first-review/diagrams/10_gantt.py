"""10 - Plan for the remaining work, by tracker phase."""
import numpy as np
from _style import plt, save, NAVY, BLUE, TEAL, AMBER, GREEN, GREY, BLACK

# Week 1 starts Monday 31 August 2026.
TASKS = [
    ("Phase 1 · Initial approvals",  0.0,  0.0, GREEN, "done"),
    ("Phase 2 · Procurement",        0.0,  2.0, TEAL,  ""),
    ("Phase 3 · Prototyping",        1.5,  3.5, TEAL,  ""),
    ("Phase 4 · Core software",      3.5,  4.5, NAVY,  ""),
    ("Phase 5 · IoT integration",    6.5,  3.0, BLUE,  ""),
    ("Phase 6 · Final polish",       8.5,  3.5, AMBER, ""),
]
MILESTONES = [(2.0, "parts in hand"), (6.0, "bench prototype runs"),
              (9.5, "dashboard live"), (12.0, "second review")]
MONTHS = [(0, "Sep"), (4.5, "Oct"), (9, "Nov"), (13, "Dec")]

fig, ax = plt.subplots(figsize=(13.6, 6.2))
for i, (name, start, dur, col, note) in enumerate(TASKS):
    y = len(TASKS) - 1 - i
    if dur == 0:
        ax.plot([start + 0.12], [y], marker="D", ms=13, color=col, zorder=4)
        ax.text(start + 0.45, y, "complete", va="center", ha="left",
                fontsize=12, color=col, fontweight="bold")
    else:
        ax.barh(y, dur, left=start, height=0.52, color=col, alpha=0.85,
                edgecolor=col, linewidth=1.6, zorder=3)
        ax.text(start + dur / 2, y, "%g weeks" % dur, va="center", ha="center",
                fontsize=12, color="white", fontweight="bold", zorder=5)

for x, label in MILESTONES:
    ax.axvline(x, color=GREY, lw=1.2, ls=(0, (4, 3)), zorder=1)
    ax.text(x, len(TASKS) - 0.32, label, rotation=0, fontsize=11, color=GREY,
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#DDDDDD"))

ax.set_yticks(range(len(TASKS)))
ax.set_yticklabels([t[0] for t in TASKS][::-1], fontsize=13)
ax.set_xticks(range(0, 14))
ax.set_xticklabels(["W%d" % w if w else "" for w in range(0, 14)], fontsize=11)
ax.set_xlim(-0.3, 13.2)
ax.set_ylim(-0.75, len(TASKS) + 0.45)
ax.set_xlabel("Weeks from 31 August 2026", fontsize=13)

for x, m in MONTHS:
    ax.text(x, -0.62, m, fontsize=12, color=BLACK, fontweight="bold", ha="left")

ax.grid(axis="x", color="#EAEAEA", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
save(fig, "10_gantt")
