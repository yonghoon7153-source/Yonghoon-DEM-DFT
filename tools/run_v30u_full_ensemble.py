"""Full ensemble UMA binding curves — 5 z-shifts × 36 xy-shifts × 6 comps.

Most defensible ensemble methodology:
  - 5 z-shifts: synthesis-frozen surface termination uncertainty
  - 36 xy-shifts (6×6 uniform grid): registry alignment uncertainty
  - = 180 configs per (comp, gap) → robust mean ± std

Output per (comp, gap): mean Wad + std + all 180 samples
Per-comp checkpoint (resume safe if mid-run interrupted).

Time estimate (gabia A100, UMA-s-1p1):
  Li6 comp (624 atoms): 36s/Z-scan × 5 z × 36 xy = 6,480s ≈ 108 min
  Li5.4 (248 atoms):    17.6s × 5 × 36 = 3,168s ≈ 53 min
  Total = 2×108 + 4×53 = ~7.1 hours

Output:
  v30u_full_ensemble_results/
    summary.json                  master (per comp, per gap: mean, std)
    samples.json                  raw 180 samples per (comp, gap) for stats
    {comp}_done.json              per-comp checkpoint (resume)
    run.log
"""
import os, json, time, sys, traceback
from pathlib import Path
import numpy as np
from ase.io import read

