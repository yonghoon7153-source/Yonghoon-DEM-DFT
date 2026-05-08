"""Phase 2a v30u — UMA Z-scan binding curve (mirror of v30 MACE but with UMA).

UMA gives PHYSICAL absolute values (W_max 0.31-1.49 J/m² matching experiment),
unlike MACE which gave -25 J/m² (unphysical scale). This script produces
the UMA binding curve for Origin plotting.

Identical method to v30 (Z-scan gap 0.5-6.0 Å, 0.25 step) but with UMA
calculator instead of MACE-MP-0.

Run on KISTI:
  conda activate uma
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -O phase2a_v30u_uma_zscan.py 'https://raw.../phase2a_v30u_uma_zscan.py'
  mkdir -p phase2a_v30u_results
  nohup python3 phase2a_v30u_uma_zscan.py > phase2a_v30u_results/run.log 2>&1 &

Time: ~5-10 min (similar to v30 MACE).
"""
import os, json, time, sys, traceback
from pathlib import Path
import numpy as np
from ase.io import read

COMPS = {
    'comp1':  {'se': 'comp1_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'se': 'comp2_slab_v2.xyz',            'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'se': 'comp4_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',  'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED.xyz', 'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

VACUUM_TOP = 30.0
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS = PAPER_COMPS + ['modelC']

GAP_MIN, GAP_MAX, GAP_STEP = 0.5, 6.0, 0.25

RESULTS_DIR = Path("phase2a_v30u_results"); RESULTS_DIR.mkdir(exist_ok=True)
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


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def get_uma_calc():
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(pred, task_name="omat")


def main():
    t0 = time.time()
    log("=" * 70)
    log(f"v30u — UMA Z-scan binding curves (gap {GAP_MIN}-{GAP_MAX} A, "
        f"step {GAP_STEP} A)")
    log("=" * 70)

    log("Loading UMA-s-1p1...")
    try:
        calc = get_uma_calc()
        log("  UMA loaded.")
    except Exception as e:
        log(f"  UMA FAILED: {e}")
        traceback.print_exc(file=sys.stdout)
        return

    gaps = np.arange(GAP_MIN, GAP_MAX + GAP_STEP/2, GAP_STEP)
    log(f"  Z-scan: {len(gaps)} gap points per comp")

    results = {}
    for c, cfg in COMPS.items():
        log(f"\n========= {c} =========")
        try:
            se = read(cfg['se'])
            ncm = read(cfg['ncm'])

            t_iso = time.time()
            se_iso = se.copy(); se_iso.calc = calc
            E_se = float(se_iso.get_potential_energy())
            ncm_iso = ncm.copy(); ncm_iso.calc = calc
            E_ncm = float(ncm_iso.get_potential_energy())
            log(f"  E_se_iso = {E_se:.4f} eV, E_ncm_iso = {E_ncm:.4f} eV "
                f"({time.time()-t_iso:.1f}s)")

            wad_curve = []
            t_scan = time.time()
            for gap in gaps:
                stacked, n_ncm = stack_rigid(se, ncm, gap)
                stacked.calc = calc
                E_int = float(stacked.get_potential_energy())
                A = xy_area(stacked.cell.array)
                wad = (E_se + E_ncm - E_int) / A * 16.0218
                wad_curve.append({'gap': float(gap), 'E_int': E_int, 'A': A, 'Wad': wad})
                if int(round(gap*4)) % 4 == 0:
                    log(f"    gap={gap:.2f}  E_int={E_int:+.4f}  Wad={wad:+.4f}")
            log(f"  Z-scan done ({time.time()-t_scan:.1f}s)")

            wads = np.array([x['Wad'] for x in wad_curve])
            i_max = int(np.argmax(wads))
            W_max = float(wads[i_max])
            d_min = float(gaps[i_max])
            log(f"  → W_max(UMA) = {W_max:+.4f} J/m^2 at d_min = {d_min:.2f} A")

            results[c] = {
                'wad_curve': wad_curve,
                'E_se_iso': E_se,
                'E_ncm_iso': E_ncm,
                'W_max_J_per_m2': W_max,
                'd_min_A': d_min,
            }
        except Exception as e:
            log(f"  {c} FAILED: {e}")
            traceback.print_exc(file=sys.stdout)
            results[c] = {'error': str(e)}

    log("\n" + "=" * 70)
    log("UMA Z-scan W_max per comp")
    log("=" * 70)
    log(f"{'comp':<8} {'paper':>6} {'W_max(J/m^2)':>14} {'d_min(A)':>10}")
    for c in ALL_COMPS:
        r = results.get(c, {})
        if 'error' in r:
            log(f"  {c}: ERROR {r['error']}")
            continue
        log(f"{c:<8} {PAPER_EXP.get(c, '?'):>6} "
            f"{r['W_max_J_per_m2']:>+14.4f} {r['d_min_A']:>10.2f}")

    if all(c in results and 'error' not in results[c] for c in PAPER_COMPS):
        x = [results[c]['W_max_J_per_m2'] for c in PAPER_COMPS]
        y = [PAPER_EXP[c] for c in PAPER_COMPS]
        R = pearson(x, y)
        log(f"\n  R(UMA W_max vs paper) = {R:+.4f}")
        log(f"\nCompare:")
        log(f"  v30u UMA Z-scan W_max:                R = {R:+.4f} (paper-scale 0.3-1.5 J/m^2)")
        log(f"  v30  MACE Z-scan W_max:               R = +0.957 (-25 J/m^2 unphysical)")
        log(f"  Phase 1 Method A UMA W_max (db):      R = +0.871")
        log(f"  v15 Cl-O density (geometric):         R = -0.914")

    log(f"\n=== v30u DONE: {(time.time()-t0)/60:.1f} min ===")
    json.dump(results, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)


if __name__ == "__main__":
    main()
