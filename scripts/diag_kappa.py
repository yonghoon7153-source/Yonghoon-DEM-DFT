#!/usr/bin/env python3
"""Diagnose WHY a case's thermal conductivity κ comes out 0.

κ (thermal) uses the FULL contact network (AM-AM + AM-SE + SE-SE), so it is a
SUPERSET of the ionic (SE-SE) and electronic (AM-AM) networks.  If ionic OR
electronic percolates, thermal MUST percolate too — a κ=0 alongside a non-zero
σ_ionic/σ_e would be a real solver bug.  A κ=0 where ionic AND electronic are
ALSO 0 is a degenerate/broken sim (no contact bridges bottom→top), and the
honest display is "—", not a fabricated value.

This script answers that question directly: it loads the case's atoms/contacts,
reports the contact-data health, then builds + solves the THERMAL network and
prints the percolation diagnostic (n_edges, bottom, top, components reaching
each plate).  All inputs are auto-discovered from the case dir — no meta.json
in results/ required.

Run:
    python3 scripts/diag_kappa.py <case_dir> [-t 1:AM_P,2:AM_S,3:SE] [-s 1000]

  <case_dir> is the folder holding atoms.csv + contacts.csv (a webapp
  results/<TIMESTAMP-cid>/ dir, or any analysed case dir).  type_map / scale
  are auto-read from input_params.json or meta.json in the case dir when the
  flags are omitted; otherwise they fall back to the webapp defaults
  (1:AM_P,2:AM_S,3:SE  and  scale=1000).
"""
import argparse
import json
import os
import sys

import numpy as np

# Force the solver's internal diagnostics on so we see the EXACT reason a
# percolating network still yields σ=None (sigma_ratio>1.5 guard vs V_source≤0
# vs G/Σg ill-conditioning) — these prints are gated on NETWORK_DEBUG.
os.environ['NETWORK_DEBUG'] = '1'

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from analyze_contacts import load_atoms_raw, load_contacts_raw  # noqa: E402
import network_conductivity as nc  # noqa: E402


def _discover_type_map(case_dir, cli):
    """Resolve type_map string from CLI > input_params.json > meta.json > default."""
    if cli:
        return cli, 'cli'
    for fn in ('input_params.json', 'meta.json'):
        p = os.path.join(case_dir, fn)
        if os.path.exists(p):
            try:
                with open(p) as fh:
                    d = json.load(fh)
            except Exception:
                continue
            tm = d.get('type_map') or d.get('types')
            if tm:
                # accept either "1:AM_P,2:AM_S,3:SE" or {"1":"AM_P",...}
                if isinstance(tm, dict):
                    tm = ','.join(f'{k}:{v}' for k, v in tm.items())
                return tm, fn
    return '1:AM_P,2:AM_S,3:SE', 'default'


def _discover_scale(case_dir, cli):
    if cli:
        return int(cli), 'cli'
    for fn in ('input_params.json', 'meta.json'):
        p = os.path.join(case_dir, fn)
        if os.path.exists(p):
            try:
                with open(p) as fh:
                    d = json.load(fh)
            except Exception:
                continue
            if d.get('scale'):
                return int(d['scale']), fn
    return 1000, 'default'


