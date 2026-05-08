"""Phase 2a v31 — re-run MLIP 600K snapshot elastic for comp1/comp2/modelC v2.

Uses VERIFIED snapshot_elastic function from existing
  /scratch/x3430a02/kgy/manuscript_support/mlip_elastic_snapshot_v2.py
with v2 anneal champion structures from STRUCTURE_PATHS.md.

Why: db/properties/elastic.json mlip_600K_snapshot used v1 data for comp1
(E=29.1), comp2 v1 (E=28.6), modelc v1 (E=32.9). comp2 already has v2
(E=34.7) showing +21% stiffer post-anneal. comp1, modelC need same v2
recalculation for paper #1 internal consistency.

Run on KISTI:
  conda activate mace
  cd /scratch/x3430a02/kgy/manuscript_support
  wget -O phase2a_v31_mlip_elastic_v2_3comp.py 'https://raw.../phase2a_v31_mlip_elastic_v2_3comp.py'
  python3 phase2a_v31_mlip_elastic_v2_3comp.py 2>&1 | tee phase2a_v31_results/run.log

Time: ~30 min (3 comps × 5 snapshots × elastic).

Note: This script must be run from /scratch/x3430a02/kgy/manuscript_support/
because it imports from the local mlip_elastic_snapshot_v2.py.
"""
import sys, os, time, json, traceback
from pathlib import Path
import numpy as np
from ase.io import read

# Import the verified function from existing script
sys.path.insert(0, '/scratch/x3430a02/kgy/manuscript_support')
try:
    from mlip_elastic_snapshot_v2 import snapshot_elastic, calc
except ImportError as e:
    print(f"FATAL: cannot import mlip_elastic_snapshot_v2: {e}")
    print("Run this script FROM /scratch/x3430a02/kgy/manuscript_support/")
    sys.exit(1)


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
    """Load atoms from QE .out or xyz."""
    if fmt == 'espresso-out':
        # Get last frame (V0 = relaxed)
        atoms = read(path, format='espresso-out', index=-1)
    elif fmt == 'extxyz':
        # Try extxyz first (has cell info), fallback to xyz
        try:
            atoms = read(path, format='extxyz')
        except Exception:
            atoms = read(path)
    else:
        atoms = read(path)
    return atoms


def main():
    t0 = time.time()
    log("=" * 70)
    log("v31 — MLIP 600K snapshot elastic (v2 anneal champions)")
    log("=" * 70)
    log(f"Imported snapshot_elastic from /scratch/x3430a02/kgy/manuscript_support/mlip_elastic_snapshot_v2.py")
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
                f"cell volume {atoms.get_volume():.2f} A^3, "
                f"composition {atoms.get_chemical_formula()}")

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
    log("v31 v2 vs db/elastic.json mlip_600K_snapshot (v1)")
    log("=" * 70)
    db_v1 = {
        "comp1_v2":  {"v1_E": 29.1, "v1_C44": 13.1, "v1_K": 21.0, "v1_G": 11.5},
        "comp2_v2":  {"v1_E": 28.6, "v1_C44": 12.7, "v1_K": 21.2, "v1_G": 11.2,
                      "v2_existing_E": 34.7},  # already in db/compositions/comp2.json
        "modelC_v2": {"v1_E": 32.9, "v1_C44": 12.9, "v1_K": 23.4, "v1_G": 13.0},
    }
    log(f"{'comp':<12} {'E (v1)':>8} {'E (v2)':>8} {'ΔE':>8} "
        f"{'C44 (v1)':>10} {'C44 (v2)':>10} {'ΔC44':>8}")
    for name, _, _ in COMPS:
        s = summary.get(name, {})
        d = db_v1.get(name, {})
        if 'error' in s:
            log(f"  {name}: ERROR {s['error']}")
            continue
        e_v1 = d.get('v1_E', 0); e_v2 = s.get('E', 0); de = e_v2 - e_v1
        c44_v1 = d.get('v1_C44', 0); c44_v2 = s.get('C44', 0); dc44 = c44_v2 - c44_v1
        log(f"  {name:<12} {e_v1:>8.1f} {e_v2:>8.1f} {de:>+8.1f} "
            f"{c44_v1:>10.1f} {c44_v2:>10.1f} {dc44:>+8.1f}")

    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)
    log(f"\n=== v31 DONE: total {(time.time()-t0)/60:.1f} min ===")


if __name__ == "__main__":
    main()
