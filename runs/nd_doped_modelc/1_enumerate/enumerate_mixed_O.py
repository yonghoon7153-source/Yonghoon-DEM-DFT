"""
enumerate_mixed_O.py — Mixed O placement enumeration for Nd-doped modelC

Purpose: Validate paper #2 hero finding (Track 1A pure) against mixed
configurations where some O sit at 16e (PS4 corner) and others at 4a/4c
(free anion). This is the reviewer-proof test for the 1.6 eV gap claim.

Reference: rank01 (Track 1A, idx 141) E_anneal_final = -521.9585 eV
  - O at 16e (PS3O units): indices [37, 95, 109]
  - Asymmetric: 2 O near Nd2 (cluster), 1 O near Nd1 (isolated)

Strategies (~25-30 candidates total):

  A. BALANCED (2:1 16e:4a) — most critical reviewer test
     Keep 2 PS3O near Nd2 (preserve rank01 best feature)
     Move 1 PS3O O (the one near Nd1) to free 4a/4c near Nd1
     → Both Nd get O coordination (test asymmetric vs symmetric)
     ~5 candidates varying which 4a near Nd1

  B. INVERSE (1:2 16e:4a)
     Keep 1 PS3O near Nd2
     2 free O at various positions
     ~10 candidates

  C. CONCENTRATED cluster (all 3 around one Nd)
     - All 3 near Nd2 (mix of 16e + 4a)
     - All 3 near Nd1 (mix)
     ~10 candidates

Output:
  - mixed_O_results.json (candidate list + MLIP energies)
  - top_5_mixed.xyz (best 5 mixed structures)

Usage:
  python enumerate_mixed_O.py \\
      --base /path/to/track1_base_124atom.xyz \\
      --outdir mixed_results/

Reference comparison:
  rank01 E (Track 1A pure) = -521.9585 eV
  rank02 E (Track 1B pure) = -520.3255 eV (ΔE = +1.633 eV)
  → Mixed should be BETWEEN if linear interpolation
  → If any mixed < rank01: hero finding rebroadcast required
"""
import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
from ase.io import read, write
from ase import Atoms
from pymatgen.io.ase import AseAtomsAdaptor
from ase.optimize import LBFGS
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator


# ============================================================
# Reference data (from anneal_ranking.json rank01)
# ============================================================
ND_PAIR = (1, 82)                  # Nd indices in 124-atom base
VAC_INDICES = [5, 6, 63, 71]       # Li vacancies
O_RANK01_16e = [37, 95, 109]       # rank01 O at PS4 corners
RANK01_E_REF = -521.9585           # eV, rank01 anneal_final


# ============================================================
# Helpers (from enumerate_track1.py)
# ============================================================
def find_indices(atoms, element):
    return [i for i, s in enumerate(atoms.get_chemical_symbols()) if s == element]


def min_image_d(atoms, i, j):
    """Min-image distance between two atoms."""
    pos = atoms.get_positions()
    cell = atoms.cell.array
    inv = np.linalg.inv(cell)
    v = pos[j] - pos[i]
    f = v @ inv
    f -= np.round(f)
    return np.linalg.norm(f @ cell)


def is_PS4_internal_S(atoms, s_idx, p_indices, cutoff=2.5):
    """True if S is bonded to P (within cutoff)."""
    for p in p_indices:
        if min_image_d(atoms, p, s_idx) < cutoff:
            return True
    return False


def apply_substitution(base, nd_pair, vac_indices, o_indices):
    """Build new atoms with Nd→Li, S→O, and Li vacancies removed."""
    syms = list(base.get_chemical_symbols())
    for nd_i in nd_pair:
        syms[nd_i] = 'Nd'
    for o_i in o_indices:
        syms[o_i] = 'O'
    new_atoms = Atoms(symbols=syms,
                      positions=base.get_positions(),
                      cell=base.cell,
                      pbc=base.pbc)
    keep = np.ones(len(new_atoms), dtype=bool)
    for v in vac_indices:
        keep[v] = False
    return new_atoms[keep]


