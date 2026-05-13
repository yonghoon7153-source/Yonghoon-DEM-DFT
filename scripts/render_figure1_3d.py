#!/usr/bin/env python3
"""Render Figure 1 panels (a), (b), (c) from a DEM case directory.

Panel (a) : DEM microstructure render — coloured by particle type
Panel (b) : Contact network — edges coloured by phase-pair
            (SE-SE blue, AM-SE green, AM-AM red)
Panel (c) : Resistor / Kirchhoff network preview — edges sized by
            inverse resistance (Holm-Sharvin estimate)

Usage:
    python3 scripts/render_figure1_3d.py <case_dir> [--out OUTDIR] \
        [--scale 1000] [--max-particles 5000] [--max-contacts 8000]

Inputs (in case_dir/):
    atoms.csv          — id, type, x, y, z, radius (sim units)
    contacts.csv       — id1, id2, contact_area, fn, delta
    meta.json          — type_map, scale
    input_params.json  — youngs_modulus_sim

Outputs (in --out, default docs/figures/):
    figure1_panel_a.png    figure1_panel_a.pdf
    figure1_panel_b.png    figure1_panel_b.pdf
    figure1_panel_c.png    figure1_panel_c.pdf

If case_dir is missing, the script falls back to a small synthetic
trimodal dataset so the layout/styling can be previewed without the
real DEM dumps.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection


TYPE_COLOR = {
    'AM_P': '#404040',   # dark gray
    'AM_S': '#7a7a7a',   # mid gray
    'SE':   '#e8c43c',   # yellow-ish (LPSCl)
    '?':    '#bbbbbb',
}

PAIR_COLOR = {
    'SE-SE':    ('#1f77b4', 0.55, 'SE-SE  (ionic)'),
    'AM_P-SE':  ('#2ca02c', 0.60, 'AM-SE  (mixed)'),
    'AM_S-SE':  ('#2ca02c', 0.60, None),  # share label with AM-SE
    'AM_P-AM_S':('#d62728', 0.70, 'AM-AM  (electronic)'),
    'AM_P-AM_P':('#d62728', 0.70, None),
    'AM_S-AM_S':('#d62728', 0.70, None),
    '?-?':      ('#aaaaaa', 0.30, None),
}


def fnum(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def load_case(case_dir: Path, scale: float | None = None):
    """Read atoms / contacts / meta from a webapp/archive-style case dir."""
    meta = {}
    if (case_dir / 'meta.json').exists():
        meta = json.loads((case_dir / 'meta.json').read_text())
    type_map = {}
    raw_tm = str(meta.get('type_map', ''))
    for tok in raw_tm.split(','):
        tok = tok.strip()
        if ':' in tok:
            k, v = tok.split(':', 1)
            type_map[int(k.strip())] = v.strip()
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    if scale is None:
        scale = float(meta.get('scale', 1000.0))

    atoms = {}
    apath = case_dir / 'atoms.csv'
    if apath.exists():
        for r in csv.DictReader(apath.open()):
            aid = int(r['id'])
            atoms[aid] = dict(
                id=aid,
                type=type_map.get(int(r.get('type', 0)), '?'),
                x=fnum(r.get('x')), y=fnum(r.get('y')), z=fnum(r.get('z')),
                r=fnum(r.get('radius') or r.get('r')),
            )
    contacts = []
    cpath = case_dir / 'contacts.csv'
    if cpath.exists():
        for r in csv.DictReader(cpath.open()):
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
                id1=i1, id2=i2,
                area=fnum(r.get('contact_area')),
                delta=fnum(r.get('delta')),
                fn=fn,
            ))
    return atoms, contacts, type_map, scale


def synth_case(n_amp=8, n_ams=80, n_se=600, box=30.0, seed=1):
    """Tiny synthetic trimodal cathode for layout/styling preview."""
    rng = np.random.default_rng(seed)
    atoms = {}
    nxt = 1

    def add(n, t, R, jitter=0):
        nonlocal nxt
        for _ in range(n):
            x = float(rng.uniform(R, box - R))
            y = float(rng.uniform(R, box - R))
            z = float(rng.uniform(R, box - R))
            atoms[nxt] = dict(id=nxt, type=t,
                              x=x, y=y, z=z,
                              r=R + jitter * (rng.random() - 0.5))
            nxt += 1

    add(n_amp, 'AM_P', 3.0)   # D=6
    add(n_ams, 'AM_S', 1.2)
    add(n_se,  'SE',   0.5)

    # Build contacts as nearest neighbours within R_i + R_j + tol
    ids = list(atoms.keys())
    contacts = []
    for i_idx in range(len(ids)):
        a = atoms[ids[i_idx]]
        for j_idx in range(i_idx + 1, len(ids)):
            b = atoms[ids[j_idx]]
            d = math.dist((a['x'], a['y'], a['z']), (b['x'], b['y'], b['z']))
            r_sum = a['r'] + b['r']
            if d < r_sum + 0.05:
                delta = max(0.0, r_sum - d)
                area = math.pi * delta * min(a['r'], b['r']) if delta > 0 else 0.01
                fn = 1e2 * delta + 1.0
                contacts.append(dict(id1=a['id'], id2=b['id'],
                                     area=area, delta=delta, fn=fn))
    type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    return atoms, contacts, type_map, 1.0


def setup_ax_3d(ax, box_lo, box_hi, title):
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(box_lo[0], box_hi[0])
    ax.set_ylim(box_lo[1], box_hi[1])
    ax.set_zlim(box_lo[2], box_hi[2])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z',
                                                          labelpad=-2)
    ax.set_title(title, fontsize=12, fontweight='bold')


def sample(items, n_max, key=None, rng=None):
    """Keep at most n_max items.  If key given, retain top-n by key first."""
    if len(items) <= n_max:
        return items
    if key is not None:
        return sorted(items, key=key, reverse=True)[:n_max]
    rng = rng or np.random.default_rng(0)
    idx = rng.choice(len(items), size=n_max, replace=False)
    return [items[i] for i in idx]


def panel_a(atoms, box_lo, box_hi, out, max_particles=5000):
    """DEM microstructure 3D scatter, colored by type."""
    atoms_list = list(atoms.values())
    atoms_list = sample(atoms_list, max_particles,
                        key=lambda a: a['r'])  # keep largest first
    by_type = {}
    for a in atoms_list:
        by_type.setdefault(a['type'], []).append(a)

    fig = plt.figure(figsize=(7, 6.5))
    ax = fig.add_subplot(111, projection='3d')
    for t, lst in by_type.items():
        xs = [a['x'] for a in lst]; ys = [a['y'] for a in lst]
        zs = [a['z'] for a in lst]; rs = [a['r'] for a in lst]
        sizes = [max(3, (r * 14) ** 2) for r in rs]
        ax.scatter(xs, ys, zs, s=sizes, c=TYPE_COLOR.get(t, '#bbbbbb'),
                   edgecolors='black', linewidth=0.2,
                   alpha=0.85, label=f'{t}  (n={len(lst)})')
    setup_ax_3d(ax, box_lo, box_hi,
                '(a)  DEM microstructure (trimodal AM + SE)')
    ax.legend(fontsize=9, loc='upper left', framealpha=0.95)
    plt.tight_layout()
    plt.savefig(out.with_suffix('.png'), dpi=180, bbox_inches='tight')
    plt.savefig(out.with_suffix('.pdf'),         bbox_inches='tight')
    plt.close(fig)
    print(f'  ✓ {out.with_suffix(".png").name}  ({len(atoms_list)} particles)')


def pair_key(t1, t2):
    return '-'.join(sorted([t1, t2]))


def collapse_pair(pk):
    """Map specific pairs to display label key."""
    if pk.startswith('AM_') and pk.endswith('-SE'):
        return 'AM_P-SE'   # unify AM-SE color
    if pk.startswith('AM_') and 'AM_' in pk[3:]:
        return 'AM_P-AM_S'
    if pk == 'SE-SE':
        return 'SE-SE'
    return '?-?'


def panel_b(atoms, contacts, box_lo, box_hi, out, max_contacts=8000):
    """Contact network — edges colored by phase pair."""
    # Keep top-n by area (most rate-limiting contacts)
    contacts_top = sample(contacts, max_contacts,
                          key=lambda c: c.get('area', 0))
    segs_by_pair = {}
    for c in contacts_top:
        a = atoms[c['id1']]; b = atoms[c['id2']]
        pk = pair_key(a['type'], b['type'])
        cls = collapse_pair(pk)
        segs_by_pair.setdefault(cls, []).append(
            [(a['x'], a['y'], a['z']), (b['x'], b['y'], b['z'])])

    fig = plt.figure(figsize=(7, 6.5))
    ax = fig.add_subplot(111, projection='3d')

    # Faded particle dots for context
    atoms_list = sample(list(atoms.values()), 1500,
                        key=lambda a: a['r'])
    ax.scatter([a['x'] for a in atoms_list],
               [a['y'] for a in atoms_list],
               [a['z'] for a in atoms_list],
               s=4, c='lightgray', alpha=0.4, zorder=1)

    legend_done = set()
    for cls, segs in segs_by_pair.items():
        color, alpha, label = PAIR_COLOR.get(cls, ('#aaaaaa', 0.3, None))
        lc = Line3DCollection(segs, colors=color, alpha=alpha,
                              linewidths=0.8)
        ax.add_collection3d(lc)
        if label and label not in legend_done:
            ax.plot([], [], [], color=color, alpha=alpha,
                    linewidth=2.5, label=f'{label} (n={len(segs)})')
            legend_done.add(label)

    setup_ax_3d(ax, box_lo, box_hi,
                '(b)  Contact network coloured by phase pair')
    ax.legend(fontsize=9, loc='upper left', framealpha=0.95)
    plt.tight_layout()
    plt.savefig(out.with_suffix('.png'), dpi=180, bbox_inches='tight')
    plt.savefig(out.with_suffix('.pdf'),         bbox_inches='tight')
    plt.close(fig)
    n_total = sum(len(s) for s in segs_by_pair.values())
    print(f'  ✓ {out.with_suffix(".png").name}  ({n_total} edges)')


def panel_c(atoms, contacts, box_lo, box_hi, out, max_contacts=4000):
    """Kirchhoff network preview — edges thicker where 1/R larger."""
    # Use contact area as proxy for 1/R (R = R_bulk + R_constriction ≈ 1/(2·σ·a))
    if not contacts:
        return
    contacts_top = sample(contacts, max_contacts,
                          key=lambda c: c.get('area', 0))
    areas = np.array([c.get('area', 0.0) for c in contacts_top])
    a_max = max(areas.max(), 1e-9)

    fig = plt.figure(figsize=(7, 6.5))
    ax = fig.add_subplot(111, projection='3d')

    atoms_list = sample(list(atoms.values()), 1200,
                        key=lambda a: a['r'])
    ax.scatter([a['x'] for a in atoms_list],
               [a['y'] for a in atoms_list],
               [a['z'] for a in atoms_list],
               s=6, c='lightgray', alpha=0.35, zorder=1)

    # Edge thickness ∝ contact area; color by conductance bin (cool→hot)
    segs = []
    widths = []
    norm_areas = []
    for c in contacts_top:
        a = atoms[c['id1']]; b = atoms[c['id2']]
        segs.append([(a['x'], a['y'], a['z']), (b['x'], b['y'], b['z'])])
        w = 0.3 + 2.5 * (c.get('area', 0.0) / a_max) ** 0.4
        widths.append(w)
        norm_areas.append(c.get('area', 0.0) / a_max)
    norm_arr = np.asarray(norm_areas)
    cmap = matplotlib.colormaps.get_cmap('plasma')
    colors = cmap(norm_arr)
    lc = Line3DCollection(segs, colors=colors, linewidths=widths, alpha=0.85)
    ax.add_collection3d(lc)

    setup_ax_3d(ax, box_lo, box_hi,
                '(c)  Equivalent Kirchhoff resistor network\n'
                '(edge thickness ∝ 1/R; colour: low → high conductance)')
    plt.tight_layout()
    plt.savefig(out.with_suffix('.png'), dpi=180, bbox_inches='tight')
    plt.savefig(out.with_suffix('.pdf'),         bbox_inches='tight')
    plt.close(fig)
    print(f'  ✓ {out.with_suffix(".png").name}  ({len(segs)} edges)')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('case_dir', nargs='?', default=None,
                   help='DEM case directory (containing atoms.csv, contacts.csv, meta.json)')
    p.add_argument('--out', default='docs/figures',
                   help='output directory for figure1_panel_*.{png,pdf}')
    p.add_argument('--scale', type=float, default=None)
    p.add_argument('--max-particles', type=int, default=5000)
    p.add_argument('--max-contacts',  type=int, default=8000)
    p.add_argument('--synthetic', action='store_true',
                   help='force synthetic preview instead of reading case_dir')
    args = p.parse_args()

    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)
    print(f'Output directory: {out_dir.resolve()}')

    if args.synthetic or args.case_dir is None:
        print('Using synthetic trimodal preview (no case_dir given).')
        atoms, contacts, type_map, scale = synth_case()
    else:
        cd = Path(args.case_dir)
        if not cd.exists():
            print(f'⚠️  case_dir not found: {cd}')
            print('   Falling back to synthetic preview.')
            atoms, contacts, type_map, scale = synth_case()
        else:
            print(f'Loading {cd}')
            atoms, contacts, type_map, scale = load_case(cd, args.scale)
            if not atoms:
                print('   atoms.csv empty/missing — falling back to synthetic.')
                atoms, contacts, type_map, scale = synth_case()

    print(f'  atoms: {len(atoms)},  contacts: {len(contacts)},  '
          f'types: {set(a["type"] for a in atoms.values())}')

    xs = [a['x'] for a in atoms.values()]
    ys = [a['y'] for a in atoms.values()]
    zs = [a['z'] for a in atoms.values()]
    pad = 1.5
    box_lo = (min(xs) - pad, min(ys) - pad, min(zs) - pad)
    box_hi = (max(xs) + pad, max(ys) + pad, max(zs) + pad)

    panel_a(atoms, box_lo, box_hi,
            out_dir / 'figure1_panel_a',
            max_particles=args.max_particles)
    panel_b(atoms, contacts, box_lo, box_hi,
            out_dir / 'figure1_panel_b',
            max_contacts=args.max_contacts)
    panel_c(atoms, contacts, box_lo, box_hi,
            out_dir / 'figure1_panel_c',
            max_contacts=args.max_contacts // 2)

    print('\nAll three panels saved.  Use them in figure1.tex composite '
          'or include directly in main.tex.')


if __name__ == '__main__':
    main()
