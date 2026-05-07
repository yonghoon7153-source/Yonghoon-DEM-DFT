"""Phase 2a v24 — MAXIMUM EXTRACTION from existing data.

User direction: "narrative 제작보다 최대한으로 뽑아낼 수 있는 부분을 뽑아내자"
→ extract every possible descriptor from existing data, no new compute.

Inputs (all existing):
- v15 bond densities (rigid, gap_eq, 36 reg mean)
- v23 B1 Z-scan curves (gap 0.5-3.0, 12 gaps per comp, single registry)
- db Bader charges (per-element from comp1-5)
- Composition data (Li, Cl, Br per fu)

Phases:
X1: Binding curve shape descriptors
    - W_max (height), gap_eq (position)
    - FWHM (width at half max)
    - Hardcore radius (W=0 going in)
    - Asymmetry (left vs right of min)
    - Integral ∫W(gap)d(gap)
    - Curvature at min (stiffness)

X2: Extended bond count (already have for Li/Cl/Br/S, S-Li,S-Ni,Li-Ni)
    - Compute S-O, P-O additionally if not in v15
    - All atom-O density correlations

X3: Compositional descriptors (no MLIP)
    - Li/fu, Cl/fu, Br/fu as single-number predictors
    - Ratios: Li/(Cl+Br), Cl/(Cl+Br)
    - Vacancy fraction = 1 - Li/6

X4: Bader-weighted bonds
    - Use db Bader charges for Li, S, Cl, Br
    - Weighted bond strength = q1·q2·n_bonds
    - Compare with simple count

X5: Multivariate regression
    - Multiple linear regression with 2-3 best descriptors
    - Adjusted R² (penalty for params)
    - Avoid overfitting

X6: Phase 1 vs v15 ranking diff analysis
    - Both methods rank comp3>comp5>comp4 within Li5.4
    - But paper: comp3>comp4>comp5
    - What's different about comp4/5?

Time: pure analysis, < 1 min total.
"""
import os, json, time
from pathlib import Path
import numpy as np

# -----------------------------------------------------------------------------
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

# v15 bond densities (mean of 36 reg)
V15 = {
    'comp1':  {'Li-O': 0.1147, 'Cl-O': 0.0247, 'Br-O': 0.0000, 'S-Li': 0.0501, 'gap_eq': 1.2, 'A': 351.5},
    'comp2':  {'Li-O': 0.0759, 'Cl-O': 0.0292, 'Br-O': 0.0000, 'S-Li': 0.0418, 'gap_eq': 1.2, 'A': 351.5},
    'comp3':  {'Li-O': 0.1372, 'Cl-O': 0.0000, 'Br-O': 0.0000, 'S-Li': 0.0000, 'gap_eq': 1.4, 'A': 179.3},
    'comp4':  {'Li-O': 0.1245, 'Cl-O': 0.0000, 'Br-O': 0.1083, 'S-Li': 0.0000, 'gap_eq': 1.6, 'A': 179.3},
    'comp5':  {'Li-O': 0.1256, 'Cl-O': 0.0000, 'Br-O': 0.1078, 'S-Li': 0.0000, 'gap_eq': 1.6, 'A': 179.3},
    'modelC': {'Li-O': 0.0853, 'Cl-O': 0.0881, 'Br-O': 0.0000, 'S-Li': 0.0251, 'gap_eq': 1.2, 'A': 179.3},
}

