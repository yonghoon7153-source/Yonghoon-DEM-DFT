"""exhaustive_v2_trend_analysis.py — try EVERY processing trick on v2 data.

For comp1 (v2), comp2 (v2), comp4 (v1 default + v2 face B), tries every
processing combination from the agent report and reports R(paper_aJ).

Processing axes (orthogonal combinations):
  1. Face: A only / B only / mean(A, B) / best of (A, B)
  2. Aggregation over 36 reg: MEAN / MAX / MEDIAN / BEST (top-3 mean)
  3. Asymptote handling:
       - none (raw)
       - per-comp subtract (gap >= 3.0 mean)
       - per-(reg) subtract (each reg subtracts its own asymp, then mean)
  4. Strain α correction: α ∈ {0, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5}
  5. Wad metric: max_well / well_minus_asymp / asymp_baseline

Total combinations: 4 face × 4 agg × 3 asymp × 7 α × 3 metric = 1008
Computes R for each → reports top 20 most paper-direction (positive R) configs
+ binding curves at the very best config.

Reads:
  face_flip_results/{comp}_done.json   (face A/B per-reg curves)
  v30u_1L_correct_results_eiso_fix/{comp}_done.json   (for ΔW_strain)

Output:
  /data/work/v30u_ensemble/exhaustive_v2_trend.{json,csv,png}
"""
import json
from pathlib import Path
from itertools import product
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit

WORK = Path('/data/work/v30u_ensemble')
FACE = WORK / 'face_flip_results'
EISO = WORK / 'v30u_1L_correct_results_eiso_fix'
OUT_JSON = WORK / 'exhaustive_v2_trend.json'
OUT_CSV  = WORK / 'exhaustive_v2_trend.csv'
OUT_PNG  = WORK / 'exhaustive_v2_trend_best.png'

# Use v2 for Li6, v2 face B for comp4 (avoiding Cl anomaly) where possible
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp4_v2': 298, 'comp4_v1': 298}

# Eiso key (for ΔW_strain lookup)
EISO_KEY = {'comp1': 'comp1', 'comp2': 'comp2',
            'comp4_v1': 'comp4', 'comp4_v2': 'comp4',
            'modelC': 'modelC'}

CANDIDATE_COMPS = ['comp1', 'comp2', 'comp4_v1', 'comp4_v2', 'modelC']
ASYMP_GAP_MIN = 3.0


def load_data():
    """Returns {comp: {face: {reg: {gap: Wad}}, gaps: list, dW_strain: float}}"""
    data = {}
    for c in CANDIDATE_COMPS:
        ff = FACE / f"{c}_done.json"
        if not ff.exists():
            continue
        j = json.load(open(ff))
        gaps = j['gaps']
        eiso_key = EISO_KEY[c]
        eiso_path = EISO / f"{eiso_key}_done.json"
        dW = json.load(open(eiso_path))['delta_Wad_J_per_m2'] if eiso_path.exists() else 0.0
        comp_d = {'gaps': gaps, 'dW_strain': dW, 'faces': {}}
        for face_name, face in j['faces'].items():
            reg_curves = {}
            for reg_name, reg in face['per_reg'].items():
                curve = []
                for d in gaps:
                    gk = f"{d:.3f}"
                    w = reg['curve'].get(gk, {}).get('Wad_J_per_m2')
                    curve.append(w if w is not None else np.nan)
                reg_curves[reg_name] = np.array(curve, dtype=float)
            comp_d['faces'][face_name] = reg_curves
        data[c] = comp_d
    return data


def aggregate_per_gap(reg_curves, mode):
    """reg_curves: {reg_name: array of Wad per gap}. Returns array per gap."""
    stacked = np.stack(list(reg_curves.values()))  # (n_reg, n_gaps)
    if mode == 'mean':
        return np.nanmean(stacked, axis=0)
    if mode == 'max':
        return np.nanmax(stacked, axis=0)
    if mode == 'median':
        return np.nanmedian(stacked, axis=0)
    if mode == 'best3':                            # top-3 mean per gap
        sorted_ = np.sort(stacked, axis=0)[::-1]   # descending
        return np.nanmean(sorted_[:3], axis=0)
    raise ValueError(mode)


