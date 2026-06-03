"""
GB Correction Fitting Analysis Report Generator
Generates a comprehensive markdown report comparing multiple regression models
for the grain boundary correction factor R = σ_brug / σ_proxy.
"""
import json
import math
import sys
import os
import numpy as np
from scipy import stats as sp_stats
from datetime import datetime


def _load_metrics(paths, names):
    """Load metrics from JSON files."""
    data = []
    for p in paths:
        with open(p) as f:
            data.append(json.load(f))
    return data


def _extract(data_list, names):
    """Extract fitting variables from metrics."""
    rows = []
    for i, d in enumerate(data_list):
        phi_se = d.get('phi_se', 0)
        f_perc = d.get('percolation_pct', 0) / 100
        tau = d.get('tortuosity_recommended', d.get('tortuosity_mean', 0))
        g_path = d.get('path_conductance_mean', 0)
        gb_d = d.get('gb_density_mean', 0)
        T = d.get('thickness_um', 0)

        sigma_brug_ratio = phi_se * f_perc / tau**2 if tau > 0 else 0
        sigma_proxy = g_path * f_perc / tau if g_path > 0 and tau > 0 else 0

        if sigma_proxy > 0 and gb_d > 0 and sigma_brug_ratio > 0 and T > 0:
            R = sigma_brug_ratio / sigma_proxy
            rows.append({
                'name': names[i], 'phi_se': phi_se, 'f_perc': f_perc,
                'tau': tau, 'g_path': g_path, 'gb_d': gb_d, 'T': T,
                'sigma_brug': sigma_brug_ratio, 'sigma_proxy': sigma_proxy, 'R': R
            })
    return rows


def _fit_models(rows):
    """Fit all candidate models and return results sorted by R²."""
    n = len(rows)
    gb = np.array([r['gb_d'] for r in rows])
    T = np.array([r['T'] for r in rows])
    R = np.array([r['R'] for r in rows])
    logR = np.log(R)

    models = []

    # --- Tier 1 candidates ---

    # A1: Exponential Decay — ln(R) = b·GB_d + ln(k)
    try:
        slope, intercept, r, _, _ = sp_stats.linregress(gb, logR)
        models.append({
            'id': 'A1', 'name': 'Exponential Decay',
            'formula': 'ln(R) = b·GB_d + ln(k)',
            'formula_R': 'R = k·exp(b·GB_d)',
            'params': {'b': round(slope, 4), 'ln(k)': round(intercept, 4)},
            'n_params': 2, 'R2': round(r**2, 4), 'n': n,
            'physics': '각 GB가 독립 barrier → 투과확률의 곱 → 지수감쇠',
        })
    except: pass

    # A2: Exponential (원점) — ln(R) = b·GB_d  (k=1 forced)
    try:
        b_a2 = np.sum(gb * logR) / np.sum(gb**2)
        pred = b_a2 * gb
        ss_res = np.sum((logR - pred)**2)
        ss_tot = np.sum((logR - np.mean(logR))**2)
        r2_a2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        models.append({
            'id': 'A2', 'name': 'Exponential (원점통과)',
            'formula': 'ln(R) = b·GB_d',
            'formula_R': 'R = exp(b·GB_d)',
            'params': {'b': round(b_a2, 4)},
            'n_params': 1, 'R2': round(r2_a2, 4), 'n': n,
            'physics': 'GB_d=0이면 R=1 (Bruggeman 정확) 강제',
        })
    except: pass

    # B1: Power Law — ln(R) = c·ln(GB_d) + d
    try:
        logGB = np.log(gb)
        slope, intercept, r, _, _ = sp_stats.linregress(logGB, logR)
        models.append({
            'id': 'B1', 'name': 'Power Law',
            'formula': 'ln(R) = c·ln(GB_d) + d',
            'formula_R': 'R = exp(d)·GB_d^c',
            'params': {'c': round(slope, 4), 'd': round(intercept, 4)},
            'n_params': 2, 'R2': round(r**2, 4), 'n': n,
            'physics': 'Percolation theory 스케일링 법칙 (Archie\'s law 유사)',
        })
    except: pass

    # E3: Square Root — ln(R) = a·√GB_d + c
    try:
        sqrtGB = np.sqrt(gb)
        slope, intercept, r, _, _ = sp_stats.linregress(sqrtGB, logR)
        models.append({
            'id': 'E3', 'name': 'Square Root',
            'formula': 'ln(R) = a·√GB_d + c',
            'formula_R': 'R = exp(c)·exp(a·√GB_d)',
            'params': {'a': round(slope, 4), 'c': round(intercept, 4)},
            'n_params': 2, 'R2': round(r**2, 4), 'n': n,
            'physics': '확산(Fick\'s law) 기반 — 저항이 √거리에 비례',
        })
    except: pass

    # M15: BLM+Constriction — ln(R) = α·ln(GB_d²×T) + ln(C)
    try:
        x_blm = gb**2 * T
        logx = np.log(x_blm)
        slope, intercept, r, _, _ = sp_stats.linregress(logx, logR)
        models.append({
            'id': 'M15', 'name': 'BLM+Constriction (GB_d²×T)',
            'formula': 'ln(R) = α·ln(GB_d²×T) + ln(C)',
            'formula_R': 'R = C·(GB_d²×T)^α',
            'params': {'α': round(slope, 4), 'ln(C)': round(intercept, 4)},
            'n_params': 2, 'R2': round(r**2, 4), 'n': n,
            'physics': 'BLM(입계 수) + Maxwell Constriction(접촉면적) → GB_d² × T',
            'derivation': True,
        })
    except: pass

    # M6: Power Law (GB_d, T 독립) — ln(R) = a·ln(GB_d) + b·ln(T) + c
    try:
        logGB = np.log(gb)
        logT = np.log(T)
        X = np.column_stack([logGB, logT, np.ones(n)])
        beta, res, _, _ = np.linalg.lstsq(X, logR, rcond=None)
        pred = X @ beta
        ss_res = np.sum((logR - pred)**2)
        ss_tot = np.sum((logR - np.mean(logR))**2)
        r2_m6 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        models.append({
            'id': 'M6', 'name': 'Power Law (GB_d, T 독립)',
            'formula': 'ln(R) = a·ln(GB_d) + b·ln(T) + c',
            'formula_R': 'R = exp(c)·GB_d^a·T^b',
            'params': {'a': round(beta[0], 4), 'b': round(beta[1], 4), 'c': round(beta[2], 4)},
            'n_params': 3, 'R2': round(r2_m6, 4), 'n': n,
            'physics': 'GB_d와 T의 독립적 기여 (M15의 일반화)',
        })
    except: pass

    # M13: Exp+Arrhenius — ln(R) = b·GB_d + c/T + d
    try:
        invT = 1.0 / T
        X = np.column_stack([gb, invT, np.ones(n)])
        beta, res, _, _ = np.linalg.lstsq(X, logR, rcond=None)
        pred = X @ beta
        ss_res = np.sum((logR - pred)**2)
        ss_tot = np.sum((logR - np.mean(logR))**2)
        r2_m13 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        models.append({
            'id': 'M13', 'name': 'Exponential + Arrhenius',
            'formula': 'ln(R) = b·GB_d + c/T + d',
            'formula_R': 'R = exp(d)·exp(b·GB_d)·exp(c/T)',
            'params': {'b': round(beta[0], 4), 'c': round(beta[1], 4), 'd': round(beta[2], 4)},
            'n_params': 3, 'R2': round(r2_m13, 4), 'n': n,
            'physics': '기존 Exp decay + 두께 보정(Arrhenius형)',
        })
    except: pass

    # C1: Linear — R = a·GB_d + c
    try:
        slope, intercept, r, _, _ = sp_stats.linregress(gb, R)
        models.append({
            'id': 'C1', 'name': 'Linear',
            'formula': 'R = a·GB_d + c',
            'formula_R': 'R = a·GB_d + c',
            'params': {'a': round(slope, 4), 'c': round(intercept, 4)},
            'n_params': 2, 'R2': round(r**2, 4), 'n': n,
            'physics': 'R_total = R_bulk + n·R_gb 단순 직렬저항',
        })
    except: pass

    # C2: Series Resistance (원점) — R = 1 + a·GB_d
    try:
        R_shifted = R - 1
        a_c2 = np.sum(gb * R_shifted) / np.sum(gb**2)
        pred = 1 + a_c2 * gb
        ss_res = np.sum((R - pred)**2)
        ss_tot = np.sum((R - np.mean(R))**2)
        r2_c2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        models.append({
            'id': 'C2', 'name': 'Series Resistance (원점)',
            'formula': 'R = 1 + a·GB_d',
            'formula_R': 'R = 1 + a·GB_d',
            'params': {'a': round(a_c2, 4)},
            'n_params': 1, 'R2': round(r2_c2, 4), 'n': n,
            'physics': 'R_total = R_bulk + (R_gb/R_bulk)·GB_d',
        })
    except: pass

    # Sort by R² descending
    models.sort(key=lambda m: m['R2'], reverse=True)
    return models


