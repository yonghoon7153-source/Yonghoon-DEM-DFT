"""Deep diagnostic — load the network for an anomaly + clean case via the
real network_conductivity.build_network/solve_network functions, then dump:

  - Edge R_total distribution (min, percentiles, max, # of zero/inf)
  - V_source after solve
  - G_eff
  - Boundary conductance ratio (g_boundary × n_top vs effective bulk g)
  - Laplacian condition-number proxy (max/min diagonal)

This bypasses the CLI wrapper and gives raw solver state for both cases
side by side, so the σ-inflation root cause is visible.

Usage:
  python3 scripts/diag_network_internals.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import spsolve

ROOT     = Path(__file__).resolve().parent.parent
SCRIPTS  = ROOT / 'scripts'
WEBAPP   = ROOT / 'webapp'

sys.path.insert(0, str(SCRIPTS))
from network_conductivity import (  # noqa: E402
    load_atoms_raw, load_contacts_raw, build_network,
)

CASES = {
    'ANOMALY_115455': WEBAPP / 'results' / '260420_115455_8c26b6',
    'ANOMALY_213836': WEBAPP / 'results' / '260421_213836_aeccd4',
    'CLEAN_212704':   WEBAPP / 'results' / '260421_212704_8d08ed',
    'CLEAN_192638':   WEBAPP / 'results' / '260421_192638_5ebcec',
}


def diag_one(name: str, case_dir: Path) -> None:
    print(f'\n{"="*78}')
    print(f'  {name}   ({case_dir.name})')
    print('='*78)

    type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    target_types = [3]  # SE only — σ_ionic graph
    scale = 1000

    atoms_raw, _ = load_atoms_raw(case_dir / 'atoms.csv')
    contacts_raw, _ = load_contacts_raw(case_dir / 'contacts.csv')

    # plate_z from mesh_info if present
    mi = case_dir / 'mesh_info.json'
    if mi.exists():
        plate_z = json.load(open(mi)).get('plate_z',
                                            max(a['z'] for a in atoms_raw.values()))
    else:
        plate_z = max(a['z'] for a in atoms_raw.values())

    # box from input_params
    ip = case_dir / 'input_params.json'
    box_x, box_y = 0.05, 0.05
    if ip.exists():
        p = json.load(open(ip))
        box_x = p.get('box_x', 0.05)
        box_y = p.get('box_y', 0.05)

    print(f'  plate_z={plate_z:.5f}  box=({box_x}, {box_y})  scale={scale}')

    net = build_network(atoms_raw, contacts_raw, target_types, scale,
                          plate_z, box_x, box_y, contact_mode='hertzian')
    if net is None:
        print('  no network built (no SE atoms?)')
        return

    edges = net['edges']
    R = np.array([e['R_total'] for e in edges], dtype=float)
    n = len(edges)
    print(f'\n  Edges: n={n}')
    print(f'  R_total stats:')
    print(f'    min        : {R.min():.4e}')
    print(f'    1%ile      : {np.percentile(R, 1):.4e}')
    print(f'    median     : {np.percentile(R, 50):.4e}')
    print(f'    99%ile     : {np.percentile(R, 99):.4e}')
    print(f'    max        : {R.max():.4e}')
    print(f'    n with R==0   : {(R == 0).sum()}')
    print(f'    n with R<1e-9 : {(R < 1e-9).sum()}')

    g = np.where(R > 0, 1.0 / R, 0.0)
    print(f'  G stats (= 1/R):')
    print(f'    median g   : {np.median(g):.4e}')
    print(f'    max g      : {g.max():.4e}')
    print(f'    sum g      : {g.sum():.4e}')

    # Boundary stats
    bottom = net['bottom']
    top    = net['top']
    print(f'\n  Boundaries:')
    print(f'    n_bottom_total : {len(bottom)}')
    print(f'    n_top_total    : {len(top)}')

    g_boundary = 1e6  # hardcoded in network_conductivity.solve_network
    print(f'    g_boundary (hardcoded) : {g_boundary:.0e}')
    print(f'    total bottom g (n × g_boundary)   : '
          f'{len(bottom) * g_boundary:.2e}')
    print(f'    total top    g (n × g_boundary)   : '
          f'{len(top) * g_boundary:.2e}')
    print(f'    bulk total   g                    : {g.sum():.2e}')
    print(f'    boundary/bulk ratio (top side)    : '
          f'{len(top) * g_boundary / g.sum():.2e}')

    # Build Laplacian and solve manually so we can extract V_source
    nodes = net['nodes']
    id_to_idx = {nid: i for i, nid in enumerate(nodes)}
    source_idx = len(nodes)
    sink_idx   = len(nodes) + 1
    total = len(nodes) + 2

    rows, cols, vals = [], [], []
    diag = np.zeros(total)

    def add(i, j, gv):
        rows.append(i); cols.append(j); vals.append(-gv)
        rows.append(j); cols.append(i); vals.append(-gv)
        diag[i] += gv; diag[j] += gv

    for e in edges:
        if e['R_total'] > 0:
            add(id_to_idx[e['id1']], id_to_idx[e['id2']], 1.0 / e['R_total'])

    # Find percolating subgraph from boundaries
    L = sparse.csr_matrix((vals + list(diag),
                             (rows + list(range(total)),
                              cols + list(range(total)))),
                            shape=(total, total))
    # connectivity check: percolation = top reachable from bottom in bulk graph
    # (simplified — just use boundary intersection with all node ids)
    perc_bottom = bottom & set(nodes)
    perc_top    = top & set(nodes)
    print(f'    perc bottom (in nodes): {len(perc_bottom)}')
    print(f'    perc top    (in nodes): {len(perc_top)}')
    if not perc_bottom or not perc_top:
        print('    (no percolation — skipping solve)')
        return

    # Add boundary edges for solve
    for bid in perc_bottom:
        add(id_to_idx[bid], source_idx, g_boundary)
    for tid in perc_top:
        add(id_to_idx[tid], sink_idx, g_boundary)

    L_full = sparse.csr_matrix((vals + list(diag),
                                  (rows + list(range(total)),
                                   cols + list(range(total)))),
                                 shape=(total, total))

    # Pin sink to 0
    L_csr = L_full.tolil()
    L_csr[sink_idx, :] = 0
    L_csr[sink_idx, sink_idx] = 1.0
    L_csr = L_csr.tocsr()

    b = np.zeros(total)
    b[source_idx] = 1.0
    b[sink_idx]   = 0.0

    try:
        V = spsolve(L_csr, b)
    except Exception as ex:
        print(f'    solve failed: {ex}')
        return

    V_source = float(V[source_idx])
    G_eff = 1.0 / V_source if V_source > 0 else float('inf')

    # σ_ratio
    T_um = plate_z * scale
    A_um2 = box_x * box_y * scale ** 2
    sigma_ratio = G_eff * T_um / A_um2

    print(f'\n  Solve results (FULL Laplacian, hertzian mode):')
    print(f'    V_source     : {V_source:.4e}')
    print(f'    G_eff (1/V)  : {G_eff:.4e}')
    print(f'    T_um         : {T_um:.2f}')
    print(f'    A_um2        : {A_um2:.2f}')
    print(f'    σ_ratio      : {sigma_ratio:.4f}   '
          f'(Bruggeman-expected ≈ 0.72; > 10 means anomaly)')

    # Diagnostic: voltage distribution
    V_internal = V[:len(nodes)]
    print(f'    V internal range : {V_internal.min():.4e} ~ '
          f'{V_internal.max():.4e}')
    print(f'    n V near 0 (<1e-12) : '
          f'{(np.abs(V_internal) < 1e-12).sum()} / {len(nodes)}')


def main() -> None:
    for name, d in CASES.items():
        if not d.exists():
            print(f'\n  {name}: not found at {d}')
            continue
        try:
            diag_one(name, d)
        except Exception as e:
            print(f'\n  {name}: error {type(e).__name__}: {e}')


if __name__ == '__main__':
    main()
