"""run_v30u_1L_vacancy_aware_relax.py — Li-only migration relax (vacancy-aware).

Captures the dominant paper-relevant effect missed by rigid scan:
  • Li5.4 has 0.6 Li vacancies per fu → Li can hop through these vacancies
    toward the NCM-O interface during contact
  • Each Li migration adds new Li-O bonds → strong Wad boost
  • Li6 has full Li sublattice → no hopping → no migration gain
  → expected: Li5.4 > Li6 (paper direction) recovered

Why Li-only relax (not full relax):
  • Full relax causes SE-NCM intermixing (P, S, halogen migrate too) → unphysical
  • Real interface: only Li is mobile at room T (Ea ~0.2 eV for Li in Li5.4)
  • Other ions stay frozen on ~hours timescale in real experiments

Constraints (FixAtoms applied to indices that CANNOT move):
  • Non-Li atoms everywhere (P, S, Cl, Br, O, Ni, Co, Mn)  → FIX
  • Li atoms in NCM region (z < ncm_z_max)                  → FIX  (no NCM-Li)
  • Li atoms in SE bulk (z > se_z_min + LI_FREE_DEPTH)      → FIX  (bulk static)
  • Li atoms within LI_FREE_DEPTH of SE-bottom face         → FREE (interface Li)

Mode 'spot' (default): z=0, R1_origin only, all 16 gaps × 4 comps = 64 relax
Mode 'z0_6sym':         z=0, 6 high-sym registries           = 384 relax (~1.5 h)
Mode 'z0_full':         z=0, 36 registries                    = 2304 relax (~6 h)

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 run_v30u_1L_vacancy_aware_relax.py [spot|z0_6sym|z0_full]
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_PRESERVED.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_PRESERVED.xyz'},
}
D_VALUES = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5, 2.8, 3.0, 3.5, 4.0, 5.0, 7.0]

HIGH_SYM = [
    ("R1_origin",   (0.0, 0.0)),
    ("R2_half_x",   (0.5, 0.0)),
    ("R3_half_y",   (0.0, 0.5)),
    ("R4_diagonal", (0.5, 0.5)),
    ("R5_hex1",     (1/3, 2/3)),
    ("R6_hex2",     (2/3, 1/3)),
]
N_RANDOM = 30
RANDOM_SEED = 42

VACUUM_TOP      = 30.0
F_MAX           = 0.03
MAXSTEPS        = 30
LI_FREE_DEPTH   = 5.0      # Å — Li within this depth of SE-bottom face is free
MAX_DISP_WARN   = 2.0      # Å — flag if any Li moves more than this (suspicious)

WORK    = Path('/data/work/v30u_ensemble')
ISO_REF = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT     = WORK / 'v30u_1L_vacancy_aware_relax_results'
OUT.mkdir(exist_ok=True)
LOG = OUT / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


# ─── Geometry (verbatim phase1/eiso_fix) ────────────────────────────────────

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
    n_ncm = len(ncm_a)
    combined = ncm_a + se_a
    new_cell = se.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0, 0, z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, n_ncm


def apply_vacancy_aware_fix(atoms, n_ncm, li_free_depth=LI_FREE_DEPTH):
    """Fix everything EXCEPT Li atoms in the SE bottom layer.

    Free set = {atom i : symbol(i)='Li' AND ncm_z_max < z(i) < se_z_min + li_free_depth}
    All other atoms (NCM all, non-Li SE, Li in bulk-SE, halogen, S, P) are FIXED.
    """
    from ase.constraints import FixAtoms
    pos  = atoms.get_positions()
    syms = atoms.get_chemical_symbols()
    ncm_z_max = pos[:n_ncm, 2].max()
    se_z_min  = pos[n_ncm:, 2].min()
    z_li_upper = se_z_min + li_free_depth

    free_idx = []
    for i in range(len(atoms)):
        if syms[i] != 'Li':
            continue                            # non-Li always fixed
        if i < n_ncm:
            continue                            # NCM Li (shouldn't exist for NCM but safe) fixed
        z = pos[i, 2]
        if ncm_z_max < z < z_li_upper:
            free_idx.append(i)
    fix_idx = [i for i in range(len(atoms)) if i not in set(free_idx)]
    atoms.set_constraint(FixAtoms(indices=fix_idx))
    return len(fix_idx), len(free_idx)


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


# ─── UMA ────────────────────────────────────────────────────────────────────

_predictor = None


def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


def relax_atoms(atoms, fmax=F_MAX, steps=MAXSTEPS):
    from ase.optimize import LBFGS
    opt = LBFGS(atoms, logfile=None)
    opt.run(fmax=fmax, steps=steps)
    return float(atoms.get_potential_energy()), opt.nsteps


# ─── MAIN ───────────────────────────────────────────────────────────────────

def get_registries(mode):
    if mode == 'spot':
        return [HIGH_SYM[0]]
    if mode == 'z0_6sym':
        return HIGH_SYM
    if mode == 'z0_full':
        rng = np.random.default_rng(RANDOM_SEED)
        rand = [(f"rand_{i+1:03d}", (rng.uniform(0, 1), rng.uniform(0, 1)))
                for i in range(N_RANDOM)]
        return HIGH_SYM + rand
    raise ValueError(f"unknown mode: {mode}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'spot'
    REGISTRIES = get_registries(mode)
    log("=" * 70)
    log(f"Vacancy-aware Li-only relax — mode={mode}")
    log(f"  registries={len(REGISTRIES)}  gaps={len(D_VALUES)}")
    log(f"  Free: Li atoms within {LI_FREE_DEPTH} Å of SE-bottom face")
    log(f"  Fixed: NCM all + non-Li SE all + bulk-Li in SE")
    log(f"  LBFGS: fmax={F_MAX}, max {MAXSTEPS} steps")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    calc = make_calc()
    log("UMA loaded.\n")

    t_global = time.time()

    for c, paths in COMPS.items():
        f_iso = ISO_REF / f"{c}_done.json"
        if not f_iso.exists():
            log(f"[{c}] missing eiso_fix JSON, skip"); continue
        d_iso = json.load(open(f_iso))

        log(f"\n========= {c} =========")
        E_se_per_z = d_iso['E_se_iso_per_z']
        E_ncm_iso  = d_iso['E_ncm_iso']
        log(f"  E_se_iso[z=0] = {E_se_per_z[0]:.4f} eV")
        log(f"  E_ncm_iso (SE cell) = {E_ncm_iso:.4f} eV")

        se  = read(WORK / paths['se'])
        ncm = read(WORK / paths['ncm'])

        comp_out = {
            'comp':           c,
            'mode':           mode,
            'fmax':           F_MAX,
            'max_steps':      MAXSTEPS,
            'li_free_depth':  LI_FREE_DEPTH,
            'E_se_iso':       E_se_per_z[0],
            'E_ncm_iso':      E_ncm_iso,
            'curves':         {},
        }

        for reg_name, shift in REGISTRIES:
            log(f"  {c} {reg_name} shift={shift}")
            reg_curve = {}
            for d in D_VALUES:
                d_key = f"{d:.3f}"
                t0 = time.time()
                stacked, n_ncm = stack_interface(se, ncm, d, shift)
                stacked.calc = calc
                E_rigid = float(stacked.get_potential_energy())
                A = xy_area(stacked.cell.array)
                Wad_rigid = -(E_rigid - E_se_per_z[0] - E_ncm_iso) / A * 16.0218
                # Vacancy-aware constraint (Li-only, interface layer)
                pos_before = stacked.get_positions().copy()
                n_fix, n_free = apply_vacancy_aware_fix(stacked, n_ncm)
                if n_free == 0:
                    log(f"    [WARN] {reg_name} d={d:.2f}: 0 free Li atoms — skip relax")
                    Wad_relaxed = Wad_rigid
                    n_steps = 0
                    max_disp = 0.0
                    dE = 0.0
                else:
                    E_relaxed, n_steps = relax_atoms(stacked)
                    pos_after = stacked.get_positions()
                    disp = np.linalg.norm(pos_after - pos_before, axis=1)
                    max_disp = float(disp.max())
                    Wad_relaxed = -(E_relaxed - E_se_per_z[0] - E_ncm_iso) / A * 16.0218
                    dE = E_rigid - float(E_relaxed)
                t_elapsed = time.time() - t0
                warn = " ⚠" if max_disp > MAX_DISP_WARN else ""
                reg_curve[d_key] = {
                    'E_rigid':     E_rigid,
                    'E_relaxed':   E_rigid - dE,
                    'dE':          dE,
                    'Wad_rigid':   Wad_rigid,
                    'Wad_relaxed': Wad_relaxed,
                    'n_steps':     n_steps,
                    'n_free_Li':   n_free,
                    'n_fixed':     n_fix,
                    'n_total':     len(stacked),
                    'max_disp_A':  max_disp,
                    'area_A2':     A,
                    't_sec':       t_elapsed,
                }
                log(f"    d={d:>4.2f}  ΔE={dE:+.2f}  Wad_rig={Wad_rigid:+.3f}  "
                    f"Wad_rlx={Wad_relaxed:+.3f}  disp={max_disp:.2f}Å{warn}  "
                    f"n={n_steps}/{MAXSTEPS}  free_Li={n_free}  t={t_elapsed:.1f}s")
                gc.collect()

            comp_out['curves'][reg_name] = {'shift': list(shift), 'curve': reg_curve}

        # Per-comp summary
        comp_out['gaps'] = D_VALUES
        means_rigid, means_relax = [], []
        for d in D_VALUES:
            dk = f"{d:.3f}"
            wr = [reg['curve'][dk]['Wad_rigid']   for reg in comp_out['curves'].values()]
            wl = [reg['curve'][dk]['Wad_relaxed'] for reg in comp_out['curves'].values()]
            means_rigid.append(float(np.mean(wr)))
            means_relax.append(float(np.mean(wl)))
        comp_out['Wad_rigid_mean']   = means_rigid
        comp_out['Wad_relaxed_mean'] = means_relax
        wr = np.array(means_rigid); wl = np.array(means_relax)
        log(f"  ─── {c} summary ───")
        log(f"     Wad_rigid    well={np.max(wr):+.3f}  asymp={wr[-1]:+.3f}")
        log(f"     Wad_relaxed  well={np.max(wl):+.3f}  asymp={wl[-1]:+.3f}")
        log(f"     ΔWad (Li relax gain at well) = {np.max(wl) - np.max(wr):+.3f} J/m²")

        json.dump(comp_out, open(OUT / f"{c}_done.json", 'w'), indent=2)
        log(f"  saved {c}_done.json")

    log(f"\nTOTAL: {(time.time() - t_global) / 60:.1f} min")
    log(f"Results: {OUT}")


if __name__ == "__main__":
    main()
