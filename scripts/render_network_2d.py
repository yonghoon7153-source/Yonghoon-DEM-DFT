#!/usr/bin/env python3
"""2D cross-section network renderer — REAL data, physics-exact colors.

Reads LIGGGHTS atom + contact dumps, extracts a thin z-slab, and renders
the contact network as a 2D figure with:
  • particles colored by phase (SE yellow / AM gray), sized by radius
  • contact edges colored by ACTUAL type pair:
      SE-SE → yellow, AM-SE → blue, AM-AM → red
    (determined from the two endpoint particle types — never guessed)
  • optional SE-SE and AM-AM percolation backbones highlighted

No color is guessed: each edge's color comes from the real types of the
two particles it connects.

Usage:
  python3 scripts/render_network_2d.py <atom.liggghts> <contact.liggghts> \
      [--type-map 1:AM_P,2:AM_S,3:SE] [--zslab 0.4,0.6] [--out fig.png]
"""
import sys, argparse, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.collections import LineCollection


def load_atoms(path):
    """Return dict id -> (x,y,z,r,type)."""
    atoms = {}
    with open(path) as f:
        lines = f.readlines()
    # find ATOMS header
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith('ITEM: ATOMS'):
            cols = ln.split()[2:]
            start = i + 1
            break
    idx = {c: k for k, c in enumerate(cols)}
    for ln in lines[start:]:
        p = ln.split()
        if len(p) < len(cols): continue
        aid = int(float(p[idx['id']]))
        atoms[aid] = (
            float(p[idx['x']]), float(p[idx['y']]), float(p[idx['z']]),
            float(p[idx['radius']]), int(float(p[idx['type']])))
    return atoms


def load_contacts(paths):
    """Return list of (x1,y1,z1, x2,y2,z2) for each contact.
    Contact dump cols: c_cpl[1..3]=pos1, c_cpl[4..6]=pos2, ..."""
    edges = []
    for path in paths:
        with open(path) as f:
            started = False
            for ln in f:
                if ln.startswith('ITEM: ENTRIES'):
                    started = True; continue
                if ln.startswith('ITEM'):
                    started = False; continue
                p = ln.split()
                if len(p) < 6: continue
                try:
                    x1, y1, z1, x2, y2, z2 = (float(p[i]) for i in range(6))
                except: continue
                edges.append((x1, y1, z1, x2, y2, z2))
    return edges


def nearest_atom(pos, atoms_arr, ids):
    """Find atom id closest to pos (x,y,z)."""
    d = (atoms_arr[:, 0]-pos[0])**2 + (atoms_arr[:, 1]-pos[1])**2 + (atoms_arr[:, 2]-pos[2])**2
    return ids[np.argmin(d)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('atom')
    ap.add_argument('contact', nargs='+')
    ap.add_argument('--type-map', default='1:AM_P,2:AM_S,3:SE')
    ap.add_argument('--zslab', default='0.45,0.55',
                    help='fractional z-range of slab to render (thin slice)')
    ap.add_argument('--out', default='docs/figures/network_2d_real.png')
    ap.add_argument('--scale', type=float, default=1000.0)
    args = ap.parse_args()

    tmap = {}
    for pair in args.type_map.split(','):
        k, v = pair.split(':'); tmap[int(k)] = v.strip()
    se_types = {k for k, v in tmap.items() if v == 'SE'}

    atoms = load_atoms(args.atom)
    ids = np.array(list(atoms.keys()))
    arr = np.array([atoms[i][:3] for i in ids])   # x,y,z
    print(f"atoms: {len(atoms)}")

    zmin = arr[:, 2].min(); zmax = arr[:, 2].max()
    f0, f1 = (float(x) for x in args.zslab.split(','))
    zlo = zmin + (zmax-zmin)*f0; zhi = zmin + (zmax-zmin)*f1
    print(f"z-slab: [{zlo:.4f}, {zhi:.4f}]  (full {zmin:.4f}-{zmax:.4f})")

    # particles in slab
    in_slab = {i for i in atoms if zlo <= atoms[i][2] <= zhi}
    print(f"particles in slab: {len(in_slab)}")

    edges = load_contacts(args.contact)
    print(f"total contacts: {len(edges)}")

    # map each contact endpoint to nearest atom, keep if both in slab
    COL = {'SE-SE': '#f5c518', 'AM-SE': '#5b9bd5', 'AM-AM': '#e03030'}
    seg_by_type = {'SE-SE': [], 'AM-SE': [], 'AM-AM': []}
    for (x1, y1, z1, x2, y2, z2) in edges:
        # only keep contacts whose midpoint is in the slab
        zm = (z1+z2)/2
        if not (zlo <= zm <= zhi): continue
        a1 = nearest_atom((x1, y1, z1), arr, ids)
        a2 = nearest_atom((x2, y2, z2), arr, ids)
        t1 = atoms[a1][4]; t2 = atoms[a2][4]
        s1 = t1 in se_types; s2 = t2 in se_types
        if s1 and s2:      key = 'SE-SE'
        elif (not s1) and (not s2): key = 'AM-AM'
        else:              key = 'AM-SE'
        seg_by_type[key].append([(x1*args.scale, y1*args.scale),
                                  (x2*args.scale, y2*args.scale)])

    print(f"edges in slab: SE-SE={len(seg_by_type['SE-SE'])}, "
          f"AM-SE={len(seg_by_type['AM-SE'])}, AM-AM={len(seg_by_type['AM-AM'])}")

    # ── render ──
    fig, ax = plt.subplots(figsize=(9, 9))
    # edges first (thin), order: SE-SE, AM-SE, AM-AM (red on top)
    for key in ['SE-SE', 'AM-SE', 'AM-AM']:
        if not seg_by_type[key]: continue
        lc = LineCollection(seg_by_type[key], colors=COL[key],
                            linewidths=0.6, alpha=0.55, zorder=2)
        ax.add_collection(lc)
    # particles
    for i in in_slab:
        x, y, z, r, t = atoms[i]
        if t in se_types:
            fc, ec = '#f5c518', '#b8950f'
        else:
            fc, ec = '#808080', '#404040'
        ax.add_patch(Circle((x*args.scale, y*args.scale), r*args.scale,
                            fc=fc, ec=ec, lw=0.5, zorder=4))
    ax.set_xlim(0, 0.05*args.scale); ax.set_ylim(0, 0.05*args.scale)
    ax.set_aspect('equal'); ax.axis('off')

    # legend (separate, right)
    from matplotlib.lines import Line2D
    leg = [
        Line2D([0],[0], marker='o', color='w', markerfacecolor='#f5c518',
               markeredgecolor='#b8950f', markersize=10, label='SE (ionic)'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor='#808080',
               markeredgecolor='#404040', markersize=12, label='AM (electronic)'),
        Line2D([0],[0], color='#f5c518', lw=2, label='SE-SE contact'),
        Line2D([0],[0], color='#5b9bd5', lw=2, label='AM-SE contact'),
        Line2D([0],[0], color='#e03030', lw=2, label='AM-AM contact'),
    ]
    ax.legend(handles=leg, loc='center left', bbox_to_anchor=(1.02, 0.5),
              fontsize=10, frameon=True)

    plt.tight_layout()
    import os; os.makedirs('docs/figures', exist_ok=True)
    plt.savefig(args.out, dpi=200, bbox_inches='tight')
    print(f"saved: {args.out}")


if __name__ == '__main__':
    main()