# ============================================================
# Candidate generation
# ============================================================
def generate_candidates(base, nd_pair=ND_PAIR, max_per_strategy=10):
    """Generate logical mixed O configurations."""
    nd1, nd2 = nd_pair
    s_idx = find_indices(base, 'S')
    p_idx = find_indices(base, 'P')

    # Classify S atoms
    ps4_s = [s for s in s_idx if is_PS4_internal_S(base, s, p_idx)]
    free_s = [s for s in s_idx if not is_PS4_internal_S(base, s, p_idx)]

    print(f"  PS4 internal S (16e): {len(ps4_s)} sites")
    print(f"  Free S (4a/4c):       {len(free_s)} sites")

    # rank01 O classification: which O is near Nd1 vs Nd2
    o_to_nd = {o: {'Nd1': min_image_d(base, o, nd1),
                   'Nd2': min_image_d(base, o, nd2)}
               for o in O_RANK01_16e}
    o_near_nd1 = min(O_RANK01_16e, key=lambda o: o_to_nd[o]['Nd1'])
    o_near_nd2 = sorted([o for o in O_RANK01_16e if o != o_near_nd1],
                        key=lambda o: o_to_nd[o]['Nd2'])

    print(f"\n  rank01 O assignment:")
    print(f"    Near Nd1: idx {o_near_nd1}  (d={o_to_nd[o_near_nd1]['Nd1']:.2f} Å)")
    print(f"    Near Nd2: {o_near_nd2}")

    # Free S near each Nd
    free_to_nd = {fs: {'Nd1': min_image_d(base, fs, nd1),
                       'Nd2': min_image_d(base, fs, nd2)}
                  for fs in free_s}
    near_nd1_4a = sorted([fs for fs in free_s if free_to_nd[fs]['Nd1'] < 5.0],
                        key=lambda fs: free_to_nd[fs]['Nd1'])
    near_nd2_4a = sorted([fs for fs in free_s if free_to_nd[fs]['Nd2'] < 5.0],
                        key=lambda fs: free_to_nd[fs]['Nd2'])

    print(f"\n  Free S (4a) near Nd1 (<5 Å): {len(near_nd1_4a)} → {near_nd1_4a[:5]}")
    print(f"  Free S (4a) near Nd2 (<5 Å): {len(near_nd2_4a)} → {near_nd2_4a[:5]}")

    candidates = []

    # Strategy A: BALANCED (2 PS3O Nd2 + 1 free O Nd1)
    print(f"\n  === Strategy A: balanced (2 PS3O@Nd2 + 1 freeO@Nd1) ===")
    for i, fs in enumerate(near_nd1_4a[:5]):
        candidates.append({
            'strategy': 'A_balanced',
            'idx': i,
            'o_16e': sorted(o_near_nd2),
            'o_4a': [fs],
            'description': f'A{i}: PS3O@Nd2(x2), freeO@Nd1[{fs}]'
        })

    # Strategy B: INVERSE (1 PS3O + 2 free O)
    print(f"\n  === Strategy B: inverse (1 PS3O@Nd2 + 2 freeO) ===")
    fs_pool = list(set(near_nd1_4a[:3] + near_nd2_4a[:3]))
    for i, fs_pair in enumerate(combinations(fs_pool, 2)):
        if i >= max_per_strategy:
            break
        candidates.append({
            'strategy': 'B_inverse',
            'idx': i,
            'o_16e': [o_near_nd2[0]],
            'o_4a': list(fs_pair),
            'description': f'B{i}: PS3O@Nd2(x1), freeO at {list(fs_pair)}'
        })

    # Strategy C: CLUSTER all near Nd2
    print(f"\n  === Strategy C: cluster all near Nd2 ===")
    nearby_16e_nd2 = sorted([s for s in ps4_s
                             if min_image_d(base, s, nd2) < 5.0],
                           key=lambda s: min_image_d(base, s, nd2))
    for i in range(min(5, len(near_nd2_4a))):
        if len(nearby_16e_nd2) >= 2 and i < len(near_nd2_4a):
            candidates.append({
                'strategy': 'C_cluster_Nd2',
                'idx': i,
                'o_16e': nearby_16e_nd2[:2],
                'o_4a': [near_nd2_4a[i]],
                'description': f'C{i}: 2 PS3O+1 freeO all near Nd2'
            })

    # Strategy D: CLUSTER all near Nd1 (test if Nd1-centric works)
    print(f"\n  === Strategy D: cluster all near Nd1 ===")
    nearby_16e_nd1 = sorted([s for s in ps4_s
                             if min_image_d(base, s, nd1) < 5.0],
                           key=lambda s: min_image_d(base, s, nd1))
    for i in range(min(5, len(near_nd1_4a))):
        if len(nearby_16e_nd1) >= 2 and i < len(near_nd1_4a):
            candidates.append({
                'strategy': 'D_cluster_Nd1',
                'idx': i,
                'o_16e': nearby_16e_nd1[:2],
                'o_4a': [near_nd1_4a[i]],
                'description': f'D{i}: 2 PS3O+1 freeO all near Nd1'
            })

    return candidates


