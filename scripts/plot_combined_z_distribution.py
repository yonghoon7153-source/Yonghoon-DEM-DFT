#!/usr/bin/env python3
"""Combined Z-profile — Brittle stages + Stress hotspots overlay.

Generates a single 2×2 PNG combining the existing brittle and stress
z-profile data on the same compaction axis so the visual reader can
see *where* fracture damage and stress hotspots co-locate.

  Panel (a) Stacked Lawn fracture stage histogram (brittle pipeline)
  Panel (b) Stacked stress bracket histogram     (stress pipeline)
  Panel (c) z-axis overlay — mean F/P_c + p95 contact pressure on
            shared z axis with twin x axes
  Panel (d) Per-bin correlation scatter:
            x = p95 contact pressure (MPa, log)
            y = brittle damaged fraction (%)
            colour = bin z position

Public API:
  compute_combined_zprofile(case_dir, bins=25) -> dict
  render_combined_figure(profile) -> matplotlib Figure
  profile_to_csv_rows(profile) -> list[list]

CLI:
  python3 scripts/plot_combined_z_distribution.py <case_dir> [--bins 25]
"""
from __future__ import annotations
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from plot_brittle_z_distribution import (         # noqa: E402
    compute_brittle_zprofile, STAGE_ORDER, STAGE_COLOR,
)
from plot_stress_z_distribution import (          # noqa: E402
    compute_stress_zprofile, BRACKET_LABELS, BRACKET_COLORS,
)


def compute_combined_zprofile(case_dir, bins: int = 25) -> dict:
    """Concurrent brittle + stress profiles on the same case_dir.

    Returns a dict with sub-dicts `brittle` and `stress` (each is the
    output of their respective compute function) plus a pre-computed
    `aligned_overlay` table that interpolates the brittle
    `damaged_fraction` onto the stress bin centers so the correlation
    panel can use it directly.
    """
    case_dir = Path(case_dir)
    brittle = compute_brittle_zprofile(case_dir, bins=bins)
    stress  = compute_stress_zprofile(case_dir, bins=bins)

    # Align by interpolating brittle damaged_fraction onto stress
    # bin centers (and reverse for stress p95 onto brittle centers).
    z_b = brittle['bin_centers_um']
    z_s = stress['bin_centers_um']
    counts_b = brittle['counts']
    bin_total_b = np.zeros(len(z_b))
    for s in STAGE_ORDER: bin_total_b += counts_b[s]
    bin_dmg_b = np.zeros(len(z_b))
    for s in STAGE_ORDER:
        if s == 'intact': continue
        bin_dmg_b += counts_b[s]
    damaged_frac_b = np.where(bin_total_b > 0,
                                100.0 * bin_dmg_b / np.maximum(bin_total_b, 1),
                                0.0)

    p95_s = stress['p95_MPa']
    # Cross-interpolations
    p95_on_z_b = (np.interp(z_b, z_s, p95_s)
                    if len(z_s) > 0 else np.zeros_like(z_b))
    dmg_on_z_s = (np.interp(z_s, z_b, damaged_frac_b)
                    if len(z_b) > 0 else np.zeros_like(z_s))

    return dict(
        case_name=brittle['case_name'],
        brittle=brittle,
        stress=stress,
        damaged_frac_brittle_bins=damaged_frac_b,
        p95_on_brittle_bins=p95_on_z_b,
        damaged_on_stress_bins=dmg_on_z_s,
    )


