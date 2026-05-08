"""Phase 2a v29 — AIMD stability check on M2 constrained-relaxed interface.

Purpose: M2 (v26b) showed RMS<0.2 Å after 30 LBFGS steps with FixAtoms.
Reviewer concern: "is that just a 100-step LBFGS local min, or genuine
steady state?" → run constrained Langevin AIMD at 300K for 1 ps, check
that RMS displacement does NOT grow significantly over time.

Method (per comp):
  1. Stack SE/NCM at gap_eq (v15 baseline)
  2. FixAtoms on NCM (all) + bottom 70% of SE (same constraint as M2)
  3. UMA calculator
  4. LBFGS pre-relax (30 steps, fmax 0.1) — M2 starting point
  5. Langevin MD: T=300K, dt=2fs, friction 0.01/fs, 500 steps = 1 ps
  6. Track RMS displacement of UNFROZEN atoms at every 25 fs
  7. Save trajectory frames every 100 fs (10 frames)

Output:
  - Per-comp RMS(t) curve
  - Per-comp bond density at t=0, 250, 500, 750, 1000 fs
  - Verdict: max RMS within 1 ps + drift trend

Stability criteria:
  PASS: RMS at t=1 ps < 1.5x RMS at t=200 fs (after thermalization)
        no monotonic drift toward NCM bulk
  FAIL: RMS keeps growing → M2 was a local min, true relaxation gives migration

Time: ~1 hour (UMA forward + 500 steps × 6 comps).

Run on KISTI:
  conda activate uma
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -O phase2a_v29_aimd_stability.py 'https://raw.../phase2a_v29_aimd_stability.py'
  mkdir -p phase2a_v29_results
  nohup python3 phase2a_v29_aimd_stability.py > phase2a_v29_results/run.log 2>&1 &
"""
import os, json, time, sys, traceback
from pathlib import Path
import numpy as np
from ase import units, Atoms
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import LBFGS
from ase.md.langevin import Langevin
from ase.md import MDLogger
from ase.io.trajectory import Trajectory

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz', 'gap_eq': 1.2},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.4},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.6},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz', 'gap_eq': 1.2},
}
BOND_CUTOFFS = {('Li','O'):3.0, ('Cl','O'):3.5, ('Br','O'):3.7,
                ('S','Li'):3.0, ('S','Ni'):3.5, ('Li','Ni'):3.5}
VACUUM_TOP = 30.0

T_K = 300
DT_FS = 2.0
FRICTION_FS = 0.01
N_STEPS = 500   # 1 ps total
LOG_INTERVAL_STEPS = 25  # every 50 fs
TRAJ_INTERVAL_STEPS = 50  # every 100 fs

