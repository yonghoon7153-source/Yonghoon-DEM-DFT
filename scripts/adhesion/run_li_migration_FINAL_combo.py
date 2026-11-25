#!/usr/bin/env python
"""run_li_migration_FINAL_combo.py — Li migration test for FINAL combo (5 comps).

Adds comp3_v2 and comp5_v2 to the existing 4-comp test (comp1, comp2,
comp4_v1, modelC) to verify the family-level vacancy mechanism.

For each comp:
  N_migrate ∈ {0, 1, 2, 3}: move N bulk Li to NCM-facing surface (rigid)
  At each N: 16 gap × R1_origin single-point UMA -> Wad_well

Hypothesis (paper):
  Li5.4 (vacancies): ΔWad(N) > 0 — migration creates favorable interface Li
  Li6 (no vacancies): ΔWad(N) < 0 — forced migration costs energy

FINAL combo slab choices (match figure R=+0.989):
  comp1     : comp1_slab_v2.xyz                        face A
  comp2     : comp2_slab_v2.xyz                        face A
  comp3_v2  : comp3_slab_v2_preShift.xyz (preShift)    face B (z-mirror)
  comp4_v2  : comp4_v2_slab_shift2.xyz                 face B (z-mirror)
  comp5_v2  : comp5_v2_slab_shift2.xyz                 face A

NCM (5x5x1) for Li5.4 family; (7x7x1) for Li6 family.

Cost: 5 comps × 4 N × 16 gap = 320 SCFs ≈ 15 min

Run from /data/work/v30u_ensemble/
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

WORK = Path('/data/work/v30u_ensemble')
OUT_DIR = WORK / 'li_migration_FINAL_results'
OUT_DIR.mkdir(exist_ok=True)
SLAB_DIR = OUT_DIR / 'slabs'
SLAB_DIR.mkdir(exist_ok=True)

# FINAL combo
COMPS = {
    'comp1':    {'se': 'comp1_slab_v2.xyz',                 'ncm': 'ncm_7x7x1_PRESERVED.xyz',
                 'face': 'A', 'family': 'Li6'},
    'comp2':    {'se': 'comp2_slab_v2.xyz',                 'ncm': 'ncm_7x7x1_PRESERVED.xyz',
                 'face': 'A', 'family': 'Li6'},
    'comp3_v2': {'se': 'comp3_slab_v2_preShift.xyz',        'ncm': 'ncm_5x5x1_PRESERVED.xyz',
                 'face': 'B', 'family': 'Li5.4'},
    'comp4_v2': {'se': 'comp4_v2_slab_shift2.xyz',          'ncm': 'ncm_5x5x1_PRESERVED.xyz',
                 'face': 'B', 'family': 'Li5.4'},
    'comp5_v2': {'se': 'comp5_v2_slab_shift2.xyz',          'ncm': 'ncm_5x5x1_PRESERVED.xyz',
                 'face': 'A', 'family': 'Li5.4'},
}
D_VALUES = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0]
N_MIGRATE_LIST = [0, 1, 2, 3]
SHIFT_FRAC = (0.0, 0.0)
SURFACE_INSERT_HEIGHT = 1.0
MIN_DIST = 1.8
RANDOM_SEED = 42
VACUUM_TOP = 30.0


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def flip_se_xy(se):
    """Mirror SE slab in z (face A ↔ face B)."""
    a = se.copy()
    pos = a.positions.copy()
    pos[:, 2] = pos[:, 2].max() + pos[:, 2].min() - pos[:, 2]
    a.set_positions(pos)
    return a


def make_se_variant(se_orig, N, seed):
    """Move top-most N Li atoms to bottom surface (NCM-facing = z_min)."""
    if N == 0:
        return se_orig.copy()
    se = se_orig.copy()
    sym = np.array(se.symbols)
    z = se.positions[:, 2]
    li_mask = sym == 'Li'
    if li_mask.sum() < N:
        return None  # not enough Li
    # Top-most N Li atoms (high z)
    li_indices = np.where(li_mask)[0]
    z_li = z[li_indices]
    top_n_local = np.argsort(z_li)[-N:]
    top_n_global = li_indices[top_n_local]

    # Delete them, get the cell + remaining positions
    keep_mask = np.ones(len(se), dtype=bool)
    keep_mask[top_n_global] = False
    se_keep = se[keep_mask]

    # Place N new Li at bottom (z_min - SURFACE_INSERT_HEIGHT pushed up by 1Å)
    z_min = se_keep.positions[:, 2].min()
    target_z = z_min + SURFACE_INSERT_HEIGHT  # 1 Å above SE bottom face
    rng = np.random.default_rng(seed + N * 100)
    cell = se_keep.cell.array

    new_atoms = []
    for trial in range(N):
        for _ in range(200):
            # Random xy fractional
            fx, fy = rng.random(2)
            cart = fx * cell[0, :2] + fy * cell[1, :2]
            pos = np.array([cart[0], cart[1], target_z])
            # Check distance to all existing atoms (including newly added)
            all_pos = np.vstack([se_keep.positions, np.array(new_atoms)]) if new_atoms else se_keep.positions
            d = all_pos - pos
            # MIC in xy
            inv = np.linalg.inv(cell[:2, :2].T)
            for i in range(len(d)):
                frac = inv @ d[i, :2]
                frac -= np.round(frac)
                d[i, :2] = cell[:2, :2].T @ frac
            dists = np.sqrt(np.sum(d**2, axis=1))
            if dists.min() > MIN_DIST:
                new_atoms.append(pos.tolist())
                break
        else:
            log(f"  WARN: couldn't place Li #{trial+1} for N={N}, skipping")
            return None

    # Append new Li atoms
    new_li = Atoms('Li' * len(new_atoms), positions=new_atoms, cell=cell, pbc=se_keep.pbc)
    combined = se_keep + new_li
    return combined


def stack(se, ncm, gap):
    se_a = se.copy()
    ncm_a = ncm.copy()
    se_a.set_pbc([True, True, False])
    ncm_a.set_pbc([True, True, False])
    se_max = se_a.positions[:, 2].max()
    ncm_min = ncm_a.positions[:, 2].min()
    shift_z = se_max + gap - ncm_min
    ncm_a.translate([0, 0, shift_z])
    combined = se_a + ncm_a
    cell = se_a.cell.array.copy()
    cell[2, 2] = combined.positions[:, 2].max() + VACUUM_TOP
    combined.set_cell(cell)
    return combined


_predictor = None

def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


def get_energy(atoms, calc):
    atoms.calc = calc
    return atoms.get_potential_energy()


def main():
    t0 = time.time()
    log("=" * 70)
    log("Li-migration FINAL combo (5 comps)")
    log(f"  comps={list(COMPS.keys())}, N={N_MIGRATE_LIST}, gaps={len(D_VALUES)}")
    log(f"  Total SCFs: {len(COMPS) * len(N_MIGRATE_LIST) * len(D_VALUES) + len(COMPS) * len(N_MIGRATE_LIST)} ≈ {(len(COMPS) * len(N_MIGRATE_LIST) * len(D_VALUES) + len(COMPS) * len(N_MIGRATE_LIST)) * 0.5 / 60:.1f} min")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.")

    summary = {}
    for comp, info in COMPS.items():
        log(f"\n========= {comp} (family {info['family']}) =========")
        # Read base SE, apply face flip if needed
        se_orig = read(WORK / info['se'], format='extxyz')
        if info['face'] == 'B':
            se_orig = flip_se_xy(se_orig)
            log(f"  face B (z-mirrored)")
        else:
            log(f"  face A (original)")
        ncm = read(WORK / info['ncm'], format='extxyz')
        # NCM iso in SE cell
        ncm_iso = ncm.copy()
        # match cell xy
        ncm_iso.set_cell([se_orig.cell.array[0], se_orig.cell.array[1],
                          ncm_iso.cell.array[2]], scale_atoms=False)
        E_ncm_iso = get_energy(ncm_iso, calc)
        log(f"  E_ncm_iso = {E_ncm_iso:.4f} eV")

        results_per_N = {}
        for N in N_MIGRATE_LIST:
            se_var = make_se_variant(se_orig, N, RANDOM_SEED)
            if se_var is None:
                log(f"  N={N}: SKIP (couldn't make variant)")
                continue
            # Save slab
            write(SLAB_DIR / f'{comp}_N{N}.xyz', se_var)
            E_se = get_energy(se_var, calc)
            log(f"  N={N}: E_se_iso = {E_se:.4f}")
            area = abs(np.cross(np.append(se_var.cell.array[0, :2], 0),
                                np.append(se_var.cell.array[1, :2], 0))[2])
            curve = []
            for d in D_VALUES:
                stacked = stack(se_var, ncm, d)
                E_st = get_energy(stacked, calc)
                Wad = -(E_st - E_se - E_ncm_iso) / area * 16.0218  # eV/Å² -> J/m²
                curve.append({'d': d, 'E_stacked': float(E_st), 'Wad': float(Wad)})
            wad_arr = np.array([p['Wad'] for p in curve])
            wad_well = float(np.nanmax(wad_arr))
            wad_asymp = float(wad_arr[-1])
            log(f"     Wad_well = {wad_well:+.4f}   asymp = {wad_asymp:+.4f}")
            results_per_N[N] = {'wad_well': wad_well, 'wad_asymp': wad_asymp, 'curve': curve}

        wells = [results_per_N[N]['wad_well'] for N in N_MIGRATE_LIST if N in results_per_N]
        dWads = [wells[i] - wells[0] for i in range(len(wells))]
        summary[comp] = {
            'family': info['family'],
            'face': info['face'],
            'wad_wells': wells,
            'dWad_per_N': dWads,
        }
        json.dump({'summary': summary[comp], 'per_N': results_per_N},
                  open(OUT_DIR / f'{comp}_done.json', 'w'), indent=2, default=str)

        log(f"  ─── {comp} summary ───")
        for i, N in enumerate(N_MIGRATE_LIST[:len(wells)]):
            log(f"    N={N}: Wad_well = {wells[i]:+.4f}   ΔWad = {dWads[i]:+.4f} J/m²")

        # cleanup
        del se_orig, ncm
        gc.collect()

    # Save master summary
    json.dump(summary, open(OUT_DIR / 'summary.json', 'w'), indent=2, default=str)
    log(f"\nSaved: {OUT_DIR}/summary.json")
    log(f"Total: {(time.time()-t0)/60:.1f} min")

    log("\n" + "=" * 70)
    log("FINAL combo summary table:")
    log(f"  {'comp':<12} {'family':<7} {'N=0':>8} {'N=1':>8} {'N=2':>8} {'N=3':>8}  ΔWad(N=3)")
    for comp, d in summary.items():
        wells_str = '  '.join(f"{w:+.3f}" for w in d['wad_wells'])
        last_dwad = d['dWad_per_N'][-1] if d['dWad_per_N'] else 0.0
        log(f"  {comp:<12} {d['family']:<7} {wells_str}   ΔWad(N=3)={last_dwad:+.4f}")


if __name__ == "__main__":
    main()
