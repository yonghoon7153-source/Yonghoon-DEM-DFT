#!/usr/bin/env python3
"""Prototype: add film-tube resistance to Maxwell spreading.

Tests Holm-Timsit extension:
    R_contact = R_Maxwell + R_film
              = 1/(2a)   + 2δ/A
    R_total_edge = R_bulk + R_contact

R_film saturates R_contact as A grows (Maxwell alone goes to 0, which
is unphysical for surface-contact Physics mode).

Runs on 5 representative cases, compares old (Maxwell-only) vs new
(Maxwell + film) σ_eff without touching the real solver. The key
questions:
  1. How much does σ_phys change? (if <5%, fit unaffected; if 10-30%,
     new calibration needed.)
  2. Does film contribution grow with cap saturation? (sanity)
  3. Is the change mode-asymmetric? (should be — Hertzian small A
     should change less than Physics large A.)
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))


def compute_edge_resistance(d_ij, r1, r2, A_contact, delta_real,
                             holm_correction=False):
    """Return (R_bulk, R_Maxwell, R_film, R_total).
    holm_correction: if True, use Maxwell + film; else Maxwell only.
    Units: R normalised with ρ = 1 (the solver's convention).
    """
    R_bulk_1 = (d_ij / 2) / (np.pi * r1**2) if r1 > 0 else 0
    R_bulk_2 = (d_ij / 2) / (np.pi * r2**2) if r2 > 0 else 0
    R_bulk = R_bulk_1 + R_bulk_2

    a = np.sqrt(A_contact / np.pi) if A_contact > 0 else 0.0
    R_Maxwell = 1.0 / (2 * a) if a > 0 else 1e12

    R_film = 0.0
    if holm_correction and delta_real > 0 and A_contact > 0:
        R_film = 2 * delta_real / A_contact

    R_contact = R_Maxwell + R_film
    return R_bulk, R_Maxwell, R_film, R_bulk + R_contact


def _load_edges_for_case(case_id, scale=1000.0, contact_mode='physics'):
    """Reproduce solver's edge construction for a specific case."""
    from plastic_coverage import film_area_from_overlap
    import csv

    case_dir = None
    for base in ('results', 'archive'):
        for p in Path(f'webapp/{base}').rglob(f'{case_id}/atoms.csv'):
            case_dir = p.parent
            break
        if case_dir: break
    if case_dir is None:
        return None

    # Load atoms
    atoms = {}
    with open(case_dir / 'atoms.csv') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            aid = int(row['id'])
            atoms[aid] = {'x': float(row['x']), 'y': float(row['y']),
                          'z': float(row['z']), 'radius': float(row['radius']),
                          'type': int(row['type'])}

    # Load contacts.csv
    edges = []
    cont_path = case_dir / 'contacts.csv'
    with open(cont_path) as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            i1, i2 = int(row['id1']), int(row['id2'])
            if i1 not in atoms or i2 not in atoms: continue
            a1, a2 = atoms[i1], atoms[i2]
            # box periodicity — assume non-PBC for simplicity of sanity check
            dx = a1['x'] - a2['x']; dy = a1['y'] - a2['y']; dz = a1['z'] - a2['z']
            d_ij_sim = np.sqrt(dx**2 + dy**2 + dz**2)
            d_ij = d_ij_sim * scale  # μm
            r1 = a1['radius'] * scale
            r2 = a2['radius'] * scale
            delta_sim = float(row.get('delta', 0) or 0)
            delta_real = delta_sim * scale  # μm
            ca_sim = float(row.get('contact_area', 0) or 0)
            A_hertz = ca_sim * scale**2

            if contact_mode == 'physics' and delta_sim > 0:
                R_star_sim = (a1['radius']*a2['radius']) / (a1['radius']+a2['radius'])
                R_min_sim = min(a1['radius'], a2['radius'])
                try:
                    A_p_sim, regime = film_area_from_overlap(
                        delta_sim, R_star_sim,
                        R_min=R_min_sim, ligg_area=ca_sim, mode='physics')
                    A_contact = A_p_sim * scale**2
                except Exception:
                    A_contact = A_hertz
                    regime = 'fallback'
            else:
                A_contact = A_hertz
                regime = 'hertzian'

            edges.append({
                'i1': i1, 'i2': i2, 'd_ij': d_ij, 'r1': r1, 'r2': r2,
                'A_contact': A_contact, 'A_hertz': A_hertz,
                'delta_real': delta_real, 'regime': regime,
            })
    return edges


def analyse_case(case_id, mode='physics', verbose=True):
    edges = _load_edges_for_case(case_id, contact_mode=mode)
    if not edges:
        print(f'  [{case_id}] no edges found'); return None

    stats = {'n': len(edges)}
    R_tot_old, R_tot_new = [], []
    R_max_list, R_film_list, A_list = [], [], []
    film_over_maxwell = []

    for e in edges:
        R_b, R_max, R_film, R_tot_new_e = compute_edge_resistance(
            e['d_ij'], e['r1'], e['r2'], e['A_contact'], e['delta_real'],
            holm_correction=True)
        _, _, _, R_tot_old_e = compute_edge_resistance(
            e['d_ij'], e['r1'], e['r2'], e['A_contact'], e['delta_real'],
            holm_correction=False)
        R_tot_old.append(R_tot_old_e)
        R_tot_new.append(R_tot_new_e)
        R_max_list.append(R_max); R_film_list.append(R_film)
        A_list.append(e['A_contact'])
        if R_max > 0: film_over_maxwell.append(R_film / R_max)

    R_old = np.array(R_tot_old); R_new = np.array(R_tot_new)
    ratio = R_new / np.maximum(R_old, 1e-12)
    A_arr = np.array(A_list)

    if verbose:
        print(f'\n=== {case_id}  ({mode} mode, n_edges={len(edges)}) ===')
        print(f'  A_contact (μm²):  median={np.median(A_arr):.3f}  '
              f'max={A_arr.max():.3f}  min={A_arr.min():.4f}')
        print(f'  R_Maxwell:         median={np.median(R_max_list):.4f}')
        print(f'  R_film:            median={np.median(R_film_list):.4f}')
        print(f'  R_film/R_Maxwell:  median={np.median(film_over_maxwell):.2%}  '
              f'max={max(film_over_maxwell):.2%}  '
              f'fraction>50%={(np.array(film_over_maxwell)>0.5).mean()*100:.0f}%')
        print(f'  R_total ratio (new/old):  median={np.median(ratio):.3f}  '
              f'max={ratio.max():.3f}')
        # Top 5 edges where film correction matters most
        top_idx = np.argsort(-np.array(film_over_maxwell))[:5]
        print(f'  Top-5 edges most film-dominated:')
        print(f'    {"A_μm²":>8} {"δ_μm":>7} {"R_max":>8} {"R_film":>8} {"film%":>7}')
        for i in top_idx:
            e = edges[i]
            print(f'    {e["A_contact"]:8.3f} {e["delta_real"]:7.3f} '
                  f'{R_max_list[i]:8.4f} {R_film_list[i]:8.4f} '
                  f'{film_over_maxwell[i]*100:6.1f}%')

    return {'case_id': case_id, 'n': len(edges),
            'R_ratio_median': float(np.median(ratio)),
            'R_ratio_max': float(ratio.max()),
            'film_dom_frac': float((np.array(film_over_maxwell)>0.5).mean()),
            'film_over_max_median': float(np.median(film_over_maxwell))}


def main():
    # 5 representative cases across regimes
    test_cases = [
        'input_thin_6_S1',      # 1mAh thin film, Physics cap active
        'input_particulate_1',  # thick, low porosity, high σ
        'input_8mAh_real40_7',  # 1.5 μm SE, large A contacts
        'input_6mAh_real_5',    # AM_P only, high porosity
        'input_1mAh_8',         # 1mAh thin, low σ
    ]
    print('=' * 70)
    print('Prototype: Maxwell + Film resistance (Holm-Timsit extension)')
    print('Testing on 5 representative cases, PHYSICS mode only')
    print('=' * 70)

    results = []
    for cid in test_cases:
        r = analyse_case(cid, mode='physics', verbose=True)
        if r: results.append(r)

    print('\n' + '=' * 70)
    print('=== SUMMARY (Physics mode) ===')
    print(f'{"case":25s}  {"n_edges":>8s}  {"R_ratio_med":>12s}  '
          f'{"R_ratio_max":>12s}  {"film>50%":>10s}')
    for r in results:
        print(f'{r["case_id"][:25]:25s}  {r["n"]:>8d}  '
              f'{r["R_ratio_median"]:>12.3f}  {r["R_ratio_max"]:>12.3f}  '
              f'{r["film_dom_frac"]*100:>9.1f}%')

    # Interpretation hint
    med = np.median([r['R_ratio_median'] for r in results])
    print(f'\nMedian edge R increases by {(med-1)*100:+.1f}% when adding film term.')
    if med > 1.05:
        print(f'→ σ_phys will DECREASE by ~{(1-1/med)*100:.1f}% on average.')
        print('→ Full solver re-run justified. Scaling law will need refit.')
    elif med > 1.02:
        print('→ Modest σ_phys shift. Fit may or may not change meaningfully.')
    else:
        print('→ Film correction negligible for this dataset.')


if __name__ == '__main__':
    main()
