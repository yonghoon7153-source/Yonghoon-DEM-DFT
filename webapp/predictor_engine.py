"""
ML Predictor Engine v2.0: 2-Stage Hybrid (GPR + Physics Scaling Laws)
Stage 1: GPR predicts microstructure from DEM design inputs
Stage 2: Physics scaling laws compute conductivity from microstructure

v2.0 Changes (ML Lecture-based improvements):
- K-fold Cross Validation for robust R² estimation
- Feature engineering: d_AM/d_SE ratio, interaction terms
- Multiple kernel comparison (Matern, RBF, RQ)
- φ_c = 0.185 (optimized)
- StandardScaler with ARD-like feature handling
"""
import json
import os
import sys
import warnings
import numpy as np
from pathlib import Path

warnings.filterwarnings('ignore')

# single source of truth for σ_grain + the σ_ion temperature convention (scripts/se_material.py)
_SCRIPTS_DIR = str(Path(__file__).resolve().parent.parent / 'scripts')
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
import se_material

# ═══ Physical Constants ═══
# ★ 2026-07-28: σ_grain now shared with the solvers via se_material (value unchanged, 3.0 mS/cm,
# declared at T_ref = 25 °C).  docs/temp_pressure_capability.md §3-4 / T1-b / T1-e.
SIGMA_GRAIN = se_material.SIGMA_GRAIN_MS_CM_25C   # mS/cm (SE grain interior, @25 °C)
SIGMA_AM = 50.0         # mS/cm (NCM811)

# ═══ Temperature convention — UNIFIED WITH THE SOLVER (audit T1-e, 2026-07-28) ═══
# BEFORE: this file used σ(T)=σ(298)·exp(−Ea/k_B·(1/T−1/298)) (the "σ form") with
#   Ea_SE = 0.30 eV and Ea_AM = 0.50 eV — the latter carrying the literal comment "rough".
#   That Ea_AM was an UNANCHORED number (§F1) and it was applied to σ_e, which
#   (a) contradicts the literature qualitative finding (Reisacher 2023: in the OHMIC regime the
#       electronic response is T-INDEPENDENT — CM-4 33.50 Ω @25 °C vs 43.89 @65 °C, uncorrelated,
#       CM-3 even opposite in sign), and
#   (b) contradicts the DEM/voxel solvers, which do not scale σ_e with T at all.
#   Same T, two code paths, two different answers — see docs/temp_pressure_capability.md §2 ②.
# NOW:
#   σ_ion → se_material (σ·T Kraft-2017 form, T_ref = 25 °C, Ea band 0.29/0.41/0.46, default 0.41)
#   σ_e   → T-INDEPENDENT BY DEFAULT (literature- AND solver-consistent).  The legacy Ea_AM
#           behaviour is still reachable EXACTLY via sigma_e_t_model='legacy_arrhenius', and every
#           response labels which model was used (`sigma_e_T_model`, `temperature_provenance`,
#           `temperature_notes`) so nothing changes silently.
# ⚠ At the UI default (298 K) BOTH models give factor 1.0 → the numbers a user has seen at the
#   default slider position are bitwise unchanged.
SIGMA_E_T_MODELS = ('none', 'legacy_arrhenius')
EA_AM_EV_LEGACY = 0.50   # ⚠ UNANCHORED ('rough' in the pre-2026-07-28 code) — legacy replay only
# The UI slider is in KELVIN and LABELS 298 as "25 °C" (webapp/templates/predictor.html:91).
# Honour that label: slider 298 IS the reference position → maps to exactly se_material.T_REF_C,
# so the reference run keeps factor == 1.0 and 303/318/333 land on exactly 30/45/60 °C.
_UI_T_REF_K = 298.0


def _ui_kelvin_to_celsius(temperature_k):
    """UI slider Kelvin → °C on the convention that the slider's 298 == T_ref (25 °C)."""
    return se_material.T_REF_C + (float(temperature_k) - _UI_T_REF_K)


# ═══ Ionic scaling law — v12-clean v3 (FINAL PRODUCTION MODEL, 2026-04-18) ═══
# σ_ionic = C_blend(τ) × σ_grain × √(φ−φc) × CN^(3/2) × cov^(2/5) × f_p³
#   R²=0.9813, LOOCV=0.9791 (n=57).  See docs/ionic_scaling_law_experiments.md.
# Half-integer exponents are within 5% of the data-native fit. The τ
# dependence lives entirely in C_blend(τ) — a sigmoid blend of a v5 two-level
# prefactor and a poly3-in-lnτ prefactor — whose coefficients are fit live
# from the corpus (self-calibrating). k, τc fixed per the doc (LOOCV-flat).
PHI_C_V12 = 0.20          # percolation threshold (fixed)
PHI_EX_FLOOR = 1e-4       # critical: 0.001 floor over-predicted sub-φc cases
V12_TAU_K = 20.0          # blend sigmoid steepness w(τ)=σ(k(τ−τc))
V12_TAU_C = 1.92          # blend sigmoid center
V12_V5_K = 5.0            # C_v5 inner sigmoid steepness
V12_V5_C = 2.1            # C_v5 inner sigmoid center


def _v12_base_log(phi_se, cn, tau, cov_frac, f_perc_frac):
    """log of the v12-clean v3 base term (no C_blend prefactor)."""
    phi_ex = max(phi_se - PHI_C_V12, PHI_EX_FLOOR)
    return (np.log(SIGMA_GRAIN) + 0.5 * np.log(phi_ex) + 1.5 * np.log(max(cn, 1e-6))
            + 0.4 * np.log(max(cov_frac, 1e-6)) + 3.0 * np.log(max(f_perc_frac, 1e-3)))


def fit_ionic_v12(rows):
    """Fit C_blend(τ) = a + b·ln τ + c·(ln τ)²  (logpoly2, 3 OLS params) for
    the ionic σ law from corpus rows.

    Returns a params dict {'b': [a, b, c]} or None when too few usable rows.
    The legacy {'b_v5', 'b_p3'} dual-branch was retired 2026-05-28 after
    scripts/screen_form_simplifications.py confirmed logpoly2 wins on LOOCV
    (0.9620 vs 0.9600) AND AIC (-10.6) AND BIC (-18.2) AT HALF the params.
    `predict_ionic_v12` accepts both schemas for backwards compatibility."""
    log_resid, taus = [], []
    for r in rows:
        phi_se, cn, tau = r.get('phi_se', 0), r.get('cn', 0), r.get('tau', 0)
        sig = r.get('sigma_ion', 0)
        cov = max(r.get('coverage', 0.20), 0.01)
        fp = max(r.get('f_perc', 0) / 100.0, 1e-3)
        if not (phi_se > PHI_C_V12 and cn > 0 and tau > 0 and sig > 0.01):
            continue
        log_resid.append(np.log(sig) - _v12_base_log(phi_se, cn, tau, cov, fp))
        taus.append(tau)
    if len(taus) < 5:
        return None
    taus = np.asarray(taus)
    y = np.asarray(log_resid)
    log_tau = np.log(np.maximum(taus, 1e-6))
    X = np.column_stack([np.ones(len(taus)), log_tau, log_tau**2])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return {'b': b.tolist()}


def predict_ionic_v12(params, phi_se, cn, tau, cov_frac, f_perc_frac):
    """Predict σ_ionic (mS/cm) with the production law + fitted logpoly2 C_blend(τ).
    Accepts both the new {'b': [a, b, c]} schema and the legacy
    {'b_v5', 'b_p3'} dual-branch schema for backwards compatibility."""
    if not params:
        return 0.0
    base = np.exp(_v12_base_log(phi_se, cn, tau, cov_frac, f_perc_frac))
    log_t = np.log(max(tau, 1e-6))
    if 'b' in params:
        # Production: logpoly2  a + b·ln τ + c·(ln τ)²
        a_, b_, c_ = params['b']
        return float(base * np.exp(a_ + b_*log_t + c_*log_t**2))
    # Legacy dual-branch schema (kept for old saved fits)
    pv = params['b_v5'][0] + params['b_v5'][1] / (1.0 + np.exp(-V12_V5_K * (tau - V12_V5_C)))
    pp = (params['b_p3'][0] + params['b_p3'][1] * log_t
          + params['b_p3'][2] * log_t**2 + params['b_p3'][3] * log_t**3)
    w = 1.0 / (1.0 + np.exp(-V12_TAU_K * (tau - V12_TAU_C)))
    return float(base * np.exp((1 - w) * pv + w * pp))

INPUT_FEATURES = [
    'd_se', 'd_am', 'am_pct', 'ps_frac', 'rve', 'loading',
    'd_ratio', 'am_loading', 'se_density_proxy', 'layer_count',
    # v2.0: Lecture 5 feature engineering — interaction & nonlinear
    'size_ratio_inv',   # d_AM/d_SE (packing regime determinant!)
    'am_se_interaction', # am_pct × (1-ps_frac) — composition coupling
    'log_d_se',         # log transform (nonlinear)
]

# Core targets (always included)
CORE_TARGETS = [
    'phi_se', 'phi_am', 'sigma_brug', 'tau', 'cn', 'gb_d', 'g_path',
    'hop_area', 'f_perc', 'thickness', 'porosity', 'am_cn', 'sigma_ion',
    'coverage'
]
# Additional targets auto-discovered from full_metrics.json
# Will be populated dynamically during data loading
MICRO_TARGETS = list(CORE_TARGETS)  # starts with core, expands in train_models()

# Cached models (module-level)
_cached_models = None
_training_data_count = 0


