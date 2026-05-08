"""Phase 2a v31c — MLIP 600K snapshot elastic for comp1/comp2/modelC v2,
using VERIFIED elastic_0K_from_snapshot protocol from older mlip_snapshot_elastic.py.

v31 (b) had two bugs from copying mlip_elastic_snapshot_v2.py:
  bug 1: shear strain ε_4_Voigt = 2δ (should be δ) → C44 2x inflated
  bug 2: no ionic relax under strain (clamped-ion) → all Cij ~2x inflated
         vs relaxed-ion baseline (paper #1 v1 used relaxed-ion)

v31c uses the older VERIFIED protocol:
  - shear strain: eps[1,2]=eps[2,1]=d/2 (correct ε_4 = d)
  - per-strain ionic relax: LBFGS(fmax=0.01, steps=200) after each strain
  - sign flip + GPa convert: s = -a.get_stress(...)*160.2176634
  - cell transform: new_cell = cell0 @ (I+eps).T
  - scale_atoms=False + set_scaled_positions(pos0) (frozen fractional)

This matches paper #1 published v1 protocol exactly. v31c should reproduce
v1 baseline values (comp1 C11~33, E~29) for comp1_v2 if v2 anneal champion is
similar to v1, OR show modest +5-15% stiffening if anneal champion is more
ordered (post-anneal effect).

Run on KISTI (mace env, anywhere):
  conda activate mace
  cd /scratch/x3430a02/kgy/manuscript_support
  pkill -f phase2a_v31  # kill any old v31
  rm -rf phase2a_v31_results
  wget -O phase2a_v31_mlip_elastic_v2_3comp.py 'https://raw.../phase2a_v31_mlip_elastic_v2_3comp.py'
  mkdir phase2a_v31_results
  nohup python3 phase2a_v31_mlip_elastic_v2_3comp.py > phase2a_v31_results/run.log 2>&1 &

Time: ~60-90 min (3 comps × longer per snap due to per-strain LBFGS).
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
from ase.optimize import LBFGS, BFGS
from mace.calculators import mace_mp


# ────────────────────── Calculator ──────────────────────
calc = mace_mp(model="large", device="cuda:0", default_dtype="float64")


# ────────────────────── elastic_0K_from_snapshot (copied from older verified) ──
def elastic_0K_from_snapshot(atoms, delta=0.005):
    """Verified from /scratch/x3430a02/kgy/manuscript_support/mlip_snapshot_elastic.py
    (older mlip_snapshot_elastic.py with comp1-4 hardcoded). Used for paper #1 v1.

    Differences vs newer (buggy) snapshot_elastic:
      - shear strain: eps[i,j]=eps[j,i]=d/2 (correct ε_Voigt=d, not 2d)
      - per-strain ionic relax (relaxed-ion, not clamped-ion)
      - cell transform (I+eps).T (transposed) with scale_atoms=False + set_scaled_positions
      - stress sign flip
    """
    opt = LBFGS(atoms, logfile=None)
    opt.run(fmax=0.005, steps=500)
    cell0 = atoms.get_cell().copy()
    pos0 = atoms.get_scaled_positions().copy()
    C = np.zeros((6, 6))
    for vi in range(6):
        sp = sm = None
        for sign in [+1, -1]:
            d = sign * delta
            eps = np.zeros((3, 3))
            if vi == 0:
                eps[0, 0] = d
            elif vi == 1:
                eps[1, 1] = d
            elif vi == 2:
                eps[2, 2] = d
            elif vi == 3:
                eps[1, 2] = eps[2, 1] = d / 2
            elif vi == 4:
                eps[0, 2] = eps[2, 0] = d / 2
            elif vi == 5:
                eps[0, 1] = eps[1, 0] = d / 2
            new_cell = cell0 @ (np.eye(3) + eps).T
            a = atoms.copy()
            a.calc = calc
            a.set_cell(new_cell, scale_atoms=False)
            a.set_scaled_positions(pos0)
            LBFGS(a, logfile=None).run(fmax=0.01, steps=200)
            s = -a.get_stress(voigt=True) * 160.2176634
            if sign > 0:
                sp = list(s)
            else:
                sm = list(s)
        for sj in range(6):
            C[sj, vi] = (sp[sj] - sm[sj]) / (2 * delta)
    C = (C + C.T) / 2
    C11 = (C[0, 0] + C[1, 1] + C[2, 2]) / 3
    C12 = (C[0, 1] + C[0, 2] + C[1, 2]) / 3
    C44 = (C[3, 3] + C[4, 4] + C[5, 5]) / 3
    K = (C11 + 2 * C12) / 3
    G = (C11 - C12 + 3 * C44) / 5
    E = 9 * K * G / (3 * K + G) if (3 * K + G) != 0 else 0
    return {"C11": C11, "C12": C12, "C44": C44, "K": K, "G": G, "E": E}


# ────────────────────── md_then_snapshot_elastic (older verified) ──
def md_then_snapshot_elastic(atoms, name, T=600, md_steps=5000,
                              n_snapshots=5, interval=1000):
    print(f"\n{'='*60}", flush=True)
    print(f"  {name} - MD({T}K) -> {n_snapshots} snapshots -> 0K elastic", flush=True)
    print(f"{'='*60}", flush=True)
    atoms.calc = calc
    MaxwellBoltzmannDistribution(atoms, temperature_K=T)
    dyn = Langevin(atoms, timestep=2.0*units.fs, temperature_K=T, friction=0.01)
    print(f"  Equilibrating at {T}K ({md_steps*2/1000:.1f} ps)...", flush=True)
    dyn.run(md_steps)

    results = []
    for snap in range(n_snapshots):
        dyn.run(interval)
        snapshot = atoms.copy()
        snapshot.calc = calc
        result = elastic_0K_from_snapshot(snapshot, delta=0.005)
        print(f"    snap {snap+1}: C11={result['C11']:.1f}, "
              f"C12={result['C12']:.1f}, C44={result['C44']:.1f}, "
              f"E={result['E']:.1f}", flush=True)
        results.append(result)

    avg = {}
    for key in ["C11", "C12", "C44", "K", "G", "E"]:
        vals = [r[key] for r in results]
        avg[key] = float(np.mean(vals))
        avg[f"{key}_std"] = float(np.std(vals))
    print(f"\n  === {name} Average ===")
    for key in ["C11", "C12", "C44", "K", "G", "E"]:
        print(f"  {key}={avg[key]:.1f}+/-{avg[f'{key}_std']:.1f}", flush=True)
    return avg


# ────────────────────── v31c wrapper main ──────────────────────
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
    log("v31c — MLIP 600K snapshot elastic (v2 anneal champions)")
    log("=" * 70)
    log("Method: 600K Langevin 10 ps + 5 snapshots × 2 ps + LBFGS quench + ")
    log("        per-strain LBFGS ionic relax + finite-strain Cij (delta=0.005)")
    log("Protocol: VERIFIED from older mlip_snapshot_elastic.py (paper #1 v1 published)")

    summary = {}
    for name, path, fmt in COMPS:
        log(f"\n========= {name} =========")
        log(f"  source: {path}")
        try:
            if not Path(path).exists():
                raise FileNotFoundError(f"Source path not found: {path}")
            atoms = load_atoms(path, fmt)
            log(f"  loaded: {len(atoms)} atoms, "
                f"V={atoms.get_volume():.2f} A^3, "
                f"formula={atoms.get_chemical_formula()}")

            t_e = time.time()
            avg = md_then_snapshot_elastic(atoms, name, T=600, md_steps=5000,
                                            n_snapshots=5, interval=1000)
            elapsed = time.time() - t_e
            log(f"  done in {elapsed/60:.1f} min")

            summary[name] = {
                "source_path": path,
                "format": fmt,
                "n_atoms": len(atoms),
                **avg,
                "elapsed_min": elapsed/60,
            }
        except Exception as e:
            log(f"  FAILED: {e}")
            traceback.print_exc(file=sys.stdout)
            summary[name] = {"error": str(e)}

    # ─────────────────────── final comparison ───────────────────────
    log("\n" + "=" * 70)
    log("v31c v2 vs db/elastic.json mlip_600K_snapshot (v1 baseline, paper #1 published)")
    log("=" * 70)
    db_v1 = {
        "comp1_v2":  {"v1_E": 29.1, "v1_C44": 13.1, "v1_K": 21.0, "v1_G": 11.5,
                      "v1_C11": 33.1, "v1_C12": 15.0},
        "comp2_v2":  {"v1_E": 28.6, "v1_C44": 12.7, "v1_K": 21.2, "v1_G": 11.2,
                      "v1_C11": 33.1, "v1_C12": 15.2,
                      "existing_v2_E": 34.7, "existing_v2_C44": 13.7,
                      "existing_v2_C11": 44.1},
        "modelC_v2": {"v1_E": 32.9, "v1_C44": 12.9, "v1_K": 23.4, "v1_G": 13.0,
                      "v1_C11": 39.3, "v1_C12": 15.4},
    }
    log(f"{'comp':<12} {'E v1':>7} {'E v2c':>7} {'ΔE':>7} "
        f"{'C44 v1':>8} {'C44 v2c':>8} {'C11 v1':>8} {'C11 v2c':>8}")
    for name, _, _ in COMPS:
        s = summary.get(name, {})
        d = db_v1.get(name, {})
        if 'error' in s:
            log(f"  {name}: ERROR {s['error']}")
            continue
        e_v1 = d.get('v1_E', 0); e_v2 = s.get('E', 0); de = e_v2 - e_v1
        c44_v1 = d.get('v1_C44', 0); c44_v2 = s.get('C44', 0)
        c11_v1 = d.get('v1_C11', 0); c11_v2 = s.get('C11', 0)
        log(f"  {name:<12} {e_v1:>7.1f} {e_v2:>7.1f} {de:>+7.1f} "
            f"{c44_v1:>8.1f} {c44_v2:>8.1f} {c11_v1:>8.1f} {c11_v2:>8.1f}")

    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)
    log(f"\n=== v31c DONE: total {(time.time()-t0)/60:.1f} min ===")


if __name__ == "__main__":
    main()
