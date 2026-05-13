"""run_v30u_1L_correct_mlip_relax.py — UMA-LBFGS relax test on top of rigid scan.

Question: rigid scan + eiso_fix gave Li6 > Li5.4 (paper inverted). Does
allowing interface atomic relaxation (UMA-driven LBFGS) recover paper's
Li5.4 > Li6 direction? Hypothesis: yes, because Li5.4's vacancies enable
Li migration toward NCM oxygen → extra Li-O bonds form upon relaxation,
boosting Wad(Li5.4) preferentially.

Method (spot test by default):
  • For each comp, for each gap in D_VALUES:
      - Build stacked interface (z=0, R1_origin shift) as in v30u_1L_correct
      - LBFGS relax atomic positions (cell FIXED), fmax=0.05 eV/Å, max 100 steps
      - Record E_int_relaxed, dE = E_rigid - E_relaxed, N_steps
  • Reuse E_se_iso (z=0) and E_ncm_iso (SE cell, eiso_fix) from existing JSON
    as references — clean apples-to-apples comparison of rigid vs relaxed E_int.
  • Wad_relaxed = (E_se_iso + E_ncm_iso_SEcell - E_int_relaxed) / A × 16.0218

Modes:
  spot      : z=0, R1_origin, all 16 gaps   → 4 comp × 16 = 64 relax (~15 min)
  z0_6sym   : z=0, 6 high-sym registries     → 4 × 96 = 384 relax  (~1.5 h)
  z0_full   : z=0, 36 registries             → 4 × 576 = 2304 relax (~6-8 h)

CLI:
  python3 run_v30u_1L_correct_mlip_relax.py [spot|z0_6sym|z0_full]
"""
import os, sys, json, time, gc
from pathlib import Path
import numpy as np
from ase.io import read

# ─── CONFIG (matches run_v30u_1L_correct.py) ────────────────────────────────
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
VACUUM_TOP = 30.0

# LBFGS relax params
F_MAX  = 0.05    # eV/Å
MAXSTEPS = 100

WORK    = Path('/data/work/v30u_ensemble')
ISO_REF = WORK / 'v30u_1L_correct_results_eiso_fix'      # for E_ncm_iso (SE cell)
RIGID   = WORK / 'v30u_1L_correct_results_eiso_fix'      # for area, E_int_rigid
OUT     = WORK / 'v30u_1L_correct_mlip_relax_results'
OUT.mkdir(exist_ok=True)
LOG = OUT / 'progress.log'


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


# ─── Reference builders (verbatim from run_v30u_1L_correct.py) ──────────────

def add_vacuum(atoms, vac):
    cell = atoms.cell.array.copy()
    cell[2, 2] += vac
    atoms.set_cell(cell, scale_atoms=False)
    atoms.set_pbc([True, True, True])
    return atoms


def stack_interface(se, ncm, gap, shift_frac):
    """Returns (combined_atoms, n_ncm) — n_ncm needed for FixAtoms partitioning."""
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


def apply_haruyama_fixes(atoms, n_ncm, fix_frac=1/3):
    """FixAtoms: bottom 1/3 of NCM (anchors NCM) + top 1/3 of SE (prevents lift).
    Middle 2/3 of each slab is free → interface relax allowed, no rigid drift,
    no intermixing through far side. Haruyama 2014 protocol."""
    from ase.constraints import FixAtoms
    pos = atoms.get_positions()
    fix_idx = []
    # NCM: bottom slice
    ncm_z = pos[:n_ncm, 2]
    ncm_z_min, ncm_z_max = ncm_z.min(), ncm_z.max()
    ncm_cut = ncm_z_min + fix_frac * (ncm_z_max - ncm_z_min)
    for i in range(n_ncm):
        if pos[i, 2] <= ncm_cut:
            fix_idx.append(i)
    # SE: top slice
    se_z = pos[n_ncm:, 2]
    se_z_min, se_z_max = se_z.min(), se_z.max()
    se_cut = se_z_max - fix_frac * (se_z_max - se_z_min)
    for i in range(n_ncm, len(atoms)):
        if pos[i, 2] >= se_cut:
            fix_idx.append(i)
    atoms.set_constraint(FixAtoms(indices=fix_idx))
    return len(fix_idx)


def xy_area(cell):
    a1 = cell[0]; a2 = cell[1]
    cross = np.cross(a1[:2].tolist() + [0], a2[:2].tolist() + [0])
    return float(np.linalg.norm(cross))