def derive_features(d_se, d_am, am_pct, ps_frac, rve, loading):
    """Compute derived features from basic inputs.
    v2.0: Added feature engineering from ML lectures (Lecture 5 φ mapping)."""
    return {
        'd_se': d_se,
        'd_am': d_am,
        'am_pct': am_pct,
        'ps_frac': ps_frac,
        'rve': rve,
        'loading': loading,
        'd_ratio': d_se / d_am if d_am > 0 else 0.1,
        'am_loading': am_pct * loading / 100,
        'se_density_proxy': (100 - am_pct) / max(d_se, 0.1),
        'layer_count': loading * 30 / max(d_se, 0.1),
        # v2.0 features
        'size_ratio_inv': d_am / d_se if d_se > 0 else 10,  # McGeary packing regime
        'am_se_interaction': am_pct * (1 - ps_frac) / 100,   # composition coupling
        'log_d_se': np.log(max(d_se, 0.1)),                  # nonlinear transform
    }


def load_training_data(results_folder, archive_folder):
    """Load all cases with DEM input + output from results and archive."""
    rows = []
    _skip_reasons = {}  # name → reason (for logging)
    for base in [Path(results_folder), Path(archive_folder)]:
        if not base.is_dir():
            continue
        for met_path in base.rglob('full_metrics.json'):
            case_dir = met_path.parent
            ip_path = case_dir / 'input_params.json'
            try:
                with open(met_path) as f:
                    m = json.load(f)
                ip = {}
                if ip_path.exists():
                    with open(ip_path) as f:
                        ip = json.load(f)
            except Exception:
                continue

            _case_name = case_dir.name
            if not m.get('phi_se'):
                _skip_reasons[_case_name] = 'no phi_se'
                continue

            scale = ip.get('scale', 1000)
            r_se = ip.get('r_SE', 0)
            d_se = r_se / scale * 1e6 * 2 if r_se > 0 and scale > 0 else 0
            r_am_p = ip.get('r_AM_P', 0)
            d_am_p = r_am_p / scale * 1e6 * 2 if r_am_p > 0 else 0
            r_am_s = ip.get('r_AM_S', 0)
            d_am_s = r_am_s / scale * 1e6 * 2 if r_am_s > 0 else 0

            am_se_str = ip.get('am_se_ratio', '')
            am_pct = 0
            if ':' in str(am_se_str):
                try:
                    am_pct = float(str(am_se_str).split(':')[0])
                except Exception:
                    pass

            ps = m.get('ps_ratio', '')
            ps_frac = 0.5
            if isinstance(ps, str) and ':' in ps:
                try:
                    parts = ps.split(':')
                    p, s = float(parts[0]), float(parts[1])
                    ps_frac = p / (p + s) if (p + s) > 0 else 0.5
                except Exception:
                    pass

            box_x = ip.get('box_x', 0.05)
            rve = box_x / scale * 1e6 if scale > 0 else 50

            if d_se <= 0:
                gb_d = m.get('gb_density_mean', 0)
                if gb_d > 0:
                    d_se = 1.0 / gb_d
            if am_pct <= 0:
                phi_am = m.get('phi_am', 0)
                phi_se = m.get('phi_se', 0)
                if phi_am > 0 and phi_se > 0:
                    am_pct = phi_am / (phi_am + phi_se) * 100
            if d_se <= 0 or am_pct <= 0:
                _skip_reasons[_case_name] = f'd_se={d_se:.2f}, am_pct={am_pct:.1f}'
                continue

            tau = m.get('tortuosity_mean', m.get('tortuosity_recommended', 0))
            sigma_ion = m.get('sigma_full_mScm', 0)

            # Quality filters: skip bad/incomplete cases
            if not tau or tau <= 0 or tau > 8:
                _skip_reasons[_case_name] = f'tau={tau}'
                continue
            if m.get('porosity', 0) > 30:
                _skip_reasons[_case_name] = f"porosity={m.get('porosity')}"
                continue
            # Skip network solver failures (σ=0) and near-percolation (σ<0.01)
            if sigma_ion < 0.01:
                _skip_reasons[_case_name] = f'sigma_ion={sigma_ion}'
                continue

            # Loading: prefer input_params, then folder name hints, then thickness estimate
            loading = 0
            if ip.get('loading'):
                loading = float(ip['loading'])
            if loading <= 0:
                folder_path = str(met_path.parent).lower()
                if '1mah' in folder_path or 'thin' in folder_path:
                    loading = 1
                elif '8mah' in folder_path:
                    loading = 8
                elif '6mah' in folder_path or 'real' in folder_path:
                    loading = 6
            # Fallback: estimate from thickness (0.05 mAh/cm² per μm, typical NCM811)
            if loading <= 0 and m.get('thickness_um', 0) > 0:
                loading = round(m['thickness_um'] * 0.05, 1)

            d_am = max(d_am_p, d_am_s)

            rows.append({
                'name': case_dir.name,
                'd_se': d_se, 'd_am': d_am, 'am_pct': am_pct, 'ps_frac': ps_frac,
                'rve': rve, 'loading': loading,
                'd_ratio': d_se / d_am if d_am > 0 else 0.1,
                'am_loading': am_pct * loading / 100,
                'se_density_proxy': (100 - am_pct) / max(d_se, 0.1),
                'layer_count': loading * 30 / max(d_se, 0.1),
                # v2.0 features
                'size_ratio_inv': d_am / d_se if d_se > 0 else 10,
                'am_se_interaction': am_pct * (1 - ps_frac) / 100,
                'log_d_se': np.log(max(d_se, 0.1)),
                'phi_se': m.get('phi_se', 0),
                'phi_am': m.get('phi_am', 0),
                'porosity': m.get('porosity', 0),
                'tau': tau,
                'cn': m.get('se_se_cn', 0),
                'gb_d': m.get('gb_density_mean', 0),
                'g_path': m.get('path_conductance_mean', 0),
                'hop_area': m.get('path_hop_area_mean', 0),
                'f_perc': m.get('percolation_pct', 0),
                'thickness': m.get('thickness_um', 0),
                'am_cn': m.get('am_am_cn', 0),
                # Coverage: fraction of AM surface in contact with SE
                'coverage': (lambda vs: sum(vs)/len(vs)/100 if vs else 0.20)([v for v in [m.get('coverage_AM_P_mean',0), m.get('coverage_AM_S_mean',0), m.get('coverage_AM_mean',0)] if v>0]),
                'sigma_ion': sigma_ion,
                'sigma_el': m.get('electronic_sigma_full_mScm', 0),
                'sigma_th': m.get('thermal_sigma_full_mScm', 0),
                'sigma_brug': m.get('sigma_ratio', 0),
            })
            # Auto-extract ALL numeric fields from full_metrics.json
            # Skip input features and already-mapped fields
            skip_keys = {'phi_se', 'phi_am', 'porosity', 'se_se_cn', 'tortuosity_mean',
                        'tortuosity_recommended', 'gb_density_mean', 'path_conductance_mean',
                        'path_hop_area_mean', 'percolation_pct', 'thickness_um', 'am_am_cn',
                        'sigma_full_mScm', 'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm',
                        'sigma_ratio', 'sigma_full', 'coverage_AM_P_mean', 'coverage_AM_S_mean',
                        'coverage_AM_mean', 'ps_ratio'}
            for mk, mv in m.items():
                if mk not in skip_keys and isinstance(mv, (int, float)) and not isinstance(mv, bool):
                    safe_key = f'fm_{mk}'  # prefix to avoid collision
                    rows[-1][safe_key] = float(mv)
            rows[-1]['_all_fm_keys'] = [f'fm_{k}' for k, v in m.items()
                                         if k not in skip_keys and isinstance(v, (int, float)) and not isinstance(v, bool)]

    # Deduplicate
    seen = set()
    unique = []
    n_dup = 0
    for r in rows:
        # ★ 2026-08-03: 키가 **지표 튜플**(phi_se·thickness·tau)이었다 — CLAUDE.md 가 기록한
        #   130c598 버그와 **같은 유형**이 여기 남아 있었다: "distinct sibling families with
        #   similar metrics were silently collapsed ... New: dedup by case_name only".
        #   결과: full_metrics 187 건인데 학습 코퍼스는 170 — 17 건이 이유 없이 사라졌고,
        #   지표가 우연히 가까운 **서로 다른 설계**가 지워질 수 있었다.
        #   중복의 진짜 원인은 같은 케이스가 results/ 와 archive/ 에 둘 다 있는 것이므로
        #   **이름**으로 지우는 것이 정확하다 (같은 이름 = 같은 케이스).
        key = r['name']
        if key not in seen:
            seen.add(key)
            unique.append(r)
        else:
            n_dup += 1

    # Log summary
    print(f"  [ML Data] Loaded: {len(rows)} → Dedup: {len(unique)} (removed {n_dup})")
    if _skip_reasons:
        print(f"  [ML Data] Skipped {len(_skip_reasons)} cases:")
        for name, reason in sorted(_skip_reasons.items()):
            print(f"    - {name}: {reason}")
    return unique


