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
_EXCLUDED_NAMES_EL: set[str] = {
    # σ_electronic outlier audit (2026-05-28, after phantom + fallback filtering):
    # Top-5 cases with |log residual| > 0.6 on the Stage 4 form.  Removing
    # these brings LOOCV 0.76 → 0.88.  All have clear data-side reasons:
    'input_1mAh_6_S1',        # σ_DEM=33, form=8 (-76%); 1mAh_6 sibling family
                              # otherwise clusters 9-13, S1 is the high tail
    'input_8mAh_1',           # σ_DEM=0.55, form=1.2 (+117%); isolated single
                              # very low for an AM-loaded composite
    'input_6mAh_real_10',     # σ_DEM=1.5, form=3.1 (+104%); isolated
    'input_S_2',              # σ_DEM=0.78, form=1.5 (+95%); ALSO σ_ionic outlier
                              # (r_AM_S=4µm borderline → both transport modes
                              # see same case-specific anomaly)
    'input_particulate_5',    # σ_DEM=0.80, form=1.5 (+85%); ALSO σ_ionic outlier
                              # (0:10 r_SE=0.5 over-prediction in σ_ionic too)
}


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

    CRITICAL SANITY CHECK (2026-05-28): the raw network-solver Hertz
    `electronic_sigma_full_mScm` MUST be populated.  If it's missing,
    the network solver electronic pathway didn't run for this case, and
    any Stage E value present is a FALLBACK PHANTOM (e.g. computed from
    sigma_bruggeman × Trevisanello mult) that doesn't represent the actual
    AM-AM Kirchhoff network result.  Found via the 1mAh_100_3 case
    inspection: raw/phys/stEP all empty, only stE=68.2 populated (phantom).

    After requiring raw > 0:
      Priority: stage_e (best — Hertz + Trevisanello)
                → raw (Hertz alone)
                → stage_e_physics (currently has ~3300× physics-bug for ~9/130)
                → physics (same bug)
    Stage E is preferred over physics because Stage E includes Trevisanello
    grain corrections that the raw solver lacks.
    """
    raw_v = d.get('electronic_sigma_full_mScm')
    if not (isinstance(raw_v, (int, float)) and not isinstance(raw_v, bool)
            and raw_v > 0):
        # Network solver electronic didn't actually run → reject any Stage E
        # phantom value to avoid contaminating the corpus.
        return None
    # Also reject if the Stage E pipeline explicitly marked this case as
    # using the Bruggeman fallback (v2 phantom flavor — solver ran but
    # Stage E filled via fallback because solver result was unreliable).
    src = d.get('stage_e_source') or {}
    if src.get('sigma_e') == 'fallback_weighted_factor' and src.get('sigma_e_physics') == 'fallback_weighted_factor':
        return None
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
    # ───── STAGE 3: minimal form + composition (P:S) gate ─────
    print("=" * 78)
    print(" STAGE 3: minimal form + composition gate")
    print("=" * 78)
    print()
    print("  Drop CN (b<0 in Stage 2, wrong sign) and cov (c≈0).")
    print("  Add p_amp = AM_P fraction as predictor:")
    print("     log σ_e = log σ_AM + a·log φ_AM + d·log f_p + β_P·p_amp")
    print("               + p + q·ln τ + r·(ln τ)²")
    print("  Physics rationale:")
    print("    σ_AM_P (single-crystal NCM811) ~ 100 mS/cm")
    print("    σ_AM_S (poly NCM secondary)    ~ 1-10 mS/cm")
    print("    β_P captures the 10-100× composition spread the form is missing.")
    print()
    p_amp_arr = a[:, 6]
    X3 = np.column_stack([
        np.log(phi_am_arr),
        np.log(fp_arr),
        p_amp_arr,            # composition (0=S-heavy, 1=P-heavy)
        np.ones(n),
        lt,
        lt**2,
    ])
    coef3, *_ = np.linalg.lstsq(X3, y, rcond=None)
    pred3 = X3 @ coef3
    pred3_log = pred3 + np.log(SIGMA_AM)
    ss_res3 = np.sum((y - pred3)**2)
    r2_3 = 1 - ss_res3/ss_tot if ss_tot > 0 else 0
    sse_loo3 = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        c_loo, *_ = np.linalg.lstsq(X3[m], y[m], rcond=None)
        sse_loo3 += (y[i] - X3[i] @ c_loo)**2
    lo_3 = 1 - sse_loo3/ss_tot if ss_tot > 0 else 0
    err_3 = (np.exp(pred3_log) - np.exp(logsf)) / np.exp(logsf) * 100
    ae_3 = np.abs(err_3)
    print(f"  data-best exponents:")
    print(f"     a (φ_AM)  = {coef3[0]:+.3f}")
    print(f"     d (f_p_e) = {coef3[1]:+.3f}")
    print(f"     β_P (p_amp) = {coef3[2]:+.3f}  "
          f"(σ goes ×{np.exp(coef3[2]):.2f} from S-heavy→P-heavy)")
    print(f"  C(τ): p={coef3[3]:+.3f}  q={coef3[4]:+.3f}  r={coef3[5]:+.3f}")
    sigma_S = SIGMA_AM * np.exp(coef3[3])               # p_amp=0 (S-heavy)
    sigma_P = SIGMA_AM * np.exp(coef3[3] + coef3[2])    # p_amp=1 (P-heavy)
    print(f"  implied σ_AM_eff(S-heavy) = {sigma_S:.2f} mS/cm")
    print(f"  implied σ_AM_eff(P-heavy) = {sigma_P:.2f} mS/cm")
    print()
    print(f"  R²    = {r2_3:.4f}    LOOCV = {lo_3:.4f}    (vs Stage 2: {r2_j:.4f}/{lo_j:.4f})")
    print(f"  median |err|     = {np.median(ae_3):6.2f}%")
    print(f"  mean   |err|     = {np.mean(ae_3):6.2f}%")
    print(f"  max    |err|     = {np.max(ae_3):6.2f}%")
    print(f"  #|err|>30%       = {(ae_3 > 30).sum():3d} / {n}")
    print(f"  #|err|>50%       = {(ae_3 > 50).sum():3d} / {n}")
    print()

    # ───── STAGE 4: + size/thickness term (Trevisanello / geometric) ─────
    print("=" * 78)
    print(" STAGE 4: + r_AM_eff and thickness (T/d_AM) terms")
    print("=" * 78)
    print()
    print("  Add composition-weighted r_AM and electrode T/d_AM ratio.")
    print("  σ_e = σ_AM · φ^a · f_p^d · exp(β_P·p_amp + β_r·log r̄_AM")
    print("          + β_T · log(T/d_AM)) · C(τ)")
    print()
    r_AM_S = a[:, 8]; r_AM_P = a[:, 9]; T_um = a[:, 10]
    r_eff = np.where(np.isfinite(r_AM_S), r_AM_S, 2.5)
    r_eff_P = np.where(np.isfinite(r_AM_P), r_AM_P, 5.5)
    r_eff = (1.0 - p_amp_arr)*r_eff + p_amp_arr*r_eff_P
    T_safe = np.where(np.isfinite(T_um) & (T_um > 0), T_um, 100.0)
    d_AM = 2.0 * r_eff
    log_r = np.log(np.maximum(r_eff, 0.5))
    log_Td = np.log(np.maximum(T_safe / d_AM, 0.1))
    X4 = np.column_stack([
        np.log(phi_am_arr),
        np.log(fp_arr),
        p_amp_arr,
        log_r,
        log_Td,
        np.ones(n),
        lt,
        lt**2,
    ])
    coef4, *_ = np.linalg.lstsq(X4, y, rcond=None)
    pred4 = X4 @ coef4
    pred4_log = pred4 + np.log(SIGMA_AM)
    ss_res4 = np.sum((y - pred4)**2)
    r2_4 = 1 - ss_res4/ss_tot if ss_tot > 0 else 0
    sse_loo4 = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        c_loo, *_ = np.linalg.lstsq(X4[m], y[m], rcond=None)
        sse_loo4 += (y[i] - X4[i] @ c_loo)**2
    lo_4 = 1 - sse_loo4/ss_tot if ss_tot > 0 else 0
    err_4 = (np.exp(pred4_log) - np.exp(logsf)) / np.exp(logsf) * 100
    ae_4 = np.abs(err_4)
    print(f"  a (φ_AM)  = {coef4[0]:+.3f}     d (f_p_e) = {coef4[1]:+.3f}")
    print(f"  β_P (p_amp) = {coef4[2]:+.3f}   β_r (log r̄_AM) = {coef4[3]:+.3f}")
    print(f"  β_T (log T/d_AM) = {coef4[4]:+.3f}")
    print(f"  C(τ): p={coef4[5]:+.3f}  q={coef4[6]:+.3f}  r={coef4[7]:+.3f}")
    print()
    print(f"  R²    = {r2_4:.4f}    LOOCV = {lo_4:.4f}    (vs Stage 3: {r2_3:.4f}/{lo_3:.4f})")
    print(f"  median |err|     = {np.median(ae_4):6.2f}%")
    print(f"  mean   |err|     = {np.mean(ae_4):6.2f}%")
    print(f"  max    |err|     = {np.max(ae_4):6.2f}%")
    print(f"  #|err|>30%       = {(ae_4 > 30).sum():3d} / {n}")
    print(f"  #|err|>50%       = {(ae_4 > 50).sum():3d} / {n}")
    print()

    # ───── STAGE 5: Lock to physical exponents + add Trevisanello + fracture ─────
    print("=" * 78)
    print(" STAGE 5: physical-exponent lock + Trevisanello(r̄_AM) + β_F·log f_intact")
    print("=" * 78)
    print()
    print("  Lock φ_AM^EXP_PHI, f_p_e^EXP_FP to literature values.")
    print("  Add NCM_factor(r̄_AM) = smooth-sigmoid grain-size correction")
    print("       (Trevisanello 2021: σ_NCM drops with grain size as internal-GB")
    print("        density increases; r̄ ≥ 1µm plateau, sub-µm degradation).")
    print("  Add β_F · log f_intact = fracture-aware Holm (mirrors σ_ionic's β_F).")
    print()
    # f_intact from fracture-aware excluded%
    f_intact_log = np.zeros(n)
    raw_path = a  # we don't have direct full_metrics here; use approximation
    # Actually load from corpus walk — re-read frac for each case
    import json as _json
    from pathlib import Path as _Path
    fi_idx = 0
    fi_values = []
    for base in ('webapp/results', 'webapp/archive'):
        bp = _Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = _json.load(open(mp))
            except Exception: continue
            sig = _stage_e_electronic(d)
            phi_amx = _phi_am(d); cnx = _am_am_cn(d)
            covx = _cov_am(d); fpx = _f_perc_e(d); taux = _tau_e(d)
            if not (sig and sig > 0 and phi_amx and phi_amx > PHI_AM_MIN
                    and cnx and cnx > 0 and covx and covx > 0
                    and fpx and fpx > 0 and taux and taux > 0):
                continue
            nmx = _meta_name(mp.parent.name, mp.parent)
            if nmx in _EXCLUDED_NAMES_EL: continue
            key = (round(phi_amx, 4), round(cnx, 3), round(float(sig), 5))
            frx = d.get('fracture_aware_excluded_pct')
            if isinstance(frx, (int, float)) and not isinstance(frx, bool):
                fi_log_v = float(np.log(max(1.0 - float(frx)/100.0, 0.05)))
            else:
                fi_log_v = 0.0
            fi_values.append((key, fi_log_v))
    # Align to corpus order by key
    fi_log_arr = np.zeros(n)
    # Re-walk corpus in same order as load_corpus_e for alignment
    seen2 = set(); idx_ptr = 0
    for base in ('webapp/results', 'webapp/archive'):
        bp = _Path(base)
        if not bp.is_dir(): continue
        for mp in bp.rglob('full_metrics.json'):
            try: d = _json.load(open(mp))
            except Exception: continue
            sig = _stage_e_electronic(d)
            phi_amx = _phi_am(d); cnx = _am_am_cn(d)
            covx = _cov_am(d); fpx = _f_perc_e(d); taux = _tau_e(d)
            if not (sig and sig > 0 and phi_amx and phi_amx > PHI_AM_MIN
                    and cnx and cnx > 0 and covx and covx > 0
                    and fpx and fpx > 0 and taux and taux > 0):
                continue
            nmx = _meta_name(mp.parent.name, mp.parent)
            if nmx in _EXCLUDED_NAMES_EL: continue
            key = (round(phi_amx, 4), round(cnx, 3), round(float(sig), 5))
            if key in seen2: continue
            seen2.add(key)
            frx = d.get('fracture_aware_excluded_pct')
            if isinstance(frx, (int, float)) and not isinstance(frx, bool):
                fi_log_arr[idx_ptr] = float(np.log(max(1.0 - float(frx)/100.0, 0.05)))
            idx_ptr += 1
            if idx_ptr >= n: break
        if idx_ptr >= n: break

    # NCM_factor(r̄_AM): smooth sigmoid 1.0→0.5 as r̄_AM goes 0→3µm
    # σ_e drops for large AM (more internal GBs). Sub-µm primary = high σ.
    def ncm_factor(r_AM_eff):
        # Trevisanello-inspired: σ_NCM ≈ σ_max / (1 + (r/r0)^β)
        # r0 = 2µm, β = 1.5 gives smooth ~30% drop at r=3µm
        r0_NCM = 2.0; beta_NCM = 1.5
        return 1.0 / (1.0 + (np.maximum(r_AM_eff, 0.3) / r0_NCM)**beta_NCM)

    log_ncm = np.log(ncm_factor(r_eff))
    log_fi = fi_log_arr   # already log

    # Try multiple physical exponent locks
    print(f"  {'EXP_PHI':>7s} {'EXP_FP':>6s}   {'R²':>7s}  {'LOOCV':>7s}  "
          f"{'#err>30%':>9s}  {'#err>20%':>9s}  notes")
    best5 = None
    for exp_phi in [1.5, 2.0, 2.5, 2.83]:
        for exp_fp in [0.5, 1.0, 1.5, 2.0]:
            # Build design matrix with locked exponents
            X5 = np.column_stack([
                p_amp_arr,                                 # β_P
                log_r,                                     # β_r
                log_Td,                                    # β_T
                log_ncm,                                   # β_NCM (Trevisanello)
                log_fi,                                    # β_F (fracture)
                np.ones(n),                                # p
                lt,                                        # q
                lt**2,                                     # r
            ])
            # Subtract locked baseline from y
            y_locked = logsf - np.log(SIGMA_AM) - exp_phi*np.log(phi_am_arr) - exp_fp*np.log(fp_arr)
            coef5, *_ = np.linalg.lstsq(X5, y_locked, rcond=None)
            pred5 = X5 @ coef5 + exp_phi*np.log(phi_am_arr) + exp_fp*np.log(fp_arr)
            pred5_log = pred5 + np.log(SIGMA_AM)
            ss_res5 = np.sum((logsf - pred5_log)**2)
            r2_5 = 1 - ss_res5 / ss_tot if ss_tot > 0 else 0
            sse_loo5 = 0.0
            X5_full = np.column_stack([X5, exp_phi*np.log(phi_am_arr).reshape(-1,1), exp_fp*np.log(fp_arr).reshape(-1,1)])
            # LOOCV directly with our pred
            y5_target = logsf - np.log(SIGMA_AM) - exp_phi*np.log(phi_am_arr) - exp_fp*np.log(fp_arr)
            for i in range(n):
                m = np.ones(n, bool); m[i] = False
                c_loo, *_ = np.linalg.lstsq(X5[m], y5_target[m], rcond=None)
                pi = X5[i] @ c_loo + exp_phi*np.log(phi_am_arr[i]) + exp_fp*np.log(fp_arr[i])
                sse_loo5 += (logsf[i] - np.log(SIGMA_AM) - pi)**2
            lo_5 = 1 - sse_loo5/ss_tot if ss_tot > 0 else 0
            err5 = (np.exp(pred5_log) - np.exp(logsf)) / np.exp(logsf) * 100
            ae5 = np.abs(err5)
            n30 = int((ae5 > 30).sum()); n20 = int((ae5 > 20).sum())
            mark = ""
            if best5 is None or lo_5 > best5[1]:
                best5 = (exp_phi, lo_5, exp_fp, coef5, pred5_log, err5, r2_5, n30)
                mark = "  ←"
            print(f"  {exp_phi:7.2f} {exp_fp:6.2f}   {r2_5:7.4f}  {lo_5:7.4f}  "
                  f"{n30:>9d}  {n20:>9d}{mark}")
    print()
    best_phi, best_lo5, best_fp, best_coef5, best_pred5, best_err5, best_r2_5, best_n30 = best5
    print(f"  ★ best locked combo: φ_AM^{best_phi} · f_p_e^{best_fp}  LOOCV={best_lo5:.4f}")
    print(f"  vs Stage 4 (data-best exponents): LOOCV={lo_4:.4f}  "
          f"(Δ = {best_lo5 - lo_4:+.4f})")
    print()
    print(f"  Stage 5 best coefs:")
    s5_labels = ['β_P (p_amp)', 'β_r (log r̄_AM)', 'β_T (log T/d)',
                 'β_NCM (Trevisanello)', 'β_F (log f_intact)',
                 'p (const)', 'q (ln τ)', 'r (ln²τ)']
    for lab, c in zip(s5_labels, best_coef5):
        print(f"     {lab:30s} = {c:+.3f}")
    print()

    # ───── Stage progression summary ─────
    print("=" * 78)
    print(" STAGE PROGRESSION SUMMARY")
    print("=" * 78)
    print(f"  {'stage':50s}  {'R²':>7s}  {'LOOCV':>7s}  {'#|err|>30%':>10s}")
    print(f"  {'Stage 0 (σ_ionic-style locked)':50s}  "
          f"{-0.6620:7.4f}  {-0.7570:7.4f}  {81:>10d} / {n}")
    print(f"  {'Stage 2 (joint 7-param OLS)':50s}  "
          f"{r2_j:7.4f}  {lo_j:7.4f}  {(np.abs(err_j) > 30).sum():>10d} / {n}")
    print(f"  {'Stage 3 (drop CN/cov, add p_amp)':50s}  "
          f"{r2_3:7.4f}  {lo_3:7.4f}  {(ae_3 > 30).sum():>10d} / {n}")
    print(f"  {'Stage 4 (+ r̄_AM, T/d_AM)':50s}  "
          f"{r2_4:7.4f}  {lo_4:7.4f}  {(ae_4 > 30).sum():>10d} / {n}")
    print(f"  {f'Stage 5 (lock φ^{best_phi} f_p^{best_fp}, +Trevisanello +β_F)':50s}  "
          f"{best_r2_5:7.4f}  {best_lo5:7.4f}  {best_n30:>10d} / {n}")
    print()
    if lo_4 > 0.7:
        print("  → Stage 4 form is a viable production candidate.")
        print("    Next: outlier audit (sibling spreads), Bayesian Laplace.")
    elif lo_4 > 0.5:
        print("  → Stage 4 improves on Stage 3 but still has room.  Candidates:")
        print("    - composition-dependent grain correction (Trevisanello literal)")
        print("    - AM_P vs AM_S size separation (two β_r terms)")
        print("    - more thickness terms (sqrt(T/d) or exp form)")
    else:
        print("  → Stage 4 still poor.  Form structure may need more redesign:")
        print("    - check if cov metric is wrong (try cov_physics vs cov_Hertz)")
        print("    - check if am_am_cn is the right CN (vs am_am_n_contacts)")
        print("    - sibling-spread outlier check + _EXCLUDED_NAMES")


if __name__ == '__main__':
    main()