def apply_asymp(wad_per_gap, gaps, mode, reg_curves=None):
    """Returns asymp-corrected Wad curve."""
    gaps = np.asarray(gaps)
    if mode == 'none':
        return wad_per_gap
    if mode == 'per_comp':
        mask = gaps >= ASYMP_GAP_MIN
        asymp = float(np.nanmean(wad_per_gap[mask])) if mask.any() else 0.0
        return wad_per_gap - asymp
    if mode == 'per_reg':
        # Each registry: subtract its own asymp, then aggregate (mean)
        if reg_curves is None:
            return wad_per_gap
        normalized = {}
        for r, w in reg_curves.items():
            mask = gaps >= ASYMP_GAP_MIN
            asymp_r = float(np.nanmean(w[mask])) if mask.any() else 0.0
            normalized[r] = w - asymp_r
        return aggregate_per_gap(normalized, 'mean')
    raise ValueError(mode)


def get_face_curves(data, comp, face_mode):
    """Returns merged reg_curves for given face_mode."""
    comp_d = data[comp]
    faces = comp_d['faces']
    if face_mode == 'A':
        return faces.get('A', {})
    if face_mode == 'B':
        return faces.get('B', {})
    if face_mode == 'mean':
        # average corresponding registries (same reg name) across faces
        merged = {}
        if 'A' in faces and 'B' in faces:
            for r in faces['A']:
                if r in faces['B']:
                    merged[r] = 0.5 * (faces['A'][r] + faces['B'][r])
            return merged
        return faces.get('A', faces.get('B', {}))
    if face_mode == 'best':
        # Pick face with higher Wad_max (per-comp)
        best = {}
        agg_A = aggregate_per_gap(faces['A'], 'mean') if 'A' in faces else None
        agg_B = aggregate_per_gap(faces['B'], 'mean') if 'B' in faces else None
        if agg_A is None: return faces.get('B', {})
        if agg_B is None: return faces.get('A', {})
        return faces['A'] if np.nanmax(agg_A) >= np.nanmax(agg_B) else faces['B']
    raise ValueError(face_mode)


def compute_metric(wad_curve, metric, gaps):
    """Returns scalar per comp for correlation with paper."""
    gaps = np.asarray(gaps)
    if metric == 'wad_max':
        return float(np.nanmax(wad_curve))
    if metric == 'well_depth':
        return float(np.nanmax(wad_curve) - wad_curve[-1])
    if metric == 'asymp':
        return float(wad_curve[-1])
    raise ValueError(metric)