def train_models(results_folder, archive_folder):
    """Train GPR models with ML best practices.
    v2.0: K-fold CV, multi-kernel comparison, feature engineering.
    v2.1: Adaptive alpha, physics fallback.
    v2.2: GPR+RF ensemble, CN features, dynamic weighting."""
    global _cached_models, _training_data_count
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import (
        ConstantKernel, Matern, WhiteKernel, RBF, RationalQuadratic
    )
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import KFold
    from sklearn.ensemble import RandomForestRegressor  # v2.2: RF ensemble

    rows = load_training_data(results_folder, archive_folder)
    _training_data_count = len(rows)

    if len(rows) < 3:
        _cached_models = None
        return {'success': False, 'message': f'Not enough training data ({len(rows)} cases, need >= 3)', 'count': len(rows)}

    # Auto-discover all numeric targets from full_metrics
    global MICRO_TARGETS
    all_fm_keys = set()
    for r in rows:
        all_fm_keys.update(r.get('_all_fm_keys', []))
    extra_targets = []
    for fk in sorted(all_fm_keys):
        vals = [r.get(fk, 0) for r in rows]
        non_zero = sum(1 for v in vals if v != 0)
        if non_zero >= len(rows) * 0.5 and np.std(vals) > 0:
            extra_targets.append(fk)
    MICRO_TARGETS = list(CORE_TARGETS) + extra_targets
    print(f"  Targets: {len(CORE_TARGETS)} core + {len(extra_targets)} auto-discovered = {len(MICRO_TARGETS)} total")

    X = np.array([[r[f] for f in INPUT_FEATURES] for r in rows])
    Y = {t: np.array([r.get(t, 0) for r in rows]) for t in MICRO_TARGETS}

    # v2.0: Feature normalization (Lecture 4 k-NN: zero mean, unit variance)
    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)

    # v2.3: Multiple kernel candidates including ARD (per-feature length scales!)
    n_features = len(INPUT_FEATURES)
    kernel_candidates = {
        'Matern2.5': ConstantKernel(1.0) * Matern(length_scale=1.0, nu=2.5) + WhiteKernel(0.1),
        'Matern1.5': ConstantKernel(1.0) * Matern(length_scale=1.0, nu=1.5) + WhiteKernel(0.1),
        'RBF': ConstantKernel(1.0) * RBF(length_scale=1.0) + WhiteKernel(0.1),
        'RQ': ConstantKernel(1.0) * RationalQuadratic(length_scale=1.0, alpha=1.0) + WhiteKernel(0.1),
        # ARD: separate length_scale per feature → auto feature importance!
        'ARD_Matern': ConstantKernel(1.0) * Matern(length_scale=np.ones(n_features), nu=2.5) + WhiteKernel(0.1),
        'ARD_RBF': ConstantKernel(1.0) * RBF(length_scale=np.ones(n_features)) + WhiteKernel(0.1),
    }

    # v2.0: K-Fold CV setup (Lecture 3: train/val/test split, Lecture 4: CV)
    n_splits = min(5, len(rows))  # 5-fold or less for small datasets
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    models = {}
    scores = {}
    cv_scores = {}

    # v2.1: Two-pass training
    # Pass 1: Quick CV to detect overfitting
    # Pass 2: Adaptive alpha for overfitting targets
    print(f"  [v2.1] Pass 1: CV overfitting detection...")
    overfit_targets = set()
    for target in CORE_TARGETS:
        y = Y.get(target)
        if y is None or np.std(y) == 0:
            continue
        use_log = np.all(y > 0) and (np.max(y) / np.min(y) > 3)
        y_t = np.log(y) if use_log else y.copy()
        sc_y = StandardScaler()
        y_sc = sc_y.fit_transform(y_t.reshape(-1, 1)).ravel()

        # Quick CV with default kernel
        fold_r2s = []
        for tr_i, va_i in kf.split(X_scaled):
            try:
                gpr_q = GaussianProcessRegressor(
                    kernel=ConstantKernel(1.0)*Matern(length_scale=1.0, nu=2.5)+WhiteKernel(0.1),
                    n_restarts_optimizer=1, alpha=1e-6)
                gpr_q.fit(X_scaled[tr_i], y_sc[tr_i])
                p_v = gpr_q.predict(X_scaled[va_i])
                p_r = sc_y.inverse_transform(p_v.reshape(-1, 1)).ravel()
                y_r = sc_y.inverse_transform(y_sc[va_i].reshape(-1, 1)).ravel()
                if use_log: p_r = np.exp(p_r); y_r = np.exp(y_r)
                ss_r = np.sum((y_r - p_r)**2)
                ss_t = np.sum((y_r - np.mean(y_r))**2)
                fold_r2s.append(1 - ss_r/ss_t if ss_t > 0 else 0)
            except: fold_r2s.append(0)
        cv_r2_quick = np.mean(fold_r2s)
        if cv_r2_quick < 0.6:
            overfit_targets.add(target)
    if overfit_targets:
        print(f"  [v2.1] Overfitting detected: {overfit_targets}")
        print(f"  [v2.1] Pass 2: Adaptive alpha for these targets")

    # Physics-based targets (don't need GPR)
    PHYSICS_TARGETS = {
        'f_perc': lambda r: min(100, max(0, (r.get('phi_se', 0.3) - 0.15) / 0.15 * 100)),
    }

    for target in MICRO_TARGETS:
        y = Y[target]
        if np.std(y) == 0:
            continue

        # v2.1: Skip physics-based targets (replace with formula)
        if target in PHYSICS_TARGETS:
            print(f"    {target:15s}: PHYSICS (GPR skipped, CV_R² was negative)")
            models[target] = {'physics': True, 'formula': PHYSICS_TARGETS[target]}
            scores[target] = -1
            cv_scores[target] = -1
            continue

        use_log = np.all(y > 0) and (np.max(y) / np.min(y) > 3)
        y_train = np.log(y) if use_log else y.copy()

        scaler_y = StandardScaler()
        y_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()

        # v2.1: Adaptive alpha (Lecture 5: soft-margin)
        # Overfitting targets get higher alpha → more regularization
        base_alpha = 1e-6
        if target in overfit_targets:
            base_alpha = 0.01  # 10000× more regularization!

        # v2.0: Try multiple kernels, pick best by CV
        best_kernel_name = 'Matern2.5'
        best_cv_r2 = -999
        best_gpr = None

        for k_name, k_template in kernel_candidates.items():
            try:
                fold_r2s = []
                for train_idx, val_idx in kf.split(X_scaled):
                    gpr_trial_fold = GaussianProcessRegressor(
                        kernel=k_template, n_restarts_optimizer=2, alpha=base_alpha
                    )
                    gpr_trial_fold.fit(X_scaled[train_idx], y_scaled[train_idx])
                    pred_val = gpr_trial_fold.predict(X_scaled[val_idx])
                    pred_real = scaler_y.inverse_transform(pred_val.reshape(-1, 1)).ravel()
                    y_val_real = scaler_y.inverse_transform(y_scaled[val_idx].reshape(-1, 1)).ravel()
                    if use_log:
                        pred_real = np.exp(pred_real)
                        y_val_real = np.exp(y_val_real)
                    ss_res = np.sum((y_val_real - pred_real)**2)
                    ss_tot = np.sum((y_val_real - np.mean(y_val_real))**2)
                    fold_r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
                    fold_r2s.append(fold_r2)
                cv_r2 = np.mean(fold_r2s)
                if cv_r2 > best_cv_r2:
                    best_cv_r2 = cv_r2
                    best_kernel_name = k_name
            except Exception:
                pass

        # Final fit with best kernel on ALL data
        best_kernel = kernel_candidates[best_kernel_name]
        gpr = GaussianProcessRegressor(kernel=best_kernel, n_restarts_optimizer=5, alpha=base_alpha)
        gpr.fit(X_scaled, y_scaled)

        # Train R² (for display)
        pred_train = gpr.predict(X_scaled)
        pred_real = scaler_y.inverse_transform(pred_train.reshape(-1, 1)).ravel()
        if use_log:
            pred_real = np.exp(pred_real)
        ss_res = np.sum((y - pred_real) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

        # v2.2: Train RF as ensemble partner (especially for low-CV targets)
        rf = RandomForestRegressor(n_estimators=100, max_depth=6, min_samples_leaf=3,
                                   random_state=42, n_jobs=-1)
        rf.fit(X_scaled, y_scaled)

        # RF CV score
        rf_cv_r2s = []
        for tr_i, va_i in kf.split(X_scaled):
            rf_fold = RandomForestRegressor(n_estimators=50, max_depth=6, min_samples_leaf=3, random_state=42)
            rf_fold.fit(X_scaled[tr_i], y_scaled[tr_i])
            p_v = rf_fold.predict(X_scaled[va_i])
            p_r = scaler_y.inverse_transform(p_v.reshape(-1, 1)).ravel()
            y_r = scaler_y.inverse_transform(y_scaled[va_i].reshape(-1, 1)).ravel()
            if use_log: p_r = np.exp(p_r); y_r = np.exp(y_r)
            ss_r = np.sum((y_r - p_r)**2)
            ss_t = np.sum((y_r - np.mean(y_r))**2)
            rf_cv_r2s.append(1 - ss_r/ss_t if ss_t > 0 else 0)
        rf_cv_r2 = np.mean(rf_cv_r2s)

        # v2.2: Dynamic ensemble weight based on CV R²
        # Better CV_R² model gets more weight
        gpr_w = max(0.1, best_cv_r2) if best_cv_r2 > 0 else 0.1
        rf_w = max(0.1, rf_cv_r2) if rf_cv_r2 > 0 else 0.1
        total_w = gpr_w + rf_w
        gpr_weight = gpr_w / total_w
        rf_weight = rf_w / total_w

        models[target] = {
            'gpr': gpr, 'rf': rf,
            'scaler_X': scaler_X, 'scaler_y': scaler_y,
            'use_log': use_log, 'r2': r2, 'kernel': best_kernel_name,
            'cv_r2': best_cv_r2, 'rf_cv_r2': rf_cv_r2,
            'gpr_weight': gpr_weight, 'rf_weight': rf_weight,
        }
        scores[target] = round(r2, 3)
        cv_scores[target] = round(max(best_cv_r2, rf_cv_r2), 3)  # best of GPR/RF

    # Log kernel selection summary (core targets only)
    print(f"  [v2.0] Kernel selection (core targets):")
    for t in CORE_TARGETS:
        if t in models:
            m = models[t]
            if m.get('physics'):
                print(f"    {t:15s}: PHYSICS   R²=N/A   CV_R²=N/A")
            else:
                rf_str = f" RF_CV={m.get('rf_cv_r2',0):.3f}" if 'rf_cv_r2' in m else ""
                w_str = f" w=[GPR:{m.get('gpr_weight',1):.0%}/RF:{m.get('rf_weight',0):.0%}]"
                print(f"    {t:15s}: {m['kernel']:10s} GPR_CV={m['cv_r2']:.3f}{rf_str}{w_str}")

    # Fit C constants from data
    # FORM X (v4++ champion): σ = C × σ_grain × (φ-φc)^(3/4) × CN × √cov / √τ
    PHI_C = 0.185  # v2.0: optimized percolation threshold (was 0.18)
    C_formX = 0.1275  # default
    log_rhs_X = []
    log_act_X = []
    for r in rows:
        phi_ex = max(r['phi_se'] - PHI_C, PHI_EX_FLOOR)
        cov_frac = max(r.get('coverage', 0.20), 0.01)
        if phi_ex > 0 and r['cn'] > 0 and r['tau'] > 0 and r['sigma_ion'] > 0.01:
            rhs = SIGMA_GRAIN * phi_ex**0.75 * r['cn'] * np.sqrt(cov_frac) / np.sqrt(r['tau'])
            log_rhs_X.append(np.log(rhs))
            log_act_X.append(np.log(r['sigma_ion']))
    if log_rhs_X:
        C_formX = float(np.exp(np.mean(np.array(log_act_X) - np.array(log_rhs_X))))

    # v3 legacy: σ = σ_brug × C × (G_path × GB_d²)^(1/4) × CN²
    C_v3 = 0.073
    log_rhs_v3 = []
    log_act_v3 = []
    for r in rows:
        if r['g_path'] > 0 and r['gb_d'] > 0 and r['cn'] > 0 and r['sigma_ion'] > 0.01 and r['sigma_brug'] > 0:
            sb = r['sigma_brug'] * SIGMA_GRAIN
            rhs = np.log(sb) + 0.25 * np.log(r['g_path'] * r['gb_d'] ** 2) + 2 * np.log(r['cn'])
            log_rhs_v3.append(rhs)
            log_act_v3.append(np.log(r['sigma_ion']))
    if log_rhs_v3:
        C_v3 = float(np.exp(np.mean(np.array(log_act_v3) - np.array(log_rhs_v3))))

    # v12-clean v3 (FINAL): base × C_blend(τ), fit live from corpus
    ionic_v12 = fit_ionic_v12(rows)

    _cached_models = {
        'models': models,
        'ionic_v12': ionic_v12,  # v12-clean v3 — primary when available
        'C_ionic': C_formX,  # FORM X — fallback / comparison
        'C_v3': C_v3,        # v3 for comparison
        'PHI_C': PHI_C,
        'count': len(rows),
        'scores': scores,
        'cv_scores': cv_scores,  # v2.0: cross-validation scores
    }

    return {'success': True, 'count': len(rows), 'scores': scores,
            'cv_scores': cv_scores,
            'C_formX': round(C_formX, 4), 'C_v3': round(C_v3, 4),
            'ionic_v12': ionic_v12 is not None}


def get_data_count(results_folder, archive_folder):
    """Get count of available training cases without training."""
    global _training_data_count
    if _training_data_count > 0:
        return _training_data_count
    rows = load_training_data(results_folder, archive_folder)
    _training_data_count = len(rows)
    return _training_data_count


def predict(d_se, d_am, am_pct, ps_frac, loading, rve, temperature=298, additive='none', ptfe=False,
            sigma_e_t_model='none', ea_ion_ev=None):
    """Run prediction using cached models.

    temperature      : UI slider value in KELVIN; 298 == the T_ref position (see _UI_T_REF_K).
    sigma_e_t_model  : 'none' (DEFAULT — σ_e is T-independent: Reisacher ohmic + matches the
                       DEM/voxel solvers) or 'legacy_arrhenius' (exact replay of the
                       pre-2026-07-28 Ea_AM = 0.50 eV 'rough' behaviour; ⚠ UNANCHORED §F1).
    ea_ion_ev        : σ_ion activation energy override; None → se_material default 0.41 eV.
                       ★ Never report a single value — sweep 0.29 / 0.41 / 0.46.
    """
    if _cached_models is None:
        return {'error': 'Models not trained. Click "Train Models" first.'}

    # Input validation
    d_se = max(0.1, float(d_se))
    d_am = max(0.5, float(d_am))
    am_pct = max(10, min(95, float(am_pct)))
    ps_frac = max(0, min(1, float(ps_frac)))
    loading = max(0.1, float(loading))
    rve = max(10, float(rve))
    temperature = max(200, min(500, float(temperature)))

    models = _cached_models['models']
    C_ionic = _cached_models['C_ionic']

    input_dict = derive_features(d_se, d_am, am_pct, ps_frac, rve, loading)

    # Stage 1: GPR predict microstructure
    micro = {}
    for target, m in models.items():
        # v2.1: Physics-based targets
        if m.get('physics'):
            val = m['formula'](input_dict)
            micro[target] = {'value': float(val), 'std': 0.0}
            continue
        x = np.array([[input_dict.get(f, 0) for f in INPUT_FEATURES]])
        x_scaled = m['scaler_X'].transform(x)

        # GPR prediction
        pred_scaled, std_scaled = m['gpr'].predict(x_scaled, return_std=True)
        pred_gpr = m['scaler_y'].inverse_transform(pred_scaled.reshape(-1, 1)).ravel()[0]
        std = std_scaled[0] * m['scaler_y'].scale_[0]

        # v2.2: RF prediction + ensemble
        if 'rf' in m:
            pred_rf_scaled = m['rf'].predict(x_scaled)[0]
            pred_rf = m['scaler_y'].inverse_transform([[pred_rf_scaled]])[0][0]
            if m['use_log']:
                pred_gpr_final = np.exp(pred_gpr)
                pred_rf_final = np.exp(pred_rf)
                std = pred_gpr_final * abs(std)
            else:
                pred_gpr_final = pred_gpr
                pred_rf_final = pred_rf
            # Weighted ensemble
            w_gpr = m.get('gpr_weight', 0.5)
            w_rf = m.get('rf_weight', 0.5)
            pred = w_gpr * pred_gpr_final + w_rf * pred_rf_final
        else:
            if m['use_log']:
                pred = np.exp(pred_gpr)
                std = pred * abs(std)
            else:
                pred = pred_gpr

        micro[target] = {'value': float(pred), 'std': float(abs(std))}

    # Stage 2: Physics scaling laws
    phi_se = micro.get('phi_se', {}).get('value', 0)
    porosity = micro.get('porosity', {}).get('value', 0)
    # v2.3: Physics constraint — φ_AM = 1 - φ_SE - porosity/100
    # Instead of independent GPR prediction, derive from other outputs
    phi_am_gpr = micro.get('phi_am', {}).get('value', 0)
    phi_am_phys = max(0, 1.0 - phi_se - porosity / 100)
    phi_am = 0.5 * phi_am_gpr + 0.5 * phi_am_phys  # ensemble with physics
    micro['phi_am']['value'] = phi_am  # update for display

    f_perc = micro.get('f_perc', {}).get('value', 100)
    tau = micro.get('tau', {}).get('value', 1)
    cn = micro.get('cn', {}).get('value', 0)
    gb_d = micro.get('gb_d', {}).get('value', 0)
    g_path = micro.get('g_path', {}).get('value', 0)
    am_cn = micro.get('am_cn', {}).get('value', 0)
    thickness = micro.get('thickness', {}).get('value', 0)
    porosity = micro.get('porosity', {}).get('value', 0)
    hop_area = micro.get('hop_area', {}).get('value', 0)
    sigma_brug_ratio = micro.get('sigma_brug', {}).get('value', 0)

    # Ionic conductivity — v12-clean v3 (FINAL, R²=0.9813):
    #   σ = C_blend(τ) × σ_grain × √(φ−φc) × CN^(3/2) × cov^(2/5) × f_p³
    # Falls back to FORM X (φ^¾·CN·√cov/√τ) when the v12 blend isn't fitted.
    PHI_C = _cached_models.get('PHI_C', 0.185)
    sigma_brug = SIGMA_GRAIN * sigma_brug_ratio
    coverage_pred = micro.get('coverage', {}).get('value', 0.20) if isinstance(micro.get('coverage'), dict) else 0.20
    coverage_frac = max(0.01, min(1.0, coverage_pred))
    f_perc_frac = max(0.0, min(1.0, f_perc / 100.0))

    sigma_ionic = 0
    ionic_v12 = _cached_models.get('ionic_v12')
    if ionic_v12 and phi_se > PHI_C_V12 and cn > 0 and tau > 0:
        sigma_ionic = predict_ionic_v12(ionic_v12, phi_se, cn, tau,
                                        coverage_frac, f_perc_frac)
    elif (phi_se - PHI_C) > PHI_EX_FLOOR and cn > 0 and tau > 0:
        # FORM X fallback (clamp 1e-4 per the doc's sub-threshold fix)
        phi_excess = max(phi_se - PHI_C, PHI_EX_FLOOR)
        sigma_ionic = C_ionic * SIGMA_GRAIN * phi_excess**0.75 * cn * np.sqrt(coverage_frac) / np.sqrt(tau)

    # v3 legacy (for comparison)
    sigma_ionic_v3 = 0
    C_v3 = _cached_models.get('C_v3', 0.073)
    if sigma_brug > 0 and g_path > 0 and gb_d > 0 and cn > 0:
        sigma_ionic_v3 = sigma_brug * C_v3 * (g_path * gb_d ** 2) ** 0.25 * cn ** 2

    # Direct GPR prediction for ensemble
    sigma_gpr = micro.get('sigma_ion', {}).get('value', 0)

    # Ensemble (0.5 hybrid + 0.5 gpr by default)
    if sigma_ionic > 0 and sigma_gpr > 0:
        sigma_ionic_final = 0.5 * sigma_ionic + 0.5 * sigma_gpr
    elif sigma_ionic > 0:
        sigma_ionic_final = sigma_ionic
    else:
        sigma_ionic_final = sigma_gpr

    # ── Temperature correction — UNIFIED WITH THE SOLVER (T1-e) ──────────────────
    # σ_ion: se_material convention  σ·T = σ₀·exp(−Ea/k_B T)  [Kraft 2017 eq 5],
    #        T_ref = 25 °C, Ea = 0.41 eV (Reisacher 2023 STATED, 375 MPa cold-press).
    #        The old code here used the σ form with Ea 0.30 eV and an undeclared T_ref — the
    #        two forms differ by ~10 % in the 30→60 °C multiplier, so the convention is pinned.
    # σ_e:   T-INDEPENDENT by default (Reisacher: ohmic regime T-independent; and the DEM/voxel
    #        solvers do not scale σ_e) — the legacy Ea_AM = 0.50 eV was self-labelled 'rough'
    #        (unanchored, §F1).  Exact legacy replay: sigma_e_t_model='legacy_arrhenius'.
    sigma_e_t_model = sigma_e_t_model if sigma_e_t_model in SIGMA_E_T_MODELS else 'none'
    temp_c = _ui_kelvin_to_celsius(temperature)
    sigma_ionic_ref = sigma_ionic_final   # T_ref (25 °C) value — feeds the σ_thermal formula,
    #                                       which has no temperature anchor of its own (§F1)
    sigma_ionic_298 = sigma_ionic_ref     # legacy alias (used further below)
    at_ref = (float(temperature) == _UI_T_REF_K)
    if not at_ref and temperature > 0:
        arrhenius_SE = se_material.arrhenius_sigma_factor(temp_c, ea_ion_ev)
        # legacy σ form + unanchored Ea_AM, reproduced BIT-EXACTLY for replay only
        arrhenius_AM = (np.exp(-EA_AM_EV_LEGACY / 8.617e-5 * (1 / temperature - 1 / 298))
                        if sigma_e_t_model == 'legacy_arrhenius' else 1.0)
        sigma_ionic_final *= arrhenius_SE
    else:
        arrhenius_SE = 1.0
        arrhenius_AM = 1.0

    # Electronic conductivity — v2.2: 2-Regime (was: exp(π/(T/d)))
    sigma_electronic = 0
    if phi_am > 0 and am_cn > 0 and d_am > 0 and thickness > 0:
        ratio = thickness / d_am
        if ratio >= 10:
            # THICK: φ⁴ × CN^(3/2) × cov × √τ (R²=0.97)
            sigma_electronic = 0.79 * SIGMA_AM * phi_am**4 * am_cn**1.5 * coverage_frac * np.sqrt(max(tau, 0.1))
        elif ratio > 0:
            # THIN: hop^0.25 × CN^0.4 × δ^0.2 × f_p^0.15 / (φ_SE^0.85 × √ξ)
            # Simplified: use available variables
            am_hop = micro.get('fm_am_am_mean_hop', {}).get('value', 8.0) if isinstance(micro.get('fm_am_am_mean_hop'), dict) else 8.0
            am_delta = micro.get('fm_am_am_mean_delta', {}).get('value', 0.1) if isinstance(micro.get('fm_am_am_mean_delta'), dict) else 0.1
            el_perc = micro.get('fm_electronic_percolating_fraction', {}).get('value', 0.9) if isinstance(micro.get('fm_electronic_percolating_fraction'), dict) else 0.9
            phi_se_val = max(phi_se, 0.01)
            sigma_electronic = 5.0 * SIGMA_AM * am_hop**0.25 * am_cn**0.4 * am_delta**0.2 * el_perc**0.15 / (phi_se_val**0.85 * ratio**0.5)
        # arrhenius_AM == 1.0 unless sigma_e_t_model='legacy_arrhenius' (see the T1-e block above):
        # σ_e is T-independent by default — Reisacher (ohmic) + the DEM/voxel solvers agree.
        sigma_electronic *= arrhenius_AM

    # ── Electronic Active AM (Dead AM estimation) ──
    # Ref: Minnmann 2021, Clausnitzer 2023, Bielefeld 2023
    # Percolation threshold: ~25-30 vol% AM
    # >55 vol%: fully percolating, 0% dead
    # 30-55%: transition zone
    # <25%: severe electronic isolation
    if phi_am >= 0.55:
        electronic_active_pct = 100.0
    elif phi_am >= 0.30:
        # Linear interpolation: 30%→87%, 55%→100%
        electronic_active_pct = 87 + (phi_am - 0.30) / 0.25 * 13
    elif phi_am >= 0.18:
        # Below threshold: sharp drop
        electronic_active_pct = 50 + (phi_am - 0.18) / 0.12 * 37
    else:
        electronic_active_pct = max(10, phi_am / 0.18 * 50)

    # ── Conductive Additive Effect ──
    # Ref: Bielefeld 2023, Minnmann 2021, Kang 2024
    # KEY: C65 percolation threshold ~4wt%! Below that, NO electronic network!
    if additive == 'vgcf':
        # VGCF 1wt%: fiber morphology, poor percolation even at 10vol%
        # σ_el ≈ 0.4 mS/cm (Bielefeld 2023) — NOT percolating, just local enhancement
        # But bridges isolated AM → dead AM reduced by ~10% (Minnmann 2021: +13% capacity)
        sigma_electronic = max(sigma_electronic, 0.4)
        sigma_ionic_final *= 0.99
        electronic_active_pct = min(100, electronic_active_pct + 10)
    elif additive == 'c65':
        # C65 1wt%: BELOW percolation threshold (~4wt%!)
        sigma_electronic += 1.0
        sigma_ionic_final *= 0.97
        electronic_active_pct = min(100, electronic_active_pct + 5)
    elif additive == 'c65_4wt':
        # C65 4wt%: AT percolation threshold — full electronic network!
        # σ_el ≈ 70 mS/cm (Bielefeld 2023, directly measured)
        sigma_electronic = max(sigma_electronic, 70)
        sigma_ionic_final *= 0.85
        electronic_active_pct = 100.0

    # ── PTFE Binder Effect (independent, stackable with additive) ──
    # Ref: Rosner 2026, Mun 2025 — 209.7 mAh/g, 97.4% retention
    # PTFE 0.5wt%: dry process binder (fibrillization)
    # Insulator but at 0.1-0.5wt% minimal content
    # Effect: slight σ_el reduction (AM surface coating), σ_ion nearly unchanged
    if ptfe:
        sigma_electronic *= 0.7   # ~30% e- reduction from surface coating
        sigma_ionic_final *= 0.99  # ~1% ionic (dry process, no solvent damage)

    # Thermal conductivity (use 298K σ_ion — formula was fitted at 298K)
    sigma_thermal = 0
    if sigma_ionic_298 > 0 and phi_am > 0 and cn > 0:
        sigma_thermal = 286 * sigma_ionic_298 ** 0.75 * phi_am ** 2 / cn

    # Uncertainty from GPR std
    sigma_ion_std = micro.get('sigma_ion', {}).get('std', 0)

    # ── Utilization: Newman Electrode Model (Corrected) ──
    # Two versions: A) Newman simplified, B) PyBaMM (if available)
    #
    # Newman: util = tanh(ν)/ν where ν = T/L_c
    # L_c = characteristic length = √(κ_eff / (a_s × j₀ × F / (R×T_K)))
    # Ref: Newman & Tobias (1962), Fuller, Doyle, Newman (1994)
    #
    # Key correction: j₀ is FIXED (exchange current density, material property)
    # C-rate affects applied current i_app, which changes overpotential η
    # At high η (high C-rate), effective reaction rate increases → ν changes

    F_const = 96485      # C/mol
    R_const = 8.314      # J/(mol·K)
    T_kelvin = 298       # K
    r_AM_cm = d_am * 1e-4 / 2 if d_am > 0 else 2.5e-4  # μm → cm
    T_cm = thickness * 1e-4 if thickness > 0 else 0.01   # μm → cm
    kappa_eff = sigma_ionic_final * 1e-3 if sigma_ionic_final > 0 else 1e-6  # mS/cm → S/cm

    # Specific interfacial area: a_s = 3 × φ_AM / r_AM (spherical particles)
    # But in ASSB, not all AM surface contacts SE — apply coverage fraction
    # Use GPR-predicted coverage (NOT fixed 20%)
    a_s_geometric = 3 * phi_am / r_AM_cm if r_AM_cm > 0 and phi_am > 0 else 1e4  # cm⁻¹
    coverage_pred = micro.get('coverage', {}).get('value', 0.20) if isinstance(micro.get('coverage'), dict) else 0.20
    coverage_fraction = max(0.05, min(0.50, coverage_pred))  # clamp to reasonable range
    a_s = a_s_geometric * coverage_fraction  # effective interfacial area

    # Exchange current density: FIXED material property (NOT C-rate dependent!)
    # NCM811/LPSCl interface: j₀ ≈ 0.01 mA/cm² (10× lower than liquid LIB)
    # ASSB solid-solid interface has much higher charge-transfer resistance
    # Ref: Sakuda (2017), Kato (2016)
    j0 = 0.01e-3  # A/cm² (0.01 mA/cm², ASSB NCM/LPSCl interface)

    # Theoretical capacity for C-rate calculation
    # NCM811: 200 mAh/g, ρ_AM = 4.8 g/cm³
    Q_theo = 200  # mAh/g
    rho_AM = 4.8  # g/cm³
    # Volumetric capacity = Q × ρ × φ_AM
    Q_vol = Q_theo * rho_AM * phi_am * 1e-3  # Ah/cm³

    c_rates = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
    utilizations = {}
    for c_rate in c_rates:
        # Applied current density (A/cm²) = C-rate × Q_vol × T
        i_app = c_rate * Q_vol * T_cm  # A/cm²

        # Newman dimensionless parameter
        # ν² = a_s × j₀ × F × T² / (κ_eff × R × T_K)
        # This gives characteristic penetration depth vs electrode thickness
        if kappa_eff > 0 and a_s > 0 and j0 > 0:
            nu_sq = a_s * j0 * F_const * T_cm**2 / (kappa_eff * R_const * T_kelvin)
            nu = np.sqrt(nu_sq) if nu_sq > 0 else 0

            # Base utilization from Newman
            util_newman = np.tanh(nu) / nu if nu > 0.01 else 1.0

            # Additional C-rate penalty: ohmic drop limits
            # ΔV_ohmic = i_app × T / (2 × κ_eff)
            delta_V = i_app * T_cm / (2 * kappa_eff) if kappa_eff > 0 else 10
            V_cutoff = 0.3  # V (typical cutoff overpotential)
            ohmic_factor = min(1.0, V_cutoff / delta_V) if delta_V > 0 else 1.0

            util = util_newman * ohmic_factor
        else:
            util = 1.0

        utilizations[f'{c_rate}C'] = round(min(1.0, max(0.0, util)), 3)

    util_1C = utilizations.get('1.0C', 1.0)
    performance_score = sigma_ionic_final * util_1C

    # Rate limiting
    rate_limiting = 'ionic'
    if sigma_ionic_final > 0 and sigma_electronic > 0:
        if sigma_electronic < sigma_ionic_final:
            rate_limiting = 'electronic'

    return {
        'microstructure': {
            'phi_se': _fmt(phi_se, micro.get('phi_se', {})),
            'phi_am': _fmt(phi_am, micro.get('phi_am', {})),
            'porosity': _fmt(porosity, micro.get('porosity', {})),
            'tau': _fmt(tau, micro.get('tau', {})),
            'cn': _fmt(cn, micro.get('cn', {})),
            'gb_d': _fmt(gb_d, micro.get('gb_d', {})),
            'g_path': _fmt(g_path, micro.get('g_path', {})),
            'hop_area': _fmt(hop_area, micro.get('hop_area', {})),
            'f_perc': _fmt(f_perc, micro.get('f_perc', {})),
            'thickness': _fmt(thickness, micro.get('thickness', {})),
            'am_cn': _fmt(am_cn, micro.get('am_cn', {})),
            'sigma_brug_ratio': _fmt(sigma_brug_ratio, micro.get('sigma_brug', {})),
        },
        'conductivity': {
            'sigma_ionic': round(sigma_ionic_final, 4),
            'sigma_ionic_formX': round(sigma_ionic, 4),
            'sigma_ionic_v3': round(sigma_ionic_v3, 4),
            'sigma_ionic_gpr': round(sigma_gpr, 4),
            'sigma_ionic_std': round(sigma_ion_std, 4),
            'sigma_electronic': round(sigma_electronic, 4),
            'sigma_thermal': round(sigma_thermal, 4),
        },
        'utilization': utilizations,
        'performance_score': round(performance_score, 4),
        'electronic_active_pct': round(electronic_active_pct, 1),
        'dead_am_pct': round(100 - electronic_active_pct, 1),
        'rate_limiting': rate_limiting,
        'temperature': temperature,
        'arrhenius_factor_SE': round(arrhenius_SE, 4),
        # ── T1-a/T1-e provenance + labels (never change a number without labelling it) ──
        'temperature_C': round(temp_c, 2),
        'temperature_provenance': se_material.provenance(
            None if at_ref else temp_c, ea_ion_ev,
            sigma_e_modelled=(sigma_e_t_model == 'legacy_arrhenius')),
        'sigma_ion_T_model': ('ARRHENIUS_sigmaT_Kraft2017' if not at_ref else 'NOT_MODELLED'),
        'sigma_e_T_model': sigma_e_t_model,
        'arrhenius_factor_AM': round(arrhenius_AM, 4),
        'sigma_ionic_at_T_ref': round(sigma_ionic_ref, 4),
        'temperature_notes': (
            'sigma_ion: sigma*T Arrhenius (Kraft 2017 eq 5), T_ref=25 °C, Ea='
            f'{se_material.EA_ION_EV_DEFAULT if ea_ion_ev is None else ea_ion_ev} eV — '
            'REPORT THE BAND 0.29/0.41/0.46, never one value.  '
            + ('sigma_e: T-INDEPENDENT (default) — matches Reisacher (ohmic regime T-independent) '
               'AND the DEM/voxel solvers.  CHANGED 2026-07-28: the previous Ea_AM=0.50 eV was '
               'unanchored (code comment said "rough") and disagreed with both; pass '
               "sigma_e_t_model='legacy_arrhenius' to reproduce the old numbers exactly."
               if sigma_e_t_model == 'none' else
               'sigma_e: LEGACY Ea_AM=0.50 eV Arrhenius — ⚠ UNANCHORED (§F1) and inconsistent '
               'with both the literature (Reisacher: ohmic regime T-independent) and the '
               'DEM/voxel solvers (which do not scale sigma_e).  Replay/comparison only.')
            + '  Not scaled at all: i0 / D_s / OCP dU/dT / kappa (no anchors, §F1) — this is NOT '
              'a full-physics temperature sweep.'),
        'input': input_dict,
    }


def _fmt(val, micro_entry):
    """Format a microstructure value with uncertainty."""
    return {
        'value': round(val, 4),
        'std': round(micro_entry.get('std', 0), 4),
    }


def generate_heatmap(x_param, y_param, target, fixed_params, n_points=20):
    """Generate 2D heatmap data for two parameters vs a target."""
    if _cached_models is None:
        return {'error': 'Models not trained.'}

    sweep_ranges = {
        'd_se': (0.3, 3.0),
        'd_am': (3, 12),
        'am_pct': (60, 90),
        'ps_frac': (0.0, 1.0),
        'loading': (1, 10),
        'rve': (30, 100),
    }

    base = {'d_se': 1.0, 'd_am': 5.0, 'am_pct': 80, 'ps_frac': 0.5, 'loading': 6, 'rve': 50}
    base.update(fixed_params or {})

    x_range = sweep_ranges.get(x_param, (0.5, 5.0))
    y_range = sweep_ranges.get(y_param, (0.5, 5.0))
    x_values = np.linspace(x_range[0], x_range[1], n_points).tolist()
    y_values = np.linspace(y_range[0], y_range[1], n_points).tolist()

    z_matrix = []
    for yi in y_values:
        row = []
        for xi in x_values:
            params = dict(base)
            params[x_param] = xi
            params[y_param] = yi
            pred = predict(
                d_se=params['d_se'], d_am=params['d_am'],
                am_pct=params['am_pct'], ps_frac=params['ps_frac'],
                loading=params['loading'], rve=params['rve'],
            )
            if 'error' in pred:
                row.append(0)
            elif target == 'sigma_ionic':
                row.append(pred['conductivity']['sigma_ionic'])
            elif target == 'sigma_electronic':
                row.append(pred['conductivity']['sigma_electronic'])
            elif target == 'energy':
                # Quick energy estimate
                phi_am_v = pred['microstructure'].get('phi_am', {}).get('value', 0.5)
                thick_v = pred['microstructure'].get('thickness', {}).get('value', 100)
                util_1c = pred.get('utilization', {}).get('1.0C', 1.0)
                row.append(200 * 4.8 * phi_am_v * thick_v * 1e-4 * 3.7 * util_1c / 1000)
            elif target == 'performance':
                row.append(pred.get('performance_score', 0))
            else:
                row.append(pred['conductivity'].get(target, 0))
            row[-1] = round(row[-1], 6)
        z_matrix.append(row)

    labels = {
        'd_se': 'd_SE (um)', 'd_am': 'd_AM (um)', 'am_pct': 'AM%',
        'ps_frac': 'P:S fraction', 'loading': 'Loading (mAh/cm2)', 'rve': 'RVE (um)',
        'sigma_ionic': 'sigma_ionic (mS/cm)', 'sigma_electronic': 'sigma_elec (mS/cm)',
        'energy': 'Energy (mWh/cm2)', 'performance': 'Perf Score',
    }

    return {
        'x_values': [round(v, 3) for v in x_values],
        'y_values': [round(v, 3) for v in y_values],
        'z_matrix': z_matrix,
        'x_label': labels.get(x_param, x_param),
        'y_label': labels.get(y_param, y_param),
        'z_label': labels.get(target, target),
    }


def sensitivity_analysis(base_params):
    """Vary each param +/-30% and measure sigma change."""
    if _cached_models is None:
        return {'error': 'Models not trained.'}

    d_am = base_params.get('d_am', max(base_params.get('d_am_p', 5), base_params.get('d_am_s', 4)))
    base_pred = predict(
        d_se=base_params['d_se'], d_am=d_am,
        am_pct=base_params['am_pct'], ps_frac=base_params['ps_frac'],
        loading=base_params['loading'], rve=base_params['rve'],
    )
    if 'error' in base_pred:
        return base_pred
    base_sigma = base_pred['conductivity']['sigma_ionic']

    params_to_vary = ['d_se', 'am_pct', 'ps_frac', 'loading']
    results = []
    for p in params_to_vary:
        val = base_params.get(p, 1.0)
        deltas = []
        for factor in [0.7, 1.3]:
            new_val = val * factor
            params_copy = dict(base_params)
            params_copy[p] = new_val
            d_am_c = max(params_copy.get('d_am_p', d_am), params_copy.get('d_am_s', d_am))
            pred = predict(
                d_se=params_copy.get('d_se', 1.0), d_am=d_am_c,
                am_pct=params_copy.get('am_pct', 80), ps_frac=params_copy.get('ps_frac', 0.5),
                loading=params_copy.get('loading', 6), rve=params_copy.get('rve', 50),
            )
            if 'error' not in pred:
                deltas.append(pred['conductivity']['sigma_ionic'] - base_sigma)
        avg_delta = np.mean([abs(d) for d in deltas]) if deltas else 0
        results.append({
            'param': p,
            'delta_sigma': round(float(avg_delta), 6),
            'delta_minus': round(float(deltas[0]), 6) if len(deltas) > 0 else 0,
            'delta_plus': round(float(deltas[1]), 6) if len(deltas) > 1 else 0,
        })

    results.sort(key=lambda x: x['delta_sigma'], reverse=True)
    return {'base_sigma': round(base_sigma, 6), 'sensitivities': results}


def compute_pareto(fixed_params=None, n_points=8):
    """Sweep combinations, compute sigma_ionic and energy_density, return Pareto front."""
    if _cached_models is None:
        return {'error': 'Models not trained.'}

    import itertools
    base = {'d_se': 1.0, 'd_am': 5.0, 'am_pct': 80, 'ps_frac': 0.5, 'loading': 6, 'rve': 50}
    base.update(fixed_params or {})

    d_se_vals = np.linspace(0.3, 3.0, n_points)
    am_pct_vals = np.linspace(60, 90, n_points)
    loading_vals = np.linspace(1, 10, n_points)

    all_points = []
    for d_se, am_pct, loading in itertools.product(d_se_vals, am_pct_vals, loading_vals):
        pred = predict(d_se=d_se, d_am=base['d_am'], am_pct=am_pct,
                       ps_frac=base['ps_frac'], loading=loading, rve=base['rve'])
        if 'error' in pred:
            continue
        sigma = pred['conductivity']['sigma_ionic']
        phi_am_v = pred['microstructure'].get('phi_am', {}).get('value', 0.5)
        thick_v = pred['microstructure'].get('thickness', {}).get('value', 100)
        util_1c = pred.get('utilization', {}).get('1.0C', 1.0)
        energy = 200 * 4.8 * phi_am_v * thick_v * 1e-4 * 3.7 * util_1c / 1000
        if sigma > 0 and energy > 0:
            all_points.append({
                'd_se': round(float(d_se), 2),
                'am_pct': round(float(am_pct), 1),
                'loading': round(float(loading), 1),
                'sigma_ionic': round(float(sigma), 4),
                'energy': round(float(energy), 4),
            })

    # Find Pareto front: no other point dominates in BOTH sigma AND energy
    pareto = []
    for p in all_points:
        dominated = False
        for q in all_points:
            if q['sigma_ionic'] >= p['sigma_ionic'] and q['energy'] >= p['energy'] and \
               (q['sigma_ionic'] > p['sigma_ionic'] or q['energy'] > p['energy']):
                dominated = True
                break
        if not dominated:
            pareto.append(p)

    pareto.sort(key=lambda x: x['sigma_ionic'])
    return {'pareto': pareto, 'all_count': len(all_points)}


def suggest_next(results_folder, archive_folder, top_n=3):
    """Suggest next DEM conditions using GPR uncertainty + predicted value (Expected Improvement)."""
    if _cached_models is None:
        return {'error': 'Models not trained.'}

    models = _cached_models['models']
    if 'sigma_ion' not in models:
        return {'error': 'sigma_ion model not available.'}

    m = models['sigma_ion']

    # Generate candidate points
    import itertools
    d_se_vals = np.linspace(0.3, 3.0, 10)
    am_pct_vals = np.linspace(60, 90, 7)
    ps_frac_vals = np.array([0.0, 0.3, 0.5, 0.7, 1.0])
    loading_vals = np.array([1, 3, 6, 8, 10])

    best_sigma = 0
    rows = load_training_data(results_folder, archive_folder)
    for r in rows:
        if r.get('sigma_ion', 0) > best_sigma:
            best_sigma = r['sigma_ion']

    candidates = []
    for d_se, am_pct, ps_frac, loading in itertools.product(d_se_vals, am_pct_vals, ps_frac_vals, loading_vals):
        d_am = 5.0
        rve = 50.0
        inp = derive_features(d_se, d_am, am_pct, ps_frac, rve, loading)
        x = np.array([[inp.get(f, 0) for f in INPUT_FEATURES]])
        x_scaled = m['scaler_X'].transform(x)
        pred_scaled, std_scaled = m['gpr'].predict(x_scaled, return_std=True)
        pred = m['scaler_y'].inverse_transform(pred_scaled.reshape(-1, 1)).ravel()[0]
        std_raw = std_scaled[0] * m['scaler_y'].scale_[0]
        if m['use_log']:
            pred = np.exp(pred)
            std_raw = pred * abs(std_raw)

        # Expected Improvement: EI = (pred - best) * Phi(z) + std * phi(z)
        # Simplified: score = pred + 1.5 * std (upper confidence bound)
        score = float(pred) + 1.5 * float(abs(std_raw))

        candidates.append({
            'd_se': round(float(d_se), 2),
            'am_pct': round(float(am_pct), 1),
            'ps_frac': round(float(ps_frac), 1),
            'loading': round(float(loading), 1),
            'predicted_sigma': round(float(pred), 4),
            'uncertainty': round(float(abs(std_raw)), 4),
            'acquisition_score': round(score, 4),
        })

    candidates.sort(key=lambda x: x['acquisition_score'], reverse=True)
    return {'suggestions': candidates[:top_n], 'best_known_sigma': round(best_sigma, 4)}


def export_training_csv(results_folder, archive_folder):
    """Export training data as CSV string."""
    rows = load_training_data(results_folder, archive_folder)
    if not rows:
        return ''

    # Collect all keys except internal ones
    skip = {'_all_fm_keys'}
    keys = []
    for r in rows:
        for k in r:
            if k not in skip and k not in keys:
                keys.append(k)

    import csv
    import io
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=keys, extrasaction='ignore')
    writer.writeheader()
    for r in rows:
        clean = {k: v for k, v in r.items() if k not in skip}
        writer.writerow(clean)
    return output.getvalue()


