#!/usr/bin/env python3
"""Generate Figure 1 panels (d), (e), (f) using matplotlib — paper-grade
schematics for the DEM-driven network solver scheme.

Panels:
  (d) R-split: two adjacent circles with overlapping region representing
      bulk resistance R_bulk + constriction resistance R_constriction
      (Holm 1967 model).
  (e) Three parallel circuit decomposition: σ_ionic / σ_e / κ extracted
      from phase-specific contact subsets.
  (f) Stage E correction + 7-Layer defense flowchart.

Outputs:
  docs/figures/figure1_panel_d.{png,pdf}
  docs/figures/figure1_panel_e.{png,pdf}
  docs/figures/figure1_panel_f.{png,pdf}

Usage:
  python3 scripts/figure1_panels.py            # all 3 panels
  python3 scripts/figure1_panels.py --panel f  # one panel
"""
from __future__ import annotations
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, FancyBboxPatch
import numpy as np


OUT_DIR = Path('docs/figures')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Paper-grade typography
plt.rcParams.update({
    'font.family':       'DejaVu Sans',  # has greek + cyrillic
    'font.size':         9,
    'axes.linewidth':    0.8,
    'pdf.fonttype':      42,   # TrueType for editable PDFs
    'ps.fonttype':       42,
})

COL_AM_P = '#3a3a3a'   # dark gray (polycrystalline)
COL_AM_S = '#888888'   # mid gray  (single-crystal)
COL_SE   = '#d4b94a'   # mustard / yellow (LPSCl)
COL_BULK = '#4a90d4'   # blue
COL_CONS = '#d44a4a'   # red
COL_BRG  = '#8e44ad'   # purple (Bruggeman)
COL_OK   = '#27ae60'   # green
COL_FAIL = '#e74c3c'   # red