def render_combined_figure(profile: dict):
    b = profile['brittle']
    s = profile['stress']

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ── (a) brittle stage stacked histogram ──────────────────────
    ax = axes[0, 0]
    z_b      = b['bin_centers_um']
    edges_b  = b['bin_edges_um']
    counts_b = b['counts']
    bin_h_b  = (edges_b[1] - edges_b[0]) * 0.92 if len(edges_b) > 1 else 1.0
    bottom = np.zeros(len(z_b))
    for stage in STAGE_ORDER:
        ax.barh(z_b, counts_b[stage], left=bottom, height=bin_h_b,
                color=STAGE_COLOR[stage], edgecolor='black',
                linewidth=0.3, label=f'{stage} (n={int(counts_b[stage].sum())})')
        bottom += counts_b[stage]
    ax.set_xlabel('AM-AM contacts per z-bin', fontsize=11)
    ax.set_ylabel('z (µm) — compaction axis', fontsize=11)
    ax.set_title('(a) Brittle fracture stages — Auerbach + Lawn 1998',
                  fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3)
    ax.set_ylim(edges_b[0], edges_b[-1])

    # ── (b) stress bracket stacked histogram ─────────────────────
    ax = axes[0, 1]
    z_s      = s['bin_centers_um']
    edges_s  = s['bin_edges_um']
    counts_s = s['counts_by_bracket']
    bin_h_s  = (edges_s[1] - edges_s[0]) * 0.92 if len(edges_s) > 1 else 1.0
    bottom = np.zeros(len(z_s))
    for lbl, col in zip(BRACKET_LABELS, BRACKET_COLORS):
        ax.barh(z_s, counts_s[lbl], left=bottom, height=bin_h_s,
                color=col, edgecolor='black', linewidth=0.3,
                label=f'{lbl} (n={int(counts_s[lbl].sum())})')
        bottom += counts_s[lbl]
    ax.set_xlabel('Particles per z-bin', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(b) Stress brackets — coolwarm 5-class (log)',
                  fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3)
    ax.set_ylim(edges_s[0], edges_s[-1])

    # ── (c) shared-z overlay: brittle damaged% (bottom x) +
    #         stress p95 (top x) ────────────────────────────────
    ax = axes[1, 0]
    ax.plot(profile['damaged_frac_brittle_bins'], z_b, '-o',
            color='#d62728', lw=2, markersize=5, label='brittle damaged %')
    ax.set_xlabel('Brittle damaged % per z-bin', fontsize=11, color='#d62728')
    ax.tick_params(axis='x', labelcolor='#d62728')
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_ylim(edges_b[0], edges_b[-1])

    ax2 = ax.twiny()
    ax2.plot(s['p95_MPa'], z_s, '-s', color='#1f77b4', lw=2, markersize=5,
              label='stress p95 (MPa)')
    ax2.set_xscale('log')
    ax2.set_xlabel('Stress p95 per z-bin (MPa, log)',
                    fontsize=11, color='#1f77b4')
    ax2.tick_params(axis='x', labelcolor='#1f77b4')

    lns1, lab1 = ax.get_legend_handles_labels()
    lns2, lab2 = ax2.get_legend_handles_labels()
    ax.legend(lns1 + lns2, lab1 + lab2, fontsize=9, loc='lower right')
    ax.set_title('(c) z-axis overlay — brittle damage vs stress p95',
                  fontsize=11, fontweight='bold')

    # ── (d) correlation scatter ──────────────────────────────────
    ax = axes[1, 1]
    p95_on_b = profile['p95_on_brittle_bins']
    sc = ax.scatter(p95_on_b, profile['damaged_frac_brittle_bins'],
                     c=z_b, cmap='viridis', s=80,
                     edgecolor='black', linewidth=0.5, zorder=3)
    ax.set_xscale('log')
    ax.set_xlabel('Stress p95 (MPa, log) at same z-bin', fontsize=11)
    ax.set_ylabel('Brittle damaged %', fontsize=11)
    ax.set_title('(d) Spatial correlation — z-bin colour-coded',
                  fontsize=11, fontweight='bold')
    cb = plt.colorbar(sc, ax=ax)
    cb.set_label('z (µm)', fontsize=10)
    ax.grid(alpha=0.3, which='both')

    # Pearson r if both arrays have variance
    if len(p95_on_b) > 2 and np.std(p95_on_b) > 0 and \
       np.std(profile['damaged_frac_brittle_bins']) > 0:
        log_p95 = np.log10(np.maximum(p95_on_b, 1.0))
        r = float(np.corrcoef(log_p95,
                                profile['damaged_frac_brittle_bins'])[0, 1])
        ax.text(0.02, 0.95, f'Pearson r (log p95, damaged %) = {r:+.3f}',
                 transform=ax.transAxes, fontsize=10,
                 va='top', color='#1f1f1f',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white',
                            ec='#888', lw=0.5))

    plt.suptitle(
        f'Combined z-profile — {profile["case_name"]}\n'
        f'AM-AM contacts: {b["n_total"]} (damaged {b["n_damaged"]}, '
        f'{(100*b["n_damaged"]/max(b["n_total"],1)):.1f}%); '
        f'stressed particles: {s["n_with_stress"]}; '
        f'thickness {b["thickness_um"]:.1f} µm',
        fontsize=13, fontweight='bold', y=1.00,
    )
    plt.tight_layout()
    return fig


