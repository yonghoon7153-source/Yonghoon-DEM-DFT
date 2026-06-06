#!/usr/bin/env python3
"""Figure 1(b) — network-solver schematic preview (matplotlib).

Geometry comes from scripts/network_schematic_data.py (shared with the
PowerPoint generator) so this PNG and the .pptx are pixel-for-pixel the
same layout.  Edge colors are computed from endpoint phases — never
guessed.  NO in-plot text.

Run:  python3 scripts/make_network_schematic.py [stage]
  stage 1 particles · 2 +AM-AM · 3 +AM-SE · 4 +SE-SE · 5 +backbones (full)
"""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Circle

from network_schematic_data import build, spring

STAGE = int(sys.argv[1]) if len(sys.argv) > 1 else 5

# ── colors ──
C_SE, C_SE_E = '#f6c623', '#c08a0a'
C_AM, C_AM_E = '#9b9b9b', '#3f3f3f'
E_SESE, E_AMSE, E_AMAM = '#f3bf1e', '#3f7fd0', '#e22b2b'
BB_Y, BB_R = '#f5a800', '#ee1111'
BG = '#fbfbfb'

D = build()
nodes = D['nodes']; edges = D['edges']
se_chain = D['se_chain']; am_chain = D['am_chain']
c = D['consts']
SUS_Y, BULK_Y, X0, X1 = c['SUS_Y'], c['BULK_Y'], c['X0'], c['X1']
TOP, BOT = c['TOP'], c['BOT']

fig = plt.figure(figsize=(15.0, 7.6), facecolor=BG)
ax = fig.add_axes([0.015, 0.03, 0.66, 0.94]); ax.set_facecolor(BG)
lax = fig.add_axes([0.70, 0.03, 0.29, 0.94])
ax.set_xlim(X0 - 0.8, X1 + 0.8); ax.set_ylim(BOT - 0.3, TOP + 0.3)
ax.set_aspect('equal'); ax.axis('off')
lax.set_xlim(0, 10); lax.set_ylim(0, 11); lax.axis('off')

# collector bars + tint bands
ax.add_patch(FancyBboxPatch((X0-0.2, SUS_Y), (X1-X0)+0.4, 0.9,
             boxstyle='round,pad=0.04', fc='#e8807f', ec='#c64a4a', lw=1.5, zorder=1,
             path_effects=[pe.withSimplePatchShadow(offset=(2,-2), alpha=0.18)]))
ax.add_patch(FancyBboxPatch((X0-0.2, BULK_Y-0.9), (X1-X0)+0.4, 0.9,
             boxstyle='round,pad=0.04', fc='#e8d3a0', ec='#b89030', lw=1.5, zorder=1,
             path_effects=[pe.withSimplePatchShadow(offset=(2,-2), alpha=0.18)]))
ax.add_patch(plt.Rectangle((X0-0.2, SUS_Y-0.5), (X1-X0)+0.4, 0.5, fc='#e8807f', alpha=0.28, zorder=0))
ax.add_patch(plt.Rectangle((X0-0.2, BULK_Y), (X1-X0)+0.4, 0.5, fc='#e8d3a0', alpha=0.30, zorder=0))

def draw_edges(kind, col, lw):
    for a, b in edges[kind]:
        zx, zy = zip(*spring((a[0], a[1]), (b[0], b[1])))
        ax.plot(zx, zy, color=col, lw=lw, alpha=0.9, zorder=3,
                solid_capstyle='round', solid_joinstyle='round')

if STAGE >= 2: draw_edges('AM-AM', E_AMAM, 1.6)
if STAGE >= 3: draw_edges('AM-SE', E_AMSE, 1.5)
if STAGE >= 4: draw_edges('SE-SE', E_SESE, 1.4)

GLOW = lambda c_, w: [pe.Stroke(linewidth=w, foreground=c_, alpha=0.22),
                      pe.Stroke(linewidth=w*0.6, foreground=c_, alpha=0.30), pe.Normal()]
if STAGE >= 5:
    for chain, bcol, gcol in [(se_chain, BB_Y, '#ffd86b'), (am_chain, BB_R, '#ff8a8a')]:
        for m in range(len(chain)-1):
            zx, zy = zip(*spring(chain[m], chain[m+1]))
            ax.plot(zx, zy, color=bcol, lw=3.4, alpha=0.97, zorder=5,
                    solid_capstyle='round', solid_joinstyle='round',
                    path_effects=GLOW(gcol, 11))

# flat solid fill (PPT-style single-color), thin outline, no shading
for x, y, ph, r, bb in nodes:
    fc, ec = (C_SE, C_SE_E) if ph == 'SE' else (C_AM, C_AM_E)
    lw = 1.6 if (bb and STAGE >= 5) else 1.0
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=6))

# legend (adaptive)
lax.add_patch(FancyBboxPatch((0.2, 0.3), 9.6, 10.4, boxstyle='round,pad=0.12',
              fc='white', ec='#333', lw=1.4,
              path_effects=[pe.withSimplePatchShadow(offset=(3,-3), alpha=0.12)]))
def L_circle(y, fc, ec, txt, rr=0.28):
    lax.add_patch(Circle((1.0, y), rr, fc=fc, ec=ec, lw=1.2))
    lax.text(1.95, y, txt, fontsize=11.5, va='center')
def L_zig(y, col, txt, w=1.8):
    zx, zy = zip(*spring((0.55, y), (1.55, y), amp=0.07, period=0.16))
    lax.plot(zx, zy, color=col, lw=w, solid_capstyle='round'); lax.text(1.95, y, txt, fontsize=11.5, va='center')
def L_bb(y, col, gcol, txt):
    zx, zy = zip(*spring((0.55, y), (1.55, y), amp=0.07, period=0.16))
    lax.plot(zx, zy, color=col, lw=2.8, solid_capstyle='round', path_effects=GLOW(gcol, 9))
    lax.text(1.95, y, txt, fontsize=11.5, va='center')

lax.text(0.55, 10.15, 'NODES', fontsize=12.5, fontweight='bold')
L_circle(9.35, C_SE, C_SE_E, 'yellow = SE (ionic, majority matrix)')
L_circle(8.5, C_AM, C_AM_E, 'gray  = AM (electronic, minority islands)', rr=0.34)
if STAGE >= 2:
    lax.text(0.55, 7.5, 'CONTACTS (resistors)', fontsize=12.5, fontweight='bold')
    if STAGE >= 2: L_zig(6.8, E_AMAM, 'red    = AM-AM')
    if STAGE >= 3: L_zig(6.2, E_AMSE, 'blue   = AM-SE')
    if STAGE >= 4: L_zig(5.6, E_SESE, 'yellow = SE-SE')
if STAGE >= 5:
    lax.text(0.55, 4.6, 'BACKBONES', fontsize=12.5, fontweight='bold')
    L_bb(3.9, BB_Y, '#ffd86b', 'yellow -> bulk (Li+ ionic path)')
    L_bb(3.1, BB_R, '#ff8a8a', 'red    -> SUS (e- electronic path)')

import os; os.makedirs('docs/figures', exist_ok=True)
out = f'docs/figures/network_schematic_stage{STAGE}.png'
plt.savefig(out, dpi=210, bbox_inches='tight', facecolor=BG)
print(f"saved: {out}  nodes={len(nodes)} AM-AM={len(edges['AM-AM'])} "
      f"AM-SE={len(edges['AM-SE'])} SE-SE={len(edges['SE-SE'])}")
