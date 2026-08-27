"""Shared design tokens for every First Review diagram.

Colours and type are derived from the review-deck template (see
docs/reviews/template-notes.md) so the figures look native to the slides:
a navy accent, black text, white ground, restrained functional hues.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Diagrams for more than one review share this module, so the folder that
# receives the .png / .svg files is set by whichever diagrams package imports it.
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def set_output_dir(path):
    """Write generated figures into `path` instead of next to this module."""
    global OUT_DIR
    OUT_DIR = path

# ── palette ─────────────────────────────────────────────────────────────
NAVY   = "#002060"   # template accent — controller, headings
BLUE   = "#2E5C8A"   # sensing
TEAL   = "#1F6F6B"   # power path
AMBER  = "#B26B00"   # protection, warning
RED    = "#A3231F"   # fault, cut-off
GREEN  = "#2E6B3E"   # normal, healthy
GREY   = "#55575B"   # neutral / secondary
BLACK  = "#000000"
WHITE  = "#FFFFFF"

# matching light fills (tinted, not transparent, so PNG and SVG agree)
FILL = {
    NAVY:  "#E4E9F2", BLUE: "#E6EDF5", TEAL: "#E2F0EF",
    AMBER: "#FBEEDC", RED:  "#F7E4E3", GREEN: "#E5F0E8",
    GREY:  "#EEEFF1",
}

# ── type ────────────────────────────────────────────────────────────────
def _pick(*names):
    have = {f.name for f in font_manager.fontManager.ttflist}
    for n in names:
        if n in have:
            return n
    return "serif"

SERIF = _pick("Times New Roman", "Liberation Serif", "Nimbus Roman", "DejaVu Serif")
MONO  = _pick("DejaVu Sans Mono", "Liberation Mono", "monospace")
# Graphviz resolves this through fontconfig; PowerPoint never sees it.
GV_FONT = SERIF

plt.rcParams.update({
    "font.family": SERIF,
    "font.size": 15,
    "text.color": BLACK,
    "axes.labelcolor": BLACK,
    "axes.edgecolor": GREY,
    "xtick.color": BLACK,
    "ytick.color": BLACK,
    "figure.facecolor": WHITE,
    "savefig.facecolor": WHITE,
    "axes.facecolor": WHITE,
    "svg.fonttype": "path",     # embed outlines so the SVG is self-contained
})

PNG_MIN_WIDTH = 2200           # px — legible when the image fills ~70% of a slide


def save(fig, stem, width_px=PNG_MIN_WIDTH, pad=0.18):
    """Write <stem>.png (>= PNG_MIN_WIDTH wide) and <stem>.svg next to this file."""
    w_in = fig.get_size_inches()[0]
    dpi = max(200, int(round(width_px / w_in)))
    png, svg = os.path.join(OUT_DIR, stem + ".png"), os.path.join(OUT_DIR, stem + ".svg")
    fig.savefig(png, dpi=dpi, bbox_inches="tight", pad_inches=pad, facecolor=WHITE)
    fig.savefig(svg, bbox_inches="tight", pad_inches=pad, facecolor=WHITE)
    plt.close(fig)
    _report(png)


def save_graphviz(g, stem, width_px=PNG_MIN_WIDTH):
    """Render a graphviz.Digraph to <stem>.png and <stem>.svg."""
    base = os.path.join(OUT_DIR, stem)
    g.attr(dpi="220")
    g.render(base, format="png", cleanup=True)
    g.attr(dpi="")
    g.render(base, format="svg", cleanup=True)
    _report(base + ".png")


def _report(png):
    try:
        from PIL import Image
        with Image.open(png) as im:
            w, h = im.size
            extrema = im.convert("L").getextrema()
        blank = extrema[0] == extrema[1]
        flag = "  <-- BLANK!" if blank else ("  <-- NARROW" if w < 1800 else "")
        print("   %-34s %5dx%-5d%s" % (os.path.basename(png), w, h, flag))
    except Exception as exc:                                   # pragma: no cover
        print("   %-34s (could not verify: %s)" % (os.path.basename(png), exc))


def gv_defaults(g, rankdir="LR", nodesep="0.45", ranksep="0.70"):
    """Common Graphviz look: generous spacing so labels never collide."""
    g.attr(rankdir=rankdir, bgcolor="white", nodesep=nodesep, ranksep=ranksep,
           margin="0.15", splines="ortho", fontname=GV_FONT)
    g.attr("node", shape="box", style="filled,rounded", fontname=GV_FONT,
           fontsize="20", margin="0.22,0.16", penwidth="2.0", color=NAVY,
           fillcolor=FILL[NAVY], fontcolor=BLACK)
    g.attr("edge", fontname=GV_FONT, fontsize="16", color=GREY,
           penwidth="1.9", arrowsize="0.9", fontcolor=BLACK)
    return g


def gv_node(g, name, label, accent=NAVY, shape="box", **kw):
    g.node(name, label, shape=shape, color=accent, fillcolor=FILL.get(accent, "#EEEEEE"), **kw)


# ── explicit block-diagram helpers ──────────────────────────────────────
# Auto-layout engines route edge labels unpredictably and can overlap boxes.
# These place everything at known coordinates, so a diagram is correct by
# construction and reviewable by eye.
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle  # noqa: E402
from matplotlib.path import Path                                           # noqa: E402
import matplotlib.patches as mpatches                                      # noqa: E402


def canvas(w, h, scale=1.0):
    """A blank figure with data units of `scale` inches each, y up, no axes.

    Font sizes are absolute points, so a scale below 1 shrinks the boxes while
    the type stays the same size — which is how a dense diagram is made legible
    once it is scaled down to fit a slide.
    """
    fig, ax = plt.subplots(figsize=(w * scale, h * scale))
    ax.set_xlim(0, w); ax.set_ylim(0, h)
    ax.set_aspect("equal"); ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def box(ax, x, y, w, h, lines, accent=NAVY, fs=13, bold_first=True,
        radius=0.10, fill=None, lw=1.8, align="center", name=None):
    """Rounded box centred on (x, y). `lines` is a str or list of strings."""
    if isinstance(lines, str):
        lines = [lines]
    _register(x, y, w, h, name or (lines[0][:22] if lines else "box"))
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0,rounding_size=%.3f" % radius,
        linewidth=lw, edgecolor=accent,
        facecolor=fill if fill else FILL.get(accent, "#EEEEEE"), zorder=2))
    n = len(lines)
    step = fs * 1.42 / 72.0
    top = y + (n - 1) * step / 2
    ha = {"center": "center", "left": "left"}[align]
    tx = x if align == "center" else x - w / 2 + 0.12
    for i, ln in enumerate(lines):
        ax.text(tx, top - i * step, ln, ha=ha, va="center",
                fontsize=fs + (1 if (i == 0 and bold_first and n > 1) else 0),
                fontweight="bold" if (i == 0 and bold_first and n > 1) else "normal",
                color=BLACK, zorder=3)
    return (x, y, w, h)


def anchor(b, side):
    x, y, w, h = b
    return {"L": (x - w / 2, y), "R": (x + w / 2, y),
            "T": (x, y + h / 2), "B": (x, y - h / 2), "C": (x, y)}[side]


def arrow(ax, p0, p1, label=None, color=GREY, dashed=False, lw=1.7,
          fs=11, lab_dx=0.0, lab_dy=0.13, waypoints=None, both=False,
          lab_ha="center", zorder=1):
    """Straight or elbowed arrow. `waypoints` gives an orthogonal route."""
    pts = [p0] + list(waypoints or []) + [p1]
    style = "-|>" if not both else "<|-|>"
    for i in range(len(pts) - 1):
        last = i == len(pts) - 2
        ax.add_patch(FancyArrowPatch(
            pts[i], pts[i + 1],
            arrowstyle=style if last else "-",
            mutation_scale=15, linewidth=lw, color=color, zorder=zorder,
            linestyle=(0, (5, 3)) if dashed else "solid",
            shrinkA=0, shrinkB=0, joinstyle="miter", capstyle="butt"))
    if label:
        mid = pts[len(pts) // 2] if len(pts) > 2 else (
            ((p0[0] + p1[0]) / 2), ((p0[1] + p1[1]) / 2))
        ax.text(mid[0] + lab_dx, mid[1] + lab_dy, label, ha=lab_ha, va="center",
                fontsize=fs, color=BLACK, zorder=4,
                bbox=dict(boxstyle="round,pad=0.16", fc=WHITE, ec="none", alpha=0.95))


def caption(ax, x, y, text, fs=11, color=GREY, ha="center", style="italic"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fs, color=color, style=style, zorder=4)


def group(ax, x0, y0, x1, y1, label=None, color=GREY, fs=11, ls=(0, (6, 4))):
    """Dashed grouping rectangle with a label tucked at its top-left."""
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False,
                           edgecolor=color, linewidth=1.3, linestyle=ls, zorder=0))
    if label:
        ax.text(x0 + 0.12, y1 - 0.16, label, ha="left", va="center", fontsize=fs,
                color=color, style="italic", zorder=4,
                bbox=dict(boxstyle="round,pad=0.14", fc=WHITE, ec="none"))


# ── layout self-check ───────────────────────────────────────────────────
_RECTS = []


def _register(x, y, w, h, name):
    _RECTS.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2, name))


def check_layout(verbose=True):
    """Report any pair of registered boxes that overlap. Returns the count."""
    bad = []
    for i in range(len(_RECTS)):
        ax0, ay0, ax1, ay1, an = _RECTS[i]
        for j in range(i + 1, len(_RECTS)):
            bx0, by0, bx1, by1, bn = _RECTS[j]
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            if ox > 0.02 and oy > 0.02:
                bad.append((an, bn, ox, oy))
    if verbose:
        for an, bn, ox, oy in bad:
            print("   !! OVERLAP  %-22s x %-22s  (%.2f x %.2f in)" % (an, bn, ox, oy))
        if not bad:
            print("   layout check: %d boxes, no overlaps" % len(_RECTS))
    return len(bad)


def reset_layout():
    _RECTS.clear()


def save_schemdraw(d, stem, width_px=PNG_MIN_WIDTH):
    """Save a schemdraw Drawing to <stem>.svg and a <stem>.png of at least
    width_px across, so labels stay legible when the image fills a slide."""
    png, svg = os.path.join(OUT_DIR, stem + ".png"), os.path.join(OUT_DIR, stem + ".svg")
    d.save(svg)
    d.save(png, dpi=300)
    try:
        from PIL import Image
        with Image.open(png) as im:
            w = im.size[0]
        if w < width_px:
            d.save(png, dpi=int(300 * width_px / w) + 1)
    except Exception:
        pass
    _report(png)


def diamond(ax, x, y, w, h, lines, accent=AMBER, fs=12, name=None):
    """Decision diamond centred on (x, y)."""
    if isinstance(lines, str):
        lines = [lines]
    _register(x, y, w, h, name or lines[0][:22])
    ax.add_patch(mpatches.Polygon(
        [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
        closed=True, linewidth=1.8, edgecolor=accent,
        facecolor=FILL.get(accent, "#EEEEEE"), zorder=2))
    step = fs * 1.42 / 72.0
    top = y + (len(lines) - 1) * step / 2
    for i, ln in enumerate(lines):
        ax.text(x, top - i * step, ln, ha="center", va="center", fontsize=fs,
                color=BLACK, zorder=3)
    return (x, y, w, h)


def stadium(ax, x, y, w, h, text, accent=GREEN, fs=13, name=None):
    """Rounded terminator (start / end)."""
    _register(x, y, w, h, name or text[:22])
    ax.add_patch(FancyBboxPatch(
        (x - w / 2 + h / 2, y - h / 2), w - h, h,
        boxstyle="round,pad=0,rounding_size=%.3f" % (h / 2),
        linewidth=1.8, edgecolor=accent, facecolor=FILL.get(accent, "#EEEEEE"), zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, fontweight="bold",
            color=BLACK, zorder=3)
    return (x, y, w, h)
