#!/usr/bin/env python3
"""Z-profile of brittle hotspots — fracture-stage histogram along the
compaction direction.

For every AM-AM contact in a case directory, classify it via
fracture_model.fracture_classify_force_sim, take the z midpoint of
the two contacting particles, and produce:

  Panel ① stacked histogram   — # contacts per z-bin, stacked by Lawn stage
  Panel ② normalised stacked  — fraction of contacts in each z-bin damaged
                                (each bin sums to 1.0)
  Panel ③ Auerbach ratio profile — mean F/P_c per z-bin
                                   (intact m<1, damage starts at m=1)

Usage:
    python3 scripts/plot_brittle_z_distribution.py <case_dir>  [--bins 25]

Outputs:
    docs/figures/brittle_z_<case_name>.png
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
STAGE_COLOR = {
    'intact':        '#cccccc',
    'microcrack':    '#ffd54f',  # yellow
    'multicrack':    '#ff8c00',  # orange
    'fragmentation': '#d62728',  # red
    'pulverization': '#9b1c8c',  # magenta
}


def fnum(x, default=0.0):
    try: return float(x)
    except Exception: return default


def load_case(case_dir: Path):
    meta = json.loads((case_dir / 'meta.json').read_text())
    scale = float(meta.get('scale', 1000.0))
    type_map = {}
    for tok in str(meta.get('type_map', '')).split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            type_map[int(k.strip())] = v.strip()
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
        contacts.append(dict(
            id1=i1, id2=i2, fn=fn,
            delta=fnum(r.get('delta')),
        ))
    return atoms, contacts, scale


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_dir')
    ap.add_argument('--bins', type=int, default=25)
    ap.add_argument('--out', default=None,
                    help='Output PNG path (default: '
                         'docs/figures/brittle_z_<case_name>.png)')
    args = ap.parse_args()

    case_dir = Path(args.case_dir)
    if not (case_dir / 'atoms.csv').exists():
        print(f'❌ {case_dir} missing atoms.csv'); sys.exit(1)
    print(f'Loading {case_dir}')

    atoms, contacts, scale = load_case(case_dir)
    print(f'  atoms: {len(atoms)},  contacts: {len(contacts)},  scale={scale}')

    # Filter AM-AM contacts and classify each
    am_am = []
    for c in contacts:
        a1 = atoms[c['id1']]; a2 = atoms[c['id2']]
        if 'AM' not in a1['type'] or 'AM' not in a2['type']:
            continue
        ct = '-'.join(sorted([a1['type'], a2['type']]))
        r_min_sim = min(a1['r'], a2['r'])
        stage, P_c_sim, m = fracture_classify_force_sim(
            c['fn'], r_min_sim, contact_type=ct, scale=scale)
        z_mid = 0.5 * (a1['z'] + a2['z'])
        am_am.append(dict(z=z_mid, stage=stage, m=m, ct=ct,
                          fn=c['fn']))

    n_total = len(am_am)
    stage_count = {s: sum(1 for x in am_am if x['stage'] == s)
                   for s in STAGE_ORDER}
    print(f'  AM-AM contacts: {n_total}')
    for s in STAGE_ORDER:
        print(f'    {s:>14s}: {stage_count[s]}')
    n_damaged = sum(stage_count[s] for s in STAGE_ORDER if s != 'intact')
    print(f'  damaged: {n_damaged}  ({100*n_damaged/max(n_total,1):.1f}%)')

    if n_total == 0:
        print('No AM-AM contacts — exit.'); sys.exit(0)

    # z range — convert to physical µm
    zs = np.array([x['z'] for x in am_am])
    z_sim_min, z_sim_max = zs.min(), zs.max()
    # Sim → physical µm: assume meta scale; positions in sim m -> µm: × 1e6
    # but display we just use sim units relative position normalised by total
    z_phys_min = z_sim_min * 1e6 / scale
    z_phys_max = z_sim_max * 1e6 / scale
    z_phys = zs * 1e6 / scale
    thickness = z_phys_max - z_phys_min
    print(f'  z range: {z_phys_min:.1f} – {z_phys_max:.1f} µm '
          f'(thickness {thickness:.1f} µm)')

    bin_edges = np.linspace(z_phys_min, z_phys_max, args.bins + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Per-bin counts by stage + mean m (Auerbach ratio)
    counts = {s: np.zeros(args.bins, dtype=int) for s in STAGE_ORDER}
    ms_in_bin = [[] for _ in range(args.bins)]
    for x, z in zip(am_am, z_phys):
        b = min(args.bins - 1, max(0, np.digitize(z, bin_edges) - 1))
        counts[x['stage']][b] += 1
        ms_in_bin[b].append(x['m'])
    mean_m = np.array([np.mean(ms) if ms else 0 for ms in ms_in_bin])

    # ── Plot ─────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(17, 6.5))

    # Panel 1: stacked count histogram
    ax = axes[0]
    bottom = np.zeros(args.bins)
    for s in STAGE_ORDER:
        ax.barh(bin_centers, counts[s], left=bottom,
                height=(bin_edges[1] - bin_edges[0]) * 0.92,
                color=STAGE_COLOR[s], edgecolor='black', linewidth=0.3,
                label=f'{s} (n={int(counts[s].sum())})')
        bottom += counts[s]
    ax.set_xlabel('AM-AM contacts per z-bin', fontsize=11)
    ax.set_ylabel('z (µm)  — compaction axis', fontsize=11)
    ax.set_title('(a) Stacked count by Lawn fracture stage',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(alpha=0.3)
    # top plate at top
    ax.set_ylim(z_phys_min, z_phys_max)

    # Panel 2: stacked normalised fraction
    ax = axes[1]
    bin_total = np.zeros(args.bins)
    for s in STAGE_ORDER:
        bin_total += counts[s]
    bin_total_safe = np.where(bin_total > 0, bin_total, 1)
    left_acc = np.zeros(args.bins)
    for s in STAGE_ORDER:
        frac = counts[s] / bin_total_safe
        ax.barh(bin_centers, frac, left=left_acc,
                height=(bin_edges[1] - bin_edges[0]) * 0.92,
                color=STAGE_COLOR[s], edgecolor='black', linewidth=0.3,
                label=s)
        left_acc += frac
    ax.axvline(1.0, color='k', lw=0.8)
    ax.set_xlabel('Fraction of contacts in bin', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(b) Per-bin damage composition (fraction)',
                 fontsize=11, fontweight='bold')
    ax.set_xlim(0, 1.05)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc='lower right')
    ax.set_ylim(z_phys_min, z_phys_max)

    # Panel 3: mean Auerbach ratio F/P_c per z-bin
    ax = axes[2]
    ax.plot(mean_m, bin_centers, '-o', color='crimson', lw=2,
            markersize=6)
    ax.axvline(1, color='gray', ls='--', lw=1,
               label='m=1 (Auerbach onset)')
    ax.axvline(3, color='orange', ls=':', lw=1, label='m=3 (multicrack)')
    ax.axvline(11, color='red', ls=':', lw=1, label='m=11 (fragmentation)')
    ax.set_xlabel('Mean F/P_c per z-bin', fontsize=11)
    ax.set_ylabel('z (µm)', fontsize=11)
    ax.set_title('(c) Mean Auerbach ratio profile',
                 fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9, loc='lower right')
    ax.set_xscale('log')
    ax.set_ylim(z_phys_min, z_phys_max)

    case_name = case_dir.name
    plt.suptitle(
        f'Brittle-hotspot z-profile — {case_name}\n'
        f'AM-AM contacts: {n_total} (damaged {n_damaged}, '
        f'{100*n_damaged/n_total:.1f}%);  thickness {thickness:.1f} µm',
        fontsize=13, fontweight='bold', y=1.00,
    )
    plt.tight_layout()

    if args.out:
        out = Path(args.out)
    else:
        out = Path('docs/figures') / f'brittle_z_{case_name}.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f'\n✓ Saved: {out.resolve()}')


if __name__ == '__main__':
    main()
