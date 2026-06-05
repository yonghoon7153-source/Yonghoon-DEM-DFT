#!/usr/bin/env python3
"""Figure 1(b) — Network solver schematic (matplotlib, precise control).

Renders the dual-percolating-network cathode schematic with:
  • SE = yellow majority matrix (many small circles)
  • AM = gray minority islands (few large circles)
  • 3 edge colors: SE-SE (yellow), AM-SE (blue), AM-AM (red)
  • phase-selective boundaries:
      top (SUS, red bar):  ONLY AM touches; SE floats below with gap
      bottom (bulk, tan):  ONLY SE touches; AM floats above with gap
  • two bold backbones:
      yellow SE backbone → touches bulk (bottom), ✕ break below SUS
      red AM backbone    → touches SUS (top),    ✕ break above bulk
  • NO text inside plot; separate legend on right.

Output: docs/figures/network_solver_schematic.png
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

rng = np.random.default_rng(42)

# ── canvas ──
fig, ax = plt.subplots(figsize=(9, 8))
ax.set_xlim(0, 10); ax.set_ylim(0, 11)
ax.axis('off')

# ── collector bars ──
SUS_Y = 10.0; BULK_Y = 1.0
ax.add_patch(FancyBboxPatch((0.3, SUS_Y), 7.4, 0.8, boxstyle='round,pad=0.05',
             fc='#f5b8b8', ec='#c44', lw=1.5, zorder=1))   # SUS red-tint
ax.add_patch(FancyBboxPatch((0.3, BULK_Y-0.8), 7.4, 0.8, boxstyle='round,pad=0.05',
             fc='#f0deb0', ec='#b89030', lw=1.5, zorder=1)) # bulk tan

# phase-selective contact zones (subtle bands)
ax.add_patch(plt.Rectangle((0.3, SUS_Y-0.45), 7.4, 0.45, fc='#c44', alpha=0.10, zorder=0))
ax.add_patch(plt.Rectangle((0.3, BULK_Y), 7.4, 0.45, fc='#b89030', alpha=0.10, zorder=0))

# ── generate particle positions (SE majority, AM minority) ──
# Grid jittered. SE small numerous, AM large sparse.
xs = np.linspace(0.8, 7.2, 11)
ys = np.linspace(BULK_Y+0.3, SUS_Y-0.3, 12)
nodes = []  # (x, y, phase, r)  phase: 'SE' or 'AM'
for j, y in enumerate(ys):
    for i, x in enumerate(xs):
        xx = x + rng.uniform(-0.18, 0.18)
        yy = y + rng.uniform(-0.18, 0.18)
        # AM only ~15%, larger; avoid AM at very bottom row, SE at very top row
        is_am = rng.random() < 0.15
        if j == 0:  is_am = False          # bottom row: SE only (touches bulk)
        if j == len(ys)-1: is_am = True    # top row: AM only (touches SUS)
        if is_am:
            nodes.append((xx, yy, 'AM', rng.uniform(0.16, 0.24)))
        else:
            nodes.append((xx, yy, 'SE', 0.10))

# ── draw edges (thin background) between nearby nodes ──
def near(a, b, d=1.1):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 < d*d

for i in range(len(nodes)):
    for k in range(i+1, len(nodes)):
        a, b = nodes[i], nodes[k]
        if not near(a, b): continue
        pa, pb = a[2], b[2]
        if pa=='SE' and pb=='SE':   col='#f5c518'; lw=0.7
        elif pa=='AM' and pb=='AM': col='#e03030'; lw=0.9
        else:                        col='#5b9bd5'; lw=0.8
        # phase-selective: don't draw SE-SE or AM-SE into SUS zone top;
        # don't draw AM-AM or AM-SE into bulk zone — handled by row rule above
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, alpha=0.45,
                zorder=2, solid_capstyle='round')

# ── draw nodes ──
for x, y, ph, r in nodes:
    if ph == 'SE':
        ax.add_patch(Circle((x, y), r, fc='#f5c518', ec='#b8950f', lw=0.8, zorder=4))
    else:
        ax.add_patch(Circle((x, y), r, fc='#808080', ec='#404040', lw=0.8, zorder=4))

# ── bold backbones ──
# Yellow SE backbone: from bulk (bottom, touches) up to ~80% then ✕ (no SUS)
se_path_x = [2.3, 2.5, 2.2, 2.6, 2.4, 2.7]
se_path_y = [BULK_Y, 2.6, 4.2, 5.8, 7.4, 8.6]   # ends at 8.6, below SUS(10) → gap
ax.plot(se_path_x, se_path_y, color='#f5a800', lw=5, alpha=0.85, zorder=5,
        solid_capstyle='round')
ax.plot(se_path_x[-1], se_path_y[-1], marker='x', ms=14, mew=4,
        color='#f5a800', zorder=6)  # ✕ break (no SUS)

# Red AM backbone: from SUS (top, touches) down to ~20% then ✕ (no bulk)
am_path_x = [5.6, 5.4, 5.7, 5.3, 5.6, 5.4]
am_path_y = [SUS_Y, 8.8, 7.0, 5.2, 3.4, 2.2]   # ends at 2.2, above bulk(1) → gap
ax.plot(am_path_x, am_path_y, color='#e02020', lw=5, alpha=0.85, zorder=5,
        solid_capstyle='round')
ax.plot(am_path_x[-1], am_path_y[-1], marker='x', ms=14, mew=4,
        color='#e02020', zorder=6)  # ✕ break (no bulk)

# ── legend (right side, separate) ──
leg_x = 8.0
items = [
    ('circle', '#f5c518', 'SE (ionic, majority)'),
    ('circle', '#808080', 'AM (electronic, minority)'),
    ('edge',   '#f5c518', 'SE-SE contact'),
    ('edge',   '#5b9bd5', 'AM-SE contact'),
    ('edge',   '#e03030', 'AM-AM contact'),
    ('bb',     '#f5a800', 'SE backbone -> bulk (Li+)'),
    ('bb',     '#e02020', 'AM backbone -> SUS (e-)'),
]
ly = 9.5
for kind, col, lbl in items:
    if kind == 'circle':
        ax.add_patch(Circle((leg_x, ly), 0.12, fc=col, ec='#333', lw=0.8))
    elif kind == 'edge':
        xx = np.linspace(leg_x-0.18, leg_x+0.18, 20)
        ax.plot(xx, ly + 0.05*np.sin((xx-leg_x)*40), color=col, lw=1.2)
    else:
        ax.plot([leg_x-0.2, leg_x+0.2], [ly, ly], color=col, lw=4)
    ax.text(leg_x+0.35, ly, lbl, fontsize=8.5, va='center')
    ly -= 0.75

plt.tight_layout()
out = 'docs/figures/network_solver_schematic.png'
import os; os.makedirs('docs/figures', exist_ok=True)
plt.savefig(out, dpi=200, bbox_inches='tight')
print(f"saved: {out}")
