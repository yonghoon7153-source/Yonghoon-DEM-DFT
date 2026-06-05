#!/usr/bin/env python3
"""Figure 1(b) — Network solver schematic v2 (physics-correct backbones).

Key fix over v1: backbones connect ONLY same-phase particles.
  - SE (yellow) backbone: chains SE→SE→SE particles via SE-SE edges,
    reaches the bulk (bottom), ✕ break below SUS.
  - AM (gray) backbone: chains AM→AM→AM particles via AM-AM edges,
    reaches the SUS (top), ✕ break above bulk.

The backbone particles are PLACED FIRST (a real connected chain of the
correct phase), then filler particles fill the rest.  This guarantees the
highlighted path passes only through its own phase.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

rng = np.random.default_rng(7)

fig, ax = plt.subplots(figsize=(9, 8))
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis('off')

SUS_Y = 10.0; BULK_Y = 1.0
X0, X1 = 0.6, 7.6

# collector bars
ax.add_patch(FancyBboxPatch((X0-0.3, SUS_Y), (X1-X0)+0.6, 0.8, boxstyle='round,pad=0.05',
             fc='#f5b8b8', ec='#c44', lw=1.5, zorder=1))
ax.add_patch(FancyBboxPatch((X0-0.3, BULK_Y-0.8), (X1-X0)+0.6, 0.8, boxstyle='round,pad=0.05',
             fc='#f0deb0', ec='#b89030', lw=1.5, zorder=1))

nodes = []   # (x, y, phase, r, is_backbone)

# ── 1. SE backbone chain: SE particles bottom→top, ends below SUS (gap) ──
se_bb_y = np.linspace(BULK_Y+0.05, SUS_Y-1.4, 9)   # last point ~8.6, gap to SUS(10)
se_bb_x = 2.3 + 0.35*np.sin(np.linspace(0, 3.2, 9))
se_bb = list(zip(se_bb_x, se_bb_y))
for (x, y) in se_bb:
    nodes.append((x, y, 'SE', 0.13, True))

# ── 2. AM backbone chain: AM particles top→bottom, ends above bulk (gap) ──
am_bb_y = np.linspace(SUS_Y-0.05, BULK_Y+1.4, 8)    # last ~2.4, gap to bulk(1)
am_bb_x = 5.6 + 0.3*np.sin(np.linspace(0, 3.0, 8))
am_bb = list(zip(am_bb_x, am_bb_y))
for (x, y) in am_bb:
    nodes.append((x, y, 'AM', 0.22, True))

# ── 3. filler particles (SE majority, AM minority), avoid overlap with bb ──
def too_close(x, y, r):
    for (nx, ny, ph, nr, bb) in nodes:
        if (x-nx)**2 + (y-ny)**2 < (r+nr+0.05)**2:
            return True
    return False

gx = np.linspace(X0+0.3, X1-0.3, 12)
gy = np.linspace(BULK_Y+0.3, SUS_Y-0.3, 13)
for j, y in enumerate(gy):
    for i, x in enumerate(gx):
        xx = x + rng.uniform(-0.16, 0.16); yy = y + rng.uniform(-0.16, 0.16)
        is_am = rng.random() < 0.13
        if j == 0: is_am = False             # bottom row SE-only (touch bulk)
        if j == len(gy)-1: is_am = True      # top row AM-only (touch SUS)
        r = rng.uniform(0.17, 0.23) if is_am else 0.095
        if too_close(xx, yy, r): continue
        nodes.append((xx, yy, 'AM' if is_am else 'SE', r, False))

# ── edges (thin background, color by pair) ──
def near(a, b, d=1.05):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 < d*d

for i in range(len(nodes)):
    for k in range(i+1, len(nodes)):
        a, b = nodes[i], nodes[k]
        if not near(a, b): continue
        pa, pb = a[2], b[2]
        if pa=='SE' and pb=='SE':   col='#f5c518'; lw=0.7
        elif pa=='AM' and pb=='AM': col='#e03030'; lw=0.9
        else:                        col='#5b9bd5'; lw=0.8
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, alpha=0.40, zorder=2)

# ── bold backbone highlights (under the nodes) ──
ax.plot([p[0] for p in se_bb], [p[1] for p in se_bb], color='#f5a800', lw=6,
        alpha=0.55, zorder=3, solid_capstyle='round')
ax.plot([p[0] for p in am_bb], [p[1] for p in am_bb], color='#e02020', lw=6,
        alpha=0.55, zorder=3, solid_capstyle='round')
# ✕ breaks at the non-touching end
ax.plot(se_bb[-1][0], se_bb[-1][1]+0.5, marker='x', ms=15, mew=4, color='#f5a800', zorder=7)
ax.plot(am_bb[-1][0], am_bb[-1][1]-0.5, marker='x', ms=15, mew=4, color='#e02020', zorder=7)

# ── nodes on top ──
for x, y, ph, r, bb in nodes:
    if ph == 'SE':
        ax.add_patch(Circle((x, y), r, fc='#f5c518', ec='#b8950f',
                            lw=1.3 if bb else 0.8, zorder=5))
    else:
        ax.add_patch(Circle((x, y), r, fc='#808080', ec='#404040',
                            lw=1.3 if bb else 0.8, zorder=5))

# ── legend ──
leg_x = 8.1; ly = 9.3
items = [
    ('c', '#f5c518', 'SE (ionic, majority matrix)'),
    ('c', '#808080', 'AM (electronic, minority)'),
    ('e', '#f5c518', 'SE-SE contact'),
    ('e', '#5b9bd5', 'AM-SE contact'),
    ('e', '#e03030', 'AM-AM contact'),
    ('b', '#f5a800', 'SE backbone -> bulk (Li+)'),
    ('b', '#e02020', 'AM backbone -> SUS (e-)'),
]
for kind, col, lbl in items:
    if kind=='c':
        ax.add_patch(Circle((leg_x, ly), 0.13, fc=col, ec='#333', lw=0.8))
    elif kind=='e':
        xx=np.linspace(leg_x-0.2, leg_x+0.2, 24)
        ax.plot(xx, ly+0.05*np.sin((xx-leg_x)*45), color=col, lw=1.3)
    else:
        ax.plot([leg_x-0.22, leg_x+0.22], [ly, ly], color=col, lw=5)
    ax.text(leg_x+0.4, ly, lbl, fontsize=8.5, va='center')
    ly -= 0.78

plt.tight_layout()
import os; os.makedirs('docs/figures', exist_ok=True)
out='docs/figures/network_solver_schematic_v2.png'
plt.savefig(out, dpi=200, bbox_inches='tight')
print(f"saved: {out}")
