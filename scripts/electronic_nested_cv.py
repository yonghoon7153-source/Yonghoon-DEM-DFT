#!/usr/bin/env python3
"""σ_electronic — clean-slate fitting infrastructure (2026-05-28).

Built from scratch after all 39 legacy electronic files were deleted
('과감하게 버려').  Mirrors σ_ionic's nested_cv_sat.py structure with
electronic-specific physics.

TARGET (Stage-E physics):
  electronic_sigma_full_mScm_stage_e_physics
    — Stage-E final value with physics (Tabor+plastic) corrections applied
      to the Kirchhoff network solver.  This is the analogue of σ_ionic's
      _stage_e_sigma() target.  Cronau-equivalent NCM grain corrections
      are already baked in here.

PHYSICS-FIRST FORM (starting point — iterate from here):
  σ_e = σ_AM · (φ_AM)^a · CN_AM^b · cov_AM^c · f_p_e^d
        · exp[ p + q·ln τ + r·(ln τ)² ]    ← C_blend logpoly2

  No threshold (φ_AM ≫ φc_AM in all cases; AM-loaded composites are
  always deep into percolation).  Bruggeman-style power on φ_AM.

CONSTANTS:
  σ_AM    = 50.0 mS/cm   (NCM811 grain bulk; literature)
  exponents (a, b, c, d) live-fit initially; we'll lock to integers/halves
    once data identifies stable values (same pattern as σ_ionic CN²).

LIVE PARAMS: a, b, c, d (exponents) + p, q, r (logpoly2) → 7 OLS coefs.
  n=88 (current corpus) / k=7 = 12.5:1 → safe but tight.  Plan to lock
  exponents to integer/half once stable → k=3.

Run on WSL:
    python3 scripts/electronic_nested_cv.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp  # for _cov_frac, _meta_name etc

SIGMA_AM = 50.0       # NCM811 grain conductivity [mS/cm]
PHI_AM_MIN = 0.30     # rough lower bound (AM-loaded composites only)
PHI_C_AM = 0.0        # no threshold by default (AM far above percolation)

# Per-case anomaly exclusion — start empty, populate after first run identifies
# outliers (same workflow as σ_ionic's _EXCLUDED_NAMES).
_EXCLUDED_NAMES_EL: set[str] = set()


_TARGET_KEYS_E = (
    # Priority order — Hertz-pathway PREFERRED 2026-05-28 after audit found
    # ~9/130 cases where the physics-pathway electronic solver
    # (electronic_sigma_full_mScm_physics) produces impossible values
    # (100K-1M mS/cm = 1000× σ_AM_single = physically nonsense).  The Hertz
    # pathway (raw + Stage E) gives plausible values (1-280 mS/cm) for the
    # SAME cases, so we route around the buggy physics solver until upstream
    # is fixed.
    #
    # σ_ionic adopted the same Hertz-preference for T1 (cov_Hertz over
    # cov_physics) on physics grounds (Tabor adhesion area ≠ Li+ conduction
    # area).  Same logic applies to electronic: Hertz contact = elastic
    # area for electron tunneling.
    #
    # Track which key was used via _last_used_key so audit shows coverage.
    'electronic_sigma_full_mScm_stage_e',           # Stage E on Hertz (best — has Trevisanello)
    'electronic_sigma_full_mScm',                   # raw Hertz fallback
    'electronic_sigma_full_mScm_stage_e_physics',   # Stage E × physics (currently buggy)
    'electronic_sigma_full_mScm_physics',           # physics only (currently buggy)
)

# Reject σ_e values above this — composite cannot exceed σ_AM × (volume frac).
# σ_AM(NCM811) ~ 50 mS/cm literature; cap at 100 mS/cm with 2× margin.
SIGMA_E_MAX = 100.0

_last_used_key: dict = {}   # case_id → which σ key supplied its target


def _stage_e_electronic(d, case_id=None):
    """Best available σ_e (analogue of _stage_e_sigma).

    Priority: stage_e_physics → stage_e → physics → raw.  Returns (value, key_used).
    Stage E is preferred over physics because Stage E includes literature
    grain corrections (Trevisanello 2021) that the raw solver doesn't have.
    """
    for k in _TARGET_KEYS_E:
        v = d.get(k)
        if (isinstance(v, (int, float)) and not isinstance(v, bool)
                and v > 0 and v <= SIGMA_E_MAX):
            if case_id is not None:
                _last_used_key[case_id] = k
            return float(v)
    return None


def _phi_am(d):
    """AM volume fraction (composite-level)."""
    v = d.get('phi_am')
    return float(v) if isinstance(v, (int, float)) and v > 0 else None


def _am_am_cn(d):
    """AM-AM coordination number (electronic network)."""
    v = d.get('am_am_cn')
    return float(v) if isinstance(v, (int, float)) and v > 0 else None


def _cov_am(d, physics=False):
    """AM-AM contact-area fraction (analog of _cov_frac for SE-SE).
    Falls back to _cov_frac if AM-specific not stored."""
    # Try several keys; prefer AM-AM coverage
    for k in (('coverage_AM_AM_mean', 'coverage_AM_AM_mean_physics')
              if physics else
              ('coverage_AM_AM_mean', 'coverage_AM_AM')):
        v = d.get(k)
        if isinstance(v, (int, float)) and v > 0:
            return float(v) / 100.0 if v > 1 else float(v)
    # Fall back: derive from am_am_mean_area × am_am_cn / (4π r_AM²) if possible
    a_avg = d.get('am_am_mean_area', 0)
    cn = _am_am_cn(d)
    r = max(d.get('r_AM_P', 0), d.get('r_AM_S', 0), 0)
    if a_avg and cn and r > 0:
        sphere_area = 4.0 * np.pi * r * r
        cov = (a_avg * cn / 2.0) / sphere_area
        return max(min(cov, 1.0), 1e-4)
    return None


def _f_perc_e(d):
    """Electronic percolating fraction."""
    v = d.get('electronic_percolating_fraction')
    if isinstance(v, (int, float)) and v > 0:
        return float(v)
    # Fall back to ionic percolation_pct (rough proxy, not ideal)
    v = d.get('percolation_pct')
    return float(v) / 100.0 if isinstance(v, (int, float)) and v > 0 else None


def _tau_e(d):
    """Electronic tortuosity.  Prefer dedicated electronic if stored;
    else fall back to ionic τ (rough proxy)."""
    for k in ('tortuosity_electronic_recommended', 'tortuosity_electronic_mean',
              'tortuosity_recommended', 'tortuosity_mean'):
        v = d.get(k)
        if isinstance(v, (int, float)) and v > 0:
            return float(v)
    return None


def _meta_name(cid, mp_parent):
    """Look up the human-readable name from meta.json."""
    for meta_p in (Path('webapp/uploads') / cid / 'meta.json',
                   mp_parent / 'meta.json'):
        if meta_p.exists():
            try:
                return json.load(open(meta_p)).get('name') or cid
            except Exception:
                pass
    return cid


def load_corpus_e():
    """Walk corpus, return (a_array, names).
    Columns: 0 phi_am  1 cn_am  2 cov_am  3 f_p_e  4 tau_e  5 sigma_DEM
             6 p_amp   7 r_SE   8 r_AM_S  9 r_AM_P 10 thickness_um
    """
    rows, names = [], []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            _cid_tmp = mp.parent.name
            sig = _stage_e_electronic(d, case_id=_cid_tmp)
            phi_am = _phi_am(d)
            cn_am = _am_am_cn(d)
            cov = _cov_am(d)
            fp = _f_perc_e(d)
            tau = _tau_e(d)
            if not (sig and sig > 0 and phi_am and phi_am > PHI_AM_MIN
                    and cn_am and cn_am > 0 and cov and cov > 0
                    and fp and fp > 0 and tau and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES_EL:
                continue
            key = (round(phi_am, 4), round(cn_am, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key); names.append(nm)
            p_amp = gcp._ps_fraction(d)
            r_SE = gcp._direct_rse_um(d) or np.nan
            ras, rap = gcp._r_am_sizes(d)
            T = d.get('thickness_um', 0)
            rows.append((phi_am, cn_am, cov, fp, tau, sig, p_amp,
                         r_SE, ras or np.nan, rap or np.nan,
                         float(T) if T else np.nan))
    return np.array(rows, float), names


def base_log_electronic(a, exp_phi=1.5, exp_cn=2.0, exp_cov=0.5, exp_fp=3.0):
    """Bruggeman-style electronic base WITHOUT C_blend τ-correction.
    Live-fit-friendly: exponents may be data-tuned, then locked."""
    phi_am, cn, cov, fp = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    return (np.log(SIGMA_AM)
            + exp_phi * np.log(phi_am)
            + exp_cn * np.log(cn)
            + exp_cov * np.log(cov)
            + exp_fp * np.log(fp))


def cblend_fit(base, logsf, taus):
    """OLS joint fit of C_blend(τ) = p + q·ln τ + r·(ln τ)² on the residual."""
    lt = np.log(taus)
    X = np.column_stack([np.ones(len(taus)), lt, lt**2])
    b, *_ = np.linalg.lstsq(X, logsf - base, rcond=None)
    return b


def cblend_pred(base, taus, b):
    lt = np.log(taus)
    return base + b[0] + b[1]*lt + b[2]*lt**2


def loocv_r2(base, logsf, taus):
    """Plain LOOCV R² for a FIXED base (no hyperparameter selection)."""
    n = len(taus); ss = np.sum((logsf - logsf.mean())**2); sse = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        b = cblend_fit(base[m], logsf[m], taus[m])
        pi = cblend_pred(base[i:i+1], taus[i:i+1], b)[0]
        sse += (logsf[i] - pi)**2
    return 1 - sse/ss


def fit_full(a, logsf, taus, exp_phi=1.5, exp_cn=2.0, exp_cov=0.5, exp_fp=3.0):
    """Full-data fit; returns (b_logpoly2, pred_log, r2, loocv)."""
    base = base_log_electronic(a, exp_phi, exp_cn, exp_cov, exp_fp)
    b = cblend_fit(base, logsf, taus)
    pred = cblend_pred(base, taus, b)
    ss_tot = np.sum((logsf - logsf.mean())**2)
    r2 = 1 - np.sum((logsf - pred)**2) / ss_tot
    lo = loocv_r2(base, logsf, taus)
    return b, pred, r2, lo


def main():
    print("=" * 78)
    print(" σ_electronic — clean-slate fitting (Stage-E physics target)")
    print("=" * 78)
    a, names = load_corpus_e()
    n = len(a)
    print(f"Corpus n = {n} (filtered: phi_AM > {PHI_AM_MIN}, valid CN/cov/fp/τ)")

    # ─── Target-key coverage breakdown ─────────────────────────────
    if _last_used_key:
        from collections import Counter
        key_counts = Counter(_last_used_key.values())
        print(f"\n  Target-key usage (which σ_e column supplied each case):")
        for k in _TARGET_KEYS_E:
            cnt = key_counts.get(k, 0)
            mark = "  ←" if cnt > 0 else ""
            print(f"     {k:50s}  n={cnt:3d}{mark}")
        print(f"  (Stage E preferred — literature grain corrections baked in)")
    if n < 8:
        print("[ABORT] need ≥8 valid cases (some metrics may be missing on disk).")
        print("  Common missing fields: am_am_cn, coverage_AM_AM_mean,")
        print("  electronic_percolating_fraction, tortuosity_electronic.")
        print("  Run scripts/backfill_am_metrics.py to populate these first.")
        return

    logsf = np.log(a[:, 5]); taus = a[:, 4]
    print(f"\n  σ_electronic range: {a[:,5].min():.4f} ~ {a[:,5].max():.4f} mS/cm")
    print(f"  median = {np.median(a[:,5]):.4f}, log range = [{logsf.min():.2f}, {logsf.max():.2f}]")
    print(f"  φ_AM   range: {a[:,0].min():.3f} ~ {a[:,0].max():.3f}")
    print(f"  CN_AM  range: {a[:,1].min():.2f} ~ {a[:,1].max():.2f}")
    print(f"  cov_AM range: {a[:,2].min():.4f} ~ {a[:,2].max():.4f}")
    print(f"  f_p_e  range: {a[:,3].min():.3f} ~ {a[:,3].max():.3f}")
    print(f"  τ_e    range: {a[:,4].min():.2f} ~ {a[:,4].max():.2f}")
    print()

    print("=" * 78)
    print(" STAGE 0: Bruggeman baseline (σ_AM · φ_AM^a · CN^b · cov^c · f_p^d · C(τ))")
    print("=" * 78)
    print()
    # Default exponents (literature Bruggeman + Holm + isotropy)
    print(f"  Locked exponents: φ_AM^1.5  CN^2.0  cov^0.5  f_p^3.0   + C_blend(τ) logpoly2")
    b, pred, r2, lo = fit_full(a, logsf, taus, 1.5, 2.0, 0.5, 3.0)
    print(f"  R²    = {r2:.4f}")
    print(f"  LOOCV = {lo:.4f}")
    print(f"  C(τ) coefs: p={b[0]:+.3f}  q={b[1]:+.3f}  r={b[2]:+.3f}")
    err_pct = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100
    ae = np.abs(err_pct)
    print(f"  median |err|     = {np.median(ae):6.2f}%")
    print(f"  mean   |err|     = {np.mean(ae):6.2f}%")
    print(f"  max    |err|     = {np.max(ae):6.2f}%")
    print(f"  #|err|>30%       = {(ae > 30).sum():3d} / {n}")
    print(f"  #|err|>50%       = {(ae > 50).sum():3d} / {n}")
    print()

    # ───── Exponent scan (Bruggeman / Holm sensitivity) ─────
    print("=" * 78)
    print(" STAGE 1: Single-exponent sensitivity (one at a time, others locked)")
    print("=" * 78)
    print()
    for name, idx, grid, locked in [
            ('φ_AM',  0, [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0], (2.0, 0.5, 3.0)),
            ('CN_AM', 1, [0.5, 1.0, 1.5, 2.0, 2.5, 3.0],         (1.5, 0.5, 3.0)),
            ('cov',   2, [0.25, 0.5, 0.75, 1.0, 1.5],            (1.5, 2.0, 3.0)),
            ('f_p_e', 3, [1.0, 1.5, 2.0, 3.0, 4.0],              (1.5, 2.0, 0.5))]:
        print(f"  {name}^? scan (others locked at {locked}):")
        best = (None, -np.inf)
        for e in grid:
            args = list(locked)
            args.insert(idx, e)
            _b, _p, _r2, _lo = fit_full(a, logsf, taus, *args)
            marker = " ←" if _lo > best[1] else ""
            if _lo > best[1]: best = (e, _lo)
            print(f"     {name}^{e:<5}  R²={_r2:.4f}  LOOCV={_lo:.4f}{marker}")
        print(f"     ★ best {name}: {best[0]} (LOOCV={best[1]:.4f})")
        print()

    # ───── Top outliers ─────
    print("=" * 78)
    print(" Top |err|>20% outliers on baseline (φ^1.5 · CN² · cov^½ · f_p³ · C(τ))")
    print("=" * 78)
    b, pred, r2, lo = fit_full(a, logsf, taus, 1.5, 2.0, 0.5, 3.0)
    err_pct = (np.exp(pred) - np.exp(logsf)) / np.exp(logsf) * 100
    order = np.argsort(-np.abs(err_pct))
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_form':>7s}  {'err%':>7s}  "
          f"{'φ_AM':>5s} {'CN':>5s} {'τ':>4s}")
    shown = 0
    for i in order:
        if abs(err_pct[i]) <= 20 or shown >= 15: break
        nm = names[i] if i < len(names) else f"(idx{i})"
        print(f"  {nm[:32]:32s}  {a[i,5]:7.4f}  {float(np.exp(pred[i])):7.4f}  "
              f"{err_pct[i]:+7.1f}  {a[i,0]:5.3f} {a[i,1]:5.2f} {a[i,4]:4.2f}")
        shown += 1
    if shown == 0:
        print("  (none — baseline captures everything within 20%)")
    print()

    # ───── STAGE 2: Joint 7-param exponent fit + intercept → data-best form ─────
    print("=" * 78)
    print(" STAGE 2: Joint fit — all 7 params (a φ_AM, b CN, c cov, d f_p,")
    print("           + p q r logpoly2) by single OLS in log space")
    print("=" * 78)
    print()
    print("  Log-space regression:  log σ_e = log σ_AM + a·log φ_AM + b·log CN")
    print("                                  + c·log cov + d·log f_p")
    print("                                  + p + q·ln τ + r·(ln τ)²")
    print(f"  σ_AM = {SIGMA_AM} mS/cm reference (intercept p will absorb any offset).")
    print()
    phi_am_arr = a[:, 0]; cn_arr = a[:, 1]
    cov_arr = a[:, 2]; fp_arr = a[:, 3]; tau_arr = a[:, 4]
    lt = np.log(tau_arr)
    X = np.column_stack([
        np.log(phi_am_arr),
        np.log(cn_arr),
        np.log(cov_arr),
        np.log(fp_arr),
        np.ones(n),
        lt,
        lt**2,
    ])
    y = logsf - np.log(SIGMA_AM)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred_y = X @ coef
    pred_log_joint = pred_y + np.log(SIGMA_AM)
    ss_res = np.sum((y - pred_y)**2); ss_tot = np.sum((y - y.mean())**2)
    r2_j = 1 - ss_res/ss_tot if ss_tot > 0 else 0
    # LOOCV (manual; X is small)
    sse_loo = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        c_loo, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
        pi = X[i] @ c_loo
        sse_loo += (y[i] - pi)**2
    lo_j = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
    err_j = (np.exp(pred_log_joint) - np.exp(logsf)) / np.exp(logsf) * 100
    ae_j = np.abs(err_j)
    print(f"  data-best exponents:")
    print(f"     a (φ_AM)  = {coef[0]:+.3f}")
    print(f"     b (CN_AM) = {coef[1]:+.3f}")
    print(f"     c (cov)   = {coef[2]:+.3f}")
    print(f"     d (f_p_e) = {coef[3]:+.3f}")
    print(f"  C(τ) coefs:")
    print(f"     p (const) = {coef[4]:+.3f}")
    print(f"     q (ln τ)  = {coef[5]:+.3f}")
    print(f"     r (ln²τ)  = {coef[6]:+.3f}")
    sigma_am_eff = SIGMA_AM * np.exp(coef[4])
    print(f"  implied σ_AM_eff = {SIGMA_AM} × exp({coef[4]:+.3f}) = {sigma_am_eff:.2f} mS/cm")
    print(f"     (literature NCM811 σ_AM range: 1-100 mS/cm depending on poly vs single-crystal)")
    print()
    print(f"  R²    = {r2_j:.4f}    LOOCV = {lo_j:.4f}")
    print(f"  median |err|     = {np.median(ae_j):6.2f}%")
    print(f"  mean   |err|     = {np.mean(ae_j):6.2f}%")
    print(f"  max    |err|     = {np.max(ae_j):6.2f}%")
    print(f"  #|err|>30%       = {(ae_j > 30).sum():3d} / {n}")
    print(f"  #|err|>50%       = {(ae_j > 50).sum():3d} / {n}")
    print()

    # ───── Top outliers in joint fit ─────
    print("─" * 78)
    print(" Top |err|>20% outliers on JOINT-fit form")
    print("─" * 78)
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_form':>7s}  {'err%':>7s}  "
          f"{'φ_AM':>5s} {'CN':>5s} {'τ':>4s}")
    order = np.argsort(-ae_j)
    shown = 0
    for i in order:
        if ae_j[i] <= 20 or shown >= 15: break
        nm = names[i] if i < len(names) else f"(idx{i})"
        print(f"  {nm[:32]:32s}  {a[i,5]:7.4f}  "
              f"{float(np.exp(pred_log_joint[i])):7.4f}  "
              f"{err_j[i]:+7.1f}  {a[i,0]:5.3f} {a[i,1]:5.2f} {a[i,4]:4.2f}")
        shown += 1
    if shown == 0:
        print("  (joint fit captures everything within 20%)")
    print()

    # ───── Interpretation ─────
    print("=" * 78)
    print(" INTERPRETATION (vs Bruggeman / σ_ionic-form physics)")
    print("=" * 78)
    physical_brug = (1.5, 2.0, 0.5, 3.0)  # σ_ionic-style exponents
    print(f"  {'term':10s}  {'data-best':>11s}  {'Bruggeman':>11s}  {'σ_ionic':>9s}  comment")
    interp = [
        ("φ_AM",  coef[0], 1.5, 1.5),
        ("CN_AM", coef[1], 0.0, 2.0),
        ("cov",   coef[2], 0.5, 0.5),
        ("f_p_e", coef[3], 1.0, 3.0),
    ]
    for nm, fit_v, brug_v, ion_v in interp:
        if abs(fit_v - ion_v) < 0.3:
            cm = "matches σ_ionic structure"
        elif abs(fit_v - brug_v) < 0.3:
            cm = "matches plain Bruggeman"
        elif abs(fit_v) < 0.2:
            cm = "≈ 0  (term not informative)"
        elif fit_v < 0:
            cm = "WRONG SIGN — anti-correlated?"
        else:
            cm = "intermediate / novel exponent"
        print(f"  {nm:10s}  {fit_v:+11.3f}  {brug_v:+11.2f}  {ion_v:+9.2f}  {cm}")
    print()
    print("=" * 78)
    print(" NEXT STEPS")
    print("=" * 78)
    print("  1. If LOOCV (Stage 2) > 0.5 → joint fit is the new baseline;")
    print("     lock exponents to clean fractions near fitted values and")
    print("     iterate on remaining residual structure.")
    print("  2. If LOOCV still negative → form structure is wrong.  Try:")
    print("     - drop CN entirely (b ≈ 0 in fit)")
    print("     - add thickness term (T/d_AM geometric factor)")
    print("     - composition-dependent (SAT-blend) AM threshold")
    print("  3. Outlier audit (analogous to σ_ionic _EXCLUDED_NAMES):")
    print("     check sibling spreads for the worst |err| cases.")
    print("  4. Once LOOCV > 0.7 reuse σ_ionic Bayesian / bootstrap toolkit.")


if __name__ == '__main__':
    main()
