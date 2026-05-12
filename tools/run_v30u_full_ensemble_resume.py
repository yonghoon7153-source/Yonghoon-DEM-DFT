"""Full ensemble UMA binding curves — WITH RESUME (per-config checkpoint).

Same protocol as run_v30u_full_ensemble.py (5 z × 36 xy × 6 comps),
but saves progress after EACH config so we can resume mid-comp if
server disconnects or process killed.

Progress files (in v30u_full_ensemble_results/):
  {comp}_progress.json    written every config; resume from here
  {comp}_done.json        only written when all 180 configs done

Resume logic:
  - On startup, for each comp:
    - if {comp}_done.json exists → skip (already done)
    - if {comp}_progress.json exists → load partial samples + skip
      already-completed (z, xy) combos
    - else → start fresh

Usage:
  python run_v30u_full_ensemble_resume.py
  # Re-run after crash — automatically resumes from last config saved
"""
import os, json, time, sys, traceback
from pathlib import Path
import numpy as np
from ase.io import read

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
N_XY_GRID = 6
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


def process_comp(c, cfg, calc, gaps, xy_shifts):
    """Process one comp with per-config checkpoint resume."""
    done_path = RESULTS_DIR / f"{c}_done.json"
    prog_path = RESULTS_DIR / f"{c}_progress.json"

    if done_path.exists():
        log(f"[{c}] already DONE, skip")
        return json.load(open(done_path))

    n_configs = N_ZSHIFTS * len(xy_shifts)
    gap_keys = [f"{g:.3f}" for g in gaps]

    # Load progress if any
    if prog_path.exists():
        progress = json.load(open(prog_path))
        log(f"[{c}] resuming from progress: "
            f"{len(progress.get('completed_keys', []))}/{n_configs} configs done")
    else:
        progress = {
            'gaps': gaps.tolist(),
            'E_se_per_z': None,
            'E_ncm': None,
            'completed_keys': [],   # list of "z{iz}_xy{ixy}" already done
            'Wad_samples': {g: [] for g in gap_keys},
        }

    # Load slabs
    se_base = read(cfg['src'])
    ncm = read(cfg['ncm'])

    # Isolated energies (compute once)
    if progress['E_ncm'] is None:
        ncm_iso = ncm.copy(); ncm_iso.calc = calc
        progress['E_ncm'] = float(ncm_iso.get_potential_energy())
    if progress['E_se_per_z'] is None:
        E_se_per_z = []
        for iz in range(N_ZSHIFTS):
            se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
            se_z.calc = calc
            E_se_per_z.append(float(se_z.get_potential_energy()))
        progress['E_se_per_z'] = E_se_per_z
        # Save initial state
        json.dump(progress, open(prog_path, 'w'))
    log(f"[{c}] E_se = {progress['E_se_per_z']}, E_ncm = {progress['E_ncm']:.2f}")

    # Process configs
    t1 = time.time()
    completed = set(progress['completed_keys'])
    idx = len(completed)
    save_every = 1   # save after every config (small files, robust)
    for iz in range(N_ZSHIFTS):
        se_z = zshift_variant(se_base, iz / N_ZSHIFTS)
        E_se = progress['E_se_per_z'][iz]
        for ixy, (dx, dy) in enumerate(xy_shifts):
            key = f"z{iz}_xy{ixy}"
            if key in completed:
                continue
            for gi, gap in enumerate(gaps):
                stacked = stack_rigid(se_z, ncm, gap, shift_frac=(dx, dy))
                stacked.calc = calc
                E_int = float(stacked.get_potential_energy())
                A = xy_area(stacked.cell.array)
                wad = (E_se + progress['E_ncm'] - E_int) / A * 16.0218
                progress['Wad_samples'][gap_keys[gi]].append(wad)
            progress['completed_keys'].append(key)
            idx += 1
            if idx % save_every == 0:
                json.dump(progress, open(prog_path, 'w'))
            if idx % 5 == 0 or idx == n_configs:
                elapsed = time.time() - t1
                done_this_run = idx - (n_configs - sum(1 for _ in completed))
                # ETA based on this-run rate
                eta = elapsed * (n_configs - idx) / max(done_this_run, 1)
                log(f"  [{c}] config {idx}/{n_configs}  z{iz} xy{ixy}  "
                    f"elapsed_run={elapsed/60:.1f}min  ETA={eta/60:.1f}min")

    # Aggregate
    Wad_mean = [float(np.mean(progress['Wad_samples'][g])) for g in gap_keys]
    Wad_std  = [float(np.std(progress['Wad_samples'][g]))  for g in gap_keys]
    final = {
        'gaps': progress['gaps'],
        'Wad_samples': progress['Wad_samples'],
        'Wad_mean': Wad_mean,
        'Wad_std': Wad_std,
        'n_samples': n_configs,
        'E_se_per_z': progress['E_se_per_z'],
        'E_ncm': progress['E_ncm'],
    }
    json.dump(final, open(done_path, 'w'))
    prog_path.unlink(missing_ok=True)
    log(f"[{c}] ✓ DONE  saved {done_path}")
    return final


def main():
    t0 = time.time()
    log("=" * 70)
    log(f"v30u FULL ensemble RESUMABLE — 5 z × 36 xy × 6 comps")
    log("=" * 70)

    log("\nLoading UMA-s-1p1...")
    try:
        calc = get_uma_calc(); log("  UMA loaded.")
    except Exception as e:
        log(f"  UMA FAILED: {e}"); return

    gaps = np.arange(GAP_MIN, GAP_MAX + GAP_STEP/2, GAP_STEP)
    xy_shifts = [(i/N_XY_GRID, j/N_XY_GRID)
                 for i in range(N_XY_GRID) for j in range(N_XY_GRID)]
    log(f"Gap points: {len(gaps)} | xy_shifts: {len(xy_shifts)} | z_shifts: {N_ZSHIFTS}")

    master = {}
    for c, cfg in COMPS.items():
        if not Path(cfg['src']).exists() or not Path(cfg['ncm']).exists():
            log(f"\n[{c}] MISSING input file(s) — skip"); continue
        log(f"\n========= {c} =========")
        try:
            master[c] = process_comp(c, cfg, calc, gaps, xy_shifts)
        except Exception as e:
            log(f"  ERROR on {c}: {e}")
            traceback.print_exc(file=sys.stdout)

    # Summary (without samples)
    summary = {}
    for c, d in master.items():
        i = int(np.argmax(d['Wad_mean']))
        summary[c] = {
            'gaps': d['gaps'],
            'Wad_mean': d['Wad_mean'],
            'Wad_std': d['Wad_std'],
            'n_samples': d['n_samples'],
            'W_max_mean': d['Wad_mean'][i],
            'W_max_std':  d['Wad_std'][i],
            'd_at_W_max': d['gaps'][i],
        }
    json.dump(summary, open(RESULTS_DIR / "summary.json", 'w'), indent=2)

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
        log(f"\nR(W_max_mean vs paper) = {R:+.4f}")
    log(f"\n=== TOTAL: {(time.time()-t0)/3600:.2f} hours ===")


if __name__ == "__main__":
    main()
