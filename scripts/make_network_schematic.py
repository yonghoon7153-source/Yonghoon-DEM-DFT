#!/usr/bin/env python3
"""Figure 1(b) — network-solver schematic (matplotlib, color-GUARANTEED).

Why programmatic and not an image-gen AI: every spring's color is COMPUTED
from the two particle phases it links, so it is impossible to mis-color.
Diffusion image models cannot enforce that graph constraint — this can.

Rule (never guessed):
  yellow spring = SE-SE   |   blue spring = AM-SE   |   red spring = AM-AM

Two percolating backbones with PHASE-SELECTIVE boundaries:
  • SE backbone (yellow glow) reaches BULK (bottom), Li+ path; ✕ before SUS.
  • AM backbone (red glow)    reaches SUS  (top),  e- path;  ✕ before bulk.
The ✕ are TRUE terminations: no SE particle above SE_TOP, no AM below AM_BOT,
and an empty pocket is carved around each ✕.  NO in-plot text.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Circle

rng = np.random.default_rng(3)

# ── colors ──
C_SE   = '#f6c623'; C_SE_E  = '#c08a0a'
C_AM   = '#9b9b9b'; C_AM_E  = '#3f3f3f'
E_SESE = '#f3bf1e'; E_AMSE  = '#3f7fd0'; E_AMAM = '#e22b2b'
BB_Y   = '#f5a800'; BB_R    = '#ee1111'
BG     = '#fbfbfb'

fig = plt.figure(figsize=(13.6, 7.2), facecolor=BG)
ax  = fig.add_axes([0.015, 0.03, 0.63, 0.94]); ax.set_facecolor(BG)
lax = fig.add_axes([0.66, 0.03, 0.33, 0.94])
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis('off')
lax.set_xlim(0, 10); lax.set_ylim(0, 11); lax.axis('off')

SUS_Y, BULK_Y = 10.0, 1.0
X0, X1 = 0.5, 9.5
SE_TOP, AM_BOT = 8.3, 2.7

# ── collector bars + phase-selective tint bands ──
ax.add_patch(FancyBboxPatch((X0-0.2, SUS_Y), (X1-X0)+0.4, 0.9,
             boxstyle='round,pad=0.04', fc='#e8807f', ec='#c64a4a', lw=1.5, zorder=1,
             path_effects=[pe.withSimplePatchShadow(offset=(2,-2), alpha=0.18)]))
ax.add_patch(FancyBboxPatch((X0-0.2, BULK_Y-0.9), (X1-X0)+0.4, 0.9,
             boxstyle='round,pad=0.04', fc='#e8d3a0', ec='#b89030', lw=1.5, zorder=1,
             path_effects=[pe.withSimplePatchShadow(offset=(2,-2), alpha=0.18)]))
ax.add_patch(plt.Rectangle((X0-0.2, SUS_Y-0.5), (X1-X0)+0.4, 0.5, fc='#e8807f', alpha=0.28, zorder=0))
ax.add_patch(plt.Rectangle((X0-0.2, BULK_Y), (X1-X0)+0.4, 0.5, fc='#e8d3a0', alpha=0.30, zorder=0))

nodes = []   # (x,y,phase,r,backbone)

# ── 1. SE backbone: bulk → SE_TOP, ✕ below SUS ──
n_se = 9
se_y = np.linspace(BULK_Y+0.15, SE_TOP, n_se)
se_x = 3.0 + 0.50*np.sin(np.linspace(0.2, 3.4, n_se))
se_chain = list(zip(se_x, se_y))
for (x, y) in se_chain: nodes.append((x, y, 'SE', 0.20, True))
SE_GAP_X = se_chain[-1][0]

# ── 2. AM backbone: SUS → AM_BOT, ✕ above bulk ──
n_am = 9
am_y = np.linspace(SUS_Y-0.15, AM_BOT, n_am)
am_x = 6.7 + 0.40*np.sin(np.linspace(0.0, 3.0, n_am))
am_chain = list(zip(am_x, am_y))
for (x, y) in am_chain: nodes.append((x, y, 'AM', 0.30, True))
AM_GAP_X = am_chain[-1][0]

# ── 3. filler: SE majority + AM minority; enforced zones + empty ✕ pockets ──
def clash(x, y, r, pad=0.05):
    for (nx, ny, ph, nr, bb) in nodes:
        if (x-nx)**2 + (y-ny)**2 < (r+nr+pad)**2: return True
    return False

gx = np.linspace(X0+0.4, X1-0.4, 12)
gy = np.linspace(BULK_Y+0.35, SUS_Y-0.35, 13)
for y in gy:
    for x in gx:
        xx = x + rng.uniform(-0.16, 0.16); yy = y + rng.uniform(-0.16, 0.16)
        if yy > SE_TOP and abs(xx - SE_GAP_X) < 0.75: continue   # SE break pocket
        if yy < AM_BOT and abs(xx - AM_GAP_X) < 0.75: continue   # AM break pocket
        if yy > SE_TOP:   is_am = True
        elif yy < AM_BOT: is_am = False
        else:             is_am = rng.random() < 0.13
        r = rng.uniform(0.26, 0.34) if is_am else 0.16
        if clash(xx, yy, r): continue
        nodes.append((xx, yy, 'AM' if is_am else 'SE', r, False))

# ── uniform resistor spring (fixed amplitude, lead-ins like a real coil) ──
def spring(p, q, amp=0.062, period=0.30):
    p = np.array(p, float); q = np.array(q, float)
    v = q - p; L = np.hypot(*v)
    if L < 1e-6: return np.array([p[0]]), np.array([p[1]])
    u = v / L; perp = np.array([-u[1], u[0]])
    lead = 0.18
    n_teeth = max(3, int(round((L*(1-2*lead))/period)))
    ts = np.linspace(lead, 1-lead, n_teeth*2+1)
    pts = [p]
    for k, t in enumerate(ts):
        off = 0.0 if (k == 0 or k == len(ts)-1) else amp*(1 if k % 2 else -1)
        pts.append(p + v*t + perp*off)
    pts.append(q)
    pts = np.array(pts)
    return pts[:, 0], pts[:, 1]

# ── draw edges (color strictly from REAL endpoint phases) ──
SE = {'SE'}
def near(a, b, d=1.15): return (a[0]-b[0])**2 + (a[1]-b[1])**2 < d*d

for i in range(len(nodes)):
    for k in range(i+1, len(nodes)):
        a, b = nodes[i], nodes[k]
        if not near(a, b): continue
        s1 = a[2] in SE; s2 = b[2] in SE
        if s1 and s2:               col = E_SESE; lw = 1.3
        elif (not s1) and (not s2): col = E_AMAM; lw = 1.5
        else:                       col = E_AMSE; lw = 1.4
        zx, zy = spring((a[0], a[1]), (b[0], b[1]))
        ax.plot(zx, zy, color=col, lw=lw, alpha=0.9, zorder=3,
                solid_capstyle='round', solid_joinstyle='round')

# ── backbone glow + bold spring (over the chain) ──
GLOW = lambda c, w: [pe.Stroke(linewidth=w, foreground=c, alpha=0.22),
                     pe.Stroke(linewidth=w*0.6, foreground=c, alpha=0.30), pe.Normal()]
for chain, bcol, gcol in [(se_chain, BB_Y, '#ffd86b'), (am_chain, BB_R, '#ff8a8a')]:
    for m in range(len(chain)-1):
        zx, zy = spring(chain[m], chain[m+1])
        ax.plot(zx, zy, color=bcol, lw=3.2, alpha=0.97, zorder=5,
                solid_capstyle='round', solid_joinstyle='round',
                path_effects=GLOW(gcol, 11))

# ── ✕ breaks in carved empty pockets (true terminations) ──
sx, sy = se_chain[-1]
ax.plot(sx, sy + 0.75, marker='x', ms=18, mew=4.5, color=BB_Y, zorder=8,
        path_effects=GLOW('#ffd86b', 9))
axb, ayb = am_chain[-1]
ax.plot(axb, ayb - 0.75, marker='x', ms=18, mew=4.5, color=BB_R, zorder=8,
        path_effects=GLOW('#ff8a8a', 9))

# ── nodes (shadow + body + highlight) ──
SHADOW = [pe.withSimplePatchShadow(offset=(2.2, -2.2), alpha=0.22, shadow_rgbFace='#777')]
for x, y, ph, r, bb in nodes:
    fc, ec = (C_SE, C_SE_E) if ph == 'SE' else (C_AM, C_AM_E)
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=1.6 if bb else 1.0,
                        zorder=6, path_effects=SHADOW))
    # soft specular highlight
    hl = '#fff7d6' if ph == 'SE' else '#d8d8d8'
    ax.add_patch(Circle((x-0.30*r, y+0.30*r), 0.34*r, fc=hl, ec='none',
                        alpha=0.55, zorder=7))

# ── legend panel ──
lax.add_patch(FancyBboxPatch((0.2, 0.3), 9.6, 10.4, boxstyle='round,pad=0.12',
              fc='white', ec='#333', lw=1.4,
              path_effects=[pe.withSimplePatchShadow(offset=(3,-3), alpha=0.12)]))
def L_circle(y, fc, ec, txt, rr=0.28):
    lax.add_patch(Circle((1.0, y), rr, fc=fc, ec=ec, lw=1.2, path_effects=SHADOW))
    lax.text(1.95, y, txt, fontsize=11.5, va='center')
def L_zig(y, col, txt):
    zx, zy = spring((0.55, y), (1.55, y), amp=0.07, period=0.16)
    lax.plot(zx, zy, color=col, lw=1.8, solid_capstyle='round')
    lax.text(1.95, y, txt, fontsize=11.5, va='center')
def L_bb(y, col, gcol, txt):
    zx, zy = spring((0.55, y), (1.55, y), amp=0.07, period=0.16)
    lax.plot(zx, zy, color=col, lw=2.8, solid_capstyle='round',
             path_effects=GLOW(gcol, 9))
    lax.text(1.95, y, txt, fontsize=11.5, va='center')

lax.text(0.55, 10.15, 'NODES', fontsize=12.5, fontweight='bold')
L_circle(9.35, C_SE, C_SE_E, 'yellow = SE (ionic, majority matrix)')
L_circle(8.5, C_AM, C_AM_E, 'gray  = AM (electronic, minority islands)', rr=0.34)
lax.text(0.55, 7.5, 'CONTACTS (resistors)', fontsize=12.5, fontweight='bold')
L_zig(6.8, E_SESE, 'yellow = SE-SE')
L_zig(6.2, E_AMSE, 'blue   = AM-SE')
L_zig(5.6, E_AMAM, 'red    = AM-AM')
lax.text(0.55, 4.6, 'BACKBONES', fontsize=12.5, fontweight='bold')
L_bb(3.9, BB_Y, '#ffd86b', 'yellow -> bulk (Li+ path); break = no SE to SUS')
L_bb(3.1, BB_R, '#ff8a8a', 'red    -> SUS (e- path);  break = no AM to bulk')

import os; os.makedirs('docs/figures', exist_ok=True)
out = 'docs/figures/network_solver_schematic.png'
plt.savefig(out, dpi=210, bbox_inches='tight', facecolor=BG)
print(f"saved: {out}")