def generate_report(data_list, names, outdir):
    """Generate comprehensive fitting analysis markdown report."""
    rows = _extract(data_list, names)
    if len(rows) < 3:
        return None

    models = _fit_models(rows)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    n = len(rows)

    # Find recommended model
    m15 = next((m for m in models if m['id'] == 'M15'), None)
    best = models[0] if models else None

    L = []
    L.append(f"# Production Scaling Laws Report")
    L.append(f"*Generated: {now} | n = {n} cases | DEM Analyzer v2.0*\n")

    L.append("**T1 (σ_ionic) + Stage 15 (σ_electronic) production forms — corpus 최신 fit.**")
    L.append("legacy proxy model (BLM+Constriction R 비교) / 9-model bake-off 등은 폐기됨.\n")

    # ─── 1. 목적 ───
    L.append("## 1. 목적\n")
    L.append("DEM corpus 의 두 production scaling law (σ_ionic T1, σ_electronic Stage 15) 에 대해")
    L.append("현재 데이터로 live-refit 후 결과를 한 문서에 정리.\n")
    L.append("- **T1 (σ_ionic)**: 2026-05-28 채택. cov_Hertz + power-gate g_phys + Cronau + P2 + log f_intact")
    L.append("- **Stage 15 (σ_electronic)**: 2026-05-29 채택. φ_AM⁴ + NCM(r̄) + √A_AM-AM + β_AC·φ_AM·log(CN)\n")

    # ─── 2. 데이터 요약 ───
    L.append("## 2. 데이터 요약\n")
    L.append(f"| 항목 | 범위 |")
    L.append(f"|------|------|")
    gb_vals = [r['gb_d'] for r in rows]
    T_vals = [r['T'] for r in rows]
    R_vals = [r['R'] for r in rows]
    L.append(f"| n (유효 데이터) | {n} |")
    L.append(f"| GB_d | {min(gb_vals):.2f} ~ {max(gb_vals):.2f} hops/μm |")
    L.append(f"| T (두께) | {min(T_vals):.0f} ~ {max(T_vals):.0f} μm |")
    L.append(f"| R (ratio) | {min(R_vals):.1f} ~ {max(R_vals):.1f} |")
    L.append("")

    L.append("### 케이스별 데이터\n")
    L.append("| Case | GB_d | T(μm) | τ | φ_SE | f_perc | σ_brug | σ_proxy | R |")
    L.append("|------|------|-------|---|------|--------|--------|---------|---|")
    for r in sorted(rows, key=lambda x: x['R']):
        L.append(f"| {r['name']} | {r['gb_d']:.3f} | {r['T']:.0f} | {r['tau']:.2f} | "
                 f"{r['phi_se']:.4f} | {r['f_perc']:.3f} | {r['sigma_brug']:.6f} | "
                 f"{r['sigma_proxy']:.6f} | {r['R']:.1f} |")
    L.append("")

    # ─── 3. Network Solver 결과 (formerly Section 8) ───
    L.append("## 3. Network Solver (Kirchhoff) 결과\n")
    L.append("Proxy R=15~1600은 single-path 근사에 의한 과장.\n"
             "Kirchhoff network solver(R_bulk + R_constriction per edge, Holm 1967)로\n"
             "Contact-free/Full ratio = **3~10×** 확인.\n")
    L.append("")

    # Network solver data if available
    net_rows = []
    for i, d in enumerate(data_list):
        sigma_net = d.get('sigma_full_mScm', 0)
        sigma_brug_ms = d.get('sigma_ratio', 0) * 3.0
        bulk_frac = d.get('bulk_resistance_fraction')
        if sigma_net and sigma_net > 0:
            ratio = sigma_brug_ms / sigma_net if sigma_net > 0 else 0
            constr_pct = (1 - bulk_frac) * 100 if bulk_frac else None
            net_rows.append({
                'name': names[i], 'sigma_net': sigma_net,
                'sigma_brug_ms': sigma_brug_ms, 'ratio': ratio,
                'constr_pct': constr_pct,
            })

    if net_rows:
        L.append("| Case | σ_ionic (mS/cm) | σ_Bruggeman (mS/cm) | σ_brug/σ_ionic | Constriction% |")
        L.append("|------|-----------------|---------------------|----------------|---------------|")
        for r in sorted(net_rows, key=lambda x: x['sigma_net'], reverse=True):
            c_str = f"{r['constr_pct']:.0f}%" if r['constr_pct'] else '-'
            L.append(f"| {r['name']} | {r['sigma_net']:.4f} | {r['sigma_brug_ms']:.4f} | {r['ratio']:.1f}× | {c_str} |")
        L.append("")

        avg_ratio = np.mean([r['ratio'] for r in net_rows])
        avg_constr = np.mean([r['constr_pct'] for r in net_rows if r['constr_pct']])
        L.append(f"- **평균 σ_brug/σ_ionic**: {avg_ratio:.1f}× (Bruggeman 과대추정)")
        if avg_constr:
            L.append(f"- **평균 Constriction 비율**: {avg_constr:.0f}% (접촉 저항 지배)")
        L.append("")
    else:
        L.append("*Network solver 결과 없음 (Network Solver 재실행 필요)*\n")

    # ─── 4. Production Scaling Laws (live-fit on corpus) ───
    L.append("## 4. Production Scaling Laws (live-fit)\n")

    # ── Ionic — T1 PRODUCTION form (2026-05-28: cov_Hertz + power gate + P2 + f_intact)
    # σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov_Hertz^½ · f_p³
    #     · exp[a + b·ln τ + c·(ln τ)² + β_P2·P2 + β_F·log f_intact]
    ion_r2, ion_loo, ion_b, ion_n = None, None, None, 0
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import generate_comparison_plots as gcp
        bl, ls, ts, phi_a, rse_a, dcov_a, p_a, fi_a = gcp._stage_e_base_arrays(data_list)
        ion_n = len(ts)
        if ion_n >= 8:
            extras, _ = gcp._c4_extras_from_arrays(phi_a, rse_a, dcov_a,
                                                   p_arr=p_a, fi_log_arr=fi_a)
            ion_r2, ion_loo, _Ct, _Cn, _pred, ion_b, _ = gcp._cblend_fit_score(
                bl, ls, ts, extras=extras)
    except Exception as _e:
        ion_r2, ion_loo, ion_n = None, None, 0

    if ion_r2 is not None:
        L.append(f"### Ionic — T1 PRODUCTION form (R²={ion_r2:.3f}, "
                 f"LOOCV={ion_loo:.3f}, n={ion_n}, 5 free params)\n")
    else:
        L.append(f"### Ionic — T1 PRODUCTION form (corpus too small: n={ion_n}<8, "
                 "show schema only)\n")
    L.append("```")
    L.append("σ_ionic = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov_Hertz^½ · f_p³")
    L.append("        · exp[ a + b·ln τ + c·(ln τ)² + β_P2·P2 + β_F·log f_intact ]")
    L.append("")
    L.append("  φ_eff   = √[ (φ − φc_eff)² + (δ · g_phys)² ]")
    L.append("  φc_eff  = (1 − g_phys)·0.200 + g_phys·0.195      [SAT-blend]")
    L.append("  g_phys  = (min(3.5 µm / r̄_AM, 1))^2              [power-law size gate]")
    L.append("  r̄_AM   = (1−p)·r_AM,S + p·r_AM,P                 (composition-weighted)")
    L.append("  P2      = g_phys · (φ − 0.195)² · (r_SE − 0.5)+   [Cronau super-µm arm]")
    L.append("  f_intact = 1 − fracture_aware_excluded_pct / 100")
    L.append("  Cronau(r) = 0.33 + 0.32·σ(50(r−0.10)) + 0.25·σ(50(r−0.30))")
    L.append("                                       + 0.10·σ(50(r−0.50))   [3-sigmoid]")
    L.append("")
    L.append("FROZEN:  σ_grain=3.0 mS/cm, δ=0.040, φc_P=0.200, φc_S=0.195,")
    L.append("         r_cut=3.5 µm (power-gate cutoff), α=2 (power-gate exponent)")
    if ion_b is not None and len(ion_b) >= 5:
        L.append(f"LIVE-fit: a={ion_b[0]:+.3f}  b={ion_b[1]:+.3f}  c={ion_b[2]:+.3f}  "
                 f"β_P2={ion_b[3]:+.3f}  β_F={ion_b[4]:+.3f}")
    L.append("```\n")


    # ── Electronic — Stage 22 PRODUCTION form (2026-06-03, Trevisanello-locked)
    # σ_e = (σ_S·NCM_S)^(1-p) · (σ_P·NCM_P)^p           ← AM material (Trevisanello LOCKED)
    #       · φ_AM⁴ · √A_AM-AM                            ← Bruggeman × Holm (structure)
    #       · (T/d_AM)^β_T · r_SE^β_logrSE                ← geometry
    #       · exp[β_AC·φ·logCN + β_v·v_AM]               ← network corrections
    #       · exp[β_bi·p(1-p)·logφ]                       ← composition coupling
    #       · exp[β_Fe·log f_intact]                      ← fracture (Holm partial)
    #       · exp[g_thin·(β_φth·logφ + β_covth·log cov + β_fpth·log fp)]  ← thin film
    #       · C(τ) = exp[p_τ + q_τ·lnτ + r_τ·ln²τ]        ← tortuosity
    el_r2, el_loo, el_b, el_n = None, None, None, 0
    try:
        # Use the same _electronic_form_arrays + _electronic_fit as the dashboard plot
        # so coefficients here match electronic_fit_final.png.
        arr_e = gcp._electronic_form_arrays(data_list, list(names))
        if arr_e is not None and arr_e['n'] >= 8:
            fit_mask = ~arr_e['excluded']
            fit_e = gcp._electronic_fit(arr_e, fit_mask=fit_mask)
            el_r2, el_loo = fit_e['r2'], fit_e['loocv']
            el_b = fit_e['coef']; el_n = fit_e['n_fit']
    except Exception:
        el_r2, el_loo, el_n = None, None, 0

    if el_r2 is not None:
        L.append(f"### Electronic — Stage 22 PRODUCTION form (R²={el_r2:.3f}, "
                 f"LOOCV={el_loo:.3f}, n={el_n}, 12 free params + 2 LOCKED endpoints)\n")
    else:
        L.append(f"### Electronic — Stage 22 PRODUCTION form (corpus too small: n={el_n}<8, "
                 "show schema only)\n")
    L.append("```")
    L.append("σ_e = (σ_S·NCM_S)^(1-p) · (σ_P·NCM_P)^p")
    L.append("      · φ_AM⁴ · √A_AM-AM · (T/d_AM)^β_T · r_SE^β_logrSE")
    L.append("      · exp[β_AC·φ·log(CN) + β_v·v_AM + β_bi·p(1-p)·logφ + β_Fe·log f_intact]")
    L.append("      · exp[g_thin·(β_φth·logφ + β_covth·log cov_AM,P + β_fpth·log f_p)]")
    L.append("      · C(τ),   C(τ) = exp[p_τ + q_τ·lnτ + r_τ·ln²τ]")
    L.append("")
    L.append("  σ_S = 10 mS/cm LOCKED, σ_P = 5 mS/cm LOCKED  (Trevisanello 2021)")
    L.append("  NCM(r) = 1 / (1 + (r/2µm)^1.5)   per-endpoint GB correction")
    L.append("  p      = AM_P mass fraction (= 1 means pure AM_P, = 0 means pure AM_S)")
    L.append("  φ_AM⁴  : dense-network percolation (locked exponent 4, Stage 14 nested CV)")
    L.append("  √A_AM-AM : Holm 1967 a-spot constriction")
    L.append("  g_thin = σ(-5·(T/d - 8))   thin-film 3D→2D crossover gate")
    L.append("  f_intact = 1 − fracture_aware_excluded_pct/100  살아있는 접촉 비율")
    L.append("")
    L.append("FROZEN: σ_S, σ_P (Trevisanello), a=4 (φ_AM exp), 0.5 (Holm), 1.5 (NCM)")
    if el_b is not None and len(el_b) >= 12:
        sS = float(np.exp(el_b[0])); sP = float(np.exp(el_b[1]))
        L.append(f"LIVE (12 OLS):  β_T={el_b[2]:+.3f}  β_v={el_b[3]:+.3f}  β_AC={el_b[7]:+.3f}")
        L.append(f"                β_φth={el_b[8]:+.3f}  β_covth={el_b[9]:+.3f}  β_bi={el_b[10]:+.3f}")
        L.append(f"                β_Fe={el_b[11]:+.3f}  β_fpth={el_b[12]:+.3f}  β_logrSE={el_b[13]:+.3f}")
        L.append(f"                C(τ) = {el_b[4]:+.2f}{el_b[5]:+.2f}·lnτ{el_b[6]:+.2f}·ln²τ")
        L.append(f"LOCKED:         σ_S={sS:.2f} mS/cm  σ_P={sP:.2f} mS/cm")
    L.append("```\n")

    # Thermal fit
    th_actual = []
    th_pred_rhs = []
    for d in data_list:
        sigma_th = d.get('thermal_sigma_full_mScm', 0)
        sigma_ion = d.get('sigma_full_mScm', 0)
        phi_am = d.get('phi_am', 0)
        cn = d.get('se_se_cn', 0)
        if sigma_th and sigma_th > 0 and sigma_ion > 0 and phi_am > 0 and cn > 0:
            rhs = sigma_ion**0.75 * phi_am**2 / cn
            th_actual.append(sigma_th)
            th_pred_rhs.append(rhs)

    if len(th_actual) >= 3:
        th_actual = np.array(th_actual)
        th_pred_rhs = np.array(th_pred_rhs)
        th_C = float(np.exp(np.mean(np.log(th_actual / th_pred_rhs))))
        th_pred = th_C * th_pred_rhs
        log_a, log_p = np.log(th_actual), np.log(th_pred)
        ss_res = np.sum((log_a - log_p)**2)
        ss_tot = np.sum((log_a - np.mean(log_a))**2)
        th_r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    L.append(f"### Thermal (R²={th_r2:.2f}, 1 free parameter)" if th_r2 else "### Thermal")
    L.append("```")
    L.append("σ_th = C × σ_ion^(3/4) × φ_AM² / CN_SE")
    L.append(f"C = {th_C:.1f} (data-fitted)" if th_C else "C ≈ 286 (default)")
    L.append("```\n")

    # Summary table
    L.append("### Summary\n")
    L.append("| Transport | R² | LOOCV | free params | n |")
    L.append("|-----------|-----|-------|------------|---|")
    if ion_r2 is not None:
        L.append(f"| Ionic (T1) | {ion_r2:.3f} | {ion_loo:.3f} | 5 (a,b,c,β_P2,β_F) | {ion_n} |")
    else:
        L.append("| Ionic (T1) | - | - | 5 | 0 |")
    if el_r2 is not None:
        L.append(f"| Electronic (Stage 15) | {el_r2:.3f} | {el_loo:.3f} | 8 (σ_S,σ_P,β_T,β_v,p,q,r,β_AC) | {el_n} |")
    else:
        L.append("| Electronic (Stage 15) | - | - | 8 | 0 |")
    L.append(f"| Thermal | {th_r2:.2f} | - | 1 (C) | {len(th_actual)} |" if th_r2 else "| Thermal | - | - | 1 | 0 |")
    L.append("")

    # ─── 5. σ_ionic 항별 친절 설명 (formerly Section 10) ───
    L.append("## 5. σ_ionic (T1) 항별 친절 설명\n")
    L.append("각 항이 무슨 물리를 잡고 있는지, 왜 그 지수/형태가 채택됐는지를 한 줄씩.\n")

    L.append("### σ_grain · Cronau(r_SE) — 재료 기준선")
    L.append("- **σ_grain = 3.0 mS/cm** — Cronau 2022가 측정한 Li₆PS₅Cl **single-crystal** ionic conductivity.")
    L.append("  pellet 값(1.3 mS/cm)이 아니라 grain interior 값을 써야 form이 '입자 안→입자 안'의 전도를")
    L.append("  계산하는 게 됨. GB/접촉 손실은 다른 항이 따로 잡음.")
    L.append("- **Cronau(r_SE)** — 같은 Cronau 2022가 보고한 sub-µm grain interior 자체의 conductivity 감소.")
    L.append("  r_SE ≥ 1µm: ×1.0, 0.5µm: ×0.65, 0.3µm: ×0.50, 0.1µm 이하: ×0.33.")
    L.append("  3개 sigmoid를 매끄럽게 이어붙인 형태 (불연속 piecewise 대신).")
    L.append("  물리: 작은 입자는 표면 amorphization 비율이 커서 grain bulk 자체 conductivity가 낮아짐.\n")

    L.append("### (φ_eff)^½ — Mean-field 3D percolation")
    L.append("- **φ = SE 부피분율**, **φc = SE percolation threshold (~0.20)**.")
    L.append("- 임계점 위로 충분히 떨어진 영역에서 σ ∝ √(φ − φc) (mean-field 3D scaling).")
    L.append("- **φ_eff = √[(φ−φc_eff)² + (δ·g_phys)²]** — threshold 근처에서 √이 갑자기 0으로 떨어지는")
    L.append("  것을 disorder rounding (δ=0.040)으로 부드럽게 만든 형태. φc_eff는 P-heavy(0.200)와")
    L.append("  S-heavy(0.195) 사이를 g_phys로 blend (SAT-blend).")
    L.append("- 91/91 case에서 nested CV exponent scan 결과 0.5 lock-in.\n")

    L.append("### CN² — Kirchhoff network 병렬 경로")
    L.append("- **CN** = SE-SE coordination number (입자당 평균 이웃 수).")
    L.append("- Kirchhoff 해석: CN이 2배면 (a) 병렬 경로 수가 2배, (b) 각 경로의 bond strength도 약간 향상")
    L.append("  → CN²로 scale. 정확히 1.0도 2.0도 아닌 데이터-locked 지수.")
    L.append("- exp_S/exp_CN scan 91/91 case 모두 2.0 선택 → 가장 강한 단일 contributor")
    L.append("  (ablation: CN² 빼면 LOOCV −0.307).\n")

    L.append("### cov_Hertz^½ — Holm 1967 constriction resistance")
    L.append("- **cov** = 한 SE 입자가 다른 SE 입자에 의해 덮이는 표면 비율 (contact area fraction).")
    L.append("- Holm 1967: 두 입자 간 전류는 √(contact area)에 비례 (spreading/constriction).")
    L.append("- **왜 Hertz냐?** 원래 Tabor adhesion 보정된 cov_physics를 썼는데, Spearman ρ(σ, cov_Hertz)")
    L.append("  =0.697 > ρ(σ, cov_physics)=0.476. 해석: Tabor 부착으로 생기는 부가 접촉 면적은")
    L.append("  기하학적으론 존재해도 vdW gap 때문에 Li⁺ 전도에는 기여 안 함 → '유효 Li⁺ 전도 면적'은")
    L.append("  elastic Hertz 면적임. (T1 adoption, 2026-05-28.)\n")

    L.append("### f_p³ — 3D isotropy")
    L.append("- **f_p** = percolating SE 비율 (= percolation_pct/100).")
    L.append("- 3D에서 σ가 잘 흐르려면 x, y, z 세 방향 모두 percolate해야 함.")
    L.append("- 단순 독립 가정: P(perc-x ∧ perc-y ∧ perc-z) = f_p³. Stauffer-Bruggeman backbone scaling과 일치.\n")

    L.append("### exp[a + b·ln τ + c·(ln τ)²] — tortuosity prefactor (logpoly2)")
    L.append("- **τ** = recommended tortuosity (path-length ratio).")
    L.append("- 단순 1/τ나 1/τ²로는 데이터 곡선을 못 잡음 → ln τ의 2차 다항식을 OLS로 live-fit.")
    L.append("- 이전 dual-branch (P/S 따로 6 params) 대비 ΔAIC = −10.6, ΔBIC = −18.2로 결정적 우위.")
    L.append("  파라미터 수 6→3으로 n/k overfit margin 2배 (15:1 → 30:1).\n")

    L.append("### β_P2·P2 — Cronau super-µm arm (corner correction)")
    L.append("- **P2 = g_phys · (φ − 0.195)² · (r_SE − 0.5)+** — g_phys로 게이트되어 62:38·D1+(=r_SE≥1µm)")
    L.append("  corner에서만 fire함.")
    L.append("- 물리: r_SE ≥ 0.5µm에서 Cronau는 ×1.0으로 saturate되지만, 실제 데이터에서 그 위로도 σ가")
    L.append("  추가 enhancement를 보임 → '상한선이 0.5µm가 아니라 더 멀리 가는' 보정.")
    L.append("- **Leave-corner-out generalization test PASSED** (sign-consistent, corner RMSE −0.119).\n")

    L.append("### β_F · log f_intact — fracture-aware Holm")
    L.append("- **f_intact = 1 − fracture_aware_excluded_pct/100** — fracture solver가 끊겼다고 본 접촉의")
    L.append("  여집합 (살아있는 접촉 비율).")
    L.append("- β ≈ +0.19 — '끊어진 접촉도 100% 잃는 게 아니라 micro-asperity로 ~60% 전도 유지'를")
    L.append("  의미하는 partial-Holm 보정.")
    L.append("- 단순 multiplicative f_intact (β=1) 대신 log-linear로 부드럽게.\n")

    L.append("### g_phys (power-law size gate) — label-free small-AM dominance")
    L.append("- **g_phys = (min(3.5µm / r̄_AM, 1))²**, r̄_AM = composition-weighted AM radius.")
    L.append("- 합성품 AM이 reference size 3.5µm보다 X배 크면 small-AM 기여가 1/X² (inverse-square,")
    L.append("  cross-section scaling).")
    L.append("- 이전엔 P:S label (10:0 vs 0:10) 기반 g_010 sigmoid 썼는데, label-convention 의존을 없애려고")
    L.append("  size 기반으로 교체. 데이터에 +0.0009 LOOCV 손해 없음, borderline 케이스 (input_S_2 r_AM_S=4µm)")
    L.append("  처리에서 더 정확.\n")

    L.append("### 항별 신뢰도 요약\n")
    L.append("| 항 | 신뢰도 | 근거 |")
    L.append("|---|---|---|")
    L.append("| σ_grain | HIGH | Cronau 2022 literature |")
    L.append("| Cronau(r_SE) | HIGH | Cronau 2022 piecewise (smoothed) |")
    L.append("| (φ_eff)^½ | MED-HIGH | mean-field 3D percolation; data-locked 91/91 |")
    L.append("| CN² | MED-HIGH | Kirchhoff network; locked 91/91 |")
    L.append("| cov_Hertz^½ | HIGH | Holm 1967 + Spearman 0.697>0.476 |")
    L.append("| f_p³ | MED | 3D isotropy + Stauffer-Bruggeman |")
    L.append("| C_blend(τ) logpoly2 | MED | ΔAIC −10.6 vs dual-branch |")
    L.append("| β_P2·P2 | MED | leave-corner-out PASSED |")
    L.append("| β_F·log f_intact | MED | fracture-aware partial-Holm |")
    L.append("| g_phys (power gate) | MED-HIGH | inverse-square + Alt-C scan 우승 |")
    L.append("")

    L.append("### 채택 history (각 단계 LOOCV로 검증)\n")
    L.append("| Step | LOOCV | ΔLOOCV |")
    L.append("|---|---|---|")
    L.append("| Baseline (bare √(φ−0.19)) | 0.9499 | — |")
    L.append("| + SAT-blend (φc_eff, δ) | 0.9578 | +0.0049 |")
    L.append("| × Cronau(r_SE) | 0.9640 | +0.0062 |")
    L.append("| C_blend → logpoly2 | 0.9660 | +0.0020 (+ΔAIC −10.6) |")
    L.append("| smooth f_small → power gate (α=2) | 0.9670 | +0.0010 |")
    L.append("| + β_P2·P2 | 0.9687 | +0.0017 |")
    L.append("| + β_F·log f_intact | 0.9710 | +0.0023 |")
    L.append("| T1: cov_physics → cov_Hertz | **0.9712** | +0.0002 (k 6→5) |")
    L.append("")

    L.append("**FINAL production**: LOOCV ≈ 0.975 (n=88-92), 5 fit params, noise ceiling.\n")

    # ─── 6. σ_electronic 항별 친절 설명 ───
    L.append("## 6. σ_electronic (Stage 22) 항별 친절 설명\n")
    L.append("σ_ionic과 마찬가지로 각 항이 무슨 물리를 잡고 있는지, 왜 그 형태가 채택됐는지 한 줄씩.")
    L.append("σ_e form은 14개 항으로 구성되지만 물리적으로는 **3 카테고리**:\n")
    L.append("- 🟢 **재료 한계** — AM 재료 자체가 최대 얼마까지 전도 가능한가")
    L.append("- 🔵 **구조 손실** — AM 네트워크 모양/연결성에 의한 감소")
    L.append("- 🟡 **경로 보정** — 미세 환경 보정 (saturation, fracture, thin-film, tortuosity)\n")

    # ── 🟢 재료 한계 (Material limits) ──
    L.append("### 🟢 재료 한계 (재료 자체의 전도 가능 최대치)\n")

    L.append("#### (σ_S · NCM_S)^(1-p) · (σ_P · NCM_P)^p — Trevisanello endpoint mix")
    L.append("- **σ_S = 10 mS/cm, σ_P = 5 mS/cm — Trevisanello 2021 LOCKED**.")
    L.append("  S-rich polycrystalline NCM (작은 단결정 입자 집합체)는 큰 입자 NCM_P 보다 2배 σ_e 높음.")
    L.append("  Stage 21까지는 live-fit (data가 σ_S≈9, σ_P≈4로 학습), Stage 22에서 문헌값으로 lock.")
    L.append("- **p = AM_P mass fraction** (0이면 순수 AM_S, 1이면 순수 AM_P).")
    L.append("- **(1−p) / p 지수**: 두 endpoint의 geometric mix — Bruggeman effective medium에서 자연스러운 형태.")
    L.append("  '복합체 σ_e는 두 종류 AM 단결정 conductivity의 (mass-weighted) 기하 평균'.")
    L.append("- **물리**: 같은 양이라도 P-rich(큰 단결정)이 S-rich(다결정 집합체)보다 전자 conductivity 절반.")
    L.append("  Trevisanello 2021 실측 (단결정 vs 다결정 NMC811): ratio ≈ 2.0× 일치.\n")

    L.append("#### NCM_S, NCM_P = 1/(1 + (r/2µm)^1.5) — Trevisanello GB correction")
    L.append("- **각 endpoint의 입자 크기에 따른 grain-boundary penalty**.")
    L.append("  r = particle radius (µm). r=2µm 기준점에서 ×0.5, r=5µm에서 ×0.18.")
    L.append("- **물리**: 다결정 NCM 입자 내부에는 primary-grain 경계 (GB)가 있어 전자 전도 막음.")
    L.append("  큰 secondary particle일수록 내부 GB 더 많음 → σ_e 감소.")
    L.append("- 지수 1.5는 Trevisanello 2021 fit. r_AM_S와 r_AM_P 각각 따로 적용 (Stage 16 endpoint-separate).\n")

    # ── 🔵 구조 손실 (Structural losses) ──
    L.append("### 🔵 구조 손실 (네트워크 모양/연결성에 의한 감소)\n")

    L.append("#### φ_AM⁴ — Bruggeman / percolation power law")
    L.append("- **φ_AM = AM 부피분율**. 4제곱 = AM 부피분율 작아지면 σ_e가 매우 급격히 감소.")
    L.append("- **물리**: AM-AM 네트워크가 percolating cluster 형성해야 전자 흐름. AM 적으면 cluster 작아짐 → 길 끊김.")
    L.append("- Bruggeman EMT의 standard 3D 분산상 exponent. Stage 14 nested CV가 4를 lock-in.")
    L.append("  '전해질 충분히 있어야 이온 통로 형성된다'를 mirroring한 '활물질 충분히 있어야 전자 통로 형성'.\n")

    L.append("#### √A_AM-AM — Holm 1967 constriction")
    L.append("- **A_AM-AM = AM-AM 평균 접촉 면적 (μm²)**.")
    L.append("- Holm 1967: 두 입자 사이 전류는 √(contact area)에 비례 (spreading/constriction resistance).")
    L.append("- **물리**: 접촉 면적 클수록 전자 잘 흐름. 단순 비례 아니라 √ — 면적 2배되면 전류 √2배만 늘어남.")
    L.append("  (current spreads through narrow 'a-spot' constriction at the contact.)")
    L.append("- σ_ionic의 cov_Hertz^½ 와 같은 물리. σ_e는 AM-AM 면적, σ_ionic은 SE-SE 면적.\n")

    L.append("#### (T/d_AM)^β_T — Pouillet thickness penalty")
    L.append("- **T = 전극 두께, d_AM = 평균 AM 직경**. T/d_AM = 전극 두께가 AM 입자 크기의 몇 배인가.")
    L.append("- **β_T 음수 (live-fit)** → 두꺼울수록 σ_e 감소.")
    L.append("- **물리**: 전자가 위→아래로 가는 길이 길수록 저항 커짐 (Pouillet law). 단순 1/T 아니라")
    L.append("  d_AM으로 정규화 — 같은 두께라도 AM이 크면 (= 적은 layer 수) 길이 짧음.\n")

    L.append("#### r_SE^β_logrSE — SE size effect on AM-AM contacts")
    L.append("- **r_SE = SE 입자 반지름 (µm)**. β_logrSE 양수 (live-fit) → SE 클수록 σ_e 증가.")
    L.append("- **물리**: 작은 SE는 AM-AM 접촉 사이에 끼어들어 직접 contact을 막음. 큰 SE는 그렇게 못 들어감.")
    L.append("  → AM-AM 직접 접촉 늘어남 → σ_e 증가. Stage 21에서 추가 (Δ +0.003 LOOCV).\n")

    # ── 🟡 경로 보정 (Path corrections) ──
    L.append("### 🟡 경로 보정 (미세 환경 보정)\n")

    L.append("#### exp(β_AC · φ_AM · log CN_AM-AM) — saturation correction")
    L.append("- **CN_AM-AM = AM 입자당 평균 이웃 수 (coordination number)**.")
    L.append("- **β_AC**: data-locked. Stage 22에선 ≈ −0.02~+0.06 (corpus에 따라 변동).")
    L.append("- **물리**: AM 너무 밀집 + 이웃 너무 많으면 saturation — 추가 이웃이 σ_e에 더 기여 안 함.")
    L.append("  Kirchhoff 네트워크의 redundant 병렬 경로 한계. φ × log(CN) coupling 형태 (Stage 15 nested CV).\n")

    L.append("#### exp(β_v · v_AM) — AM vulnerability")
    L.append("- **v_AM = AM_S_vulnerable_pct/100** — coverage 낮아 SE에 노출 덜 된 AM 비율.")
    L.append("- **물리**: 'vulnerable'한 AM은 fracture 위험 → 일부 전도 잃음. β_v 음수 (vulnerable 많을수록 σ_e 감소).\n")

    L.append("#### exp(β_bi · p(1-p) · log φ_AM) — bimodal coupling")
    L.append("- **p(1-p)**: 0 (순수 P-rich) ~ 0.25 (50:50 mixed) ~ 0 (순수 S-rich).")
    L.append("- **물리**: P-S 혼합이 단일 endpoint보다 packing 효율 좋음 (bimodal sphere packing).")
    L.append("  φ가 같아도 mixed가 더 dense network → σ_e 더 큼. β_bi 음수면 mixed가 +ve boost.")
    L.append("- Stage 19에서 추가 (ΔLOOCV +0.008).\n")

    L.append("#### exp(β_Fe · log f_intact) — fracture-aware Holm")
    L.append("- **f_intact = 1 − fracture_severe_pct/100** — 부서지지 않고 살아있는 AM-AM 접촉 비율.")
    L.append("- **물리**: 압착 중 일부 접촉 균열 발생 (Lawn 1998). 완전히 끊긴 게 아니라 micro-asperity로")
    L.append("  부분 전도 유지. β_Fe ≈ +0.05 (σ_ionic의 +0.19보다 작음 — AM-AM은 SE-SE보다 fracture 민감도 낮음).")
    L.append("- '부서진 접촉도 완전 손실 아님' — σ_ionic의 fracture term과 같은 사상.\n")

    L.append("#### g_thin · [β_φth·logφ + β_covth·log cov_AM,P + β_fpth·log f_p] — thin-film gate")
    L.append("- **g_thin = σ(-5·(T/d_AM − 8))** — sigmoid gate. T/d_AM > 8 (= 두꺼운 전극)이면 g_thin ≈ 0")
    L.append("  → 이 보정 비활성. T/d_AM < 8 (= 얇은 전극)이면 g_thin ≈ 1 → 보정 활성.")
    L.append("- **물리**: 얇은 박막에서는 3D bulk percolation 가정 깨짐 — 2D-like effects 등장:")
    L.append("  - β_φth·logφ — φ 의존성 추가 보정 (3D φ⁴ exponent로는 부족)")
    L.append("  - β_covth·log cov_AM,P — AM_P coverage가 더 중요 (얇으면 AM_P 직접 다리 역할)")
    L.append("  - β_fpth·log f_p — percolation prob의 thin-film 보정 (Stage 21 추가)")
    L.append("- Stage 17/21에서 단계적으로 추가. 모든 thin 케이스 (1mAh family)에서만 fire.\n")

    L.append("#### C(τ) = exp(p_τ + q_τ·lnτ + r_τ·ln²τ) — tortuosity logpoly2")
    L.append("- **τ = tortuosity_electronic_recommended** (전자 경로의 굴곡도).")
    L.append("- **logpoly2** = ln τ의 2차 다항식. σ_ionic과 같은 형태.")
    L.append("- **물리**: 전자 가는 길이 직선에 가까울수록 σ_e ↑. 굴곡이 심하면 그만큼 저항 증가.")
    L.append("  단순 1/τ 또는 1/τ² 안 맞음 → 데이터-driven 2차 다항식이 다양한 굴곡 형태를 흡수.")
    L.append("- 3개 OLS 파라미터 (p_τ, q_τ, r_τ).\n")

    # ── 항별 신뢰도 + 채택 history ──
    L.append("### 항별 신뢰도 요약\n")
    L.append("| 항 | 신뢰도 | 근거 |")
    L.append("|---|---|---|")
    L.append("| σ_S, σ_P (Trevisanello LOCKED) | HIGH | Trevisanello 2021 literature |")
    L.append("| NCM(r) | HIGH | Trevisanello 2021 측정 (단결정 vs 다결정) |")
    L.append("| φ_AM⁴ | MED-HIGH | Bruggeman EMT + Stage 14 nested CV lock |")
    L.append("| √A_AM-AM | HIGH | Holm 1967 (literature 정확히 -½) |")
    L.append("| (T/d_AM)^β_T | MED | Pouillet 두께 의존성 (data-fit) |")
    L.append("| r_SE^β_logrSE | MED | Stage 21 추가, β > 0 직관과 일치 |")
    L.append("| β_AC·φ·log CN | MED | Stage 15 nested CV ΔLOOCV +0.024 |")
    L.append("| β_v·v_AM | MED | fracture-aware, sign 직관 일치 |")
    L.append("| β_bi·p(1-p)·log φ | MED | bimodal packing, Stage 19 추가 |")
    L.append("| β_Fe·log f_intact | MED | Lawn 1998 partial-Holm, β ≈ +0.05 |")
    L.append("| Thin-film gate (3 params) | MED | Stage 17/21 thin-only 활성 |")
    L.append("| C(τ) logpoly2 | MED | σ_ionic T1과 동일 구조 |\n")

    L.append("### 채택 history (각 단계 LOOCV로 검증)\n")
    L.append("| Step | LOOCV | ΔLOOCV |")
    L.append("|---|---|---|")
    L.append("| Stage 0 baseline (σ_ionic-style locked) | −0.76 | — |")
    L.append("| Stage 2 joint OLS + raw-required | +0.48 | +1.22 |")
    L.append("| Stage 4 composition + thickness | 0.76 | +0.07 |")
    L.append("| Stage 12 + outlier exclusion (R1) | 0.88 | +0.12 |")
    L.append("| Stage 15 + β_AC·φ·log CN saturation | 0.91 | +0.024 |")
    L.append("| Stage 17 + thin gates (β_φth, β_covth) | 0.92 | +0.012 |")
    L.append("| Stage 19 + β_bi bimodal coupling | 0.93 | +0.008 |")
    L.append("| Stage 20 + β_Fe·log f_intact (fracture) | 0.95 | +0.020 |")
    L.append("| Stage 21 + β_fpth + β_logrSE | 0.96 | +0.003 |")
    L.append("| Stage 22 σ_S/σ_P LOCKED Trevisanello | **0.96+** | (literature anchor) |")
    L.append("| Stage 22.5 — WEAK BLOCK ablation (drop 4) | **0.9531** | +0.006 (12→8 LIVE) |\n")

    L.append("**FINAL production (Stage 22.5)**: LOOCV ≈ 0.9531, R² 0.9613, n_fit=76, "
             "8 LIVE OLS + 2 LOCKED endpoints (10 total).  n/k = 9.5:1.\n")

    # ─── NEW: LOCKED-exponent validation table (Stage 22.5 close-out) ───
    L.append("### LOCKED 지수 데이터 검증 (corpus-driven literature validation)\n")
    L.append("Stage 22.5 form 채택 후 추가로 **literature-locked exponents가 진짜로 옳은지** ")
    L.append("n=76 corpus에 대해 독립 검증.  0 추가 DOF (log_offset shift만으로 테스트).")
    L.append("`scripts/electronic_locked_exponent_screen.py` 결과 (모든 LOCKED 5개 PASS):\n")

    L.append("| LOCKED 지수 | 값 | 출처 | 검증 결과 | 차점 |")
    L.append("|---|---|---|---|---|")
    L.append("| φ_AM^a Bruggeman | **a = 4** | Stauffer-Bruggeman backbone + Stage 14 nested CV "
             "| ★ exact lock | a=3.5 → ΔLOOCV −0.007 |")
    L.append("| √A_AM-AM Holm | **exp = 0.5** | Holm 1967 constriction "
             "| ★ exact lock | 0.4/0.6 → ±−0.022 (symmetric) |")
    L.append("| NCM(r) β | **β = 1.5** | Trevisanello 2021 GB scaling "
             "| ★ exact lock | β=1.75 → −0.0008 (within noise) |")
    L.append("| C(τ) 차수 | **logpoly2** (3 params) | σ_ionic T1 mirror "
             "| best | logpoly1 → −0.005 (marginal) |")
    L.append("| Bimodal (p(1-p))^a | **a = 1** | symmetric mixing "
             "| ★ within ±0.0003 (noise floor) | a=0.5~2 all equivalent |\n")

    L.append("**해석**:")
    L.append("- 5개 LOCKED 지수 **모두 데이터가 literature value를 골랐거나 noise 안에서 동일**")
    L.append("- 즉 form의 LOCKED core는 over-fit 위험 없이 **literature physics에 그대로 정렬**")
    L.append("- 만약 어느 하나라도 \"DEVIATES\"가 떴다면 → 신규 finding 또는 corpus bias 의심")
    L.append("- 모두 PASS → **paper-grade strong claim**: \"corpus confirms Stauffer-Bruggeman + ")
    L.append("  Holm 1967 + Trevisanello 2021 in NCM-LPSCl composite cathode at production scale\"\n")

    L.append("**중요**: 이 검증은 **0 DOF 비용**.  LOCKED 지수 재fit 시도 (예: NCM β live)는")
    L.append("ΔLOOCV < 0.001 gain at +1 LIVE param 비용 — 명백히 손해. 그대로 LOCK 유지.\n")

    # ─── 7. 한계점 (T1 + Stage 22) ───
    L.append("## 7. 한계점 (T1 + Stage 22)\n")
    L.append("> ⚠ 아래 σ_electronic 항목 일부는 Stage 15 시점 (2026-05-29) 기준 — Stage 22 (2026-06-03)\n")
    L.append("> 까지의 진화를 반영하지 못함. 6번 섹션 (친절 설명)이 최신.\n")
    L.append("### σ_ionic (T1) — 데이터-편향 outlier 잔재\n")
    L.append("- **sibling-tail per-seed anomaly 삭제 완료** (2026-05-29): input_1mAh_9_S5,")
    L.append("  particulate_12_S2, **input_1mAh_8 base + _S5** (new), **input_1mAh_8_AMS base + S4** (new).")
    L.append("  family-level 통계로 식별 후 디스크 삭제. 남은 4-5 sibling 으로 design point 유지.")
    L.append("- **1mAh family-wide systematic bias** (form 한계, 데이터 부족 영역):")
    L.append("  input_1mAh_8_S1/_S3, _1mAh_5_AMP/_AMS, _1mAh_8_AMP 등 1mAh 전반 +25~37% over-prediction.")
    L.append("  → corpus 의 6/8mAh 편중 때문에 σ_S endpoint 가 6/8mAh 쪽으로 calibrated.")
    L.append("  → 진짜 해결: 1mAh seed 추가 (현재 input_1mAh_8_AMS x5, input_1mAh_8 x4 들어옴).")
    L.append("- **특이 케이스 (form-limited isolated single)**:")
    L.append("  - input_8mAh_real_10 (−40%, 4-form-edge 동시 발현)")
    L.append("  - input_S_2 (+27%, 0:10 r_AM_S=4µm borderline)")
    L.append("  - input_particulate_5 (+27%, 0:10 r_SE=0.5 corner)")
    L.append("- **φc_P/φc_S/δ FROZEN**: 재선별 금지 — selection bias (+0.0095) > 노이즈 SE.\n")

    L.append("### σ_electronic (Stage 15) — 1mAh family-wide bias + 데이터 공백\n")
    L.append("- **1mAh family over-prediction +30~45%**: input_1mAh_5 / _5_AMP / _5_AMS,")
    L.append("  input_1mAh_8_AMS_S3 등.  Stage 12 → Stage 15 (φ_AM·log(CN) saturation) 으로")
    L.append("  input_8mAh_real_10 (+56% → +32%), input_6mAh_real_5 (+54% → +34%) 등 dense+CN")
    L.append("  영역은 부분 해결.  그러나 1mAh-specific bias 잔존.")
    L.append("- **데이터 공백 (4개 metric 미수집)**: am_am_n_contacts, am_am_mean_force,")
    L.append("  am_am_n × A total area, coverage_AM_mean — 모두 Stage 14 nested CV 의 다음 후보")
    L.append("  였으나 corpus 의 모든 case 에서 0 → 테스트 불가.  analyze_contacts.py 가 출력하지 않음.")
    L.append("- **β_AC = -0.50** (Stage 14 prediction -0.46 일치): dense+over-coordinated saturation")
    L.append("  의 진정한 물리적 보정.  Stage 14 nested CV Δ+0.024 그대로 production 에 반영.")
    L.append("- **σ_S/σ_P 비대칭 (12.18 / 5.29)**: Trevisanello 단결정/다결정 NCM 보고와 일치.")
    L.append("  Pure-case median ratio 2.39× (audit 검증).\n")

    L.append("### Thermal — 별도 form 없음\n")
    L.append("- 임시 1-param `σ_th = C · σ_ion^(3/4) · φ_AM² / CN_SE` (R²≈0.22). production 아님.")
    L.append("- nested-CV / Bayesian Laplace / Cronau-equivalent 방법론으로 Phase 1 마지막 sub-step 으로")
    L.append("  σ_thermal form 별도 finalization 예정.\n")

    L.append("### 일반\n")
    L.append("- **DEM 접촉 모델 의존**: hooke/hysteresis 모델의 접촉면적이 실제 cold-pressed")
    L.append("  argyrodite 와 일치하는지는 별도 검증 필요.")
    L.append("- **노이즈 floor**: LOOCV-SE ≈ 0.0045 (σ_ionic) / 0.005 (σ_e). 두 channel 모두")
    L.append("  데이터 ceiling 근접.  더 올리려면 데이터, 아니면 Bayesian Laplace ±band 가서야.")
    L.append("")

    L.append("---\n")
    L.append(f"*Report generated by DEM Analyzer v2.0 — Kirchhoff Network Solver + T1/Stage 15 Production Scaling Laws*")

    report_text = '\n'.join(L)
    # Clean up excessive blank lines
    import re
    report_text = re.sub(r'\n{3,}', '\n\n', report_text)

    # Save
    out_path = os.path.join(outdir, 'fitting_report.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    return out_path


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', nargs='+', required=True, help='Input metrics JSON files')
    parser.add_argument('-n', nargs='+', required=True, help='Case names')
    parser.add_argument('-o', required=True, help='Output directory')
    args = parser.parse_args()

    data = _load_metrics(args.i, args.n)
    out = generate_report(data, args.n, args.o)
    if out:
        print(f"Report saved: {out}")
    else:
        print("Not enough valid data for fitting report", file=sys.stderr)
        sys.exit(1)