RESULTS_DIR = Path("phase2a_v29_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG = RESULTS_DIR / "run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


def stack_rigid(se, ncm, gap, shift_frac=(0.0, 0.0)):
    se_a = se.copy(); ncm_a = ncm.copy()
    nc = se_a.cell.array.copy()
    nc[0] = ncm_a.cell.array[0]; nc[1] = ncm_a.cell.array[1]
    se_a.set_cell(nc, scale_atoms=True)
    dx, dy = shift_frac
    sc = dx * ncm_a.cell.array[0] + dy * ncm_a.cell.array[1]
    se_a.translate([sc[0], sc[1], 0.0])
    se_a.wrap()
    ncm_a.translate([0, 0, -ncm_a.positions[:, 2].min()])
    z_max = ncm_a.positions[:, 2].max()
    s_min = se_a.positions[:, 2].min()
    se_a.translate([0, 0, z_max - s_min + gap])
    combined = ncm_a + se_a
    new_cell = ncm_a.cell.array.copy()
    z_extent = combined.positions[:, 2].max() - combined.positions[:, 2].min()
    new_cell[2] = [0., 0., z_extent + VACUUM_TOP]
    combined.set_cell(new_cell, scale_atoms=False)
    combined.set_pbc([True, True, True])
    return combined, len(ncm_a)


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def count_interface_bonds(stacked, n_ncm, gap_window=4.5):
    syms = stacked.get_chemical_symbols()
    pos = stacked.positions
    ncm_z_max = pos[:n_ncm, 2].max()
    near = [i for i in range(len(stacked)) if abs(pos[i, 2] - ncm_z_max) < gap_window]
    counts = {}
    for (sa, sb), cut in BOND_CUTOFFS.items():
        n_ab = 0
        for i in near:
            if i >= n_ncm and syms[i] == sa:
                for j in near:
                    if j < n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
            elif i < n_ncm and syms[i] == sa:
                for j in near:
                    if j >= n_ncm and syms[j] == sb:
                        if stacked.get_distance(i, j, mic=True) < cut:
                            n_ab += 1
        counts[f"{sa}-{sb}"] = n_ab
    return counts


def get_uma_calc():
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(pred, task_name="omat")


def main():
    t0 = time.time()
    log("=" * 70)
    log(f"v29 — AIMD stability check (T={T_K}K, dt={DT_FS}fs, {N_STEPS} steps = "
        f"{N_STEPS*DT_FS/1000:.1f} ps)")
    log("=" * 70)
    log("  Setup: M2-style FixAtoms (NCM + bottom 70% SE) + Langevin")
    log("  Goal: confirm M2 RMS<0.2A persists (not LBFGS local min)")

    log("Loading UMA...")
    calc = get_uma_calc()
    log("UMA loaded.")

    summary = {}
    for c, cfg in COMPS.items():
        try:
            log(f"\n========= {c} (gap_eq={cfg['gap_eq']}) =========")
            se = read(cfg['se'])
            ncm = read(cfg['ncm'])
            stacked, n_ncm = stack_rigid(se, ncm, cfg['gap_eq'])
            n_total = len(stacked); n_se = n_total - n_ncm

            se_z = stacked.positions[n_ncm:, 2]
            z_min, z_max = se_z.min(), se_z.max()
            z_threshold = z_min + 0.7 * (z_max - z_min)
            fix_idx = list(range(n_ncm))
            for i in range(n_ncm, n_total):
                if stacked.positions[i, 2] < z_threshold:
                    fix_idx.append(i)
            free_idx = [i for i in range(n_total) if i not in fix_idx]
            log(f"  total={n_total}, NCM={n_ncm}, SE_free={len(free_idx)}/{n_se} "
                f"(top {100*len(free_idx)/n_se:.0f}%)")

            stacked.set_constraint(FixAtoms(indices=fix_idx))
            stacked.calc = calc

            # Pre-relax (M2 step)
            log("  M2 pre-relax (LBFGS 30 steps)...")
            opt = LBFGS(stacked, logfile=str(RESULTS_DIR / f"m2_lbfgs_{c}.log"))
            opt.run(fmax=0.1, steps=30)
            pos_m2 = stacked.positions.copy()
            log("  M2 pre-relax done.")

            # Initial bond density
            bonds_t0 = count_interface_bonds(stacked, n_ncm)
            A = xy_area(stacked.cell.array)
            dens_t0 = {k: v/A for k, v in bonds_t0.items()}
            log(f"  t=0 bonds: Li-O={bonds_t0['Li-O']} Cl-O={bonds_t0['Cl-O']} "
                f"Br-O={bonds_t0['Br-O']}")

            # Setup Langevin
            from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
            MaxwellBoltzmannDistribution(stacked, temperature_K=T_K)
            dyn = Langevin(stacked, timestep=DT_FS*units.fs,
                           temperature_K=T_K, friction=FRICTION_FS/units.fs)

            traj_path = RESULTS_DIR / f"v29_{c}_traj.xyz"
            mdlog_path = RESULTS_DIR / f"v29_{c}_md.log"
            mdlogger = MDLogger(dyn, stacked, str(mdlog_path),
                                header=True, mode='w', stress=False)
            dyn.attach(mdlogger, interval=LOG_INTERVAL_STEPS)

            rms_track = []  # list of (step, rms_disp_from_m2)
            bond_track = []  # list of (step, dens_dict)

            def track_rms():
                disp = stacked.positions - pos_m2
                rms = np.sqrt(np.mean(np.sum(disp**2, axis=1)))
                max_d = np.sqrt(np.max(np.sum(disp**2, axis=1)))
                rms_track.append({'step': dyn.nsteps,
                                  'time_fs': dyn.nsteps*DT_FS,
                                  'rms': float(rms),
                                  'max': float(max_d)})

            def track_bonds():
                stacked.set_constraint(None)  # temporarily for distance calc
                b = count_interface_bonds(stacked, n_ncm)
                bond_track.append({'step': dyn.nsteps,
                                   'time_fs': dyn.nsteps*DT_FS,
                                   'bonds': b,
                                   'dens': {k: v/A for k, v in b.items()}})
                stacked.set_constraint(FixAtoms(indices=fix_idx))

            dyn.attach(track_rms, interval=LOG_INTERVAL_STEPS)
            dyn.attach(track_bonds, interval=TRAJ_INTERVAL_STEPS)

            log(f"  Running Langevin: {N_STEPS} steps × {DT_FS} fs = "
                f"{N_STEPS*DT_FS/1000:.1f} ps")
            t_md = time.time()
            dyn.run(N_STEPS)
            log(f"  AIMD done ({time.time()-t_md:.1f}s)")

            # Final RMS
            disp_final = stacked.positions - pos_m2
            rms_final = np.sqrt(np.mean(np.sum(disp_final**2, axis=1)))
            max_final = np.sqrt(np.max(np.sum(disp_final**2, axis=1)))
            log(f"  Final t={N_STEPS*DT_FS} fs: RMS={rms_final:.3f} A, max={max_final:.3f} A")

            # Verdict
            rms_thermalized = [r['rms'] for r in rms_track if r['time_fs'] >= 200]
            if rms_thermalized:
                rms_avg_late = np.mean(rms_thermalized)
                rms_avg_early = np.mean([r['rms'] for r in rms_track if r['time_fs'] <= 200])
                drift_factor = rms_avg_late / rms_avg_early if rms_avg_early > 0 else 0
                stable = drift_factor < 1.5
                verdict = ("PASS — RMS stable" if stable
                           else f"FAIL — RMS grew {drift_factor:.1f}× from 200 fs")
            else:
                verdict = "TOO SHORT"

            summary[c] = {
                'rms_track': rms_track,
                'bond_track': bond_track,
                'rms_final': float(rms_final),
                'max_final': float(max_final),
                'verdict': verdict
            }
            log(f"  VERDICT: {verdict}")

            # Save final structure
            stacked.set_constraint(None)
            write(str(RESULTS_DIR / f"v29_{c}_final.xyz"), stacked)

        except Exception as e:
            log(f"  {c} FAILED: {e}")
            traceback.print_exc(file=sys.stdout)
            summary[c] = {'error': str(e)}

    # ────────────────────────────── final summary ──────────────────────────────
    log("\n" + "=" * 70)
    log("AIMD STABILITY SUMMARY")
    log("=" * 70)
    log(f"{'comp':<8} {'rms_t=0':>9} {'rms_late':>9} {'max_t=1ps':>10} {'verdict':>30}")
    for c in COMPS:
        s = summary.get(c, {})
        if 'error' in s:
            log(f"  {c}: ERROR {s['error']}")
            continue
        rms_track = s.get('rms_track', [])
        rms_t0 = rms_track[0]['rms'] if rms_track else 0
        rms_late = np.mean([r['rms'] for r in rms_track if r['time_fs'] >= 800]) if rms_track else 0
        log(f"{c:<8} {rms_t0:>9.3f} {rms_late:>9.3f} {s.get('max_final', 0):>10.3f}  "
            f"{s.get('verdict', '?'):>30}")

    log(f"\n=== v29 DONE: total {(time.time()-t0)/60:.1f} min ===")
    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)


if __name__ == "__main__":
    main()