# ─── UMA (lazy) ─────────────────────────────────────────────────────────────

_predictor = None


def make_calc():
    global _predictor
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    if _predictor is None:
        _predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(_predictor, task_name="omat")


def relax_atoms(atoms, fmax=F_MAX, steps=MAXSTEPS):
    """LBFGS atomic relax with cell fixed. Returns (E_final, n_steps)."""
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
    log(f"MLIP relax test — mode={mode}  registries={len(REGISTRIES)}  gaps={len(D_VALUES)}")
    log(f"  E_se_iso and E_ncm_iso reused from eiso_fix JSON (SE cell refs)")
    log(f"  Relax: cell FIXED, fmax={F_MAX} eV/Å, max {MAXSTEPS} steps")
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
        E_ncm_iso  = d_iso['E_ncm_iso']                # SE-cell value (eiso_fix)
        log(f"  E_se_iso[z=0] = {E_se_per_z[0]:.4f} eV")
        log(f"  E_ncm_iso (SE cell) = {E_ncm_iso:.4f} eV")

        se  = read(WORK / paths['se'])
        ncm = read(WORK / paths['ncm'])

        comp_out = {
            'comp':       c,
            'mode':       mode,
            'fmax':       F_MAX,
            'max_steps':  MAXSTEPS,
            'E_se_iso':   E_se_per_z[0],
            'E_ncm_iso':  E_ncm_iso,
            'curves':     {},
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
                # Haruyama FixAtoms (anti-intermixing): NCM bottom 1/3 + SE top 1/3
                n_fixed = apply_haruyama_fixes(stacked, n_ncm, fix_frac=1/3)
                # Relax
                E_relaxed, n_steps = relax_atoms(stacked)
                Wad_relaxed = -(E_relaxed - E_se_per_z[0] - E_ncm_iso) / A * 16.0218
                dE = E_rigid - E_relaxed
                t_elapsed = time.time() - t0
                reg_curve[d_key] = {
                    'E_rigid':     E_rigid,
                    'E_relaxed':   E_relaxed,
                    'dE':          dE,
                    'Wad_rigid':   Wad_rigid,
                    'Wad_relaxed': Wad_relaxed,
                    'n_steps':     n_steps,
                    'n_fixed':     n_fixed,
                    'n_total':     len(stacked),
                    'area_A2':     A,
                    't_sec':       t_elapsed,
                }
                log(f"    d={d:>4.2f}  E_rig={E_rigid:.3f}  E_rlx={E_relaxed:.3f}  "
                    f"ΔE={dE:+.3f}  Wad_rig={Wad_rigid:+.3f}  Wad_rlx={Wad_relaxed:+.3f}  "
                    f"n={n_steps}  t={t_elapsed:.1f}s")
                gc.collect()

            comp_out['curves'][reg_name] = {'shift': list(shift), 'curve': reg_curve}

        # Summary: mean over registries per gap
        comp_out['gaps'] = D_VALUES
        means_rigid, means_relax = [], []
        for d in D_VALUES:
            dk = f"{d:.3f}"
            wr = [reg['curve'][dk]['Wad_rigid']
                  for reg in comp_out['curves'].values()]
            wl = [reg['curve'][dk]['Wad_relaxed']
                  for reg in comp_out['curves'].values()]
            means_rigid.append(float(np.mean(wr)))
            means_relax.append(float(np.mean(wl)))
        comp_out['Wad_rigid_mean']   = means_rigid
        comp_out['Wad_relaxed_mean'] = means_relax

        # well & asymp
        wr = np.array(means_rigid); wl = np.array(means_relax)
        log(f"  ─── {c} summary ───")
        log(f"     Wad_rigid    max={np.max(wr):+.3f}  asymp={wr[-1]:+.3f}")
        log(f"     Wad_relaxed  max={np.max(wl):+.3f}  asymp={wl[-1]:+.3f}")
        log(f"     ΔWad (relax effect at well) = {np.max(wl) - np.max(wr):+.3f} J/m²")

        json.dump(comp_out, open(OUT / f"{c}_done.json", 'w'), indent=2)
        log(f"  saved {c}_done.json")

    log(f"\nTOTAL: {(time.time() - t_global) / 60:.1f} min")
    log(f"Results in: {OUT}")


if __name__ == "__main__":
    main()