def _discover_plate_z(case_dir, atoms_raw):
    mesh = os.path.join(case_dir, 'mesh_info.json')
    if os.path.exists(mesh):
        try:
            with open(mesh) as fh:
                return json.load(fh)['plate_z'], 'mesh_info.json'
        except Exception:
            pass
    return max(a['z'] for a in atoms_raw.values()), 'max(atom z)'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_dir')
    ap.add_argument('-t', '--type-map', default=None)
    ap.add_argument('-s', '--scale', default=None)
    ap.add_argument('--contact-mode', default='hertzian',
                    choices=['hertzian', 'physics'])
    a = ap.parse_args()

    cd = os.path.abspath(a.case_dir)
    atoms_csv = os.path.join(cd, 'atoms.csv')
    contacts_csv = os.path.join(cd, 'contacts.csv')
    for p in (atoms_csv, contacts_csv):
        if not os.path.exists(p):
            sys.exit(f"ERROR: missing {p}")

    tm_str, tm_src = _discover_type_map(cd, a.type_map)
    scale, sc_src = _discover_scale(cd, a.scale)
    type_map = {int(k): v.strip() for k, v in
                (pair.split(':') for pair in tm_str.split(','))}

    atoms_raw, _ = load_atoms_raw(atoms_csv)
    contacts_raw, _ = load_contacts_raw(contacts_csv)
    plate_z, pz_src = _discover_plate_z(cd, atoms_raw)

    box_x, box_y = 0.05, 0.05
    ip = os.path.join(cd, 'input_params.json')
    if os.path.exists(ip):
        try:
            with open(ip) as fh:
                d = json.load(fh)
            box_x = d.get('box_x', 0.05); box_y = d.get('box_y', 0.05)
        except Exception:
            pass

    print("=" * 64)
    print(f"κ DIAGNOSTIC  —  {cd}")
    print("=" * 64)
    print(f"  type_map = {tm_str}   (from {tm_src})")
    print(f"  scale    = {scale}    (from {sc_src})")
    print(f"  plate_z  = {plate_z:.6f}  (from {pz_src});  box={box_x}×{box_y}")
    print(f"  atoms    = {len(atoms_raw)}   contacts = {len(contacts_raw)}")

    # ── contact-data health ──────────────────────────────────────────
    ca = np.array([c.get('contact_area', 0) or 0 for c in contacts_raw], float)
    dl = np.array([c.get('delta', 0) or 0 for c in contacts_raw], float)
    n_ca = int((ca > 0).sum()); n_dl = int((dl > 0).sum())
    n_either = int(((ca > 0) | (dl > 0)).sum())
    print(f"  contacts with contact_area>0 : {n_ca}")
    print(f"  contacts with delta>0        : {n_dl}")
    print(f"  contacts usable (ca>0 OR δ>0): {n_either}  "
          f"← these become thermal edges")
    if n_either == 0:
        print("\n  ✗ ROOT CAUSE: NO usable contacts (all contact_area=0 AND")
        print("    delta=0).  The thermal network has zero edges → κ=0 is a")
        print("    BROKEN-SIM signature, not a solver bug.  Honest display = '—'.")
        return

    # atom-type histogram
    from collections import Counter
    hist = Counter(a['type'] for a in atoms_raw.values())
    print("  atom types: " + ", ".join(
        f"{type_map.get(t, '?')}({t})={n}" for t, n in sorted(hist.items())))

    # ── build + solve THERMAL network (all contacts) ─────────────────
    all_types = list(type_map.keys())
    print("\n--- THERMAL network (ALL contacts) ---")
    net = nc.build_network(atoms_raw, contacts_raw, all_types, scale,
                           plate_z, box_x, box_y, mode='thermal',
                           type_map=type_map, contact_mode=a.contact_mode)
    if net is None:
        print("  build_network returned None (no target ids / no edges).")
        return
    print(f"  nodes={len(net['nodes'])}  edges={len(net['edges'])}  "
          f"bottom={len(net['bottom'])}  top={len(net['top'])}")
    G, sig = nc.solve_network(net, mode='full')
    if sig is None:
        print("\n  ✗ THERMAL did NOT percolate (see DIAGNOSTIC above).")
        print("    If σ_ionic / σ_e are ALSO 0 here → degenerate sim, κ='—'.")
        print("    If either is >0 → real solver bug (thermal is their superset).")
    else:
        kappa_mScm = sig * nc.K_SE_THERMAL * 1000
        print(f"\n  ✓ THERMAL percolates:  σ/σ_bulk={sig:.6g}  →  "
              f"κ_full = {kappa_mScm:.4f} mS/cm-equiv")
        print("    (κ baseline is NON-zero — if the webapp shows 0.00 the bug")
        print("     is in how the pipeline stores/reads thermal_sigma_full_mScm,")
        print("     not in the solver.)")


if __name__ == '__main__':
    main()