# Slabs (same as ensemble v1)
COMPS = {
    'comp1':  {'src': 'comp1_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp2':  {'src': 'comp2_slab_v2.xyz',                  'ncm': 'ncm_7x7x1_3Lconv.xyz'},
    'comp3':  {'src': 'comp3_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp4':  {'src': 'comp4_slab_v2_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'comp5':  {'src': 'comp5_slab_v1_PRESERVED.xyz',        'ncm': 'ncm_5x5x1_3Lconv.xyz'},
    'modelC': {'src': 'modelC_slab_v2_PRESERVED.xyz',       'ncm': 'ncm_5x5x1_3Lconv.xyz'},
}

VACUUM_TOP = 30.0
N_ZSHIFTS = 5
N_XY_GRID = 6     # 6×6 = 36 xy-shifts
GAP_MIN, GAP_MAX, GAP_STEP = 0.5, 6.0, 0.25
PAPER_EXP   = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

RESULTS_DIR = Path("v30u_full_ensemble_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG = RESULTS_DIR / "run.log"

def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG, 'a') as f:
        f.write(s + "\n")


def zshift_variant(atoms, frac):
    a = atoms.copy()
    cz = a.cell.lengths()[2]
    pos = a.positions.copy()
    pos[:, 2] = (pos[:, 2] + frac * cz) % cz
    a.set_positions(pos)
    return a


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


def main():
    t0 = time.time()
    log("=" * 70)
    log(f"v30u FULL ensemble — {N_ZSHIFTS} z × {N_XY_GRID*N_XY_GRID} xy × {len(COMPS)} comps")
    log(f"Total configs per (comp, gap): {N_ZSHIFTS * N_XY_GRID * N_XY_GRID} = 180")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    try:
        calc = get_uma_calc(); log("  UMA loaded.")
    except Exception as e:
        log(f"  UMA FAILED: {e}"); traceback.print_exc(file=sys.stdout); return

    gaps = np.arange(GAP_MIN, GAP_MAX + GAP_STEP/2, GAP_STEP)
    xy_shifts = [(i/N_XY_GRID, j/N_XY_GRID)
                 for i in range(N_XY_GRID) for j in range(N_XY_GRID)]
    log(f"\nGap points: {len(gaps)}  |  xy_shifts: {len(xy_shifts)}  |  z_shifts: {N_ZSHIFTS}")

    master = {}
    for c, cfg in COMPS.items():
        checkpoint = RESULTS_DIR / f"{c}_done.json"
        if checkpoint.exists():
            log(f"\n[{c}] checkpoint found — loading")
            master[c] = json.load(open(checkpoint))
            continue

        log(f"\n========= {c} =========")
        if not Path(cfg['src']).exists() or not Path(cfg['ncm']).exists():
            log(f"  MISSING file(s) — skip"); continue
        se_base = read(cfg['src'])
        ncm = read(cfg['ncm'])

        # Pre-compute isolated SE & NCM energies (same for all gaps)
        ncm_iso = ncm.copy(); ncm_iso.calc = calc
        E_ncm = float(ncm_iso.get_potential_energy())
        # SE isolated for each z-shift (z-shift doesn't change cell, just rolls atoms)
        E_se_per_z = []
        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
            se_z.calc = calc
            E_se_per_z.append(float(se_z.get_potential_energy()))
        log(f"  E_se (5 zs) = [{', '.join(f'{e:.2f}' for e in E_se_per_z)}]")
        log(f"  E_ncm = {E_ncm:.2f}")

        comp_data = {'gaps': gaps.tolist(),
                     'Wad_samples': {f"{g:.3f}": [] for g in gaps}}
        n_configs = N_ZSHIFTS * len(xy_shifts)
        idx = 0
        t1 = time.time()
        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
            E_se = E_se_per_z[iz]
            for ixy, (dx, dy) in enumerate(xy_shifts):
                idx += 1
                for gap in gaps:
                    stacked = stack_rigid(se_z, ncm, gap, shift_frac=(dx, dy))
                    stacked.calc = calc
                    E_int = float(stacked.get_potential_energy())
                    A = xy_area(stacked.cell.array)
                    wad = (E_se + E_ncm - E_int) / A * 16.0218
                    comp_data['Wad_samples'][f"{gap:.3f}"].append(wad)
                if idx % 5 == 0 or idx == n_configs:
                    elapsed = time.time() - t1
                    eta = elapsed * (n_configs - idx) / idx
                    log(f"  {c}: config {idx}/{n_configs}  z{iz} xy{ixy}  "
                        f"elapsed={elapsed/60:.1f}min  ETA={eta/60:.1f}min")

        # Aggregate per gap
        comp_data['Wad_mean'] = []
        comp_data['Wad_std'] = []
        for g in gaps:
            samples = comp_data['Wad_samples'][f"{g:.3f}"]
            comp_data['Wad_mean'].append(float(np.mean(samples)))
            comp_data['Wad_std'].append(float(np.std(samples)))
        comp_data['n_samples'] = n_configs

        # Save per-comp checkpoint
        json.dump(comp_data, open(checkpoint, 'w'), indent=2)
        master[c] = comp_data
        log(f"  ✓ {c} done in {(time.time()-t1)/60:.1f} min  ({n_configs} configs)")

    # Master summary (without samples to save space)
    summary = {}
    for c, d in master.items():
        summary[c] = {
            'gaps': d['gaps'],
            'Wad_mean': d['Wad_mean'],
            'Wad_std':  d['Wad_std'],
            'n_samples': d['n_samples'],
            'W_max_mean': float(max(d['Wad_mean'])),
            'W_max_std':  d['Wad_std'][int(np.argmax(d['Wad_mean']))],
            'd_at_W_max': d['gaps'][int(np.argmax(d['Wad_mean']))],
        }
    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'), indent=2)
    json.dump(master, open(RESULTS_DIR / "samples.json", 'w'), indent=2)

    log("\n" + "=" * 70)
    log(f"{'comp':<8} {'W_max_mean':>12} {'W_max_std':>10} {'d':>6} {'paper':>6}")
    for c in PAPER_COMPS + ['modelC']:
        if c in summary:
            s = summary[c]
            log(f"{c:<8} {s['W_max_mean']:>+12.3f} {s['W_max_std']:>10.3f} "
                f"{s['d_at_W_max']:>6.2f} {PAPER_EXP.get(c,'—'):>6}")

    have = [c for c in PAPER_COMPS if c in summary]
    if len(have) >= 3:
        x = [summary[c]['W_max_mean'] for c in have]
        y = [PAPER_EXP[c] for c in have]
        R = float(np.corrcoef(x, y)[0, 1])
        log(f"\nR(W_max_mean vs paper) = {R:+.4f}  (n={len(have)})")

    log(f"\n=== TOTAL: {(time.time()-t0)/3600:.2f} hours ===")
    log(f"saved {RESULTS_DIR / 'summary.json'}")
    log(f"saved {RESULTS_DIR / 'samples.json'}")


if __name__ == "__main__":
    main()