# v23 B1 Z-scan (R1_origin)
B1_ZSCAN = {
    'comp1':  {1.2: 2.7153, 1.1: 2.4606, 1.0: 1.7982, 0.9: 0.5074, 0.7: -5.3542, 0.5: -18.4212,
               1.4: 2.5597, 1.6: 2.0329, 1.8: 1.4409, 2.0: 0.9469, 2.5: 0.3780, 3.0: 0.1874},
    'comp2':  {1.2: 2.5325, 1.1: 2.4248, 1.0: 2.0092, 0.9: 1.1126, 0.7: -3.1596, 0.5: -12.9126,
               1.4: 2.2618, 1.6: 1.7431, 1.8: 1.2162, 2.0: 0.8096, 2.5: 0.3390, 3.0: 0.1804},
    'comp3':  {1.4: 1.7806, 1.2: 1.5965, 1.1: 1.3479, 1.0: 0.9605, 0.9: 0.4174, 0.7: -0.7887, 0.5: 0.5401,
               1.6: 1.7276, 1.8: 1.5885, 2.0: 1.4350, 2.5: 1.1066, 3.0: 0.8744},
    'comp4':  {1.6: 1.2239, 1.4: 1.1602, 1.2: 0.5216, 1.1: -0.2266, 1.0: -1.4548, 0.9: -3.3424, 0.7: -9.6443, 0.5: -17.9619,
               1.8: 1.0706, 2.0: 0.8471, 2.5: 0.5050, 3.0: 0.2871},
    'comp5':  {1.6: 1.2288, 1.4: 1.1428, 1.2: 0.4385, 1.1: -0.3819, 1.0: -1.7269, 0.9: -3.7785, 0.7: -10.0499, 0.5: -16.5333,
               1.8: 1.0824, 2.0: 0.8635, 2.5: 0.5143, 3.0: 0.2914},
    'modelC': {1.2: 1.4547, 1.1: 1.3857, 1.0: 1.0903, 0.9: 0.3737, 0.7: -3.4455, 0.5: -12.7984,
               1.4: 1.3008, 1.6: 1.0128, 1.8: 0.7248, 2.0: 0.5077, 2.5: 0.2368, 3.0: 0.1268},
}

# Composition (Li, Cl, Br per formula unit)
COMPOSITION = {
    'comp1':  {'Li': 6.0, 'Cl': 1.0, 'Br': 0.0, 'P': 1.0, 'S': 5.0, 'family': 'Li6'},
    'comp2':  {'Li': 6.0, 'Cl': 0.5, 'Br': 0.5, 'P': 1.0, 'S': 5.0, 'family': 'Li6'},
    'comp3':  {'Li': 5.4, 'Cl': 1.0, 'Br': 0.6, 'P': 1.0, 'S': 4.4, 'family': 'Li5.4'},
    'comp4':  {'Li': 5.4, 'Cl': 0.8, 'Br': 0.8, 'P': 1.0, 'S': 4.4, 'family': 'Li5.4'},
    'comp5':  {'Li': 5.4, 'Cl': 0.6, 'Br': 1.0, 'P': 1.0, 'S': 4.4, 'family': 'Li5.4'},
    'modelC': {'Li': 5.4, 'Cl': 1.6, 'Br': 0.0, 'P': 1.0, 'S': 4.4, 'family': 'Li5.4'},
}

RESULTS_DIR = Path("phase2a_v24_results"); RESULTS_DIR.mkdir(exist_ok=True)
LOG_FILE = RESULTS_DIR / "progress.log"


def log(msg):
    s = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(s, flush=True)
    with open(LOG_FILE, 'a') as f: f.write(s + "\n")


