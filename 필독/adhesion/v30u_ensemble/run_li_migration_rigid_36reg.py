"""run_li_migration_rigid_36reg.py — Li-migration rigid test, 36 registries.

Extends run_li_migration_rigid_test.py (spot, 1 reg) to full phase1-style
36-registry mean (6 high-sym + 30 random seed=42), at z=0 only.

Cost: 4 comp × 4 N_migrate × 36 reg × 16 gap = 9216 SCFs ≈ 80 min
      + 4 × 4 = 16 E_se_iso SCFs

For each (comp, N_migrate), reports:
  • Wad_well mean over 36 reg
  • Wad_asymp mean over 36 reg
  • Wad_well std (registry variance)

Run on gabia (recommend background):
  cd /data/work/v30u_ensemble
  nohup python3 run_li_migration_rigid_36reg.py > li_mig_36reg.log 2>&1 &
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'family': 'Li6'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz', 'family': 'Li6'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz', 'family': 'Li5.4'},
}
D_VALUES = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0]
N_MIGRATE_LIST = [0, 1, 2, 3]

HIGH_SYM = [
    ("R1_origin",   (0.0, 0.0)),
    ("R2_half_x",   (0.5, 0.0)),
    ("R3_half_y",   (0.0, 0.5)),
    ("R4_diagonal", (0.5, 0.5)),
    ("R5_hex1",     (1/3, 2/3)),
    ("R6_hex2",     (2/3, 1/3)),
]
N_RANDOM = 30
RANDOM_SEED_REG  = 42         # for registry shifts (phase1 protocol)
RANDOM_SEED_BASE = 42         # for Li migration placement (per-N reproducible)

SURFACE_INSERT_HEIGHT = 1.0
MIN_DIST = 1.8
VACUUM_TOP = 30.0

WORK    = Path('/data/work/v30u_ensemble')
ISO_REF = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT     = WORK / 'li_migration_36reg_results'
OUT.mkdir(exist_ok=True)
SLAB_OUT = OUT / 'slabs'
SLAB_OUT.mkdir(exist_ok=True)
LOG = OUT / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


# ─── geometry helpers (verbatim) ─────────────────────────────────────────────

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
    if n_migrate == 0:
        return se.copy(), 0
    se_new = se.copy()
    syms = se_new.get_chemical_symbols()
    pos  = se_new.get_positions()
    li_indices = [i for i, s in enumerate(syms) if s == 'Li']
    if len(li_indices) < n_migrate:
        return se_new, 0
    li_indices_sorted = sorted(li_indices, key=lambda i: -pos[i, 2])
    to_move = li_indices_sorted[:n_migrate]
    cell = se_new.cell.array
    z_min = pos[:, 2].min()
    z_surf_target = z_min + SURFACE_INSERT_HEIGHT
    keep_mask = np.ones(len(se_new), dtype=bool)
    for i in to_move:
        keep_mask[i] = False
    new_syms = [s for s, k in zip(syms, keep_mask) if k]
    new_pos  = pos[keep_mask].copy()
    n_added = 0
    for _ in range(n_migrate):
        for trial in range(50):
            frac_xy = rng.random(2)
            cart_xy = frac_xy[0] * cell[0, :2] + frac_xy[1] * cell[1, :2]
            cand = np.array([cart_xy[0], cart_xy[1], z_surf_target])
            diffs = new_pos - cand
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
    se_out = Atoms(symbols=new_syms, positions=new_pos,
                   cell=cell, pbc=[True, True, True])
    return se_out, n_added


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
    rng_reg = np.random.default_rng(RANDOM_SEED_REG)
    RANDOM_REG = [(f"rand_{i+1:03d}", (rng_reg.uniform(0, 1), rng_reg.uniform(0, 1)))
                  for i in range(N_RANDOM)]
    ALL_REG = HIGH_SYM + RANDOM_REG

    n_configs_total = len(COMPS) * len(N_MIGRATE_LIST) * len(ALL_REG) * len(D_VALUES)
    log("=" * 70)
    log(f"Li-migration RIGID test — 36 registries, z=0")
    log(f"  comps={len(COMPS)} × N_migrate={len(N_MIGRATE_LIST)} × "
        f"reg={len(ALL_REG)} × gaps={len(D_VALUES)} = {n_configs_total} SCFs")
    log(f"  Expected time: ~{n_configs_total * 0.5 / 60:.0f} min "
        f"(0.5 s/SCF on A100/A6000)")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.\n")

    t_global = time.time()
    summary = {}
    idx_global = 0

    for c, info in COMPS.items():
        f_iso = ISO_REF / f"{c}_done.json"
        if not f_iso.exists():
            log(f"[{c}] missing eiso JSON, skip"); continue
        d_iso = json.load(open(f_iso))
        E_ncm_iso = d_iso['E_ncm_iso']

        log(f"\n========= {c} (family {info['family']}) =========")
        se_base = read(WORK / info['se'])
        ncm     = read(WORK / info['ncm'])
        log(f"  E_ncm_iso (SE cell) = {E_ncm_iso:.4f} eV")

        comp_result = {
            'comp':            c,
            'family':          info['family'],
            'N_migrate_list':  N_MIGRATE_LIST,
            'gaps':            D_VALUES,
            'registries':      [r[0] for r in ALL_REG],
            'E_ncm_iso':       E_ncm_iso,
            'variants':        {},
        }

        for N in N_MIGRATE_LIST:
            # Build migrated SE slab (fixed for all registries of this N)
            rng_N = np.random.default_rng(RANDOM_SEED_BASE + N)
            se_var, n_actual = make_migrated_slab(se_base, N, rng_N)
            write(SLAB_OUT / f"{c}_Nmig{N}.xyz", se_var)

            # E_se_iso for this variant
            se_iso = se_var.copy()
            cell_iso = se_iso.cell.array.copy()
            cell_iso[2, 2] += VACUUM_TOP
            se_iso.set_cell(cell_iso, scale_atoms=False)
            se_iso.set_pbc([True, True, True])
            se_iso.calc = calc
            E_se_var = float(se_iso.get_potential_energy())

            log(f"  N_migrate={N} (moved {n_actual}/{N})  E_se_iso = {E_se_var:.4f} eV")

            variant_data = {
                'n_actually_moved': n_actual,
                'E_se_iso':         E_se_var,
                'per_reg':          {},
                'Wad_samples':      {f"{g:.3f}": [] for g in D_VALUES},
            }

            t_reg = time.time()
            for reg_name, shift in ALL_REG:
                reg_curve = {}
                for d in D_VALUES:
                    idx_global += 1
                    try:
                        stacked = stack_interface(se_var, ncm, d, shift)
                        stacked.calc = calc
                        E_int = float(stacked.get_potential_energy())
                        A = xy_area(stacked.cell.array)
                        Wad = -(E_int - E_se_var - E_ncm_iso) / A * 16.0218
                        reg_curve[f"{d:.3f}"] = {
                            'E_int': E_int, 'Wad_J_per_m2': Wad, 'area_A2': A,
                        }
                        variant_data['Wad_samples'][f"{d:.3f}"].append(Wad)
                    except Exception as e:
                        reg_curve[f"{d:.3f}"] = {'E_int': None, 'error': str(e)}
                variant_data['per_reg'][reg_name] = {'shift': list(shift), 'curve': reg_curve}
                if (idx_global % 100) == 0:
                    el = time.time() - t_global
                    eta = el * (n_configs_total - idx_global) / idx_global
                    log(f"    progress {idx_global}/{n_configs_total}  "
                        f"({c} N={N} {reg_name})  el={el/60:.1f}min ETA={eta/60:.1f}min")

            # Aggregate over 36 registries
            wad_mean, wad_std = [], []
            for d in D_VALUES:
                samples = variant_data['Wad_samples'][f"{d:.3f}"]
                if samples:
                    wad_mean.append(float(np.mean(samples)))
                    wad_std.append(float(np.std(samples)))
                else:
                    wad_mean.append(None); wad_std.append(None)
            variant_data['Wad_mean'] = wad_mean
            variant_data['Wad_std']  = wad_std
            valid_mean = np.array([m for m in wad_mean if m is not None])
            wad_well_mean = float(np.nanmax(valid_mean))
            wad_well_std_at_max = wad_std[int(np.nanargmax(valid_mean))] if wad_std[int(np.nanargmax(valid_mean))] is not None else 0.0
            wad_asymp_mean = float(wad_mean[-1])
            variant_data['Wad_well_mean'] = wad_well_mean
            variant_data['Wad_well_std']  = wad_well_std_at_max
            variant_data['Wad_asymp_mean'] = wad_asymp_mean
            log(f"    [{c} N={N}]  Wad_well = {wad_well_mean:+.4f} ± {wad_well_std_at_max:.4f}  "
                f"asymp = {wad_asymp_mean:+.4f}  (36-reg mean,  {(time.time()-t_reg)/60:.1f} min)")

            comp_result['variants'][f"N{N}"] = variant_data
            gc.collect()

        json.dump(comp_result, open(OUT / f"{c}_done.json", 'w'), indent=2)

        # Per-comp ΔWad(N) summary
        wells = [comp_result['variants'][f"N{N}"]['Wad_well_mean']
                 for N in N_MIGRATE_LIST]
        stds  = [comp_result['variants'][f"N{N}"]['Wad_well_std']
                 for N in N_MIGRATE_LIST]
        log(f"  ─── {c} 36-reg summary (Wad_well ± σ vs N_migrate) ───")
        for N, w, s in zip(N_MIGRATE_LIST, wells, stds):
            dW = w - wells[0]
            log(f"     N={N}: Wad_well = {w:+.4f} ± {s:.4f}   ΔWad = {dW:+.4f} J/m²")
        summary[c] = {
            'family':     info['family'],
            'Wad_wells':  wells,
            'Wad_stds':   stds,
            'dWad_per_N': [w - wells[0] for w in wells],
        }

    json.dump(summary, open(OUT / 'summary.json', 'w'), indent=2)

    log("\n" + "=" * 70)
    log("INTERPRETATION:")
    log("  • Compare 36-reg mean ΔWad(N) per family:")
    log("    Li5.4 should show positive slope (vacancy benefits Li-O contact)")
    log("    Li6   should show negative slope (forced vacancy costs energy)")
    log("  • Combined with α=1.0 strain: Wad_combined = Wad(N) - ΔWad_strain")
    log("    Expected R(Wad_combined, paper_aJ) > +0.96 (α alone gave +0.96)")
    log(f"  • Output: {OUT}")
    log("=" * 70)
    log(f"\nTOTAL: {(time.time() - t_global) / 60:.1f} min")


if __name__ == "__main__":
    main()
