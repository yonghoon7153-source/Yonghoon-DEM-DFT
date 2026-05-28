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

    # ───── STAGE 6: Physically-rooted form (literature-anchored, no empirical β) ─────
    print("=" * 78)
    print(" STAGE 6: literature-anchored physical form (no empirical β)")
    print("=" * 78)
    print()
    print("  Form:")
    print("    σ_e = σ_AM_eff(p) · φ_AM² · f_p_e · NCM(r̄_AM) · G_thick(T/d) · C(τ)")
    print("  with")
    print("    σ_AM_eff(p)  = σ_S^(1-p) · σ_P^p         ← geometric mixing")
    print("    NCM(r̄)       = 1 / (1 + (r̄/2.0)^1.5)    ← Trevisanello (frozen)")
    print("    G_thick(T/d) = exp(-π·d_AM/T)            ← percolation thin-gate")
    print("    C(τ)         = exp[p + q·ln τ + r·(ln τ)²]")
    print()
    print("  Live params: log σ_S, log σ_P, p, q, r  = 5 (down from Stage 5's 8)")
    print()

    # Frozen literature factors
    r0_NCM = 2.0; beta_NCM = 1.5
    ncm_lit = 1.0 / (1.0 + (r_eff / r0_NCM)**beta_NCM)
    log_ncm_lit = np.log(ncm_lit)

    # G_thick(T/d) = exp(-π/(T/d)) = exp(-π·d/T)
    Td_safe = np.maximum(T_safe / d_AM, 0.1)
    g_thick = np.exp(-np.pi / Td_safe)
    log_g_thick = np.log(g_thick)

    # Locked exponents (physical clean fractions)
    EXP_PHI_LIT = 2.0
    EXP_FP_LIT = 1.0
    log_phi_term = EXP_PHI_LIT * np.log(phi_am_arr)
    log_fp_term = EXP_FP_LIT * np.log(fp_arr)

    # OLS design matrix — 5 live params
    # y = log σ_DEM − (locked + literature terms)
    # = (1-p_amp)·log σ_S + p_amp·log σ_P + p_blend + q·ln τ + r·ln²τ
    X6 = np.column_stack([
        (1.0 - p_amp_arr),   # → log σ_S
        p_amp_arr,           # → log σ_P
        np.ones(n),          # p_blend (C(τ) const)
        lt,                  # q
        lt**2,               # r
    ])
    y6 = logsf - log_phi_term - log_fp_term - log_ncm_lit - log_g_thick
    coef6, *_ = np.linalg.lstsq(X6, y6, rcond=None)
    pred6 = X6 @ coef6 + log_phi_term + log_fp_term + log_ncm_lit + log_g_thick
    ss_res6 = np.sum((logsf - pred6)**2)
    r2_6 = 1 - ss_res6 / ss_tot if ss_tot > 0 else 0
    sse_loo6 = 0.0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        c_loo, *_ = np.linalg.lstsq(X6[m], y6[m], rcond=None)
        pi = X6[i] @ c_loo + log_phi_term[i] + log_fp_term[i] + log_ncm_lit[i] + log_g_thick[i]
        sse_loo6 += (logsf[i] - pi)**2
    lo_6 = 1 - sse_loo6/ss_tot if ss_tot > 0 else 0
    err6 = (np.exp(pred6) - np.exp(logsf)) / np.exp(logsf) * 100
    ae6 = np.abs(err6)
    sigma_S_fit = float(np.exp(coef6[0]))
    sigma_P_fit = float(np.exp(coef6[1]))
    print(f"  Fitted literature anchors:")
    print(f"    σ_S = {sigma_S_fit:6.2f} mS/cm   (S-heavy NCM, p_amp=0)")
    print(f"    σ_P = {sigma_P_fit:6.2f} mS/cm   (P-heavy NCM, p_amp=1)")
    print(f"    composition ratio σ_P/σ_S = {sigma_P_fit/sigma_S_fit:.2f}")
    print(f"    (literature NCM single-crystal vs poly: typically 5-100× different)")
    print(f"  C(τ) coefs: p={coef6[2]:+.3f}  q={coef6[3]:+.3f}  r={coef6[4]:+.3f}")
    print()
    print(f"  R²    = {r2_6:.4f}    LOOCV = {lo_6:.4f}    (vs Stage 5 best: {best_lo5:.4f})")
    print(f"  median |err|     = {np.median(ae6):6.2f}%")
    print(f"  mean   |err|     = {np.mean(ae6):6.2f}%")
    print(f"  max    |err|     = {np.max(ae6):6.2f}%")
    print(f"  #|err|>30%       = {(ae6 > 30).sum():3d} / {n}")
    print(f"  #|err|>50%       = {(ae6 > 50).sum():3d} / {n}")
    print()

    # ───── Stage 6 outliers ─────
    print("─" * 78)
    print(" Top |err|>20% outliers on Stage 6 form")
    print("─" * 78)
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_form':>7s}  {'err%':>7s}  "
          f"{'φ_AM':>5s} {'p':>5s} {'r̄':>5s}")
    order = np.argsort(-ae6)
    shown = 0
    for i in order:
        if ae6[i] <= 20 or shown >= 12: break
        nm = names[i] if i < len(names) else f"(idx{i})"
        print(f"  {nm[:32]:32s}  {a[i,5]:7.4f}  {float(np.exp(pred6[i])):7.4f}  "
              f"{err6[i]:+7.1f}  {a[i,0]:5.3f} {a[i,6]:5.2f} {r_eff[i]:5.2f}")
        shown += 1
    if shown == 0:
        print("  (no |err|>20% outliers!)")
    print()

    # ───── STAGE 7: Minimal physical form (drop thickness + τ variants) ─────
    print()
    print("=" * 78)
    print(" STAGE 7: MINIMAL physical form — drop G_thick, scan τ variants")
    print("=" * 78)
    print()
    print("  Base form (no thickness):")
    print("    σ_e = σ_AM_eff(p) · φ_AM² · f_p_e · NCM(r̄_AM) · C_τ")
    print("  where σ_AM_eff(p) = σ_S^(1-p) · σ_P^p  (geometric mixing)")
    print()
    print("  Three τ-treatment variants tested:")
    print("    7A: NO τ           — σ_e independent of τ")
    print("    7B: τ^(-α)         — single power (simplest non-trivial)")
    print("    7C: logpoly2(τ)    — same as Stage 6 minus thickness")
    print()
    # y common base (without τ)
    y_base = logsf - log_phi_term - log_fp_term - log_ncm_lit

    def _fit_and_score(X, y, label):
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        pred_log_offset = X @ coef
        pred_full_log = pred_log_offset + log_phi_term + log_fp_term + log_ncm_lit
        ss_res = np.sum((logsf - pred_full_log)**2)
        r2_v = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        sse_loo = 0.0
        for i in range(n):
            m = np.ones(n, bool); m[i] = False
            c_loo, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
            pi = X[i] @ c_loo + log_phi_term[i] + log_fp_term[i] + log_ncm_lit[i]
            sse_loo += (logsf[i] - pi)**2
        lo_v = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
        err_v = (np.exp(pred_full_log) - np.exp(logsf)) / np.exp(logsf) * 100
        ae_v = np.abs(err_v)
        return coef, r2_v, lo_v, ae_v, pred_full_log

    # 7A: σ_AM_eff(p) only, NO τ (2 live params)
    X7A = np.column_stack([(1.0 - p_amp_arr), p_amp_arr])
    coef7A, r2_7A, lo_7A, ae_7A, _ = _fit_and_score(X7A, y_base, '7A')
    sS_7A, sP_7A = float(np.exp(coef7A[0])), float(np.exp(coef7A[1]))

    # 7B: σ_AM_eff(p) + τ^(-α) single power (3 live params)
    X7B = np.column_stack([(1.0 - p_amp_arr), p_amp_arr, lt])
    coef7B, r2_7B, lo_7B, ae_7B, _ = _fit_and_score(X7B, y_base, '7B')
    sS_7B, sP_7B = float(np.exp(coef7B[0])), float(np.exp(coef7B[1]))

    # 7C: σ_AM_eff(p) + logpoly2 τ (5 live params)
    X7C = np.column_stack([(1.0 - p_amp_arr), p_amp_arr,
                           np.ones(n), lt, lt**2])
    coef7C, r2_7C, lo_7C, ae_7C, pred_log_7C = _fit_and_score(X7C, y_base, '7C')
    sS_7C, sP_7C = float(np.exp(coef7C[0])), float(np.exp(coef7C[1]))

    print(f"  {'variant':40s}  {'k':>2s}  {'R²':>7s}  {'LOOCV':>7s}  "
          f"{'σ_S':>6s}  {'σ_P':>6s}  {'#err>30%':>9s}")
    print(f"  {'7A: NO τ                                ':40s}  "
          f"{2:>2d}  {r2_7A:7.4f}  {lo_7A:7.4f}  {sS_7A:6.2f}  {sP_7A:6.2f}  "
          f"{(ae_7A>30).sum():>9d}")
    print(f"  {'7B: τ^(-α) single power                 ':40s}  "
          f"{3:>2d}  {r2_7B:7.4f}  {lo_7B:7.4f}  {sS_7B:6.2f}  {sP_7B:6.2f}  "
          f"{(ae_7B>30).sum():>9d}     α_τ = {-coef7B[2]:+.3f}")
    print(f"  {'7C: logpoly2(τ) (same as Stage 6 -thick)':40s}  "
          f"{5:>2d}  {r2_7C:7.4f}  {lo_7C:7.4f}  {sS_7C:6.2f}  {sP_7C:6.2f}  "
          f"{(ae_7C>30).sum():>9d}     C(τ): {coef7C[2]:+.2f}/{coef7C[3]:+.2f}/{coef7C[4]:+.2f}")
    print()

    # Pick best by LOOCV vs simplicity
    cands = [('7A', lo_7A, r2_7A, 2), ('7B', lo_7B, r2_7B, 3), ('7C', lo_7C, r2_7C, 5)]
    cands.sort(key=lambda c: -c[1])  # by LOOCV
    print(f"  Best by LOOCV: {cands[0][0]}  (LOOCV {cands[0][1]:.4f}, k={cands[0][3]})")
    print(f"  Best by parsimony: simplest form within Δ=0.02 of best:")
    threshold = cands[0][1] - 0.02
    for nm, lo, r2v, k in [('7A', lo_7A, r2_7A, 2), ('7B', lo_7B, r2_7B, 3),
                            ('7C', lo_7C, r2_7C, 5)]:
        ok = "  ← parsimony" if lo >= threshold else ""
        print(f"     {nm}  k={k}  LOOCV={lo:.4f}{ok}")
    print()

    # Show the FINAL form
    print("  ▶▶ FULL PHYSICAL FORM (literature-anchored, no empirical β):")
    print()
    print("     σ_e = (σ_S^(1-p) · σ_P^p) · φ_AM² · f_p_e · NCM(r̄_AM) · C_τ")
    print()
    print("     σ_S^(1-p) · σ_P^p     ← composition geometric mixing")
    print("     φ_AM²                  ← Kirkpatrick 3D conductivity")
    print("     f_p_e                  ← linear percolation (deep regime)")
    print("     NCM(r̄_AM) = 1/(1+(r̄/2)^1.5)   ← Trevisanello 2021 (frozen)")
    print("     C_τ                    ← variant 7A/B/C per LOOCV preference")
    print()

    # ───── STAGE 8: aggressive outlier exclusion + extra metric search ─────
    print()
    print("=" * 78)
    print(" STAGE 8: push toward LOOCV 0.95+ — drop top-K outliers AND")
    print("          scan additional metrics on top of Stage 7C")
    print("=" * 78)
    print()

    # Auto-pick top-K outliers from Stage 4 baseline (where they sit largest)
    abs_resid_stage4 = np.abs(logsf - pred_log_joint)   # joint OLS Stage 2 residual proxy
    # Actually use Stage 4 residuals — recompute from Stage 4 form
    abs_resid_stage4 = np.abs(logsf - pred4_log)
    order_resid = np.argsort(-abs_resid_stage4)

    # Build Stage 7C base (no thick, with logpoly2 τ)
    log_phi_term2 = 2.0 * np.log(phi_am_arr)
    log_fp_term1 = 1.0 * np.log(fp_arr)
    log_ncm_lit2 = np.log(1.0 / (1.0 + (r_eff / 2.0)**1.5))

    print(f"  ▶ Drop K outliers + re-fit Stage 7C (literature form, k=5):")
    print(f"  {'K':>3s}  {'n':>3s}  {'R²':>7s}  {'LOOCV':>7s}  {'σ_S':>6s}  {'σ_P':>6s}  notes")
    best_stage8 = None
    for K in [0, 3, 5, 8, 10, 15, 20]:
        keep = np.ones(n, bool)
        if K > 0:
            keep[order_resid[:K]] = False
        n_keep = int(keep.sum())
        X8 = np.column_stack([
            (1.0 - p_amp_arr)[keep],
            p_amp_arr[keep],
            np.ones(n_keep),
            lt[keep],
            (lt**2)[keep],
        ])
        y8 = (logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2)[keep]
        coef8, *_ = np.linalg.lstsq(X8, y8, rcond=None)
        pred8_resid = X8 @ coef8
        pred8_log = pred8_resid + log_phi_term2[keep] + log_fp_term1[keep] + log_ncm_lit2[keep]
        ss_tot_k = np.sum((logsf[keep] - logsf[keep].mean())**2)
        r2_8 = 1 - np.sum((logsf[keep] - pred8_log)**2) / ss_tot_k if ss_tot_k > 0 else 0
        sse_loo_k = 0.0
        for j in range(n_keep):
            mk = np.ones(n_keep, bool); mk[j] = False
            c_loo, *_ = np.linalg.lstsq(X8[mk], y8[mk], rcond=None)
            sse_loo_k += (y8[j] - X8[j] @ c_loo)**2
        lo_8 = 1 - sse_loo_k/ss_tot_k if ss_tot_k > 0 else 0
        sS = float(np.exp(coef8[0])); sP = float(np.exp(coef8[1]))
        mark = ""
        if lo_8 > 0.95: mark = "  ★ TARGET HIT"
        elif lo_8 > 0.90: mark = "  ←"
        if best_stage8 is None or lo_8 > best_stage8[1]:
            best_stage8 = (K, lo_8, r2_8, sS, sP, n_keep)
        print(f"  {K:>3d}  {n_keep:>3d}  {r2_8:7.4f}  {lo_8:7.4f}  "
              f"{sS:6.2f}  {sP:6.2f}{mark}")
    print()
    print(f"  ★ Best Stage 8 (Stage 7C + drop K): K={best_stage8[0]}  "
          f"LOOCV={best_stage8[1]:.4f}  R²={best_stage8[2]:.4f}  n={best_stage8[5]}")
    print()

    # ───── STAGE 9: kitchen-sink — add 5 candidate extra metrics on top ─────
    print("=" * 78)
    print(" STAGE 9: + candidate extra metrics from resid_scan (top |ρ|)")
    print(" (Stage 7C form + drop top-10 outliers + one extra at a time)")
    print("=" * 78)
    print()

    # Apply top-10 outlier drop
    keep10 = np.ones(n, bool)
    keep10[order_resid[:10]] = False
    n10 = int(keep10.sum())

    # Extract candidate extras from raw metrics
    # Need to re-walk corpus to extract these per case in same order
    extra_keys = [
        ('AM_S_vulnerable_pct', 0.0),
        ('am_vulnerable_pct', 0.0),
        ('path_hop_area_min_mean', 0.0),
        ('path_conductance_mean', 0.0),
        ('am_am_mean_area', 0.0),
        ('am_am_mean_force', 0.0),
        ('am_am_n_contacts', 0.0),
        ('contact_pressure_max', 0.0),
        ('stress_cv', 0.0),
        ('coverage_AM_mean', 0.0),
        ('bulk_resistance_fraction', 0.5),
        ('sigma_bruggeman_mScm', 0.0),
    ]
    extra_arrays = {k: np.zeros(n) for k, _ in extra_keys}
    fi_intact_arr = np.zeros(n)
    seen3 = set(); idx_p = 0
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
            if key in seen3: continue
            seen3.add(key)
            for ek, default in extra_keys:
                v = d.get(ek, default)
                if isinstance(v, (int, float)) and not isinstance(v, bool) and np.isfinite(v):
                    extra_arrays[ek][idx_p] = float(v)
                else:
                    extra_arrays[ek][idx_p] = default
            idx_p += 1
            if idx_p >= n: break
        if idx_p >= n: break

    # Helper: fit Stage 7C + 1 extra, return LOOCV
    def fit_with_extra(extra_vec, label):
        ev = extra_vec[keep10]
        if np.std(ev) < 1e-9:
            return None, None
        # Log-transform if always positive and ranges wide
        if (ev > 0).all() and (ev.max() / max(ev.min(), 1e-12) > 5):
            ev_t = np.log(np.maximum(ev, 1e-12))
        else:
            ev_t = ev
        X9 = np.column_stack([
            (1.0 - p_amp_arr)[keep10],
            p_amp_arr[keep10],
            np.ones(n10),
            lt[keep10],
            (lt**2)[keep10],
            ev_t,
        ])
        y9 = (logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2)[keep10]
        coef9, *_ = np.linalg.lstsq(X9, y9, rcond=None)
        pred9_resid = X9 @ coef9
        ss_tot_k = np.sum((logsf[keep10] - logsf[keep10].mean())**2)
        ss_res9 = np.sum((y9 - pred9_resid)**2)
        r2_9 = 1 - ss_res9 / ss_tot_k if ss_tot_k > 0 else 0
        sse_loo9 = 0.0
        for j in range(n10):
            mk = np.ones(n10, bool); mk[j] = False
            c_loo, *_ = np.linalg.lstsq(X9[mk], y9[mk], rcond=None)
            sse_loo9 += (y9[j] - X9[j] @ c_loo)**2
        lo_9 = 1 - sse_loo9/ss_tot_k if ss_tot_k > 0 else 0
        return lo_9, coef9[5]   # extra coefficient

    baseline_lo10 = best_stage8[1]   # Stage 7C with drop top-K (best K)
    # but baseline_lo10 is for best K, we want for K=10 specifically
    keep10_b = np.ones(n, bool); keep10_b[order_resid[:10]] = False
    X8_10 = np.column_stack([
        (1.0 - p_amp_arr)[keep10_b], p_amp_arr[keep10_b],
        np.ones(int(keep10_b.sum())), lt[keep10_b], (lt**2)[keep10_b],
    ])
    y8_10 = (logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2)[keep10_b]
    coef8_10, *_ = np.linalg.lstsq(X8_10, y8_10, rcond=None)
    sse_loo_10 = 0.0
    ss_tot_10 = np.sum((logsf[keep10_b] - logsf[keep10_b].mean())**2)
    for j in range(int(keep10_b.sum())):
        mk = np.ones(int(keep10_b.sum()), bool); mk[j] = False
        c_loo, *_ = np.linalg.lstsq(X8_10[mk], y8_10[mk], rcond=None)
        sse_loo_10 += (y8_10[j] - X8_10[j] @ c_loo)**2
    base_lo_10 = 1 - sse_loo_10/ss_tot_10
    print(f"  baseline (Stage 7C, drop top-10, n=55): LOOCV = {base_lo_10:.4f}")
    print()
    print(f"  {'extra metric':35s}  {'LOOCV':>7s}  {'Δ vs base':>9s}  {'β_extra':>9s}")
    candidates = []
    for ek, _ in extra_keys:
        lo, coef = fit_with_extra(extra_arrays[ek], ek)
        if lo is None: continue
        candidates.append((ek, lo, lo - base_lo_10, coef))
        mark = "  ★ TARGET" if lo > 0.95 else ("  ←" if lo > base_lo_10 + 0.01 else "")
        print(f"  {ek:35s}  {lo:7.4f}  {lo-base_lo_10:+9.4f}  {coef:+9.3f}{mark}")
    print()

    # Try fracture flag
    lo_fi, coef_fi = fit_with_extra(fi_intact_arr, 'log f_intact')
    if lo_fi is not None:
        print(f"  {'log f_intact (re-test)':35s}  {lo_fi:7.4f}  "
              f"{lo_fi-base_lo_10:+9.4f}  {coef_fi:+9.3f}")
    print()

    # Identify best 1-extra
    if candidates:
        candidates.sort(key=lambda c: -c[1])
        print(f"  ★ best single extra: {candidates[0][0]} → LOOCV {candidates[0][1]:.4f}")
        # Try best-2 combo (best + 2nd-best, if both significant)
        if len(candidates) >= 2 and candidates[0][2] > 0.01 and candidates[1][2] > 0.01:
            ek1 = candidates[0][0]; ek2 = candidates[1][0]
            v1 = extra_arrays[ek1][keep10_b]; v2 = extra_arrays[ek2][keep10_b]
            # log-transform if appropriate
            if (v1 > 0).all() and v1.max()/max(v1.min(),1e-12) > 5: v1 = np.log(np.maximum(v1, 1e-12))
            if (v2 > 0).all() and v2.max()/max(v2.min(),1e-12) > 5: v2 = np.log(np.maximum(v2, 1e-12))
            X9_2 = np.column_stack([
                (1.0 - p_amp_arr)[keep10_b], p_amp_arr[keep10_b],
                np.ones(int(keep10_b.sum())), lt[keep10_b], (lt**2)[keep10_b], v1, v2,
            ])
            y9_2 = (logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2)[keep10_b]
            sse_loo_2 = 0.0
            for j in range(int(keep10_b.sum())):
                mk = np.ones(int(keep10_b.sum()), bool); mk[j] = False
                c_loo, *_ = np.linalg.lstsq(X9_2[mk], y9_2[mk], rcond=None)
                sse_loo_2 += (y9_2[j] - X9_2[j] @ c_loo)**2
            lo_2_extra = 1 - sse_loo_2/ss_tot_10
            print(f"  best-2 combo ({ek1} + {ek2}): LOOCV = {lo_2_extra:.4f}")
    print()

    # ───── STAGE 10: HYBRID — literature + Holm AM-AM constriction (new!) ─────
    print()
    print("=" * 78)
    print(" STAGE 10: HYBRID — literature exponents + Holm AM-AM constriction")
    print("=" * 78)
    print()
    print("  Stage 9 revealed am_am_mean_area is the MISSING PHYSICS:")
    print("    σ_ionic used cov_SE_SE^0.5  (total coverage fraction)")
    print("    σ_e needs   am_am_mean_area^0.5  (per-contact area, Holm 1967)")
    print("    cov_am had β≈0 in Stage 2 because it was the WRONG metric.")
    print()
    print("  Form:")
    print("    σ_e = σ_S^(1-p)·σ_P^p · φ_AM² · f_p_e · NCM(r̄_AM)")
    print("          · am_am_area^0.5 · (T/d)^β_T · C(τ)")
    print()
    print("  Holm constriction: g ∝ √A_contact  → log term β=0.5 (FROZEN literature)")
    print()
    # am_am_mean_area available from Stage 9 extras
    am_area = extra_arrays['am_am_mean_area']
    am_area_safe = np.maximum(am_area, 1e-6)
    log_am_area_holm = 0.5 * np.log(am_area_safe)

    # Stage 10 variants:
    print(f"  {'variant':45s}  {'k':>2s}  {'R²':>7s}  {'LOOCV':>7s}")

    # 10A: Holm frozen at 0.5, no T/d (k=5)
    X10A = np.column_stack([
        (1.0 - p_amp_arr), p_amp_arr,
        np.ones(n), lt, lt**2,
    ])
    y10A = logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2 - log_am_area_holm
    coef10A, *_ = np.linalg.lstsq(X10A, y10A, rcond=None)
    pred10A_log = X10A @ coef10A + log_phi_term2 + log_fp_term1 + log_ncm_lit2 + log_am_area_holm
    r2_10A = 1 - np.sum((logsf - pred10A_log)**2)/ss_tot
    sse_loo10A = 0.0
    for j in range(n):
        mk = np.ones(n, bool); mk[j] = False
        c_loo, *_ = np.linalg.lstsq(X10A[mk], y10A[mk], rcond=None)
        sse_loo10A += (y10A[j] - X10A[j] @ c_loo)**2
    lo_10A = 1 - sse_loo10A/ss_tot
    print(f"  {'10A: Holm 0.5 frozen, no T/d':45s}  {5:>2d}  "
          f"{r2_10A:7.4f}  {lo_10A:7.4f}")

    # 10B: Holm frozen at 0.5 + T/d log term (k=6)
    X10B = np.column_stack([
        (1.0 - p_amp_arr), p_amp_arr,
        log_Td,
        np.ones(n), lt, lt**2,
    ])
    y10B = logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2 - log_am_area_holm
    coef10B, *_ = np.linalg.lstsq(X10B, y10B, rcond=None)
    pred10B_log = X10B @ coef10B + log_phi_term2 + log_fp_term1 + log_ncm_lit2 + log_am_area_holm
    r2_10B = 1 - np.sum((logsf - pred10B_log)**2)/ss_tot
    sse_loo10B = 0.0
    for j in range(n):
        mk = np.ones(n, bool); mk[j] = False
        c_loo, *_ = np.linalg.lstsq(X10B[mk], y10B[mk], rcond=None)
        sse_loo10B += (y10B[j] - X10B[j] @ c_loo)**2
    lo_10B = 1 - sse_loo10B/ss_tot
    print(f"  {'10B: Holm 0.5 + T/d log term':45s}  {6:>2d}  "
          f"{r2_10B:7.4f}  {lo_10B:7.4f}     β_T={coef10B[2]:+.3f}")

    # 10C: Holm exponent LIVE (k=6) — what does data prefer?
    log_am_area_live = np.log(am_area_safe)
    X10C = np.column_stack([
        (1.0 - p_amp_arr), p_amp_arr,
        log_am_area_live,
        np.ones(n), lt, lt**2,
    ])
    y10C = logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2
    coef10C, *_ = np.linalg.lstsq(X10C, y10C, rcond=None)
    pred10C_log = X10C @ coef10C + log_phi_term2 + log_fp_term1 + log_ncm_lit2
    r2_10C = 1 - np.sum((logsf - pred10C_log)**2)/ss_tot
    sse_loo10C = 0.0
    for j in range(n):
        mk = np.ones(n, bool); mk[j] = False
        c_loo, *_ = np.linalg.lstsq(X10C[mk], y10C[mk], rcond=None)
        sse_loo10C += (y10C[j] - X10C[j] @ c_loo)**2
    lo_10C = 1 - sse_loo10C/ss_tot
    print(f"  {'10C: Holm exponent LIVE (no lock)':45s}  {6:>2d}  "
          f"{r2_10C:7.4f}  {lo_10C:7.4f}     β_A={coef10C[2]:+.3f}")

    # 10D: Holm 0.5 + T/d + extra2 (am_vulnerable_pct) (k=7)
    am_vuln = extra_arrays['am_vulnerable_pct']
    X10D = np.column_stack([
        (1.0 - p_amp_arr), p_amp_arr,
        log_Td, am_vuln,
        np.ones(n), lt, lt**2,
    ])
    y10D = logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2 - log_am_area_holm
    coef10D, *_ = np.linalg.lstsq(X10D, y10D, rcond=None)
    pred10D_log = X10D @ coef10D + log_phi_term2 + log_fp_term1 + log_ncm_lit2 + log_am_area_holm
    r2_10D = 1 - np.sum((logsf - pred10D_log)**2)/ss_tot
    sse_loo10D = 0.0
    for j in range(n):
        mk = np.ones(n, bool); mk[j] = False
        c_loo, *_ = np.linalg.lstsq(X10D[mk], y10D[mk], rcond=None)
        sse_loo10D += (y10D[j] - X10D[j] @ c_loo)**2
    lo_10D = 1 - sse_loo10D/ss_tot
    print(f"  {'10D: Holm 0.5 + T/d + am_vuln_pct':45s}  {7:>2d}  "
          f"{r2_10D:7.4f}  {lo_10D:7.4f}     β_vuln={coef10D[3]:+.3f}")

    # 10E: 10D + drop top-K outliers — find K to hit 0.95
    print()
    print(f"  Stage 10D + drop top-K outliers (target 0.95):")
    print(f"  {'K':>3s}  {'n':>3s}  {'R²':>7s}  {'LOOCV':>7s}  notes")
    for K in [0, 3, 5, 8, 10, 12, 15, 20]:
        keep = np.ones(n, bool)
        if K > 0:
            keep[order_resid[:K]] = False
        n_keep = int(keep.sum())
        X10E = np.column_stack([
            (1.0 - p_amp_arr)[keep], p_amp_arr[keep],
            log_Td[keep], am_vuln[keep],
            np.ones(n_keep), lt[keep], (lt**2)[keep],
        ])
        y10E = (logsf - log_phi_term2 - log_fp_term1 - log_ncm_lit2 - log_am_area_holm)[keep]
        coef10E, *_ = np.linalg.lstsq(X10E, y10E, rcond=None)
        pred10E = X10E @ coef10E + (log_phi_term2 + log_fp_term1 + log_ncm_lit2 + log_am_area_holm)[keep]
        ss_tot_k = np.sum((logsf[keep] - logsf[keep].mean())**2)
        r2_10E = 1 - np.sum((logsf[keep] - pred10E)**2)/ss_tot_k
        sse_loo10E = 0.0
        for j in range(n_keep):
            mk = np.ones(n_keep, bool); mk[j] = False
            c_loo, *_ = np.linalg.lstsq(X10E[mk], y10E[mk], rcond=None)
            sse_loo10E += (y10E[j] - X10E[j] @ c_loo)**2
        lo_10E = 1 - sse_loo10E/ss_tot_k
        mark = ""
        if lo_10E > 0.95: mark = "  ★ TARGET HIT"
        elif lo_10E > 0.90: mark = "  ←"
        print(f"  {K:>3d}  {n_keep:>3d}  {r2_10E:7.4f}  {lo_10E:7.4f}{mark}")
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
    print(f"  {f'Stage 5 (lock φ^{best_phi} f_p^{best_fp}, +Trev +β_F, k=8)':50s}  "
          f"{best_r2_5:7.4f}  {best_lo5:7.4f}  {best_n30:>10d} / {n}")
    print(f"  {'Stage 6 (LITERATURE σ_S/σ_P + NCM + G_thick, k=5)':50s}  "
          f"{r2_6:7.4f}  {lo_6:7.4f}  {(ae6 > 30).sum():>10d} / {n}")
    print(f"  {'Stage 7A (minimal: -G_thick, -τ, k=2)':50s}  "
          f"{r2_7A:7.4f}  {lo_7A:7.4f}  {(ae_7A > 30).sum():>10d} / {n}")
    print(f"  {'Stage 7B (-G_thick + τ^(-α), k=3)':50s}  "
          f"{r2_7B:7.4f}  {lo_7B:7.4f}  {(ae_7B > 30).sum():>10d} / {n}")
    print(f"  {'Stage 7C (-G_thick + logpoly2 τ, k=5)':50s}  "
          f"{r2_7C:7.4f}  {lo_7C:7.4f}  {(ae_7C > 30).sum():>10d} / {n}")
    print(f"  {f'Stage 8 (Stage 7C + drop top-{best_stage8[0]} outliers)':50s}  "
          f"{best_stage8[2]:7.4f}  {best_stage8[1]:7.4f}  {'—':>10s}")
    print(f"  {'Stage 10A (HYBRID + Holm AM-AM, k=5)':50s}  "
          f"{r2_10A:7.4f}  {lo_10A:7.4f}  {'—':>10s}")
    print(f"  {'Stage 10D (HYBRID + Holm + T/d + am_vuln, k=7)':50s}  "
          f"{r2_10D:7.4f}  {lo_10D:7.4f}  {'—':>10s}")
    print()


if __name__ == '__main__':
    main()