def generate_phase_diagram(x_param, y_param, fixed_params, n_points=30):
    """Generate phase diagram with contour boundaries.
    Returns grid data + boundary lines for multiple criteria."""
    if _cached_models is None:
        return {'error': 'Models not trained.'}

    sweep_ranges = {
        'd_se': (0.3, 3.0),
        'd_am': (3, 12),
        'am_pct': (60, 90),
        'ps_frac': (0.0, 1.0),
        'loading': (1, 10),
        'rve': (30, 100),
    }

    labels = {
        'd_se': 'd_SE (\u03bcm)', 'd_am': 'd_AM (\u03bcm)', 'am_pct': 'AM%',
        'ps_frac': 'P:S fraction', 'loading': 'Loading (mAh/cm\u00b2)', 'rve': 'RVE (\u03bcm)',
    }

    base = {'d_se': 1.0, 'd_am': 5.0, 'am_pct': 80, 'ps_frac': 0.5, 'loading': 6, 'rve': 50}
    base.update(fixed_params or {})

    x_range = sweep_ranges.get(x_param, (0.5, 5.0))
    y_range = sweep_ranges.get(y_param, (0.5, 5.0))
    x_values = np.linspace(x_range[0], x_range[1], n_points).tolist()
    y_values = np.linspace(y_range[0], y_range[1], n_points).tolist()

    sigma_ionic_grid = []
    electronic_active_grid = []
    util_1C_grid = []
    performance_grid = []

    for yi in y_values:
        sigma_row = []
        elec_row = []
        util_row = []
        perf_row = []
        for xi in x_values:
            params = dict(base)
            params[x_param] = xi
            params[y_param] = yi
            pred = predict(
                d_se=params['d_se'], d_am=params['d_am'],
                am_pct=params['am_pct'], ps_frac=params['ps_frac'],
                loading=params['loading'], rve=params['rve'],
            )
            if 'error' in pred:
                sigma_row.append(0)
                elec_row.append(0)
                util_row.append(0)
                perf_row.append(0)
            else:
                sigma_row.append(round(pred['conductivity']['sigma_ionic'], 6))
                elec_row.append(round(pred.get('electronic_active_pct', 0), 2))
                util_row.append(round(pred.get('utilization', {}).get('1.0C', 0), 4))
                perf_row.append(round(pred.get('performance_score', 0), 6))
        sigma_ionic_grid.append(sigma_row)
        electronic_active_grid.append(elec_row)
        util_1C_grid.append(util_row)
        performance_grid.append(perf_row)

    # Extract contour boundary points
    def find_boundary(grid, threshold):
        """Find cells where the grid crosses the threshold value."""
        points = []
        ny = len(grid)
        nx = len(grid[0]) if ny > 0 else 0
        for j in range(ny):
            for i in range(nx):
                val = grid[j][i]
                # Check neighbors (right and down)
                crosses = False
                if i + 1 < nx:
                    neighbor = grid[j][i + 1]
                    if (val < threshold and neighbor >= threshold) or (val >= threshold and neighbor < threshold):
                        crosses = True
                if j + 1 < ny:
                    neighbor = grid[j + 1][i]
                    if (val < threshold and neighbor >= threshold) or (val >= threshold and neighbor < threshold):
                        crosses = True
                if crosses:
                    points.append({'x': round(x_values[i], 4), 'y': round(y_values[j], 4), 'i': i, 'j': j})
        return points

    boundaries = {
        'sigma_0.1': find_boundary(sigma_ionic_grid, 0.1),
        'sigma_0.2': find_boundary(sigma_ionic_grid, 0.2),
        'electronic_80': find_boundary(electronic_active_grid, 80),
        'util_80': find_boundary(util_1C_grid, 0.8),
    }

    return {
        'x_values': [round(v, 4) for v in x_values],
        'y_values': [round(v, 4) for v in y_values],
        'x_label': labels.get(x_param, x_param),
        'y_label': labels.get(y_param, y_param),
        'sigma_ionic': sigma_ionic_grid,
        'electronic_active': electronic_active_grid,
        'util_1C': util_1C_grid,
        'performance': performance_grid,
        'boundaries': boundaries,
    }


