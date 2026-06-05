#!/usr/bin/env python3
"""Figure 1(b) — clean network-solver schematic (matplotlib).

Style target: the reference figure — SE yellow majority matrix, AM gray
minority islands, zigzag resistor edges colored by REAL endpoint pair
(SE-SE yellow / AM-SE blue / AM-AM red), two highlighted backbones, SUS
(red) and bulk (tan) bars, separate right-side legend, NO in-plot text.

Edge color is NEVER guessed: each edge's color is set from the two
particle phases it connects.  Backbones are placed as connected chains of
a single phase, so the highlighted path passes only through its own phase.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D

rng = np.random.default_rng(3)

# ── colors ──
C_SE   = '#f5c518'; C_SE_E  = '#b8950f'
C_AM   = '#9a9a9a'; C_AM_E  = '#454545'
E_SESE = '#f5c518'; E_AMSE  = '#3f7fd0'; E_AMAM = '#e02828'
BB_Y   = '#f5a800'; BB_R    = '#ee1111'

fig = plt.figure(figsize=(13, 7))
ax  = fig.add_axes([0.02, 0.04, 0.62, 0.92])   # main panel
lax = fig.add_axes([0.66, 0.04, 0.32, 0.92])   # legend panel
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis('off')
lax.set_xlim(0, 10); lax.set_ylim(0, 11); lax.axis('off')

SUS_Y, BULK_Y = 10.0, 1.0
X0, X1 = 0.5, 9.5

# ── collector bars + phase-selective tint bands ──
ax.add_patch(FancyBboxPatch((X0-0.2, SUS_Y), (X1-X0)+0.4, 0.85,
             boxstyle='round,pad=0.04', fc='#ef8e8e', ec='#cc4444', lw=1.4, zorder=1))
ax.add_patch(FancyBboxPatch((X0-0.2, BULK_Y-0.85), (X1-X0)+0.4, 0.85,
             boxstyle='round,pad=0.04', fc='#ecd9a8', ec='#b89030', lw=1.4, zorder=1))
ax.add_patch(plt.Rectangle((X0-0.2, SUS_Y-0.5), (X1-X0)+0.4, 0.5, fc='#ef8e8e', alpha=0.30, zorder=0))
ax.add_patch(plt.Rectangle((X0-0.2, BULK_Y), (X1-X0)+0.4, 0.5, fc='#ecd9a8', alpha=0.30, zorder=0))

nodes = []   # (x,y,phase,r,backbone)

# ── 1. SE backbone chain (bottom→top), touches bulk, ✕ below SUS ──
n_se = 9
se_y = np.linspace(BULK_Y+0.05, SUS_Y-1.5, n_se)
se_x = 3.0 + 0.55*np.sin(np.linspace(0.2, 3.4, n_se))
se_chain = list(zip(se_x, se_y))
for (x, y) in se_chain:
    nodes.append((x, y, 'SE', 0.20, True))

# ── 2. AM backbone chain (top→bottom), touches SUS, ✕ above bulk ──
n_am = 8
am_y = np.linspace(SUS_Y-0.05, BULK_Y+1.5, n_am)
am_x = 6.7 + 0.45*np.sin(np.linspace(0.0, 3.0, n_am))
am_chain = list(zip(am_x, am_y))
for (x, y) in am_chain:
    nodes.append((x, y, 'AM', 0.30, True))

# ── 3. filler particles: SE majority, AM minority ──
def clash(x, y, r, pad=0.04):
    for (nx, ny, ph, nr, bb) in nodes:
        if (x-nx)**2 + (y-ny)**2 < (r+nr+pad)**2:
            return True
    return False

gx = np.linspace(X0+0.35, X1-0.35, 13)
gy = np.linspace(BULK_Y+0.35, SUS_Y-0.35, 13)
for j, y in enumerate(gy):
    for i, x in enumerate(gx):
        xx = x + rng.uniform(-0.18, 0.18); yy = y + rng.uniform(-0.18, 0.18)
        is_am = rng.random() < 0.14
        if j == 0:            is_am = False     # bottom row SE-only → touch bulk
        if j == len(gy)-1:    is_am = True      # top row AM-only → touch SUS
        r = rng.uniform(0.26, 0.34) if is_am else 0.16
        if clash(xx, yy, r): continue
        nodes.append((xx, yy, 'AM' if is_am else 'SE', r, False))

# ── zigzag edge generator ──
def zigzag(p, q, n=7, amp=0.05):
    p = np.array(p); q = np.array(q)
    v = q - p; L = np.hypot(*v)
    if L < 1e-6: return [p], [q]
    u = v / L; perp = np.array([-u[1], u[0]])
    ts = np.linspace(0, 1, n)
    pts = [p + v*t + perp*amp*L*(1 if k % 2 else -1)*(0 < k < n-1)
           for k, t in enumerate(ts)]
    pts = np.array(pts)
    return pts[:, 0], pts[:, 1]

# ── draw edges (color from REAL endpoint phases) ──
SE = {'SE'}
def near(a, b, d=1.15):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 < d*d

drawn = set()
for i in range(len(nodes)):
    for k in range(i+1, len(nodes)):
        a, b = nodes[i], nodes[k]
        if not near(a, b): continue
        s1 = a[2] in SE; s2 = b[2] in SE
        if s1 and s2:        col = E_SESE; lw = 1.0
        elif (not s1) and (not s2): col = E_AMAM; lw = 1.2
        else:                col = E_AMSE; lw = 1.1
        zx, zy = zigzag((a[0], a[1]), (b[0], b[1]), amp=0.045)
        ax.plot(zx, zy, color=col, lw=lw, alpha=0.85, zorder=3,
                solid_capstyle='round')

# ── backbone glow (under nodes) ──
ax.plot([p[0] for p in se_chain], [p[1] for p in se_chain],
        color=BB_Y, lw=7, alpha=0.40, zorder=2, solid_capstyle='round')
ax.plot([p[0] for p in am_chain], [p[1] for p in am_chain],
        color=BB_R, lw=7, alpha=0.40, zorder=2, solid_capstyle='round')
# zigzag bold backbone edges over the chain
for chain, col in [(se_chain, BB_Y), (am_chain, BB_R)]:
    for m in range(len(chain)-1):
        zx, zy = zigzag(chain[m], chain[m+1], amp=0.05)
        ax.plot(zx, zy, color=col, lw=3.0, alpha=0.95, zorder=5,
                solid_capstyle='round')
# ✕ breaks at non-touching ends
ax.plot(se_chain[-1][0], se_chain[-1][1]+0.55, marker='x', ms=16, mew=4,
        color=BB_Y, zorder=8)
ax.plot(am_chain[-1][0], am_chain[-1][1]-0.55, marker='x', ms=16, mew=4,
        color=BB_R, zorder=8)

# ── nodes on top ──
for x, y, ph, r, bb in nodes:
    fc, ec = (C_SE, C_SE_E) if ph == 'SE' else (C_AM, C_AM_E)
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec,
                        lw=1.6 if bb else 0.9, zorder=6))

# ── legend panel ──
lax.add_patch(FancyBboxPatch((0.2, 0.3), 9.6, 10.4, boxstyle='round,pad=0.1',
              fc='white', ec='#333', lw=1.3))
def L_circle(y, fc, ec, txt, rr=0.28):
    lax.add_patch(Circle((1.0, y), rr, fc=fc, ec=ec, lw=1.0))
    lax.text(1.9, y, txt, fontsize=11, va='center')
def L_zig(y, col, txt):
    zx, zy = zigzag((0.6, y), (1.5, y), amp=0.05)
    lax.plot(zx, zy, color=col, lw=1.6); lax.text(1.9, y, txt, fontsize=11, va='center')
def L_bb(y, col, txt):
    lax.plot([0.6, 1.5], [y, y], color=col, lw=5, alpha=0.5, solid_capstyle='round')
    zx, zy = zigzag((0.6, y), (1.5, y), amp=0.05)
    lax.plot(zx, zy, color=col, lw=2.5); lax.text(1.9, y, txt, fontsize=11, va='center')

lax.text(0.6, 10.1, 'NODES', fontsize=12, fontweight='bold')
L_circle(9.3, C_SE, C_SE_E, 'yellow = SE (ionic, majority matrix)')
L_circle(8.5, C_AM, C_AM_E, 'gray  = AM (electronic, minority islands)', rr=0.34)
lax.text(0.6, 7.5, 'CONTACTS (resistors)', fontsize=12, fontweight='bold')
L_zig(6.8, E_SESE, 'yellow = SE-SE')
L_zig(6.2, E_AMSE, 'blue   = AM-SE')
L_zig(5.6, E_AMAM, 'red    = AM-AM')
lax.text(0.6, 4.6, 'BACKBONES', fontsize=12, fontweight='bold')
L_bb(3.9, BB_Y, 'yellow -> bulk (Li+ path)')
L_bb(3.1, BB_R, 'red    -> SUS (e- path)')

import os; os.makedirs('docs/figures', exist_ok=True)
out = 'docs/figures/network_solver_schematic.png'
plt.savefig(out, dpi=200, bbox_inches='tight')
print(f"saved: {out}")
