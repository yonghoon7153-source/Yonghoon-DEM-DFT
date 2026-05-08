"""Phase 2a v31 — re-run MLIP 600K snapshot elastic for comp1/comp2/modelC v2.

Uses snapshot_elastic function copied VERBATIM from
  /scratch/x3430a02/kgy/manuscript_support/mlip_elastic_snapshot_v2.py
to avoid import side-effects (the original .py runs comp2B/comp5 loop on
import). Function body is byte-identical; only the comp loop is replaced.

v2 anneal champion structures from STRUCTURE_PATHS.md:
- comp1_v2:  post_relax_comp1_v2/comp1v2_scf.out (espresso-out)
- comp2_v2:  pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz (extxyz)
- modelC_v2: pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz

Run on KISTI from anywhere (no path dependency now):
  conda activate mace
  cd /scratch/x3430a02/kgy/manuscript_support
  wget -O phase2a_v31_mlip_elastic_v2_3comp.py 'https://raw.../phase2a_v31_mlip_elastic_v2_3comp.py'
  mkdir -p phase2a_v31_results
  nohup python3 phase2a_v31_mlip_elastic_v2_3comp.py > phase2a_v31_results/run.log 2>&1 &
"""
import sys, os, time, json, traceback
from pathlib import Path
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from ase import units
from ase.io import read
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import BFGS
from mace.calculators import mace_mp


# ────────────────────── Calculator ──────────────────────
calc = mace_mp(model="large", device="cuda:0", default_dtype="float64")