# ==========================================================================
#  PANEL (d) — R-split (Holm 1967)
# ==========================================================================
def panel_d():
    fig, ax = plt.subplots(figsize=(5.5, 2.8), dpi=300)
    ax.set_aspect('equal')
    ax.axis('off')

    # Two adjacent circles representing two particles
    r = 1.0
    c1 = (-1.0, 0)
    c2 = ( 1.0, 0)
    p1 = Circle(c1, r, fill=True, facecolor=COL_AM_P, edgecolor='black',
                linewidth=1.2, zorder=2)
    p2 = Circle(c2, r, fill=True, facecolor=COL_SE, edgecolor='black',
                linewidth=1.2, zorder=2)
    ax.add_patch(p1)
    ax.add_patch(p2)

    # Hertzian contact circle (overlap region, exaggerated for visibility)
    contact_w = 0.12
    contact = mpatches.FancyBboxPatch(
        (-contact_w, -0.15), 2*contact_w, 0.30,
        boxstyle="round,pad=0.02", linewidth=1.4,
        facecolor=COL_CONS, edgecolor='black', zorder=3, alpha=0.85)
    ax.add_patch(contact)

    # R_bulk arrows inside each particle
    ax.annotate('', xy=(-0.15, 0), xytext=(-1.85, 0),
                arrowprops=dict(arrowstyle='-|>', color=COL_BULK, lw=2.2),
                zorder=4)
    ax.annotate('', xy=(1.85, 0), xytext=(0.15, 0),
                arrowprops=dict(arrowstyle='-|>', color=COL_BULK, lw=2.2),
                zorder=4)

    # Labels — stagger y so R_bulk (sides) and R_constriction (center) don't overlap.
    ax.text(-1.0, -1.25, r'$R_{bulk}$',
            ha='center', va='top', color=COL_BULK, fontsize=11, fontweight='bold')
    ax.text(-1.0, -1.65, '(Internal)',
            ha='center', va='top', color=COL_BULK, fontsize=8, style='italic')
    ax.text( 1.0, -1.25, r'$R_{bulk}$',
            ha='center', va='top', color=COL_BULK, fontsize=11, fontweight='bold')
    ax.text( 1.0, -1.65, '(Internal)',
            ha='center', va='top', color=COL_BULK, fontsize=8, style='italic')
    # R_constriction below the others, with leader line up to the contact patch
    ax.annotate('', xy=(0, -0.18), xytext=(0, -1.85),
                arrowprops=dict(arrowstyle='-', color=COL_CONS, lw=0.8))
    ax.text( 0.0, -2.0, r'$R_{constriction}$' '\n(Holm 1967)',
            ha='center', va='top', color=COL_CONS, fontsize=10, fontweight='bold')

    # Equation
    ax.text(0, 1.85,
            r'$R_{total} = R_{bulk} + R_{constriction}$',
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(0, 1.30,
            '(this case: 84 % constriction)',
            ha='center', va='center', fontsize=9, style='italic',
            color='#555')

    # Schematic resistor circuit on right (legend-style)
    sx = 2.6
    ax.plot([sx, sx+1.4], [0.5, 0.5], 'k-', lw=1.2)
    ax.plot([sx+0.6, sx+0.6], [0.5, 0.4], 'k-', lw=1.2)
    # zigzag for R_bulk
    zig_x = np.linspace(sx, sx+0.6, 9)
    zig_y = 0.5 + 0.08*np.array([0,1,-1,1,-1,1,-1,1,0])
    ax.plot(zig_x, zig_y, 'k-', lw=1.2)
    # zigzag for R_constriction
    zig_x2 = np.linspace(sx+0.8, sx+1.4, 9)
    zig_y2 = 0.5 + 0.08*np.array([0,1,-1,1,-1,1,-1,1,0])
    ax.plot(zig_x2, zig_y2, color=COL_CONS, lw=1.4)

    ax.set_xlim(-3, 4.3)
    ax.set_ylim(-2.6, 2.2)
    ax.set_title('(d) Resistance Split',
                 fontsize=11, fontweight='bold', loc='left', pad=8)

    plt.tight_layout()
    fig.savefig(OUT_DIR / 'figure1_panel_d.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT_DIR / 'figure1_panel_d.pdf',          bbox_inches='tight')
    plt.close(fig)
    print(f'  ✓ panel (d) → {OUT_DIR}/figure1_panel_d.{{png,pdf}}')


# ==========================================================================
#  PANEL (e) — Three Parallel Circuit Decomposition
# ==========================================================================
def panel_e():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5), dpi=300)

    titles = [r'$\sigma_{\rm ionic}$',
              r'$\sigma_{\rm e}$',
              r'$\kappa$']
    subtitles = ['(SE-SE + AM-SE)', '(AM-AM only)', '(All Contacts)']
    colors    = ['#3a78d6', '#d63a3a', '#e69138']

    # Reproducible particle layout shared across all 3 panels (same DEM →
    # different contact-subset visualization)
    rng = np.random.RandomState(42)
    n_AM_P, n_AM_S, n_SE = 4, 6, 30
    AM_P = rng.uniform(0.5, 9.5, (n_AM_P, 2))
    AM_S = rng.uniform(1, 9, (n_AM_S, 2))
    SE   = rng.uniform(0.5, 9.5, (n_SE, 2))

    def _draw_particles(ax, draw_AM_P, draw_AM_S, draw_SE):
        for p in AM_P:
            c = Circle(p, 0.8, facecolor=COL_AM_P if draw_AM_P else '#dadada',
                       edgecolor='black', lw=0.6, zorder=2,
                       alpha=1.0 if draw_AM_P else 0.25)
            ax.add_patch(c)
        for p in AM_S:
            c = Circle(p, 0.4, facecolor=COL_AM_S if draw_AM_S else '#dadada',
                       edgecolor='black', lw=0.5, zorder=2,
                       alpha=1.0 if draw_AM_S else 0.25)
            ax.add_patch(c)
        for p in SE:
            c = Circle(p, 0.18, facecolor=COL_SE if draw_SE else '#dadada',
                       edgecolor='black', lw=0.4, zorder=2,
                       alpha=1.0 if draw_SE else 0.25)
            ax.add_patch(c)

    def _draw_contacts(ax, source_xy, target_xy, color, max_dist=1.5,
                       max_edges=40):
        edges = []
        for s in source_xy:
            for t in target_xy:
                if np.array_equal(s, t): continue
                d = np.linalg.norm(s - t)
                if d < max_dist:
                    edges.append((s, t, d))
        edges.sort(key=lambda e: e[2])
        for s, t, _ in edges[:max_edges]:
            ax.plot([s[0], t[0]], [s[1], t[1]], color=color, lw=1.2,
                    alpha=0.75, zorder=3)

    # Panel (e1) σ_ionic = SE-SE + AM-SE
    ax = axes[0]
    _draw_particles(ax, draw_AM_P=True, draw_AM_S=True, draw_SE=True)
    _draw_contacts(ax, SE, SE, colors[0], max_dist=0.7, max_edges=80)
    AM_all = np.vstack([AM_P, AM_S])
    _draw_contacts(ax, AM_all, SE, colors[0], max_dist=1.2, max_edges=60)

    # Panel (e2) σ_e = AM-AM only
    ax = axes[1]
    _draw_particles(ax, draw_AM_P=True, draw_AM_S=True, draw_SE=False)
    _draw_contacts(ax, AM_P, AM_P, colors[1], max_dist=4.0, max_edges=20)
    _draw_contacts(ax, AM_P, AM_S, colors[1], max_dist=2.5, max_edges=20)

    # Panel (e3) κ = All contacts
    ax = axes[2]
    _draw_particles(ax, draw_AM_P=True, draw_AM_S=True, draw_SE=True)
    _draw_contacts(ax, SE, SE, colors[2], max_dist=0.7, max_edges=80)
    _draw_contacts(ax, AM_all, SE, colors[2], max_dist=1.2, max_edges=60)
    _draw_contacts(ax, AM_P, AM_P, colors[2], max_dist=4.0, max_edges=20)

    for i, ax in enumerate(axes):
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-0.5, 10.5)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(colors[i])
            spine.set_linewidth(2)
        ax.set_title(f'{titles[i]}\n{subtitles[i]}',
                     fontsize=12, fontweight='bold', color=colors[i], pad=10)

    fig.suptitle('(e) Three Parallel Circuit Decomposition',
                 fontsize=12, fontweight='bold', y=0.99, x=0.5)
    plt.tight_layout()
    fig.savefig(OUT_DIR / 'figure1_panel_e.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT_DIR / 'figure1_panel_e.pdf',          bbox_inches='tight')
    plt.close(fig)
    print(f'  ✓ panel (e) → {OUT_DIR}/figure1_panel_e.{{png,pdf}}')


# ==========================================================================
#  PANEL (f) — Stage E + 7-Layer Defense Flowchart
# ==========================================================================
def panel_f():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis('off')

    def _box(x, y, w, h, label, color='#f0f0f0', edgecolor='black',
             fontsize=9, fontweight='normal', text_color='black'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor=edgecolor,
                             linewidth=1.2)
        ax.add_patch(box)
        # wrap=True can break $...$ math expressions across lines.
        # We control line breaks explicitly via embedded \n in label.
        ax.text(x + w/2, y + h/2, label, ha='center', va='center',
                fontsize=fontsize, fontweight=fontweight,
                color=text_color, wrap=False)

    def _arrow(x1, y1, x2, y2, color='black', label=None,
               label_offset=(0, 0), label_color='black', style='->'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.4))
        if label:
            mx, my = (x1+x2)/2 + label_offset[0], (y1+y2)/2 + label_offset[1]
            ax.text(mx, my, label, fontsize=8, color=label_color,
                    fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle="round,pad=0.2",
                              facecolor='white', edgecolor='none', alpha=0.9))

    # ── BASE R (top-left)
    _box(0.3, 8.5, 1.8, 1.0,
         'Base R\n(panels b–e)',
         color='#e0eaff', fontweight='bold', fontsize=10)

    # ── Generic solver (top, center)
    _box(2.7, 8.5, 2.0, 1.0,
         'Lx = b\nGeneric Solver',
         color='#fff3d4', fontweight='bold', fontsize=10)
    _arrow(2.1, 9.0, 2.7, 9.0)

    # ── Comparison case label
    ax.text(7.5, 9.0, 'Generic solver\n(comparison case)',
            fontsize=9, ha='center', va='center', style='italic', color='#555')
    _arrow(4.7, 9.0, 6.5, 9.0)

    # ── Stage E factor box (mid-left)
    _box(0.3, 6.4, 4.4, 1.6,
         '★ Stage E Fracture Correction\n(Lawn 1998 dependence)\n\n'
         r'$f_r = f_{Cronau} \times f_{Trev.} \times f_{Wang}$',
         color='#fde4d4', fontweight='bold', fontsize=10)
    _arrow(1.2, 8.5, 1.2, 8.0, color='#888')

    # ── 7-Layer defense (mid-center, below Stage E)
    _box(0.3, 4.4, 4.4, 1.6,
         '★ 7-Layer Defense & Sanity Checks\n'
         r'(L1–L4: $g_{boundary}$, spsolve, CG, $\sigma_{ratio}$)',
         color='#fde4d4', fontweight='bold', fontsize=10)
    _arrow(2.5, 6.4, 2.5, 6.0)

    # ── Decision diamond — "Solver OK?"
    diamond = mpatches.RegularPolygon((6.5, 5.2), 4, radius=0.9, orientation=0,
                                       facecolor='#fff3d4',
                                       edgecolor='black', lw=1.3)
    ax.add_patch(diamond)
    ax.text(6.5, 5.2, 'Solver\nOK?', ha='center', va='center',
            fontsize=10, fontweight='bold')
    _arrow(4.7, 5.2, 5.7, 5.2)

    # ── PASS branch (down-right)
    _box(7.7, 4.6, 2.0, 1.2,
         '✓ Direct\nsolver\n(L1–L4 pass)',
         color='#d4f0d4', fontweight='bold', fontsize=10,
         text_color=COL_OK)
    _arrow(7.4, 5.2, 7.7, 5.2, color=COL_OK,
           label='PASS', label_offset=(0, 0.25), label_color=COL_OK)

    # ── FAIL branch (down-left): Bruggeman fallback
    _box(0.3, 2.4, 4.4, 1.6,
         '★ L6: Bruggeman EMT Fallback\n'
         r'$\sigma_{eff} \approx \sigma_{base} \cdot \Sigma g_i f_i / \Sigma g_i$',
         color='#e8d4f0', fontweight='bold', fontsize=9,
         text_color=COL_BRG)
    _arrow(6.5, 4.3, 2.5, 4.0, color=COL_FAIL,
           label='FAIL', label_offset=(0.5, 0.3), label_color=COL_FAIL)

    # ── Modified R (combine both branches)
    _box(5.7, 2.6, 4.0, 1.3,
         "Modified R'\n"
         r"$= (R_{bulk} + R_{constriction}) / f_r$",
         color='#fff3d4', fontweight='bold', fontsize=10)
    _arrow(8.7, 4.6, 8.0, 3.9, color=COL_OK)
    _arrow(4.7, 3.2, 5.7, 3.2, color=COL_BRG)

    # ── Multi-channel grouping (bottom-center)
    _box(2.5, 0.5, 4.5, 1.4,
         'Multi-channel R-Groupings\n'
         r'($\sigma_{ionic}$, $\sigma_e$, $\kappa$)',
         color='#e0eaff', fontweight='bold', fontsize=10)
    _arrow(7.5, 2.6, 5.5, 1.9)

    # ── Final output (bottom-right)
    _box(7.5, 0.5, 2.2, 1.4,
         '★ Robust $\sigma_{eff}$\n'
         r'($\sigma_{ionic}, \sigma_e, \kappa$)',
         color='#d4f0d4', fontweight='bold', fontsize=11,
         text_color=COL_OK)
    _arrow(7.0, 1.2, 7.5, 1.2)

    ax.text(5.0, 9.7, '(f) Stage E Correction & 7-Layer Defense',
            ha='center', va='center', fontsize=13, fontweight='bold')

    fig.savefig(OUT_DIR / 'figure1_panel_f.png', dpi=300, bbox_inches='tight')
    fig.savefig(OUT_DIR / 'figure1_panel_f.pdf',          bbox_inches='tight')
    plt.close(fig)
    print(f'  ✓ panel (f) → {OUT_DIR}/figure1_panel_f.{{png,pdf}}')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--panel', choices=['d', 'e', 'f', 'all'], default='all')
    args = ap.parse_args()
    print(f'Generating Figure 1 panels → {OUT_DIR}/\n')
    if args.panel in ('d', 'all'): panel_d()
    if args.panel in ('e', 'all'): panel_e()
    if args.panel in ('f', 'all'): panel_f()
    print('\nDone. Open the .png files for preview, .pdf for paper inclusion.')


if __name__ == '__main__':
    main()
