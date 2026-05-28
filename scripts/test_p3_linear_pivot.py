#!/usr/bin/env python3
"""Test P2 → P3 linear-pivot swap to fix the bidirectional 0:10·SE-rich
corner bias (r_SE=0.5 OVER-prediction vs r_SE≥1.0 UNDER-prediction).

CURRENT (T1 production):
    P2  = g_phys · (φ − 0.195)² · (r_SE − 0.5)+    [zero at r_SE=0.5]
    extras = [P2, log f_intact]
    LOOCV ≈ 0.971  (5 live params: a,b,c,β_P2,β_F)

PROPOSED:
    P3  = g_phys · (φ − 0.195)² · (r_SE − r0)      [SIGNED linear, pivots at r0]
    extras = [P3, log f_intact]
    Same param count.  At r_SE < r0 → P3<0 (form pulls DOWN), at r_SE > r0 → P3>0
    (form pulls UP).  β_P3 fits BOTH sides with one coefficient.

TESTS PER r0 ∈ {0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2}:
  1. Full LOOCV (n=90 minus excluded)
  2. Corner-only |err| stats (0:10 ∧ φ>0.30 cases)
  3. Leave-corner-out: fit on bulk, predict corner → bulk-RMSE vs corner-RMSE
     (passes if β_P3 sign-consistent between bulk-only and full-fit,
      AND corner RMSE drops vs T1)

REFERENCE: T1 production (P2) measured on same fold scheme for apples-to-apples.

ALSO: brief Cronau-sharpening probe (independent of P2/P3) — sharpen the
mid-plateau values to see if D0.25 / S-series 72:28 over-prediction is
better explained by a steeper sub-µm Cronau curve.

Run from repo root:
    python3 scripts/test_p3_linear_pivot.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from nested_cv_sat import (load_corpus, base_log_sat, cronau_factor,
                           cblend_fit, cblend_pred, loocv_r2, _g_phys_smooth,
                           PHICP_F, PHICS_F, DELTA_F, PHIC_PROD)


def p3_feature(a, r0, g_gate=None):
    """Linear-pivot P3: g_phys · (φ−0.195)² · (r_SE − r0).
    Signed: negative at r_SE<r0 (pulls form DOWN), positive at r_SE>r0 (UP)."""
    phi = a[:, 0]; r_SE = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    r_safe = np.where(np.isfinite(r_SE) & (r_SE > 0), r_SE, r0)  # neutral at pivot
    p3 = pex**2 * (r_safe - r0)
    if g_gate is not None:
        p3 = g_gate * p3
    return p3


def p2_feature_local(a, g_gate=None):
    """Current production P2 = g_phys · (φ−0.195)² · (r_SE − 0.5)+."""
    phi = a[:, 0]; r_SE = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    r_safe = np.where(np.isfinite(r_SE) & (r_SE > 0), r_SE, 0.5)
    rse_hi = np.maximum(r_safe - 0.5, 0.0)
    p2 = pex**2 * rse_hi
    if g_gate is not None:
        p2 = g_gate * p2
    return p2


def _f_intact_log(a):
    return a[:, 19] if a.shape[1] >= 20 else np.zeros(a.shape[0])


def _corner_mask(a):
    """0:10 SE-rich corner: AM_P fraction < 0.05 AND φ > 0.30."""
    return (a[:, 6] < 0.05) & (a[:, 0] > 0.30)


def _err_pct(pred_log, logsf):
    return (np.exp(pred_log) - np.exp(logsf)) / np.exp(logsf) * 100.0


def fit_predict_full(base, logsf, taus, extras):
    """Full-corpus fit, return (b, pred_log)."""
    b = cblend_fit(base, logsf, taus, extras=extras)
    pred = cblend_pred(base, taus, b, extras=extras)
    return b, pred


def leave_corner_out(base, logsf, taus, extras, mask):
    """Fit on bulk (~mask), predict corner — measure how well the form
    generalizes ONTO the corner without using corner data.
    Returns (β_bulk, β_full, corner_pred_log, corner_actual_log).
    PASS condition: sign(β_bulk) == sign(β_full)  AND  corner_RMSE finite (<0.4)."""
    bulk = ~mask
    if bulk.sum() < 10:
        return None, None, None, None
    extras_bulk = [e[bulk] for e in extras]
    extras_corner = [e[mask] for e in extras]
    b_bulk = cblend_fit(base[bulk], logsf[bulk], taus[bulk], extras=extras_bulk)
    b_full = cblend_fit(base, logsf, taus, extras=extras)
    pred_corner = cblend_pred(base[mask], taus[mask], b_bulk, extras=extras_corner)
    return b_bulk, b_full, pred_corner, logsf[mask]


def _rmse(a, b):
    return float(np.sqrt(np.mean((a - b)**2)))


def main():
    print("=" * 78)
    print(" P2 → P3 LINEAR-PIVOT SCAN — fix bidirectional 0:10·SE-rich bias")
    print("=" * 78)
    a = load_corpus()
    n = len(a)
    print(f"Corpus n = {n}")
    if n < 8 or a.ndim < 2:
        print("[ABORT] corpus too small (need ≥8 cases with full_metrics.json).")
        print("        Run from repo ROOT on the WSL machine where webapp/results/")
        print("        and webapp/archive/ have the 90-case dataset.")
        return
    logsf = np.log(a[:, 5]); taus = a[:, 4]

    # Base = SAT-blend × Cronau (current T1 base, no extras)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    g_phys = _g_phys_smooth(a)
    fi_log = _f_intact_log(a)

    corner = _corner_mask(a)
    n_corner = corner.sum()
    print(f"0:10·SE-rich corner cases: {n_corner} / {n}")
    print()

    # ───── 1. Reference: T1 production (P2) ─────
    p2 = p2_feature_local(a, g_gate=g_phys)
    extras_t1 = [p2, fi_log]
    lo_t1 = loocv_r2(base, logsf, taus, extras=extras_t1)
    b_t1, pred_t1 = fit_predict_full(base, logsf, taus, extras_t1)
    err_t1 = _err_pct(pred_t1, logsf)
    corner_rmse_t1 = _rmse(pred_t1[corner], logsf[corner])
    bulk_rmse_t1 = _rmse(pred_t1[~corner], logsf[~corner])
    b_bulk_t1, b_full_t1, pcorn_t1, _ = leave_corner_out(base, logsf, taus,
                                                          extras_t1, corner)
    lco_rmse_t1 = _rmse(pcorn_t1, logsf[corner]) if pcorn_t1 is not None else np.nan
    sign_t1 = "match" if (np.sign(b_bulk_t1[3]) == np.sign(b_full_t1[3])) else "FLIP"

    print("─" * 78)
    print(" REFERENCE: T1 production (P2 = g_phys·(φ−0.195)²·(r_SE−0.5)+)")
    print("─" * 78)
    print(f"  LOOCV              : {lo_t1:.4f}")
    print(f"  Corner RMSE (in-sample) : {corner_rmse_t1:.4f}")
    print(f"  Bulk   RMSE (in-sample) : {bulk_rmse_t1:.4f}")
    print(f"  Leave-corner-out RMSE   : {lco_rmse_t1:.4f}")
    print(f"  β_P2 bulk-only / full   : {b_bulk_t1[3]:+.3f} / {b_full_t1[3]:+.3f}  "
          f"[sign {sign_t1}]")
    print(f"  Corner |err%| cases     :")
    for i in np.where(corner)[0]:
        print(f"     phi={a[i,0]:.3f}  CN={a[i,1]:.2f}  r_SE={a[i,8]:.2f}  "
              f"σ_act={a[i,5]:.4f}  err={err_t1[i]:+6.1f}%")
    print()

    # ───── 2. P3 pivot scan ─────
    print("─" * 78)
    print(" P3 SCAN: P3 = g_phys · (φ−0.195)² · (r_SE − r0)  [signed linear]")
    print("─" * 78)
    print(f"  {'r0':>5s}  {'LOOCV':>7s}  {'ΔLOOCV':>8s}   "
          f"{'in-corn RMSE':>13s}  {'in-bulk RMSE':>13s}   "
          f"{'LCO RMSE':>9s}   {'β_P3 bulk':>10s}  {'β_P3 full':>10s}  {'sign':>5s}")
    print("─" * 78)
    results = []
    for r0 in [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]:
        p3 = p3_feature(a, r0, g_gate=g_phys)
        extras = [p3, fi_log]
        lo = loocv_r2(base, logsf, taus, extras=extras)
        b_f, pred = fit_predict_full(base, logsf, taus, extras)
        crmse = _rmse(pred[corner], logsf[corner])
        brmse = _rmse(pred[~corner], logsf[~corner])
        b_b, b_full, pcorn, _ = leave_corner_out(base, logsf, taus, extras, corner)
        lco = _rmse(pcorn, logsf[corner]) if pcorn is not None else np.nan
        sg = "match" if (np.sign(b_b[3]) == np.sign(b_full[3])) else "FLIP"
        results.append((r0, lo, crmse, brmse, lco, b_b[3], b_full[3], sg))
        print(f"  {r0:5.1f}  {lo:7.4f}  {lo-lo_t1:+8.4f}   "
              f"{crmse:13.4f}  {brmse:13.4f}   {lco:9.4f}   "
              f"{b_b[3]:+10.3f}  {b_full[3]:+10.3f}  {sg:>5s}")
    print()

    # ───── 3. Per-case error on best P3 candidate ─────
    best = max(results, key=lambda r: r[1])
    print(f"Best P3 by full LOOCV: r0={best[0]:.1f}  LOOCV={best[1]:.4f}  "
          f"ΔLOOCV={best[1]-lo_t1:+.4f}  sign={best[7]}")
    print()
    p3_best = p3_feature(a, best[0], g_gate=g_phys)
    extras_best = [p3_best, fi_log]
    b_best, pred_best = fit_predict_full(base, logsf, taus, extras_best)
    err_best = _err_pct(pred_best, logsf)
    print(f"  Corner |err%| with P3 (r0={best[0]:.1f}):")
    for i in np.where(corner)[0]:
        delta = abs(err_best[i]) - abs(err_t1[i])
        flag = "  ↓ improved" if delta < -2 else ("  ↑ worse" if delta > 2 else "  ≈")
        print(f"     phi={a[i,0]:.3f}  CN={a[i,1]:.2f}  r_SE={a[i,8]:.2f}  "
              f"σ_act={a[i,5]:.4f}  err={err_best[i]:+6.1f}%   "
              f"(T1 was {err_t1[i]:+6.1f}%){flag}")
    print()

    # ───── 4. Cronau sharpening probe (independent of P2/P3) ─────
    print("─" * 78)
    print(" CRONAU SHARPENING PROBE (independent of P2/P3)")
    print("─" * 78)
    print("  Test: sharpen Cronau mid plateaus by scaling (1, 0.90, 0.65, 0.33)")
    print("        → (1, 0.85, 0.55, 0.25) — steeper sub-µm drop-off.")
    print()

    def cronau_sharp(rse_um):
        """Sharpened: plateaus at r→∞=1.00, r=0.4=0.85, r=0.2=0.55, r→0=0.25.
        Smooth-3-sigmoid form: 0.25 + 0.30·σ(K(r−0.10)) + 0.30·σ(K(r−0.30))
                                + 0.15·σ(K(r−0.50))."""
        r = np.asarray(rse_um, float)
        K = 50.0
        f = (0.25
             + 0.30 / (1.0 + np.exp(-K*(r - 0.10)))
             + 0.30 / (1.0 + np.exp(-K*(r - 0.30)))
             + 0.15 / (1.0 + np.exp(-K*(r - 0.50))))
        return np.where(np.isfinite(r) & (r > 0), f, 1.0)

    base_sharp = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_sharp(a[:, 8]))
    # Re-fit with sharpened Cronau + current P2
    p2_s = p2_feature_local(a, g_gate=g_phys)
    extras_s = [p2_s, fi_log]
    lo_sharp = loocv_r2(base_sharp, logsf, taus, extras=extras_s)
    b_s, pred_s = fit_predict_full(base_sharp, logsf, taus, extras_s)
    err_s = _err_pct(pred_s, logsf)
    crmse_s = _rmse(pred_s[corner], logsf[corner])
    print(f"  T1 (current Cronau)      LOOCV={lo_t1:.4f}  corner-RMSE={corner_rmse_t1:.4f}")
    print(f"  T1 + sharpened Cronau    LOOCV={lo_sharp:.4f}  corner-RMSE={crmse_s:.4f}  "
          f"ΔLOOCV={lo_sharp-lo_t1:+.4f}")
    # Also report D0.25 / S-series 72:28 cases specifically
    print()
    print("  72:28 / sub-µm r_SE per-case error (T1 vs sharpened Cronau):")
    # rough proxy: phi in 0.25-0.32 range (72:28 ish), small r_SE
    sample_mask = (a[:, 0] > 0.22) & (a[:, 0] < 0.33) & (a[:, 6] < 0.05) & (a[:, 8] < 0.6)
    if sample_mask.any():
        for i in np.where(sample_mask)[0]:
            print(f"     phi={a[i,0]:.3f}  r_SE={a[i,8]:.2f}  "
                  f"σ_act={a[i,5]:.4f}   T1 err={err_t1[i]:+6.1f}%   "
                  f"sharp err={err_s[i]:+6.1f}%")
    else:
        print("     (no cases match D0.25-like filter)")
    print()

    # ───── 5. VERDICT ─────
    print("=" * 78)
    print(" VERDICT")
    print("=" * 78)
    best_delta = best[1] - lo_t1
    noise_se = 0.0016
    print(f"  noise SE (LOOCV)         : ±{noise_se:.4f}")
    print(f"  Best P3 ΔLOOCV vs T1     : {best_delta:+.4f}  "
          f"({'above' if best_delta > noise_se else 'below'} noise)")
    print(f"  Best P3 sign consistency : {best[7]} "
          f"({'PASS' if best[7] == 'match' else 'FAIL'})")
    print(f"  Best P3 corner-RMSE      : {best[2]:.4f}  "
          f"(T1 was {corner_rmse_t1:.4f})")
    print(f"  Best P3 LCO-RMSE         : {best[4]:.4f}  "
          f"(T1 was {lco_rmse_t1:.4f})")
    print(f"  Cronau-sharp ΔLOOCV      : {lo_sharp-lo_t1:+.4f}  "
          f"({'above' if (lo_sharp-lo_t1) > noise_se else 'below'} noise)")
    print()
    if best_delta > noise_se and best[7] == 'match' and best[4] < lco_rmse_t1:
        print(f"  → P3 (r0={best[0]:.1f}) PASSES — recommend adoption.")
    elif lo_sharp - lo_t1 > noise_se:
        print(f"  → Cronau sharpening PASSES — recommend adoption (literature-check needed).")
    else:
        print(f"  → Neither alternative meaningfully improves over T1.")
        print(f"     Remaining bias is data-limited — multi-seed sim is the path.")


if __name__ == '__main__':
    main()
