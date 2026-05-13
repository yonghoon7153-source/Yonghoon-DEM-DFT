#!/usr/bin/env python3
"""Z-profile of brittle hotspots — fracture-stage histogram along the
compaction direction.

For every AM-AM contact in a case directory, classify it via
fracture_model.fracture_classify_force_sim, take the z midpoint of
the two contacting particles, and produce a 3-panel figure +
optional CSV dump:

  Panel ① stacked histogram   — # contacts per z-bin, stacked by Lawn stage
  Panel ② normalised stacked  — fraction of contacts in each z-bin damaged
  Panel ③ Auerbach ratio profile — mean F/P_c per z-bin

Public API (used by both CLI and webapp endpoint):
    compute_brittle_zprofile(case_dir, bins=25) -> dict
        Returns the raw arrays / counts ready to plot or serialise.
    render_brittle_figure(profile, case_name=None) -> matplotlib.Figure
    profile_to_csv_rows(profile) -> list[list]   (csv.writer-friendly)

CLI:
    python3 scripts/plot_brittle_z_distribution.py <case_dir>  [--bins 25]
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
from fracture_model import fracture_classify_force_sim


STAGE_ORDER = ['intact', 'microcrack', 'multicrack',
               'fragmentation', 'pulverization']
# ColorBrewer YlOrRd 5-class — academic-style sequential severity ramp.
# Mirrors webapp/static/js/viewer3d.js STAGE_COL so the 3D viewer, the
# z-profile PNG, and the modal table all agree.
STAGE_COLOR = {
    'intact':        '#d9d9d9',
    'microcrack':    '#ffeda0',
    'multicrack':    '#feb24c',
    'fragmentation': '#f03b20',
    'pulverization': '#800026',
}


def fnum(x, default=0.0):
    try: return float(x)
    except Exception: return default


def _load_case(case_dir: Path):
    # meta.json is preferred but historic archive cases sometimes ship
    # without it; fall back to input_params.json or project defaults so
    # this loader works on every directory that has atoms.csv +
    # contacts.csv (matches the 3D viewer's own tolerance).
    meta: dict = {}
    meta_p = case_dir / 'meta.json'
    if meta_p.exists():
        try:
            meta = json.loads(meta_p.read_text())
        except Exception:
            meta = {}
    if not meta:
        ip_p = case_dir / 'input_params.json'
        if ip_p.exists():
            try:
                meta = json.loads(ip_p.read_text())
            except Exception:
                meta = {}
    scale = float(meta.get('scale', 1000.0))
    type_map = {}
    for tok in str(meta.get('type_map', '')).split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try:
                type_map[int(k.strip())] = v.strip()
            except Exception:
                pass
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

    atoms = {}
    for r in csv.DictReader((case_dir / 'atoms.csv').open()):
        aid = int(r['id'])
        atoms[aid] = dict(
            id=aid,
            type=type_map.get(int(r.get('type', 0)), '?'),
            x=fnum(r.get('x')), y=fnum(r.get('y')), z=fnum(r.get('z')),
            r=fnum(r.get('radius') or r.get('r')),
        )
    contacts = []
    for r in csv.DictReader((case_dir / 'contacts.csv').open()):
        try:
            i1 = int(r['id1']); i2 = int(r['id2'])
        except Exception:
            continue
        if i1 not in atoms or i2 not in atoms:
            continue
        fn = fnum(r.get('fn'))
        if not fn:
            fn = math.sqrt(fnum(r.get('fn_x'))**2 +
                           fnum(r.get('fn_y'))**2 +
                           fnum(r.get('fn_z'))**2)
        contacts.append(dict(id1=i1, id2=i2, fn=fn,
                             delta=fnum(r.get('delta'))))
    return atoms, contacts, scale


# ── Public API ────────────────────────────────────────────────

def compute_brittle_zprofile(case_dir, bins: int = 25) -> dict:
    """Compute the z-binned fracture-stage profile for a case directory.

    Returns a dict with keys:
      case_name, thickness_um, n_total, n_damaged, damaged_pct,
      bin_edges_um, bin_centers_um,
      counts (dict of stage → np.array of length `bins`),
      mean_m (np.array of length `bins`),
      stage_totals (dict of stage → int),
    """
    case_dir = Path(case_dir)
    atoms, contacts, scale = _load_case(case_dir)
    am_am = []
    for c in contacts:
        a1 = atoms[c['id1']]; a2 = atoms[c['id2']]
        if 'AM' not in a1['type'] or 'AM' not in a2['type']:
            continue
        ct = '-'.join(sorted([a1['type'], a2['type']]))
        r_min_sim = min(a1['r'], a2['r'])
        stage, _, m = fracture_classify_force_sim(
            c['fn'], r_min_sim, contact_type=ct, scale=scale)
        z_mid = 0.5 * (a1['z'] + a2['z'])
        am_am.append((z_mid, stage, m))

    n_total = len(am_am)
    stage_totals = {s: 0 for s in STAGE_ORDER}
    for _, s, _ in am_am: stage_totals[s] += 1
    n_damaged = sum(v for k, v in stage_totals.items() if k != 'intact')

    if n_total == 0:
        return dict(case_name=case_dir.name,
                    thickness_um=0.0, n_total=0,
                    n_damaged=0, damaged_pct=0.0,
                    bin_edges_um=np.array([0.0, 1.0]),
                    bin_centers_um=np.array([0.5]),
                    counts={s: np.zeros(1, dtype=int)
                            for s in STAGE_ORDER},
                    mean_m=np.zeros(1),
                    stage_totals=stage_totals)

    zs = np.array([x[0] for x in am_am])
    z_min_um = zs.min() * 1e6 / scale
    z_max_um = zs.max() * 1e6 / scale
    z_phys = zs * 1e6 / scale
    thickness = z_max_um - z_min_um

    bin_edges = np.linspace(z_min_um, z_max_um, bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    counts = {s: np.zeros(bins, dtype=int) for s in STAGE_ORDER}
    ms_in_bin: list[list[float]] = [[] for _ in range(bins)]
    for (_, stage, m), z in zip(am_am, z_phys):
        b = min(bins - 1, max(0, np.digitize(z, bin_edges) - 1))
        counts[stage][b] += 1
        ms_in_bin[b].append(m)
    mean_m = np.array([np.mean(ms) if ms else 0 for ms in ms_in_bin])

    return dict(
        case_name=case_dir.name,
        thickness_um=float(thickness),
        n_total=int(n_total),
        n_damaged=int(n_damaged),
        damaged_pct=100.0 * n_damaged / n_total,
        bin_edges_um=bin_edges,
        bin_centers_um=bin_centers,
        counts=counts,
        mean_m=mean_m,
        stage_totals=stage_totals,
    )


def render_brittle_figure(profile: dict):
    """Render the 3-panel matplotlib Figure from a compute result."""
    counts        = profile['counts']
    bin_edges     = profile['bin_edges_um']
    bin_centers   = profile['bin_centers_um']
    mean_m        = profile['mean_m']
    case_name     = profile['case_name']
    thickness     = profile['thickness_um']
    n_total       = profile['n_total']
    n_damaged     = profile['n_damaged']
    z_lo, z_hi    = bin_edges[0], bin_edges[-1]
    bin_h         = (bin_edges[1] - bin_edges[0]) * 0.92 if len(bin_edges) > 1 else 1.0
    bins          = len(bin_centers)

    fig, axes = plt.subplots(1, 3, figsize=(17, 6.5))

    # (a) stacked count
    ax = axes[0]
    bottom = np.zeros(bins)
    for s in STAGE_ORDER:
        ax.barh(bin_centers, counts[s], left=bottom, height=bin_h,
                color=STAGE_COLOR[s], edgecolor='black', linewidth=0.3,
                label=f'{s} (n={int(counts[s].sum())})')
        bottom += counts[s]
    ax.set_xlabel('AM-AM contacts per z-bin', fontsize=11)
    ax.set_ylabel('z (µm) — compaction axis', fontsize=11)
    ax.set_title('(a) Stacked count by Lawn fracture stage',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3); ax.set_ylim(z_lo, z_hi)

    # (b) per-bin damage composition
    ax = axes[1]
    bin_total = np.zeros(bins)
    for s in STAGE_ORDER: bin_total += counts[s]
    bin_total_safe = np.where(bin_total > 0, bin_total, 1)
    left_acc = np.zeros(bins)
    for s in STAGE_ORDER:
        frac = counts[s] / bin_total_safe
        ax.barh(bin_centers, frac, left=left_acc, height=bin_h,
                color=STAGE_COLOR[s], edgecolor='black', linewidth=0.3,
                label=s)
        left_acc += frac
    ax.axvline(1.0, color='k', lw=0.8)
    ax.set_xlabel('Fraction of contacts in bin', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(b) Per-bin damage composition (fraction)',
                 fontsize=11, fontweight='bold')
    ax.set_xlim(0, 1.05); ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc='lower right'); ax.set_ylim(z_lo, z_hi)

    # (c) mean F/P_c
    ax = axes[2]
    ax.plot(mean_m, bin_centers, '-o', color='crimson', lw=2, markersize=6)
    ax.axvline(1, color='gray', ls='--', lw=1, label='m=1 (Auerbach onset)')
    ax.axvline(3, color='orange', ls=':', lw=1, label='m=3 (multicrack)')
    ax.axvline(11, color='red', ls=':', lw=1, label='m=11 (fragmentation)')
    ax.set_xlabel('Mean F/P_c per z-bin', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(c) Mean Auerbach ratio profile',
                 fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3); ax.legend(fontsize=9, loc='lower right')
    ax.set_xscale('log'); ax.set_ylim(z_lo, z_hi)

    plt.suptitle(
        f'Brittle-hotspot z-profile — {case_name}\n'
        f'AM-AM contacts: {n_total} (damaged {n_damaged}, '
        f'{(100*n_damaged/max(n_total,1)):.1f}%);  '
        f'thickness {thickness:.1f} µm',
        fontsize=13, fontweight='bold', y=1.00,
    )
    plt.tight_layout()
    return fig


def profile_to_csv_rows(profile: dict) -> list[list]:
    """Flatten profile to list-of-rows suitable for csv.writer."""
    rows = [[
        'z_bin_center_um', 'z_bin_low_um', 'z_bin_high_um',
        'count_intact', 'count_microcrack', 'count_multicrack',
        'count_fragmentation', 'count_pulverization',
        'count_total', 'count_damaged', 'damaged_fraction',
        'mean_F_over_Pc',
    ]]
    counts      = profile['counts']
    centers     = profile['bin_centers_um']
    edges       = profile['bin_edges_um']
    mean_m      = profile['mean_m']
    for i, c in enumerate(centers):
        n_i = counts['intact'][i]
        n_mu = counts['microcrack'][i]
        n_m  = counts['multicrack'][i]
        n_f  = counts['fragmentation'][i]
        n_p  = counts['pulverization'][i]
        n_tot = n_i + n_mu + n_m + n_f + n_p
        n_dmg = n_mu + n_m + n_f + n_p
        rows.append([
            f'{c:.3f}', f'{edges[i]:.3f}', f'{edges[i+1]:.3f}',
            int(n_i), int(n_mu), int(n_m), int(n_f), int(n_p),
            int(n_tot), int(n_dmg),
            f'{(n_dmg/n_tot if n_tot else 0):.4f}',
            f'{mean_m[i]:.4f}',
        ])
    return rows


# ── CLI ───────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_dir')
    ap.add_argument('--bins', type=int, default=25)
    ap.add_argument('--out', default=None,
                    help='Output PNG path (default: '
                         'docs/figures/brittle_z_<case>.png)')
    ap.add_argument('--csv', default=None,
                    help='Also write CSV to this path')
    args = ap.parse_args()

    case_dir = Path(args.case_dir)
    if not (case_dir / 'atoms.csv').exists():
        print(f'❌ {case_dir} missing atoms.csv'); sys.exit(1)
    print(f'Loading {case_dir}')

    profile = compute_brittle_zprofile(case_dir, bins=args.bins)
    print(f'  AM-AM contacts: {profile["n_total"]}')
    for s in STAGE_ORDER:
        print(f'    {s:>14s}: {profile["stage_totals"][s]}')
    print(f'  damaged: {profile["n_damaged"]}  '
          f'({profile["damaged_pct"]:.1f}%)')
    print(f'  thickness: {profile["thickness_um"]:.1f} µm')

    if profile['n_total'] == 0:
        print('No AM-AM contacts — exit.'); sys.exit(0)

    fig = render_brittle_figure(profile)
    out = Path(args.out) if args.out else \
          Path('docs/figures') / f'brittle_z_{profile["case_name"]}.png'
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