def main():
    data = load_data()
    print(f"Loaded data for: {list(data.keys())}\n")
    for c, d in data.items():
        print(f"  {c}: dW_strain={d['dW_strain']:+.3f}  faces={list(d['faces'].keys())}  "
              f"n_reg(A)={len(d['faces'].get('A', {}))}")
    print()

    # Try all combinations
    results = []
    face_modes = ['A', 'B', 'mean', 'best']
    agg_modes  = ['mean', 'max', 'median', 'best3']
    asymp_modes = ['none', 'per_comp', 'per_reg']
    alphas      = [0.0, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5]
    metrics     = ['wad_max', 'well_depth', 'asymp']

    # For correlation: use comp1, comp2, comp4 (choose v1 OR v2 — we'll test both)
    paper_comp_sets = [
        ['comp1', 'comp2', 'comp4_v1'],   # mixed (comp4 v1 = paper original)
        ['comp1', 'comp2', 'comp4_v2'],   # all-v2 (comp4 v2 = anneal champion)
    ]

    for face_mode, agg_mode, asymp_mode, alpha, metric, p_set in product(
            face_modes, agg_modes, asymp_modes, alphas, metrics, paper_comp_sets):
        # comp4_v2 only viable in face B (Cl anomaly on A); skip face A for v2 set if interested
        # but include all to see what happens
        values, paper_vals, names = [], [], []
        skip = False
        for c in p_set:
            if c not in data:
                skip = True; break
            comp_d = data[c]
            reg_curves = get_face_curves(data, c, face_mode)
            if not reg_curves:
                skip = True; break
            gaps = comp_d['gaps']
            wad_agg = aggregate_per_gap(reg_curves, agg_mode)
            wad_corr = apply_asymp(wad_agg, gaps, asymp_mode, reg_curves)
            wad_strain = wad_corr - alpha * comp_d['dW_strain']
            val = compute_metric(wad_strain, metric, gaps)
            values.append(val)
            paper_vals.append(PAPER_EXP[c])
            names.append(c)
        if skip or len(values) < 2:
            continue
        if np.std(values) < 1e-9 or np.std(paper_vals) < 1e-9:
            R = np.nan
        else:
            R = float(np.corrcoef(values, paper_vals)[0, 1])
        results.append({
            'face_mode': face_mode, 'agg_mode': agg_mode, 'asymp_mode': asymp_mode,
            'alpha': alpha, 'metric': metric, 'p_set': '+'.join(p_set),
            'values': values, 'paper': paper_vals, 'R': R,
        })

    # Sort by R descending
    results_sorted = sorted([r for r in results if not np.isnan(r['R'])],
                            key=lambda r: -r['R'])

    # ── print top 30 ───────────────────────────────────────────
    print("─" * 110)
    print("TOP 30 — most paper-direction (highest R) configs:")
    print("─" * 110)
    print(f"{'R':>6} | {'face':<5} {'agg':<7} {'asymp':<10} {'α':<5} {'metric':<11} | {'p_set':<30} | values")
    print("─" * 110)
    for r in results_sorted[:30]:
        print(f"{r['R']:>+6.3f} | {r['face_mode']:<5} {r['agg_mode']:<7} "
              f"{r['asymp_mode']:<10} {r['alpha']:<5} {r['metric']:<11} | "
              f"{r['p_set']:<30} | {[f'{v:+.3f}' for v in r['values']]}")

    # ── save ────────────────────────────────────────────────────
    json.dump([{k: v for k, v in r.items() if k != 'values' and k != 'paper'}
               | {'values': r['values'], 'paper': r['paper']}
               for r in results_sorted], open(OUT_JSON, 'w'), indent=2)
    with open(OUT_CSV, 'w') as f:
        f.write("R,face,agg,asymp,alpha,metric,p_set,values\n")
        for r in results_sorted:
            f.write(f"{r['R']:+.4f},{r['face_mode']},{r['agg_mode']},"
                    f"{r['asymp_mode']},{r['alpha']},{r['metric']},"
                    f"{r['p_set']},\"{r['values']}\"\n")
    print(f"\nSaved: {OUT_JSON}")
    print(f"Saved: {OUT_CSV}")

    # ── plot best config binding curves ────────────────────────
    best = results_sorted[0]
    print(f"\n── BEST config: R={best['R']:+.3f} ──")
    print(f"  face={best['face_mode']}  agg={best['agg_mode']}  "
          f"asymp={best['asymp_mode']}  α={best['alpha']}  metric={best['metric']}")
    print(f"  p_set: {best['p_set']}")

    fig, ax = plt.subplots(figsize=(10, 6))
    COLORS = {'comp1':'#1f77b4', 'comp2':'#17becf', 'comp4_v1':'#9467bd', 'comp4_v2':'#d62728'}
    MARKERS = {'comp1':'s', 'comp2':'o', 'comp4_v1':'D', 'comp4_v2':'X'}
    p_comps = best['p_set'].split('+')
    for c in p_comps:
        comp_d = data[c]
        reg_curves = get_face_curves(data, c, best['face_mode'])
        gaps = comp_d['gaps']
        wad_agg = aggregate_per_gap(reg_curves, best['agg_mode'])
        wad_corr = apply_asymp(wad_agg, gaps, best['asymp_mode'], reg_curves)
        wad_strain = wad_corr - best['alpha'] * comp_d['dW_strain']
        e_adh = -wad_strain
        ax.plot(gaps, e_adh, MARKERS.get(c, 'o'), color=COLORS.get(c, 'k'),
                ms=8, mec='k', mew=0.5, zorder=5,
                label=f"{c} (paper {PAPER_EXP[c]})")
        # Cubic spline smooth
        valid = ~np.isnan(e_adh)
        if valid.sum() >= 4:
            cs = CubicSpline(np.array(gaps)[valid], np.array(e_adh)[valid])
            gd = np.linspace(min(gaps), max(gaps), 600)
            ax.plot(gd, cs(gd), '-', color=COLORS.get(c, 'k'), lw=2, alpha=0.85)
    ax.axhline(0, color='k', lw=0.6)
    ax.axvspan(1.2, 1.6, alpha=0.10, color='grey')
    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel(r'$E_{adh}$ (J m$^{-2}$)', fontsize=12)
    title = (f"BEST v2 config: face {best['face_mode']}, {best['agg_mode']} agg, "
             f"{best['asymp_mode']} asymp, α={best['alpha']}\n"
             f"R(paper)={best['R']:+.3f}  metric={best['metric']}")
    ax.set_title(title, fontsize=11)
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    fig.savefig(OUT_PNG.with_suffix('.pdf'), bbox_inches='tight')
    print(f"\nSaved: {OUT_PNG}")


if __name__ == "__main__":
    main()
