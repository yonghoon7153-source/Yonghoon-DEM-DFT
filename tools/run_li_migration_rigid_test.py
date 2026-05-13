"""run_li_migration_rigid_test.py — pre-stack Li migration, rigid scan only.

Captures vacancy-migration effect within RIGID framework by physically
moving N bulk-Li atoms to the NCM-facing surface BEFORE stacking. No LBFGS,
no atomic optimization during scan — just rigid single-point UMA on
"migration-pre-equilibrated" SE slabs.

Hypothesis:
  • Li5.4 (with vacancies): each migration creates a real new low-energy
    interface Li site → ΔWad positive, growing with N
  • Li6 (no vacancies): forced migration creates an artificial vacancy
    in bulk + over-coordinated Li at surface → ΔWad negative or flat

  If true → rigid scan can recover paper trend (Li5.4 > Li6) via the
  vacancy-aware SE slab variants, without any relax.

Variants per comp:
  N_migrate ∈ {0, 1, 2, 3}
  N=0: original SE  (baseline)
  N=k: top-most k Li atoms (highest z = bulk) deleted, k new Li atoms
       placed at bottom of SE (low z, ~1 Å above SE-min) with random xy
       (positions screened to keep ≥ 1.8 Å from all existing atoms)

Spot test: z=0, R1_origin, all 16 gaps × 4 comps × 4 N_migrate = 256 SCFs
           ~13 min

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 run_li_migration_rigid_test.py
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'family': 'Li6'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'family': 'Li6'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
}
D_VALUES = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0]
N_MIGRATE_LIST = [0, 1, 2, 3]
SHIFT_FRAC = (0.0, 0.0)        # R1_origin
SURFACE_INSERT_HEIGHT = 1.0    # Å above SE z_min for inserted Li
MIN_DIST = 1.8                  # Å — keep new Li at least this from all atoms
RANDOM_SEED = 42
VACUUM_TOP = 30.0

WORK    = Path('/data/work/v30u_ensemble')
ISO_REF = WORK / 'v30u_1L_correct_results_eiso_fix'   # for E_se_iso[z=0] & E_ncm_iso
OUT     = WORK / 'li_migration_rigid_results'
OUT.mkdir(exist_ok=True)
SLAB_OUT = OUT / 'slabs'
SLAB_OUT.mkdir(exist_ok=True)
LOG = OUT / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


# ─── geometry helpers ───────────────────────────────────────────────────────

def stack_interface(se, ncm, gap, shift_frac):
    se_a = se.copy(); ncm_a = ncm.copy()
    dx, dy = shift_frac
    shift_cart = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    ncm_a.translate([shift_cart[0], shift_cart[1], 0])
    ncm_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    ncm_z_max = ncm_a.positions[:, 2].max()
    se_z_min  = se_a.positions[:, 2].min()
    se_a.translate([0, 0, ncm_z_max - se_z_min + gap])
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


def make_migrated_slab(se, n_migrate, rng):
    """Move N top-most Li atoms (highest z) to bottom surface positions.

    Returns (new_se, n_actually_moved). If no valid surface position found
    for some Li, just deletes that Li (creating real vacancy + bulk loss).
    """
    if n_migrate == 0:
        return se.copy(), 0

    se_new = se.copy()
    syms = se_new.get_chemical_symbols()
    pos  = se_new.get_positions()
    li_indices = [i for i, s in enumerate(syms) if s == 'Li']
    if len(li_indices) < n_migrate:
        return se_new, 0

    # Top-most N_migrate Li (highest z)
    li_indices_sorted = sorted(li_indices, key=lambda i: -pos[i, 2])
    to_move = li_indices_sorted[:n_migrate]

    # Mark them for deletion, will replace with new Li at surface
    cell = se_new.cell.array
    z_min = pos[:, 2].min()
    z_surf_target = z_min + SURFACE_INSERT_HEIGHT

    # Build new positions: remove old, then add new
    keep_mask = np.ones(len(se_new), dtype=bool)
    for i in to_move:
        keep_mask[i] = False
    new_syms = [s for s, k in zip(syms, keep_mask) if k]
    new_pos  = pos[keep_mask].copy()

    # Place new Li at surface: random xy in cell, z = z_surf_target
    n_added = 0
    for _ in range(n_migrate):
        for trial in range(50):
            frac_xy = rng.random(2)
            cart_xy = frac_xy[0] * cell[0, :2] + frac_xy[1] * cell[1, :2]
            cand = np.array([cart_xy[0], cart_xy[1], z_surf_target])
            # Check distance to all existing (and previously added) atoms
            diffs = new_pos - cand
            # Wrap diffs in xy by min-image
            for j in range(2):
                lvec = cell[j, :2]
                ll = np.linalg.norm(lvec)
                if ll > 0:
                    proj = (diffs[:, :2] @ lvec) / (ll * ll)
                    proj_round = np.round(proj)
                    diffs[:, :2] -= np.outer(proj_round, lvec)
            dists = np.linalg.norm(diffs, axis=1)
            if dists.min() >= MIN_DIST:
                new_syms.append('Li')
                new_pos  = np.vstack([new_pos, cand])
                n_added += 1
                break
        # If 50 trials fail, leave Li deleted

    se_new = se_new.copy()
    se_new.set_cell(cell, scale_atoms=False)
    # Rebuild atoms with new symbols + positions
    from ase import Atoms
    se_new = Atoms(symbols=new_syms, positions=new_pos,
                   cell=cell, pbc=[True, True, True])
    return se_new, n_added


# ─── UMA ────────────────────────────────────────────────────────────────────

_predictor = None


def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    rng = np.random.default_rng(RANDOM_SEED)
    log("=" * 70)
    log(f"Li-migration rigid test")
    log(f"  N_migrate ∈ {N_MIGRATE_LIST}  shift={SHIFT_FRAC}  gaps={len(D_VALUES)}")
    log(f"  4 comps × 4 N × 16 gap = 256 SCFs total (~13 min)")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.\n")

    t_global = time.time()

    summary = {}
    for c, info in COMPS.items():
        f_iso = ISO_REF / f"{c}_done.json"
        if not f_iso.exists():
            log(f"[{c}] missing eiso JSON, skip"); continue
        d_iso = json.load(open(f_iso))
        E_se_z0_orig  = d_iso['E_se_iso_per_z'][0]
        E_ncm_iso     = d_iso['E_ncm_iso']

        log(f"\n========= {c} (family {info['family']}) =========")
        se_base = read(WORK / info['se'])
        ncm     = read(WORK / info['ncm'])
        log(f"  E_se_iso[z=0,orig] = {E_se_z0_orig:.4f} eV")
        log(f"  E_ncm_iso (SE cell) = {E_ncm_iso:.4f} eV")

        comp_result = {
            'comp':            c,
            'family':          info['family'],
            'N_migrate_list':  N_MIGRATE_LIST,
            'gaps':            D_VALUES,
            'E_ncm_iso':       E_ncm_iso,
            'variants':        {},
        }

        for N in N_MIGRATE_LIST:
            # Build migrated SE slab
            rng_N = np.random.default_rng(RANDOM_SEED + N)  # reproducible per N
            se_var, n_actual = make_migrated_slab(se_base, N, rng_N)
            # Save xyz for inspection
            from ase.io import write
            write(SLAB_OUT / f"{c}_Nmig{N}.xyz", se_var)

            # E_se_iso for this variant (need new SCF since slab changed)
            from ase.atoms import Atoms
            se_iso = se_var.copy()
            # Add vacuum on top, same convention as v30u_1L_correct
            cell = se_iso.cell.array.copy()
            cell[2, 2] += VACUUM_TOP
            se_iso.set_cell(cell, scale_atoms=False)
            se_iso.set_pbc([True, True, True])
            se_iso.calc = calc
            E_se_var = float(se_iso.get_potential_energy())

            log(f"  N_migrate={N}  (moved {n_actual}/{N})  E_se_iso = {E_se_var:.4f} eV")

            curve = {}
            wad_curve = []
            for d in D_VALUES:
                stacked = stack_interface(se_var, ncm, d, SHIFT_FRAC)
                stacked.calc = calc
                E_int = float(stacked.get_potential_energy())
                A = xy_area(stacked.cell.array)
                Wad = -(E_int - E_se_var - E_ncm_iso) / A * 16.0218
                curve[f"{d:.3f}"] = {
                    'E_int': E_int, 'Wad_J_per_m2': Wad, 'area_A2': A,
                }
                wad_curve.append(Wad)
            wad_arr = np.array(wad_curve)
            wad_max = float(np.nanmax(wad_arr))
            wad_asymp = float(wad_arr[-1])
            log(f"    Wad_well = {wad_max:+.4f}   asymp = {wad_asymp:+.4f}")

            comp_result['variants'][f"N{N}"] = {
                'n_actually_moved': n_actual,
                'E_se_iso':         E_se_var,
                'curve':            curve,
                'Wad_well':         wad_max,
                'Wad_asymp':        wad_asymp,
            }
            gc.collect()

        json.dump(comp_result, open(OUT / f"{c}_done.json", 'w'), indent=2)

        # Per-comp ΔWad(N) summary
        wad_wells = [comp_result['variants'][f"N{N}"]['Wad_well'] for N in N_MIGRATE_LIST]
        log(f"  ─── {c} summary  (Wad_well vs N_migrate) ───")
        for N, w in zip(N_MIGRATE_LIST, wad_wells):
            dW = w - wad_wells[0]
            log(f"     N={N}: Wad_well = {w:+.4f}   ΔWad = {dW:+.4f} J/m²")

        summary[c] = {
            'family':        info['family'],
            'wad_wells':     wad_wells,
            'dWad_per_N':    [w - wad_wells[0] for w in wad_wells],
        }

    json.dump(summary, open(OUT / 'summary.json', 'w'), indent=2)

    log("\n" + "=" * 70)
    log("INTERPRETATION:")
    log("  • Li5.4 (comp4, modelC): expect positive slope ΔWad(N) — migration gains")
    log("  • Li6  (comp1, comp2):  expect negative or flat — no vacancies, forced")
    log("  • Family split at large N → rigid framework captures paper trend")
    log("  • Slabs saved to: " + str(SLAB_OUT))
    log("=" * 70)
    log(f"\nTOTAL: {(time.time() - t_global) / 60:.1f} min")


if __name__ == "__main__":
    main()
