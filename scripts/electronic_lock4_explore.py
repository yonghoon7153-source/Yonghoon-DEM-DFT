#!/usr/bin/env python3
"""Stage 14 — lock φ_AM^4 and re-scan for missing physics terms.

Stage 12 settled at a=3.5 / d=0 (LOOCV 0.9559).  Locking to a=4 (LOOCV 0.9537,
clean integer) we then ask: does ANY additional physics term improve over
the locked baseline?  Each candidate uses the EXACT Stage 12 production
base (Holm + NCM + log σ_S/σ_P mixing + T/d + am_vuln + logpoly2 τ).

Candidates (with physical motivation):
  1. log(am_am_cn)             — AM-AM coordination (σ_ionic CN_SE² analog;
                                  dropped at Stage 2 with wrong sign, RE-TEST
                                  now that other terms absorb collinearity)
  2. log(am_am_n_contacts)     — contact COUNT (Holm extends: total g ∝ √A × n)
  3. log(am_am_mean_force)     — Hertz a-spot ∝ F^(1/3); independent of A?
  4. log(am_am_n × am_am_area) — TOTAL contact channel area (sum vs mean)
  5. log(bulk_resistance_frac) — bulk vs surface conduction split
  6. log(path_conductance_mean)— network-solver path-aware contact stiffness
  7. log(coverage_AM_mean)     — SE coverage on AM (interface BLOCKER?)
  8. φ_AM × log(cn_am)         — density × connectivity interaction
  9. log(phi_AM_S/phi_AM_P)    — phase imbalance (saturate when ≈0/inf)
 10. p_amp × log(cn_am)        — composition-gated CN (if AM_P has lower CN)

For each: LOOCV(Stage 12 base + extra) vs Stage 12 baseline LOOCV.
Threshold to ADD: Δ > +0.005 and physically interpretable β.

Run on WSL (or cloud container — pure numpy, no sklearn):
    python3 scripts/electronic_lock4_explore.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from electronic_nested_cv import (
    load_corpus_e, _stage_e_electronic, _phi_am, _am_am_cn, _cov_am,
    _f_perc_e, _tau_e, _meta_name, _EXCLUDED_NAMES_EL, PHI_AM_MIN, SIGMA_AM,
)


def gather_extra_metrics(a, names):
    """Walk the corpus again in the SAME order as load_corpus_e and
    pull additional per-case metrics not in the core 11-column array."""
    n = len(a)
    extra = {
        'am_am_cn': np.zeros(n),
        'am_am_n_contacts': np.zeros(n),
        'am_am_mean_area': np.zeros(n),
        'am_am_mean_force': np.zeros(n),
        'bulk_resistance_fraction': np.zeros(n),
        'path_conductance_mean': np.zeros(n),
        'coverage_AM_mean': np.zeros(n),
        'phi_AM_S': np.zeros(n),
        'phi_AM_P': np.zeros(n),
    }
    seen = set(); idx = 0
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            if idx >= n:
                break
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            _cid = mp.parent.name
            sig = _stage_e_electronic(d, case_id=_cid)
            phi_am = _phi_am(d); cn_am = _am_am_cn(d)
            cov = _cov_am(d); fp = _f_perc_e(d); tau = _tau_e(d)
            if not (sig and sig > 0 and phi_am and phi_am > PHI_AM_MIN
                    and cn_am and cn_am > 0 and cov and cov > 0
                    and fp and fp > 0 and tau and tau > 0):
                continue
            nm = _meta_name(_cid, mp.parent)
            if nm in _EXCLUDED_NAMES_EL:
                continue
            key = (round(phi_am, 4), round(cn_am, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key)
            for k in extra:
                v = d.get(k, 0)
                if isinstance(v, (int, float)) and not isinstance(v, bool) and np.isfinite(v):
                    extra[k][idx] = float(v)
            idx += 1
        if idx >= n:
            break
    return extra


def build_stage12_base(a):
    """Stage 12 LOCKED at a=4, d=0.  Returns (X_fixed, design_cols, names).
    X_fixed shape: (n, 7) with columns [σ_S, σ_P, β_T, β_v, p, q, r].
    The locked exponent contribution (4·log φ_AM + log NCM + 0.5·log A) is
    subtracted from y, not put in X — same convention as Stage 12 in
    electronic_nested_cv.py.
    """
    n = len(a)
    phi_am = a[:, 0]; tau = a[:, 4]; p_amp = a[:, 6]
    r_AM_S = a[:, 8]; r_AM_P = a[:, 9]; T_um = a[:, 10]
    r_eff = np.where(np.isfinite(r_AM_S), r_AM_S, 2.5)
    r_eff_P = np.where(np.isfinite(r_AM_P), r_AM_P, 5.5)
    r_eff = (1.0 - p_amp)*r_eff + p_amp*r_eff_P
    T_safe = np.where(np.isfinite(T_um) & (T_um > 0), T_um, 100.0)
    d_AM = 2.0 * r_eff
    log_Td = np.log(np.maximum(T_safe / d_AM, 0.1))
    lt = np.log(tau)

    # NCM(r̄) = 1/(1+(r̄/2)^1.5)   Trevisanello literature
    ncm = 1.0 / (1.0 + np.power(np.maximum(r_eff, 0.05) / 2.0, 1.5))
    log_ncm = np.log(np.maximum(ncm, 1e-6))
    return n, phi_am, tau, p_amp, log_Td, log_ncm, lt, T_safe, r_eff, d_AM


def fit_and_loocv(X, y):
    """OLS fit + LOOCV in log space.  Returns (coef, r2, loocv)."""
    n = X.shape[0]
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - float(np.sum((y - pred)**2)) / ss_tot if ss_tot > 0 else 0.0
    sse_loo = 0.0
    for j in range(n):
        m = np.ones(n, bool); m[j] = False
        c_loo, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
        sse_loo += (y[j] - X[j] @ c_loo)**2
    loocv = 1 - float(sse_loo) / ss_tot if ss_tot > 0 else 0.0
    return coef, r2, loocv


def maybe_log_transform(v, name):
    """If positive + spans >5× range, log-transform.  Else center."""
    if (v > 0).all() and v.max() / max(v.min(), 1e-12) > 5:
        return np.log(np.maximum(v, 1e-12)), f"log({name})"
    return v - v.mean(), f"({name})"


def main():
    print("=" * 78)
    print(" STAGE 14 — lock φ_AM^4, scan for missing physics terms")
    print("=" * 78)
    a, names = load_corpus_e()
    n = len(a)
    print(f"  Corpus n = {n} (same as Stage 12)")
    if n < 10:
        print(f"  [ABORT] corpus too small (n={n}).  Need ≥10 cases.")
        print(f"  This script must run on the WSL machine with the full")
        print(f"  webapp/results + webapp/archive populated.")
        return

    logsf = np.log(a[:, 5])
    n_, phi_am, tau, p_amp, log_Td, log_ncm, lt, T_safe, r_eff, d_AM = build_stage12_base(a)

    # Pull extras
    extras = gather_extra_metrics(a, names)
    am_am_area = extras['am_am_mean_area']
    log_holm = 0.5 * np.log(np.maximum(am_am_area, 1e-12))

    # Use a=4 lock + drop top-15 outliers (same exclusion set logic as Stage 12)
    # First do a Stage 11-like preliminary fit to identify residual ranking
    a_lock = 4.0
    log_phi_lock = a_lock * np.log(phi_am)
    am_vuln = extras['am_am_n_contacts']  # placeholder; real am_vuln comes from corpus

    # Actually need am_vulnerable_pct — pull it
    # Re-walk for am_vulnerable_pct (used as β_v term)
    am_vuln_arr = np.zeros(n)
    seen2 = set(); idx = 0
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            if idx >= n:
                break
            try: d = json.load(open(mp))
            except Exception: continue
            _cid = mp.parent.name
            sig = _stage_e_electronic(d, case_id=_cid)
            phi_amx = _phi_am(d); cn_am = _am_am_cn(d)
            cov = _cov_am(d); fp = _f_perc_e(d); taux = _tau_e(d)
            if not (sig and sig > 0 and phi_amx and phi_amx > PHI_AM_MIN
                    and cn_am and cn_am > 0 and cov and cov > 0
                    and fp and fp > 0 and taux and taux > 0):
                continue
            nm = _meta_name(_cid, mp.parent)
            if nm in _EXCLUDED_NAMES_EL:
                continue
            key = (round(phi_amx, 4), round(cn_am, 3), round(float(sig), 5))
            if key in seen2:
                continue
            seen2.add(key)
            v = d.get('AM_S_vulnerable_pct', d.get('am_vulnerable_pct', 0))
            am_vuln_arr[idx] = float(v) if isinstance(v, (int, float)) else 0.0
            idx += 1
        if idx >= n: break

    am_vuln = am_vuln_arr

    # Stage 12 BASELINE design (a=4, d=0, drop NONE first to identify resid)
    X_base = np.column_stack([
        (1.0 - p_amp),     # log σ_S
        p_amp,             # log σ_P
        log_Td,            # β_T
        am_vuln,           # β_v
        np.ones(n),        # p
        lt,                # q
        lt**2,             # r
    ])
    y_base = logsf - log_ncm - log_holm - log_phi_lock

    coef0, r2_full, lo_full = fit_and_loocv(X_base, y_base)
    print(f"  Stage 12 (a=4, d=0, NO outlier drop): R²={r2_full:.4f}  LOOCV={lo_full:.4f}")

    # Apply drop-top-15 (same as Stage 12 in nested_cv)
    pred0 = X_base @ coef0
    resid = np.abs(y_base - pred0)
    order = np.argsort(-resid)
    keep = np.ones(n, bool); keep[order[:15]] = False
    n_k = int(keep.sum())
    print(f"  After drop top-15 (n={n_k}):")

    Xk = X_base[keep]; yk = y_base[keep]
    coef_b, r2_b, lo_b = fit_and_loocv(Xk, yk)
    print(f"    BASELINE  R²={r2_b:.4f}  LOOCV={lo_b:.4f}  ★ Stage 12 lock4 reference")
    print()
    print(f"  σ_S = {np.exp(coef_b[0]):.2f} mS/cm,  σ_P = {np.exp(coef_b[1]):.2f} mS/cm")
    print(f"  β_T = {coef_b[2]:+.3f}  β_v = {coef_b[3]:+.4f}")
    print(f"  C(τ) = {coef_b[4]:+.3f} + {coef_b[5]:+.3f}·lnτ + {coef_b[6]:+.3f}·ln²τ")
    print()

    # ───── Candidate physics terms ─────
    print("─" * 78)
    print(" CANDIDATE EXTRA PHYSICS TERMS (each added singly to Stage 12 base)")
    print("─" * 78)

    cn_am = a[:, 1]   # AM-AM coordination (in core array col 1)

    candidates = []  # (label, raw_vec, physical_meaning)

    candidates.append((
        "log(am_am_cn)",
        cn_am,
        "AM-AM CN: σ_ionic CN_SE² analog; was dropped Stage 2 w/ wrong sign"
    ))

    candidates.append((
        "log(am_am_n_contacts)",
        extras['am_am_n_contacts'],
        "contact COUNT: Holm extension g_tot ∝ √A × n"
    ))

    candidates.append((
        "log(am_am_mean_force)",
        extras['am_am_mean_force'],
        "Hertz force: a-spot radius ∝ F^(1/3), pressure-aware"
    ))

    n_a = extras['am_am_n_contacts'] * extras['am_am_mean_area']
    candidates.append((
        "log(n × A) total area",
        n_a,
        "TOTAL Hertz channel area = sum of all a-spots"
    ))

    candidates.append((
        "log(bulk_R_fraction)",
        extras['bulk_resistance_fraction'],
        "bulk vs surface R split (network-solver derived)"
    ))

    candidates.append((
        "log(path_conductance)",
        extras['path_conductance_mean'],
        "network-solver mean path conductance (composite g)"
    ))

    candidates.append((
        "log(coverage_AM)",
        extras['coverage_AM_mean'],
        "SE coverage on AM surface — interface BLOCKER hypothesis"
    ))

    candidates.append((
        "φ_AM × log(cn_am)",
        phi_am * np.log(np.maximum(cn_am, 1e-3)),
        "density × connectivity interaction"
    ))

    pas = extras['phi_AM_S']; pap = extras['phi_AM_P']
    if (pas > 0).any() or (pap > 0).any():
        ratio = np.where((pas > 0) & (pap > 0), pas / np.maximum(pap, 1e-6), 1.0)
        candidates.append((
            "log(φ_AM_S/φ_AM_P)",
            np.where(ratio > 0, ratio, 1.0),
            "phase imbalance — single vs poly mixing weight"
        ))

    candidates.append((
        "p_amp × log(cn_am)",
        p_amp * np.log(np.maximum(cn_am, 1e-3)),
        "composition-gated CN (if AM_P inherently lower CN)"
    ))

    print(f"  {'term':30s}  {'LOOCV':>7s}  {'Δ':>7s}  {'β':>9s}  status")
    print(f"  {'─'*30}  {'─'*7}  {'─'*7}  {'─'*9}  {'─'*30}")

    results = []
    for label, vec, meaning in candidates:
        # Skip if all zeros or constant
        if vec is None or len(vec) == 0:
            continue
        if (np.std(vec) < 1e-9) or (~np.isfinite(vec)).all():
            print(f"  {label:30s}  {'—':>7s}  {'—':>7s}  {'—':>9s}  ❌ no variation")
            continue
        # Sanitize
        vec_c = np.where(np.isfinite(vec), vec, 0.0)
        # Log-transform if all-positive AND spans >5×
        if (vec_c > 0).all() and vec_c.max() / max(vec_c.min(), 1e-12) > 5:
            vt = np.log(np.maximum(vec_c, 1e-12))
        else:
            vt = vec_c
        # Add to Stage 12 design as column 7
        X_ext = np.column_stack([X_base, vt])
        Xek = X_ext[keep]; yek = y_base[keep]
        coef_e, r2_e, lo_e = fit_and_loocv(Xek, yek)
        delta = lo_e - lo_b
        beta = coef_e[-1]
        if delta > 0.01:
            tag = "★★ STRONG ADD"
        elif delta > 0.005:
            tag = "★ marginal add"
        elif delta > 0:
            tag = "  ≈ noise"
        else:
            tag = "  ✗ no help"
        results.append((label, lo_e, delta, beta, meaning, tag))
        print(f"  {label:30s}  {lo_e:7.4f}  {delta:+7.4f}  {beta:+9.3f}  {tag}")

    print()

    # ───── Verdict ─────
    print("=" * 78)
    print(" VERDICT")
    print("=" * 78)
    results.sort(key=lambda r: -r[2])
    strong = [r for r in results if r[2] > 0.01]
    marginal = [r for r in results if 0.005 < r[2] <= 0.01]
    print(f"  Stage 12 (a=4) baseline LOOCV: {lo_b:.4f}")
    print(f"  Strong improvements (Δ > +0.01): {len(strong)}")
    for r in strong:
        print(f"     ★★ {r[0]}: LOOCV {r[1]:.4f} (Δ={r[2]:+.4f}), β={r[3]:+.3f}")
        print(f"        physics: {r[4]}")
    print(f"  Marginal improvements (+0.005..+0.01): {len(marginal)}")
    for r in marginal:
        print(f"     ★ {r[0]}: LOOCV {r[1]:.4f} (Δ={r[2]:+.4f}), β={r[3]:+.3f}")
        print(f"        physics: {r[4]}")
    print()
    if not strong and not marginal:
        print(f"  → NO additional term improves over Stage 12 (a=4) by Δ > +0.005.")
        print(f"    Form is at info-theoretic ceiling for current corpus.")
        print(f"    Stage 12 with a=4 is PRODUCTION-READY as σ_electronic final form.")
    elif strong:
        print(f"  → {len(strong)} STRONG candidate(s) found.  Consider Stage 15:")
        print(f"    add top candidate to base, lock its exponent, refit.")
    else:
        print(f"  → Only marginal candidates.  Worth ablation on production data")
        print(f"    but NOT decisive enough to add new DoF.")

    # ───── Best-2 combo if any strong ─────
    if len(results) >= 2 and results[0][2] > 0.005 and results[1][2] > 0.005:
        print()
        print(f"  Trying best-2 combo: {results[0][0]} + {results[1][0]}")
        # Re-collect vectors
        def get_vec(label):
            for label_, vec, _ in candidates:
                if label_ == label:
                    vec_c = np.where(np.isfinite(vec), vec, 0.0)
                    if (vec_c > 0).all() and vec_c.max()/max(vec_c.min(), 1e-12) > 5:
                        return np.log(np.maximum(vec_c, 1e-12))
                    return vec_c
            return None
        v1 = get_vec(results[0][0]); v2 = get_vec(results[1][0])
        X_ext2 = np.column_stack([X_base, v1, v2])
        Xek2 = X_ext2[keep]; yek2 = y_base[keep]
        coef_2, r2_2, lo_2 = fit_and_loocv(Xek2, yek2)
        print(f"    LOOCV = {lo_2:.4f}  (Δ vs baseline = {lo_2-lo_b:+.4f})")
        print(f"    β1 = {coef_2[-2]:+.3f}, β2 = {coef_2[-1]:+.3f}")
        if lo_2 > max(results[0][1], results[1][1]) + 0.003:
            print(f"    ★ combo > either alone — both terms carry independent info")
        else:
            print(f"    ≈ combo ≤ best individual — terms are collinear, pick one")


if __name__ == '__main__':
    main()
