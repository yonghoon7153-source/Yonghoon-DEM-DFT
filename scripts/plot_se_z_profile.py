#!/usr/bin/env python3
"""Phase C — Per-case z-profile of SE network diagnostics.

Histogram of cut-node z, bottleneck-edge z, dead-end-cluster z across
the electrode thickness.  Shows WHERE the percolation fragility lives:
near plate, mid-bulk, or current-collector side.

Usage:
  python3 scripts/plot_se_z_profile.py <case_id>
  python3 scripts/plot_se_z_profile.py <case_id> --out my_profile.png
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path

ROOT   = Path(__file__).resolve().parent.parent
WEBAPP = ROOT / 'webapp'
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from viewer3d_data import compute_se_network_diagnostics
from extract_se_network_diagnostics import (
    load_case, load_contacts, estimate_plate_z, load_composition)

plt.rcParams.update({
    'font.family': 'DejaVu Serif',
    'font.size': 10,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def find_case_dir(case_id: str) -> Path:
    for base in ('results', 'archive'):
        d = WEBAPP / base / case_id
        if d.exists() and (d / 'atoms.csv').exists():
            return d
    raise FileNotFoundError(f'case_id {case_id} not found')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_id')
    ap.add_argument('--out', default=None)
    ap.add_argument('--n-bins', type=int, default=25)
    args = ap.parse_args()

    case_dir = find_case_dir(args.case_id)
    print(f'Loading {case_dir}')
    atoms, type_map, scale, meta = load_case(case_dir)
    contacts = load_contacts(case_dir)
    plate_z = estimate_plate_z(atoms)
    diag = compute_se_network_diagnostics(
        contacts, atoms, type_map, plate_z=plate_z, scale=scale)
    comp = load_composition(case_dir, meta)
    plate_z_um = plate_z * scale

    # Per-element z (real μm)
    perc       = set(diag.get('percolating_se') or [])
    art_pts    = set(diag.get('articulation_points') or [])
    bn_edges   = diag.get('bottleneck_edges') or []
    dead_ends  = diag.get('dead_end_clusters') or []

    z_perc = np.array([atoms[p]['z'] * scale for p in perc if p in atoms])
    z_cut  = np.array([atoms[p]['z'] * scale for p in art_pts if p in atoms])
    z_bn   = np.array([0.5 * (atoms[e['id1']]['z'] + atoms[e['id2']]['z']) * scale
                       for e in bn_edges
                       if e['id1'] in atoms and e['id2'] in atoms])
    z_dead_top = np.array([atoms[p]['z'] * scale
                           for d in dead_ends if d['type'] == 'top_only'
                           for p in d['ids'] if p in atoms])
    z_dead_bot = np.array([atoms[p]['z'] * scale
                           for d in dead_ends if d['type'] == 'bottom_only'
                           for p in d['ids'] if p in atoms])

    # ── Plot ──────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(14, 5),
                              gridspec_kw={'wspace': 0.32})
    bins = np.linspace(0, plate_z_um, args.n_bins + 1)
    bin_mid = 0.5 * (bins[:-1] + bins[1:])

    # (a) cut nodes + bottleneck edges z-histogram (counts)
    ax = axes[0]
    if z_perc.size:
        ax.hist(z_perc, bins=bins, color='#14b8a6', alpha=0.30,
                 label=f'Percolating SE ({z_perc.size})',
                 orientation='horizontal')
    if z_cut.size:
        ax.hist(z_cut, bins=bins, color='#facc15', alpha=0.85,
                 label=f'Cut nodes ({z_cut.size})',
                 orientation='horizontal')
    ax.set_ylabel('z (μm)  ↑ top'); ax.set_xlabel('count per z-bin')
    ax.set_title('(a)  Cut-node distribution',
                  loc='left', fontweight='bold')
    ax.invert_xaxis()   # so counts go left, z-axis vertical with top at top
    ax.legend(loc='lower left', fontsize=8)
    ax.set_ylim(0, plate_z_um)
    ax.grid(alpha=0.25)

    # Reverse the bars: actually flip back — invert_xaxis() flipped only x
    # Just leave as standard horizontal bars

    # (b) bn edges + dead-end z-profile
    ax = axes[1]
    if z_bn.size:
        ax.hist(z_bn, bins=bins, color='#dc2626', alpha=0.85,
                 label=f'Bottleneck edges ({z_bn.size})',
                 orientation='horizontal')
    if z_dead_top.size:
        ax.hist(z_dead_top, bins=bins, color='#ec4899', alpha=0.65,
                 label=f'Dead-end (top-only, {z_dead_top.size})',
                 orientation='horizontal')
    if z_dead_bot.size:
        ax.hist(z_dead_bot, bins=bins, color='#f97316', alpha=0.65,
                 label=f'Dead-end (bot-only, {z_dead_bot.size})',
                 orientation='horizontal')
    ax.set_ylabel('z (μm)  ↑ top'); ax.set_xlabel('count per z-bin')
    ax.set_title('(b)  Bottleneck + dead-end distribution',
                  loc='left', fontweight='bold')
    ax.invert_xaxis()
    ax.legend(loc='lower left', fontsize=8)
    ax.set_ylim(0, plate_z_um)
    ax.grid(alpha=0.25)

    # (c) Cut fraction profile: n_cut(z) / n_percolating(z)
    ax = axes[2]
    perc_hist, _ = np.histogram(z_perc, bins=bins)
    cut_hist, _  = np.histogram(z_cut, bins=bins)
    with np.errstate(divide='ignore', invalid='ignore'):
        cut_frac = np.where(perc_hist > 0, cut_hist / perc_hist, 0.0)
    ax.barh(bin_mid, cut_frac, height=(bins[1]-bins[0])*0.85,
            color='#7c3aed', alpha=0.85)
    ax.axvline(np.mean(cut_frac), color='black', ls='--', lw=1,
                label=f'mean = {np.mean(cut_frac):.3f}')
    ax.set_ylabel('z (μm)  ↑ top'); ax.set_xlabel('cut fraction per z-bin')
    ax.set_title('(c)  Local fragility profile  $n_{\\mathrm{cut}}/n_{\\mathrm{perc}}$',
                  loc='left', fontweight='bold')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_ylim(0, plate_z_um)
    ax.grid(alpha=0.25)

    # Header annotation
    head = (f'{args.case_id}   '
            f'AM:SE = {comp["am_wt"]:.0f}:{comp["se_wt"]:.0f},  '
            f'φ_SE = {comp["phi_SE"]:.3f},  '
            f'λ_eff = {comp["lam_eff"]:.2f},  '
            f'plate_z = {plate_z_um:.1f} μm')
    fig.suptitle(head, fontsize=11, fontweight='bold', y=0.99)

    out = args.out or str(ROOT / 'docs' / 'figures' /
                           f'se_z_profile_{args.case_id}.png')
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f'Figure → {out}')

    # Also write per-case z-profile CSV for downstream analysis
    csv_path = Path(out).with_suffix('.csv')
    with csv_path.open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['z_um_mid', 'n_perc', 'n_cut', 'cut_fraction',
                     'n_bn', 'n_dead_top', 'n_dead_bot'])
        bn_hist, _ = np.histogram(z_bn, bins=bins) if z_bn.size else (np.zeros(args.n_bins), None)
        dt_hist, _ = np.histogram(z_dead_top, bins=bins) if z_dead_top.size else (np.zeros(args.n_bins), None)
        db_hist, _ = np.histogram(z_dead_bot, bins=bins) if z_dead_bot.size else (np.zeros(args.n_bins), None)
        for i in range(args.n_bins):
            w.writerow([f'{bin_mid[i]:.2f}',
                         int(perc_hist[i]), int(cut_hist[i]),
                         f'{cut_frac[i]:.4f}',
                         int(bn_hist[i]), int(dt_hist[i]), int(db_hist[i])])
    print(f'CSV    → {csv_path}')


if __name__ == '__main__':
    main()