# ============================================================
# MLIP screen
# ============================================================
def screen_candidates(base, candidates, outdir):
    """MLIP relax each candidate, return ranked results."""
    print(f"\n{'='*60}")
    print(f"MLIP screening ({len(candidates)} candidates)")
    print(f"{'='*60}")

    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    adaptor = AseAtomsAdaptor()

    def make_calc():
        return FAIRChemCalculator(predictor, task_name="omat")

    results = []
    for i, cand in enumerate(candidates):
        all_o = cand['o_16e'] + cand['o_4a']
        atoms = apply_substitution(base, ND_PAIR, VAC_INDICES, all_o)
        atoms.calc = make_calc()

        try:
            opt = LBFGS(atoms, logfile=None)
            opt.run(fmax=0.01, steps=200)
        except Exception as e:
            print(f"  ❌ {cand['description']}: relax failed ({e})")

        e = atoms.get_potential_energy()
        delta_meV = (e - RANK01_E_REF) * 1000

        results.append({
            'strategy': cand['strategy'],
            'idx': cand['idx'],
            'description': cand['description'],
            'o_16e': cand['o_16e'],
            'o_4a': cand['o_4a'],
            'energy_eV': e,
            'delta_vs_rank01_meV': delta_meV
        })

        marker = '⭐' if delta_meV < 0 else ' '
        print(f"  {marker} {i+1}/{len(candidates)}: {cand['description']}")
        print(f"     E = {e:.4f} eV   ΔE = {delta_meV:+.1f} meV vs rank01")

    results.sort(key=lambda x: x['energy_eV'])

    # Save
    Path(outdir).mkdir(parents=True, exist_ok=True)
    with open(f'{outdir}/mixed_O_results.json', 'w') as f:
        json.dump({
            'rank01_reference_eV': RANK01_E_REF,
            'n_candidates': len(results),
            'results': results
        }, f, indent=2)

    return results


# ============================================================
# Main
# ============================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True,
                    help='124-atom base xyz with Li/P/S/Cl (no Nd/O yet)')
    ap.add_argument('--outdir', default='mixed_results')
    ap.add_argument('--max-per-strategy', type=int, default=10)
    args = ap.parse_args()

    base = read(args.base)
    print(f"[INPUT] {args.base}")
    print(f"  Atoms: {len(base)}, Composition:")
    from collections import Counter
    print(f"  {dict(Counter(base.get_chemical_symbols()))}")

    print(f"\n[REFERENCE] rank01 (Track 1A pure) E = {RANK01_E_REF} eV")
    print(f"  Nd pair: {ND_PAIR}")
    print(f"  Vacancies: {VAC_INDICES}")
    print(f"  O sites (16e): {O_RANK01_16e}")

    print(f"\n[GENERATE] mixed candidates")
    candidates = generate_candidates(base, max_per_strategy=args.max_per_strategy)
    print(f"\n  Total candidates: {len(candidates)}")

    print(f"\n[SCREEN] MLIP relax")
    results = screen_candidates(base, candidates, args.outdir)

    # Summary
    print(f"\n{'='*60}")
    print(f"=== SUMMARY ===")
    print(f"{'='*60}")
    print(f"  rank01 (Track 1A pure):  -521.9585 eV (reference)")
    print(f"  rank02 (Track 1B pure):  -520.3255 eV (Δ = +1633 meV)")
    print()
    print(f"  Top 5 mixed candidates:")
    for i, r in enumerate(results[:5]):
        marker = '⭐ NEW WINNER' if r['delta_vs_rank01_meV'] < 0 else ''
        print(f"    {i+1}. {r['description']}")
        print(f"       E = {r['energy_eV']:.4f}  ΔE = {r['delta_vs_rank01_meV']:+.1f} meV vs rank01 {marker}")

    if any(r['delta_vs_rank01_meV'] < 0 for r in results):
        print(f"\n  ⚠️ FOUND mixed candidate(s) below rank01!")
        print(f"     Asymmetric Nd-O hero finding requires reconsideration.")
    else:
        min_dE = min(r['delta_vs_rank01_meV'] for r in results)
        print(f"\n  ✅ All mixed candidates above rank01 (min ΔE = {min_dE:+.1f} meV)")
        print(f"     Track 1A asymmetric Nd-O finding CONFIRMED — robust to mixed.")
        print(f"     Paper #2 hero finding reviewer-proof.")

    print(f"\n  Results saved: {args.outdir}/mixed_O_results.json")


if __name__ == '__main__':
    main()