def sweep_optimal(top_n=5, fixed_params=None, sweep_keys=None, defaults=None):
    """Sweep unchecked parameters, keep checked ones fixed."""
    if _cached_models is None:
        return {'error': 'Models not trained.'}

    if fixed_params is None:
        fixed_params = {}
    if defaults is None:
        defaults = {}

    # Sweep ranges for each parameter
    sweep_ranges = {
        'd_se': np.arange(0.3, 3.1, 0.1),
        'd_am_p': np.arange(3, 13, 1),
        'd_am_s': np.arange(1, 9, 0.5),
        'am_pct': np.arange(60, 91, 2),
        'ps_frac': np.arange(0.0, 1.05, 0.1),
        'loading': np.arange(1, 11, 1),
        'rve': np.array([30, 50, 100]),
    }

    if sweep_keys is None:
        sweep_keys = ['d_se', 'am_pct', 'ps_frac', 'loading']

    # Build combinations for sweep params only
    import itertools
    sweep_vals = [sweep_ranges.get(k, np.array([defaults.get(k, 1.0)])) for k in sweep_keys]
    combos = list(itertools.product(*sweep_vals))

    # Base params from fixed + defaults
    base = {
        'd_se': 1.0, 'd_am_p': 10, 'd_am_s': 4, 'am_pct': 80,
        'ps_frac': 0.5, 'loading': 6, 'rve': 50,
    }
    base.update(defaults)
    base.update(fixed_params)

    results = []
    for combo in combos:
        params = dict(base)
        for i, k in enumerate(sweep_keys):
            params[k] = float(combo[i])
        d_am = max(params.get('d_am_p', 5), params.get('d_am_s', 4))
        pred = predict(params['d_se'], d_am, params['am_pct'],
                      params['ps_frac'], params['loading'], params['rve'])
        if 'error' in pred:
            continue
        sig = pred['conductivity']['sigma_ionic']
        if sig > 0:
            # Calculate energy density & performance score
            util_1c = pred.get('utilization', {}).get('1.0C', 1.0)
            perf_score = sig * util_1c
            thickness_pred = pred['microstructure'].get('thickness', {})
            T_pred = thickness_pred.get('value', 100) if isinstance(thickness_pred, dict) else 100
            if T_pred <= 0:
                T_pred = params.get('loading', 6) * 20  # rough estimate: 1mAh≈20μm

            phi_am_pred = pred['microstructure'].get('phi_am', {})
            phi_am_val = phi_am_pred.get('value', 0.5) if isinstance(phi_am_pred, dict) else 0.5
            if phi_am_val <= 0:
                phi_am_val = (100 - params['am_pct']) / 100 * 0.65  # rough

            # Energy density: Q(mAh/cm²) = specific_cap × ρ_AM × φ_AM × T(cm)
            Q_per_cm2 = 200 * 4.8 * phi_am_val * T_pred * 1e-4  # mAh/cm²
            E_density = Q_per_cm2 * 3.7 * util_1c  # μWh/cm² → mWh/cm² (keep as mWh)

            # σ_electronic from prediction
            sigma_el_val = pred['conductivity'].get('sigma_electronic', 0)
            if sigma_el_val is None or sigma_el_val == 0:
                sigma_el_val = 0

            r = {
                'd_se': round(float(params['d_se']), 1),
                'am_pct': int(params['am_pct']),
                'ps_frac': round(float(params['ps_frac']), 1),
                'loading': round(float(params['loading']), 1),
                'sigma_ionic': round(sig, 4),
                'sigma_electronic': round(sigma_el_val, 2),
                'sigma_thermal': pred['conductivity'].get('sigma_thermal', 0),
                'util_1C': round(util_1c, 3),
                'perf_score': round(perf_score, 4),
                'energy_mWh_cm2': round(E_density, 2),
                'rate_limiting': pred['rate_limiting'],
            }
            # Add sweep params to result
            for k in sweep_keys:
                if k not in r:
                    r[k] = round(float(params[k]), 1)
            results.append(r)

    # Sort by performance score (σ × util@1C) — realistic optimum
    results.sort(key=lambda x: x.get('perf_score', x['sigma_ionic']), reverse=True)
    return results[:top_n]