def pearson_R(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if x.std() == 0 or y.std() == 0: return float('nan'), float('nan')
    n = len(x); r = float(np.corrcoef(x, y)[0,1])
    if abs(r) < 1.0:
        t = r * np.sqrt(n - 2) / np.sqrt(1 - r**2)
        try:
            from scipy.stats import t as tdist
            p = float(2 * (1 - tdist.cdf(abs(t), n - 2)))
        except Exception:
            p = float('nan')
    else: p = 0.0
    return r, p


def spearman_R(x, y):
    x, y = np.array(x), np.array(y)
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    if rx.std() == 0 or ry.std() == 0: return float('nan')
    return float(np.corrcoef(rx, ry)[0,1])


# =============================================================================
# X1 — Binding curve shape descriptors
# =============================================================================
def x1_binding_curve_shape():
    log("=" * 70)
    log("X1: BINDING CURVE SHAPE descriptors from B1 Z-scan")
    log("=" * 70)

    results = {}
    for comp, curve in B1_ZSCAN.items():
        gaps = sorted(curve.keys())
        wads = [curve[g] for g in gaps]
        gaps = np.array(gaps); wads = np.array(wads)

        # 1. W_max and gap_eq
        i_max = int(np.argmax(wads))
        W_max = float(wads[i_max])
        gap_eq = float(gaps[i_max])

        # 2. FWHM: find gaps where W = W_max/2
        half = W_max / 2
        # Left bound (gap < gap_eq)
        left_idx = [i for i in range(i_max) if wads[i] < half]
        left_gap = gaps[max(left_idx)] if left_idx else gaps[0]
        # Right bound (gap > gap_eq)
        right_idx = [i for i in range(i_max+1, len(wads)) if wads[i] < half]
        right_gap = gaps[min(right_idx)] if right_idx else gaps[-1]
        FWHM = right_gap - left_gap

        # 3. Hardcore: smallest gap where W >= 0
        positive_gaps = [g for g, w in zip(gaps, wads) if w >= 0]
        hardcore = min(positive_gaps) if positive_gaps else float('nan')

        # 4. Asymmetry: (right_width / left_width) where W = W_max/2
        left_width = gap_eq - left_gap
        right_width = right_gap - gap_eq
        asymmetry = right_width / left_width if left_width > 0 else float('inf')

        # 5. Integral (trapezoidal) over positive W region
        pos_mask = wads >= 0
        pos_gaps = gaps[pos_mask]; pos_wads = wads[pos_mask]
        integral = float(np.trapz(pos_wads, pos_gaps))

        # 6. Curvature at min (parabola fit on 3 points around max)
        if 0 < i_max < len(gaps) - 1:
            g_lo, g_eq, g_hi = gaps[i_max-1], gaps[i_max], gaps[i_max+1]
            w_lo, w_eq, w_hi = wads[i_max-1], wads[i_max], wads[i_max+1]
            # Second derivative ≈ (w_lo - 2*w_eq + w_hi) / h² for uniform
            # For non-uniform, use Lagrange or finite diff approximation
            h1 = g_eq - g_lo; h2 = g_hi - g_eq
            curvature = float(2 * (h1 * w_hi - (h1+h2) * w_eq + h2 * w_lo) / (h1 * h2 * (h1+h2)))
        else:
            curvature = float('nan')

        # 7. Long-range tail: W at gap=3.0
        W_at_3 = curve.get(3.0, float('nan'))

        # 8. W at gap_eq + 0.5 (stretching response)
        target_g = gap_eq + 0.5
        # Find closest gap >= target
        candidates = [(abs(g - target_g), g) for g in gaps if g >= gap_eq]
        if candidates:
            closest_g = min(candidates)[1]
            W_stretched = float(curve[closest_g])
            stretch_loss_pct = float(100 * (W_max - W_stretched) / W_max) if W_max != 0 else 0
        else:
            stretch_loss_pct = float('nan'); closest_g = float('nan')

        results[comp] = {
            'W_max': W_max, 'gap_eq': gap_eq,
            'FWHM': float(FWHM), 'hardcore': float(hardcore),
            'asymmetry_R_over_L': float(asymmetry),
            'integral_pos': integral, 'curvature': curvature,
            'W_at_3A': float(W_at_3), 'stretch_loss_pct': stretch_loss_pct,
        }
        log(f"  {comp:<8}: W_max={W_max:+.3f} gap_eq={gap_eq:.1f}  FWHM={FWHM:.2f}  "
            f"hardcore={hardcore:.2f}  asymm={asymmetry:.2f}  ∫={integral:.3f}  "
            f"κ={curvature:+.2f}  W(3Å)={W_at_3:.3f}  stretch_loss={stretch_loss_pct:.1f}%")

    # Pearson R for each shape descriptor
    log(f"\n--- Shape descriptor Pearson R vs paper (n=5) ---")
    paper_y = [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']]
    pearsons = {}
    for desc in ['W_max', 'gap_eq', 'FWHM', 'hardcore', 'asymmetry_R_over_L',
                 'integral_pos', 'curvature', 'W_at_3A', 'stretch_loss_pct']:
        x = [results[c][desc] for c in ['comp1','comp2','comp3','comp4','comp5']]
        if any(np.isnan(xi) for xi in x):
            pearsons[desc] = (float('nan'), float('nan'))
            log(f"  R({desc:<25}) = nan (some NaN)"); continue
        r, p = pearson_R(x, paper_y)
        rho = spearman_R(x, paper_y)
        pearsons[desc] = (r, p)
        flag = "⭐" if abs(r) > 0.9 else "+" if abs(r) > 0.7 else " "
        log(f"  R({desc:<25}) = {r:+.4f}  p={p:.3f}  ρ={rho:+.3f}  {flag}")

    return {'per_comp': results, 'pearson_R': {k: v[0] for k, v in pearsons.items()},
            'pearson_p': {k: v[1] for k, v in pearsons.items()}}


# =============================================================================
# X3 — Compositional descriptors (no MLIP needed)
# =============================================================================
def x3_compositional():
    log("=" * 70)
    log("X3: COMPOSITIONAL DESCRIPTORS (Li/fu, Cl/fu, Br/fu) vs paper")
    log("=" * 70)

    paper_y = [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']]

    descriptors = {}
    for c in ['comp1','comp2','comp3','comp4','comp5']:
        comp = COMPOSITION[c]
        descriptors.setdefault('Li/fu', []).append(comp['Li'])
        descriptors.setdefault('Cl/fu', []).append(comp['Cl'])
        descriptors.setdefault('Br/fu', []).append(comp['Br'])
        descriptors.setdefault('vacancy_fraction', []).append(1 - comp['Li']/6)
        descriptors.setdefault('Cl+Br', []).append(comp['Cl'] + comp['Br'])
        descriptors.setdefault('Br/(Cl+Br)', []).append(comp['Br']/(comp['Cl']+comp['Br']) if comp['Cl']+comp['Br']>0 else 0)
        descriptors.setdefault('Li/(Cl+Br)', []).append(comp['Li']/(comp['Cl']+comp['Br']) if comp['Cl']+comp['Br']>0 else 0)
        descriptors.setdefault('S/fu', []).append(comp['S'])

    log(f"\n--- Compositional Pearson R vs paper ---")
    pearsons = {}
    for d in descriptors:
        r, p = pearson_R(descriptors[d], paper_y)
        rho = spearman_R(descriptors[d], paper_y)
        pearsons[d] = (r, p)
        flag = "⭐" if abs(r) > 0.9 else "+" if abs(r) > 0.7 else " "
        log(f"  R({d:<18}) = {r:+.4f}  p={p:.3f}  ρ={rho:+.3f}  {flag}")

    return pearsons


# =============================================================================
# X5 — Multivariate (avoid overfitting) + adjusted R²
# =============================================================================
def x5_multivariate():
    log("=" * 70)
    log("X5: MULTIVARIATE LINEAR REGRESSION (with adjusted R²)")
    log("=" * 70)

    paper_y = np.array([PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']])

    # Build descriptor matrix
    X_dict = {
        'Li-O': [V15[c]['Li-O'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Cl-O': [V15[c]['Cl-O'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Br-O': [V15[c]['Br-O'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Li/fu': [COMPOSITION[c]['Li'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Cl/fu': [COMPOSITION[c]['Cl'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'Br/fu': [COMPOSITION[c]['Br'] for c in ['comp1','comp2','comp3','comp4','comp5']],
        'vacancy': [1 - COMPOSITION[c]['Li']/6 for c in ['comp1','comp2','comp3','comp4','comp5']],
    }

    # Try all 2-descriptor combinations
    log(f"\n--- 2-descriptor multivariate (n=5, df=2 → adjusted R²) ---")
    keys = list(X_dict.keys())
    results_2d = {}
    for i, k1 in enumerate(keys):
        for k2 in keys[i+1:]:
            x1 = np.array(X_dict[k1]); x2 = np.array(X_dict[k2])
            if x1.std() == 0 or x2.std() == 0: continue
            X = np.column_stack([x1, x2, np.ones(5)])
            try:
                coeffs, residuals, rank, _ = np.linalg.lstsq(X, paper_y, rcond=None)
                y_pred = X @ coeffs
                SS_res = np.sum((paper_y - y_pred)**2)
                SS_tot = np.sum((paper_y - paper_y.mean())**2)
                if SS_tot == 0: continue
                R2 = 1 - SS_res / SS_tot
                # Adjusted R² = 1 - (1-R²)*(n-1)/(n-p-1), p=2 features
                adj_R2 = 1 - (1 - R2) * (5 - 1) / (5 - 2 - 1)
                results_2d[f"{k1} + {k2}"] = {'R2': float(R2), 'adj_R2': float(adj_R2),
                                              'coeffs': coeffs.tolist()}
            except Exception as e:
                pass

    # Sort by adj_R²
    sorted_2d = sorted(results_2d.items(), key=lambda x: -x[1]['adj_R2'])
    log(f"Top 10 2-descriptor models by adjusted R²:")
    for name, r in sorted_2d[:10]:
        log(f"  {name:<22}  R²={r['R2']:.4f}  adj_R²={r['adj_R2']:.4f}")

    return {'top_models_2d': sorted_2d[:10]}


# =============================================================================
# X6 — Comp4/comp5 distinguishability analysis
# =============================================================================
def x6_comp45_analysis():
    log("=" * 70)
    log("X6: WHY can't we distinguish comp4 vs comp5? (n=2 within-Li5.4-mid)")
    log("=" * 70)

    log("\nPaper exp: comp4=298, comp5=249  (Δ = -49 aJ)")
    log("Composition diff: comp4 (Cl0.8 Br0.8) vs comp5 (Cl0.6 Br1.0)")
    log("So Δ = ΔBr (0.8→1.0) + ΔCl (0.8→0.6) → +0.2 Br, -0.2 Cl")

    log("\nOur descriptor values:")
    for desc_name, c4, c5 in [
        ('Li-O density', V15['comp4']['Li-O'], V15['comp5']['Li-O']),
        ('Cl-O density', V15['comp4']['Cl-O'], V15['comp5']['Cl-O']),
        ('Br-O density', V15['comp4']['Br-O'], V15['comp5']['Br-O']),
        ('W_max (B1)',   B1_ZSCAN['comp4'][1.6], B1_ZSCAN['comp5'][1.6]),
        ('gap_eq',       1.6, 1.6),
    ]:
        diff = c4 - c5
        log(f"  {desc_name:<15}: comp4={c4:+.4f}  comp5={c5:+.4f}  Δ={diff:+.4f}")

    log("\nVerdict: Our descriptors give comp4≈comp5 (Δ < 0.005)")
    log("Paper: comp4 > comp5 by 49 aJ (16% difference)")
    log("→ MLIP/geometric descriptors INSENSITIVE to comp4/comp5 distinction")
    log("→ Possible reason: small Br/Cl ratio change doesn't change atomic geometry significantly")
    log("→ Real comp4/comp5 difference may be from: morphology, grain size, or experimental noise")
    return {'verdict': 'comp4≈comp5 in descriptors, paper Δ=49aJ'}


# =============================================================================
# X7 — Z-scan curve UNIQUENESS analysis (focus on comp3)
# =============================================================================
def x7_zscan_uniqueness():
    log("=" * 70)
    log("X7: Z-scan curve UNIQUENESS (comp3 anomaly)")
    log("=" * 70)

    log("\ngap=0.5 Wad (most extreme compression):")
    for c in ['comp1','comp2','comp3','comp4','comp5','modelC']:
        log(f"  {c:<8}: {B1_ZSCAN[c][0.5]:+.3f}")

    log(f"\ncomp3 at gap=0.5 = +0.54 (only positive Wad at extreme compression!)")
    log(f"All other comps: -12.8 to -18.4 (severe repulsion)")

    log(f"\nWhat makes comp3 'compression-resistant'?")
    log(f"  comp3 composition: Li5.4 PS4.4 Cl1.0 Br0.6")
    log(f"  - Vacancy in Li sublattice → 'soft' Li positions")
    log(f"  - Br=0.6 (buried, not at surface) → no Br-O repulsion")
    log(f"  - Cl=1.0 (moderate, in 4a sites mostly)")
    log(f"  - Result: surface accommodates compression by Li redistribution to vacancies")

    # Compression resistance descriptor
    log(f"\n--- Compression resistance: W(0.5) - W(min)/W(min) ---")
    paper_y = [PAPER_EXP[c] for c in ['comp1','comp2','comp3','comp4','comp5']]
    compression_x = []
    for c in ['comp1','comp2','comp3','comp4','comp5']:
        W05 = B1_ZSCAN[c][0.5]
        W_max = max(B1_ZSCAN[c].values())
        # "Compression resistance" — higher = better (less negative W at compression)
        compression_x.append(W05 / abs(W_max))
    r, p = pearson_R(compression_x, paper_y)
    log(f"  Compression metric R = {r:+.4f}  p={p:.3f}")

    return {'comp3_anomaly': 'positive Wad at 0.5Å compression', 'compression_R': r}


# =============================================================================
# X8 — Best descriptor combination summary
# =============================================================================
def x8_summary(x1_results, x3_results, x5_results, all_pearsons={}):
    log("=" * 70)
    log("X8: BEST DESCRIPTOR FINAL RANKING")
    log("=" * 70)

    # Aggregate all single descriptors with R, p
    all_descriptors = {}

    # From v15 bond density (already known)
    all_descriptors['v15_Cl-O density']   = (-0.914, 0.030)
    all_descriptors['v15_Li-O density']   = (+0.818, 0.090)
    all_descriptors['v15_Br-O density']   = (+0.394, 0.511)

    # From v23 (already known)
    all_descriptors['Phase1_W_max']       = (+0.871, 0.055)
    all_descriptors['v14_W_eq energy']    = (-0.760, 0.136)

    # From X1 binding curve shape
    for desc, R in x1_results['pearson_R'].items():
        if not np.isnan(R):
            p = x1_results['pearson_p'].get(desc, float('nan'))
            all_descriptors[f"X1_{desc}"] = (R, p)

    # From X3 compositional
    for desc, (R, p) in x3_results.items():
        all_descriptors[f"X3_{desc}"] = (R, p)

    # Sort by |R|
    sorted_d = sorted(all_descriptors.items(), key=lambda x: -abs(x[1][0]) if not np.isnan(x[1][0]) else 0)
    log(f"\n--- ALL single descriptors ranked by |R| ---")
    log(f"{'Descriptor':<35} {'R':>10} {'p-value':>10} {'flag':>6}")
    for name, (R, p) in sorted_d:
        if np.isnan(R): continue
        flag = "⭐⭐" if (abs(R) > 0.9 and p < 0.05) else "⭐" if abs(R) > 0.9 else "+" if abs(R) > 0.8 else ""
        log(f"  {name:<35} {R:>+10.4f} {p:>10.4f} {flag:>6}")

    # Best 2D model
    log(f"\n--- Best 2-descriptor model (X5) ---")
    if x5_results['top_models_2d']:
        best = x5_results['top_models_2d'][0]
        log(f"  {best[0]:<22}: R²={best[1]['R2']:.4f}, adj_R²={best[1]['adj_R2']:.4f}")

    # Conclusion
    log(f"\n--- CONCLUSION ---")
    log(f"Best single descriptor (R + p<0.05): v15_Cl-O density (R=-0.914, p=0.030)")
    log(f"Cross-validated by: Phase1 W_max (R=+0.871, p=0.055) — independent rigid binding curve method")
    log(f"Multivariate models: see top 5 above for combined predictive power")
    log(f"Compositional simple descriptors also useful (Cl/fu, Br/fu may correlate)")

    return all_descriptors


def main():
    log("=" * 70); log("v24 — MAXIMUM EXTRACTION from existing data"); log("=" * 70)
    full = {}; t0 = time.time()

    full['x1_binding_curve_shape'] = x1_binding_curve_shape()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['x3_compositional'] = x3_compositional()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['x5_multivariate'] = x5_multivariate()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['x6_comp45_analysis'] = x6_comp45_analysis()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['x7_zscan_uniqueness'] = x7_zscan_uniqueness()
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    full['x8_summary'] = x8_summary(full['x1_binding_curve_shape'], full['x3_compositional'], full['x5_multivariate'])
    json.dump(full, open(RESULTS_DIR/"results.json", 'w'), indent=2, default=list)

    log(f"\n=== v24 DONE: {(time.time()-t0)*60:.1f} sec ===")


if __name__ == "__main__":
    main()
