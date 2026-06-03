#!/usr/bin/env python3
"""Verify Trevisanello sigma_AM_relative is firing per-particle in solver.

Reads type_map from meta.json (the wrapper's actual source).

Usage:
    python3 scripts/debug_trevisanello_check.py input_1mAh_5
"""
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from network_conductivity import sigma_AM_relative, SIGMA_AM_ELECTRONIC


def find_case(name):
    for base in ('webapp/archive', 'webapp/results'):
        for p in Path(base).rglob(name):
            if p.is_dir():
                return p
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
        sys.exit("usage: debug_trevisanello_check.py <case_name>")
    name = sys.argv[1]
    case = find_case(name)
    if case is None:
        sys.exit(f"case not found: {name}")
    print(f"Case: {case}")

    # Source of truth: meta.json (per wrapper run_one() line 549)
    type_map = {}
    meta_p = case / 'meta.json'
    ip_p   = case / 'input_params.json'
    if meta_p.exists():
        meta = json.load(open(meta_p))
        tm_str = meta.get('type_map')
        if tm_str:
            type_map = parse_type_map(tm_str)
            print(f"  type_map (meta.json) = {type_map}")
    if not type_map and ip_p.exists():
        ip = json.load(open(ip_p))
        tm = ip.get('type_map')
        if tm:
            type_map = parse_type_map(tm) if isinstance(tm, str) else tm
            print(f"  type_map (input_params.json) = {type_map}")
    if not type_map:
        sys.exit("  ERROR: no type_map found in meta.json or input_params.json")

    scale = float(json.load(open(meta_p)).get('scale', 1000))
    print(f"  scale = {scale}")

    atoms_path = case / 'atoms.csv'
    df = pd.read_csv(atoms_path)
    print(f"  atoms.csv: {len(df)} rows")

    print(f"\nSolver reference: SIGMA_AM_ELECTRONIC = {SIGMA_AM_ELECTRONIC*1000:.1f} mS/cm")
    print(f"Trevisanello formula: σ_rel = 1/(1+(r/2)^1.5)  ONLY for AM_P\n")

    for tid, label in sorted(type_map.items()):
        sub = df[df['type'] == tid]
        if len(sub) == 0:
            print(f"  type={tid} ({label}): n=0 (not in atoms.csv)")
            continue
        r_real_um = sub['radius'].values * 1e6 / scale  # sim → μm
        r_med = float(np.median(r_real_um))
        r_min = float(r_real_um.min())
        r_max = float(r_real_um.max())

        # Direct call to solver's function with proper label
        sig_rels = np.array([sigma_AM_relative(r, label) for r in r_real_um])
        sr_med = float(np.median(sig_rels))
        sigma_eff = sr_med * SIGMA_AM_ELECTRONIC * 1000  # mS/cm

        # Verdict
        if label == 'AM_P':
            flag = "✓ Trevisanello FIRING" if sr_med < 0.99 else "✗ BUG: not firing"
        elif label == 'AM_S':
            flag = "✓ single-crystal (no GB scaling)" if sr_med > 0.99 else "✗ BUG: applying to AM_S"
        else:
            flag = "(SE / other — irrelevant)"

        print(f"  type={tid} ({label}): n={len(sub):>5d}, "
              f"r_med={r_med:.3f}μm (range {r_min:.3f}–{r_max:.3f}), "
              f"σ_rel={sr_med:.4f}, σ_eff={sigma_eff:.2f} mS/cm  {flag}")

    print("\nExpected for AM_P:")
    for r_test in (2.0, 4.0, 5.0, 6.0):
        sr = 1.0 / (1.0 + (r_test / 2.0) ** 1.5)
        print(f"  r={r_test:.1f} μm  → σ_rel={sr:.4f} → σ_eff={sr*50:.2f} mS/cm")


if __name__ == '__main__':
    main()
