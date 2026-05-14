#!/usr/bin/env python3
"""Z-profile of per-AM particle SE-coverage %.

Sister script to plot_brittle_z_distribution.py + plot_stress_z_
distribution.py — reads the case's coverage_per_am.csv (output of
scripts/coverage_physics_vs_hertzian.py), joins with atoms.csv for
z positions, and produces a 3-panel figure + matching CSV.

Coverage = (SE-contact surface area on this AM) / (total AM surface
area), already given in % by the upstream computation.

  Panel ① Coverage band stacked histogram (5 classes from
           ColorBrewer RdYlGn diverging palette: red = critically
           low coverage, green = optimal)
  Panel ② Per-bin median ± [p5, p95] band on a coverage axis
  Panel ③ AM_P vs AM_S coverage distributions side-by-side as
           horizontal bin counts

Public API:
  compute_coverage_zprofile(case_dir, bins=25) -> dict
  render_coverage_figure(profile) -> matplotlib Figure
  profile_to_csv_rows(profile) -> list[list]

CLI:
  python3 scripts/plot_coverage_z_distribution.py <case_dir> [--bins 25]
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from plot_brittle_z_distribution import _load_case   # noqa: E402


# 5-class ColorBrewer RdYlGn discrete cutoffs.  Red = critical, green
# = optimal — matches the 3D viewer's coverage colormap.
BAND_LABELS = ['critical', 'low', 'mid', 'high', 'optimal']
BAND_COLORS = ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']
PARTICLE_TYPE_ORDER = ['AM_P', 'AM_S']


def _load_coverage_csv(case_dir: Path) -> dict[int, float]:
    """Returns {am_id: coverage_pct}.  Prefers physics column when
    available, falls back to hertzian (matches viewer3d_data.build_
    coverage_map)."""
    p = case_dir / 'coverage_per_am.csv'
    out: dict[int, float] = {}
    if not p.exists():
        return out
    try:
        import pandas as pd
        df = pd.read_csv(p)
    except Exception:
        return out
    col = ('coverage_physics_pct' if 'coverage_physics_pct' in df.columns
           else 'coverage_hertzian_pct' if 'coverage_hertzian_pct' in df.columns
           else None)
    if 'am_id' not in df.columns or col is None:
        return out
    for _, r in df.iterrows():
        try:
            out[int(r['am_id'])] = float(r[col])
        except Exception:
            pass
    return out


def compute_coverage_zprofile(case_dir, bins: int = 25) -> dict:
    """Z-binned coverage statistics for every AM particle that has a
    coverage value in coverage_per_am.csv."""
    case_dir = Path(case_dir)
    atoms, _, scale = _load_case(case_dir)
    cov_map = _load_coverage_csv(case_dir)

    # Collect (z_um, coverage_pct, type) per AM particle that has data
    rows = []
    for aid, cov in cov_map.items():
        a = atoms.get(aid)
        if a is None:
            continue
        t = a.get('type', '?')
        if 'AM' not in t:
            continue
        rows.append((a['z'] * 1.0e6 / scale, float(cov), t))

    n_with_cov = len(rows)
    if not rows:
        return dict(case_name=case_dir.name, thickness_um=0.0,
                    n_with_cov=0,
                    bin_edges_um=np.array([0.0, 1.0]),
                    bin_centers_um=np.array([0.5]),
                    counts_per_type={t: np.zeros(1, dtype=int)
                                     for t in PARTICLE_TYPE_ORDER},
                    counts_by_band={b: np.zeros(1, dtype=int)
                                    for b in BAND_LABELS},
                    mean_pct=np.zeros(1), median_pct=np.zeros(1),
                    p5_pct=np.zeros(1), p95_pct=np.zeros(1),
                    band_edges_pct=np.array([0]*6),
                    type_totals={t: 0 for t in PARTICLE_TYPE_ORDER},
                    cLo=0.0, cMed=0.0, cHi=0.0, cMean=0.0)

    zs = np.array([r[0] for r in rows])
    cs = np.array([r[1] for r in rows])

    z_min, z_max = float(zs.min()), float(zs.max())
    thickness = z_max - z_min
    bin_edges = np.linspace(z_min, z_max, bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Global percentile anchors
    sorted_c = np.sort(cs)
    def pct(p): return float(sorted_c[int(p * (len(sorted_c) - 1))])
    cLo, cMed, cHi = pct(0.05), pct(0.50), pct(0.95)
    cMean = float(cs.mean())

    # 5-class band cutoffs anchored to the percentile range so the
    # bracketing matches what the 3D viewer's colormap shows.
    band_edges = np.linspace(cLo, cHi, 6)

    counts_per_type = {t: np.zeros(bins, dtype=int) for t in PARTICLE_TYPE_ORDER}
    counts_by_band  = {b: np.zeros(bins, dtype=int) for b in BAND_LABELS}
    cs_in_bin: list[list[float]] = [[] for _ in range(bins)]
    type_totals = {t: 0 for t in PARTICLE_TYPE_ORDER}

    for (z, c, t) in rows:
        b = min(bins - 1, max(0, int(np.digitize(z, bin_edges) - 1)))
        cs_in_bin[b].append(c)
        if t in counts_per_type:
            counts_per_type[t][b] += 1
            type_totals[t] += 1
        bi = int(np.searchsorted(band_edges, c, side='right') - 1)
        bi = max(0, min(len(BAND_LABELS) - 1, bi))
        counts_by_band[BAND_LABELS[bi]][b] += 1

    def _stat(idx, fn, default=0.0):
        return float(fn(cs_in_bin[idx])) if cs_in_bin[idx] else default
    mean_pct   = np.array([_stat(i, np.mean) for i in range(bins)])
    median_pct = np.array([_stat(i, np.median) for i in range(bins)])
    p5_pct     = np.array([_stat(i, lambda v: np.percentile(v, 5))  for i in range(bins)])
    p95_pct    = np.array([_stat(i, lambda v: np.percentile(v, 95)) for i in range(bins)])

    return dict(
        case_name=case_dir.name,
        thickness_um=float(thickness),
        n_with_cov=int(n_with_cov),
        bin_edges_um=bin_edges,
        bin_centers_um=bin_centers,
        counts_per_type=counts_per_type,
        counts_by_band=counts_by_band,
        mean_pct=mean_pct, median_pct=median_pct,
        p5_pct=p5_pct, p95_pct=p95_pct,
        band_edges_pct=band_edges,
        type_totals=type_totals,
        cLo=cLo, cMed=cMed, cHi=cHi, cMean=cMean,
    )


def render_coverage_figure(profile: dict):
    bin_edges = profile['bin_edges_um']
    centers   = profile['bin_centers_um']
    counts_b  = profile['counts_by_band']
    counts_t  = profile['counts_per_type']
    median_   = profile['median_pct']
    p5_       = profile['p5_pct']
    p95_      = profile['p95_pct']
    mean_     = profile['mean_pct']
    name      = profile['case_name']
    n_cov     = profile['n_with_cov']
    cMean     = profile['cMean']

    z_lo, z_hi = bin_edges[0], bin_edges[-1]
    bins = len(centers)
    bin_h = (bin_edges[1] - bin_edges[0]) * 0.92 if len(bin_edges) > 1 else 1.0

    fig, axes = plt.subplots(1, 3, figsize=(17, 6.5))

    # (a) coverage band stacked histogram
    ax = axes[0]
    bottom = np.zeros(bins)
    for lbl, col in zip(BAND_LABELS, BAND_COLORS):
        ax.barh(centers, counts_b[lbl], left=bottom, height=bin_h,
                color=col, edgecolor='black', linewidth=0.3,
                label=f'{lbl} (n={int(counts_b[lbl].sum())})')
        bottom += counts_b[lbl]
    ax.set_xlabel('AM particles per z-bin', fontsize=11)
    ax.set_ylabel('z (µm) — compaction axis', fontsize=11)
    ax.set_title('(a) Coverage band distribution\nColorBrewer RdYlGn 5-class',
                  fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3); ax.set_ylim(z_lo, z_hi)

    # (b) per-bin median + [p5, p95] band
    ax = axes[1]
    ax.fill_betweenx(centers, p5_, p95_, color='#a6d96a',
                      alpha=0.35, label='p5 – p95 band')
    ax.plot(median_, centers, '-o', color='#1a9641', lw=2, markersize=5, label='median')
    ax.plot(mean_,   centers, '--', color='#444',    lw=1, label='mean')
    ax.axvline(cMean, color='#888', ls=':', lw=0.8,
                label=f'case mean ≈ {cMean:.1f}%')
    ax.set_xlabel('Coverage (% of AM surface)', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(b) Per-bin coverage stats', fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3); ax.legend(fontsize=9, loc='lower right')
    ax.set_ylim(z_lo, z_hi)

    # (c) AM_P vs AM_S split bin counts
    ax = axes[2]
    bottom = np.zeros(bins)
    type_colors = {'AM_P': '#444444', 'AM_S': '#888888'}
    for t in PARTICLE_TYPE_ORDER:
        ax.barh(centers, counts_t[t], left=bottom, height=bin_h,
                color=type_colors[t], edgecolor='black', linewidth=0.3,
                label=f'{t} (n={int(counts_t[t].sum())})')
        bottom += counts_t[t]
    ax.set_xlabel('AM particles per z-bin (by type)', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(c) AM_P vs AM_S distribution',
                  fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3); ax.set_ylim(z_lo, z_hi)

    plt.suptitle(
        f'Coverage z-profile — {name}\n'
        f'AM particles with coverage data: {n_cov} ; '
        f'thickness {profile["thickness_um"]:.1f} µm ; '
        f'case mean ≈ {cMean:.1f}%',
        fontsize=13, fontweight='bold', y=1.00,
    )
    plt.tight_layout()
    return fig


def profile_to_csv_rows(profile: dict) -> list[list]:
    header = [
        'z_bin_center_um', 'z_bin_low_um', 'z_bin_high_um',
        'count_total',
        'mean_pct', 'median_pct', 'p5_pct', 'p95_pct',
    ]
    for t in PARTICLE_TYPE_ORDER:
        header.append(f'count_{t}')
    for lbl in BAND_LABELS:
        header.append(f'count_band_{lbl}')
    rows = [header]

    centers = profile['bin_centers_um']
    edges   = profile['bin_edges_um']
    cpT     = profile['counts_per_type']
    cpB     = profile['counts_by_band']
    mean_   = profile['mean_pct']
    median_ = profile['median_pct']
    p5_     = profile['p5_pct']
    p95_    = profile['p95_pct']

    for i, c in enumerate(centers):
        total = sum(int(cpT[t][i]) for t in PARTICLE_TYPE_ORDER)
        row = [
            f'{c:.3f}', f'{edges[i]:.3f}', f'{edges[i+1]:.3f}',
            total,
            f'{mean_[i]:.2f}', f'{median_[i]:.2f}',
            f'{p5_[i]:.2f}',   f'{p95_[i]:.2f}',
        ]
        for t in PARTICLE_TYPE_ORDER:
            row.append(int(cpT[t][i]))
        for lbl in BAND_LABELS:
            row.append(int(cpB[lbl][i]))
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_dir')
    ap.add_argument('--bins', type=int, default=25)
    ap.add_argument('--out', default=None)
    ap.add_argument('--csv', default=None)
    args = ap.parse_args()

    case_dir = Path(args.case_dir)
    if not (case_dir / 'coverage_per_am.csv').exists():
        print(f'❌ {case_dir} missing coverage_per_am.csv — '
              f'run scripts/coverage_physics_vs_hertzian.py first')
        sys.exit(1)
    print(f'Loading {case_dir}')

    profile = compute_coverage_zprofile(case_dir, bins=args.bins)
    print(f'  AM with coverage data: {profile["n_with_cov"]}')
    print(f'  global — mean: {profile["cMean"]:.1f}%   '
          f'median: {profile["cMed"]:.1f}%   '
          f'5/95th: {profile["cLo"]:.1f} / {profile["cHi"]:.1f}%')

    if profile['n_with_cov'] == 0:
        print('No AM with coverage data — exit.'); sys.exit(0)

    fig = render_coverage_figure(profile)
    out = Path(args.out) if args.out else \
          Path('docs/figures') / f'coverage_z_{profile["case_name"]}.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches='tight')
    print(f'\n✓ Saved PNG: {out.resolve()}')

    if args.csv:
        out_csv = Path(args.csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        with out_csv.open('w', newline='') as f:
            csv.writer(f).writerows(profile_to_csv_rows(profile))
        print(f'✓ Saved CSV: {out_csv.resolve()}')


if __name__ == '__main__':
    main()