# ══════════════════════════════════════════════════════════════════════════════
def _selftest_temp():
    """Temperature-convention selftest for the predictor surrogate (T1-e).

    Runs WITHOUT sklearn / trained models: it exercises the temperature helpers and the
    exact arithmetic `predict()` applies, which is where the solver↔surrogate divergence lived.
    """
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    chk('SIGMA_GRAIN is bitwise 3.0 and shared with the solvers (se_material)',
        float(SIGMA_GRAIN).hex() == (3.0).hex()
        and SIGMA_GRAIN is se_material.SIGMA_GRAIN_MS_CM_25C, float(SIGMA_GRAIN).hex())

    # UI slider mapping: 298 K is the reference position (the UI labels it "25 °C")
    chk('slider 298 K → exactly T_ref 25.0 °C', _ui_kelvin_to_celsius(298) == 25.0)
    for k, c in ((303, 30.0), (318, 45.0), (333, 60.0)):
        chk(f'slider {k} K → {c} °C (on the step-5 grid)',
            abs(_ui_kelvin_to_celsius(k) - c) < 1e-12)

    # at the UI default the σ_ion factor is EXACTLY 1.0 → what the user has already seen
    # at the default slider position is bitwise unchanged
    chk('σ_ion factor at the default slider (298 K) is exactly 1.0',
        se_material.arrhenius_sigma_factor(_ui_kelvin_to_celsius(298)) == 1.0)

    # σ_ion now uses the SOLVER convention (σ·T Kraft 2017), matching the docs table
    for k, want in ((303, 1.28), (318, 2.56), (333, 4.79)):
        f = se_material.arrhenius_sigma_factor(_ui_kelvin_to_celsius(k))
        chk(f'σ_ion @ {k} K → x{want} (same number network_conductivity --temp-c gives)',
            abs(round(f, 2) - want) < 5e-3, f'got x{f:.4f}')

    # the OLD surrogate convention (σ form, Ea 0.30, T_ref 298 K) was materially different
    old = np.exp(-0.30 / 8.617e-5 * (1 / 333 - 1 / 298))
    new = se_material.arrhenius_sigma_factor(_ui_kelvin_to_celsius(333))
    chk('old σ_ion convention differed materially (documented, not silent)',
        abs(old / new - 1.0) > 0.10, f'old x{old:.3f} vs new x{new:.3f} ({100*(old/new-1):+.1f} %)')

    # σ_e default = T-independent (Reisacher ohmic + solver-consistent); legacy is replayable
    chk("sigma_e_t_model default is 'none' in predict()'s signature",
        __import__('inspect').signature(predict).parameters['sigma_e_t_model'].default == 'none')
    legacy = np.exp(-EA_AM_EV_LEGACY / 8.617e-5 * (1 / 333 - 1 / 298))
    chk('legacy σ_e Arrhenius inflated σ_e ~7.7x at 60 °C (why it is off by default)',
        abs(legacy - 7.741) < 0.01, f'x{legacy:.3f}')
    chk('se_material declares the σ_e policy as NOT_MODELLED',
        se_material.SIGMA_E_T_DEPENDENCE == 'NOT_MODELLED'
        and se_material.provenance()['sigma_e_T_dependence'] == 'NOT_MODELLED')
    chk('legacy replay is still selectable and labelled',
        SIGMA_E_T_MODELS == ('none', 'legacy_arrhenius')
        and se_material.provenance(60.0, sigma_e_modelled=True)['sigma_e_T_dependence'] == 'ARRHENIUS')

    print('PREDICTOR TEMP SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    import sys as _s
    if '--selftest-temp' in _s.argv:
        _s.exit(_selftest_temp())
    print(__doc__)
