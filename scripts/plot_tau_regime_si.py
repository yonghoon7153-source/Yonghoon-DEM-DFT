"""
Generate SI-quality figures from /tmp/tau_regime_db.json.

Figures produced:
  /tmp/si_fig_regime_map.pdf       Main regime map (Le/D vs SE-SE CN, colored by
                                    constriction fraction)
  /tmp/si_fig_literature_match.pdf τ² vs φ_SE + Minnmann/Wang/Dewald anchors
  /tmp/si_fig_ratio_distribution.pdf 3 histograms (Le/Lg, Lg/D, Le/D) — for
                                     median non-commutativity footnote
  /tmp/si_fig_bottleneck_showcase.pdf  Annotated showcase: input_8_AMS +
                                        input_real8_40_7 as bottleneck examples

Usage:
  python3 scripts/build_tau_regime_db.py   # first, build DB
  python3 scripts/plot_tau_regime_si.py    # then, plot
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


DB_PATH = '/tmp/tau_regime_db.json'
OUT_DIR = '/tmp'


def load_db():
    with open(DB_PATH) as f:
        return json.load(f)


# ─── Figure 1: Regime map ────────────────────────────────────────────────

def fig_regime_map(records):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    xs = np.array([r['SE_SE_CN_mean'] for r in records if r.get('SE_SE_CN_mean') and r.get('Le_over_D')])
    ys = np.array([r['Le_over_D'] for r in records if r.get('SE_SE_CN_mean') and r.get('Le_over_D')])
    cs = np.array([(r['constriction_frac'] or 0.75) for r in records
                   if r.get('SE_SE_CN_mean') and r.get('Le_over_D')])
    names = [r['name'] for r in records if r.get('SE_SE_CN_mean') and r.get('Le_over_D')]

    # Regime zones
    ax.axhspan(1.3, 2.3, alpha=0.1, color='tab:green', zorder=0)
    ax.axhspan(2.3, ys.max() * 1.1 if len(ys) else 4, alpha=0.1, color='tab:red', zorder=0)
    ax.axhspan(min(ys.min() * 0.9, 0.5) if len(ys) else 0.5, 1.3, alpha=0.1, color='tab:blue', zorder=0)
    ax.axvspan(0, 3.5, alpha=0.15, color='tab:red', zorder=0)

    # Reference lines
    ax.axhline(1.76, color='k', ls='--', lw=1, alpha=0.6)
    ax.text(xs.max()*0.95 if len(xs) else 6, 1.80, 'median 1.76', fontsize=8, ha='right')
    ax.axvline(3.5, color='tab:red', ls=':', lw=1, alpha=0.8)
    ax.text(3.45, 3.5, 'SE-SE CN\nthreshold 3.5', fontsize=8, ha='right', color='tab:red')

    # Scatter
    sc = ax.scatter(xs, ys, c=cs, cmap='viridis', s=50, edgecolor='k',
                    linewidth=0.5, vmin=0.6, vmax=0.85, zorder=3)
    cbar = plt.colorbar(sc, ax=ax, label='Constriction fraction  R$_{GB}$/(R$_{GB}$+R$_{bulk}$)')

    # Annotate bottleneck outliers
    for x, y, n in zip(xs, ys, names):
        if y > 2.5:
            ax.annotate(n.replace('input_', ''), (x, y),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=7, color='tab:red', fontweight='bold')

    # Regime labels
    ax.text(xs.max()*0.98 if len(xs) else 6, 2.7, 'BOTTLENECK\n(Le/D > 2.3)',
            fontsize=9, ha='right', color='tab:red', alpha=0.8)
    ax.text(xs.max()*0.98 if len(xs) else 6, 1.7, 'NORMAL (1.3–2.3)',
            fontsize=9, ha='right', color='tab:green', alpha=0.8)
    ax.text(xs.max()*0.98 if len(xs) else 6, 1.0, 'SURROGATE CLEAN (<1.3)',
            fontsize=9, ha='right', color='tab:blue', alpha=0.8)

    ax.set_xlabel('SE–SE coordination number  ⟨CN⟩', fontsize=11)
    ax.set_ylabel(r'$\tau_{Lap,\,eff}\,/\,\tau_{Dij}$  (bottleneck indicator)',
                  fontsize=11)
    ax.set_title(f'Tortuosity regime map (n={len(xs)} DEM cases)')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_regime_map.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─── Figure 2: Literature match ──────────────────────────────────────────

def fig_literature_match(records):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    xs = np.array([r['phi_SE'] for r in records if r.get('phi_SE') and r.get('tau_sq_Lap_eff')])
    ys = np.array([r['tau_sq_Lap_eff'] for r in records
                   if r.get('phi_SE') and r.get('tau_sq_Lap_eff')])

    ax.scatter(xs, ys, s=45, c='steelblue', edgecolor='k', linewidth=0.5,
               alpha=0.7, label=f'This work DEM (n={len(xs)})')

    # Literature anchors
    anchors = [
        ('Minnmann 2021 (42% CAM)', 0.44, 4.3,  'tab:red'),
        ('Wang 2023 (70% CAM)',      0.26, 7.78, 'tab:orange'),
        ('Wang 2023 (80% CAM)',      0.16, 17.24, 'tab:orange'),
        ('Dewald 2021 (25% NCM)',    0.65, 2.4,  'tab:purple'),
    ]
    for name, phi, tau2, col in anchors:
        ax.scatter(phi, tau2, marker='*', s=300, c=col, edgecolor='k',
                   linewidth=1, zorder=5, label=name)

    # Bruggeman reference
    phi_range = np.linspace(0.15, 0.7, 50)
    ax.plot(phi_range, phi_range**(-1.0), 'k--', alpha=0.5,
            label='Bruggeman (α=1.5): τ²=φ$^{-1}$')
    ax.plot(phi_range, phi_range**(-2.36), 'k:', alpha=0.5,
            label="Wang 2023 fit (α=2.36): τ²=φ$^{-1.72}$")

    ax.set_xlabel(r'$\varphi_\mathrm{SE}$', fontsize=11)
    ax.set_ylabel(r'$\tau^2_{Lap,\,eff}$', fontsize=11)
    ax.set_yscale('log')
    ax.set_title('Tortuosity² vs SE fraction — literature match')
    ax.grid(alpha=0.3, which='both')
    ax.legend(fontsize=8, loc='upper right')

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_literature_match.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─── Figure 3: Ratio distributions (median non-commutativity) ────────────

def fig_ratio_distributions(records):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

    cols = [('Le_over_Lg', r'$\tau_{Lap,eff}\,/\,\tau_{Lap,geom}$', 2.01, 'tab:red'),
            ('Lg_over_D',  r'$\tau_{Lap,geom}\,/\,\tau_{Dij}$',    0.79, 'tab:green'),
            ('Le_over_D',  r'$\tau_{Lap,eff}\,/\,\tau_{Dij}$',     1.76, 'tab:blue')]

    for ax, (key, lbl, med, col) in zip(axes, cols):
        vals = [r[key] for r in records if r.get(key) is not None]
        ax.hist(vals, bins=20, color=col, alpha=0.7, edgecolor='k')
        ax.axvline(med, color='k', ls='--', lw=1.5, label=f'median = {med}')
        ax.set_xlabel(lbl, fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel('Count')
    fig.suptitle(f'Per-case ratio distributions (n={len(records)}) — '
                 f'medians are independent, not multiplicatively constrained')

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_ratio_distribution.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─── Figure 4: Bottleneck showcase ───────────────────────────────────────

def fig_bottleneck_showcase(records):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Main population
    xs = np.array([r['phi_SE'] for r in records if r.get('phi_SE') and r.get('Le_over_D')])
    ys = np.array([r['Le_over_D'] for r in records if r.get('phi_SE') and r.get('Le_over_D')])
    cns = np.array([(r.get('SE_SE_CN_mean') or 4.0) for r in records
                    if r.get('phi_SE') and r.get('Le_over_D')])
    names = [r['name'] for r in records if r.get('phi_SE') and r.get('Le_over_D')]

    sc = ax.scatter(xs, ys, c=cns, cmap='plasma_r', s=60, edgecolor='k',
                    linewidth=0.5, vmin=2.5, vmax=6, alpha=0.85)
    cbar = plt.colorbar(sc, ax=ax, label='SE-SE CN mean')

    # Reference lines
    ax.axhline(1.76, color='k', ls='--', lw=1, alpha=0.5,
               label='bulk median  Le/D = 1.76')
    ax.axhline(2.3, color='tab:red', ls=':', lw=1.2, alpha=0.7,
               label='bottleneck onset  (Le/D = 2.3)')

    # Highlight bottleneck outliers
    for x, y, cn, n in zip(xs, ys, cns, names):
        if y > 2.3:
            ax.annotate(f'{n.replace("input_", "")}\n(CN={cn:.1f})', (x, y),
                        xytext=(10, 5), textcoords='offset points',
                        fontsize=8, color='tab:red', fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color='tab:red', alpha=0.6))

    ax.set_xlabel(r'$\varphi_\mathrm{SE}$', fontsize=11)
    ax.set_ylabel(r'$\tau_{Lap,\,eff}\,/\,\tau_{Dij}$', fontsize=11)
    ax.set_title('Bottleneck regime identification — Dijkstra underestimates flux resistance\n'
                 'when Le/D > 2.3 and SE-SE CN approaches percolation threshold')
    ax.grid(alpha=0.3)
    ax.legend(loc='upper left', fontsize=9)

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_bottleneck_showcase.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


def main():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: {DB_PATH} not found. Run build_tau_regime_db.py first.")
        return
    records = load_db()
    print(f"Loaded {len(records)} records from {DB_PATH}\n")

    out1 = fig_regime_map(records)
    print(f"  [1/4] Regime map → {out1} (+png)")

    out2 = fig_literature_match(records)
    print(f"  [2/4] Literature match → {out2} (+png)")

    out3 = fig_ratio_distributions(records)
    print(f"  [3/4] Ratio distributions → {out3} (+png)")

    out4 = fig_bottleneck_showcase(records)
    print(f"  [4/4] Bottleneck showcase → {out4} (+png)")

    print(f"\n✓ All SI figures generated in {OUT_DIR}/")


if __name__ == '__main__':
    main()
