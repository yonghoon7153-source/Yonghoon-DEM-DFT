"""Run v30u UMA Z-scan using zshift-selected slabs (bulk v2 + v1-like surface).

Same protocol as 필독/adhesion/phase2a_v30u_uma_zscan.py but with SE slabs
swapped to the user-chosen zshift variant for each comp (best v1-like surface).

Default zshift picks (override via --override comp=N):
  comp1:  zshift0 (Cl=4, no Br alternative)
  comp2:  zshift2 (Br=8, Cl=0)        — v1-like
  comp4:  zshift1 (Br=4, Cl=0)        — v1-like, restored
  modelC: zshift1 (halogen-free)      — even cleaner than v1
  comp3:  uses original v1 slab (comp3_slab_v1_PRESERVED.xyz)
  comp5:  uses original v1 slab (comp5_slab_v1_PRESERVED.xyz)

Usage on KISTI:
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -q https://raw.githubusercontent.com/.../tools/run_v30u_zshift.py
  python3 run_v30u_zshift.py
  # results in v30u_zshift_results/summary.json + v30u_zshift_curves.json
"""
import os, json, time, sys, traceback, argparse
from pathlib import Path
import numpy as np
from ase.io import read

# Default slab choices — edit here or pass --override
COMPS = {
    'comp1':  {'se': 'comp1_slab_v2_zshifts/comp1_slab_v2_zshift0.xyz',
               'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'se': 'comp2_slab_v2_zshifts/comp2_slab_v2_zshift2.xyz',
               'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'se': 'comp3_slab_v1_PRESERVED.xyz',
               'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'se': 'comp4_slab_v2_PRESERVED_zshifts/comp4_slab_v2_PRESERVED_zshift1.xyz',
               'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'se': 'comp5_slab_v1_PRESERVED.xyz',
               'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'se': 'modelC_slab_v2_PRESERVED_zshifts/modelC_slab_v2_PRESERVED_zshift1.xyz',
               'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

VACUUM_TOP = 30.0
PAPER_EXP   = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS   = PAPER_COMPS + ['modelC']
GAP_MIN, GAP_MAX, GAP_STEP = 0.5, 6.0, 0.25

RESULTS_DIR = Path("v30u_zshift_results"); RESULTS_DIR.mkdir(exist_ok=True)
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--override', action='append', default=[],
                        help='override slab: comp=PATH (repeatable)')
    args = parser.parse_args()
    for ov in args.override:
        k, v = ov.split('=', 1)
        if k in COMPS:
            COMPS[k]['se'] = v
            print(f"override {k} se -> {v}")

    t0 = time.time()
    log("=" * 70)
    log(f"v30u zshift — UMA Z-scan binding curves (gap {GAP_MIN}-{GAP_MAX} A)")
    log("=" * 70)
    log("Slab choices:")
    for c, cfg in COMPS.items():
        log(f"  {c}: SE={cfg['se']}  NCM={cfg['ncm']}")

    log("\nLoading UMA-s-1p1...")
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
            if not Path(cfg['se']).exists():
                raise FileNotFoundError(f"SE slab not found: {cfg['se']}")
            if not Path(cfg['ncm']).exists():
                raise FileNotFoundError(f"NCM not found: {cfg['ncm']}")
            se = read(cfg['se']); ncm = read(cfg['ncm'])

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
                'slab_file': cfg['se'],
                'wad_curve': wad_curve,
                'E_se_iso': E_se,
                'E_ncm_iso': E_ncm,
                'W_max_J_per_m2': W_max,
                'd_min_A': d_min,
            }
        except Exception as e:
            log(f"  {c} FAILED: {e}")
            traceback.print_exc(file=sys.stdout)
            results[c] = {'error': str(e), 'slab_file': cfg['se']}

    log("\n" + "=" * 70)
    log("UMA zshift Z-scan W_max per comp")
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

    json.dump(results, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)
    # Also save in v30u_v2_curves.json compatible format for plot scripts
    curves = {c: [[w['gap'], w['Wad']] for w in r.get('wad_curve', [])]
              for c, r in results.items() if 'wad_curve' in r}
    json.dump(curves, open(RESULTS_DIR / "v30u_zshift_curves.json", 'w'), indent=2)
    log(f"\n=== DONE: {(time.time()-t0)/60:.1f} min ===")
    log(f"saved {RESULTS_DIR / 'summary.json'}")
    log(f"saved {RESULTS_DIR / 'v30u_zshift_curves.json'}")


if __name__ == "__main__":
    main()