def profile_to_csv_rows(profile: dict) -> list[list]:
    """Merged CSV — one row per (aligned) z-bin combining the brittle
    fracture counts with the stress percentile stats.  Uses the
    brittle bin centers as the primary axis (stress p95 is
    interpolated onto them)."""
    b = profile['brittle']
    s = profile['stress']
    z_b      = b['bin_centers_um']
    edges_b  = b['bin_edges_um']
    counts_b = b['counts']
    mean_m   = b['mean_m']
    damaged  = profile['damaged_frac_brittle_bins']
    p95_on_b = profile['p95_on_brittle_bins']
    z_s_centers = s['bin_centers_um']

    header = [
        'z_bin_center_um',
        'z_bin_low_um',
        'z_bin_high_um',
    ] + [f'count_{st}' for st in STAGE_ORDER] + [
        'count_total_amam',
        'damaged_pct',
        'mean_F_over_Pc',
        # Interpolated stress p95 at this z (from stress pipeline)
        'stress_p95_MPa_at_z',
        'stress_mean_MPa_at_z',
        'stress_median_MPa_at_z',
        'stress_max_MPa_at_z',
    ]

    mean_at_b   = (np.interp(z_b, z_s_centers, s['mean_MPa'])
                    if len(z_s_centers) else np.zeros_like(z_b))
    median_at_b = (np.interp(z_b, z_s_centers, s['median_MPa'])
                    if len(z_s_centers) else np.zeros_like(z_b))
    max_at_b    = (np.interp(z_b, z_s_centers, s['max_MPa'])
                    if len(z_s_centers) else np.zeros_like(z_b))
    rows = [header]
    for i, c in enumerate(z_b):
        n_total = sum(int(counts_b[st][i]) for st in STAGE_ORDER)
        rows.append([
            f'{c:.3f}', f'{edges_b[i]:.3f}', f'{edges_b[i+1]:.3f}',
            *(int(counts_b[st][i]) for st in STAGE_ORDER),
            n_total,
            f'{damaged[i]:.2f}',
            f'{mean_m[i]:.4f}',
            f'{p95_on_b[i]:.2f}',
            f'{mean_at_b[i]:.2f}',
            f'{median_at_b[i]:.2f}',
            f'{max_at_b[i]:.2f}',
        ])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_dir')
    ap.add_argument('--bins', type=int, default=25)
    ap.add_argument('--out', default=None)
    ap.add_argument('--csv', default=None)
    args = ap.parse_args()
    case_dir = Path(args.case_dir)
    print(f'Loading {case_dir}')
    profile = compute_combined_zprofile(case_dir, bins=args.bins)
    fig = render_combined_figure(profile)
    out = Path(args.out) if args.out else \
          Path('docs/figures') / f'combined_z_{profile["case_name"]}.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches='tight')
    print(f'✓ Saved PNG: {out.resolve()}')
    if args.csv:
        out_csv = Path(args.csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        with out_csv.open('w', newline='') as f:
            csv.writer(f).writerows(profile_to_csv_rows(profile))
        print(f'✓ Saved CSV: {out_csv.resolve()}')


if __name__ == '__main__':
    main()