# ────────────────────── snapshot_elastic (copied from mlip_elastic_snapshot_v2.py) ──
def snapshot_elastic(atoms, name, T=600, n_snapshots=5, equil_steps=3000,
                     interval=1000, delta=0.005):
    print(f"\n--- {name} ({len(atoms)} atoms) ---")
    atoms.calc = calc
    MaxwellBoltzmannDistribution(atoms, temperature_K=T)
    dyn = Langevin(atoms, timestep=2.0*units.fs, temperature_K=T, friction=0.01)
    print(f"  Equilibrating at {T}K ({equil_steps*2/1000:.1f} ps)...", flush=True)
    dyn.run(equil_steps)

    all_results = []
    for snap in range(n_snapshots):
        dyn.run(interval)
        snapshot = atoms.copy()
        snapshot.calc = calc

        opt = BFGS(snapshot, logfile=None)
        opt.run(fmax=0.05)

        cell0 = snapshot.get_cell().copy()
        # FIXED shear strain: d/2 each off-diagonal so Voigt ε_4 = d (correct).
        # Original v2 script used full d each → ε_4 = 2d → C44 inflated 2x.
        # Verified against older mlip_snapshot_elastic.py for comps 1-4 paper #1 v1.
        strains = np.zeros((6, 3, 3))
        strains[0] = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        strains[1] = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        strains[2] = [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        strains[3] = [[0, 0, 0], [0, 0, 0.5], [0, 0.5, 0]]   # yz: d/2 each
        strains[4] = [[0, 0, 0.5], [0, 0, 0], [0.5, 0, 0]]   # xz: d/2 each
        strains[5] = [[0, 0.5, 0], [0.5, 0, 0], [0, 0, 0]]   # xy: d/2 each

        C = np.zeros((6, 6))
        for i in range(6):
            for sign in [+1, -1]:
                eps = np.eye(3) + sign * delta * strains[i]
                s = snapshot.copy()
                s.set_cell(cell0 @ eps, scale_atoms=True)
                s.calc = calc
                stress = s.get_stress(voigt=True)
                if sign == +1:
                    sp = stress
                else:
                    sm = stress
            for j in range(6):
                C[j, i] = (sp[j] - sm[j]) / (2 * delta)

        C *= 160.2176634
        C = (C + C.T) / 2
        C11 = (C[0, 0] + C[1, 1] + C[2, 2]) / 3
        C12 = (C[0, 1] + C[0, 2] + C[1, 2]) / 3
        C44 = (C[3, 3] + C[4, 4] + C[5, 5]) / 3
        K = (C11 + 2 * C12) / 3
        G = (C11 - C12 + 3 * C44) / 5
        E = 9 * K * G / (3 * K + G) if (3 * K + G) != 0 else 0

        print(f"    snap {snap+1}: C11={C11:.1f}, C12={C12:.1f}, "
              f"C44={C44:.1f}, E={E:.1f}", flush=True)
        all_results.append([C11, C12, C44, K, G, E])

    arr = np.array(all_results)
    avg = np.mean(arr, axis=0)
    std = np.std(arr, axis=0)
    print(f"  AVG: C11={avg[0]:.1f}±{std[0]:.1f}, C12={avg[1]:.1f}±{std[1]:.1f}, "
          f"C44={avg[2]:.1f}±{std[2]:.1f}")
    print(f"       K={avg[3]:.1f}±{std[3]:.1f}, G={avg[4]:.1f}±{std[4]:.1f}, "
          f"E={avg[5]:.1f}±{std[5]:.1f}", flush=True)
    return avg, std


# ────────────────────── v31 wrapper main ──────────────────────
COMPS = [
    ("comp1_v2",
     "/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_scf.out",
     'espresso-out'),
    ("comp2_v2",
     "/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz",
     'extxyz'),
    ("modelC_v2",
     "/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz",
     'extxyz'),
]

RESULTS_DIR = Path("phase2a_v31_results")
RESULTS_DIR.mkdir(exist_ok=True)
LOG = RESULTS_DIR / "run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


def load_atoms(path, fmt):
    if fmt == 'espresso-out':
        return read(path, format='espresso-out', index=-1)
    elif fmt == 'extxyz':
        try:
            return read(path, format='extxyz')
        except Exception:
            return read(path)
    return read(path)


def main():
    t0 = time.time()
    log("=" * 70)
    log("v31 — MLIP 600K snapshot elastic (v2 anneal champions)")
    log("=" * 70)
    log("Method: 600K Langevin 6 ps + 5 snapshots × 2 ps + BFGS quench + "
        "finite-strain Cij (delta=0.005)")
    log(f"Calculator: {calc}")

    summary = {}
    for name, path, fmt in COMPS:
        log(f"\n========= {name} =========")
        log(f"  source: {path}")
        log(f"  format: {fmt}")
        try:
            if not Path(path).exists():
                raise FileNotFoundError(f"Source path not found: {path}")
            atoms = load_atoms(path, fmt)
            log(f"  loaded: {len(atoms)} atoms, "
                f"V={atoms.get_volume():.2f} A^3, "
                f"formula={atoms.get_chemical_formula()}")

            t_e = time.time()
            avg, std = snapshot_elastic(atoms, name)
            elapsed = time.time() - t_e
            log(f"  done in {elapsed/60:.1f} min")

            summary[name] = {
                "source_path": path,
                "format": fmt,
                "n_atoms": len(atoms),
                "C11": float(avg[0]), "C11_std": float(std[0]),
                "C12": float(avg[1]), "C12_std": float(std[1]),
                "C44": float(avg[2]), "C44_std": float(std[2]),
                "K":   float(avg[3]), "K_std":   float(std[3]),
                "G":   float(avg[4]), "G_std":   float(std[4]),
                "E":   float(avg[5]), "E_std":   float(std[5]),
                "elapsed_min": elapsed/60,
            }
        except Exception as e:
            log(f"  FAILED: {e}")
            traceback.print_exc(file=sys.stdout)
            summary[name] = {"error": str(e)}

    # ─────────────────────── final comparison ───────────────────────
    log("\n" + "=" * 70)
    log("v31 v2 vs db/elastic.json mlip_600K_snapshot (v1 baseline)")
    log("=" * 70)
    db_v1 = {
        "comp1_v2":  {"v1_E": 29.1, "v1_C44": 13.1, "v1_K": 21.0, "v1_G": 11.5},
        "comp2_v2":  {"v1_E": 28.6, "v1_C44": 12.7, "v1_K": 21.2, "v1_G": 11.2,
                      "v2_existing_E": 34.7, "v2_existing_C44": 13.7},
        "modelC_v2": {"v1_E": 32.9, "v1_C44": 12.9, "v1_K": 23.4, "v1_G": 13.0},
    }
    log(f"{'comp':<12} {'E (v1)':>8} {'E (v2 new)':>10} {'ΔE':>8} "
        f"{'C44 (v1)':>10} {'C44 (v2)':>10} {'ΔC44':>8}")
    for name, _, _ in COMPS:
        s = summary.get(name, {})
        d = db_v1.get(name, {})
        if 'error' in s:
            log(f"  {name}: ERROR {s['error']}")
            continue
        e_v1 = d.get('v1_E', 0)
        e_v2 = s.get('E', 0)
        de = e_v2 - e_v1
        c44_v1 = d.get('v1_C44', 0)
        c44_v2 = s.get('C44', 0)
        dc44 = c44_v2 - c44_v1
        log(f"  {name:<12} {e_v1:>8.1f} {e_v2:>10.1f} {de:>+8.1f} "
            f"{c44_v1:>10.1f} {c44_v2:>10.1f} {dc44:>+8.1f}")

    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)
    log(f"\n=== v31 DONE: total {(time.time()-t0)/60:.1f} min ===")


if __name__ == "__main__":
    main()
