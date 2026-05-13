#!/usr/bin/env python3
"""Z-profile of per-particle MAX contact pressure (Stress hotspots).

Mirrors scripts/plot_brittle_z_distribution.py but for the stress
field that drives the Brittle Hotspots upstream:

  Panel ① stacked histogram of N particles per z-bin, coloured
           by stress bracket (low → high)
  Panel ② per-bin pressure stats — median, p95, max
  Panel ③ box-like spread of stress values per z-bin

Public API:
  compute_stress_zprofile(case_dir, bins=25) -> dict
  render_stress_figure(profile) -> matplotlib Figure
  profile_to_csv_rows(profile) -> list[list]

CLI:
  python3 scripts/plot_stress_z_distribution.py <case_dir> [--bins 25]
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))


# Reuse the brittle loader so meta.json / input_params.json /
# default fallback resolution stays consistent across the two
# z-profile flavours.
from plot_brittle_z_distribution import _load_case  # noqa: E402


PARTICLE_TYPE_ORDER = ['AM_P', 'AM_S', 'SE']

# 5-class blue-to-red bracketing for the stacked-count panel.  Anchored
# at the same log10 / percentile split the 3D viewer uses, so the
# colour banding in the PNG matches the in-browser field.
BRACKET_LABELS = ['low', 'mid-low', 'mid', 'mid-high', 'high']
BRACKET_COLORS = ['#3b4cc0', '#7d97c5', '#dddddd', '#d6604d', '#b40426']


def _aggregate_stress_max(case_dir: Path):
    """Recompute per-particle max contact pressure from contacts.csv +
    atoms.csv, matching the in-browser aux.stress_max derivation."""
    atoms, contacts, scale = _load_case(case_dir)
    stress_max: dict[int, float] = {}
    pressure_conv = scale / 1.0e6  # sim Pa → real MPa
    for c in contacts:
        i1, i2 = c['id1'], c['id2']
        if i1 not in atoms or i2 not in atoms:
            continue
        # We need contact_area; the loader keeps fn + delta but not
        # area.  Re-read contacts.csv directly here for the area.
        # Simpler: also pull contact_area inline.
        pass

    # Direct re-parse of contacts.csv for contact_area + fn.
    p = case_dir / 'contacts.csv'
    if not p.exists():
        return atoms, {}, scale
    for r in csv.DictReader(p.open()):
        try:
            i1 = int(r['id1']); i2 = int(r['id2'])
        except Exception:
            continue
        if i1 not in atoms or i2 not in atoms:
            continue
        try:
            area = float(r.get('contact_area') or 0)
            fn = float(r.get('fn') or 0)
            if not fn:
                fn = math.sqrt(float(r.get('fn_x') or 0)**2 +
                               float(r.get('fn_y') or 0)**2 +
                               float(r.get('fn_z') or 0)**2)
        except Exception:
            continue
        if area <= 0 or fn <= 0:
            continue
        p_MPa = fn / area * pressure_conv
        for aid in (i1, i2):
            if p_MPa > stress_max.get(aid, 0):
                stress_max[aid] = p_MPa
    return atoms, stress_max, scale


def compute_stress_zprofile(case_dir, bins: int = 25) -> dict:
    """Z-binned per-particle max contact pressure statistics.

    Returns dict with:
      case_name, thickness_um, n_total, n_with_stress,
      bin_edges_um, bin_centers_um,
      counts_per_type (dict of type → np.array of length `bins`),
      counts_by_bracket (dict of bracket label → np.array),
      mean_MPa, median_MPa, p95_MPa, max_MPa  (each length-`bins` np.array),
      bracket_edges_MPa  (5-class log cutoffs, length-6),
      type_totals (dict of type → int),
      sLo / sMed / sHi / sMax — global 5th / 50th / 95th / max in MPa.
    """
    case_dir = Path(case_dir)
    atoms, stress_max, scale = _aggregate_stress_max(case_dir)

    # Collect per-particle (z_um, stress, type) for particles with a
    # positive max stress
    rows = []
    for aid, s in stress_max.items():
        a = atoms.get(aid)
        if a is None or not (s > 0):
            continue
        rows.append((a['z'] * 1.0e6 / scale, s, a['type']))

    n_total = len(stress_max)
    n_with_stress = len(rows)

    if not rows:
        return dict(case_name=case_dir.name,
                    thickness_um=0.0, n_total=n_total, n_with_stress=0,
                    bin_edges_um=np.array([0.0, 1.0]),
                    bin_centers_um=np.array([0.5]),
                    counts_per_type={t: np.zeros(1, dtype=int)
                                     for t in PARTICLE_TYPE_ORDER},
                    counts_by_bracket={lbl: np.zeros(1, dtype=int)
                                       for lbl in BRACKET_LABELS},
                    mean_MPa=np.zeros(1), median_MPa=np.zeros(1),
                    p95_MPa=np.zeros(1), max_MPa=np.zeros(1),
                    bracket_edges_MPa=np.array([0]*6),
                    type_totals={t: 0 for t in PARTICLE_TYPE_ORDER},
                    sLo=0.0, sMed=0.0, sHi=0.0, sMax=0.0)

    zs = np.array([r[0] for r in rows])
    ss = np.array([r[1] for r in rows])
    ts = [r[2] for r in rows]

    z_min, z_max = float(zs.min()), float(zs.max())
    thickness = z_max - z_min
    bin_edges = np.linspace(z_min, z_max, bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Global percentile anchors
    sorted_s = np.sort(ss)
    def pct(p): return float(sorted_s[int(p * (len(sorted_s) - 1))])
    sLo, sMed, sHi, sMax = pct(0.05), pct(0.50), pct(0.95), float(sorted_s[-1])

    # 5-class brackets in log space between the 5th and 95th percentile
    log_lo = math.log10(max(1.0, sLo))
    log_hi = math.log10(max(sLo * 1.5, sHi))
    bracket_edges = np.logspace(log_lo, log_hi, 6)

    counts_per_type   = {t: np.zeros(bins, dtype=int) for t in PARTICLE_TYPE_ORDER}
    counts_by_bracket = {lbl: np.zeros(bins, dtype=int) for lbl in BRACKET_LABELS}
    ss_in_bin: list[list[float]] = [[] for _ in range(bins)]
    type_totals = {t: 0 for t in PARTICLE_TYPE_ORDER}

    for (z, s, t) in rows:
        b = min(bins - 1, max(0, int(np.digitize(z, bin_edges) - 1)))
        ss_in_bin[b].append(s)
        if t in counts_per_type:
            counts_per_type[t][b] += 1
            type_totals[t] += 1
        # Bracket index 0-4 by where s falls in bracket_edges
        # bracket_edges has 6 entries → 5 brackets
        bi = int(np.searchsorted(bracket_edges, s, side='right') - 1)
        bi = max(0, min(len(BRACKET_LABELS) - 1, bi))
        counts_by_bracket[BRACKET_LABELS[bi]][b] += 1

    def _stat(idx, fn, default=0.0):
        return float(fn(ss_in_bin[idx])) if ss_in_bin[idx] else default
    mean_MPa   = np.array([_stat(i, np.mean) for i in range(bins)])
    median_MPa = np.array([_stat(i, np.median) for i in range(bins)])
    p95_MPa    = np.array([_stat(i, lambda v: np.percentile(v, 95)) for i in range(bins)])
    max_MPa    = np.array([_stat(i, np.max) for i in range(bins)])

    return dict(
        case_name=case_dir.name,
        thickness_um=float(thickness),
        n_total=int(n_total),
        n_with_stress=int(n_with_stress),
        bin_edges_um=bin_edges,
        bin_centers_um=bin_centers,
        counts_per_type=counts_per_type,
        counts_by_bracket=counts_by_bracket,
        mean_MPa=mean_MPa,
        median_MPa=median_MPa,
        p95_MPa=p95_MPa,
        max_MPa=max_MPa,
        bracket_edges_MPa=bracket_edges,
        type_totals=type_totals,
        sLo=float(sLo), sMed=float(sMed), sHi=float(sHi), sMax=float(sMax),
    )


def render_stress_figure(profile: dict):
    bin_edges = profile['bin_edges_um']
    centers   = profile['bin_centers_um']
    counts_b  = profile['counts_by_bracket']
    mean_     = profile['mean_MPa']
    median_   = profile['median_MPa']
    p95_      = profile['p95_MPa']
    max_      = profile['max_MPa']
    name      = profile['case_name']
    n_with    = profile['n_with_stress']
    sMed      = profile['sMed']
    sHi       = profile['sHi']

    z_lo, z_hi = bin_edges[0], bin_edges[-1]
    bins = len(centers)
    bin_h = (bin_edges[1] - bin_edges[0]) * 0.92 if len(bin_edges) > 1 else 1.0

    fig, axes = plt.subplots(1, 3, figsize=(17, 6.5))

    # (a) stacked count by stress bracket
    ax = axes[0]
    bottom = np.zeros(bins)
    for lbl, col in zip(BRACKET_LABELS, BRACKET_COLORS):
        ax.barh(centers, counts_b[lbl], left=bottom, height=bin_h,
                color=col, edgecolor='black', linewidth=0.3,
                label=f'{lbl} (n={int(counts_b[lbl].sum())})')
        bottom += counts_b[lbl]
    ax.set_xlabel('Particles per z-bin', fontsize=11)
    ax.set_ylabel('z (µm) — compaction axis', fontsize=11)
    ax.set_title('(a) Stress bracket distribution\n'
                 'coolwarm 5-class on log scale', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3); ax.set_ylim(z_lo, z_hi)

    # (b) per-bin pressure stats (median + p95 + max)
    ax = axes[1]
    ax.plot(median_, centers, '-o', color='#3b4cc0', lw=2, markersize=5, label='median')
    ax.plot(p95_,    centers, '-s', color='#d6604d', lw=2, markersize=5, label='p95')
    ax.plot(max_,    centers, '-^', color='#7f1d1d', lw=1, markersize=4, label='max')
    ax.axvline(sMed, color='gray',  ls='--', lw=0.8, label=f'global median ≈ {sMed:.0f}')
    ax.axvline(sHi,  color='red',   ls=':',  lw=0.8, label=f'global p95 ≈ {sHi:.0f}')
    ax.set_xscale('log')
    ax.set_xlabel('Contact pressure (MPa, log)', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(b) Per-bin pressure stats', fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3, which='both'); ax.legend(fontsize=9, loc='lower right')
    ax.set_ylim(z_lo, z_hi)

    # (c) box-like spread — mean ± half(p95 - median) shaded band
    ax = axes[2]
    lo_band = np.maximum(mean_ - (mean_ - median_), 1.0)
    hi_band = np.maximum(p95_, mean_)
    ax.fill_betweenx(centers, lo_band, hi_band, color='#d6604d',
                      alpha=0.30, label='median–p95 band')
    ax.plot(mean_, centers, '-o', color='#1f1f1f', lw=2, markersize=4,
            label='bin mean')
    ax.set_xscale('log')
    ax.set_xlabel('Contact pressure (MPa, log)', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(c) Mean + median-to-p95 spread',
                  fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3, which='both'); ax.legend(fontsize=9, loc='lower right')
    ax.set_ylim(z_lo, z_hi)

    plt.suptitle(
        f'Stress-hotspot z-profile — {name}\n'
        f'particles with positive contact pressure: {n_with}; '
        f'thickness {profile["thickness_um"]:.1f} µm',
        fontsize=13, fontweight='bold', y=1.00,
    )
    plt.tight_layout()
    return fig


def profile_to_csv_rows(profile: dict) -> list[list]:
    """Flatten profile to list-of-rows (z bin centers + per-bin stats +
    per-type counts + per-bracket counts)."""
    header = [
        'z_bin_center_um', 'z_bin_low_um', 'z_bin_high_um',
        'count_total',
        'mean_MPa', 'median_MPa', 'p95_MPa', 'max_MPa',
    ]
    for t in PARTICLE_TYPE_ORDER:
        header.append(f'count_{t}')
    for lbl in BRACKET_LABELS:
        header.append(f'count_bracket_{lbl}')
    rows = [header]

    centers = profile['bin_centers_um']
    edges   = profile['bin_edges_um']
    cpT     = profile['counts_per_type']
    cpB     = profile['counts_by_bracket']
    mean_   = profile['mean_MPa']
    median_ = profile['median_MPa']
    p95_    = profile['p95_MPa']
    max_    = profile['max_MPa']

    for i, c in enumerate(centers):
        total = sum(int(cpT[t][i]) for t in PARTICLE_TYPE_ORDER)
        row = [
            f'{c:.3f}', f'{edges[i]:.3f}', f'{edges[i+1]:.3f}',
            total,
            f'{mean_[i]:.2f}',   f'{median_[i]:.2f}',
            f'{p95_[i]:.2f}',    f'{max_[i]:.2f}',
        ]
        for t in PARTICLE_TYPE_ORDER:
            row.append(int(cpT[t][i]))
        for lbl in BRACKET_LABELS:
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
    if not (case_dir / 'atoms.csv').exists():
        print(f'❌ {case_dir} missing atoms.csv'); sys.exit(1)
    print(f'Loading {case_dir}')

    profile = compute_stress_zprofile(case_dir, bins=args.bins)
    print(f'  particles with positive stress: {profile["n_with_stress"]}')
    print(f'  global stats — median: {profile["sMed"]:.1f}  '
          f'p95: {profile["sHi"]:.1f}  max: {profile["sMax"]:.1f} MPa')
    print(f'  thickness: {profile["thickness_um"]:.1f} µm')

    if profile['n_with_stress'] == 0:
        print('No stressed particles — exit.'); sys.exit(0)

    fig = render_stress_figure(profile)
    out = Path(args.out) if args.out else \
          Path('docs/figures') / f'stress_z_{profile["case_name"]}.png'
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
