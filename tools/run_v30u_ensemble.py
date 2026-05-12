"""Ensemble UMA binding curves — 5 z-shifts × 6 comps + mean ± std.

Honest methodology (vs cherry-picking single z-shift):
  - For each comp, generate 5 z-shifted slab variants (if not already done)
  - Run UMA Z-scan on each variant (rigid stack, gap 0.5-6.0 A)
  - Aggregate per (comp, gap): mean Wad + std across 5 z-shifts
  - Output: ensemble_summary.json (per-zshift detail + aggregate)
  -         v30u_ensemble_curves.json (gap × comp × {mean, std} for plotting)

Rationale: synthesis-frozen surface termination is uncertain → average over
plausible terminations. Std at each gap = surface-chemistry sensitivity →
itself a paper-message (Li5.4 family expected to show larger std = vacancy
chemical anchor mechanism evidence).

Usage on KISTI:
  cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
  wget -q https://raw.githubusercontent.com/.../tools/zshift_slab_variants.py
  wget -q https://raw.githubusercontent.com/.../tools/run_v30u_ensemble.py
  # auto-generates zshift variants if missing
  python3 run_v30u_ensemble.py
"""
import os, json, time, sys, traceback, subprocess
from pathlib import Path
import numpy as np
from ase.io import read

# Source slabs (will be z-shifted)
COMPS = {
    'comp1':  {'src': 'comp1_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'src': 'comp2_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'src': 'comp3_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'src': 'comp4_slab_v2_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'src': 'comp5_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'src': 'modelC_slab_v2_PRESERVED.xyz',       'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

VACUUM_TOP = 30.0
N_SHIFTS = 5
PAPER_EXP   = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
ALL_COMPS   = PAPER_COMPS + ['modelC']
GAP_MIN, GAP_MAX, GAP_STEP = 0.5, 6.0, 0.25

RESULTS_DIR = Path("v30u_ensemble_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG = RESULTS_DIR / "run.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


def ensure_zshifts(comp, src_xyz):
    """Generate zshift variants if not already present. Returns list of N_SHIFTS xyz paths."""
    src = Path(src_xyz)
    out_dir = src.parent / (src.stem + "_zshifts")
    variants = [out_dir / f"{src.stem}_zshift{i}.xyz" for i in range(N_SHIFTS)]
    if all(v.exists() for v in variants):
        log(f"  {comp}: zshift variants already present in {out_dir}")
        return variants
    log(f"  {comp}: generating zshift variants...")
    out_dir.mkdir(parents=True, exist_ok=True)
    atoms = read(src)
    cz = atoms.cell.lengths()[2]
    for i in range(N_SHIFTS):
        frac = i / N_SHIFTS
        a = atoms.copy()
        pos = a.positions.copy()
        pos[:, 2] = (pos[:, 2] + frac * cz) % cz
        a.set_positions(pos)
        from ase.io import write
        write(variants[i], a)
    return variants


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
    return combined


def xy_area(cell):
    return float(abs(np.cross(cell[0], cell[1])[2]))


def get_uma_calc():
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda")
    return FAIRChemCalculator(pred, task_name="omat")


def scan_one_slab(se, ncm, calc, gaps):
    """Run gap Z-scan on one (SE, NCM) pair, return list of Wad per gap."""
    se_iso = se.copy(); se_iso.calc = calc
    E_se = float(se_iso.get_potential_energy())
    ncm_iso = ncm.copy(); ncm_iso.calc = calc
    E_ncm = float(ncm_iso.get_potential_energy())
    wads = []
    for gap in gaps:
        stacked = stack_rigid(se, ncm, gap)
        stacked.calc = calc
        E_int = float(stacked.get_potential_energy())
        A = xy_area(stacked.cell.array)
        wad = (E_se + E_ncm - E_int) / A * 16.0218
        wads.append({'gap': float(gap), 'Wad': wad, 'E_int': E_int, 'A': A})
    return E_se, E_ncm, wads


def main():
    t0 = time.time()
    log("=" * 70)
    log(f"v30u ensemble — {N_SHIFTS} z-shifts × {len(COMPS)} comps")
    log("=" * 70)

    # 1) Ensure all zshift variants exist
    log("\nStep 1: generate/check zshift variants")
    all_variants = {}
    for c, cfg in COMPS.items():
        if not Path(cfg['src']).exists():
            log(f"  {c}: SRC NOT FOUND: {cfg['src']}")
            continue
        all_variants[c] = ensure_zshifts(c, cfg['src'])

    # 2) Load UMA
    log("\nStep 2: load UMA-s-1p1")
    try:
        calc = get_uma_calc()
        log("  UMA loaded.")
    except Exception as e:
        log(f"  UMA FAILED: {e}")
        return

    gaps = np.arange(GAP_MIN, GAP_MAX + GAP_STEP/2, GAP_STEP)
    log(f"  Z-scan: {len(gaps)} gap points per (comp, zshift)")

    # 3) Run Z-scan on all (comp, zshift)
    log(f"\nStep 3: run UMA Z-scan on {sum(len(v) for v in all_variants.values())} slabs")
    results = {}     # results[comp][zshift_i] = list of {gap, Wad, ...}
    for c, variants in all_variants.items():
        ncm_path = COMPS[c]['ncm']
        if not Path(ncm_path).exists():
            log(f"  {c}: NCM NOT FOUND: {ncm_path}")
            continue
        ncm = read(ncm_path)
        results[c] = {}
        for i, slab_path in enumerate(variants):
            tag = f"{c}_zs{i}"
            t1 = time.time()
            log(f"\n  -- {tag} ({slab_path.name}) --")
            try:
                se = read(slab_path)
                E_se, E_ncm, wads = scan_one_slab(se, ncm, calc, gaps)
                W = np.array([w['Wad'] for w in wads])
                i_max = int(np.argmax(W))
                log(f"    E_se={E_se:.4f}  E_ncm={E_ncm:.4f}  "
                    f"W_max={W[i_max]:+.4f} at d={gaps[i_max]:.2f}  "
                    f"({time.time()-t1:.1f}s)")
                results[c][f"zs{i}"] = {
                    'slab_file': str(slab_path),
                    'E_se': E_se, 'E_ncm': E_ncm,
                    'W_max': float(W[i_max]), 'd_min': float(gaps[i_max]),
                    'wads': wads,
                }
            except Exception as e:
                log(f"    FAILED: {e}")
                traceback.print_exc(file=sys.stdout)
                results[c][f"zs{i}"] = {'error': str(e)}

    # 4) Aggregate ensemble per (comp, gap): mean ± std across z-shifts
    log("\nStep 4: aggregate ensemble (mean ± std across z-shifts per gap)")
    ensemble = {}
    for c, zs_dict in results.items():
        ok_zs = [v for v in zs_dict.values() if 'wads' in v]
        if not ok_zs:
            log(f"  {c}: no valid zshifts")
            continue
        gap_arr = [w['gap'] for w in ok_zs[0]['wads']]
        wad_matrix = np.array([[w['Wad'] for w in z['wads']] for z in ok_zs])  # (n_zs, n_gaps)
        mean = wad_matrix.mean(axis=0)
        std  = wad_matrix.std(axis=0)
        ensemble[c] = {
            'n_zshifts_used': len(ok_zs),
            'gap_A': gap_arr,
            'Wad_mean': mean.tolist(),
            'Wad_std':  std.tolist(),
            'W_max_mean': float(mean.max()),
            'W_max_std':  float(std[mean.argmax()]),  # std at the gap where mean is maximal
            'd_min': float(gap_arr[int(mean.argmax())]),
        }
        log(f"  {c}: n_zs={len(ok_zs)}  "
            f"W_max_mean={ensemble[c]['W_max_mean']:+.4f} ± {ensemble[c]['W_max_std']:.4f}  "
            f"d_min={ensemble[c]['d_min']:.2f}")

    # 5) Pearson R on ensemble mean
    have = [c for c in PAPER_COMPS if c in ensemble]
    if len(have) >= 3:
        x = np.array([ensemble[c]['W_max_mean'] for c in have])
        y = np.array([PAPER_EXP[c] for c in have])
        R = float(np.corrcoef(x, y)[0, 1])
        log(f"\nR(ensemble W_max_mean vs paper exp Wad) = {R:+.4f}  (n={len(have)})")

    # 6) Save
    json.dump(results, open(RESULTS_DIR / "summary.json", 'w'),
              indent=2, default=str)
    json.dump(ensemble, open(RESULTS_DIR / "v30u_ensemble_curves.json", 'w'),
              indent=2)
    log(f"\n=== DONE: {(time.time()-t0)/60:.1f} min ===")
    log(f"saved {RESULTS_DIR / 'summary.json'}")
    log(f"saved {RESULTS_DIR / 'v30u_ensemble_curves.json'}")


if __name__ == "__main__":
    main()
