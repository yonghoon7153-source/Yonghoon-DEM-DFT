#!/usr/bin/env python3
"""Trace whether sigma_AM_relative is actually called inside build_network.

Loads a case, calls build_network for electronic mode, monkey-patches
sigma_AM_relative to count calls + record arg values, then reports.

Usage:
    python3 scripts/debug_solver_gate.py input_1mAh_5
"""
import sys, json, os
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
import network_conductivity as nc
from analyze_contacts import load_atoms_raw, load_contacts_raw


def find_case(name):
    for base in ('webapp/archive', 'webapp/results'):
        for p in Path(base).rglob(name):
            if p.is_dir(): return p
    return None


def parse_type_map(s):
    out = {}
    for pair in str(s).split(','):
        if ':' not in pair: continue
        k, v = pair.split(':')
        out[int(k.strip())] = v.strip()
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: debug_solver_gate.py <case_name>")
    name = sys.argv[1]
    case = find_case(name)
    if case is None: sys.exit(f"not found: {name}")
    print(f"Case: {case}\n")

    meta = json.load(open(case / 'meta.json'))
    type_map = parse_type_map(meta['type_map'])
    scale = float(meta.get('scale', 1000))
    am_types = [k for k, v in type_map.items() if 'AM' in v]
    se_types = [k for k, v in type_map.items() if v == 'SE']
    print(f"type_map = {type_map}")
    print(f"am_types = {am_types}, se_types = {se_types}\n")

    atoms_raw, _ = load_atoms_raw(case / 'atoms.csv')
    contacts_raw, _ = load_contacts_raw(case / 'contacts.csv')

    # mesh_info.json for plate_z
    mi = json.load(open(case / 'mesh_info.json')) if (case / 'mesh_info.json').exists() else {}
    plate_z = mi.get('plate_z', 0.15)
    box_x = box_y = 0.05  # standard RVE

    # Monkey-patch to count calls + record values
    orig_fn = nc.sigma_AM_relative
    call_log = []
    def wrapped(r_um, particle_type):
        v = orig_fn(r_um, particle_type)
        call_log.append((float(r_um), str(particle_type), float(v)))
        return v
    nc.sigma_AM_relative = wrapped

    print("Calling build_network with mode='electronic', target_types=am_types ...\n")
    try:
        net = nc.build_network(atoms_raw, contacts_raw, am_types, scale,
                                plate_z, box_x=box_x, box_y=box_y,
                                mode='electronic', type_map=type_map,
                                contact_mode='hertzian')
    except Exception as e:
        print(f"  build_network failed: {type(e).__name__}: {e}")
        return

    print(f"\n── sigma_AM_relative call summary ──")
    print(f"  Total calls: {len(call_log)}")
    if not call_log:
        print(f"  ✗✗✗ NEVER CALLED — gate condition NOT firing in build_network")
        print(f"      → check line 312-314 condition logic")
        return

    by_type = Counter((lbl, round(r, 3)) for r, lbl, _ in call_log)
    print(f"  Unique (label, radius_µm) seen:")
    for (lbl, r), n in sorted(by_type.items()):
        sigma_rel = [v for rr, ll, v in call_log if ll == lbl and round(rr, 3) == r][0]
        flag = "✓" if (lbl == 'AM_P' and sigma_rel < 1.0) or (lbl == 'AM_S' and sigma_rel == 1.0) else "?"
        print(f"    {lbl:>6s}  r={r:.3f}µm  σ_rel={sigma_rel:.4f}  ×{n}  {flag}")

    # Now repeat WITHOUT mode='electronic' (default 'ionic') to see if it still fires
    call_log.clear()
    print(f"\nCalling build_network WITHOUT mode (defaults to 'ionic'), target_types=am_types ...\n")
    try:
        nc.build_network(atoms_raw, contacts_raw, am_types, scale,
                          plate_z, box_x=box_x, box_y=box_y,
                          type_map=type_map, contact_mode='hertzian')
    except Exception as e:
        print(f"  build_network failed: {type(e).__name__}: {e}")
        return

    print(f"\n── (mode=default ionic) call count: {len(call_log)} ──")
    if call_log:
        print(f"  ✓ gate condition's target_types fallback works")
    else:
        print(f"  ✗ gate condition fails without explicit mode — production wrapper")
        print(f"    needs to pass mode='electronic' to run_decomposition.")


if __name__ == '__main__':
    main()
