#!/usr/bin/env python3
"""Diagnose Stage E σ_ionic discrepancy — why does median loss show ~43%
when expected behavior is unchanged for r_SE ≥ 0.5 cases?

Hypothesis: Stage E may be reading a different key than baseline (e.g.,
physics-corrected sigma_full_mScm via the network_conductivity dual mode),
OR the apply_corrections function may have an unintended side-effect on
SE-SE contacts even when f_SE_ionic = 1.0.

Output: per-case comparison of baseline σ_ionic vs Stage E σ_ionic with
the actual ratio per case, identifying the source of the 0.53 systematic.

Usage:
  python3 scripts/diag_stage_e_sigma_ionic.py            # all cases
  python3 scripts/diag_stage_e_sigma_ionic.py CID …      # specific cases
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT     = Path(__file__).resolve().parent.parent
WEBAPP   = ROOT / 'webapp'


def discover_case_dirs() -> list[Path]:
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for d in sorted(root.iterdir()):
            if d.is_dir() and (d / 'full_metrics.json').exists():
                out.append(d)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cases', nargs='*', help='Specific case_ids')
    args = ap.parse_args()

    cases = discover_case_dirs()
    if args.cases:
        wanted = set(args.cases)
        cases = [d for d in cases if d.name in wanted]

    print(f'{"case_id":33s} {"r_SE":>5s} {"σ_i_base":>10s} {"σ_i_phys":>10s} '
          f'{"σ_i_StageE":>11s} {"E/base":>8s} {"E/phys":>8s} {"loss%":>8s}')
    print('-' * 100)

    rows = []
    for d in cases:
        try:
            with open(d / 'full_metrics.json') as f:
                fm = json.load(f)
        except Exception:
            continue

        sigma_base = fm.get('sigma_full_mScm')
        # Try multiple physics key locations
        sigma_phys = (fm.get('sigma_full_mScm_physics')
                       or fm.get('sigma_full_mScm_phys')
                       or fm.get('sigma_phys_full_mScm'))
        # Fallback: read from auxiliary JSONs in case dir
        if sigma_phys is None:
            for aux_name in ('network_conductivity_physics.json',
                              'network_conductivity_dual.json'):
                aux_p = d / aux_name
                if not aux_p.exists():
                    continue
                try:
                    with open(aux_p) as af:
                        aux = json.load(af)
                    # dual.json has nested 'physics' subdict
                    if 'physics' in aux and isinstance(aux['physics'], dict):
                        sigma_phys = aux['physics'].get('sigma_full_mScm')
                    else:
                        sigma_phys = aux.get('sigma_full_mScm')
                    if sigma_phys is not None:
                        break
                except Exception:
                    pass
        sigma_e    = fm.get('sigma_full_mScm_stage_e')
        loss_pct   = fm.get('sigma_ionic_loss_pct_stage_e')

        # Detect r_SE from atoms.csv
        atoms_p = d / 'atoms.csv'
        r_SE = None
        if atoms_p.exists():
            try:
                df = pd.read_csv(atoms_p, usecols=['type', 'radius'])
                meta_p = d / 'meta.json'
                scale = 1000.0
                type_map_str = '1:AM_P,2:AM_S,3:SE'
                if meta_p.exists():
                    try:
                        meta = json.load(open(meta_p))
                        scale = float(meta.get('scale', 1000))
                        type_map_str = meta.get('type_map', type_map_str)
                    except Exception: pass
                # Find SE type id
                se_types = []
                for tok in type_map_str.split(','):
                    if ':' in tok:
                        k, v = tok.split(':', 1)
                        if 'SE' in v.strip():
                            try: se_types.append(int(k.strip()))
                            except Exception: pass
                if se_types:
                    sub = df[df['type'].isin(se_types)]
                    if not sub.empty:
                        r_SE = float(sub['radius'].median()) * 1.0e6 / scale
            except Exception: pass

        if sigma_base is None or sigma_e is None:
            continue
        e_over_base = sigma_e / sigma_base if sigma_base else None
        e_over_phys = sigma_e / sigma_phys if sigma_phys else None

        rows.append((d.name, r_SE, sigma_base, sigma_phys, sigma_e,
                     e_over_base, e_over_phys, loss_pct))

    # Sort by r_SE then case_id
    rows.sort(key=lambda r: (r[1] or 0, r[0]))
    for cid, r, sb, sp, se, eb, ep, loss in rows:
        r_str   = f'{r:.2f}' if r else '?'
        sb_str  = f'{sb:.4f}' if sb is not None else '?'
        sp_str  = f'{sp:.4f}' if sp is not None else '-'
        se_str  = f'{se:.4f}' if se is not None else '?'
        eb_str  = f'{eb:.3f}' if eb is not None else '?'
        ep_str  = f'{ep:.3f}' if ep is not None else '-'
        loss_str= f'{loss:.1f}%' if loss is not None else '?'
        print(f'{cid:33s} {r_str:>5s} {sb_str:>10s} {sp_str:>10s} '
              f'{se_str:>11s} {eb_str:>8s} {ep_str:>8s} {loss_str:>8s}')

    # Summary stats
    if not rows:
        print('No cases.'); return
    df = pd.DataFrame(rows, columns=['case_id', 'r_SE', 'base', 'phys', 'stage_e',
                                       'E/base', 'E/phys', 'loss_pct'])
    print('\n=== Stratified by r_SE ===')
    df['r_SE_band'] = pd.cut(df['r_SE'].fillna(0),
                              bins=[0, 0.3, 0.7, 1.2, 2.0],
                              labels=['<0.3', '0.3-0.7', '0.7-1.2', '>1.2'])
    g = df.groupby('r_SE_band', observed=True).agg(
        n=('case_id', 'count'),
        E_base_med=('E/base', 'median'),
        E_phys_med=('E/phys', 'median'),
        loss_med=('loss_pct', 'median')
    )
    print(g.round(3).to_string())

    print('\n=== Diagnosis ===')
    e_base_med = df['E/base'].median()
    e_phys_med = df['E/phys'].median()
    print(f'Median ratio Stage_E / baseline       : {e_base_med:.3f}')
    print(f'Median ratio Stage_E / physics-baseline: {e_phys_med:.3f}')
    if e_phys_med and 0.95 < e_phys_med < 1.05:
        print('\n→ Stage_E σ_ionic ≈ physics-baseline (NOT Hertzian-baseline).')
        print('  Cause: network_conductivity --contact-mode both produces both')
        print('  Hertzian and physics outputs; Stage E may be picking the wrong one,')
        print('  OR the Stage E baseline comparison should use physics value.')
        print('\n  Verdict: σ_ionic Stage E result is NOT a true correction —')
        print('  the σ_grain factor 1.0 was applied correctly, but the comparison')
        print('  is between physics-mode (Stage E) and Hertzian-mode (baseline).')
        print('  The ~43% "loss" is the Tabor+volume physics correction itself,')
        print('  NOT the σ_grain effect.')


if __name__ == '__main__':
    main()
