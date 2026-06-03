#!/usr/bin/env python3
"""Verify Trevisanello sigma_AM_relative is firing per-particle in solver.

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


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: debug_trevisanello_check.py <case_name>")
    name = sys.argv[1]
    case = find_case(name)
    if case is None:
        sys.exit(f"case not found: {name}")
    print(f"Case: {case}")

    ip = json.load(open(case / 'input_params.json'))
    type_map = ip.get('type_map', {})
    scale = ip.get('scale', 1000)
    print(f"  type_map = {type_map}")
    print(f"  scale = {scale}")

    atoms_path = case / 'atoms.csv'
    if not atoms_path.exists():
        for p in case.iterdir():
            if p.suffix == '.csv' and 'atom' in p.name.lower():
                atoms_path = p; break
    df = pd.read_csv(atoms_path)
    print(f"  atoms.csv: {len(df)} rows, columns = {list(df.columns)}")

    if 'type' not in df.columns or 'radius' not in df.columns:
        sys.exit(f"  unexpected columns in atoms.csv")

    print(f"\nSIGMA_AM_ELECTRONIC = {SIGMA_AM_ELECTRONIC*1000:.1f} mS/cm (literature reference)")
    print()

    # Per particle-type breakdown
    for tid_str, label in type_map.items():
        tid = int(tid_str) if isinstance(tid_str, str) else tid_str
        sub = df[df['type'] == tid]
        if len(sub) == 0:
            continue
        r_real_um = sub['radius'].values * 1e6 / scale  # sim → μm real
        r_med = float(np.median(r_real_um))
        r_min = float(r_real_um.min())
        r_max = float(r_real_um.max())
        sig_rels = np.array([sigma_AM_relative(r, label) for r in r_real_um])
        sr_med = float(np.median(sig_rels))
        sigma_eff = sr_med * SIGMA_AM_ELECTRONIC * 1000  # mS/cm
        flag = "✓ Trevisanello applied" if sr_med < 0.99 else (
               "  no GB scaling (single-crystal)" if label == 'AM_S' else
               "⚠ NOT APPLIED — should be < 1.0 for AM_P")
        print(f"  type={tid} ({label}): n={len(sub)}, "
              f"r = {r_med:.2f} μm (range {r_min:.2f}–{r_max:.2f}), "
              f"σ_rel = {sr_med:.4f}, "
              f"σ_eff = {sigma_eff:.2f} mS/cm  {flag}")

    print()
    print("Expected for AM_P:")
    print("  r=2 μm  → σ_rel = 1/(1+(2/2)^1.5) = 0.500 → σ_eff = 25.0 mS/cm")
    print("  r=4 μm  → σ_rel = 1/(1+(4/2)^1.5) = 0.261 → σ_eff = 13.1 mS/cm")
    print("  r=6 μm  → σ_rel = 1/(1+(6/2)^1.5) = 0.161 → σ_eff =  8.1 mS/cm")
    print()
    print("Expected for AM_S: σ_rel = 1.0 → σ_eff = 50.0 mS/cm (no GB scaling)")


if __name__ == '__main__':
    main()
